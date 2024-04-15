from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from multiprocessing import Process
from time import sleep
import random
import requests

def setup_driver(proxy_url):
    """Setup Firefox WebDriver with the specified proxy settings."""
    firefox_options = Options()
    # firefox_options.add_argument('--headless')  # Enable headless mode for automation
    
    proxy = Proxy({
    'proxyType': ProxyType.MANUAL,
    'httpProxy': proxy_url,  # Format: username:password@host:port
    'sslProxy': proxy_url    # Format: username:password@host:port
    })
    firefox_options.proxy = proxy

    driver = webdriver.Firefox(options=firefox_options, service=FirefoxService(GeckoDriverManager().install()))
    return driver

def check_ip(driver):
    """Function to fetch and print the current IP using the driver instance."""
    driver.get("https://api.ipify.org")
    ip = driver.find_element(By.TAG_NAME, "body").text
    print("Current IP:", ip)

def fetch_proxy():
    """Fetch a proxy URL from a proxy service."""
    response = requests.get(
    "https://proxy.webshare.io/api/v2/proxy/list/?mode=direct&page=1&page_size=25",
    headers={"Authorization": "Token eij38i9lm23710br1g2sm7naoblvmojp8b1ytwn1"})
 
    print(response)
    if response.status_code == 200:
        proxies = response.json()['results']
        if proxies:
            return random.choice(proxies)['proxy_address']
    return None

def main():
    proxy_url = fetch_proxy()
    if proxy_url is None:
        print("Failed to obtain proxy.")
        return

    print(f"Using proxy: {proxy_url}")
    driver = setup_driver(proxy_url)
    print(driver)
    # check_ip(driver)  # Validate the proxy IP
    iteration = 0
    while True:
        try:
            if iteration>=100:
                print('-----limit completed----')
                break
            print("[+] Dextools Bot Starting")
            
            url = "https://www.dextools.io/app/en/solana/pair-explorer/A6k5YJk3ALuSMrZjLdSz41HRhzMk4v7w8TRCX6LXiKcZ"
            driver.get(url)
            # driver.implicitly_wait(30)
            # print("[+] Go to Dextools")
            # check_ip(driver)            
            # driver.implicitly_wait(5)
            # sleep(random.randint(3,5))
            # try:
            #     driver.find_element(By.CLASS_NAME,'card__close').click()
            #     print('1st close button by class')
            # except:
            #     # driver.find_element(By.CSS_SELECTOR,'svg[data-icon="xmark"]').click()
            #     print('by selector')
            # sleep(random.randint(2,5))
            # driver.implicitly_wait(5)
            # try:
            #     driver.execute_script("document.querySelector('.close').click();")
            #     print('2nd close button close')
            # except:
            #     print('noting 2nd found')


            # try:
            #     driver.implicitly_wait(5)
            #     driver.find_element(By.CSS_SELECTOR,'button[data-event-name="add - Fav: A6k5YJk3ALuSMrZjLdSz41HRhzMk4v7w8TRCX6LXiKcZ"]').click()
            #     print('fav button clicked')
            #     sleep(2)
            # except Exception as e:
            #     print('no fav button',e)
                
            # main_window = driver.current_window_handle
            # print('get the main window',main_window)
            # sleep(3)
            # driver.implicitly_wait(5)
            # shareBtn = driver.find_element(By.CSS_SELECTOR,'a[class="shared-button ng-tns-c567420296-2 ng-star-inserted"]')

            # shareBtn.click()

            # try:
            #     driver.implicitly_wait(5)
            #     links_monk = driver.find_element(By.CSS_SELECTOR,'div[class="share-btn"][data-desc="Shared from DEXTools.io"]').find_elements(By.TAG_NAME,'a')
            #     print('links found')
            #     for link in links_monk:
            #         try:
            #             print('clicking on the link:',link)
            #             link.click()
            #             print('clicked')
            #             sleep(3)
            #             new_window = driver.window_handles[1]
            #             print('get the new window')
            #             driver.switch_to.window(new_window)
            #             print('switched to new window')
            #             sleep(3)
            #             driver.close()
            #             print('new window closes')
            #             driver.switch_to.window(main_window)
            #             print('back to new window')
            #             sleep(2)
            #         except:
            #             print('error in loading the url')
            # except:
            #     print('links not found')


            # try:
            #     driver.implicitly_wait(5)
            #     driver.find_element(By.CSS_SELECTOR,'button[class="close"]').click()
            #     print('mondel window closed')
            #     sleep(3)
            # except Exception as e:
            #     print('error in closing model window')
            #     pass

            # screen_height = driver.execute_script("return window.screen.height;")   # get the screen height of the web
            # print('get the screen height',screen_height)
            # i = 1
            #     # scroll one screen height each time
            # scrol_numb= 3
            # while True:
            #     driver.implicitly_wait(5)
            #     driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))
            #     print(f'scrloing {i} time')
            #     i += 1
            #     sleep(3)
            #     # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
            #     scroll_height = driver.execute_script("return document.body.scrollHeight;") 
            #     print(f'setting the now height:',screen_height) 
            #     # Break the loop when the height we need to scroll to is larger than the total scroll height
            #     if i==scrol_numb:
            #         print('break the loop bcz the scroll window ended...')
            #         break



            iteration+=1
            sleep(2)
            print('-------complete--------')
            driver.delete_all_cookies()
            driver.quit()
        
        except:
            driver.quit()
            print('Some error occured so we do next iteration')
            continue

if __name__ == '__main__':
    thread_count = 1
    processes = []
    for _ in range(thread_count):
        process = Process(target=main)
        processes.append(process)
        process.start()

    for process in processes:
        process.join()
