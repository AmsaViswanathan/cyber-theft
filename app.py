from flask import Flask, render_template, request, redirect, url_for, session, flash
import joblib
import os
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Load the trained model
model = joblib.load('model.pkl')

# Upload config
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # 2 MB max


# ----------- Utility Functions -----------

def validate_user(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    result = cursor.fetchone()
    conn.close()
    return result is not None


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'txt'
import random  # Add this if not already imported

suspicious_reasons = [
    "Contains phishing keywords like 'urgent', 'verify your account', 'click here'.",
    "Suspicious punctuation or capitalization detected.",
    "Deceptive URL or domain pattern found.",
    "Grammar mistakes typical of fake messages.",
    "Threatening tone detected such as 'your account will be blocked'.",
    "Abnormal pattern matched from phishing dataset.",
    "Includes financial urgency such as 'lottery' or 'reward'.",
    "Message structure matches known phishing style.",
    "Requests for sensitive personal info detected.",
    "Emotional manipulation found like 'congrats you’ve been selected'."
]

safe_reasons = [
    "Content uses neutral and clean language.",
    "No phishing trigger keywords found.",
    "No masked or fake links detected.",
    "Grammar and punctuation appear normal.",
    "No phishing features matched from dataset.",
    "Message doesn’t request private data.",
    "Tone is friendly or informative.",
    "Message structure is standard.",
    "Prediction confidence high with no red flags.",
    "Appears to be a normal message."
]
phishing_keywords = [
    "urgent", "verify", "click", "update", "account", "login",
    "limited time", "confirm", "alert", "security", "dear customer",
    "transaction", "withdrawn", "available balance", "block your card",
    "call", "forward this", "not withdrawn by you"
]
def extract_reason(text):
    matched = []
    for word in phishing_keywords:
        if word.lower() in text.lower():
            matched.append(word)
    if matched:
        return "Contains suspicious keywords: " + ", ".join(matched)
    else:
        return "No suspicious patterns were detected."


def extract_reason(text):
    matched = []
    for word in phishing_keywords:
        if word.lower() in text.lower():
            matched.append(word)

    if matched:
        return (
            f"⚠️ The message contains potentially suspicious keywords: {', '.join(matched)}.\n"
            "Please verify the sender's email address and the context before clicking or replying."
        )
    else:
        return "✅ No suspicious patterns were detected."


# ----------- Routes -----------

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if validate_user(username, password):
            session['user'] = username
            return redirect(url_for('home'))
        else:
            error = 'Invalid username or password'
            return render_template('login.html', error=error, page='login', title='')
    return render_template('login.html', page='login', title=' ')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash("Username and password are required.")
            return redirect(url_for('register'))

        try:
            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            conn.close()
            flash("Registration successful. Please login.")
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash("Username already exists. Please choose another.")
            return redirect(url_for('register'))

    return render_template('register.html', page='register', title='')


@app.route('/home')
def home():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('home.html', user=session['user'], page='home', title='')


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        file = request.files.get('file')
        if file and allowed_file(file.filename):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            with open(filepath, 'r', encoding='utf-8') as f:
                text = f.read()

            prediction = model.predict([text])[0]
            status = "Safe ✅" if prediction == 0 else "Suspicious ⚠️"

            reason = "This file has spam-like content and suspicious keywords." if prediction == 1 else "No threat detected in uploaded file."

            os.remove(filepath)
            return render_template('result.html', data=text, result=status, reason=reason, page='result')
    return render_template('upload.html', page='upload')


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    results = []
    if request.method == 'POST':
        file = request.files['file']
        if file.filename != '':
            # Read file as dataframe
            df = pd.read_csv(file, header=None, names=["message"])

            for msg in df['message']:
                # Vectorize each message
                vector = vectorizer.transform([msg])
                pred = model.predict(vector)[0]
                prob = model.predict_proba(vector)[0]

                # Reason - top keywords
                reason = []
                for word in msg.split():
                    if word.lower() in vectorizer.get_feature_names_out():
                        reason.append(word)

                result = {
                    "message": msg,
                    "prediction": "Suspicious ⚠️" if pred == 1 else "Safe ✅",
                    "confidence": f"{max(prob) * 100:.2f}%",
                    "reason": ", ".join(reason) if reason else "No phishing keywords"
                }
                results.append(result)
    return render_template("upload_result.html", results=results)
@app.route('/result', methods=['POST'])
def result():
    if 'user' not in session:
        return redirect(url_for('login'))

    input_text = request.form.get('input_data')
    prediction = model.predict([input_text])[0]
    proba = model.predict_proba([input_text])[0]  # confidence level

    confidence = round(max(proba) * 100, 2)

    if prediction == 0:
        status = "Safe ✅"
        reason = """✅ No suspicious patterns were detected in the message.

  Why it's safe:
- No keywords like 'urgent', 'click here', 'verify', 'account suspended'.
- Tone is informative and professional.
- Message includes organization name, event details, or contact info.
- URLs are proper and not suspicious or shortened.
- No requests for passwords, OTPs, or bank info."""
    else:
        reason = """⚠️ This message contains phishing or suspicious keywords.

 Why it's suspicious:
- Words like 'urgent', 'verify your account', or 'click here' found.
- Tries to create urgency or fear (like 'account blocked').
- Suspicious or shortened links detected.
- Might request personal or banking information.
- Not from verified or known source."""
        status = "Suspicious ⚠️"

    return render_template('result.html',
                           data=input_text,
                           result=status,
                           confidence=confidence,
                           reason=reason,
                           page='result')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


# ----------- Main -----------

if __name__ == '__main__':
    app.run(debug=True)
