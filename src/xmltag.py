from lxml.builder import E, ElementMaker


class XmlTag:
    # soap envelope
    _E_soap = ElementMaker(
        namespace="http://www.w3.org/2003/05/soap-envelope",
        nsmap={
            "soap": "http://www.w3.org/2003/05/soap-envelope",
            "xml": "http://www.w3.org/XML/1998/namespace",
        },
    )
    # _E_xml = ElementMaker(
    #     namespace="http://www.w3.org/XML/1998/namespace",
    #     nsmap={"xml": "http://www.w3.org/XML/1998/namespace"},
    # )
    soap_Envelope = _E_soap.Envelope
    soap_Body = _E_soap.Body
    soap_Fault = _E_soap.Fault
    soap_Code = _E_soap.Code
    soap_Value = _E_soap.Value
    soap_Reason = _E_soap.Reason
    soap_Text = lambda x: XmlTag._E_soap.Text(
        x, {"{http://www.w3.org/XML/1998/namespace}lang": "en-US"}
    )
    soap_Detail = _E_soap.Detail

    # c2f
    CelsiusToFahrenheitResponse = lambda x: E.CelsiusToFahrenheitResponse(
        x, {"xmlns": "https://www.w3schools.com/xml/"}
    )
    CelsiusToFahrenheitResult = lambda x: E.CelsiusToFahrenheitResult(x)
