import xmltodict
import json

# Convert XML to JSON
def xml_to_json(xml_string):
    return json.dumps(xmltodict.parse(xml_string), indent=2)
