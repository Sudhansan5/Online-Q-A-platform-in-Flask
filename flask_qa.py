from flask import Flask, render_template, url_for
app = Flask(__name__)

ques = [
    {
        'asker': 'Sudhanshu',
        'title': 'Question 1',
        'question': 'First question',
        'date_posted': 'December 8, 2020'
    },
    {
        'asker': 'Anish',
        'title': 'Question 2',
        'question': 'Second question',
        'date_posted': 'April 1, 2019'
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', ques=ques)

if __name__ == '__main__':
    app.run(debug=True)
