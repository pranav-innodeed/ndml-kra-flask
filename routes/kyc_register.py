from flask import Blueprint, request, jsonify
from services.ndml_client import NDMLClient
from services.xml_builder import kyc_register_xml
from services.utils import xml_to_json
import json
bp = Blueprint("kyc_register", __name__)
client = NDMLClient()


@bp.route("/ndml/api/v1/kyc-register", methods=["POST"])
def kyc_register():
    try:
        data = request.json

        xml = kyc_register_xml(data)

        print(f"kyc register request: {xml}")
        response = client.call("registration", xml)
        print(f"kyc register response: {response}")
        response = xml_to_json(response)
        response = {"status": "success", "data": json.loads(response)}
        return response, 200
    except Exception as e:
        response = {"status": "error", "message": str(e)}
        return response, 500
