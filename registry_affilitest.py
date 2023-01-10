# -*- coding: utf-8 -*-
"""
Created on Sun Aug 16 10:01:10 2020

@author: OHyic
"""

# system libraries
from patch import download_latest_chromedriver, webdriver_folder_name
import logging

# system libraries
import os
import random
import re
import sys
import time
import urllib
from datetime import datetime

import pydub
import requests
import speech_recognition as sr
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
import threading

DEBUG = True

# custom patch libraries
# custom patch libraries
global SOCKS5, USER_AGENT_LIST, a_file

with open(f"socks.txt") as f:
    SOCKS5 = f.read().splitlines()

with open(f"user_agent.txt") as f:
    USER_AGENT_LIST = f.read().splitlines()

number = int(sys.argv[1]) if len(sys.argv) > 1 else 1


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
    driver.find_element_by_id("audio-response").send_keys(key.lower())
    driver.find_element_by_id("audio-response").send_keys(Keys.ENTER)
    time.sleep(1)
    driver.switch_to.default_content()


def get_mail(proxies=None):
    email = None
    session = None
    while not email:
        try:
            if proxies:
                request = requests.get(
                    "https://10minutemail.net/address.api.php?new=1", proxies=proxies
                )
            else:
                request = requests.get("https://10minutemail.net/address.api.php?new=1")

            data = request.json()
            email = data["mail_get_mail"]
            session = data["session_id"]

        except Exception as e:
            DEBUG and logging.exception(e)

    return email, session


def get_mail_inbox(session_id, proxies=None):
    payload = {"sessionid": session_id}
    if proxies:
        request = requests.get(
            f"https://10minutemail.net/address.api.php", params=payload, proxies=proxies
        )
    else:
        request = requests.get(f"https://10minutemail.net/address.api.php", params=payload)
    return request.json()


def get_mail_detail(session_id, mail_id, proxies=None):
    payload = {"mailid": mail_id, "sessionid": session_id}
    if proxies:
        r = requests.get(f"https://10minutemail.net/mail.api.php", params=payload, proxies=proxies)
    else:
        r = requests.get(f"https://10minutemail.net/mail.api.php", params=payload)

    return r.json()


def create_account_affilitest():
    def delay(waiting_time=5):
        driver.implicitly_wait(waiting_time)

    user_agent = random.choice(USER_AGENT_LIST)
    socks5 = random.choice(SOCKS5)
    PROXIES = {
        "http": f"socks5://{socks5}",
        "https": f"socks5://{socks5}",
    }
    email, session_id = get_mail(PROXIES)
    DEBUG and print("[INFO] Email: %s and session_id: %s" % (email, session_id))

    # response = requests.get("http://ip-api.com/json/", proxies=PROXIES)
    # result = json.loads(response.content)
    # print(
    #     "[INFO] IP Address [%s]: %s %s %s"
    #     % (datetime.now().strftime("%d-%m-%Y %H:%M:%S"), result["query"], result["country"], socks5)
    # )
    DEBUG and print("[INFO] User agent %s" % user_agent)

    chrome_options = webdriver.ChromeOptions()

    chrome_options.add_argument(f"user-agent={user_agent}")
    chrome_options.add_argument("headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-setuid-sandbox")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("disable-infobars")
    chrome_options.add_argument(f"--proxy-server=socks5://{socks5}")

    # For linux and mac
    driver = webdriver.Chrome(options=chrome_options)

    # For windown
    # driver = webdriver.Chrome(options=chrome_options, executable_path="chromedriver.exe")

    delay()
    # go to website
    driver.get("https://affilitest.com/")
    wait = WebDriverWait(driver, 40)
    try:
        # main program
        # auto locate recaptcha frames
        try:
            driver.find_element_by_class_name("mfp-close").click()
        except:
            pass

        register = driver.find_element_by_id("registerButton")
        ActionChains(driver).move_to_element(register).pause(1).click(register).perform()

        register_windown = driver.current_window_handle
        wait.until(ec.visibility_of_element_located((By.XPATH, "//*[@id='form']/input[5]")))
        driver.find_element_by_name("email").send_keys(email)
        driver.find_element_by_name("password").send_keys(email)
        driver.find_element_by_name("name").send_keys(email)
        driver.find_element_by_name("surName").send_keys(email)
        driver.find_element_by_name("company").send_keys(email)

        delay()
        frames = driver.find_elements_by_tag_name("iframe")
        delay()
        recaptcha_control_frame = None
        for frame in frames:
            if re.search("reCAPTCHA", frame.get_attribute("title")):
                recaptcha_control_frame = frame

        driver.switch_to.frame(recaptcha_control_frame)
        wait.until(
            ec.visibility_of_element_located((By.CLASS_NAME, "recaptcha-checkbox-border"))
        )
        driver.find_element_by_class_name("recaptcha-checkbox-border").click()

        driver.switch_to.window(register_windown)
        frames = driver.find_elements_by_tag_name("iframe")

        recaptcha_challenge_frame = None
        for frame in frames:
            if re.search("recaptcha challenge", frame.get_attribute("title")):
                recaptcha_challenge_frame = frame

        delay()
        driver.switch_to.frame(recaptcha_challenge_frame)
        try:
            audio_button = driver.find_element_by_id("recaptcha-audio-button")
        except:
            audio_button = None

        if audio_button:
            delay(15)
            audio_button.click()

            # get the mp3 audio file
            delay(15)
            src = driver.find_element_by_id("audio-source").get_attribute("src")

            path_to_mp3 = os.path.normpath(os.path.join(os.getcwd(), "sample.mp3"))
            path_to_wav = os.path.normpath(os.path.join(os.getcwd(), "sample.wav"))

            # download the mp3 audio file from the source
            urllib.request.urlretrieve(src, path_to_mp3)
            speech_recognition(driver, path_to_mp3, path_to_wav)

        driver.switch_to.window(register_windown)
        driver.find_element_by_name("agree").click()
        driver.find_element_by_xpath("//*[@id='form']/input[7]").click()
        mail_id = None
        while not mail_id:
            time.sleep(5)
            inbox_mail = get_mail_inbox(session_id, PROXIES)
            for data in inbox_mail["mail_list"]:
                if "AffiliTest" in data["from"]:
                    mail_id = data["mail_id"]

        data_mail = get_mail_detail(session_id, mail_id, PROXIES)
        if "ct.sendgrid.net" in data_mail["urls"][0]:
            driver.get(data_mail["urls"][0])
            try:
                driver.find_element_by_class_name("mfp-close").click()
            except:
                pass

            with open(f"account/account_{number}.txt", "a") as a_file:
                print(f"Success .... {email}")
                a_file.write(email)
                a_file.write("\n")

    except Exception as e:
        DEBUG and logging.exception(e)
        pass
    finally:
        driver.quit()


if __name__ == "__main__":
    for i in range(1000):
        try:
            DEBUG and print("--------")
            create_account_affilitest()
        except Exception as e:
            DEBUG and logging.exception(e)
            pass
