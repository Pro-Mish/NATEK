from flask import Flask, render_template, request, redirect, url_for, flash
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import dotenv


# Load environment variables from .env file
dotenv.load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')  # Needed for flashing messages

# Configure your email settings
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL_ADDRESS = 'mishackmadubandlela@gmail.com'      # Replace with your email
EMAIL_PASSWORD = os.getenv('APP_PASSWORD')        # Use App Password if using Gmail

@app.route('/')
def hindex():
    return render_template('hindex.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    email = request.form.get('email')
    subject = request.form.get('subject')
    message = request.form.get('message')

    try:
        # Construct the email
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = EMAIL_ADDRESS
        msg['Subject'] = f"New Contact Form Submission: {subject}"

        body = f"""
        Name: {name}
        Email: {email}
        Subject: {subject}
        Message:
        {message}
        """

        msg.attach(MIMEText(body, 'plain'))

        # Send the email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)

        flash('Message sent successfully!', 'success')

    except Exception as e:
        print(f"Error: {e}")
        flash('Failed to send message.', 'danger')

    return redirect(url_for('hindex'))

if __name__ == '__main__':
    app.run(debug=True)