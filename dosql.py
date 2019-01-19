import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "py_energy.settings")
import django
from django.utils import timezone

django.setup()
from energy.models import Message, Type
from django.db import connection


def add_column():
    cursor = connection.cursor()
    cursor.excute("alter table Message add typr")


if __name__ == "__main__":
    add_column()
