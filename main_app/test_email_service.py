
import os
import sys
import traceback

from flask import Flask
from flask_mail import Mail, Message
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

# ============================================================
# Configuration
# ============================================================

ENV_FILE = "/opt/journal_project/.env"

# Change this to the email address where you want the test email.
TEST_EMAIL = "shahf8604@gmail.com"


# ============================================================
# Helpers
# ============================================================

def mask_value(value):
    """Hide sensitive values when displaying configuration."""
    if not value:
        return "<EMPTY>"

    if len(value) <= 4:
        return "****"

    return value[:2] + "****" + value[-2:]


def load_environment():
    """
    Load .env and provide clear error messages.
    """

    print("\n========================================")
    print("1. Loading Environment")
    print("========================================")

    if not os.path.exists(ENV_FILE):
        print(f"ERROR: .env file was not found.")
        print(f"Expected location: {ENV_FILE}")
        return False

    if not os.path.isfile(ENV_FILE):
        print(f"ERROR: {ENV_FILE} exists but is not a regular file.")
        return False

    if not os.access(ENV_FILE, os.R_OK):
        print(f"ERROR: Permission denied while reading {ENV_FILE}")
        print("The current user does not have permission to read the .env file.")
        return False

    try:
        # Load the .env file into os.environ
        loaded = load_dotenv(
            dotenv_path=ENV_FILE,
            override=False
        )

        if not loaded:
            print("WARNING: .env file was found, but no variables were loaded.")
            print("Check whether the file contains valid KEY=VALUE entries.")
            return False

        print(f"SUCCESS: Environment loaded from {ENV_FILE}")
        return True

    except PermissionError:
        print(f"ERROR: Permission denied while loading {ENV_FILE}")
        print("Check the file and parent-directory permissions.")
        return False

    except UnicodeDecodeError:
        print(f"ERROR: Unable to read {ENV_FILE} because of an encoding problem.")
        print("Make sure the .env file is saved as UTF-8.")
        return False

    except Exception as e:
        print(f"ERROR: Unexpected error while loading .env")
        print(f"Details: {type(e).__name__}: {e}")
        return False


def check_variables():
    """
    Check required mail environment variables.
    """

    print("\n========================================")
    print("2. Checking Environment Variables")
    print("========================================")

    required_variables = {
        "MAIL_SERVER": "SMTP server hostname",
        "MAIL_PORT": "SMTP server port",
        "MAIL_USERNAME": "SMTP username/email",
        "MAIL_PASSWORD": "SMTP password",
        "MAIL_USE_TLS": "TLS setting",
    }

    missing = []

    for variable, description in required_variables.items():
        value = os.getenv(variable)

        if value is None:
            print(f"ERROR: {variable} is missing")
            print(f"       Expected: {description}")
            missing.append(variable)
            continue

        if value.strip() == "":
            print(f"ERROR: {variable} is empty")
            print(f"       Expected: {description}")
            missing.append(variable)
            continue

        # Never display the password.
        if variable == "MAIL_PASSWORD":
            print(f"OK: {variable} = ********")
        else:
            print(f"OK: {variable} = {value}")

    if missing:
        print("\nERROR: Required environment variables are missing:")
        for variable in missing:
            print(f"  - {variable}")

        print("\nPlease check:")
        print("  1. /opt/journal_project/.env exists")
        print("  2. Variable names are correct")
        print("  3. There are no accidental spaces or invalid entries")

        return False

    return True


def validate_mail_configuration():
    """
    Validate SMTP configuration before trying to send.
    """

    print("\n========================================")
    print("3. Validating Mail Configuration")
    print("========================================")

    try:
        server = os.getenv("MAIL_SERVER")
        port = os.getenv("MAIL_PORT")
        username = os.getenv("MAIL_USERNAME")
        password = os.getenv("MAIL_PASSWORD")
        use_tls = os.getenv("MAIL_USE_TLS")

        # Validate port
        try:
            port = int(port)
        except (TypeError, ValueError):
            print(f"ERROR: MAIL_PORT must be a number.")
            print(f"Current value: {port}")
            return False

        if port < 1 or port > 65535:
            print(f"ERROR: MAIL_PORT must be between 1 and 65535.")
            print(f"Current value: {port}")
            return False

        # Validate TLS
        if use_tls.lower() not in ("true", "false", "1", "0", "yes", "no"):
            print("ERROR: MAIL_USE_TLS must be True or False.")
            print(f"Current value: {use_tls}")
            return False

        print(f"SMTP Server : {server}")
        print(f"SMTP Port   : {port}")
        print(f"SMTP User   : {mask_value(username)}")
        print(f"SMTP TLS    : {use_tls}")
        print("SMTP Password: ********")

        print("\nSUCCESS: Mail configuration looks valid.")
        return True

    except Exception as e:
        print("ERROR: Failed while validating mail configuration.")
        print(f"Details: {type(e).__name__}: {e}")
        return False


