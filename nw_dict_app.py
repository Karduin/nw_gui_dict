"""Search in source string and show context,
source, translation of novelWrier GUI.

Usage:
    - run python nw_dict_app.py
    then go to http;/localhost:5000
"""

__version__ = "0.1"
__author__ = "Jean-Michel Heras"

import sqlite3

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route('/')
def show_list():
    return redirect(url_for("result"))

@app.route('/search', methods=["GET", "POST"])
def search():
    if request.method == "POST":
        data = request.form.get("source")

        return redirect(url_for("result", source=data))
    else:
        return render_template("search.html")

@app.route('/result')
def result():
    source = request.args.get('source', None)
    con = sqlite3.connect("nw_gui_dict.db")
    con.row_factory = sqlite3.Row
    if source is None:
        search_string = ""
    else:
        search_string = f'%{source}%'
    cur = con.cursor()
    cur.execute("PRAGMA foreign_keys = ON")
    cur.execute("SELECT name, source, translation FROM nw_translation INNER JOIN \
                 nw_context ON nw_translation.fk_context = nw_context.id WHERE source LIKE '%s';" % search_string)
    rows = cur.fetchall();
    return render_template("result.html",rows = rows)


if __name__ == '__main__':

   app.run(debug = True)

