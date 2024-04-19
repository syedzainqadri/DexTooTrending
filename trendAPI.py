from flask import Flask, request, jsonify
import threading
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


import json
from datetime import datetime
from flask import Flask, request, jsonify


# def log_to_json(message, level='info'):
#     log_entry = {
#         'message': message,
#         'level': level.upper(),
#         'timestamp': datetime.now().isoformat()
#     }
#     with open('automation_logs.json', 'a') as f:
#         f.write(json.dumps(log_entry) + ',\n')



def check_ip(driver, url="https://api.ipify.org"):
 driver.get(url)
 ip = driver.find_element(By.TAG_NAME,"body").text
 print("Current IP:", ip)


def restart(driver):
 try:
    driver.delete_all_cookies()
 except:
    print('no cookies')
 driver.quit()


def check_captcha(driver):
 try: 
  WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, 'challenge-running')))
  clng = driver.find_element(By.ID,'challenge-running')
  print(clng.text)
  # driver.switch_to.frame(driver.find_element(By.XPATH,'//iframe[@sandbox="allow-same-origin allow-scripts allow-popups"]'))
#   element = WebDriverWait(driver,40).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="challenge-stage"]/div/label')))
  element = driver.find_element(By.ID, "challenge-running")
  
#   print(str(element))
  if element!=None:
   sleep(random.randint(3,5))
   driver.switch_to.frame(driver.find_element(By.XPATH,'//iframe[@sandbox="allow-same-origin allow-scripts allow-popups"]'))
   print('capcha iframe found')
   WebDriverWait(driver,30).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="challenge-stage"]/div/label')))
   driver.find_element(By.XPATH,'//*[@id="challenge-stage"]/div/label').click()
   print('--captch resolved--')
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
 sleep(3)
 trade_btn = driver.find_element(By.CSS_SELECTOR,'div[class="chakra-stack custom-1ievikz"]')      
 trade_btn.click()
 print('trade btn clicked')
 sleep(8)
 try:
   WebDriverWait(driver,30).until(EC.visibility_of_element_located((By.CSS_SELECTOR,'div[class="h-full flex flex-col items-center justify-center pb-4"]')))
   print('trade pop up loaded')
 except:
    print('no trade loaded')
    pass
 sleep(2)
 driver.find_element(By.CSS_SELECTOR,'button[class="chakra-button cancel custom-113js0t"][title="Close"]').click()
 print('pop up closed')
 main_window = driver.current_window_handle
 print('get the main window',main_window)
 
 try:
    element = driver.find_element(By.CSS_SELECTOR,'button.custom-pr2mrc:nth-child(1)')
    sleep(3)
    try:
       try:
         print(f'likes:{str(element.text)}')
       except:
         likes = element.find_element(By.TAG_NAME,'span')
         print(f'likes:{str(element.text)}')

    except:
       print('noting found')
       pass
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
   try:
    WebDriverWait(driver,20).until(EC.visibility_of_element_located((By.TAG_NAME,'body')))
   except:
      pass
   print('move to new tab')
   sleep(5)  
#    driver.close()  # Close the current tab
   print('new tab closes')
   # Switch back to the remaining tab
   driver.switch_to.window(handles[0])
   print('move to main tab')
   sleep(3)
  except Exception as e:
   print(f'url error:{(e)}',level='error')  



def run_bot(dexUrl,token_pair):
    iteration = 1
    while True:
        try:
            if iteration>=2000:
                print('-----limit completed----')
                break
            
            print(f'-----------Running Iteration:{str(iteration)}------------')
            print("[+] Dextools Bot Starting")
                        
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
            driver.get(dexUrl)
            url = 'C4ZHt1fPtb6CLcUkivhnnNtxBfxYoJq6x8HEZpUexQvR'
            print("[+] Go to Dextools")
            sleep(10)
            check_captcha(driver)
            driver.implicitly_wait(10)
            sleep(5)
             
            actions(driver,token_pair)
            print('------DONE-------')
            restart(driver)
            
            print('-----completed-----')
            iteration+=1
            
            
        except Exception as e:
            print(f"Error so we move to next iteration:{str(e)} ",level='error')
            restart(driver)
          

def multiThread(dexUrl, token_pair):
    processes = []
    for _ in range(5):
        process_obj = Process(target=run_bot, args=(dexUrl, token_pair))
        processes.append(process_obj)
        process_obj.start()

    for process in processes:
        process.join()



app = Flask(__name__)


def background_task(dexUrl, token_pair):
    """Function to run in the background."""
    multiThread(dexUrl=dexUrl, token_pair=token_pair)

# API endpoint to generate a URL based on blockchain and pairAddress
@app.route('/generate-url', methods=['POST'])
def generate_url():
    data = request.get_json()
    dexType = data.get('dexType')
    blockchain = data.get('blockchain')
    pairAddress = data.get('pairAddress')

    # Check if both parameters are provided
    if not blockchain or not pairAddress:
        return jsonify({'error': "Both 'blockchain' and 'pairAddress' parameters are required."}), 400

    # Construct the URL with the provided parameters
    print(dexType,pairAddress)
    # jsonify({'url': generated_url})
    thread = threading.Thread(target=background_task, args=(dexType, pairAddress))
    thread.start()
    generated_url = f'https://{dexType}/{pairAddress}'
    # Send the generated URL back as a response
    return jsonify({'url': generated_url})

@app.route('/', methods=['Get'])
def print_hello_world():
    print('hello_world')
    return jsonify({'url': 'hello_world'})




# Start the server and listen on the specified port
if __name__ == '__main__':
    app.run(port=3000, debug=True)

