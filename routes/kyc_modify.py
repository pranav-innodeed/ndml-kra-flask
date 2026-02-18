from flask import Blueprint, request, jsonify
from services.ndml_client import NDMLClient
from services.xml_builder import kyc_modify_xml
from services.utils import xml_to_json
import json
bp = Blueprint("kyc_modify", __name__)
client = NDMLClient()


@bp.route("/ndml/api/v1/kyc-modify", methods=["POST"])
def kyc_modify():
    try:
        data = request.json

        xml = kyc_modify_xml(data)

        print(f"kyc modify request: {xml}")
        response = client.call("processModification", xml)
        print(f"kyc modify response: {response}")
        response = xml_to_json(response)
        response = {"status": "success", "data": json.loads(response)}
        return response, 200
    except Exception as e:
        response = {"status": "error", "message": str(e)}
        return response, 500
