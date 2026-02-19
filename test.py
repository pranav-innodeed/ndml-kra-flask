import xml.etree.ElementTree as ET


response = """<?xml version="1.0" encoding="UTF-8"?><soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"><soapenv:Body><ns2:getPasscodeResponse xmlns:ns2="http://service.webservice.pan.kra.ndml.com/"><return>Tn4HvEiLv2ngR/AS2rU88Q==</return></ns2:getPasscodeResponse></soapenv:Body></soapenv:Envelope>"""
response_xml = response
root = ET.fromstring(response_xml)

enc_pwd = root.find(".//return").text
print("Encrypted Password:", enc_pwd)
