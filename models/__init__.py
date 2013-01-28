# -*- coding: utf-8 -*-
'''
    Copyright [2012] [Redacted Labs]

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
-------------

This sets up sqlalchemy.
For more information about sqlalchemy check out http://www.sqlalchemy.org/

'''


from sqlalchemy import create_engine
from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.types import Integer
from sqlalchemy.orm import sessionmaker
from models.BaseObject import BaseObject
from libs.ConfigManager import ConfigManager

metadata = BaseObject.metadata

config = ConfigManager.Instance()
db_connection = 'mysql://%s:%s@%s/%s' % (
    config.db_user, config.db_password, config.db_server, config.db_name)
engine = create_engine(db_connection)
Session = sessionmaker(bind=engine, autocommit=True)

#Many to Many tables
dork_tag_table = Table('dork_tag', BaseObject.metadata,
    Column('dork_id', Integer, ForeignKey('dork.id')),
    Column('tag_id', Integer, ForeignKey('tag.id')))

# Import the dbsession instance to execute queries
dbsession = Session(autoflush=True)

# Import models (or the tables won't get created)
from models.Permission import Permission
from models.User import User
from models.Dork import Dork
from models.Tag import Tag

# Calling this will create the tables at the database
create_tables = lambda: (
    setattr(engine, 'echo', True), metadata.create_all(engine))

# Bootstrap the databases


def boot_strap():
    import setup.bootstrap
