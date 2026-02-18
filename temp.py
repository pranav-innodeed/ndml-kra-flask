import xmltodict
import json

def xml_to_json(xml_string):
    return json.dumps(xmltodict.parse(xml_string), indent=2)


xml = """<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>\n<APP_RES_ROOT>\n    <APP_PAN_INQ>\n        <APP_IPV_FLAG></APP_IPV_FLAG>\n        <APP_KYC_MODE></APP_KYC_MODE>\n        <APP_PAN_NO>BZVPV6683D</APP_PAN_NO>\n        <APP_REQ_NO>263022949</APP_REQ_NO>\n        <APP_RES_NO>1015458160</APP_RES_NO>\n        <APP_STATUS>Not Available [Validation Pending with CAMS, CVL, KARVY KRA]</APP_STATUS>\n        <APP_STATUSDT></APP_STATUSDT>\n    </APP_PAN_INQ>\n</APP_RES_ROOT>\n"""

print(xml_to_json(xml))