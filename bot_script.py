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
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db= firestore.client()

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename='bot.log',  # You can also direct this to 'app.log' if you want a single log file
                    filemode='a')  

def log_to_json(message, orderId, pairAddress):

    log_entry = {
        'message': message,
        'level': 'Info',
        'timestamp': datetime.now().isoformat()
    }
    db.collection('orderIDs').document(orderId).collection(pairAddress).add(log_entry)


def setup_driver(proxy_address):
    options = Options()
    # options.add_argument("--headless")    # Run in headless mode.
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

def check_ip(driver, orderId, pairAddress,url="https://api.ipify.org"):
 driver.get(url)
 ip = driver.find_element(By.TAG_NAME,"body").text
 log_to_json(f"Current IP:{ip}", orderId, pairAddress)

def restart(driver,orderId, pairAddress):
 try:
    driver.delete_all_cookies()
 except:
    log_to_json('no cookies',orderId, pairAddress)
 driver.quit()

def check_captcha(driver,orderId, pairAddress):
 try: 
  WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, 'challenge-running')))
  clng = driver.find_element(By.ID,'challenge-running')
  log_to_json(f"{clng.text}",orderId, pairAddress)

  element = driver.find_element(By.ID, "challenge-running")
  

  if element!=None:
   sleep(random.randint(3,5))
   driver.switch_to.frame(driver.find_element(By.XPATH,'//iframe[@sandbox="allow-same-origin allow-scripts allow-popups"]'))
   log_to_json('capcha iframe found',orderId, pairAddress)
    #    WebDriverWait(driver,30).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="challenge-stage"]/div/label')))
   WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="challenge-stage"]/div/label')))
   driver.find_element(By.XPATH,'//*[@id="challenge-stage"]/div/label').click()
   log_to_json('--captch resolved--',orderId, pairAddress)
  sleep(random.randint(3,5))
     
 except:
  log_to_json('------No captcha ------',orderId, pairAddress)

