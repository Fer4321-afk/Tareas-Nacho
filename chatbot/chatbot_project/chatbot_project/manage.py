# manage.py (en Asignatura_Nacho/)
#!/usr/bin/env python
import os
import sys

def main():
    """Run administrative tasks."""
    # IMPORTANTE: Apuntar a ChatBOTProject.settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatbot_project.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()