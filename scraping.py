#importing selenium, beautiful soup, and webdriver_manager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import time

def driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def scrape_nike(search_term):
    print(f"\n Searching Nike for '{search_term}'...")
    
    #formatting url
    url = f"https://www.nike.com/w?q={search_term.replace(' ', '%20')}&vst={search_term.replace(' ', '%20')}"
    driver = driver()
    
    #naviage to the url
    driver.get(url)
    
    #wait for page to load
    time.sleep(5)
    
    #grabs the raw html
    html = BeautifulSoup(driver.page_source, "html.parser")
    
    #selects the first 5 items from the search results
    products = html.select("div.product-card__body", limit=5)
    
    #stores results in a list
    results = []
    for product in products:
        title = product.select_one("div.product-card__title")
        price = product.select_one("div.product-price")
        if title and price:
            results.append({
                "store": "Nike", "name": title.get_text(strip=True), "price": price.get_text(strip=True)
            })

    driver.quit()
    return results

def scrape_bestbuy(search_term):
    print(f"\n🔍 Searching Best Buy for '{search_term}'...")
    url = f"https://www.bestbuy.com/site/searchpage.jsp?st={search_term.replace(' ', '+')}"
    driver = driver()
    driver.get(url)
    time.sleep(5)

    html = BeautifulSoup(driver.page_source, "html.parser")
    products = html.find_all("li", {"class": "sku-item"}, limit=5)

    results = []
    for product in products:
        name = product.find("h4")
        price = product.find("div", {"class": "priceView-hero-price priceView-customer-price"})
        if name and price:
            results.append({
                "store": "Best Buy", "name": name.get_text(strip=True), "price": price.find("span").get_text(strip=True)
            })

    driver.quit()
    return results