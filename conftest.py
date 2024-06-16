# conftest.py

import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookstore.settings')

django.setup()
