from flask import Blueprint, request, jsonify
from services.ndml_client import NDMLClient
from services.xml_builder import kyc_download_xml

bp = Blueprint("kyc_download", __name__)
client = NDMLClient()

@bp.route("/ndml/api/v1/kyc-download", methods=["POST"])
def kyc_download():
    data = request.json

    xml = kyc_download_xml(
        pan=data["pan"],
        dob=data["dob"],
        mobile=data["mobile"],
        request_no=data["request_no"]
    )

    response = client.call(
        "panDownloadDetailsComplete",
        xml
    )

    return jsonify(response)
