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
    drive = driver()
    
    #naviage to the url
    drive.get(url)
    
    #wait for page to load
    time.sleep(5)
    
    #grabs the raw html
    html = BeautifulSoup(drive.page_source, "html.parser")
    
    #gathers items from the search results up to 5 of them
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

    drive.quit()
    return results

def scrape_bestbuy(search_term):
    print(f"\nSearching Best Buy for '{search_term}'...")
    
    #formatting url
    url = f"https://www.bestbuy.com/site/searchpage.jsp?st={search_term.replace(' ', '+')}"
    drive = driver()
    
    #navigate to the url
    drive.get(url)
    
    #waiting for page to load
    time.sleep(5)

    #grabs the raw html
    html = BeautifulSoup(drive.page_source, "html.parser")
    
    #gathers items from the search results up to 5 of them
    products = html.find_all("li", {"class": "sku-item"}, limit=5)

    #stores results in a list
    results = []
    for product in products:
        name = product.find("h4")
        price = product.find("div", {"class": "priceView-hero-price priceView-customer-price"})
        if name and price:
            results.append({
                "store": "Best Buy", "name": name.get_text(strip=True), "price": price.find("span").get_text(strip=True)
            })

    drive.quit()
    return results

def display_results(results):
    print("\nThese are the products I found sorted from lowest to highest price :)")
    for item in results:
        print(f"- {item['name']} | {item['store']} | {item['price']}")
        
        
def store_results(results, dict, search_term):
    print("\n Stored results in database")
    dict[search_term] = results
    
def convert_to_float(product):
    return float(product["price"].replace("$", "").replace(",", "").strip())
    
def sort(products):
    stack = [(0, len(products) - 1)]  # Stack stores tuples of (low, high)
    while stack:
        low, high = stack.pop()
        
        # If there's more than one element in the range
        if low < high:
            pivot_index = partition(products, low, high)
            stack.append((low, pivot_index - 1))  # Left side
            stack.append((pivot_index + 1, high))  # Right side

    return products

def partition(products, low, high):
    pivot = convert_to_float(products[high])  # Choosing the last element as pivot
    i = low - 1
    
    for j in range(low, high):
        if convert_to_float(products[j]) <= pivot:
            i += 1
            products[i], products[j] = products[j], products[i]  # Swap elements
    
    products[i + 1], products[high] = products[high], products[i + 1]  # Swap pivot to the correct position
    return i + 1


def main():
    print("//// Price Comparison Tool Proof of Concept ////\n")
    
    search = input("Enter the product name you want to compare: ").strip()
    
    nike = {}
    bestbuy = {}
    
    nike_products = scrape_nike(search)
    bestbuy_products = scrape_bestbuy(search)
    
    if(not nike_products):
        print("No products were found for Nike")
    if(not bestbuy_products):
        print("No products were found for best buy")
        
    combined = nike_products + bestbuy_products
    sorted = sort(combined)
    display_results(sorted)
    
main()
    
    
    
    
    