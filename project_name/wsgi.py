import os

from configurations.wsgi import get_wsgi_application

configuration = os.getenv('DJANGO_CONFIGURATION', 'Development')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{{ project_name }}.settings')
os.environ.setdefault('DJANGO_CONFIGURATION', configuration)

application = get_wsgi_application()
