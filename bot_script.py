import sys
from seleniumwire import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
import random
from multiprocessing import Process
from datetime import datetime
import json 
import os
import logging

def setup_logging():
    # Configure logging
    logging.basicConfig(filename='bot.log', level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Example of adding a console handler as well
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.ERROR)  # Only log errors to the console
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    logging.getLogger('').addHandler(console_handler)

    # Example to log to the console all messages
    # logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def log_info(message):
    logging.info(message)

def log_error(message):
    logging.error(message)


def setup_driver(proxy_address):
    options = Options()
    # options.add_argument("--headless")  # Run in headless mode.
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    if os.name == 'nt':
       geckodriver_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'geckodriver'))
       os.environ['PATH'] += ';' + geckodriver_path
       
    else:
       geckodriver_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'geckodriver'))
       os.environ['PATH'] += os.pathsep + geckodriver_path
    # Proxy setup, adjust as necessary
    seleniumwire_options = {
        'proxy': {
            'http': f'http://{proxy_address}',
            'https': f'http://{proxy_address}'
        }
    }

    # Setup WebDriver with options
    driver = webdriver.Firefox(options=options, seleniumwire_options=seleniumwire_options)
    return driver

def log_to_json(message, level='info'):
    log_entry = {
        'message': message,
        'level': level.upper(),
        'timestamp': datetime.now().isoformat()
    }
    with open('automation_logs.json', 'a') as f:
        f.write(json.dumps(log_entry) + ',\n')

def check_ip(driver, url="https://api.ipify.org"):
 driver.get(url)
 ip = driver.find_element(By.TAG_NAME,"body").text
 logging.info("Current IP:", ip)

def restart(driver):
 try:
    driver.delete_all_cookies()
 except:
    logging.info('no cookies')
 driver.quit()

def check_captcha(driver):
 try: 
  WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, 'challenge-running')))
  clng = driver.find_element(By.ID,'challenge-running')
  logging.info(clng.text)
  # driver.switch_to.frame(driver.find_element(By.XPATH,'//iframe[@sandbox="allow-same-origin allow-scripts allow-popups"]'))
#   element = WebDriverWait(driver,40).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="challenge-stage"]/div/label')))
  element = driver.find_element(By.ID, "challenge-running")
  
#   print(str(element))
  if element!=None:
   sleep(random.randint(3,5))
   driver.switch_to.frame(driver.find_element(By.XPATH,'//iframe[@sandbox="allow-same-origin allow-scripts allow-popups"]'))
   logging.info('capcha iframe found')
   WebDriverWait(driver,30).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="challenge-stage"]/div/label')))
   driver.find_element(By.XPATH,'//*[@id="challenge-stage"]/div/label').click()
   logging.info('--captch resolved--')
  sleep(random.randint(3,5))
     
 except:
  logging.info('------No captcha ------')

