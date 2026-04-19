import socket
import re
from urllib.parse import urlparse
from django.core.exceptions import ValidationError
from django.conf import settings

def validate_url(url):
    """
    Validates that a URL is well-formed, uses http/https, 
    and is not pointing to a private internal network (unless allowed).
    """
    if not url:
        raise ValidationError("URL cannot be empty.")
    
    parsed = urlparse(url)
    if parsed.scheme not in ['http', 'https']:
        raise ValidationError("URL must use http or https scheme.")
    
    if not parsed.netloc:
        raise ValidationError("Invalid URL structure.")
    
    # Resolve hostname
    try:
        hostname = parsed.hostname
        ip = socket.gethostbyname(hostname)
    except Exception:
        raise ValidationError(f"Could not resolve hostname: {parsed.hostname}")
    
    # Private IP range check
    is_private = False
    if ip.startswith('127.') or ip.startswith('10.') or ip.startswith('192.168.'):
        is_private = True
    elif ip.startswith('172.'):
        # 172.16.0.0 – 172.31.255.255
        second_octet = int(ip.split('.')[1])
        if 16 <= second_octet <= 31:
            is_private = True
            
    if is_private and not getattr(settings, 'ALLOW_INTERNAL_SCAN', False):
        raise ValidationError(f"Scanning internal IP addresses ({ip}) is not allowed.")
    
    return True

def validate_repo(repo_url):
    """
    Validates that a repository URL is a valid GitHub or GitLab URL.
    """
    if not repo_url:
        raise ValidationError("Repository URL cannot be empty.")
    
    patterns = [
        r'^https?://github\.com/[\w\-\.]+ / [\w\-\.]+$',
        r'^https?://gitlab\.com/[\w\-\./]+$'
    ]
    
    is_valid = any(re.match(pattern, repo_url) for pattern in patterns)
    if not is_valid:
        raise ValidationError("Invalid repository URL. Must be a valid GitHub or GitLab URL.")
    
    return True

def validate_file(file_content):
    if not file_content:
        raise ValidationError("File content cannot be empty.")
    
    # Enforce 5MB limit
    if len(file_content.encode('utf-8')) > 5 * 1024 * 1024:
        raise ValidationError("File exceeds 5MB limit.")

    try:
        if isinstance(file_content, bytes):
            file_content.decode('utf-8')
        else:
            str(file_content).encode('utf-8').decode('utf-8')
    except UnicodeDecodeError:
        raise ValidationError("Only text/source code files are allowed.")

    return True
