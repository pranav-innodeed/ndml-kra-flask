from flask import Blueprint, request, jsonify
from services.ndml_client import NDMLClient
from services.xml_builder import kyc_download_xml
from services.utils import xml_to_json
import json
bp = Blueprint("kyc_download", __name__)
client = NDMLClient()


@bp.route("/ndml/api/v1/kyc-download", methods=["POST"])
def kyc_download():
    try:
        data = request.json

        xml = kyc_download_xml(
            pan=data["pan"],
            dob=data["dob"],
            mobile=data["mobile"],
            request_no=data["request_no"],
        )

        print(f"kyc download request: {xml}")
        response = client.call("panDownloadDetailsComplete", xml)
        print(f"kyc download response: {response}")
        response = xml_to_json(response)
        response = {"status": "success", "data": json.loads(response)}
        return response, 200
    except Exception as e:
        response = {"status": "error", "message": str(e)}
        return response, 500
