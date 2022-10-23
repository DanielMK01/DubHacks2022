import os
from flask import Flask, request, render_template, jsonify
from sapling import SaplingClient

app = Flask(__name__)

 
@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def my_form_post():
    errors = []
    text = request.form['text']
    text_to_change = text
    # processed_text = add_new_input(text)

    API_KEY = 'YORSDR2PHC1W5KFFLCG9IJG29DH3O2NG'
    client = SaplingClient(api_key=API_KEY)
    edits = client.edits(text, session_id='test_session', variety=None, auto_apply=True)
    while (len(edits) is not 0):
        errors.append(edits[0]['error_type'])
        start = edits[0]['sentence_start'] + edits[0]['start']
        end = edits[0]['sentence_start'] + edits[0]['end']
        if not (start > len(text_to_change) or end > len(text_to_change)):
            text_to_change = text_to_change[: start] + edits[0]['replacement'] + text_to_change[end:]
        edits = client.edits(text_to_change, session_id='test_session', variety=None, auto_apply=True)
    links = lessons(errors)
    links_to_ret = request.form.getlist('handles[]')
    if not links_to_ret:
        links_to_ret = links
    # return render_template(my-form.html', link=links, count=len(links), the_links=links_to_ret)
    return render_template('returnPage.html', original=text, corrected=text_to_change, the_links=links_to_ret)
    # return hello() + text + str(errors)
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
        elif 'VERB:FORM' in error: 
            links.add('https://www.englishgrammar101.com/module-3/verbs-types-tenses-and-moods/lesson-8/tenses-of-verbs')
        elif 'VERB:TENSE' in error:
            links.add('https://www.englishgrammar101.com/module-3/verbs-types-tenses-and-moods/lesson-8/tenses-of-verbs')
        # elif 'SPELL' in error:

        #I like cats, dogs, zebras
        elif 'CONJ' in error:
            links.add('https://www.englishgrammar101.com/module-8/conjunctions-and-interjections/lesson-1/coordinate-conjunctions')

    return links



if __name__=='__main__':
   app.run()

def add_new_input(inp):
    return inp[::-1]
    
# print(edits)
