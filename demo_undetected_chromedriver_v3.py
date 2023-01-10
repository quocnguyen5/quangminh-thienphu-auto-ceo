import argparse
import logging
import os
import random
import re
import time
import urllib

import pydub
import requests
import schedule
import speech_recognition as sr
import undetected_chromedriver.v2 as uc
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

# Initialize parser


parser = argparse.ArgumentParser()
parser.add_argument("-p", "--proxy", help="Proxy", default="1")
parser.add_argument("--headless", help="Headless", type=bool, default=False)
parser.add_argument("--reset-proxy", help="Reset proxy", type=int, default=0)
parser.add_argument("--key", help="Key", type=int, default=1)
parser.add_argument("-t", "--type", help="Tilte", default='4g')
args = parser.parse_args()

DEBUG = True
ENABLE_PROXY = True
RESET_PROXY = bool(args.reset_proxy)
CLICK_WEBSITE = True
CLICK_MAPS = True
CLICK_CALL = True
HEADLESS = args.headless

# with open(f"ua_test.txt") as f:
with open(f"userAgentIOS.txt") as f:
    USER_AGENT_LIST = f.read().splitlines()

with open(f"address.txt") as f:
    ADDRESS_LIST = f.read().splitlines()

url = "https://google.com"
PROXY_LIST_4G = {
    "1": "100009773418904.ldproxy.com:14102",
    "2": "100009773418904.ldproxy.com:14107",
    "3": "100009773418904.ldproxy.com:14109",
    "4": "100009773418904.ldproxy.com:14108",
    "5": "100009773418904.ldproxy.com:14113",
    "6": "100009773418904.ldproxy.com:14115",
    "7": "100009773418904.ldproxy.com:14117",
}
PROXY_LIST_WAN = {
    "1": "wan.100009773418904.ldproxy.com:4307",
    "2": "wan.100009773418904.ldproxy.com:4407",
    "3": "wan.100009773418904.ldproxy.com:4007",
    "4": "wan.100009773418904.ldproxy.com:4008",
    "5": "wan.100009773418904.ldproxy.com:4009",
    "6": "wan.100009773418904.ldproxy.com:4007",
    "7": "wan.100009773418904.ldproxy.com:4008",
}
PROXY_LIST = PROXY_LIST_4G if args.type == "4g" else PROXY_LIST_WAN
PROXY = PROXY_LIST[args.proxy]

proxy_url_4g = "100009773418904.ldproxy.com:11222"
proxy_url_wan = "wan.100009773418904.ldproxy.com:14222"
PROXY_url = proxy_url_4g if args.type == "4g" else proxy_url_wan

reset_proxy_url = f"http://{PROXY_url}/reset?proxy={PROXY}"
status_proxy_url = f"http://{PROXY_url}/status?proxy={PROXY}"
# reset_proxy_url = f"http://171.236.158.16:14222/reset?proxy={PROXY}"
# status_proxy_url = f"http://171.236.158.16:14222/status?proxy={PROXY}"
reset_proxy_time = 5

search_keys_1 = [
    ("Quang Vinh", f"Đà Nẵng Rút Tiền Thẻ Tín Dụng Quang Vinh"),
    ("Quang Vinh", f"da nang rut tien the tin dung Quang Vinh"),
    ("Quang Vinh", f"Rút Tiền Thẻ Tín Dụng Đà Nẵng Quang Vinh"),
    ("Quang Vinh", f"Đà Nẵng rut tien the tin dung Quang Vinh"),
    ("Quang Vinh", f"rut tien the tin dung da nang Quang Vinh"),
    ("Benny", f"rút tiền thẻ tín dụng đà nẵng Benny"),
    ("Benny", f"rút tiền thẻ tín dụng đà nẵng Benny"),
    ("Benny", f"rút tiền thẻ tín dụng đà nẵng Benny"),
    ("Benny", f"đà nẵng rút tiền thẻ tín dụng Benny"),
    # ("Benny", f"rut tien the tin dung Benny"),
    # ("Benny", f"rut tien the tin dung da nang Benny"),
    # ("Benny", f"Đà Nẵng rut tien the tin dung Benny"),
    ("Quang Vinh", f"đà nẵng Rút tiền thẻ tín dụng quang vinh")
]

search_keys_2 = [
    ("Quang Vinh", f"Đà Nẵng Rút Tiền Thẻ Tín Dụng Quang Vinh"),
    ("Quang Vinh", f"Đà Nẵng rut tien the tin dung Quang Vinh"),
    ("Quang Vinh", f"Rút Tiền Thẻ Tín Dụng Đà Nẵng Quang Vinh"),
    ("Quang Vinh", f"Đà Nẵng rut tien the tin dung Quang Vinh"),
    ("Quang Vinh", f"rut tien the tin dung da nang Quang Vinh"),
    ("Quang Vinh", f"đà nẵng Rút tiền thẻ tín dụng quang vinh")
]

