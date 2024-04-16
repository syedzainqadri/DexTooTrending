from seleniumwire import webdriver

from time import sleep
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
import random
from selenium.webdriver.firefox.options import Options
from multiprocessing import Process
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def check_ip(driver, url="https://api.ipify.org"):
    driver.get(url)
    ip = driver.find_element(By.TAG_NAME,"body").text
    print("Current IP:", ip)


def actions(driver,url):
    sleep(6)
    try:
        driver.find_element(By.CLASS_NAME,'card__close').click()
        print('1st close button by class')
    except:
        print('no close button found')
    sleep(random.randint(2,5))
    try:
        driver.find_element(By.CLASS_NAME,'card__close').click()
        print('1st close button by class')
    except:
        
        print('no extra close')
    driver.implicitly_wait(5)

    try:
        driver.execute_script("document.querySelector('.close').click();")
        print('2nd close button close')
    except:
        print('noting 2nd found')
    try:
        driver.find_element(By.CLASS_NAME,'card__close').click()
        print('1st close button by class')
    except:
        
        print('no extra close')
    driver.implicitly_wait(5)

    try:
        driver.execute_script("document.querySelector('.close').click();")
        print('2nd close button close')
    except:
        print('noting 2nd found')


    sleep(random.randint(3,5))
    
    #---------searching the tokkten-------------

    WebDriverWait(driver,60).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'div[class="search-container ng-tns-c2047943673-5"]')))
    search_input = driver.find_element(By.CSS_SELECTOR,'div[class="search-container ng-tns-c2047943673-5"]')
    search_input.click()
    print('-----search input clicked-----')
    sleep(1)
    search_input = driver.switch_to.active_element
    search_input.send_keys(url)
    sleep(3)
    link = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.results-container li a')))
    driver.execute_script("document.querySelectorAll('.results-container li a')[0].click();")
    print('cllicked on the 1st searched tokken')
    
    sleep(3)

    # --------- adding to fav by clicking star
    
    WebDriverWait(driver,60).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'button[data-event-name="add - Fav: A6k5YJk3ALuSMrZjLdSz41HRhzMk4v7w8TRCX6LXiKcZ"]')))
    driver.find_element(By.CSS_SELECTOR,'button[data-event-name="add - Fav: A6k5YJk3ALuSMrZjLdSz41HRhzMk4v7w8TRCX6LXiKcZ"]').click()
    print('fav button clicked')
    sleep(2)

    # -------- clicking on social links-------
    try:    
        main_window = driver.current_window_handle
        print('get the main window',main_window)
        
        WebDriverWait(driver,60).until(EC.element_to_be_clickable((By.CLASS_NAME,'shared-button')))
        shareBtn = driver.find_element(By.CLASS_NAME,'shared-button')
        shareBtn.click()

        sleep(3)
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
            
            WebDriverWait(driver,60).until(EC.element_to_be_clickable((By.CSS_SELECTOR ,'.modal-header > button:nth-child(2)')))
            driver.find_element(By.CSS_SELECTOR ,'.modal-header > button:nth-child(2)').click()
            print('mondel window closed')
            sleep(3)
        except Exception as e:
            print('error in closing model window')
            pass
    except Exception as e:
        print('error in share links',e)

    # ---------clicking on swaping button--------
    try:
        driver.find_element(By.CSS_SELECTOR,'div[class="aggregator-accordion"]').click()
        print('swap button found')
        sleep(1)
        driver.find_element(By.CSS_SELECTOR,'button[class="btn btn-primary btn-disclaimer"]').click()
        sleep(3)
    except:
        print('unable to track swap button ')
    
    # --------scrolling the window---------
    screen_height = driver.execute_script("return window.screen.height;")   # get the screen height of the web
    print('get the screen height',screen_height)
    i = 1
        # scroll one screen height each time
    scrol_numb= random.randint(2,3)
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



