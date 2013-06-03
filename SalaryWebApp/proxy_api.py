
import urllib.parse, urllib.request
import json

def proxy_api_call(method, params):
    try:
        url = 'http://localhost:8084/?method={0}'.format(method)
        data = urllib.parse.urlencode(params)
        bin_data = data.encode('ascii')
        request = urllib.request.Request(url, bin_data, method='POST')
        response = urllib.request.urlopen(request)
        payload = response.read().decode('utf-8')
        return json.loads(payload)
    except Exception:
        raise AssertionError('Unable to call proxy API')