def dexscreenerActions(driver,pairAddress,target_Rocket, iteration, newlikes, startRocket,orderId):



    log_to_json(f'iteration:{iteration}, newlikes:{newlikes}, targetRocket:{target_Rocket}, ',orderId,pairAddress)
    # search button cliking and searching pairAddress

    try:
        search_click = WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'.custom-1qxok6w')))
        search_click.click()
        log_to_json('search button clicked selector',orderId=orderId,pairAddress=pairAddress)
    except:
        search_click = driver.find_element(By.XPATH,'/html/body/div[1]/div/nav/div[2]/div/button')
        search_click.click()
        log_to_json('search button clicked by xpath',orderId,pairAddress)
    # sleep(2)
    try:
        srch_input = WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.CLASS_NAME,'chakra-input')))
        srch_input.click()
        srch_input.send_keys(pairAddress)
        log_to_json('token url searched',orderId,pairAddress)
    except:
        try:
            search_click = driver.find_element(By.XPATH,'/html/body/div[1]/div/nav/div[2]/div/button')
            search_click.click()
            log_to_json('search button clicked by 2xpath',orderId,pairAddress)
            srch_input = WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.CLASS_NAME,'chakra-input')))
            srch_input.click()
            srch_input.send_keys(pairAddress)
            log_to_json('token url searched',orderId,pairAddress)
        except:
            search_click = WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'.custom-1qxok6w')))
            search_click.click()
            log_to_json('search button clicked selector',orderId,pairAddress)
            srch_input = WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.CLASS_NAME,'chakra-input')))
            srch_input.click()
            srch_input.send_keys(pairAddress)
            log_to_json('token url searched',orderId,pairAddress)

        #  clicking on first pairaddress result

    try:
        token = WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'div[class="chakra-stack custom-ktfa8s"]')))
        token.click()
        log_to_json('clicked on the token',orderId,pairAddress)
        sleep(3)
    except:
        pass 
        #   clicking on the  wishlist button 


    try:
        fav_btn = WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.CLASS_NAME,'custom-1rr4qq7')))
        fav_btn.click()
        log_to_json('add to wishlist',orderId,pairAddress)
        sleep(1)
        wish_btn = WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'div[class="chakra-menu__group"]')))
        wish_btn.click()
        log_to_json('added to wishlist',orderId,pairAddress)
        sleep(3)
    except:
        pass
        #  clicking on the trade button 


    try:
        trade_btn = driver.find_element(By.CSS_SELECTOR,'div[class="chakra-stack custom-1ievikz"]')      
        trade_btn.click()
        log_to_json('trade btn clicked',orderId=orderId,pairAddress=pairAddress)
        sleep(3)
        try:
            WebDriverWait(driver,30).until(EC.visibility_of_element_located((By.CSS_SELECTOR,'div[class="h-full flex flex-col items-center justify-center pb-4"]')))
            log_to_json('trade pop up loaded',orderId=orderId,pairAddress=pairAddress)
        except:
            log_to_json('no trade loaded',orderId=orderId,pairAddress=pairAddress)
            pass
        sleep(2) 
        driver.find_element(By.CSS_SELECTOR,'button[class="chakra-button cancel custom-113js0t"][title="Close"]').click()
        log_to_json('pop up closed',orderId=orderId,pairAddress=pairAddress)
        main_window = driver.current_window_handle
        log_to_json('get the main window {main_window}',orderId=orderId,pairAddress=pairAddress)
    except:
        pass
        
        # ------- clicking on links and get back-------
    try:
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
                log_to_json('move to new tab',orderId=orderId,pairAddress=pairAddress)
                sleep(5)  
                #    driver.close()  # Close the current tab
                log_to_json('new tab closes',orderId=orderId,pairAddress=pairAddress)
                # Switch back to the remaining tab
                driver.switch_to.window(handles[0])
                log_to_json('move to main tab',orderId=orderId,pairAddress=pairAddress)
                sleep(3)
            except Exception as e:
                log_to_json(f'url error:{(e)}',orderId=orderId,pairAddress=pairAddress)  
    except:
        pass
        #  clicking on the rocket button 
    try:
        element = driver.find_element(By.CSS_SELECTOR,'button.custom-pr2mrc:nth-child(1)')
        sleep(3)
        try:
            try:
                likes = int(element.text)
                log_to_json(f'likes:{str(likes)}',orderId=orderId,pairAddress=pairAddress)
            except:
                likes = element.find_element(By.TAG_NAME,'span').text
                log_to_json(f'likes:{str(likes)}',orderId=orderId,pairAddress=pairAddress)
            if iteration == 1:
                startRocket = int(likes)
                log_to_json(f'initial Rockets are: {startRocket}',orderId=orderId,pairAddress=pairAddress)

            try:
                element.click()
                iteration +=1
                newlikes  +=1
                log_to_json(f'rocket clicked:{newlikes}',orderId=orderId,pairAddress=pairAddress)
                sleep(3)
            except:
                log_to_json('clicked already or some error',orderId=orderId,pairAddress=pairAddress)  

            if newlikes >= target_Rocket:
                log_to_json('-----targeted likes completed----',orderId=orderId,pairAddress=pairAddress)
                target = True
            else:
                target = False
        except:
            log_to_json('noting found',orderId=orderId,pairAddress=pairAddress)
        pass
        
    except:
        log_to_json('not found rockect',orderId=orderId,pairAddress=pairAddress)
    return target , iteration , newlikes, startRocket





