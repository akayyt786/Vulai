from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

# Special development-only settings
# e.g., enabling browsable API renderer
REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] += [
    'rest_framework.renderers.BrowsableAPIRenderer',
]
