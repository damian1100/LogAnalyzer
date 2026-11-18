"""Regular expressions used to recognize Common/Combined Log Format records."""
import re

# Named groups make extracted fields self-documenting.
ACCESS_LOG_RE = re.compile(
    r'(?P<ip>(?:\d{1,3}\.){3}\d{1,3})\s+'
    r'(?P<ident>\S+)\s+(?P<user>\S+)\s+'
    r'\[(?P<timestamp>[^\]]+)\]\s+'
    r'"(?P<method>GET|POST|PUT|DELETE|PATCH|HEAD|OPTIONS)\s+'
    r'(?P<url>\S+)\s+HTTP/(?P<http_version>\d\.\d)"\s+'
    r'(?P<status>\d{3})\s+(?P<size>\d+|-)'
)
EMAIL_RE = re.compile(r'(?P<local>[A-Za-z0-9._%+-]+)@(?P<domain>[A-Za-z0-9.-]+\.[A-Za-z]{2,})')
DATE_RE = re.compile(r'(?P<day>\d{2})/(?P<month>[A-Za-z]{3})/(?P<year>\d{4})')
IP_VALIDATION_RE = re.compile(r'^(?:\d{1,3}\.){3}\d{1,3}$')


def is_valid_ipv4(value: str) -> bool:
    """Validate IPv4 octet ranges, not only the dotted shape."""
    if not IP_VALIDATION_RE.fullmatch(value):
        return False
    return all(0 <= int(part) <= 255 for part in value.split("."))
