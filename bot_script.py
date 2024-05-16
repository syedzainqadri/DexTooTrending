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

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename='bot.log',  # You can also direct this to 'app.log' if you want a single log file
                    filemode='a')  

def log_to_json(message, level='info'):
    log_entry = {
        'message': message,
        'level': level.upper(),
        'timestamp': datetime.now().isoformat()
    }
    with open('automation_logs.json', 'a') as f:
        f.write(json.dumps(log_entry) + ',\n')


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

def check_ip(driver, url="https://api.ipify.org"):
 driver.get(url)
 ip = driver.find_element(By.TAG_NAME,"body").text
 log_to_json(f"Current IP:{ip}")

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

  element = driver.find_element(By.ID, "challenge-running")
  
  #   print(str(element))
  if element!=None:
   sleep(random.randint(3,5))
   driver.switch_to.frame(driver.find_element(By.XPATH,'//iframe[@sandbox="allow-same-origin allow-scripts allow-popups"]'))
   log_to_json('capcha iframe found')
    #    WebDriverWait(driver,30).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="challenge-stage"]/div/label')))
   WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="challenge-stage"]/div/label')))
   driver.find_element(By.XPATH,'//*[@id="challenge-stage"]/div/label').click()
   log_to_json('--captch resolved--')
  sleep(random.randint(3,5))
     
 except:
  log_to_json('------No captcha ------')

def dexscreenerActions(driver,pairAddress,target_Rocket, iteration, newlikes, startRocket):



    print(f'iteration:{iteration}, newlikes:{newlikes}, targetRocket:{target_Rocket}, ')
    # search button cliking and searching pairAddress

    try:
        search_click = WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'.custom-1qxok6w')))
        search_click.click()
        log_to_json('search button clicked selector')
    except:
        search_click = driver.find_element(By.XPATH,'/html/body/div[1]/div/nav/div[2]/div/button')
        search_click.click()
        log_to_json('search button clicked by xpath')
    # sleep(2)
    try:
        srch_input = WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.CLASS_NAME,'chakra-input')))
        srch_input.click()
        srch_input.send_keys(pairAddress)
        log_to_json('token url searched')
    except:
        try:
            search_click = driver.find_element(By.XPATH,'/html/body/div[1]/div/nav/div[2]/div/button')
            search_click.click()
            log_to_json('search button clicked by 2xpath')
            srch_input = WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.CLASS_NAME,'chakra-input')))
            srch_input.click()
            srch_input.send_keys(pairAddress)
            log_to_json('token url searched')
        except:
            search_click = WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'.custom-1qxok6w')))
            search_click.click()
            log_to_json('search button clicked selector')
            srch_input = WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.CLASS_NAME,'chakra-input')))
            srch_input.click()
            srch_input.send_keys(pairAddress)
            log_to_json('token url searched')

        #  clicking on first pairaddress result

    try:
        token = WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'div[class="chakra-stack custom-ktfa8s"]')))
        token.click()
        log_to_json('clicked on the token')
        sleep(3)
    except:
        pass 
        #   clicking on the  wishlist button 


    try:
        fav_btn = WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.CLASS_NAME,'custom-1rr4qq7')))
        fav_btn.click()
        log_to_json('add to wishlist')
        sleep(1)
        wish_btn = WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'div[class="chakra-menu__group"]')))
        wish_btn.click()
        log_to_json('added to wishlist')
        sleep(3)
    except:
        pass
        #  clicking on the trade button 


    try:
        trade_btn = driver.find_element(By.CSS_SELECTOR,'div[class="chakra-stack custom-1ievikz"]')      
        trade_btn.click()
        log_to_json('trade btn clicked')
        sleep(3)
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
        log_to_json('get the main window {main_window}')
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
                log_to_json('move to new tab')
                sleep(5)  
                #    driver.close()  # Close the current tab
                log_to_json('new tab closes')
                # Switch back to the remaining tab
                driver.switch_to.window(handles[0])
                log_to_json('move to main tab')
                sleep(3)
            except Exception as e:
                log_to_json(f'url error:{(e)}')  
    except:
        pass
        #  clicking on the rocket button 
    try:
        element = driver.find_element(By.CSS_SELECTOR,'button.custom-pr2mrc:nth-child(1)')
        sleep(3)
        try:
            try:
                likes = int(element.text)
                log_to_json(f'likes:{str(likes)}')
            except:
                likes = element.find_element(By.TAG_NAME,'span').text
                log_to_json(f'likes:{str(likes)}')
            if iteration == 1:
                startRocket = int(likes)
                log_to_json(f'initial Rockets are: {startRocket}')

            try:
                element.click()
                iteration +=1
                newlikes  +=1
                log_to_json(f'rocket clicked:{newlikes}')
                sleep(3)
            except:
                log_to_json('clicked already or some error')  

            if newlikes >= target_Rocket:
                log_to_json('-----targeted likes completed----')
                target = True
            else:
                target = False
        except:
            log_to_json('noting found')
        pass
        
    except:
        log_to_json('not found rockect')
    return target , iteration , newlikes, startRocket