def dextoolActions(driver, pairAddress, target_Rocket, iteration, newlikes, startRocket,orderId):
    try:
        WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.CLASS_NAME,'card__close')))
        driver.find_element(By.CLASS_NAME,'card__close').click()
        log_to_json('1st close button by class',orderId,pairAddress)
        sleep(3)
    except:
        pass
    
    try:
        driver.find_element(By.CLASS_NAME,'card__close').click()
        log_to_json('1st close button by class',orderId,pairAddress)
        sleep(3)
    except:
        pass
        
    

    try:
        driver.execute_script("document.querySelector('.close').click();")
        log_to_json('2nd close button close',orderId,pairAddress)
        sleep(3)
    except:
        
        pass
    try:
        driver.find_element(By.CLASS_NAME,'card__close').click()
        log_to_json('1st close button by class',orderId,pairAddress)
        sleep(3)
    except:
        pass
        
    
    try:
        driver.execute_script("document.querySelector('.close').click();")
        log_to_json('2nd close button close',orderId,pairAddress)
        sleep(3)
    except:
        pass
        

    
    #---------searching the tokkten-------------
    try:
        # WebDriverWait(driver,60).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'input[placeholder="Search pair by symbol, name, contract or token"]')))
        search_input = driver.find_element(By.CSS_SELECTOR,'input[placeholder="Search pair by symbol, name, contract or token"]')
        log_to_json('found by good xpath',orderId,pairAddress)
        # sleep(3)
    except:
        # WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CLASS_NAME,'search-container')))
        search_input = driver.find_element(By.CLASS_NAME,'search-container')
        
    
    search_input.click()
    log_to_json('-----search input clicked-----',orderId,pairAddress)
    sleep(2)
    search_input = driver.switch_to.active_element
    search_input.send_keys(pairAddress)
    sleep(3)
    # link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.results-container li a')))
    driver.execute_script("document.querySelectorAll('.results-container li a')[0].click();")
    log_to_json('cllicked on the 1st searched tokken',orderId,pairAddress)
    sleep(3)
    try:
        driver.find_element(By.CSS_SELECTOR,'button[class="close ng-star-inserted"]').click()
    except:
        pass


    # --------- adding to fav by clicking star
    try:
        # WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'button[data-event-action="click_action_fav"]')))
        driver.find_element(By.CSS_SELECTOR,'button[data-event-action="click_action_fav"]').click()
        log_to_json('fav button clicked by selector',orderId,pairAddress)
        # sleep(3)
    except:
        # WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'button[class="ng-star-inserted"]')))
        driver.find_element(By.CLASS_NAME,'ng-star-inserted').click()
        log_to_json('fav button clicked by class',orderId,pairAddress)
    # sleep(3)
    iteration +=1
    newlikes  +=1
    if newlikes >= target_Rocket:
        log_to_json('-----targeted likes completed----',orderId=orderId,pairAddress=pairAddress)
        target = True
    else:
        target = False

    # -------- clicking on social links-------
    try:    
        main_window = driver.current_window_handle
        log_to_json(f'get the main window {main_window}',orderId,pairAddress)
        
        # WebDriverWait(driver,60).until(EC.element_to_be_clickable((By.CLASS_NAME,'shared-button'))).
        shareBtn = driver.find_element(By.CLASS_NAME,'shared-button')
        shareBtn.click()

        sleep(3)
        try:
            links_monk = driver.find_element(By.CSS_SELECTOR,'div[class="share-btn"][data-desc="Shared from DEXTools.io"]').find_elements(By.TAG_NAME,'a')
            log_to_json('links found',orderId,pairAddress)
            for link in links_monk:
                try:
                    log_to_json('clicking on the link:',orderId,pairAddress)
                    link.click()
                    log_to_json('clicked',orderId,pairAddress)
                    sleep(3)
                    new_window = driver.window_handles[1]
                    log_to_json('get the new window',orderId,pairAddress)
                    driver.switch_to.window(new_window)
                    log_to_json('switched to new window',orderId,pairAddress)
                    sleep(3)
                    driver.close()
                    log_to_json('new window closes',orderId,pairAddress)
                    driver.switch_to.window(main_window)
                    log_to_json('back to new window',orderId,pairAddress)
                    sleep(2)
                except:
                    log_to_json('error in loading the url',orderId,pairAddress)
        except:
            log_to_json('links not found',orderId,pairAddress)
        try:            
            # WebDriverWait(driver,60).until(EC.element_to_be_clickable((By.CSS_SELECTOR ,'.modal-header > button:nth-child(2)')))
            driver.find_element(By.CSS_SELECTOR ,'.modal-header > button:nth-child(2)').click()
            log_to_json('mondel window closed',orderId,pairAddress)
            sleep(3)
        except Exception as e:
            log_to_json('error in closing model window',orderId,pairAddress)
            pass
    except Exception as e:
        log_to_json('error in share links {e}',orderId,pairAddress)

    # ---------clicking on swaping button--------
    try:
        driver.find_element(By.CSS_SELECTOR,'div[class="aggregator-accordion"]').click()
        log_to_json('swap button found',orderId,pairAddress)
        sleep(1)
        driver.find_element(By.CSS_SELECTOR,'button[class="btn btn-primary btn-disclaimer"]').click()
        sleep(3)
    except:
        log_to_json('unable to track swap button ',orderId,pairAddress)
    return target , iteration , newlikes, startRocket
   
    


