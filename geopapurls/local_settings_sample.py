ADMINS = (('The admin','admin@yourdomain.com'),)
SERVER_EMAIL = 'admin@yourdomain.com'

# Example for a SSL/TSL SMTP server
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.yourhost.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'info@yourdomain.com'
EMAIL_HOST_PASSWORD = 'password'
EMAIL_USE_TLS = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'geopapurls': {
            'handlers': ['suggested_services_email'],
            'level': 'INFO',
            'propagate': True,
        }
    }
}