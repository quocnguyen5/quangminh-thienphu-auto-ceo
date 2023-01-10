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
parser.add_argument("--reset-proxy", help="Test", type=int, default=1)
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
PROXY_LIST = {
    "1": "100009773418904.ldproxy.com:14106",
    "2": "100009773418904.ldproxy.com:14102",
    "3": "100009773418904.ldproxy.com:14117",
    "4": "100009773418904.ldproxy.com:14109",
}
PROXY = PROXY_LIST[args.proxy]

reset_proxy_url = f"http://100009773418904.ldproxy.com:11222/reset?proxy={PROXY}"
status_proxy_url = f"http://100009773418904.ldproxy.com:11222/status?proxy={PROXY}"
reset_proxy_time = 5

search_keys = [
    ("Quang Vinh", f"Đà Nẵng Rút Tiền Thẻ Tín Dụng"),
    # ("Quang Vinh", f"Đà Nẵng Rút Tiền Thẻ Tín Dụng"),
    # ("Quang Vinh", f"Đà Nẵng Rút Tiền Thẻ Tín Dụng Thanh Khê"),
    # ("Quang Vinh", f"Đà Nẵng Rút Tiền Thẻ Tín Dụng Hải Châu"),
    # ("Quang Vinh", f"Đà Nẵng Rút Tiền Thẻ Tín Dụng Sơn Trà"),
    # ("Quang Vinh", f"Đà Nẵng Rút Tiền Thẻ Tín Dụng Liên Chiểu"),
    # ("Quang Vinh", f"Rút Tiền Thẻ Tín Dụng Đà Nẵng Quang Vinh"),
    # ("Quang Vinh", f"Đáo Hạn Thẻ Tín Dụng Đà Nẵng Quang Vinh"),
    # ("Phúc Thịnh", f"Rút Tiền Thẻ Tín Dụng Đà Nẵng Phúc Thịnh"),
    # ("Phúc Thịnh", f"Đáo Hạn Thẻ Tín Dụng Đà Nẵng Phúc Thịnh"),
    # ("Thiên Phú", f"rút tiền thẻ tín dụng đà nẵng thiên phú"),
    # ("Thiên Phú", f"đáo hạn thẻ tín dụng thiên phú"),
]


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
    options.add_argument("--start-maximized")
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

    return data


def reset_proxy():
    print("Reset proxy .....")
    requests.get(reset_proxy_url)
    time.sleep(5)
    data = check_proxy()
    print("Ip: ", data.get("public_ip", None))


RESET_PROXY and schedule.every(5).minutes.do(reset_proxy)


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
    for i in range(100000):
        check_proxy()
        options, user_agent = get_option()
        print(f"Start Chrome: {user_agent}")
        driver = uc.Chrome(options=options)

        try:
            wait = WebDriverWait(driver, 20)
            driver.set_window_size(390, 844)
            driver.get(url)
            time.sleep(random.randint(3, 7))
            key, search_key = random.choice(search_keys)
            print(f"Searching with {search_key} .....")
            search_box = driver.find_element("name", "q")
            time.sleep(random.randint(3, 7))
            search_box.send_keys(search_key)
            time.sleep(random.randint(2, 7))
            # search_box.submit()
            time.sleep(random.randint(5, 9))
            # pass_captcha(driver)

            wait.until(ec.visibility_of_element_located(("class name", "MjjYud")))
            search_results = driver.find_elements("class name", "MjjYud")

            driver.execute_script(
                "arguments[0].scrollIntoView();",
                search_results[random.randint(0, len(search_results) - 1)],
            )
            time.sleep(1000)
            print(f"Done ..... {i}")
            driver.quit()

        except Exception as e:
            logging.exception(e)
            driver.quit()

        finally:
            RESET_PROXY and schedule.run_pending()
