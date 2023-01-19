import urllib3

timeout = urllib3.util.Timeout(connect=2.0, read=7.0)

http = urllib3.PoolManager(timeout=timeout)

resp = http.request("GET", "https://example.com/")

print(resp.status)