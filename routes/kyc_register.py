from flask import Blueprint, request, jsonify
from services.ndml_client import NDMLClient
from services.xml_builder import kyc_register_xml

bp = Blueprint("kyc_register", __name__)
client = NDMLClient()

@bp.route("/ndml/api/v1/kyc-register", methods=["POST"])
def kyc_register():
    data = request.json

    xml = kyc_register_xml(data)

    response = client.call(
        "registration",
        xml
    )

    return jsonify(response)
