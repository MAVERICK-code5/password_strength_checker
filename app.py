from flask import Flask, render_template, request
import re
import math

app = Flask(__name__)

dictionary_words = {'password', 'admin', '123456', 'qwerty', 'letmein', 'welcome'}

def check_password_strength(password):
    feedback = []
    score = 0

    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
    else:
        feedback.append("Password is too short (min 8 characters).")

    if re.search(r'[A-Z]', password): score += 1
    else: feedback.append("Add uppercase letters.")
    if re.search(r'[a-z]', password): score += 1
    else: feedback.append("Add lowercase letters.")
    if re.search(r'[0-9]', password): score += 1
    else: feedback.append("Add digits.")
    if re.search(r'[^a-zA-Z0-9]', password): score += 1
    else: feedback.append("Add special characters (!@#$%^&*, etc).")

    if any(word in password.lower() for word in dictionary_words):
        feedback.append("Password contains a common word or pattern.")
        score -= 2

    return {
        'score': max(score, 0),
        'suggestions': feedback or ["Good job! Password looks strong."]
    }

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        password = request.form['password']
        result = check_password_strength(password)
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
