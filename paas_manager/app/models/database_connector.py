import mysql.connector
import os

from ... import config

# FIXME: use proper config files
if os.environ.get('PAAS_MANAGER_ENV') == 'test':
    config['mysql']['database'] += '_test'


class DatabaseConnector():
    connect = mysql.connector.connect(**config['mysql'])
    cursor = connect.cursor()

    def __init__(self, args=None):
        self.id = None
        if args is None:
            args = {}
        self._args = args
        for k, v in args.items():
            setattr(self, k, v)

    @classmethod
    def hydrate_obj(cls, values):
        if not values:
            return None
        fields = [i[0] for i in cls.cursor.description]
        obj = cls()
        for i, f in enumerate(fields):
            setattr(obj, f, values[i])
        return obj

    @classmethod
    def _val_to_cond(cls, v):
        return str(v[0]) + "=%s"

    @classmethod
    def _conditions_to_str(cls, conditions):
        return ' AND '.join(map(cls._val_to_cond, conditions.items()))

    @classmethod
    def _make_query(cls, conditions, options):
        if 'one' in options:
            options['limit'] = 1
        query_template = "select * from {table}"
        args = ()
        if conditions:
            query_template += " where {conditions}"
            args += tuple(conditions.values())

        if 'limit' in options:
            query_template += " limit %s"
            args += (options['limit'],)

        query = query_template.format(
            table=cls.table, conditions=cls._conditions_to_str(conditions))
        cls.cursor.execute(query, args)
        if 'one' in options:
            return cls.hydrate_obj(cls.cursor.fetchone())
        else:
            return [cls.hydrate_obj(obj) for obj in cls.cursor.fetchall()]

    @classmethod
    def find(cls, conditions=None):
        if conditions is None:
            conditions = {}
        return cls._make_query(conditions, {})

    @classmethod
    def create(cls, args=None):
        obj = cls(args)
        return obj.save()

    @classmethod
    def find_by(cls, conditions):
        return cls._make_query(conditions, {'one': True})

    @classmethod
    def remove_all(cls):
        query_template = "delete from {table}"
        query = query_template.format(table=cls.table)
        cls.cursor.execute(query)

    def is_new(self):
        return self.id is None

    def before_save(self):
        pass

    def save(self):
        self.before_save()
        query_template = "insert into {table} ({fields}) values ({values})"
        fields = ', '.join([str(key) for key in self._args.keys()])
        values = ', '.join(['%s' for _ in self._args.values()])
        query = query_template.format(
            table=self.table, fields=fields, values=values)
        self.cursor.execute(query, tuple(self._args.values()))
        if self.is_new():
            self.id = self.cursor.lastrowid
        self.connect.commit()
        return self

    def remove(cls):
        query_template = "delete from {table} where id=%s"
        query = query_template.format(table=self.table)
        cls.cursor.execute(query, (self.id,))

    def _add_attr(self, key, value):
        setattr(self, key, value)
        self._args[key] = value

    def _del_attr(self, key):
        if hasattr(self, key):
            delattr(self, key)
        if key in self._args:
            del self._args[key]
