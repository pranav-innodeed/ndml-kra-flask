from flask import Blueprint, request, jsonify
from services.ndml_client import NDMLClient
from services.xml_builder import pan_inquiry_detailed_xml

bp = Blueprint("pan_inquiry_detailed", __name__)
client = NDMLClient()

@bp.route("/ndml/api/v1/pan-inquiry-detailed", methods=["POST"])
def pan_inquiry_detailed():
    data = request.json

    xml = pan_inquiry_detailed_xml(
        data["pan"],
        data["mobile"],
        data["request_no"]
    )

    response = client.call(
        "panInquiryDetailsTwo",
        xml
    )

    return jsonify(response)
