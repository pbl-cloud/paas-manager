# paas-manager

Module to run MapReduce tasks with Hadoop.

## Installation for development

### Requirements

* Python 3.4
* pip
* MySQL server

### Setup

```
pip install --allow-external mysql-connector-python mysql-connector-python
pip install -r requirements.txt
cp config/paas_manager.local.yml.example config/paas_manager.local.yml
```

Fix settings in `config/paas_manager.local.yml`.

Run with

```
python runserver.py
```

## Modules

### DatabaseConnector

`DatabaseConnector` provides a basic ORM.

```python
class Users extends DatabaseConnector:
    table = users

user = Users.create({'email': 'foo@foo.bar', 'password': 'foobar'})
user.email = 'foo@foo.baz'
user.password = 'abcdef'
user.save

assert(Users.find(user.id).id == Users.find_by({'email': 'foo@foo.baz'}).id)

user.update({'email': 'foo@bar.baz', 'password': 'barbaz'})
assert(user.email == 'foo@bar.baz')

user.update_one('email', 'bar@foo.bar')
assert(user.email == 'bar@foo.bar')

user.delete()
```