def dexscreenerActions(driver,pairAddress):
 try:
    search_click = WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'.custom-1qxok6w')))
    search_click.click()
    logging.info('search button clicked selector')
 except:
    search_click = driver.find_element(By.XPATH,'/html/body/div[1]/div/nav/div[2]/div/button')
    search_click.click()
    logging.info('search button clicked by xpath')
 sleep(2)
 try:
    srch_input = WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.CLASS_NAME,'chakra-input')))
    srch_input.click()
    srch_input.send_keys(pairAddress)
    logging.info('token url searched')
 except:
    try:
        search_click = driver.find_element(By.XPATH,'/html/body/div[1]/div/nav/div[2]/div/button')
        search_click.click()
        logging.info('search button clicked by xpath')
        srch_input = WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.CLASS_NAME,'chakra-input')))
        srch_input.click()
        srch_input.send_keys(pairAddress)
        logging.info('token url searched')
    except:
        search_click = WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'.custom-1qxok6w')))
        search_click.click()
        logging.info('search button clicked selector')
        srch_input = WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.CLASS_NAME,'chakra-input')))
        srch_input.click()
        srch_input.send_keys(pairAddress)
        logging.info('token url searched')
 token = WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'div[class="chakra-stack custom-ktfa8s"]')))
 token.click()
 logging.info('clicked on the token')
 sleep(3)
 fav_btn = WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.CLASS_NAME,'custom-1rr4qq7')))
 fav_btn.click()
 logging.info('add to wishlist')
 sleep(1)
 wish_btn = WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'div[class="chakra-menu__group"]')))
 wish_btn.click()
 logging.info('added to wishlist')
 sleep(3)
 trade_btn = driver.find_element(By.CSS_SELECTOR,'div[class="chakra-stack custom-1ievikz"]')      
 trade_btn.click()
 logging.info('trade btn clicked')
 sleep(8)
 try:
   WebDriverWait(driver,30).until(EC.visibility_of_element_located((By.CSS_SELECTOR,'div[class="h-full flex flex-col items-center justify-center pb-4"]')))
   logging.info('trade pop up loaded')
 except:
    logging.error('no trade loaded')
    pass
 sleep(2)
 driver.find_element(By.CSS_SELECTOR,'button[class="chakra-button cancel custom-113js0t"][title="Close"]').click()
 logging.info('pop up closed')
 main_window = driver.current_window_handle
 logging.info('get the main window',main_window)
 
 try:
    element = driver.find_element(By.CSS_SELECTOR,'button.custom-pr2mrc:nth-child(1)')
    sleep(3)
    try:
       try:
         logging.info(f'likes:{str(element.text)}')
       except:
         likes = element.find_element(By.TAG_NAME,'span')
         logging.info(f'likes:{str(element.text)}')

    except:
       logging.error('noting found')
       pass
    try:
        element.click()
        logging.info('rocket clicked')
        sleep(3)
    except:
        logging.error('clicked already or some error')  
 except:
    logging.error('not found rockect')
 # ------- clicking on links and get back-------
 
 links = driver.find_element(By.CSS_SELECTOR,'div[class="chakra-wrap custom-1art13b"]').find_elements(By.TAG_NAME,'a')
 for link in links:
  try:
   link.click()
   sleep(2)
   handles = driver.window_handles
   driver.switch_to.window(handles[1])  # Switch to the tab you want to close
   try:
    WebDriverWait(driver,20).until(EC.visibility_of_element_located((By.TAG_NAME,'body')))
   except:
      pass
   logging.info('move to new tab')
   sleep(5)  
#    driver.close()  # Close the current tab
   logging.info('new tab closes')
   # Switch back to the remaining tab
   driver.switch_to.window(handles[0])
   logging.info('move to main tab')
   sleep(3)
  except Exception as e:
   logging.error(f'url error:{(e)}')  

