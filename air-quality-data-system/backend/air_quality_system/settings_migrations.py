"""
Migration helper settings.

This repository may have an existing MySQL database whose migration history becomes
inconsistent after introducing a custom AUTH_USER_MODEL (accounts.User). Django's
`makemigrations` checks the connected DB's applied migration graph and will abort.

Use this settings module to run `makemigrations` against a clean local SQLite DB.
The generated migration files remain valid for MySQL.
"""

from .settings import *  # noqa: F403

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db_migrations.sqlite3",  # noqa: F405
    }
}

