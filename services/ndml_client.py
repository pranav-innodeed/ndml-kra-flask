import os

class NDMLClient:
    def __init__(self):
        self.use_mock = os.getenv("USE_MOCK", "true").lower() == "true"

    def call(self, method_name, xml_bytes):
        if self.use_mock:
            return self.mock_response(method_name, xml_bytes)

        # REAL NDML CALL (will be used later)
        from requests import Session
        from zeep import Client
        from zeep.transports import Transport

        session = Session()
        server_ip = os.getenv("SERVERIP")
        if server_ip:
            session.headers.update({"SERVERIP": server_ip})

        client = Client(
            wsdl=os.getenv("NDML_WSDL"),
            transport=Transport(session=session, timeout=30)
        )

        enc_pwd = client.service.getPasscode(
            os.getenv("NDML_PASSWORD"),
            os.getenv("NDML_PASSKEY")
        )

        method = getattr(client.service, method_name)
        return method(
            xml_bytes,
            os.getenv("NDML_USER_ID"),
            enc_pwd,
            os.getenv("NDML_PASSKEY")
        )

    def mock_response(self, method_name, xml_bytes):
        return {
            "mock": True,
            "method": method_name,
            "received_xml": xml_bytes.decode("utf-8"),
            "message": "This is a mock response. NDML not called."
        }
