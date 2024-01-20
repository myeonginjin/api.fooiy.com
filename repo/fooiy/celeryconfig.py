from fooiy.settings import CACHES

broker_url = CACHES["default"]["LOCATION"]
# result_backend = "django-db"
task_always_eager = False
accept_content = ["json", "pickle", "application/x-python-serialize"]
