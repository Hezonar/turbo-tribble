from selenium import webdriver
from xvfbwrapper import Xvfb
vdisplay = Xvfb()
vdisplay.start()
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-setuid-sandbox")
driver = webdriver.Chrome('chromedriver.exe', chrome_options=chrome_options)
driver.get('https://google.com')
ff = open("file.txt", "w")
ff.write(driver.page_source.encode("utf-8"))
ff.close()
driver.close()
vdisplay.stop()
