import xml.etree.ElementTree as ET

def get_twilml_body(
        twilml : str
    ) -> str:
    """Extract message body from TwilML.
    
    Parameters
    ----------
    twilml
        TwilML string.

    Returns
    -------
    message
        Message body.
    """
    root = ET.fromstring(twilml)
    return root.find('Message').text