def dextoolActions(driver,pairAddress):
    sleep(6)
    try:
        WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.CLASS_NAME,'card__close')))
        driver.find_element(By.CLASS_NAME,'card__close').click()
        log_to_json('1st close button by class')
    except:
       pass
    
    # sleep(random.randint(2,5))
    try:
        driver.find_element(By.CLASS_NAME,'card__close').click()
        log_to_json('1st close button by class')
    except:
        
        log_to_json('no extra close')
    driver.implicitly_wait(5)

    try:
        driver.execute_script("document.querySelector('.close').click();")
        log_to_json('2nd close button close')
    except:
        log_to_json('noting 2nd found')
    try:
        driver.find_element(By.CLASS_NAME,'card__close').click()
        log_to_json('1st close button by class')
    except:
        
        log_to_json('no extra close')
    driver.implicitly_wait(5)

    try:
        driver.execute_script("document.querySelector('.close').click();")
        log_to_json('2nd close button close')
    except:
        log_to_json('noting 2nd found')


    sleep(random.randint(3,5))
    
    #---------searching the tokkten-------------
    try:
     WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CLASS_NAME,'search-container')))
     search_input = driver.find_element(By.CLASS_NAME,'search-container')
    except:
     WebDriverWait(driver,60).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'div[placeholder="Search pair by symbol, name, contract or token"]')))
     search_input = driver.find_element(By.CSS_SELECTOR,'div[placeholder="Search pair by symbol, name, contract or token"]')
     log_to_json('found by good xpath')
    search_input.click()
    log_to_json('-----search input clicked-----')
    sleep(1)
    search_input = driver.switch_to.active_element
    search_input.send_keys(pairAddress)
    sleep(3)
    link = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.results-container li a')))
    driver.execute_script("document.querySelectorAll('.results-container li a')[0].click();")
    log_to_json('cllicked on the 1st searched tokken')
    
    sleep(3)

    # --------- adding to fav by clicking star
    try:
        WebDriverWait(driver,60).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'button[data-event-action="click_action_fav"]')))
        driver.find_element(By.CSS_SELECTOR,'button[data-event-action="click_action_fav"]').click()
        log_to_json('fav button clicked')
        sleep(2)
    except:
       pass

    # -------- clicking on social links-------
    try:    
        main_window = driver.current_window_handle
        log_to_json(f'get the main window:{main_window}')
        
        WebDriverWait(driver,60).until(EC.element_to_be_clickable((By.CLASS_NAME,'shared-button')))
        shareBtn = driver.find_element(By.CLASS_NAME,'shared-button')
        shareBtn.click()

        sleep(3)
        try:
            driver.implicitly_wait(5)
            WebDriverWait(driver,5).until(EC.visibility_of_element_located((By.CSS_SELECTOR,'div[class="share-btn"][data-desc="Shared from DEXTools.io"]')))
            links_monk = driver.find_element(By.CSS_SELECTOR,'div[class="share-btn"][data-desc="Shared from DEXTools.io"]').find_elements(By.TAG_NAME,'a')
            log_to_json('links found')
            for link in links_monk:
                try:
                    log_to_json('clicking on the link:',link)
                    link.click()
                    log_to_json('clicked')
                    sleep(3)
                    new_window = driver.window_handles[1]
                    log_to_json('get the new window')
                    driver.switch_to.window(new_window)
                    log_to_json('switched to new window')
                    sleep(3)
                    driver.close()
                    log_to_json('new window closes')
                    driver.switch_to.window(main_window)
                    log_to_json('back to new window')
                    sleep(2)
                except:
                    log_to_json('error in loading the url')
        except:
            log_to_json('links not found')


        try:
            
            WebDriverWait(driver,60).until(EC.element_to_be_clickable((By.CSS_SELECTOR ,'.modal-header > button:nth-child(2)')))
            driver.find_element(By.CSS_SELECTOR ,'.modal-header > button:nth-child(2)').click()
            log_to_json('mondel window closed')
            sleep(3)
        except Exception as e:
            log_to_json('error in closing model window')
            pass
    except Exception as e:
        log_to_json('error in share links',e)

    # ---------clicking on swaping button--------
    try:
        driver.find_element(By.CSS_SELECTOR,'div[class="aggregator-accordion"]').click()
        log_to_json('swap button found')
        sleep(1)
        driver.find_element(By.CSS_SELECTOR,'button[class="btn btn-primary btn-disclaimer"]').click()
        sleep(3)
    except:
        log_to_json('unable to track swap button ')
    
    # --------scrolling the window---------
    screen_height = driver.execute_script("return window.screen.height;")   # get the screen height of the web
    log_to_json(f'get the screen height:{screen_height}')
    i = 1
        # scroll one screen height each time
    scrol_numb= random.randint(2,3)
    while True:
        driver.implicitly_wait(5)   
        driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))
        log_to_json(f'scrloing {i} time')
        i += 1
        sleep(3)
        # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
        scroll_height = driver.execute_script("return document.body.scrollHeight;") 
        log_to_json(f'setting the now height:{screen_height}') 
        # Break the loop when the height we need to scroll to is larger than the total scroll height
        if i==scrol_numb:
            log_to_json('break the loop bcz the scroll window ended...')
            break


