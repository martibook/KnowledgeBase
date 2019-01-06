from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField
from wtforms.validators import InputRequired, Length
from collections import namedtuple
import os


Twenty = 20
Fourty = 40


Knowledge_Tuple = namedtuple('Knowledge_Tuple', ['cover', 'cat', 'content'])
Addr_Knowledge_Tuple = namedtuple('Knowledge_Tuple', ['cover', 'cat', 'content', 'addr'])


class SearchForm(FlaskForm):
    search = StringField('search', validators=[InputRequired(), Length(max=Fourty)])


class CreateForm(FlaskForm):
    password = PasswordField('Need A Password To Go Ahead', validators=[InputRequired()])
    cover = StringField('Note Cover', validators=[InputRequired(), Length(max=Fourty)])
    cat = StringField('Note Category', validators=[InputRequired(), Length(max=Twenty)])
    content = TextAreaField('Note Content', validators=[InputRequired()])


from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Text


database_config = {
    'database': 'marti',
    'user': 'marti',
    'port': 5432,
    'host': 'localhost',
    'protocol': 'postgresql'
}

docker_database_config = {
    'database': 'marti',
    'user': 'marti',
    'port': 5432,
    'host': 'db',  # name of ur database service
    'protocol': 'postgresql'
}

mode = os.environ['MODE'] if 'MODE' in os.environ else 'docker'
if mode == 'docker':
    database_uri = '{protocol}://{user}@{host}/{database}'.format(**docker_database_config)
else:
    database_uri = '{protocol}:///{database}'.format(**database_config)


engine = create_engine(database_uri, convert_unicode=True)
DB_Session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = DB_Session.query_property()


class Knowledge(Base):

    __tablename__ = 'knowledge'
    cover = Column(String(Fourty), primary_key=True)
    cat = Column(String(Twenty), primary_key=True)
    owner = Column(String(Twenty), primary_key=True)
    content = Column(Text)

    def __init__(self, cover=None, content=None, cat=None, owner=None):
        self.cover = cover
        self.content = content
        self.cat = cat
        self.owner = owner

    def __repr__(self):
        return """{cover}\n{cat}\n{content}""".format(cover=self.cover, content=self.content, cat=self.cat)


class Users(Base):

    __tablename__ = 'users'
    username = Column(String(), primary_key=True)
    password = Column(String(), primary_key=True)

    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password

    def __repr__(self):
        return """{username}\n{password}""".format(username=self.username, password=self.password)


def insert_users():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file = os.path.join(dir_path, "data_init", "users.txt")
    if not os.path.exists(file):
        return

    db_session = DB_Session()
    exist_users = db_session.query(Users).all()
    known_pass = [u.password for u in exist_users]
    with open(file, 'r') as in_f:
        for line in in_f:
            username, password = line.split()
            if password not in known_pass:
                user = Users(username=username, password=password)
                db_session.add(user)
        db_session.commit()


def init_db():
    Base.metadata.create_all(bind=engine)
    insert_users()
    return DB_Session






