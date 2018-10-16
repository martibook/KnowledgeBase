from flask import Flask, request
from flask import render_template
from data import SearchForm, CreateForm, init_db, Knowledge_Tuple


app = Flask(__name__)
app.config['SECRET_KEY'] = "I'll give you a key"
DB_Session = init_db()
db_session = DB_Session()


@app.route('/')
def index():
    form = SearchForm()
    return render_template('index.html', form=form)


@app.route('/search', methods=['POST'])
def search():
    form = SearchForm(request.form)
    sql_stat = "SELECT cover, cat, content FROM knowledge WHERE LOWER(cover) LIKE '%{keyword}%' OR LOWER(cat) LIKE '%{keyword}%'"
    if form.validate_on_submit():
        query = form.search.data
        keywords = query.split()
        item_set = set()
        for keyword in keywords:
            raw_data = db_session.execute(sql_stat.format(keyword=keyword.lower())).fetchall()
            item_set |= set(Knowledge_Tuple(e[0], e[1], e[2]) for e in raw_data)
        item_list = [e for e in item_set]
        if len(item_list) == 0:
            item_list.append(Knowledge_Tuple(cover='No Result Matched Your Search', cat='try again', content=None))
        row_range = len(item_list) // 3 + int(len(item_list) % 3 != 0)
        return render_template('list.html', form=form, item_list=item_list, row_range=row_range)
    else:
        return ''


@app.route('/create')
def create():
    form = CreateForm()
    return render_template('create.html', form=form)
    # return 'create test passed!'


@app.route('/detailed')
def list():
    return render_template('list.html')


@app.route('/created', methods=['POST'])
def created():
    form = CreateForm(request.form)
    if form.validate_on_submit():
        return '{}'.format(form.cover.data)
    else:
        return '{}'.format(form.errors)


