from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType

# Replace 'path_to_geckodriver' with the path to your geckodriver executable
geckodriver_path = '/Users/xain/Documents/GitHub/DexTooTrending/geckodriver.exe'
dexscreener_url = 'https://dexscreener.com/'

# Set up proxy
proxy_address = 'otaflimz-rotate:dkii86y6u68v@p.webshare.io:80'  # Replace with your proxy IP and port
proxy = Proxy({
    'proxyType': ProxyType.MANUAL,
    'httpProxy': proxy_address,
    'sslProxy': proxy_address,
})

# Set up Firefox webdriver with proxy
firefox_capabilities = webdriver.DesiredCapabilities.FIREFOX.copy()
proxy.add_to_capabilities(firefox_capabilities)

# Set up webdriver
driver = webdriver.Firefox(executable_path=geckodriver_path, capabilities=firefox_capabilities)

# Open Dexscreener
driver.get(dexscreener_url)
