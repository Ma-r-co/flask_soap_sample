import xmltodict
import logging
from collections import defaultdict


def recursive_defaultdict():
    return defaultdict(recursive_defaultdict)


def multiply(data: bytes) -> str:
    result = "<a> no data ingested </a>"
    try:
        in_xml = xmltodict.parse(data)
        intA = in_xml["soapenv:Envelope"]["soapenv:Body"]["tem:Multiply"]["tem:intA"]
        intB = in_xml["soapenv:Envelope"]["soapenv:Body"]["tem:Multiply"]["tem:intB"]
        res_soap_data = recursive_defaultdict()
        res_soap_data["soap:Envelope"][
            "@xmlns:soap"
        ] = "http://schemas.xmlsoap.org/soap/envelope/"
        res_soap_data["soap:Envelope"][
            "@xmlns:xsi"
        ] = "http://www.w3.org/2001/XMLSchema-instance"
        res_soap_data["soap:Envelope"][
            "@xmlns:xsd"
        ] = "http://www.w3.org/2001/XMLSchema"
        res_soap_data["soap:Envelope"]["soap:Body"]["MultiplyResponse"][
            "@xmlns"
        ] = "http://tempuri.org/"
        res_soap_data["soap:Envelope"]["soap:Body"]["MultiplyResponse"][
            "MultiplyResult"
        ] = int(intA) * int(intB)
        result = xmltodict.unparse(res_soap_data, pretty=True, indent="  ")
    except (Exception, ValueError) as ex:
        logging.getLogger().warn("Error parsing xml payload: " + str(ex))
    return result
