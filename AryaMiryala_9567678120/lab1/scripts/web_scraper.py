import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType

url = "https://www.cnbc.com/world/?region=world"

def scrape_data():
    print("Setting up Headless Chrome Driver...")
    
    # configuarations
    chrome_options = Options()
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    try:
        # initialize the driver
        service = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        print(f"Loading {url}...")
        driver.get(url)
        
        print("Waiting 5 seconds for dynamic content...")
        time.sleep(5)
        
        # get the html
        page_source = driver.page_source
        
        # save to file
        file_path = os.path.join("..", "data", "raw_data", "web_data.html")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(page_source)
            
        print(f"Success! Saved rendered HTML to {file_path}")

    except Exception as e:
        print(f"Error: {e}")
        
    finally:
        if 'driver' in locals():
            driver.quit()

if __name__ == "__main__":
    scrape_data()