def run_bot(dexUrl,blockChain,pairAddress,orderId,target_Rocket):
    log_to_json(f"Starting bot for {dexUrl} on Blockchain {blockChain} with pair {pairAddress}",orderId=orderId,pairAddress=pairAddress)
    
    proxy_address = 'shnuqnvu-rotate:mg5i9hbxda5c@p.webshare.io:80'
    # Example target
    iteration = 1
    newlikes = 0
    startRocket = 0
    continue_loop = True

    while continue_loop and iteration <= 2000:  # Example limit for iterations
        try:
            driver = setup_driver(proxy_address=proxy_address)
            driver.implicitly_wait(10)
            # driver.get(dexUrl)
            # check_captcha(driver,orderId,pairAddress)  # Check and resolve captcha if any


            # Perform actions specific to DexScreener
            if dexUrl == 'https://dexscreener.com/':
                driver.get(dexUrl)
                check_captcha(driver,orderId,pairAddress)
                target, iteration, newlikes, startRocket = dexscreenerActions(driver, pairAddress, target_Rocket, iteration, newlikes, startRocket,orderId)
                if target:
                    log_to_json("Target likes reached.",orderId=orderId,pairAddress=pairAddress)
                    continue_loop = False # Stop if target is reached
            else:
                # Other actions for different URLs
                # Navigate to the specific blockchain page
                driver.get(f'https://www.dextools.io/app/en/{blockChain}')
                check_captcha(driver,orderId,pairAddress)
                target, iteration, newlikes, startRocket = dextoolActions(driver, pairAddress, target_Rocket, iteration, newlikes, startRocket,orderId)
                if target:
                    log_to_json("Target likes reached.",orderId=orderId,pairAddress=pairAddress)
                    continue_loop = False # Stop if target is reached


            restart(driver,orderId,pairAddress)  # Clean up and prepare for next iteration
        except Exception as e:
            # log_to_json(f"An error occurred: {e}",orderId=orderId,pairAddress=pairAddress)
            log_to_json('error:{e}',log_to_json,pairAddress)
            restart(driver,orderId,pairAddress)  # Ensure driver is properly restarted after an error



# Corrected global variables initialization

if __name__ == "__main__":
    dexUrl =  sys.argv[1]
    blockChain =  sys.argv[2]
    pairAddress = sys.argv[3]
    orderId = sys.argv[4]
    target_Rocket = 5
    log_to_json('Starting the bot_script----',orderId=orderId,pairAddress=pairAddress)
    log_to_json(f'got the variable {dexUrl}, {blockChain}, {pairAddress}.target{target_Rocket}',orderId=orderId,pairAddress=pairAddress)

    processes = []
    for _ in range(2):
        process_obj = Process(target=run_bot, args=(dexUrl, blockChain, pairAddress,orderId,target_Rocket))
        processes.append(process_obj)
        process_obj.start()

    for process in processes:
        process.join()

