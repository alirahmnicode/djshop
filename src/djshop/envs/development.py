from .common import *


INSTALLED_APPS = [
    "drf_spectacular",
] + INSTALLED_APPS



SPECTACULAR_SETTINGS = {
    "TITLE": "Your Project API",
    "DESCRIPTION": "Your project description",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}
