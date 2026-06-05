#!/bin/bash

set -euo pipefail

###########################################
# CONFIGURATION
###########################################

APP_NAME="journal_project"
APP_USER="ubuntu"

DOMAIN="curevitajournals.com"
EMAIL="infocvrb@curevita.org"

GIT_REPO="https://github.com/shah5fahad/journal_project"
BRANCH="main"

APP_DIR="/opt/$APP_NAME"

APP_MODULE="app:app"

# Marker files — each section writes one so it is skipped on re-runs
MARKER_DIR="$APP_DIR/.deploy_markers"

###########################################
# HELPERS
###########################################

# Usage: marker_done  <name>   — returns 0 if marker exists, 1 if not
marker_done() { [ -f "$MARKER_DIR/$1" ]; }

# Usage: mark <name>
mark() { mkdir -p "$MARKER_DIR" && touch "$MARKER_DIR/$1"; }

log() { echo ""; echo ">>> $*"; }

###########################################
# SYSTEM UPDATE
###########################################

if ! marker_done "system_update"; then
    log "Updating system..."
    sudo apt-get update -y
    sudo apt-get upgrade -y
    mark "system_update"
else
    log "System update already done — skipping."
fi

###########################################
# INSTALL PACKAGES
###########################################

if ! marker_done "packages"; then
    log "Installing dependencies..."
    sudo apt-get install -y \
        python3 \
        python3-pip \
        python3-venv \
        nginx \
        git \
        certbot \
        python3-certbot-nginx \
        build-essential
    mark "packages"
else
    log "Packages already installed — skipping."
fi

###########################################
# CREATE APPLICATION DIRECTORY
###########################################

if ! marker_done "app_dir"; then
    log "Creating app directory..."
    sudo mkdir -p "$APP_DIR"
    sudo chown -R "$APP_USER:$APP_USER" "$APP_DIR"
    mark "app_dir"
else
    log "App directory already exists — skipping."
fi

# Ensure marker dir is always available (needed even on re-runs)
mkdir -p "$MARKER_DIR"

###########################################
# CLONE OR UPDATE REPOSITORY
###########################################

# FIX: Always pull latest code on every run (intentional — deploys new code).
#      We don't gate this behind a marker so re-running the script deploys
#      whatever is on the branch at that moment.
log "Fetching source code..."

if [ -d "$APP_DIR/.git" ]; then
    cd "$APP_DIR"
    git fetch origin
    git reset --hard "origin/$BRANCH"