def dextoolActions(driver,pairAddress):
    sleep(6)
    try:
        driver.find_element(By.CLASS_NAME,'card__close').click()
        logging.info('1st close button by class')
    except:
        logging.error('no close button found')
    sleep(random.randint(2,5))
    try:
        driver.find_element(By.CLASS_NAME,'card__close').click()
        logging.info('1st close button by class')
    except:
        
        logging.error('no extra close')
    driver.implicitly_wait(5)

    try:
        driver.execute_script("document.querySelector('.close').click();")
        logging.info('2nd close button close')
    except:
        logging.error('noting 2nd found')
    try:
        driver.find_element(By.CLASS_NAME,'card__close').click()
        logging.info('1st close button by class')
    except:
        
        logging.error('no extra close')
    driver.implicitly_wait(5)

    try:
        driver.execute_script("document.querySelector('.close').click();")
        logging.info('2nd close button close')
    except:
        logging.error('noting 2nd found')


    sleep(random.randint(3,5))
    
    #---------searching the tokkten-------------

    WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'div[class="search-container ng-tns-c2047943673-5"]')))
    search_input = driver.find_element(By.CSS_SELECTOR,'div[class="search-container ng-tns-c2047943673-5"]')
    search_input.click()
    logging.info('-----search input clicked-----')
    sleep(1)
    search_input = driver.switch_to.active_element
    logging.info(f"pairAddress:{pairAddress}")
    search_input.send_keys(pairAddress)
    sleep(3)
    link = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.results-container li a')))
    driver.execute_script("document.querySelectorAll('.results-container li a')[0].click();")
    logging.info('old method')
    
    sleep(3)

    # --------- adding to fav by clicking star
    
    WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'button[data-event-name="add - Fav: A6k5YJk3ALuSMrZjLdSz41HRhzMk4v7w8TRCX6LXiKcZ"]')))
    driver.find_element(By.CSS_SELECTOR,'button[data-event-name="add - Fav: A6k5YJk3ALuSMrZjLdSz41HRhzMk4v7w8TRCX6LXiKcZ"]').click()
    logging.info('fav button clicked')
    sleep(2)

    # -------- clicking on social links-------
    try:    
        main_window = driver.current_window_handle
        logging.info('get the main window',main_window)
        
        WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.CLASS_NAME,'shared-button')))
        shareBtn = driver.find_element(By.CLASS_NAME,'shared-button')
        shareBtn.click()

        sleep(3)
        try:
            driver.implicitly_wait(5)
            links_monk = driver.find_element(By.CSS_SELECTOR,'div[class="share-btn"][data-desc="Shared from DEXTools.io"]').find_elements(By.TAG_NAME,'a')
            logging.info('links found')
            for link in links_monk:
                try:
                    logging.info('clicking on the link:',link)
                    link.click()
                    logging.info('clicked')
                    sleep(3)
                    new_window = driver.window_handles[1]
                    logging.info('get the new window')
                    driver.switch_to.window(new_window)
                    logging.info('switched to new window')
                    sleep(3)
                    driver.close()
                    logging.info('new window closes')
                    driver.switch_to.window(main_window)
                    logging.info('back to new window')
                    sleep(2)
                except:
                    logging.error('error in loading the url')
        except:
            logging.error('links not found')


        try:
            
            WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.CSS_SELECTOR ,'.modal-header > button:nth-child(2)')))
            driver.find_element(By.CSS_SELECTOR ,'.modal-header > button:nth-child(2)').click()
            logging.info('mondel window closed')
            sleep(3)
        except Exception as e:
            logging.error('error in closing model window')
            pass
    except Exception as e:
        logging.error('error in share links',e)

    # ---------clicking on swaping button--------
    try:
        driver.find_element(By.CSS_SELECTOR,'div[class="aggregator-accordion"]').click()
        logging.info('swap button found')
        sleep(1)
        driver.find_element(By.CSS_SELECTOR,'button[class="btn btn-primary btn-disclaimer"]').click()
        sleep(3)
    except:
        logging.error('unable to track swap button ')
    
    # --------scrolling the window---------
    screen_height = driver.execute_script("return window.screen.height;")   # get the screen height of the web
    logging.info('get the screen height',screen_height)
    i = 1
        # scroll one screen height each time
    scrol_numb= random.randint(2,3)
    while True:
        driver.implicitly_wait(5)   
        driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))
        logging.info(f'scrloing {i} time')
        i += 1
        sleep(3)
        # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
        scroll_height = driver.execute_script("return document.body.scrollHeight;") 
        logging.info(f'setting the now height:',screen_height) 
        # Break the loop when the height we need to scroll to is larger than the total scroll height
        if i==scrol_numb:
            logging.info('break the loop bcz the scroll window ended...')
            break



    iteration+=1
    sleep(2)
    logging.info('-------complete--------')


def run_bot(dexUrl,pairAddress):
    logging.info(f"Starting bot for {dexUrl} with pair {pairAddress}")
    iteration = 1
    proxy_address = 'shnuqnvu-rotate:mg5i9hbxda5c@p.webshare.io:80'
    while True:
        try:
            if iteration>=2000:
                logging.info('-----limit completed----')
                break
            
            

            driver = setup_driver(proxy_address=proxy_address)  

            check_ip(driver)
            driver.get(dexUrl)
            logging.info("[+] Go to Dextools")
            sleep(10)
            check_captcha(driver)
            driver.implicitly_wait(10)
            sleep(5)
            #  check which dex and then use the function acccordingly
            if dexUrl == 'https://dexscreener.com/':
               dexscreenerActions(driver,pairAddress)
            else:
               dextoolActions(driver,pairAddress) 
            # actions(driver,token_pair)
            logging.info('------DONE-------')
            restart(driver)
            
            logging.info('-----completed-----')
            iteration+=1
            
            
        except Exception as e:
            logging.error(f"Error so we move to next iteration:{str(e)} ")
            restart(driver)


if __name__ == "__main__":
    dexUrl = sys.argv[1]
    pairAddress = sys.argv[2]
    processes = []
    for _ in range(1):
        process_obj = Process(target=run_bot, args=(dexUrl, pairAddress))
        processes.append(process_obj)
        process_obj.start()

    for process in processes:
        process.join()
