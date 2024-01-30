import sys
import pandas as pd
import spacy
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from langdetect import detect
from deep_translator import GoogleTranslator
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')

driver = webdriver.Chrome(options=options)

data = None

nlp1 = spacy.load("models/DP_detector/trained")
nlp1.add_pipe('sentencizer')
nlp2 = spacy.load("models/DP_classifier/trained")
translator = GoogleTranslator(target="en")


def split_paragraph(paragraph):
    doc = nlp1(paragraph)
    return [sent.text for sent in doc.sents]

def extractor(url):
    driver.get(url)
    js = 'return document.getElementsByTagName("html")'

    element = driver.execute_script(js)

    temp = element[0].text.split("\n")
    textList = []
    for i in temp:
        if i not in ['',' ','\t','\\']:
            if len(i) > 180:
                textList.extend(split_paragraph(i))    
            else:
                textList.append(i)
    return textList

def dpChecker(url):
    textlist = extractor(url)
    textContainingDP = {}
    data_to_database = []
    global translation
    translation = 0
    for text in textlist:
        # try:
        #     detectedLang = detect(text)
        # except:
        #     print("Language not detected : ",text, file=sys.stderr)
        #     try:
        #         translation = translator.translate(text)
        #         print("translated ",text,file=sys.stderr)
        #     except:
        #         print("Language not detected for translation : ",text, file=sys.stderr)
        #         continue
        # else:
        #     if detectedLang != 'en':
        #         translation = translator.translate(text)
        #         print("translated ",text,file=sys.stderr)
        #     else:
        #         translation = text
        translation = text   
        try:
            doc = nlp1(translation)
        except ValueError:
            print("Invalid value in nlp : ", translation, file=sys.stderr)
        except:
            print("Unknown error")
        else:
            prediction = doc.cats.get('positive') >= 0.65
            if prediction:
                doc = nlp2(translation)
                prediction = max(doc.cats, key = doc.cats.get)
                if prediction not in textContainingDP:
                    textContainingDP.update({prediction:[text]})
                else:
                    textContainingDP.get(prediction).append(text)
                data_to_database.append([text,1,prediction])
            else:
                data_to_database.append([text,0,"None"])
            
    try:
        with open("ScrapedData.csv","a", encoding='utf-8') as f:
            pd.DataFrame(data_to_database).to_csv(f,index=False,header=False)
    except:
        print("Couldn't encode", file=sys.stderr)
    return textContainingDP

app = Flask(__name__)
CORS(app , resources={r'/*': {"origins": "*"}})

@app.route("/", methods = ['POST'])
def index():
        global data
        data = request.get_json()
        textList = dpChecker(data["URL"])
        return jsonify(textList)


@app.route("/feedback")
def show_form():
    return render_template("form.html")

@app.route("/thankyou")
def show_thankyou():
    return render_template("thankyou.html")

@app.route("/submit-form", methods = ['POST'])
def submit_form():
    UserFeedback_data = request.get_json()
    UserData = []
    for keys in UserFeedback_data:
        UserData.append(UserFeedback_data[keys])
    
    print(UserData, file=sys.stderr)
    with open("FeedbackData.csv", "a", encoding='utf-8') as fd:
            pd.DataFrame([UserData]).to_csv(fd, index=False, header=False)

    return UserFeedback_data

app.run(debug=True)