else
    # FIX: removed bare `rm -rf $APP_DIR/*` that would wipe marker files;
    #      use a temp clone then move instead.
    TMPDIR_CLONE=$(mktemp -d)
    git clone -b "$BRANCH" "$GIT_REPO" "$TMPDIR_CLONE"
    # Move repo contents into APP_DIR, preserving the marker directory
    shopt -s dotglob
    mv "$TMPDIR_CLONE"/* "$APP_DIR"/
    shopt -u dotglob
    rm -rf "$TMPDIR_CLONE"
fi

###########################################
# PYTHON VENV
###########################################

if ! marker_done "venv"; then
    log "Creating virtual environment..."
    cd "$APP_DIR"
    python3 -m venv venv
    mark "venv"
else
    log "Virtual environment already exists — skipping creation."
fi

log "Installing/updating Python packages..."
cd "$APP_DIR"
# FIX: always activate with full path — `source` on a path with spaces is fragile;
#      use the direct binary path instead.
"$APP_DIR/venv/bin/pip" install --upgrade pip wheel setuptools

if [ -f "$APP_DIR/requirements.txt" ]; then
    "$APP_DIR/venv/bin/pip" install -r "$APP_DIR/requirements.txt"
fi

"$APP_DIR/venv/bin/pip" install gunicorn

###########################################
# GUNICORN SYSTEMD SERVICE
###########################################

if ! marker_done "systemd_service"; then
    log "Creating systemd service..."

    sudo tee /etc/systemd/system/${APP_NAME}.service > /dev/null <<EOF
[Unit]
Description=Gunicorn service for ${APP_NAME}
After=network.target

[Service]
User=${APP_USER}
Group=www-data

WorkingDirectory=${APP_DIR}

Environment="PATH=${APP_DIR}/venv/bin"

ExecStart=${APP_DIR}/venv/bin/gunicorn \\
    --workers 4 \\
    --bind unix:${APP_DIR}/${APP_NAME}.sock \\
    ${APP_MODULE}

Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

    sudo systemctl daemon-reload
    sudo systemctl enable "${APP_NAME}"
    mark "systemd_service"
else
    log "Systemd service already configured — reloading daemon only."
    sudo systemctl daemon-reload
fi

# FIX: Always restart gunicorn so new code is picked up on every deploy.
log "Restarting gunicorn service..."
sudo systemctl restart "${APP_NAME}"

###########################################
# ONE-TIME DATA SEED
###########################################

# FIX: kept original marker logic; moved marker file inside MARKER_DIR
#      for consistency. Also fixed: original script called `source venv/bin/activate`
#      inside an `if` block but $APP_DIR/venv/bin/python is used directly below
#      to avoid subshell activation issues.
if ! marker_done "data_seed"; then
    log "First deployment detected. Running data seed scripts..."

    SCRIPTS=(
        "insert_journal_master.py"
        "insert_contact_detail.py"
        "insert_editor_boards.py"
        "insert_research_papers.py"
    )

    for script in "${SCRIPTS[@]}"; do
        log "Running $script ..."
        # FIX: use full venv python path instead of relying on `source activate`
        "$APP_DIR/venv/bin/python" "$APP_DIR/single_run_scripts/$script"
    done

    mark "data_seed"
    log "Data initialization completed."
else
    log "Data seed already executed previously — skipping."
fi

###########################################
# NGINX CONFIG
###########################################

if ! marker_done "nginx_config"; then
    log "Creating nginx config..."

    sudo tee /etc/nginx/sites-available/${APP_NAME} > /dev/null <<EOF
server {
    listen 80;
    server_name ${DOMAIN};

    client_max_body_size 100M;

    location / {
        include proxy_params;
        proxy_pass http://unix:${APP_DIR}/${APP_NAME}.sock;
    }
}
EOF

    # FIX: only symlink if it doesn't already exist (ln -sf is safe but
    #      being explicit avoids misleading log output)
    sudo ln -sf \
        /etc/nginx/sites-available/${APP_NAME} \
        /etc/nginx/sites-enabled/${APP_NAME}

    sudo rm -f /etc/nginx/sites-enabled/default

    mark "nginx_config"
else
    log "Nginx config already created — skipping."
fi

# FIX: always test and reload nginx so any gunicorn socket changes take effect
log "Testing and reloading nginx..."
sudo nginx -t
sudo systemctl reload nginx

###########################################
# FIREWALL
###########################################

if ! marker_done "firewall"; then
    if command -v ufw >/dev/null 2>&1; then
        log "Configuring firewall..."
        sudo ufw allow OpenSSH
        sudo ufw allow 'Nginx Full'
        sudo ufw --force enable
    fi
    mark "firewall"
else
    log "Firewall already configured — skipping."
fi

###########################################
# SSL CERTIFICATE
###########################################

# FIX: check whether a certificate already exists before calling certbot,
#      which would fail or prompt interactively if the cert is still valid.
if ! marker_done "ssl"; then
    log "Generating SSL certificate..."
    sudo certbot \
        --nginx \
        --non-interactive \
        --agree-tos \
        -m "${EMAIL}" \
        -d "${DOMAIN}" \
        --redirect
    mark "ssl"
else
    log "SSL certificate already issued — skipping certbot run."
fi

###########################################
# CERTBOT AUTO-RENEWAL TIMER
###########################################

if ! marker_done "certbot_timer"; then
    log "Enabling certbot renewal timer..."
    sudo systemctl enable certbot.timer
    sudo systemctl start certbot.timer
    mark "certbot_timer"
else
    log "Certbot timer already enabled — skipping."
fi

###########################################
# STATUS
###########################################

echo ""
echo "======================================"
echo "Deployment Complete"
echo "======================================"
echo "Domain : https://${DOMAIN}"
echo ""
echo "Service status:"
sudo systemctl status "${APP_NAME}" --no-pager
echo ""
echo "Nginx status:"
sudo systemctl status nginx --no-pager