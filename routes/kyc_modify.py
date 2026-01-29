from flask import Blueprint, request, jsonify
from services.ndml_client import NDMLClient
from services.xml_builder import kyc_modify_xml

bp = Blueprint("kyc_modify", __name__)
client = NDMLClient()

@bp.route("/kyc-modify", methods=["POST"])
def kyc_modify():
    data = request.json

    xml = kyc_modify_xml(data)

    response = client.call(
        "processModification",
        xml
    )

    return jsonify(response)
