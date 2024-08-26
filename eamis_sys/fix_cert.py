import sys, importlib
from urllib3.exceptions import InsecureRequestWarning
from .utils import supress_warning

try:
    import pip_system_certs.wrapt_requests
    REQUESTS_CERTS_PATCHED = True
except ImportError: 
    REQUESTS_CERTS_PATCHED = False

if REQUESTS_CERTS_PATCHED:
    requests_loaded = 'requests' in sys.modules
    import requests
    if requests_loaded: importlib.reload(requests)
    del requests_loaded

if REQUESTS_CERTS_PATCHED:
    def patch_session(sess: requests.Session): pass
else:
    def patch_session(sess: requests.Session):
        sess.verify = False
        sess.request = supress_warning(InsecureRequestWarning)(sess.request)


__all__ = ['REQUESTS_CERTS_PATCHED', 'patch_session']
