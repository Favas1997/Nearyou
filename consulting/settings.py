"""
Django settings for consulting project.

Generated by 'django-admin startproject' using Django 3.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-(sg__vwd@wfcpzhd0(c4ncswg=(z^b5-#p8cb@@k*$)bdnq%j0'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Admin1',
    'patients',
    'doctors',
    'social_django',
    'channels',
    'medicalshop',
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'consulting.urls'
ASGI_APPLICATION = 'consulting.asgi.application'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'template')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'consulting.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME':'onlineconsult',
        'USER':'favas',
        'PASSWORD':'123456',
        'HOST':'localhost'
    }
}


# Number of seconds of inactivity before a user is marked offline
USER_ONLINE_TIMEOUT = 300

# Number of seconds that we will keep track of inactive users for before 
# their last seen is removed from the cache
USER_LASTSEEN_TIMEOUT = 60 * 60 * 24 * 7


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTHENTICATION_BACKENDS = [
 
 
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.github.GithubOAuth2',
    'social_core.backends.linkedin.LinkedinOAuth2',
    'django.contrib.auth.backends.ModelBackend',
 
 
]
SOCIAL_AUTH_FACEBOOK_KEY = '2920893384835686'
SOCIAL_AUTH_FACEBOOK_SECRET ='c68d5637db1c430fbeb44b3c854f7f8c'

SOCIAL_AUTH_GITHUB_KEY = 'b4fe004a14512d40ccb9'
SOCIAL_AUTH_GITHUB_SECRET ='3f7db08cc3353a6ef9aa05b1dae93e73ae4c74fd'


SOCIAL_AUTH_LINKEDIN_OAUTH_KEY = '868obmw4vdv89i'
SOCIAL_AUTH_LINKEDIN_OAUTH_SECRET ='UNxEoVvBBFPTWwLD'




LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR,'static')]



MEDIA_URL = '/media/'
MEDIA_ROOT =os.path.join(BASE_DIR,'media')

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}



EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST_USER='favasm123@gmail.com'
EMAIL_HOST='smtp.gmail.com'
EMAIL_PORT='587'
EMAIL_USE_TLS=True
EMAIL_HOST_PASSWORD=''
# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STRIPE_SECRET_KEY = 'sk_test_51Is8bGSFh8PQNiatOE2nPviQi3KLbfmuf3bnhay4xRMP6PlGzKrOBM8PFgdNNlPuwfUduqj2a6jG5yk08H1YpOZt00rf2PirGa'
STRIPE_PUBLISHABLE_KEY = 'pk_test_51Is8bGSFh8PQNiatWcVVCwYCafX4rlfNHJx5tKdFiLL7twGRqkV29jwLrkm0urlBQ12HUobMadhcrNZV5p3GG22J00cHwfxnRO'

