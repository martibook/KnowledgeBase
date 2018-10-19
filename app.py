from flask import Flask, request, redirect, url_for
from flask import render_template
from data import SearchForm, CreateForm, init_db, Knowledge_Tuple, Addr_Knowledge_Tuple
from data import Knowledge


app = Flask(__name__)
app.config['SECRET_KEY'] = "I'll give you a key"
DB_Session = init_db()
db_session = DB_Session()


@app.route('/')
def index():
    form = SearchForm()
    return render_template('index.html', form=form)


def encode_space(text):
    return text.replace(' ', '%20')


@app.route('/search', methods=['POST'])
def search():
    form = SearchForm(request.form)
    item_addr_tpl = '/item/{cover}/{cat}'
    if form.validate_on_submit():
        keywords = form.search.data.split()
        item_set = set()
        for keyword in keywords:
            condition = '%{}%'.format(keyword.lower())
            knowledge_list = db_session.query(Knowledge).filter(Knowledge.cover.like(condition)).all()
            knowledge_list.extend(db_session.query(Knowledge).filter(Knowledge.cat.like(condition)).all())
            item_set |= set(Addr_Knowledge_Tuple(e.cover, e.cat, e.content, item_addr_tpl.format(
                cover=encode_space(e.cover), cat=encode_space(e.cat))) for e in knowledge_list)
        item_list = [e for e in item_set]
        if len(item_list) == 0:
            item_list.append(Addr_Knowledge_Tuple(cover='No Result Matched Your Search', cat='try again', content=None, addr='#'))
        row_range = len(item_list) // 3 + int(len(item_list) % 3 != 0)
        return render_template('list.html', form=form, item_list=item_list, row_range=row_range)
    else:
        error = {
            'cover': 'Encountered Errors',
            'info': form.errors
        }
        return present_error(error)


@app.route('/create')
def create():
    form = CreateForm()
    return render_template('create.html', form=form)


@app.route('/item/<cover>/<cat>')
def item(cover, cat):
    search_form = SearchForm()
    knowledge = db_session.query(Knowledge).filter(Knowledge.cover==cover).filter(Knowledge.cat==cat).first()
    if knowledge:
        item = Knowledge_Tuple(knowledge.cover, knowledge.cat, knowledge.content.split('\n'))
        return render_template('item.html', item=item, form=search_form)
    else:
        item = {
            'cover': 'No Corresponding Knowledge Record',
            'cat': '',
            'content': []
        }
        return render_template('item.html', item=item, form=search_form)


def present_error(error):
    form = SearchForm()
    return render_template('error.html', error=error, form=form)


@app.route('/create_item', methods=['POST'])
def create_item():
    form = CreateForm(request.form)
    if form.validate_on_submit():
        try:
            cover, cat, content = form.cover.data, form.cat.data, form.content.data
            knowledge = Knowledge(cover=cover, cat=cat, content=content)
            db_session.add(knowledge)
            db_session.commit()
            return redirect(url_for('item', cover=cover, cat=cat))
        except Exception as e:
            error = {
                'cover': 'Failed to Create A New Knowledge Record',
                'info': str(e)
            }
            return present_error(error)
    else:
        error = {
            'cover': 'Failed to Create A New Knowledge Record',
            'info': form.errors
        }
        return present_error(error)
