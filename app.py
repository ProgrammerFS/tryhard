import os
import csv
import openai
from flask import Flask, redirect, render_template, request, url_for
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
openai.api_key = "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"


@app.route("/", methods=("GET", "POST"))
@cross_origin()
def index():
    if request.method == "POST":
        symptoms = request.form["symptoms"]
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=generate_prompt(symptoms),
            temperature=0.4,
            max_tokens=500
        )
        return {"result" : response.choices[0].text}

    result = request.args.get("result")
    return render_template("index.html", result=result)

@app.route("/test", methods=("GET", "POST"))
@cross_origin()
def test():
    return {"diseases" : "trash ahmed"}

# @app.route("/login")
# def login():
#     return "Login"

# @app.route("/register")
# def register():
#     return "Register"
@app.route("/add-meds", methods=("GET", "POST"))
@cross_origin()
def add_meds():
    if request.method == "POST":
        r = request.form
        med = r.get("medication")
        frequency = r.get("frequency")
        startDate = r.get("startDate")
        endDate = r.get("endDate")
        with open("./database.csv", "a") as f:
            writer= csv.writer(f, delimiter=",")
            writer.writerow([med, frequency, startDate, endDate])
        return "Prescription added"
    else:
        return "Add prescription first"



def generate_prompt(symptoms):
    return "Give me a list of possible diseases if I have " + symptoms + "Give me a list of UK medications as well and links to articles for more information. Response should be divided into diseases,medcines, and article section. Respond with a JSON string where each section is a property in lowercase.The JSON string has properties articles, medicines, diseases There should be atleast 5 Article links which should be from NHS, Mayo clinic, Web MD and other reputable websites. Remove all new line characters in the response."
if __name__ == "__main__":
    app.run(debug=True)
