from bs4 import BeautifulSoup 
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys 
import time 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import numpy as np

# reportlab
from reportlab.lib.pagesizes import letter, A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Frame, PageTemplate, BaseDocTemplate
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus.paragraph import Paragraph

def to_pdf(df: pd.DataFrame, most_expensive: pd.DataFrame, most_review: pd.DataFrame, average_storage_capacity: float):
    try:
        # styling        
        table_style = TableStyle([
            ('GRID',(0,0),(-1,-1),0.25,"black"),
            ('BOX',(0,0),(-1,-1),0.25,"black", None, (2,2,1))]
        )

        # build table
        df_table = Table(np.array(df).tolist())
        
        most_expensive_table = Table(np.array(most_expensive).tolist())
        most_review_table = Table(np.array(most_review).tolist())
        most_expensive_table.setStyle(table_style)
        most_review_table.setStyle(table_style)
        df_table.setStyle(table_style)
        
        # add to elements array
        elements = []
        elements.append(Paragraph("All"))
        elements.append(df_table)
        elements.append(Paragraph("Most expensive"))
        elements.append(most_expensive_table)
        elements.append(Paragraph("Most review"))
        elements.append(most_review_table)
        elements.append(Paragraph("Average storage capacity of all scraped laptops: " + str(average_storage_capacity) + "GB"))

        doc = SimpleDocTemplate("laptop_info.pdf", pagesize=A4)
        doc.build(elements)
        
    except Exception as e:
        print("Error when converting to markdown or pdf file with error: ", str(e))
    pass

def get_storage_capacity(description_text: str) -> str:
    try:
        phrases = description_text.split(", ")
        final_phrase = ""
        for phrase in phrases: 
            if phrase.find("GB") != -1 and len(phrase) > 3 and phrase.find("GTX") == -1 and phrase.find("TB") == -1 and phrase.find("Radeon") == -1 and phrase.find("GeForce") == -1 and phrase.find("RGB") == -1 and phrase.find("AMD") == -1:
                # check if it is plus
                if phrase.find("+") != -1:
                    multi_storage = phrase.split("+")
                    # return "GB+" + phrase
                    return str(
                        sum(
                            [
                                int(storage.split("GB")[0].strip()) 
                                for storage in multi_storage
                            ]
                        )
                    )
                   
                final_phrase = phrase.split("GB")[0].strip()

            if phrase.find("TB") != -1:
                if phrase.find("+") != -1:
                    multi_storage = phrase.split("+")
                    if multi_storage[0].find("TB") != -1 and multi_storage[1].find("GB") != -1: 
                        return str(int(multi_storage[0].split("TB")[0].strip()) * 1000 + int(multi_storage[1].split("GB")[0].strip()))
                    
                    if multi_storage[0].find("GB") != -1 and multi_storage[1].find("TB") != -1: 
                        return str(int(multi_storage[0].split("GB")[0].strip()) + int(multi_storage[1].split("TB")[0].strip()) * 1000)
                
                final_phrase = str(int(phrase.split("TB")[0].strip()) * 1000) # convert to GB
        return final_phrase
    except Exception as e:
        print("Error when getting storage capacity")
        return ""

# get_storage_capacity('Lenovo Legion Y720, 15.6" FHD IPS, Core i7-7700HQ, 8GB, 128GB SSD + 2TB HDD, GeForce GTX 1060 6GB, DOS, RGB backlit keyboard')
  
#url of the page we want to scrape 
url = "https://webscraper.io/test-sites/e-commerce/more/computers/laptops"
  
# initiating the webdriver. Parameter includes the path of the webdriver. 
driver = webdriver.Chrome()  
driver.get(url)  
wait = WebDriverWait(driver, 1) 
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

        result = {
            "laptops": [
                {
                    "title": card_body.a.get_text(strip=True),
                    "price": float(card_body.h4.get_text(strip=True)[1:]), # should handle exception here
                    "storage_capacity": int(get_storage_capacity(card_body.p.get_text(strip=True)) or '0'),
                    "review": int(card_body.find("p", {"class": "float-end review-count pull-right"}).get_text(strip=True).split(" ")[0]) # get the number only from string "x reviews"
                }
                for card_body in card_bodies
            ]
        }
       

        # build dataframe from dict and getting max price and review laptop information
        df = pd.DataFrame(result['laptops'])
        print(df)
        print("len(result['laptops'])", len(result['laptops']))
        most_expensive = df[df['price']==df['price'].max()]
        most_review = df[df['review']==df['review'].max()]
        print("\nlaptop with max price\n", df[df['price']==df['price'].max()])
        print("\nlaptop has max review\n", df[df['review']==df['review'].max()])
        print("\naverage scraped laptops\n", (round(df['storage_capacity'].sum() / len(result['laptops'])), 1))
        # write to pdf
        to_pdf(df, 
               most_expensive=most_expensive, 
               most_review=most_review, 
               average_storage_capacity=round(df['storage_capacity'].sum() / len(result['laptops']), 1)
        )
        break
    
    # click action on load more button 
    driver.execute_script("arguments[0].click();", load_more)
driver.close()




