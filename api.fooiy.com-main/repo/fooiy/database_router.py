from django.db import transaction


class Router:
    @staticmethod
    def db_for_read(model, **hints):
        if model._meta.app_label == "django_cache":
            return "default"

        conn = transaction.get_connection("default")
        if conn.in_atomic_block:
            return "default"

        return "production"

    @staticmethod
    def db_for_write(model, **hints):
        return "default"

    @staticmethod
    def allow_relation(obj1, obj2, **hints):
        return True

    @staticmethod
    def allow_migrate(db, app_label, model_name=None, **hints):
        return True