# search_keys = search_keys_1 if args.key == 1 else search_keys_2
search_keys = search_keys_1
# search_keys = [
#     ("Quang Vinh", f"Đáo Hạn Thẻ Tín Dụng Đà Nẵng Quang Vinh"),
# ]

def get_option():
    user_agent = random.choice(USER_AGENT_LIST)
    options = uc.ChromeOptions()
    HEADLESS and options.add_argument("--headless")
    options.add_argument("--incognito")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument('--deny-permission-prompts')
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-notifications")
    # options.add_argument("--start-maximized")
    options.add_argument("--disable-infobars")
    ENABLE_PROXY and options.add_argument(f"--proxy-server=http://{PROXY}")
    options.add_argument("--no-first-run --no-service-autorun --password-store=basic")
    options.add_argument(f"--user-agent={user_agent}")

    return options, user_agent


def check_proxy():
    print("Checking proxy .....")
    active = False
    data = {}
    while active is False:
        resp = requests.get(status_proxy_url)
        data = resp.json()
        active = data["status"]
        if active is False:
            time.sleep(5)

    return data


def reset_proxy():
    print("Reset proxy .....")
    requests.get(reset_proxy_url)
    time.sleep(5)
    data = check_proxy()
    print("Ip: ", data.get("public_ip", None))


RESET_PROXY and schedule.every(15).minutes.do(reset_proxy)


def speech_recognition(driver, path_to_mp3, path_to_wav):
    # load downloaded mp3 audio file as .wav
    sound = pydub.AudioSegment.from_mp3(path_to_mp3)
    sound.export(path_to_wav, format="wav")
    sample_audio = sr.AudioFile(path_to_wav)

    # translate audio to text with google voice recognition
    driver.implicitly_wait(5)
    r = sr.Recognizer()
    with sample_audio as source:
        audio = r.record(source)
    key = r.recognize_google(audio)
    DEBUG and print(f"[INFO] Recaptcha Passcode: {key}")

    # key in results and submit
    driver.implicitly_wait(5)
    driver.find_element("id", "audio-response").send_keys(key.lower())
    driver.find_element("id", "audio-response").send_keys(Keys.ENTER)
    time.sleep(1)
    driver.switch_to.default_content()


def pass_captcha(driver):
    register_window = driver.current_window_handle
    try:
        frames = driver.find_elements("tag name", "iframe")
    except Exception as e:
        logging.exception(e)
        return

    time.sleep(5)
    recaptcha_control_frame = None
    for frame in frames:
        if re.search("reCAPTCHA", frame.get_attribute("title")):
            recaptcha_control_frame = frame
    if recaptcha_control_frame is None:
        return

    print("Pass captcha .....")
    driver.switch_to.frame(recaptcha_control_frame)
    wait.until(ec.visibility_of_element_located(("class name", "recaptcha-checkbox-border")))
    driver.find_element("class name", "recaptcha-checkbox-border").click()

    driver.switch_to.window(register_window)
    frames = driver.find_elements("tag name", "iframe")

    recaptcha_challenge_frame = None
    for frame in frames:
        if re.search("recaptcha challenge", frame.get_attribute("title")):
            recaptcha_challenge_frame = frame

    time.sleep(5)
    driver.switch_to.frame(recaptcha_challenge_frame)
    try:
        audio_button = driver.find_element("id", "recaptcha-audio-button")
    except:
        audio_button = None

    if audio_button:
        time.sleep(10)
        audio_button.click()

        # get the mp3 audio file
        time.sleep(10)
        src = driver.find_element("id", "audio-source").get_attribute("src")

        path_to_mp3 = os.path.normpath(os.path.join(os.getcwd(), "sample.mp3"))
        path_to_wav = os.path.normpath(os.path.join(os.getcwd(), "sample.wav"))

        # download the mp3 audio file from the source
        urllib.request.urlretrieve(src, path_to_mp3)
        speech_recognition(driver, path_to_mp3, path_to_wav)


def click_website(driver, wait):
    print("Click webiste .....")
    wait.until(ec.visibility_of_element_located(("class name", "FFdnyb")))
    elements = driver.find_elements("class name", "FFdnyb")
    for element in elements:
        try:
            website_string = element.find_element("class name", "Dc68Je")
        except:
            continue
        if "Trang web" in website_string.get_attribute("innerHTML"):
            element.click()
            time.sleep(random.randint(3, 10))
            driver.back()


