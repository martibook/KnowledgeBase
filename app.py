from flask import Flask, request
from flask import render_template
from data import SearchForm, init_db, Knowledge_Tuple


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
    sql_stat = "select cover, cat, content from knowledge where cover like '%{keyword}%' or cat like '%{keyword}%'"
    if request.method == 'POST':
        query = form.search.data
        keywords = query.split()
        item_set = set()
        for keyword in keywords:
            raw_data = db_session.execute(sql_stat.format(keyword=keyword)).fetchall()
            item_set |= set(Knowledge_Tuple(e[0], e[1], e[2]) for e in raw_data)
        item_list = [e for e in item_set]
        row_range = len(item_list) // 3 + int(len(item_list) % 3 != 0)
        return render_template('list.html', item_list=item_list, row_range=row_range)
    else:
        return ''


@app.route('/create')
def create():
    return 'create test passed!'


@app.route('/list')
def list():
    return render_template('list.html')

