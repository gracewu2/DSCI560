import pandas as pd
import requests
from bs4 import BeautifulSoup
import pdfplumber
import os


CSV_FILENAME = 'marathon_winners.csv'
PDF_FILENAME = 'la_marathon_rules.pdf'
WEB_URL = 'https://en.wikipedia.org/wiki/Marathon'

#task 1
def explore_csv_data():
  
    print("TASK 1: EXPLORING CSV DATA")
    
    if not os.path.exists(CSV_FILENAME):
        print(f"Error: {CSV_FILENAME} not found. Please download it first.")
        return

    df = pd.read_csv(CSV_FILENAME)
    
    #display first 5 records
    print(f"\n[Preview] First 5 rows of {CSV_FILENAME}:")
    print(df.head())

    #get dataset size and dimensions
    rows, cols = df.shape
    print(f"\n[Stats] The dataset has {rows} rows and {cols} columns.")

    missing_data = df.isnull().sum()
    print("\n[Data Quality] Missing values per column:")
    print(missing_data[missing_data > 0]) 

  
    if 'Country' in df.columns:
        top_countries = df['Country'].value_counts().head(3)
        print(f"\n[Insight] Top 3 Winning Countries:\n{top_countries}")
    
    print("-" * 40)

#task 2
def explore_web_data():
   
    print("\nTASK 2: WEB SCRAPING")
    print(f"Scraping: {WEB_URL}")

    try:
        
        #  add header to bypass 403 error
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(WEB_URL, headers=headers)
        response.raise_for_status() 

        # parse html
        soup = BeautifulSoup(response.text, 'html.parser')

        paragraphs = soup.find_all('p')
        
        extracted_text = [p.get_text().strip() for p in paragraphs if p.get_text().strip()]
        
        if extracted_text:
            print(f"\n[Success] Extracted {len(extracted_text)} paragraphs.")
            print(f"[Sample] First paragraph: {extracted_text[0][:100]}...")

            # save to csv
            df_web = pd.DataFrame(extracted_text, columns=['Article_Content'])
            output_file = 'scraped_nutrition_data.csv'
            df_web.to_csv(output_file, index=False)
            print(f"[Storage] Saved scraped data to '{output_file}'")
        else:
            print("[Warning] No text found in <p> tags.")

    except Exception as e:
        print(f"Error scraping website: {e}")

    print("-" * 40)

#task 3
def explore_pdf_data():
    
    print("\nTASK 3: PDF TEXT EXTRACTION")
    
    if not os.path.exists(PDF_FILENAME):
        print(f"Error: {PDF_FILENAME} not found. Please download it first.")
        return

    try:
        # open the pdf
        with pdfplumber.open(PDF_FILENAME) as pdf:
            print(f"[Info] Processing {PDF_FILENAME} with {len(pdf.pages)} pages.")
            
            # extract text from the first page
            first_page = pdf.pages[0]
            text = first_page.extract_text()
            
            if text:
                print("\n[Sample] Extracted text from Page 1 (First 300 chars):")
                print(text[:300] + "...")
                
                # save to a text file
                with open("extracted_rules.txt", "w", encoding="utf-8") as f:
                    f.write(text)
                print(f"\n[Storage] Full text of Page 1 saved to 'extracted_rules.txt'")
            else:
                print("[Warning] No text found on Page 1. It might be an image-only PDF.")

    except Exception as e:
        print(f"Error processing PDF: {e}")
        
    print("-" * 40)

if __name__ == "__main__":

    explore_csv_data()
    explore_web_data()
    explore_pdf_data()
    print("\nData Exploration Complete.")