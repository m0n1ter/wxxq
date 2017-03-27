
from selenium import webdriver
from selenium.webdriver.common.by import By
chromedriver = 'C:/Program Files (x86)/Google/Chrome/Application/chromedriver.exe'
driver = webdriver.Chrome(chromedriver)
driver.get('http://trains.ctrip.com/TrainBooking/Search.aspx?from=shanghai&to=taiyuannan&day=2&number=&fromCn=%C9%CF%BA%A3&toCn=%CC%AB%D4%AD%C4%CF')
price_list = driver.find_element(By.CLASS_NAME,'trainList_box')
print price_list.get_attribute('innerHTML')