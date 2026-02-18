from flask import Flask
from dotenv import load_dotenv

from routes.pan_inquiry import bp as pan_inquiry
from routes.pan_inquiry_detailed import bp as pan_inquiry_detailed
from routes.kyc_download import bp as kyc_download
from routes.kyc_register import bp as kyc_register
from routes.kyc_modify import bp as kyc_modify

load_dotenv()

app = Flask(__name__)

app.register_blueprint(pan_inquiry)
app.register_blueprint(pan_inquiry_detailed)
app.register_blueprint(kyc_download)
app.register_blueprint(kyc_register)
app.register_blueprint(kyc_modify)

if __name__ == "__main__":
    app.run(debug=True, port=8080)
