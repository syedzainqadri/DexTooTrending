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


def check_ip(driver, url="https://api.ipify.org"):
 driver.get(url)
 ip = driver.find_element(By.TAG_NAME,"body").text
 print("Current IP:", ip)


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
     
 except:
  print('------No captcha ------')



def actions(driver,url):
 try:
    search_click = WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'.custom-1qxok6w')))
    search_click.click()
    print('search button clicked selector')
 except:
    search_click = driver.find_element(By.XPATH,'/html/body/div[1]/div/nav/div[2]/div/button')
    search_click.click()
    print('search button clicked by xpath')
 sleep(2)
 try:
    srch_input = WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.CLASS_NAME,'chakra-input')))
    srch_input.click()
    srch_input.send_keys(url)
    print('token url searched')
 except:
    try:
        search_click = driver.find_element(By.XPATH,'/html/body/div[1]/div/nav/div[2]/div/button')
        search_click.click()
        print('search button clicked by xpath')
        srch_input = WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.CLASS_NAME,'chakra-input')))
        srch_input.click()
        srch_input.send_keys(url)
        print('token url searched')
    except:
        search_click = WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'.custom-1qxok6w')))
        search_click.click()
        print('search button clicked selector')
        srch_input = WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.CLASS_NAME,'chakra-input')))
        srch_input.click()
        srch_input.send_keys(url)
        print('token url searched')
 token = WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'div[class="chakra-stack custom-ktfa8s"]')))
 token.click()
 print('clicked on the token')
 sleep(3)
 fav_btn = WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.CLASS_NAME,'custom-1rr4qq7')))
 fav_btn.click()
 print('add to wishlist')
 sleep(1)
 wish_btn = WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'div[class="chakra-menu__group"]')))
 wish_btn.click()
 print('added to wishlist')
 sleep(1)
 trade_btn = driver.find_element(By.CSS_SELECTOR,'div[class="chakra-stack custom-1ievikz"]')      
 trade_btn.click()
 print('trade btn clicked')
 sleep(5)
 WebDriverWait(driver,30).until(EC.visibility_of_element_located((By.CSS_SELECTOR,'div[class="h-full flex flex-col items-center justify-center pb-4"]')))
 print('trade pop up loaded')
 sleep(2)
 driver.find_element(By.CSS_SELECTOR,'button[class="chakra-button cancel custom-113js0t"][title="Close"]').click()
 print('pop up closed')
 main_window = driver.current_window_handle
 print('get the main window',main_window)
 # driver.execute_script("window.scrollTo(0, window.screen.height)")
 try:
    element = driver.find_element(By.CSS_SELECTOR,'button.custom-pr2mrc:nth-child(1)')
    sleep(3)
    try:
        element.click()
        print('rocket clicked')
        sleep(3)
    except:
        print('clicked already or some error')  
 except:
    print('not found rockect')
 # ------- clicking on links and get back-------
 
 links = driver.find_element(By.CSS_SELECTOR,'div[class="chakra-wrap custom-1art13b"]').find_elements(By.TAG_NAME,'a')
 for link in links:
  try:
   link.click()
   sleep(2)
   handles = driver.window_handles
   driver.switch_to.window(handles[1])  # Switch to the tab you want to close
   print('move to new tab')
   sleep(5)  
   driver.close()  # Close the current tab
   print('new tab closes')
   # Switch back to the remaining tab
   driver.switch_to.window(handles[0])
   print('move to main tab')
   sleep(3)
  except Exception as e:
   print('url error',e)  

 


 


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
            driver.get('https://dexscreener.com/')
            url = 'a6k5yjk3alusmrzjldsz41hrhzmk4v7w8trcx6lxikcz'
            print("[+] Go to Dextools")
            sleep(10)
            check_captcha(driver)
            driver.implicitly_wait(10)
            sleep(5)
             
            actions(driver,url)
            print('------DONE-------')
            # restart(driver)
            driver.delete_all_cookies()
            
        except Exception as e:
            print("Error so we move to next iteration",e)
            restart(driver)
            


thread = 2

if __name__=='__main__':
    main()
    # for _ in range(thread):
    #     process_obj = Process(target=main)
    #     process_obj.start()

    # for __ in range(thread):
    #     process_obj.join()
