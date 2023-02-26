import os
import csv
import openai
from flask import Flask, redirect, render_template, request, url_for
from flask_cors import cross_origin

app = Flask(__name__)
openai.api_key = "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"


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        symptoms = request.form["symptoms"]
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=generate_prompt(symptoms),
            temperature=0.4,
            max_tokens=500
        )
        return redirect(url_for("index", result=response.choices[0].text))

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
    return """I have {} what is the most probable disease I have
give me the probable diseases in bullet points and give me web links on more information on these diseases""".format(
        symptoms.capitalize()
    )
if __name__ == "__main__":
    app.run(debug=True)
