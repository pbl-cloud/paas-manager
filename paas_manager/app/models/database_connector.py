import mysql.connector
import os

from ... import config

# FIXME: use proper config files
if os.environ.get('PAAS_MANAGER_ENV') == 'test':
    config['mysql']['database'] += '_test'


def db_action(fn):
    def wrapped(*args, **kwargs):
        res = fn(*args, **kwargs)
        DatabaseConnector.connect.commit()
        return res
    return wrapped


class DatabaseConnector():
    connect = mysql.connector.connect(**config['mysql'])
    cursor = connect.cursor()

    def __init__(self, args=None):
        if args is None:
            args = {}
        self.__dict__ = args
        if not hasattr(self, 'id'):
            self.id = None
        for k, v in args.items():
            setattr(self, k, v)

    @classmethod
    def hydrate_obj(cls, values):
        if not values:
            return None
        fields = [i[0] for i in cls.cursor.description]
        obj = cls()
        for i, f in enumerate(fields):
            obj._add_attr(f, values[i])
        return obj

    @classmethod
    def _val_to_cond(cls, v):
        return str(v[0]) + "=%s"

    @classmethod
    def _conditions_to_str(cls, conditions):
        return ' AND '.join(map(cls._val_to_cond, conditions.items()))

    @classmethod
    def _make_query(cls, conditions, options):
        if 'fields' in options:
            fields = ', '.join(options['fields'])
        else:
            fields = '*'

        if 'one' in options:
            options['limit'] = 1
        query_template = "select {fields} from {table}"
        args = ()
        if conditions:
            query_template += " where {conditions}"
            args += tuple(conditions.values())

        if 'limit' in options:
            query_template += " limit %s"
            args += (options['limit'],)

        query = query_template.format(
            fields=fields,
            table=cls.table,
            conditions=cls._conditions_to_str(conditions)
        )
        cls.cursor.execute(query, args)
        if 'one' in options:
            return cls.hydrate_obj(cls.cursor.fetchone())
        else:
            return [cls.hydrate_obj(obj) for obj in cls.cursor.fetchall()]

    @classmethod
    def query(cls, conditions=None, options=None):
        if conditions is None:
            conditions = {}
        if options is None:
            options = {}
        return cls._make_query(conditions, {})

    @classmethod
    def count(cls, conditions=None):
        options = {'fields': 'id'}
        result = cls.query(conditions, options)
        return len(result)

    @classmethod
    def exists(cls, conditions=None):
        return cls.count(conditions) > 0

    @classmethod
    def create(cls, args=None):
        obj = cls(args)
        return obj.save()

    @classmethod
    def find(cls, id):
        return cls.find_by({'id': id})

    @classmethod
    def find_by(cls, conditions):
        return cls._make_query(conditions, {'one': True})

    @classmethod
    @db_action
    def remove_all(cls):
        query_template = "delete from {table}"
        query = query_template.format(table=cls.table)
        cls.cursor.execute(query)

    def is_new(self):
        return self.id is None

    def before_save(self):
        pass

    def _insert(self):
        query_template = "insert into {table} ({fields}) values ({values})"
        fields = ', '.join([str(key) for key in self.__dict__.keys()])
        values = ', '.join(['%s' for _ in self.__dict__.values()])
        query = query_template.format(
            table=self.table, fields=fields, values=values)
        self.cursor.execute(query, tuple(self.__dict__.values()))
        self.id = self.cursor.lastrowid

    def _update(self):
        query_template = "update {table} set {fields} where id=%s"
        fields = ', '.join(map(self._val_to_cond, self.__dict__.items()))
        query = query_template.format(table=self.table, fields=fields)
        self.cursor.execute(query, tuple(self.__dict__) + (self.id,))

    @db_action
    def save(self):
        self.before_save()
        if self.is_new():
            self._insert()
        else:
            self._update()
        return self

    @db_action
    def remove(self):
        query_template = "delete from {table} where id=%s"
        query = query_template.format(table=self.table)
        self.cursor.execute(query, (self.id,))
