from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/profile')
def profile():
    return render_template('u_account.html')


@app.route('/my_qstns')
def my_qstns():
    return render_template('my_qstns.html')


@app.route('/my_recent_qstns')
def my_recent_qstns():
    return render_template('my_recent_qstns.html')


@app.route('/my_answers')
def my_answers():
    return render_template('my_answers.html')


@app.route('/question')
def question():
    return render_template('question.html')


if __name__ == '__main__':
    app.run(debug=True)