def click_direction(driver, wait):
    print("Click direction .....")
    wait.until(ec.visibility_of_element_located(("class name", "FFdnyb")))
    elements = driver.find_elements("class name", "FFdnyb")
    for element in elements:
        try:
            website_string = element.find_element("class name", "Dc68Je")
        except:
            continue
        if "đường đi" in website_string.get_attribute(
            "innerHTML"
        ).lower() or "chỉ đường" in website_string.get_attribute("innerHTML").lower():
            element.click()
            time.sleep(random.randint(3, 7))
            wait.until(ec.visibility_of_element_located(("id", "ml-waypoint-input-0")))
            input_addr = driver.find_element("id", "ml-waypoint-input-0")
            address = random.choice(ADDRESS_LIST)
            input_addr.send_keys(f"{random.randint(1, 200)} {address}")
            time.sleep(random.randint(2, 5))
            input_addr.send_keys(Keys.RETURN)
            time.sleep(random.randint(7, 15))
            driver.back()


def click_call(driver, wait):
    print("Click call .....")
    wait.until(ec.visibility_of_element_located(("class name", "FFdnyb")))
    elements = driver.find_elements("class name", "FFdnyb")
    for element in elements:
        try:
            website_string = element.find_element("class name", "Dc68Je")
        except:
            continue

        if "Gọi" in website_string.get_attribute("innerHTML"):
            element.click()
            time.sleep(random.randint(1, 3))
            driver.back()


if __name__ == "__main__":
    RESET_PROXY and reset_proxy()
    for i in range(10000):
        # check_proxy()
        options, user_agent = get_option()
        print(f"Start Chrome: {user_agent}")
        driver = uc.Chrome(options=options)

        try:
            wait = WebDriverWait(driver, 20)
            driver.set_window_size(390, 844)
            driver.get(url)
            # time.sleep(10000)
            time.sleep(random.randint(3, 7))
            key, search_key = random.choice(search_keys)
            print(f"Searching with {search_key} .....")
            search_box = driver.find_element("name", "q")
            time.sleep(random.randint(3, 7))
            search_box.send_keys(search_key)
            time.sleep(random.randint(2, 7))
            search_box.submit()
            time.sleep(random.randint(5, 9))
            pass_captcha(driver)

            wait.until(ec.visibility_of_element_located(("class name", "MjjYud")))
            search_results = driver.find_elements("class name", "MjjYud")

            driver.execute_script(
                "arguments[0].scrollIntoView();",
                search_results[random.randint(0, len(search_results) - 1)],
            )
            try:
                maps = driver.find_element("class name", "EyBRub")
            except:
                maps = None
            try:
                maps_list = driver.find_elements("class name", "aJOXUd")
            except:
                maps_list = None

            if maps:
                names = maps.find_elements("tag name", "span")

                for item in names:
                    if key in item.get_attribute("innerHTML"):
                        driver.execute_script("arguments[0].scrollIntoView();", item)
                        if CLICK_WEBSITE is True and random.randint(0, 4) == 1:
                            click_website(driver, wait)
                            time.sleep(random.randint(3, 7))

                        if CLICK_MAPS is True:
                            click_direction(driver, wait)

                        if CLICK_CALL is True and random.randint(0, 10) == 1:
                            click_call(driver, wait)
                        break

            if maps_list:
                done = False
                for maps in maps_list:
                    names = maps.find_elements("tag name", "span")
                    for item in names:
                        if key in item.get_attribute("innerHTML"):
                            driver.execute_script("arguments[0].scrollIntoView();", item)
                            maps.click()
                            time.sleep(random.randint(1, 5))

                            if CLICK_WEBSITE is True and random.randint(0, 4) == 1:
                                click_website(driver, wait)
                                time.sleep(random.randint(3, 7))

                            if CLICK_MAPS is True:
                                click_direction(driver, wait)

                            if CLICK_CALL is True and random.randint(0, 10) == 1:
                                click_call(driver, wait)
                            done = True
                            break

                if done is False:
                    wait.until(ec.visibility_of_element_located(("class name", "U48fD")))
                    other_result_button = driver.find_element("class name", "U48fD")
                    other_result_button.click()
                    wait.until(ec.visibility_of_element_located(("class name", "l6Ea0c")))
                    maps_list = driver.find_elements("class name", "l6Ea0c")
                    for maps in maps_list:
                        names = maps.find_elements("tag name", "span")
                        for item in names:
                            if key in item.get_attribute("innerHTML"):
                                driver.execute_script("arguments[0].scrollIntoView();", item)
                                maps.click()
                                time.sleep(random.randint(5, 10))

                                if CLICK_WEBSITE is True and random.randint(0, 4) == 1:
                                    click_website(driver, wait)
                                    time.sleep(random.randint(3, 7))

                                if CLICK_MAPS is True:
                                    click_direction(driver, wait)

                                if CLICK_CALL is True and random.randint(0, 10) == 1:
                                    click_call(driver, wait)
                                break

            print(f"Done ..... {i}")
            driver.quit()

        except Exception as e:
            logging.exception(e)
            driver.quit()

        finally:
            try:
                RESET_PROXY and schedule.run_pending()
            except:
                pass
