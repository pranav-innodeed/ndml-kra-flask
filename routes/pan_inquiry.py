from flask import Blueprint, request, jsonify
from services.ndml_client import NDMLClient
from services.xml_builder import pan_inquiry_xml
from services.utils import xml_to_json

bp = Blueprint("pan_inquiry", __name__)
client = NDMLClient()


@bp.route("/ndml/api/v1/pan-inquiry", methods=["POST"])
def pan_inquiry():
    try:
        data = request.json

        xml = pan_inquiry_xml(data["pan"], data["mobile"], data["request_no"])

        response = client.call("panInquiryDetails", xml)
        print(f"pan inquiry response: {response}")
        response = xml_to_json(response)
        response = {"status": "success", "data": response}
        return response, 200
    except Exception as e:
        response = {"status": "error", "message": str(e)}
        return response, 500