def send_test_email():
    """
    Create a Flask application using the loaded configuration
    and send a test email.
    """

    print("\n========================================")
    print("4. Testing SMTP / Sending Email")
    print("========================================")

    try:
        # Create a small Flask application specifically for testing.
        app = Flask(__name__)

        # Flask-Mail configuration
        app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER")
        app.config["MAIL_PORT"] = int(os.getenv("MAIL_PORT"))
        app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
        app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")

        app.config["MAIL_USE_TLS"] = (
            os.getenv("MAIL_USE_TLS", "False").lower()
            in ("true", "1", "yes")
        )

        app.config["MAIL_USE_SSL"] = (
            os.getenv("MAIL_USE_SSL", "False").lower()
            in ("true", "1", "yes")
        )

        app.config["MAIL_DEFAULT_SENDER"] = (
            os.getenv("MAIL_DEFAULT_SENDER")
            or os.getenv("MAIL_USERNAME")
        )

        mail = Mail(app)

        with app.app_context():

            msg = Message(
                subject="Email Verification Code - Curevita Research",
                recipients=[TEST_EMAIL],
            )

            msg.body = """Hello,

            This is a test email from the Curevita Research production server.

            If you received this email, the SMTP configuration is working correctly.

            Thank you,
            Curevita Research Team
            """

            print(f"Sending test email to: {TEST_EMAIL}")

            mail.send(msg)

        print("\nSUCCESS: Email sent successfully.")
        print(f"Check the inbox for: {TEST_EMAIL}")

        return True

    except ConnectionRefusedError:
        print("\nERROR: SMTP connection was refused.")
        print("Possible causes:")
        print("  - Wrong MAIL_SERVER")
        print("  - Wrong MAIL_PORT")
        print("  - SMTP server is blocking the connection")
        print("  - AWS/security-group/firewall restriction")

        return False

    except TimeoutError:
        print("\nERROR: SMTP connection timed out.")
        print("Possible causes:")
        print("  - Wrong SMTP server or port")
        print("  - Firewall/security-group blocking SMTP")
        print("  - SMTP server is unreachable")

        return False

    except PermissionError:
        print("\nERROR: Permission denied.")
        print("Check that the current Linux user can access the application files.")

        return False

    except Exception as e:
        error_type = type(e).__name__
        error_message = str(e)

        print("\nERROR: Failed to send email.")
        print(f"Error type: {error_type}")
        print(f"Error: {error_message}")

        print("\nPossible causes:")

        if "authentication" in error_message.lower():
            print("  - SMTP username/password is incorrect")
            print("  - SMTP authentication is disabled")
            print("  - Gmail/app password configuration is incorrect")

        elif "connection" in error_message.lower():
            print("  - SMTP server is unreachable")
            print("  - Incorrect MAIL_SERVER or MAIL_PORT")
            print("  - Firewall/security group is blocking SMTP")

        elif "tls" in error_message.lower() or "ssl" in error_message.lower():
            print("  - TLS/SSL configuration is incorrect")
            print("  - Check MAIL_USE_TLS and MAIL_USE_SSL")

        else:
            print("  - Check SMTP configuration")
            print("  - Check SMTP credentials")
            print("  - Check firewall/security-group rules")
            print("  - Check the full traceback below")

        print("\nFull technical error:")
        traceback.print_exc()

        return False


# ============================================================
# Main
# ============================================================

def main():

    print("\n")
    print("============================================")
    print(" Curevita Research - Production Mail Test")
    print("============================================")

    print(f"Running user: {os.getenv('USER', 'unknown')}")
    print(f"Working directory: {os.getcwd()}")
    print(f"Python: {sys.executable}")
    print(f".env file: {ENV_FILE}")

    # --------------------------------------------------------
    # Step 1 - Load .env
    # --------------------------------------------------------

    if not load_environment():
        print("\nMAIL TEST FAILED")
        print("Reason: Could not load environment variables.")
        sys.exit(1)

    # --------------------------------------------------------
    # Step 2 - Check variables
    # --------------------------------------------------------

    if not check_variables():
        print("\nMAIL TEST FAILED")
        print("Reason: Required environment variables are missing.")
        sys.exit(1)

    # --------------------------------------------------------
    # Step 3 - Validate configuration
    # --------------------------------------------------------

    if not validate_mail_configuration():
        print("\nMAIL TEST FAILED")
        print("Reason: Mail configuration is invalid.")
        sys.exit(1)

    # --------------------------------------------------------
    # Step 4 - Send test email
    # --------------------------------------------------------

    if not send_test_email():
        print("\nMAIL TEST FAILED")
        print("Reason: Email could not be sent.")
        sys.exit(1)

    # --------------------------------------------------------
    # Success
    # --------------------------------------------------------

    print("\n")
    print("============================================")
    print(" MAIL TEST PASSED")
    print("============================================")
    print("Environment loading : OK")
    print("Variable validation  : OK")
    print("SMTP configuration   : OK")
    print("Email sending        : OK")
    print("============================================")


if __name__ == "__main__":
    main()
