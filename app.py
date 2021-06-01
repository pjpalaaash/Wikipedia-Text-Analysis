from flask import Flask , render_template , request
from werkzeug.utils import redirect
from os import error, link
import requests
import urllib
import bs4 as bs
import html5lib
import os
import nltk
from nltk.corpus import stopwords
import string
import re
nltk.download('stopwords')


app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/wiki",methods = ["POST"]) 
def findit():

    if request.method == "POST":
        error = False
        temp = request.form["wiki"]
        if "https://en.wikipedia.org/wiki/" not in temp.lower():
            error = True
            return render_template("home.html",error=error)
            
        #For Fetching Wikipedia Text:
        else:
            source = urllib.request.urlopen(temp).read()

            soup = bs.BeautifulSoup(source, 'lxml')

            text = ""

            for para in soup.find_all('p'):

                text+= para.text


            text = re.sub(r'\[[0-9]*\]',' ',text)

            text = re.sub(r'\s+',' ',text)

            text = text.lower()

            text = re.sub(r'\d',' ',text)
            text = re.sub(r'\s+',' ',text)

            words = text.split()
            new_words = []

            for every in words:
                if every == str('') or str(every) == ":" or str(every) == ";" or str(every) == " ":
                    continue
                else:
                    new_words.append(re.sub(r"[^\w\s]",'',str(every)))

            
            #Logic for Counting Frequency of a Words Using Dictionary in Python:

            counts = dict()

            for word in new_words:

                if word in counts:
                    counts[word] = counts[word] + 1

                else:
                    counts[word] = 1

            sorted_counts = sorted(counts.values(),reverse=True)
            final_counts = dict()

            for i in sorted_counts:
                for k in counts.keys():
                    if k == '':
                        continue

                    else:
                        if counts[k] == i:
                            final_counts[k] = counts[k]
                            break


            #print(final_counts)
            N = 10
            out = out = dict(list(final_counts.items())[0: N])
            return render_template("table.html",counts=out)

    
if __name__ == "__main__":
    app.run(debug=True)