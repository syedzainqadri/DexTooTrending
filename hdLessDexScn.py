# from seleniumwire import webdriver
from seleniumwire import webdriver
##
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
##
from time import sleep
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
import random
from selenium.webdriver.firefox.options import Options
from multiprocessing import Process

# import logging
import json
from datetime import datetime

# # Configure logging
# logging.basicConfig(level=logging.INFO, filename='automation_logs.json', filemode='a',
#                     format='%(asctime)s - %(levelname)s - %(message)s')

def log_to_json(message, level='info'):
    log_entry = {
        'message': message,
        'level': level.upper(),
        'timestamp': datetime.now().isoformat()
    }
    with open('automation_logs.json', 'a') as f:
        f.write(json.dumps(log_entry) + '\n')



def check_ip(driver, url="https://api.ipify.org"):
 driver.get(url)
 ip = driver.find_element(By.TAG_NAME,"body").text
 log_to_json("Current IP:", ip)


def restart(driver):
 try:
    driver.delete_all_cookies()
 except:
    log_to_json('no cookies')
 driver.quit()


def check_captcha(driver):
 try: 
  WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, 'challenge-running')))
  clng = driver.find_element(By.ID,'challenge-running')
  log_to_json(clng.text)
  # driver.switch_to.frame(driver.find_element(By.XPATH,'//iframe[@sandbox="allow-same-origin allow-scripts allow-popups"]'))
#   element = WebDriverWait(driver,40).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="challenge-stage"]/div/label')))
  element = driver.find_element(By.ID, "challenge-running")
  
  # log_to_json(element)
  if element!=None:
   sleep(random.randint(3,5))
   driver.switch_to.frame(driver.find_element(By.XPATH,'//iframe[@sandbox="allow-same-origin allow-scripts allow-popups"]'))
   log_to_json('capcha iframe found')
   WebDriverWait(driver,30).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="challenge-stage"]/div/label')))
   driver.find_element(By.XPATH,'//*[@id="challenge-stage"]/div/label').click()
   log_to_json('--captch resolved--')
  sleep(random.randint(3,5))
     
 except:
  log_to_json('------No captcha ------')

def actions(driver,url):
 try:
    search_click = WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'.custom-1qxok6w')))
    search_click.click()
    log_to_json('search button clicked selector')
 except:
    search_click = driver.find_element(By.XPATH,'/html/body/div[1]/div/nav/div[2]/div/button')
    search_click.click()
    log_to_json('search button clicked by xpath')
 sleep(2)
 try:
    srch_input = WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.CLASS_NAME,'chakra-input')))
    srch_input.click()
    srch_input.send_keys(url)
    log_to_json('token url searched')
 except:
    try:
        search_click = driver.find_element(By.XPATH,'/html/body/div[1]/div/nav/div[2]/div/button')
        search_click.click()
        log_to_json('search button clicked by xpath')
        srch_input = WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.CLASS_NAME,'chakra-input')))
        srch_input.click()
        srch_input.send_keys(url)
        log_to_json('token url searched')
    except:
        search_click = WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'.custom-1qxok6w')))
        search_click.click()
        log_to_json('search button clicked selector')
        srch_input = WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.CLASS_NAME,'chakra-input')))
        srch_input.click()
        srch_input.send_keys(url)
        log_to_json('token url searched')
 token = WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'div[class="chakra-stack custom-ktfa8s"]')))
 token.click()
 log_to_json('clicked on the token')
 sleep(3)
 fav_btn = WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.CLASS_NAME,'custom-1rr4qq7')))
 fav_btn.click()
 log_to_json('add to wishlist')
 sleep(1)
 wish_btn = WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'div[class="chakra-menu__group"]')))
 wish_btn.click()
 log_to_json('added to wishlist')
 sleep(3)
 trade_btn = driver.find_element(By.CSS_SELECTOR,'div[class="chakra-stack custom-1ievikz"]')      
 trade_btn.click()
 log_to_json('trade btn clicked')
 sleep(8)
 try:
   WebDriverWait(driver,30).until(EC.visibility_of_element_located((By.CSS_SELECTOR,'div[class="h-full flex flex-col items-center justify-center pb-4"]')))
   log_to_json('trade pop up loaded')
 except:
    log_to_json('no trade loaded')
    pass
 sleep(2)
 driver.find_element(By.CSS_SELECTOR,'button[class="chakra-button cancel custom-113js0t"][title="Close"]').click()
 log_to_json('pop up closed')
 main_window = driver.current_window_handle
 log_to_json('get the main window',main_window)
 # driver.execute_script("window.scrollTo(0, window.screen.height)")
 try:
    element = driver.find_element(By.CSS_SELECTOR,'button.custom-pr2mrc:nth-child(1)')
    sleep(3)
    try:
       try:
         log_to_json(f'likes:{str(element.text)}')
       except:
         likes = element.find_element(By.TAG_NAME,'span')
         log_to_json(f'likes:{str(element.text)}')

    except:
       log_to_json('noting found')
       pass
    try:
        element.click()
        log_to_json('rocket clicked')
        sleep(3)
    except:
        log_to_json('clicked already or some error')  
 except:
    log_to_json('not found rockect')
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
   log_to_json('move to new tab')
   sleep(5)  
#    driver.close()  # Close the current tab
   log_to_json('new tab closes')
   # Switch back to the remaining tab
   driver.switch_to.window(handles[0])
   log_to_json('move to main tab')
   sleep(3)
  except Exception as e:
   log_to_json(f'url error:{(e)}',level='error')  



def main():
    iteration = 0
    while True:
        try:
            if iteration>=20:
                log_to_json('-----limit completed----')
                break
            
            
            log_to_json("[+] Dextools Bot Starting")
            
            
            options = Options()
            options.add_argument("--headless")  # This line sets the headless mode
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-gpu")
            options.add_argument("--disable-dev-shm-usage")
            
            proxy_options = {
             'proxy':{
              'http':'http://shnuqnvu-rotate:mg5i9hbxda5c@p.webshare.io:80'
             }
            }

            driver = webdriver.Firefox(options=options, seleniumwire_options=proxy_options)  

            check_ip(driver)
            driver.get('https://dexscreener.com/')
            url = 'C4ZHt1fPtb6CLcUkivhnnNtxBfxYoJq6x8HEZpUexQvR'
            log_to_json("[+] Go to Dextools")
            sleep(10)
            check_captcha(driver)
            driver.implicitly_wait(10)
            sleep(5)
             
            actions(driver,url)
            log_to_json('------DONE-------')
            restart(driver)
            # driver.delete_all_cookies()
            log_to_json('-----completed-----')
            
            
        except Exception as e:
            log_to_json(f"Error so we move to next iteration:{str(e)} ",level='error')
            restart(driver)
            


thread = 2

if __name__=='__main__':
    main()
   #  for _ in range(thread):
   #      process_obj = Process(target=main)
   #      process_obj.start()

   #  for __ in range(thread):
   #      process_obj.join()

