import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from time import sleep
import requests

def load_proxies(file_path):
    """ Load the list of proxies from a given file. """
    with open(file_path, 'r') as file:
        proxies = [line.strip() for line in file if line.strip()]
    random.shuffle(proxies)  # Shuffle to randomize the order initially
    return proxies

def check_ip(driver):
    """Function to fetch and print the current IP using the driver instance."""
    try:
        driver.get("https://api.ipify.org")
        ip = driver.find_element(By.TAG_NAME, "body").text
        print("Current IP:", ip)
    except Exception as e:
        print("Failed to fetch IP from the driver:", str(e))

def setup_driver(proxy_url):
    """Setup Firefox WebDriver with the specified proxy settings."""
    firefox_options = Options()
    firefox_options.add_argument('--headless')  # Run headless if you don't need a GUI
    firefox_profile = webdriver.FirefoxProfile()
    firefox_profile.set_preference("network.proxy.type", 1)
    firefox_profile.set_preference("network.proxy.http", proxy_url.split(':')[0])
    firefox_profile.set_preference("network.proxy.http_port", int(proxy_url.split(':')[1]))
    firefox_profile.set_preference("network.proxy.ssl", proxy_url.split(':')[0])
    firefox_profile.set_preference("network.proxy.ssl_port", int(proxy_url.split(':')[1]))
    firefox_profile.set_preference("network.proxy.no_proxies_on", "")  # No exceptions
    firefox_profile.update_preferences()
    driver = webdriver.Firefox(options=firefox_options, firefox_profile=firefox_profile)
    return driver

def main():
 # Ensure this file path is correct and file is populated
    iteration = 0
    while iteration < 100:  # Let's say we want to run this 100 times
        # if not proxies:  # Reload and shuffle if list is empty
            # proxies = load_proxies("proxies.txt")

        # proxy_url = proxies.pop()  # Get a proxy from the list

        proxy_url=requests.get(
                 "https://ipv4.webshare.io/",
                    proxies={
                     "http": "http://shnuqnvu-rotate:mg5i9hbxda5c@p.webshare.io:80/",
                     "https": "http://shnuqnvu-rotate:mg5i9hbxda5c@p.webshare.io:80/"
                            }
                    ).text
        print(f"Using proxy: {proxy_url}")

        driver = setup_driver(proxy_url)
        check_ip(driver)

        sleep(5)  # Wait for some time before the next operation
        driver.quit()  # Close the browser after checking
        iteration += 1
        print('Iteration completed:', iteration)

if __name__ == '__main__':
        main()
