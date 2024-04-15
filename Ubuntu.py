
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
import random
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
# from webdriver_manager.firefox import GeckoDriverManager
from multiprocessing import Process
import time
import requests

def load_proxies(file_path):
    """ Load the list of proxies from a given file. """
    with open(file_path, 'r') as file:
        proxies = [line.strip() for line in file if line.strip()]
    random.shuffle(proxies)  # Shuffle to randomize the order initially
    return proxies


def check_ip(driver):
    """Function to fetch and print the current IP using the driver instance."""
    driver.get("https://api.ipify.org")
    ip = driver.find_element(By.TAG_NAME, "body").text
    print("Current IP:", ip)


def setup_driver(proxy_url):
    """Setup Firefox WebDriver with the specified proxy settings."""
    firefox_options = Options()
    firefox_options.add_argument('--headless')  # Enable headless mode for automation
    firefox_options.add_argument(f'--proxy-server=http://{proxy_url}')
    # service = FirefoxService(executable_path=GeckoDriverManager().install())
    driver = webdriver.Firefox(options=firefox_options)
    return driver

def main():
    iteration = 0
    while True:
        try:
            if iteration>=100:
                print('-----limit completed----')
                break
            print("[+] Dextools Bot Starting")
            # proxy_url = "shnuqnvu-rotate:mg5i9hbxda5c@p.webshare.io:80"  # Replace with your details
            # proxy_url = proxies.pop()
            proxy_url=requests.get(
                 "https://ipv4.webshare.io/",
                    proxies={
                     "http": "http://shnuqnvu-rotate:mg5i9hbxda5c@p.webshare.io:80/",
                     "https": "http://shnuqnvu-rotate:mg5i9hbxda5c@p.webshare.io:80/"
                            }
                    ).text
            print("proxy is:",proxy_url)
            driver = setup_driver(proxy_url)
            
            
            url = "https://www.dextools.io/app/en/solana/pair-explorer/A6k5YJk3ALuSMrZjLdSz41HRhzMk4v7w8TRCX6LXiKcZ"
            driver.get(url)
            driver.implicitly_wait(30)
            print("[+] Go to Dextools")
            check_ip(driver)            
            driver.implicitly_wait(5)
            sleep(random.randint(3,5))
            try:
                driver.find_element(By.CLASS_NAME,'card__close').click()
                print('1st close button by class')
            except:
                # driver.find_element(By.CSS_SELECTOR,'svg[data-icon="xmark"]').click()
                print('by selector')
            sleep(random.randint(2,5))
            driver.implicitly_wait(5)
            try:
                driver.execute_script("document.querySelector('.close').click();")
                print('2nd close button close')
            except:
                print('noting 2nd found')


            try:
                driver.implicitly_wait(5)
                driver.find_element(By.CSS_SELECTOR,'button[data-event-name="add - Fav: A6k5YJk3ALuSMrZjLdSz41HRhzMk4v7w8TRCX6LXiKcZ"]').click()
                print('fav button clicked')
                sleep(2)
            except Exception as e:
                print('no fav button',e)
                
            main_window = driver.current_window_handle
            print('get the main window',main_window)
            sleep(3)
            driver.implicitly_wait(5)
            shareBtn = driver.find_element(By.CSS_SELECTOR,'a[class="shared-button ng-tns-c567420296-2 ng-star-inserted"]')

            shareBtn.click()

            try:
                driver.implicitly_wait(5)
                links_monk = driver.find_element(By.CSS_SELECTOR,'div[class="share-btn"][data-desc="Shared from DEXTools.io"]').find_elements(By.TAG_NAME,'a')
                print('links found')
                for link in links_monk:
                    try:
                        print('clicking on the link:',link)
                        link.click()
                        print('clicked')
                        sleep(3)
                        new_window = driver.window_handles[1]
                        print('get the new window')
                        driver.switch_to.window(new_window)
                        print('switched to new window')
                        sleep(3)
                        driver.close()
                        print('new window closes')
                        driver.switch_to.window(main_window)
                        print('back to new window')
                        sleep(2)
                    except:
                        print('error in loading the url')
            except:
                print('links not found')


            try:
                driver.implicitly_wait(5)
                driver.find_element(By.CSS_SELECTOR,'button[class="close"]').click()
                print('mondel window closed')
                sleep(3)
            except Exception as e:
                print('error in closing model window')
                pass

            screen_height = driver.execute_script("return window.screen.height;")   # get the screen height of the web
            print('get the screen height',screen_height)
            i = 1
                # scroll one screen height each time
            scrol_numb= 3
            while True:
                driver.implicitly_wait(5)
                driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))
                print(f'scrloing {i} time')
                i += 1
                sleep(3)
                # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
                scroll_height = driver.execute_script("return document.body.scrollHeight;") 
                print(f'setting the now height:',screen_height) 
                # Break the loop when the height we need to scroll to is larger than the total scroll height
                if i==scrol_numb:
                    print('break the loop bcz the scroll window ended...')
                    break



            iteration+=1
            time.sleep(2)
            print('-------complete--------')
            driver.delete_all_cookies()
            driver.quit()
        
        except:
            driver.quit()
            print('Some error occured so we do next iteration')
            continue


thread = 1

if __name__=='__main__':
    # proxy_list = load_proxies("proxies.txt")  # Path to your proxy file
    processes = []
    # main()
    for _ in range(thread):  # Adjust number of processes as needed
        process = Process(target=main)
        processes.append(process)
        process.start()

    for process in processes:
        process.join()