def run_bot(dexUrl,blockChain,pairAddress,target_Rocket):
    log_to_json(f"Starting bot for {dexUrl} on Blockchain {blockChain} with pair {pairAddress}")
    
    proxy_address = 'shnuqnvu-rotate:mg5i9hbxda5c@p.webshare.io:80'
    # Example target
    iteration = 1
    newlikes = 0
    startRocket = 0
    continue_loop = True

    while continue_loop and iteration <= 2000:  # Example limit for iterations
        try:
            driver = setup_driver(proxy_address=proxy_address)
            driver.get(dexUrl)
            check_captcha(driver)  # Check and resolve captcha if any

            # Navigate to the specific blockchain page
            driver.get(f'{dexUrl}{blockChain}')
            check_captcha(driver)

            # Perform actions specific to DexScreener
            if dexUrl == 'https://dexscreener.com/':
                target, iteration, newlikes, startRocket = dexscreenerActions(driver, pairAddress, target_Rocket, iteration, newlikes, startRocket)
                if target:
                    print("Target likes reached.")
                    continue_loop = False # Stop if target is reached
            else:
                # Other actions for different URLs
                pass

            restart(driver)  # Clean up and prepare for next iteration
        except Exception as e:
            print(f"An error occurred: {e}")
            restart(driver)  # Ensure driver is properly restarted after an error

# Corrected global variables initialization

if __name__ == "__main__":
    print('Starting the bot_script----')
    dexUrl =   sys.argv[1]
    blockChain = sys.argv[2]
    pairAddress = sys.argv[3]
    target_Rocket = 100
    print(f'got the variable {dexUrl}, {blockChain}, {pairAddress}.target{target_Rocket}')

    processes = []
    for _ in range(2):
        process_obj = Process(target=run_bot, args=(dexUrl, blockChain, pairAddress,target_Rocket))
        processes.append(process_obj)
        process_obj.start()

    for process in processes:
        process.join()

