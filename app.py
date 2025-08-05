from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("kaibbrultvtxxeks")
TO_EMAIL = "digvijaybhati33@gmail.com"  # Your email to receive order details

@app.route("/checkout", methods=["POST"])
def checkout():
    data = request.json
    name = data.get("name")
    phone = data.get("phone")
    email = data.get("email")
    address = data.get("address")
    pincode = data.get("pincode")
    product = data.get("product")

    if not all([name, phone, email, address, pincode, product]):
        return jsonify({"success": False, "message": "Missing required fields"}), 400

    subject = f"🛒 New Order: {product}"
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = EMAIL_USER
    message["To"] = TO_EMAIL

    html = f"""
    <html>
      <body>
        <h2>New Order Received</h2>
        <p><strong>Product:</strong> {product}</p>
        <p><strong>Name:</strong> {name}</p>
        <p><strong>Phone:</strong> {phone}</p>
        <p><strong>Email:</strong> {email}</p>
        <p><strong>Address:</strong> {address}</p>
        <p><strong>Pincode:</strong> {pincode}</p>
      </body>
    </html>
    """

    message.attach(MIMEText(html, "html"))

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(EMAIL_USER, EMAIL_PASS)
            server.sendmail(EMAIL_USER, TO_EMAIL, message.as_string())

        return jsonify({"success": True, "message": "Order placed successfully!"})
    except Exception as e:
        print("Error sending email:", e)
        return jsonify({"success": False, "message": "Error placing order."}), 500

if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, render_template, jsonify
import os
import requests
from dotenv import load_dotenv

# Load from .env file
load_dotenv()

app = Flask(__name__)
API_KEY = os.getenv("API_KEY")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/data/<city>")
def get_data(city):
    url = f"https://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}"
    res = requests.get(url)
    return jsonify(res.json())

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # use PORT from Render, fallback to 5000
    app.run(host="0.0.0.0", port=port)

