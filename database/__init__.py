import sqlite3
import os

# Check if we have an existing DB.
should_create_db = not os.path.exists('database.db')

connection = sqlite3.connect('database.db')

# If we didn't have an existing DB, create an empty one.
if should_create_db:
    create_sql = open('database/createDatabase.sql').read()
    cursor = connection.cursor()
    for statement in create_sql.split(';'):
        cursor.execute(statement)


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def cached_property(f):
    """returns a cached property that is calculated by function f"""
    def get(self):  # webscale
        try:
            return self._property_cache[f]
        except AttributeError:
            self._property_cache = {}
            x = self._property_cache[f] = f(self)
            return x
        except KeyError:
            x = self._property_cache[f] = f(self)
            return x

    return property(get)
