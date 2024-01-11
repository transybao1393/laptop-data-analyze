import requests 
from bs4 import BeautifulSoup 
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys 
import time 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd

def get_storage_capacity(description_text: str) -> str:
    phrases = description_text.split(", ")
    final_phrase = ""
    for phrase in phrases: 
        if phrase.find("GB") != -1 and len(phrase) > 3 and phrase.find("GTX") == -1 and phrase.find("TB") == -1 and phrase.find("Radeon") == -1 and phrase.find("GeForce") == -1 and phrase.find("RGB") == -1:
            # print(phrase.strip()) 
            final_phrase = phrase.strip()

        if phrase.find("TB") != -1:
            # print(phrase.strip()) 
            final_phrase = phrase.strip()
    return final_phrase

# get_storage_capacity('Lenovo Legion Y720, 15.6" FHD IPS, Core i7-7700HQ, 8GB, 128GB SSD + 2TB HDD, GeForce GTX 1060 6GB, DOS, RGB backlit keyboard')
  
#url of the page we want to scrape 
url = "https://webscraper.io/test-sites/e-commerce/more/computers/laptops"
  
# initiating the webdriver. Parameter includes the path of the webdriver. 
driver = webdriver.Chrome()  
driver.get(url)  
wait = WebDriverWait(driver, 1)
  
# this is just to ensure that the page is loaded 
# time.sleep(5)  

wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[3]/div/div[2]/a')))

# running until meet stop condition
while True:
    load_more = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[3]/div/div[2]/a")))
    # load_more.location_once_scrolled_into_view
    actions = ActionChains(driver)
    actions.move_to_element(load_more).perform()
    time.sleep(0.5)
    driver.execute_script("arguments[0].scrollIntoView();", load_more)
    time.sleep(0.5)
    displayed = load_more.get_attribute("style")
    if "none" in displayed:
        time.sleep(4) # time sleep to make sure the page is loaded
        html = driver.page_source 
        soup = BeautifulSoup(html, "html.parser") 
        all_divs = soup.find('div', {'class' : 'row ecomerce-items ecomerce-items-more'}) 
        
        # get all card body
        card_bodies = soup.find_all("div", {"class": "card-body"})
        
        # build result dict to serve dataframe
        result = {
            "laptops": [
                {
                    "title": card_body.a.get_text(strip=True),
                    "price": float(card_body.h4.get_text(strip=True)[1:]), # should handle exception here
                    "description": card_body.p.get_text(strip=True),
                    "storage_capacity": get_storage_capacity(card_body.p.get_text(strip=True)),
                    "review": int(card_body.find("p", {"class": "review-count"}).get_text(strip=True)[0]) # get the number only from string "x reviews"
                }
                for card_body in card_bodies
            ]
        }

        # build dataframe from dict and getting max price and review laptop information
        df = pd.DataFrame(result['laptops'])
        print(df)
        print("\nlaptop with max price\n", df[df['price']==df['price'].max()])
        print("\nlaptop has max review\n", df[df['review']==df['review'].max()])

        break
    
    # click action on load more button 
    driver.execute_script("arguments[0].click();", load_more)
driver.close()




