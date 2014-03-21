ADMINS = (('The admin','admin@yourdomain.com'),)
SERVER_EMAIL = 'admin@yourdomain.com'

# Example for a SSL/TSL SMTP server
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.yourhost.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'info@yourdomain.com'
EMAIL_HOST_PASSWORD = 'password'
EMAIL_USE_TLS = True