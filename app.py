import os
import sqlite3
import os.path
from flask import Flask, request, render_template, jsonify
from sapling import SaplingClient

app = Flask(__name__)

curr_user = 'steve'

def get_db_connection():
    conn = sqlite3.connect("students.db")
    conn.row_factory = sqlite3.Row
    return conn


def insert_data(errors):
    curr = get_db_connection()
    cur = curr.cursor()
    result = cur.execute('SELECT COUNT(*) FROM categories WHERE id = ?', (curr_user,)).fetchone()
    # print(result[0])
    if result[0] == 0:
        print("is here")
        cur.execute('INSERT INTO categories (id) VALUES(?)', (curr_user,))
        curr.commit()
        print("is also here")
    for error in errors:
        error = error[1:]
        print(error)
        curr_count = cur.execute("SELECT ? FROM categories WHERE id = 'steve'", (str(error))).fetchone()[0]
        print(curr_count)
        new_count = curr_count + 1
        cur.execute('UPDATE categories SET ? = ? WHERE id = ?', (error, new_count, curr_user,))
        curr.commit()
    curr.close()
    
def extract_group_rankings():
    conn = get_db_connection()
    cur = conn.cursor()
    # result = cur.execute('SELECT COUNT(*) FROM categories WHERE id = ?', (curr_user,)).fetchone()
    # if result is None:
    #     cur.execute('INSERT INTO categories.db (id) VALUES(?)', (curr_user))
    desc_cur = cur.execute('SELECT * FROM categories')
    names = [description[0] for description in desc_cur.description]
    count = cur.execute('SELECT COUNT(*) FROM categories')
    totals = []
    row = cur.execute('SELECT * FROM categories WHERE id = ?', (curr_user,))
    max_int = 0
    max_index = 0
    for i in range(1, len(row)):
        if row[i] > max_int:
            max_int = row[i]
            max_index = i
    # result = cur.execute(SELECT MAX FROM )
    # res = sorted(range(len(totals)), key = lambda sub: totals[sub])[-5:]
    conn.close()
    return names[max_index]

@app.route('/')
def hello():
    return render_template('index2.html')

# @app.route('/')
# def hello2():
#     return render_template('index2.html')

@app.route('/', methods=['POST'])
def my_form_post():
    errors = []
    text = request.form['text']
    text_to_change = text
    # processed_text = add_new_input(text)

    API_KEY = '15836DYNP6DZALUOGI867TOA3D84OYXQ'
    client = SaplingClient(api_key=API_KEY)
    edits = client.edits(text, session_id='test_session', variety=None, auto_apply=True)
    while (len(edits) is not 0):
        temp = edits[0]['error_type']
        errors.append(temp.replace(":", ""))
        start = edits[0]['sentence_start'] + edits[0]['start']
        end = edits[0]['sentence_start'] + edits[0]['end']
        if not (start > len(text_to_change) or end > len(text_to_change)):
            text_to_change = text_to_change[: start] + edits[0]['replacement'] + text_to_change[end:]
        edits = client.edits(text_to_change, session_id='test_session', variety=None, auto_apply=True)
    links = lessons(errors)
    links_to_ret = request.form.getlist('handles[]')
    # insert_data(errors)
    if not links_to_ret:
        links_to_ret = links
    # eturn render_template('my-formhtml', link=links, count=len(links), the_links=links_to_ret))
    return render_template('returnPage2.html', original=text, corrected=text_to_change, the_links=links_to_ret)    # # return hello() + text + str(len(errors))
    #  return hello() + str(links_to_ret)
    # str(len(lessons(errors)))

def lessons(errors:list):
    links = set()
    for error in errors:
        #commas
        if 'PUNCT' in error:
            links.add('https://www.englishgrammar101.com/capitalization-and-punctuation')
        elif 'NOUN' in error:
            links.add('https://www.englishgrammar101.com/module-1/nouns/lesson-1/what-is-a-noun')
        #"I walk yesterday"
        elif 'VERBFORM' in error: 
            links.add('https://www.englishgrammar101.com/module-3/verbs-types-tenses-and-moods/lesson-8/tenses-of-verbs')
        elif 'CONTR' in error:
            links.add('https://www.myenglishpages.com/english/grammar-lesson-contraction.php')
        elif 'CONJ' in error:
            links.add('https://www.englishgrammar101.com/module-8/conjunctions-and-interjections/lesson-1/coordinate-conjunctions')
        elif 'PRON' in error:
            links.add('https://www.englishgrammar101.com/module-2/pronouns/lesson-1/personal-pronouns')
        elif 'ADJFORM' in error or 'ADJ' in error:
            links.dd('https://www.englishgrammar101.com/module-6/modifiers-adjectives-and-adverbs/lesson-1/adjectives')
        elif 'VERBSVA' in error:
            links.add('https://www.englishgrammar101.com/module-4/verbs-agreement-and-challenges/lesson-2/agreement-subjects-with-and-or-or-nor')
        elif 'VERBTENSE' in error:
            links.add('https://www.khanacademy.org/humanities/grammar/parts-of-speech-the-verb/the-tenses/e/intro-to-verb-tense')
        elif 'OTHER' in error:
            links.add('https://www.englishgrammar101.com')
        elif 'DET' in error:
            links.add('https://www.myenglishpages.com/english/grammar-lesson-determiners.php')
        return links

if __name__ == "main":
    app.run()

def add_new_input(inp):
    return inp[::-1]
    
# print(edits)
