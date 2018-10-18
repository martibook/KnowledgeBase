from flask import Flask, request, redirect, url_for
from flask import render_template
from data import SearchForm, CreateForm, init_db, Knowledge_Tuple, Addr_Knowledge_Tuple

app = Flask(__name__)
app.config['SECRET_KEY'] = "I'll give you a key"
DB_Session = init_db()
db_session = DB_Session()

INPUT_ERROR_MARK = 'encounter error when creating a new knowledge record'


@app.route('/')
def index():
    form = SearchForm()
    return render_template('index.html', form=form)


def encode_space(text):
    return text.replace(' ', '%20')


@app.route('/search', methods=['POST'])
def search():
    form = SearchForm(request.form)
    sql_stat = "SELECT cover, cat, content FROM knowledge WHERE LOWER(cover) LIKE '%{keyword}%' OR LOWER(cat) LIKE '%{keyword}%'"
    item_addr_tpl = '/item/{cover}/{cat}'
    if form.validate_on_submit():
        query = form.search.data
        keywords = query.split()
        item_set = set()
        for keyword in keywords:
            raw_data = db_session.execute(sql_stat.format(keyword=keyword.lower())).fetchall()
            item_set |= set(Addr_Knowledge_Tuple(e[0], e[1], e[2], item_addr_tpl.format(cover=encode_space(e[0]), cat=encode_space(e[1]))) for e in raw_data)
        item_list = [e for e in item_set]
        if len(item_list) == 0:
            item_list.append(Addr_Knowledge_Tuple(cover='No Result Matched Your Search', cat='try again', content=None, addr='#'))
        row_range = len(item_list) // 3 + int(len(item_list) % 3 != 0)
        return render_template('list.html', form=form, item_list=item_list, row_range=row_range)
    else:
        return ''


@app.route('/create')
def create():
    form = CreateForm()
    return render_template('create.html', form=form)


@app.route('/item/<cover>/<cat>')
def item(cover, cat):
    search_form = SearchForm()
    if cat == INPUT_ERROR_MARK:
        item = {
            'cover': 'Failed to Create A New Knowledge Record',
            'cat': '',
            'content': [cover]
        }
        return render_template('item.html', item=item, form=search_form)
    else:
        sql_stat = "SELECT cover, cat, content FROM knowledge WHERE LOWER(cover) = '{cover}' and LOWER(cat) = '{cat}'" \
            .format(cover=cover, cat=cat)
        raw_data = db_session.execute(sql_stat).fetchone()
        if raw_data:
            item = Knowledge_Tuple(raw_data[0], raw_data[1], raw_data[2].split('\n'))
            return render_template('item.html', item=item, form=search_form)
        else:
            item = {
                'cover': 'No Corresponding Knowledge Record',
                'cat': '',
                'content': []
            }
            return render_template('item.html', item=item, form=search_form)


@app.route('/create_item', methods=['POST'])
def create_item():
    form = CreateForm(request.form)
    if form.validate_on_submit():
        cover, cat, content = form.cover.data, form.cat.data, form.content.data

        return '{}'.format('no problem')

    else:
        cover, cat = ['{v}({k})'.format(k=k, v=v[0]) for k, v in form.errors.items()][0], INPUT_ERROR_MARK
        return redirect(url_for('item', cover=cover, cat=cat))
