from .base import *

DEBUG = False

ALLOWED_HOSTS = [
  'Lemon-dev.ap-northeast-2.elasticbeanstalk.com',
  '52.78.138.222',
  'lemon-bs.com',
  'www.lemon-bs.com',
  ]

# Media Files
# ---For Prod Env---
MEDIA_URL = 'https://{AWS_S3_CUSTOM_DOMAIN}/media/'
DEFAULT_FILE_STORAGE = 'config.storages.MediaStorage'

# # Static Files
# # ---For Prod Env---
# STATIC_URL = 'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
# STATICFILES_STORAGE = 'config.storages.StaticStorage'