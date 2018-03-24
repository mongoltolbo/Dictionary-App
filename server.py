from flask import Flask, render_template, request
import json
import requests
import urllib

app = Flask(__name__)

@app.route("/")
def server():
    return render_template('home.html')

@app.route("/results", methods=['POST'])
def results():
    # Extract the required data from the form
    word_id = str(request.form.get('query'))
    word_ori = word_id
    word_id = word_id.replace(' ','_')
    word_id = word_id.lower()
    word_id = urllib.parse.quote_plus(word_id)
    app_id = '' # Obtain tha App Id from https://developer.oxforddictionaries.com/documentation/getting_started
    app_key = '' # Obtain tha App Key from https://developer.oxforddictionaries.com/documentation/getting_started
    language = 'en'
    url = 'https://od-api.oxforddictionaries.com:443/api/v1/entries/' + language + '/' + word_id
    r = requests.get(url, headers = {'app_id': app_id, 'app_key': app_key})
    try :
        json_data = r.json()
        resultsArr = json_data["results"]
        i=1
        for result in resultsArr :
            lexicalEntriesArr = resultsArr[0]["lexicalEntries"]
            definition = list()
            for lexical in lexicalEntriesArr :
                entriesArr = lexical["entries"]
                sensesArr = entriesArr[0]["senses"]
                definitionsArr = sensesArr[0]["definitions"]
                definitionsArr[0] = definitionsArr[0].replace(u"\u2018", "'").replace(u"\u2019", "'")
                definition.append(str(i) + ". " + str(definitionsArr[0]))
                i=i+1
        return render_template('results.html', query=word_ori, definitions=definition)
    except :
        return render_template('error.html')
    

if __name__=='__main__':
    app.run()
