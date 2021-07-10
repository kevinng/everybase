def get_twilml_body(
        twilml: str
    ) -> str:
    """Extract body from TwilML"""
    start_pos = twilml.index('<Message>') + len('<Message>')
    end_pos = twilml.index('</Message>')
    return twilml[start_pos:end_pos]