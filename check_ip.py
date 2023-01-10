import requests
proxy_url = "wan.100009773418904.ldproxy.com:14222"


def check_proxy():
    print("Checking proxy .....")
    for i in range(4000,10000):
        PROXY = f"100009773418904.ldproxy.com:{i}"
        status_proxy_url = f"http://{proxy_url}/status?proxy={PROXY}"
        resp = requests.get(status_proxy_url)
        data = resp.json()
        if data["status"] is True:
            print(PROXY)
            print(data)


check_proxy()