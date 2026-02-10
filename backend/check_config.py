import os
import sys
import django

sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chemical_visualizer.settings')
django.setup()

from django.conf import settings

print("=== CORS Settings ===")
print(f"CORS_ALLOWED_ORIGINS: {getattr(settings, 'CORS_ALLOWED_ORIGINS', 'NOT SET')}")
print(f"CORS_ALLOW_ALL_ORIGINS: {getattr(settings, 'CORS_ALLOW_ALL_ORIGINS', 'NOT SET')}")
print(f"\n=== Installed Apps ===")
if 'corsheaders' in settings.INSTALLED_APPS:
    print("✅ corsheaders is installed")
else:
    print("❌ corsheaders is NOT installed")
    
print(f"\n=== Middleware ===")
middleware = settings.MIDDLEWARE
if any('cors' in m.lower() for m in middleware):
    print("✅ CORS middleware is configured")
else:
    print("❌ CORS middleware is MISSING")