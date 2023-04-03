# lxml
from lxml import etree
from lxml.builder import E, ElementMaker

# xmltag
from .xmltag import XmlTag

# typing
from typing import Tuple

PATH_TO_WSDL = "./src/tempconvert.wsdl"


def celsius2fahrenheit(data: bytes) -> bytes:
    xsd_validator = get_xsd_validator(PATH_TO_WSDL)
    try:
        request_xml = etree.fromstring(data)
    except etree.ParseError as e:
        return generate_soap_fault(str(e))

    try:
        soap_message = request_xml.find("soap:Body/*", namespaces=request_xml.nsmap)
        if soap_message is None:
            raise etree.DocumentInvalid("something wrong")
        xsd_validator.assertValid(soap_message)
        cdegree_text = soap_message.findtext(
            "ns:Celsius", namespaces=soap_message.nsmap
        )
        if cdegree_text is None:
            raise etree.DocumentInvalid("Value is empty or non-numeric.")
        cdegree = float(cdegree_text)
    except (etree.DocumentInvalid, ValueError) as e:
        return generate_soap_response(str(e))

    return generate_soap_response(str(c2f(cdegree)))


def get_xsd_validator(path_to_wsdl: str) -> etree.XMLSchema:
    wsdl = etree.parse(path_to_wsdl)
    xmlschema_doc = wsdl.find("wsdl:types/s:schema", namespaces=wsdl.getroot().nsmap)
    if xmlschema_doc is None:
        raise Exception('Cannot locate "wsdl:types/s:schema in ' + path_to_wsdl)
    return etree.XMLSchema(xmlschema_doc)


def generate_soap_response(fdegree: str) -> bytes:
    soap_env = XmlTag.soap_Envelope(
        XmlTag.soap_Body(
            XmlTag.CelsiusToFahrenheitResponse(
                XmlTag.CelsiusToFahrenheitResult(fdegree)
            )
        )
    )
    return etree.tostring(soap_env, xml_declaration=True, encoding="utf-8")


def generate_soap_fault(message: str) -> bytes:
    soap_env = XmlTag.soap_Envelope(
        XmlTag.soap_Body(
            XmlTag.soap_Fault(
                XmlTag.soap_Code(XmlTag.soap_Value("soap:Receiver")),
                XmlTag.soap_Reason(XmlTag.soap_Text(message)),
                XmlTag.soap_Detail(),
            )
        )
    )
    return etree.tostring(soap_env, xml_declaration=True, encoding="utf-8")


def c2f(cdegree: float) -> float:
    return (cdegree * 1.8) + 32.0
