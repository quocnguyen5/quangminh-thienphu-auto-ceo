from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time 

MAX = 15

browser = webdriver.Safari()
for i in range(MAX):
    browser.get('https://google.com')
    time.sleep(2)
    search_box = browser.find_element("name", "q")
    search_box.send_keys('Thúi trăm củ')
    time.sleep(2)
    # search_box.submit()
    search_box.send_keys(Keys.RETURN)

    time.sleep(2)

browser.quit()
    # with open('img.txt', 'w') as f:

#     for i in range(MAX):
#         try:
#             # Works also:
#             # a = browser.find_element_by_id('comic').find_element_by_tag_name('img')
#             time.sleep(1)
#             browser.execute_script('window.scrollTo(0, document.getElementById("comic").scrollHeight);')
#             time.sleep(3)
#             a = browser.find_element_by_xpath('//*[@id="comic"]/img')
#             src = a.get_attribute('src')
#             print("Image Source:", src)
#             f.write(src + '\n')

#             prev = browser.find_element_by_link_text("< Prev")
#             # In other browsers: prev.click()
#             prev.send_keys(Keys.RETURN)
#             print("Navigated to previous entry.")
#         except:
#             print('Unable to find comic image.')