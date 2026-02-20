from flask import Blueprint, request, jsonify
from services.ndml_client import NDMLClient
from services.xml_builder import pan_inquiry_detailed_xml
from services.utils import xml_to_json
import json

bp = Blueprint("pan_inquiry_detailed2", __name__)
client = NDMLClient()

import requests
import os
import xml.etree.ElementTree as ET


@bp.route("/ndml/api/v1/pan-inquiry-detailed2", methods=["POST"])
def pan_inquiry_detailed2():
    try:
        data = request.json

        xml = pan_inquiry_detailed_xml(data["pan"], data["mobile"], data["request_no"])

        response = client.call("panInquiryDetailsTwo", xml)
        print(f"pan details response: {response}")
        response = xml_to_json(response)
        response = {"status": "success", "data": response}
        return response, 200
    except Exception as e:
        response = {"status": "error", "message": str(e)}
        return response, 500
