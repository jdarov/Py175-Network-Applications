from flask import Flask, render_template, g, redirect, request
import re

app = Flask(__name__)


@app.before_request
def load_contents():
    with open('book_viewer/data/toc.txt', 'r') as file:
        g.contents = file.readlines()

def in_paragraphs(text):
    return text.split("\n\n")

app.jinja_env.filters['in_paragraphs'] = in_paragraphs

def highlight_query(text, query):
    if not query:
        return text
    
    pattern = f"({re.escape(query)})"

    return re.sub(pattern, r"<strong>\1</strong>", text, flags=re.IGNORECASE)

app.jinja_env.filters['highlight_query'] = highlight_query

@app.route("/")
def index():
        
    return render_template('home.html', 
                           title="Book Viewer", 
                           contents=g.contents)

@app.route("/chapters/<int:page_num>")
def chapter(page_num):
    if 1 <= page_num <= len(g.contents):
        chapter_title = f"Chapter {page_num}: {g.contents[page_num - 1]}"

        with open(f'book_viewer/data/chp{page_num}.txt', 'r') as file:
            chapter = file.read()
    
        return render_template('chapter.html',
                               chapter_title=chapter_title,
                               contents=g.contents,
                               chapter=chapter)
    else:
        return redirect("/")
    
@app.route("/search")
def search():
    query = request.args.get('query', '')
    if not query:
        return render_template('search.html', query=query)
    
    results = list()

    for index, title in enumerate(g.contents, start = 1):
        with open(f'book_viewer/data/chp{index}.txt', 'r') as file:
            chapter_contents = file.read()

        matches = {}

        for para_index, paragraph_contents in enumerate(chapter_contents.split("\n\n")):
            if query.lower() in paragraph_contents.lower():
               matches[para_index] = paragraph_contents

        if matches:
            results.append({'num': index, 'title': title, 'paragraphs': matches})

    return render_template('search.html',
                           query=query,
                           results=results,
                           matches=matches)

@app.errorhandler(404)
def page_not_found(error):
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True, port=5003)