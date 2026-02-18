import os
from lxml import etree

def xml_to_dict(element):
    """Convert XML element to dictionary recursively."""
    result = {}
    
    # Process child elements
    children = list(element)
    
    if children:
        # Element has children - process them
        for child in children:
            child_tag = child.tag
            child_data = xml_to_dict(child)
            
            # If multiple children with same tag, make it a list
            if child_tag in result:
                if not isinstance(result[child_tag], list):
                    result[child_tag] = [result[child_tag]]
                result[child_tag].append(child_data)
            else:
                result[child_tag] = child_data
        
        # Add attributes if present
        if element.attrib:
            result['_attributes'] = element.attrib
        
        return result
    
    # Leaf element - no children
    # Get text content (handle None and empty strings)
    text_content = element.text.strip() if element.text and element.text.strip() else ""
    
    # Add attributes if present
    if element.attrib:
        if text_content:
            result['_text'] = text_content
        result['_attributes'] = element.attrib
        return result if result else text_content
    
    # Return text content or empty string for empty elements
    return text_content

def parse_xml_response(response):
    """Parse XML response to JSON-compatible dictionary."""
    # If already a dict, return as-is
    if isinstance(response, dict):
        return response
    
    # If None or empty, return empty dict
    if not response:
        return {}
    
    # Handle zeep objects (structured objects from SOAP)
    try:
        from zeep.helpers import serialize_object
        # Convert zeep object to dict
        serialized = serialize_object(response)
        return serialized
    except (ImportError, AttributeError, TypeError):
        pass
    
    # Handle XML strings
    try:
        xml_str = response
        # If it's bytes, decode it
        if isinstance(xml_str, bytes):
            xml_str = xml_str.decode('utf-8')
        
        # If it's a string, parse as XML
        if isinstance(xml_str, str):
            root = etree.fromstring(xml_str.encode('utf-8'))
            return xml_to_dict(root)
    except (etree.XMLSyntaxError, ValueError, TypeError):
        pass
    
    # If all parsing fails, try to convert to string representation
    try:
        # Try to get string representation
        if hasattr(response, '__dict__'):
            return response.__dict__
        return {"response": str(response)}
    except Exception as e:
        return {
            "raw_response": str(response),
            "parse_error": str(e)
        }

class NDMLClient:
    def __init__(self):
        self.use_mock = os.getenv("USE_MOCK", "true").lower() == "true"

    def call(self, method_name, xml_bytes):
        if self.use_mock:
            return self.mock_response(method_name, xml_bytes)

        # REAL NDML CALL (will be used later)
        from zeep import Client
        from zeep.transports import Transport


        client = Client(
            wsdl=os.getenv("NDML_WSDL"),
            transport=Transport(timeout=30)
        )

        enc_pwd = client.service.getPasscode(
            os.getenv("NDML_PASSWORD"),
            os.getenv("NDML_PASSKEY")
        )

        method = getattr(client.service, method_name)
        response = method(
            xml_bytes,
            os.getenv("NDML_USER_ID"),
            enc_pwd,
            os.getenv("NDML_PASSKEY")
        )
        print(response)
        # Parse XML response to JSON
        return parse_xml_response(response)

    def mock_response(self, method_name, xml_bytes):
        return {
            "mock": True,
            "method": method_name,
            "received_xml": xml_bytes.decode("utf-8"),
            "message": "This is a mock response. NDML not called."
        }
