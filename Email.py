
from flask import Flask, request, render_template
import ssl
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)

# Replace with your credentials
sender_email = ///
sender_password = ///
# recipient_email = "abdalazizshtia@gmail.com"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/send_email", methods=["POST"])
def send_email():
    recipient_email = request.form["recipient_email"]
    subject = request.form["subject"]
    body = request.form["body"]
    file = request.files["file"]

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    with file.stream as attachment:
        part = MIMEApplication(attachment.read(), Name=file.filename)
        part["Content-Disposition"] = f'attachment; filename="{file.filename}"'
        msg.attach(part)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
        smtp.login(sender_email, sender_password)
        smtp.send_message(msg)

    return "Email sent successfully."


if __name__ == "__main__":
    app.run(debug=True)
