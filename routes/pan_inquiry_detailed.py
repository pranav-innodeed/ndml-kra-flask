from flask import Blueprint, request, jsonify
from services.ndml_client import NDMLClient
from services.xml_builder import pan_inquiry_detailed_xml
from services.utils import xml_to_json
import json

bp = Blueprint("pan_inquiry_detailed", __name__)
client = NDMLClient()

import requests
import os
import xml.etree.ElementTree as ET


def get_passcode():
    url = os.getenv("NDML_ENDPOINT")  # without ?wsdl

    soap_body = f"""
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                      xmlns:ns="http://service.webservice.pan.kra.ndml.com/">
       <soapenv:Header/>
       <soapenv:Body>
          <ns:getPasscode>
             <arg0>{os.getenv("NDML_PASSWORD")}</arg0>
             <arg1>{os.getenv("NDML_PASSKEY")}</arg1>
          </ns:getPasscode>
       </soapenv:Body>
    </soapenv:Envelope>
    """

    headers = {"Content-Type": "text/xml;charset=UTF-8", "SOAPAction": "getPasscode"}

    response = requests.post(url, data=soap_body, headers=headers, timeout=30)
    print(response.text)
    return response.text


def pan_inquiry(xml_bytes, enc_pwd):
    url = os.getenv("NDML_ENDPOINT")

    # soap_body = f"""
    # <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
    #                   xmlns:ns="http://service.webservice.pan.kra.ndml.com/">
    #    <soapenv:Header/>
    #    <soapenv:Body>
    #       <ns:panInquiryDetailsTwo>
    #          <arg0>{xml_bytes}</arg0>
    #          <arg1>{os.getenv("NDML_USER_ID")}</arg1>
    #          <arg2>{enc_pwd}</arg2>
    #          <arg3>{os.getenv("NDML_PASSKEY")}</arg3>
    #          <arg4>{os.getenv("BP_ID")}</arg4>
    #       </ns:panInquiryDetailsTwo>
    #    </soapenv:Body>
    # </soapenv:Envelope>
    # """
    soap_body = f"""
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                    xmlns:ns="http://service.webservice.pan.kra.ndml.com/">
    <soapenv:Header/>
    <soapenv:Body>
        <ns:panInquiryDetailsTwo>
            <arg0><![CDATA[{xml_bytes}]]></arg0>
            <arg1>{os.getenv("NDML_USER_ID")}</arg1>
            <arg2>{enc_pwd}</arg2>
            <arg3>{os.getenv("NDML_PASSKEY")}</arg3>
            <arg4>{os.getenv("BP_ID")}</arg4>
        </ns:panInquiryDetailsTwo>
    </soapenv:Body>
    </soapenv:Envelope>
    """

    headers = {
        "Content-Type": "text/xml;charset=UTF-8",
        "SOAPAction": "panInquiryDetailsTwo",
    }

    response = requests.post(url, data=soap_body, headers=headers, timeout=30)
    return response.text


@bp.route("/ndml/api/v1/pan-inquiry-detailed", methods=["POST"])
def pan_inquiry_detailed():
    try:
        data = request.json

        xml = pan_inquiry_detailed_xml(data["pan"], data["mobile"], data["request_no"])
        print(f"xml\n")
        print(xml)
        # response = client.call("panInquiryDetailsTwo", xml)
        # print(f"pan details response: {response}")
        enc_pwd = get_passcode()
        response_xml = enc_pwd
        root = ET.fromstring(response_xml)

        enc_pwd = root.find(".//return").text
        print("Encrypted Password:", enc_pwd)

        response = pan_inquiry(xml, enc_pwd)
        print(f"pan inquiry response: {response}")
        response = xml_to_json(response)
        response = {"status": "success", "data": json.loads(response)}
        return response, 200
    except Exception as e:
        response = {"status": "error", "message": str(e)}
        return response, 500
