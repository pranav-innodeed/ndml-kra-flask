import os
import xml.etree.ElementTree as ET

import requests


class NDMLClient:
    def __init__(self):
        self.use_mock = os.getenv("USE_MOCK", "true").lower() == "true"

    def call(self, method_name, xml_bytes):
        if self.use_mock:
            return self.mock_response(method_name, xml_bytes)

        xml = xml_bytes.decode("utf-8") if isinstance(xml_bytes, bytes) else xml_bytes

        # panInquiryDetailsTwo needs BP_ID (arg4). WSDL only declares arg0–arg3,
        # so zeep cannot call it correctly — use raw SOAP like pan-inquiry-detailed.
        if method_name == "panInquiryDetailsTwo":
            return self._call_pan_inquiry_details_two(xml)

        from zeep import Client
        from zeep.transports import Transport

        client = Client(wsdl=os.getenv("NDML_WSDL"), transport=Transport(timeout=30))

        enc_pwd = client.service.getPasscode(
            os.getenv("NDML_PASSWORD"), os.getenv("NDML_PASSKEY")
        )
        if not enc_pwd:
            raise ValueError(
                "getPasscode returned empty. Check NDML_PASSWORD / NDML_PASSKEY."
            )

        method = getattr(client.service, method_name)
        response = method(
            xml,
            os.getenv("NDML_USER_ID"),
            enc_pwd,
            os.getenv("NDML_PASSKEY"),
        )
        if response is None:
            raise ValueError(
                f"{method_name} returned empty response from NDML."
            )
        return response

    def _get_passcode_raw(self):
        url = os.getenv("NDML_ENDPOINT")
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
        headers = {
            "Content-Type": "text/xml;charset=UTF-8",
            "SOAPAction": "getPasscode",
        }
        response = requests.post(url, data=soap_body, headers=headers, timeout=30)
        root = ET.fromstring(response.text)
        enc_pwd = root.find(".//{*}return")
        if enc_pwd is None or not enc_pwd.text:
            raise ValueError(
                "getPasscode returned empty. Check NDML_PASSWORD / NDML_PASSKEY "
                f"and NDML_ENDPOINT. Raw: {response.text[:500]}"
            )
        return enc_pwd.text

    def _call_pan_inquiry_details_two(self, xml):
        enc_pwd = self._get_passcode_raw()
        url = os.getenv("NDML_ENDPOINT")
        soap_body = f"""
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                          xmlns:ns="http://service.webservice.pan.kra.ndml.com/">
           <soapenv:Header/>
           <soapenv:Body>
              <ns:panInquiryDetailsTwo>
                 <arg0><![CDATA[{xml}]]></arg0>
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
        root = ET.fromstring(response.text)
        result = root.find(".//{*}return")
        if result is None or result.text is None:
            raise ValueError(
                "panInquiryDetailsTwo returned empty from NDML. "
                f"Raw: {response.text[:500]}"
            )
        return result.text

    def mock_response(self, method_name, xml_bytes):
        received = (
            xml_bytes.decode("utf-8")
            if isinstance(xml_bytes, bytes)
            else xml_bytes
        )
        return {
            "mock": True,
            "method": method_name,
            "received_xml": received,
            "message": "This is a mock response. NDML not called.",
        }
