from flask import Flask, request, render_template
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "Backend is running."

@app.route("/submit", methods=["POST"])
def submit():
    data = request.form

    # Applicant info
    name = data.get("name")
    email = data.get("email")
    phone = data.get("phone")
    grade = data.get("grade")
    syllabus = data.get("syllabus")
    session = data.get("session")
    motivation = data.get("motivation")

    # Financial aid info (optional)
    aid_name = data.get("aid_name")
    income = data.get("income")
    members = data.get("family_members")
    reason = data.get("reason")
    partial = data.get("partial_aid")

    # Compose email
    subject = f"New Application from {name}"
    body = f"""
    --- Applicant Info ---
    Name: {name}
    Email: {email}
    Phone: {phone}
    Grade: {grade}
    Syllabus: {syllabus}
    Session: {session}
    Motivation: {motivation}

    --- Financial Aid Info ---
    Aid Name: {aid_name}
    Family Income: {income}
    Family Members: {members}
    Reason: {reason}
    Partial Aid Sufficient: {partial}
    """

    send_email(subject, body)
    return render_template("success.html", name=name)

def send_email(subject, body):
    sender = os.environ.get("SENDER_EMAIL")
    password = os.environ.get("SENDER_PASSWORD")
    receiver = os.environ.get("RECEIVER_EMAIL")

    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = receiver
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.send_message(msg)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
