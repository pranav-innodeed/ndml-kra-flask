from lxml import etree

def pan_inquiry_xml(pan, mobile, req_no):
    root = etree.Element("APP_REQ_ROOT")
    node = etree.SubElement(root, "APP_PAN_INQ")
    etree.SubElement(node, "APP_PAN_NO").text = pan
    etree.SubElement(node, "APP_MOBILE_NO").text = mobile
    etree.SubElement(node, "APP_REQ_NO").text = req_no
    return etree.tostring(root, encoding="utf-8")


def pan_inquiry_detailed_xml(pan, mobile, req_no):
    root = etree.Element("APP_REQ_ROOT")
    node = etree.SubElement(root, "APP_PAN_INQ_TWO")
    etree.SubElement(node, "APP_PAN_NO").text = pan
    etree.SubElement(node, "APP_MOBILE_NO").text = mobile
    etree.SubElement(node, "APP_REQ_NO").text = req_no
    return etree.tostring(root, encoding="utf-8")


def kyc_download_xml(pan, dob, mobile, request_no):
    from lxml import etree

    root = etree.Element("APP_REQ_ROOT")
    node = etree.SubElement(root, "APP_PAN_DOWN")

    etree.SubElement(node, "APP_PAN_NO").text = pan
    etree.SubElement(node, "APP_PAN_DOB").text = dob
    etree.SubElement(node, "APP_MOBILE_NO").text = mobile
    etree.SubElement(node, "APP_REQ_NO").text = request_no

    return etree.tostring(root, encoding="utf-8")


def kyc_register_xml(data):
    from lxml import etree

    root = etree.Element("APP_REQ_ROOT")
    node = etree.SubElement(root, "APP_PAN_INQ")

    for key, value in data.items():
        etree.SubElement(node, key).text = str(value)

    return etree.tostring(root, encoding="utf-8")


def kyc_modify_xml(data):
    from lxml import etree

    root = etree.Element("APP_REQ_ROOT")
    node = etree.SubElement(root, "APP_PAN_MOD")

    for key, value in data.items():
        etree.SubElement(node, key).text = str(value)

    return etree.tostring(root, encoding="utf-8")
