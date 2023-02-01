from django.db import connection


def TableExists(table_name):
    return table_name in connection.introspection.table_names()
