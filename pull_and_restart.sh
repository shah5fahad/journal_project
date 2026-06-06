#!/bin/bash

set -euo pipefail

###########################################
# CONFIGURATION
###########################################

APP_NAME="journal_project"
APP_DIR="/opt/$APP_NAME"
BRANCH="main"

###########################################
# HELPERS
###########################################

log() { echo ""; echo ">>> $*"; }

###########################################
# PULL LATEST CODE
###########################################

log "Pulling latest code from branch '$BRANCH'..."

cd "$APP_DIR"
git fetch origin
git reset --hard "origin/$BRANCH"

###########################################
# UPDATE PYTHON DEPENDENCIES
###########################################

log "Updating Python dependencies..."

"$APP_DIR/venv/bin/pip" install --upgrade pip wheel setuptools

if [ -f "$APP_DIR/requirements.txt" ]; then
    "$APP_DIR/venv/bin/pip" install -r "$APP_DIR/requirements.txt"
fi

###########################################
# RESTART GUNICORN
###########################################

log "Restarting gunicorn service..."

sudo systemctl restart "${APP_NAME}"

###########################################
# RELOAD NGINX
###########################################

log "Testing and reloading nginx..."

sudo nginx -t
sudo systemctl reload nginx

###########################################
# STATUS
###########################################

echo ""
echo "======================================"
echo "Redeploy Complete"
echo "======================================"
echo ""
echo "Service status:"
sudo systemctl status "${APP_NAME}" --no-pager
echo ""
echo "Nginx status:"
sudo systemctl status nginx --no-pager