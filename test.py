import os
import json


# REAL NDML CALL (will be used later)
from zeep import Client
from zeep.transports import Transport

NDML_WSDL = (
    "https://pilot.kra.ndml.in/sms-ws/PANServiceImplService/PANServiceImplService.wsdl"
)
client = Client(wsdl=NDML_WSDL, transport=Transport(timeout=30))
print(client.wsdl.dump())
