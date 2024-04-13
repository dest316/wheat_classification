from app import app
from flask import render_template, request, url_for


@app.route('/', methods=['GET'])
def main_page():
    html = render_template('main_page.html',
                           root_route=request.url_root)
    return html
