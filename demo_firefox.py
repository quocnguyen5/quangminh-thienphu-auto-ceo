from selenium import webdriver
import time
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import random
import requests
options = FirefoxOptions()
from selenium.webdriver.common.proxy import Proxy, ProxyType

with open(f"userAgentIOS.txt") as f:
    USER_AGENT_LIST = f.read().splitlines()

"Define Both ProxyHost and ProxyPort as String"
ProxyHost = "100009773418904.ldproxy.com" 
ProxyPort = "14106"
url = "https://google.com"
PROXY = f"{ProxyHost}:{ProxyPort}"
reset_proxy_url = f"http://100009773418904.ldproxy.com:11222/reset?proxy={PROXY}"
status_proxy_url = f"http://100009773418904.ldproxy.com:11222/status?proxy={PROXY}"

key ="what is my ip"
# key ="what is my user agent"
# key ="Rút Tiền Thẻ Tín Dụng Đà Nẵng Quang Vinh"

firefox_capabilities = webdriver.DesiredCapabilities.IPHONE
# firefox_capabilities = webdriver.DesiredCapabilities.IPHONE.copy()
firefox_capabilities['marionette'] = True
options.headless = True

firefox_capabilities['proxy'] = {
    "proxyType": "MANUAL",
    "httpProxy": PROXY,
    "sslProxy": PROXY
}
proxy = Proxy({
    'proxyType': ProxyType.MANUAL,
    'httpProxy': PROXY,
    'sslProxy': PROXY,
    'noProxy': '' # set this value as desired
    })
resp = requests.get(status_proxy_url)
print(resp.status_code)

for i in range(1000):
    fp = webdriver.FirefoxProfile()
    user_agent = random.choice(USER_AGENT_LIST)
    fp.set_preference('general.useragent.override', user_agent)  # Change user-agent
    options.set_preference('intl.accept_language', 'es')  # Setting accept language to Spanish
    # options.set_preference("network.proxy.type", 1)
    # fp.set_preference('network.proxy.http', ProxyHost)
    # fp.set_preference('network.proxy.http_port', int(ProxyPort))
    fp.update_preferences()
    options.profile = fp
    # firefox_capabilities['general.useragent.override'] = user_agent
    print(firefox_capabilities)
    driver = webdriver.Firefox(options=options, capabilities=firefox_capabilities,)
    # driver = webdriver.Firefox(fp)
    driver.set_window_size(390, 844)
    driver.get(url)
    time.sleep(random.randint(3, 7))
    search_box =  driver.find_element("name", "q")
    search_box.send_keys(key)
    time.sleep(random.randint(3, 7))
    search_box.submit()
    time.sleep(random.randint(5, 9))
    time.sleep(10000)
    driver.quit()
    requests.get(reset_proxy_url)
    time.sleep(5)
    active = False
    data = {}
    while active is False:
        resp = requests.get(status_proxy_url)
        data = resp.json()
        active = data["status"]
    
    print("New ip: ", data.get("public_ip", None))