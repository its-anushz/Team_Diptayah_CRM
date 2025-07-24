#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CRMsystem.settings')
    try:
        from django.core.management import execute_from_command_line
    except ModuleNotFoundError as e:
        logger.critical(f"ModuleNotFoundError: {e}. Did you forget to install Django or activate the virtual environment?")
        raise e
    except ImportError as exc:
        logger.critical("Couldn't import Django. Are you sure it's installed and available on your PYTHONPATH?")
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    try:
        execute_from_command_line(sys.argv)
    except Exception as e:
        logger.exception(f"Unexpected error running Django command: {e}")
        raise e

if __name__ == '__main__':
    main()
