from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message
import pickle
import os
import numpy as np

# Initialize Flask app
app = Flask(__name__)
app.secret_key = "Sakthi@123" 

# Flask-Mail Configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'sakthidhanaraj123@gmail.com'  
app.config['MAIL_PASSWORD'] = 'qrvekdcioypotnlk' 
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)

# Load the trained model with error handling
model = pickle.load(open('dib.pkl', 'rb'))


# Transaction type mapping
transaction_map = {
    "CASH_IN": 3,
    "CASH_OUT": 1,
    "DEBIT": 5,
    "PAYMENT": 2,
    "TRANSFER": 4
}

# Admin login credentials
ADMIN_USERNAME = "USER"
ADMIN_PASSWORD_HASH = generate_password_hash("Sakthi@123")

@app.route('/')
def main():
    return render_template('main1.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == ADMIN_USERNAME and check_password_hash(ADMIN_PASSWORD_HASH, password):
            session['admin_logged_in'] = True
            return render_template('main2.html')
        else:
            return render_template('main1.html', error="Invalid credentials")

    return render_template('main1.html')

@app.route('/main')
def main1():
    return render_template('main2.html')

@app.route('/mm')
def mm():
    return render_template('index.html')

# Function to send fraud alert email
def send_fraud_alert(email, transaction_type, amount, old_balance, new_balance):
    msg = Message(
        subject="Fraud Alert: Suspicious Transaction Detected",
        sender="sakthidhanaraj123@gmail.com",
        recipients=[email]
    )
    msg.body = f"""
We have detected a potentially fraudulent transaction in our system. Please review the details below and take the necessary actions immediately.

**Transaction Details:**
- **Transaction Type:** {transaction_type}
- **Amount:** {amount}
- **Old Balance:** {old_balance}
- **New Balance:** {new_balance}

**Risk Status:** This transaction has been flagged as **potentially fraudulent** by our system.

**Recommended Action:**
- Please log in to the admin portal and review the transaction history.
- If this transaction is unauthorized, take immediate action to block the account.
- Contact the user for verification if necessary.

If you believe this alert was triggered by mistake, please report it to the security team.

For any further assistance, feel free to reach out.

Best regards,  
User 
Fraud Detection System  
"""

    try:
        mail.send(msg)
        print(f"Fraud alert email sent to {email}")
    except Exception as e:
        print(f"Error sending fraud alert email: {str(e)}")

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return "Model not loaded! Cannot make predictions."

    transaction_type = request.form['a']
    amount = float(request.form['b'])
    old_balance = float(request.form['c'])
    new_balance = float(request.form['d'])

    transaction_type_num = transaction_map.get(transaction_type, -1)

    if transaction_type_num == -1:
        return "Invalid transaction type selected."

    arr = np.array([[transaction_type_num, amount, old_balance, new_balance]])
    pred = model.predict(arr)

    if pred[0] == 1:
        result = "This is a fraudulent transaction!"

        send_fraud_alert("sakthidhanaraj123@gmail.com", transaction_type, amount,old_balance, new_balance)
    else:
        result = "This is a non-fraudulent transaction."

    return render_template('result.html', data=result)

@app.route('/insights')
def insight():
    return render_template('insight.html')

@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('login'))

@app.route('/Faqs')
def faq():
    return render_template('Faq.html')

if __name__ == "__main__":
    app.run(debug=True)  