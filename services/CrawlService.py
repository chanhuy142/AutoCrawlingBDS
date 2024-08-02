import instructor
import google.generativeai as genai
from pydantic import BaseModel
import ollama
from ast import Return
from logging import config
from multiprocessing import process
from matplotlib.pyplot import cla
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from typing import Deque, List, Optional, Tuple
import os
load_dotenv()
def process_data(data):
    # Process your data here
    #convert to json
    
    return {'processed': True, 'data': data}
#a helper function to scroll down the page
def scroll_down_page(driver, speed=8):
    current_scroll_position, new_height= 0, 1
    while current_scroll_position <= new_height:
        current_scroll_position += speed
        driver.execute_script("window.scrollTo(0, {});".format(current_scroll_position))
        new_height = driver.execute_script("return document.body.scrollHeight")

#this will return driver object
def getHtmlFile(url):
    options = uc.ChromeOptions() 
    #options.headless = False  

    driver = uc.Chrome(use_subprocess=True, options=options) 
    
    t = time.time()
    driver.set_page_load_timeout(10)
    try:
        driver.get(url)
    except TimeoutException:
        driver.execute_script("window.stop();")
        return driver
    return driver




#this will return list of links
def getLinks(driver, className):
    #sleep to wait for page to load
    time.sleep(3)
    elements=driver.find_elements(By.CSS_SELECTOR,className)
    links = []
    print(len(elements))
    #get href of all elements
    for element in elements:
        #print(element.get_attribute("href"))
        links.append(element.get_attribute("href"))
    return links

def getObject(driver, link):
    try:
        driver.get(link)
        #sleep to wait for page to load
        time.sleep(1)
        
    except TimeoutException:
        driver.execute_script("window.stop();")
    html=driver.page_source
    #get all image source as string
    images = driver.find_elements(By.CSS_SELECTOR, "img")

    

    
    soup = BeautifulSoup(html, 'html.parser')
    html = soup.get_text()
    
    for image in images:
        if image.get_attribute("src") is not None:
            html += " "+image.get_attribute("src")
    
    
    
    
    try:
        class Project(BaseModel):
            name: str
            price: int
            area: float
            legal: str
            address: str
            province: str
            district: str
            image: str
            


        genai.configure(api_key=os.getenv('API_KEY')) # alternative API key configuration
        client = instructor.from_gemini(
            client=genai.GenerativeModel(
                model_name="models/gemini-1.5-flash-latest",  
            ),
            mode=instructor.Mode.GEMINI_JSON,
        )

        resp = client.chat.completions.create(
            
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": html}
            ],
            response_model=Project,
        ) 
        jsonObject= {
            "name": resp.name,
            "price": resp.price,
            "area": resp.area,
            "legal": resp.legal,
            "address": resp.address,
            "province": resp.province,
            "district": resp.district,
            "image": resp.image,
        }
    except:
        jsonObject= {
            "name": "N/A",
            "price": "N/A",
            "area": "N/A",
            "legal": "N/A",
            "address": "N/A",
            "province": "N/A",
            "district": "N/A",
            "image": "N/A",}
    return jsonObject
def genPageLink(url):
    class Link(BaseModel):
        link: List[str]
    genai.configure(api_key=os.getenv('API_KEY')) # alternative API key configuration
    client = instructor.from_gemini(
        client=genai.GenerativeModel(
            model_name="models/gemini-1.5-flash-latest",  
        ),
        mode=instructor.Mode.GEMINI_JSON,
    )

    resp=client.chat.completions.create(
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content":"be awared of trailing character,create 1 link like this with different page:" +url}
        ],
        response_model=Link,
    )
    print(resp.link)
    return resp.link
    
   
    
    
    
def Crawl(url, classConfig):
    #print("this is link"+genPageLink(url))
    URLs=genPageLink(url)
    items = []
    for URL in URLs:
        print(URL)
        driver = getHtmlFile(URL)
        links = getLinks(driver, classConfig["link"])
        print(links)
        driver.set_page_load_timeout(5)
        for link in links:
            item = getObject(driver, link)
            print(item)
            items.append(item)
    
    return items

