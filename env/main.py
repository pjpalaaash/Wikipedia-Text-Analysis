from flask import Flask , render_template , request
from werkzeug.utils import redirect
from os import link
import pandas
from pandas.io import html
import requests
import pandas as pd
from bs4 import BeautifulSoup
import html5lib
import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/wiki",methods = ["POST"]) 
def findit():

    if request.method == "POST":
        temp = request.form["wiki"]
        # if "wikipedia" not in temp.lower():
        #     print("Not found")
            

        #     return redirect("/")

        # else:

        htmls = requests.get(temp)
        html = BeautifulSoup(htmls.content,"html.parser")
        para = html.findAll(id="p")
        para = list(para)
        
        para1 = html.findAll('p')[1].get_text()
        temp = para1.split()
        counter = 0
        check = dict()
        for i in temp:
            curr_frequency = temp.count(i)
            if i in check:
                check[i] = check[i]+1
            else:
                check[i] = 1
            if(curr_frequency> counter):
                counter = curr_frequency
                most = i
        print(check)
        return render_template("home.html",heading=check.keys,data=check.values)

    
if __name__ == "__main__":
    app.run(debug=True)