from flask import render_template, abort, request

from app import app
from app.sources.registry import registry


@app.route('/')
@app.route('/index')
def index():
    return render_template('home.html', title='Home', sources=registry.all())


@app.route('/source/<source_id>')
def source_detail(source_id):
    source = registry.get(source_id)
    if source is None:
        abort(404)

    query = request.args.get('q', '')
    page = request.args.get('page', 1, type=int)

    result = source.search(query, page=page) if query else source.get_popular(page=page)

    return render_template(
        'source.html', title=source.name, source=source,
        result=result, query=query, page=page,
    )