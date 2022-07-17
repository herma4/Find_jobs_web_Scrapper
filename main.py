from logging import exception
from flask import Flask, render_template, request, redirect, send_file
from scrapper import get_jobs
from exporter import save_to_csv

app = Flask("FlaskScrapper")#, template_folder='../templates')

db = {}

@app.route("/")
def home():
    return render_template(template_name_or_list="home.html")

# @app.route("/<userName>")
# def userName(userName):
#     return f"Hello {userName} how are you doing"
    
@app.route("/report")
def report():
    word = request.args.get("word")
    if word:
        word = word.lower() 
        existingJobs = db.get(word)
        if existingJobs:
            jobs = existingJobs
        else:
            jobs = get_jobs(word)
            db[word] = jobs
    else:
        return redirect("/")
    return render_template(
        template_name_or_list="report.html", 
        searchingBy=word, 
        resultsNumber=len(jobs),
        jobs = jobs
        )

@app.route("/export")
def export():
    try:
        word = request.args.get("word")
        if not word:
            raise Exception()
        word = word.lower()
        jobs = db.get(word)
        if not jobs:
            raise Exception()
        save_to_csv(jobs, word)
        return send_file(f"SerachResults_{word}.csv")
            
    except:
        return redirect("/")
        

# app.run(host = "0.0.0.0")
if __name__ == '__main__':
    app.debug = True
    app.run()