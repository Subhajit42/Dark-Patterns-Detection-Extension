import sys
import pandas as pd
import spacy
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
# from langdetect import detect
from deep_translator import GoogleTranslator
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os

# Configure Selenium WebDriver options
options = Options()
options.add_argument('--headless')  # Run in headless mode
options.add_argument('--no-sandbox')  # Disable sandboxing
options.add_argument('--disable-dev-shm-usage')  # Disable shared memory usage
options.add_argument('--disable-gpu')  # Disable GPU usage

driver = webdriver.Chrome(options=options)

# Load NLP models
nlp1 = spacy.load("models/DP_detector/trained")
nlp1.add_pipe('sentencizer')  # Add sentence segmentation pipeline
nlp2 = spacy.load("models/DP_classifier/trained")
translator = GoogleTranslator(target="en")  # Translator for non-English text

# Ensure the CSV files exist
if not os.path.exists("ScrapedData.csv"):
    with open("ScrapedData.csv", "w", encoding='utf-8') as f:
        pd.DataFrame(columns=["Text", "Contains_DP", "Category"]).to_csv(f, index=False)

if not os.path.exists("FeedbackData.csv"):
    with open("FeedbackData.csv", "w", encoding='utf-8') as f:
        pd.DataFrame(columns=["Feedback"]).to_csv(f, index=False)


def split_paragraph(paragraph):
    """
    Splits a paragraph into sentences using the NLP model.

    Args:
        paragraph (str): The input paragraph.

    Returns:
        list: A list of sentences.
    """
    doc = nlp1(paragraph)
    return [sent.text for sent in doc.sents]


def extractor(url):
    """
    Extracts text content from a webpage.

    Args:
        url (str): The URL of the webpage.

    Returns:
        list: A list of text segments extracted from the webpage.
    """
    driver.get(url)
    js = 'return document.getElementsByTagName("html")'
    element = driver.execute_script(js)

    temp = element[0].text.split("\n")
    textList = []
    for i in temp:
        if i not in ['', ' ', '\t', '\\']:
            if len(i) > 180:
                textList.extend(split_paragraph(i))  # Split long text into sentences
            else:
                textList.append(i)
    return textList


def dpChecker(url):
    """
    Checks for dark patterns in the text extracted from a webpage.

    Args:
        url (str): The URL of the webpage.

    Returns:
        dict: A dictionary containing detected dark patterns and their categories.
    """
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
                prediction = max(doc.cats, key=doc.cats.get)
                if prediction not in textContainingDP:
                    textContainingDP.update({prediction: [text]})
                else:
                    textContainingDP.get(prediction).append(text)
                data_to_database.append([text, 1, prediction])
            else:
                data_to_database.append([text, 0, "None"])

    # Save results to CSV
    try:
        with open("ScrapedData.csv", "a", encoding='utf-8') as f:
            pd.DataFrame(data_to_database).to_csv(f, index=False, header=False)
    except:
        print("Couldn't encode", file=sys.stderr)

    return textContainingDP


# Flask app setup
app = Flask(__name__)
CORS(app, resources={r'/*': {"origins": "*"}})


@app.route("/", methods=['POST'])
def index():
    """
    Endpoint to process a URL and detect dark patterns.

    Returns:
        JSON: A dictionary of detected dark patterns.
    """
    global data
    data = request.get_json()
    textList = dpChecker(data["URL"])
    return jsonify(textList)


@app.route("/feedback")
def show_form():
    """
    Endpoint to render the feedback form.

    Returns:
        HTML: The feedback form page.
    """
    return render_template("form.html")


@app.route("/thankyou")
def show_thankyou():
    """
    Endpoint to render the thank-you page.

    Returns:
        HTML: The thank-you page.
    """
    return render_template("thankyou.html")


@app.route("/submit-form", methods=['POST'])
def submit_form():
    """
    Endpoint to handle feedback form submission.

    Returns:
        JSON: The submitted feedback data.
    """
    UserFeedback_data = request.get_json()
    UserData = []
    for keys in UserFeedback_data:
        UserData.append(UserFeedback_data[keys])

    print(UserData, file=sys.stderr)
    with open("FeedbackData.csv", "a", encoding='utf-8') as fd:
        pd.DataFrame([UserData]).to_csv(fd, index=False, header=False)

    return UserFeedback_data


# Run the Flask app
app.run(host='127.0.0.1', port=5000, debug=True)