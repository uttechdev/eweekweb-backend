import re
from bson import ObjectId
from typing import List, Dict, Any
from datetime import datetime


def serialize_document(document):
    """Recursively convert MongoDB documents, handling ObjectId and datetime."""
    if isinstance(document, dict):
        for key, value in document.items():
            document[key] = serialize_document(value)
    elif isinstance(document, list):
        return [serialize_document(item) for item in document]
    elif isinstance(document, ObjectId):
        return str(document)
    elif isinstance(document, datetime):
        # Use .isoformat() to include the timezone information if present
        # Append 'Z' if datetime is naive (assumed to be in UTC)
        return document.isoformat() if document.tzinfo else document.isoformat() + 'Z'
    return document

def extract_url_from_html(html_string):
    """Extracts a URL from an HTML anchor tag string."""
    match = re.search(r'href="([^"]+)"', html_string)
    if match:
        return match.group(1)  # Returns the captured group from the regex, which is the URL.
    
    url_pattern = re.compile(r'https?://[^\s]+')
    if url_pattern.match(html_string):
        return html_string  # Return the input string if it matches a URL pattern
    
    return None  # Return None or an appropriate value if no URL is found.