from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired
from collections import namedtuple


Knowledge_Tuple = namedtuple('Knowledge_Tuple', ['cover', 'cat', 'content'])


class SearchForm(FlaskForm):
    search = StringField('search', validators=[InputRequired()])


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
# database_uri = '{protocol}://{user}@{host}:{port}/database'.format(**database_config)
database_uri = '{protocol}:///{database}'.format(**database_config)
engine = create_engine(database_uri, convert_unicode=True)
DB_Session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = DB_Session.query_property()


class Knowledge(Base):
    __tablename__ = 'knowledge'
    cover = Column(String(30), primary_key=True)
    content = Column(Text)
    cat = Column(String(10))

    def __init__(self, cover=None, content=None, cat=None):
        self.cover = cover
        self.content = content
        self.cat = cat

    def __repr__(self):
        return """{cover}\n{cat}\n{content}""".format(cover=self.cover, content=self.content, cat=self.cat)


def init_db():
    Base.metadata.create_all(bind=engine)
    return DB_Session






