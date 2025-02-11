#!/usr/bin/env python
"""
Django's command-line utility for administrative tasks.

This script allows you to interact with the Django project by running commands such as running the development server, 
applying database migrations, and creating superusers. It sets up the appropriate environment and delegates 
commands to Django's management utilities.

Usage:
    python manage.py <command> [options]

Example:
    python manage.py runserver         # Start the development server to view the project
    python manage.py migrate           # Apply database migrations
    python manage.py createsuperuser   # Create an admin user
"""

import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GTMovies.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