def actionsddd(driver,url):
            print('resolving captcha...')
            sleep(6)
            
           # Assuming the driver is already navigating to the correct page
            try:
                # Wait until the element is clickable
                driver.find_element(By.XPATH,'//*[@id="challenge-stage"]/div/label').click()
                print("Checkbox clicked successfully")
            except Exception as e:
                print("Error clicking the checkbox:", e)
            print('box xpath')
            driver.implicitly_wait(5)
            try:
                driver.find_element(By.CLASS_NAME,'card__close').click()
                print('1st close button by class')
            except:
                print('no close button found')
            sleep(random.randint(2,5))
            try:
                driver.find_element(By.CLASS_NAME,'card__close').click()
                print('1st close button by class')
            except:
                
                print('no extra close')
            driver.implicitly_wait(5)

            try:
                driver.execute_script("document.querySelector('.close').click();")
                print('2nd close button close')
            except:
                print('noting 2nd found')
            try:
                driver.find_element(By.CLASS_NAME,'card__close').click()
                print('1st close button by class')
            except:
                
                print('no extra close')
            driver.implicitly_wait(5)

            try:
                driver.execute_script("document.querySelector('.close').click();")
                print('2nd close button close')
            except:
                print('noting 2nd found')


            sleep(random.randint(3,5))
            try:
                search_input = driver.find_element(By.CSS_SELECTOR,'div[class="search-container ng-tns-c2047943673-5"]')
                search_input.click()
                print('-----search input clicked-----')
                sleep(1)
                search_input = driver.switch_to.active_element
                search_input.send_keys(url)
                sleep(3)
                
                driver.execute_script("document.querySelectorAll('.results-container li a')[0].click();")
                print('old method')
            except Exception as e:
                print('loading token error',e)

            sleep(3)

            try:
                driver.implicitly_wait(5)
                driver.find_element(By.CSS_SELECTOR,'button[data-event-name="add - Fav: A6k5YJk3ALuSMrZjLdSz41HRhzMk4v7w8TRCX6LXiKcZ"]').click()
                print('fav button clicked')
                sleep(2)
            except Exception as e:
                print('no fav button',e)
            
            try:    
                main_window = driver.current_window_handle
                print('get the main window',main_window)
                driver.implicitly_wait(10)
                shareBtn = driver.find_element(By.CLASS_NAME,'shared-button')
                shareBtn.click()

                sleep(3)
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
                    sleep(2)
                    # driver.implicitly_wait(5)
                    driver.find_element(By.CSS_SELECTOR ,'.modal-header > button:nth-child(2)').click()
                    print('mondel window closed')
                    sleep(3)
                except Exception as e:
                    print('error in closing model window')
                    pass
            except Exception as e:
                print('error in share links',e)

            try:
                driver.find_element(By.CSS_SELECTOR,'div[class="aggregator-accordion"]').click()
                print('swap button found')
                sleep(1)
                driver.find_element(By.CSS_SELECTOR,'button[class="btn btn-primary btn-disclaimer"]').click()
                sleep(3)
            except:
                print('unable to track')
            

            screen_height = driver.execute_script("return window.screen.height;")   # get the screen height of the web
            print('get the screen height',screen_height)
            i = 1
                # scroll one screen height each time
            scrol_numb= random.randint(2,3)
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


# Verify you are human by completing the action below.
# id="challenge-running"
            iteration+=1
            time.sleep(2)
            print('-------complete--------')
            # Funtion end

def restart(driver):
            driver.delete_all_cookies()
            driver.quit()
            print('Some error occured so we do next iteration')

def check_captcha(driver):
            try: 
                WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, 'challenge-running')))
                clng = driver.find_element(By.ID,'challenge-running')
                print(clng.text)
                # driver.switch_to.frame(driver.find_element(By.XPATH,'//iframe[@sandbox="allow-same-origin allow-scripts allow-popups"]'))
                element = WebDriverWait(driver,30).until(EC.visibility_of_element_located((By.ID, "challenge-running")))
                # element = driver.find_element(By.ID, "challenge-running")
                print(element)
                if element!=None:
                    print('capcha iframe found by xpath')
                    sleep(random.randint(3,5))
                    driver.switch_to.frame(driver.find_element(By.XPATH,'//iframe[@sandbox="allow-same-origin allow-scripts allow-popups"]'))
                    driver.find_element(By.XPATH,'//*[@id="challenge-stage"]/div/label').click()
                sleep(random.randint(3,5))
                captcha = True
            except:
                print('------No captcha ------')
                captcha = False
            return captcha           


def main():
    iteration = 0
    while True:
        try:
            if iteration>=20:
                print('-----limit completed----')
                break
            
            
            print("[+] Dextools Bot Starting")
            
            options = {
             'proxy':{
              'http':'http://shnuqnvu-rotate:mg5i9hbxda5c@p.webshare.io:80'
             }
            }        
            driver = webdriver.Firefox(seleniumwire_options=options)  

            # check_ip(driver)
            url = "A6k5YJk3ALuSMrZjLdSz41HRhzMk4v7w8TRCX6LXiKcZ"
            driver.get('https://www.dextools.io/app/en/solana')
            print("[+] Go to Dextools")
            sleep(10)
            driver.implicitly_wait(10)
            check_captcha(driver)
            sleep(5)
             
            actions(driver,url)
            # restart(driver)
            
        except Exception as e:
            print(e)
            restart(driver)
            continue


thread = 2

if __name__=='__main__':
    main()
    # for _ in range(thread):
    #     process_obj = Process(target=main)
    #     process_obj.start()

    # for __ in range(thread):
    #     process_obj.join()
