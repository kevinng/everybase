import xml.etree.ElementTree as ET

def get_twilml_body(
        twilml: str
    ) -> str:
    """Extract body from TwilML"""
    root = ET.fromstring(twilml)
    return root.find('Message').text