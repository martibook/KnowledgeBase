from flask import Flask, session, request, redirect, url_for
from flask import render_template
from data import SearchForm, CreateForm, init_db, Knowledge_Tuple, Addr_Knowledge_Tuple
from data import Knowledge, Users


app = Flask(__name__)
app.config['SECRET_KEY'] = "I'll give you a key"
DB_Session = init_db()


def encode_space(text):
    return text.replace(' ', '%20')


def present_error(error):
    form = SearchForm()
    return render_template('error.html', error=error, form=form)


@app.route('/')
def index():
    form = SearchForm()
    return render_template('index.html', form=form)


@app.route('/search', methods=['POST'])
def search():
    db_session = DB_Session()
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
            error = {
                'cover': 'No Corresponding Knowledge Record',
                'info': 'Check your search words and try again ~'
            }
            return present_error(error)

        row_range = len(item_list) // 3 + int(len(item_list) % 3 != 0)
        return render_template('list.html', form=form, item_list=item_list, row_range=row_range)

    else:
        error = {
            'cover': 'Encountered Errors',
            'info': form.errors
        }
        return present_error(error)


@app.route('/preparation_create')
def preparation_create():
    form = CreateForm()
    return render_template('create.html', form=form)


@app.route('/preparation_update')
def preparation_update():
    form = CreateForm()
    if all(('cover' in session, 'cat' in session, 'content' in session)):
        form.cover.data, form.cat.data, form.content.data = session['cover'], session['cat'], session['content']
    return render_template('update.html', form=form)


@app.route('/item/<cover>/<cat>')
def item(cover, cat):
    db_session = DB_Session()
    search_form = SearchForm()

    knowledge = db_session.query(Knowledge).filter(Knowledge.cover==cover).filter(Knowledge.cat==cat).first()
    if knowledge:
        session['cover'] = knowledge.cover
        session['cat'] = knowledge.cat
        session['content'] = knowledge.content
        item = Knowledge_Tuple(knowledge.cover, knowledge.cat, knowledge.content.split('\n'))
        return render_template('item.html', item=item, form=search_form)

    else:
        error = {
            'cover': 'No Corresponding Knowledge Record',
            'info': 'Redirected URL went wrong ~'
        }
        return present_error(error)


def check_password_valid(password):
    db_session = DB_Session()
    users = db_session.query(Users).all()
    auth_passwords = [u.password for u in users]
    if password in auth_passwords:
        return True
    else:
        return False


def operation_create(form):
    db_session = DB_Session()
    try:
        cover, cat, content = form.cover.data, form.cat.data, form.content.data
        knowledge = Knowledge(cover=cover, cat=cat, content=content)
        db_session.add(knowledge)
        db_session.commit()
        return redirect(url_for('item', cover=cover, cat=cat))
    except Exception as e:
        db_session.rollback()
        error = {
            'cover': 'Failed to Create A New Knowledge Record',
            'info': str(e)
        }
        return present_error(error)


def operation_update(form):
    db_session = DB_Session()
    try:
        old_cover, old_cat, old_content = session['cover'], session['cat'], session['content']
        old_knowledge = db_session.query(Knowledge).filter(Knowledge.cover==old_cover).filter(Knowledge.cat==old_cat).first()
        db_session.delete(old_knowledge)

        cover, cat, content = form.cover.data, form.cat.data, form.content.data
        knowledge = Knowledge(cover=cover, cat=cat, content=content)
        db_session.add(knowledge)

        db_session.commit()
        return redirect(url_for('item', cover=cover, cat=cat))
    except Exception as e:
        db_session.rollback()
        error = {
            'cover': 'Failed to Update The Knowledge Record',
            'info': str(e)
        }
        return present_error(error)
    finally:
        session.pop('cover')
        session.pop('cat')
        session.pop('content')


@app.route('/operation/<act>', methods=['POST'])
def operation(act):
    form = CreateForm(request.form)

    if form.validate_on_submit():

        if not check_password_valid(form.password.data):
            error = {
                'cover': "Ohh.. You Don't Have The Correct Password ~",
                'info': "Well this is a space which welcomes everyone to visit while only someones can USE it :)"
            }
            return present_error(error)

        else:
            if act == 'create':
                return operation_create(form)
            elif act == 'update':
                return operation_update(form)
            else:
                pass

    else:
        error = {
            'cover': 'Failed to Create A New Knowledge Record',
            'info': form.errors
        }
        return present_error(error)
