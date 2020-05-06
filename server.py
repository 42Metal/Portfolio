import csv
import json
from flask import Flask, render_template, url_for, request, redirect

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/<string:page_name>')
def page(page_name):
    return render_template(page_name)


def write_email_to_file(data):
    with open('database.txt', mode='a') as database:
        email_json = json.dumps(data)
        file = database.write(email_json)


def write_email_to_csv(data):
    with open('database.csv', newline='', mode='a') as database:
        email = data['email_addr']
        subject = data['email_subject']
        body = data['email_body']
        csv_writer = csv.writer(database, delimiter=',', quotechar='|',
                                quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([email, subject, body])


@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    error = None
    if request.method == 'POST':
        try:
            email_data = request.form.to_dict()
            write_email_to_csv(email_data)
            return redirect('/thankyou.html')
        except:
            return 'Exception: could not write to DB.'
    else:
        return 'Something went wrong.'


if __name__ == '__main__':
    app.run()
