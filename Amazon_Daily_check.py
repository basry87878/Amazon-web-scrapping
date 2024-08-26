#!/usr/bin/env python
# coding: utf-8

# # Amazon webscrapping for some products 

# The task goal is getting daily data for a product, each target product has a unique ASIN that will be used in filtering the target product

# ## Planning

# ##### using the webpage link to find the target Product 
# - parsing data from the returned webpage data:
# - Product Title
# - ASIN
# - (Best Sellers Rank , Category, Sub-Category) 
# - Normal Price
# - Deal Price
# - Best Seller URL
# - Review
# - Global Rating
# - Latest Review (filter by most recent)
# 

# after getting my data ready:
# 
# - Generate Google sheet, add today's date, the daily data
# - automate the program to run once each day
#     

# ##### future work
# 
# - Com. High: Competitor high price (high deal price )
# - Comp. Low: Competitor lower price (low deal price )
# - Liquidation Price: the lowest price in latest ,90 days
# - Number of Reviews
# - Recommended Price (AVG (Best Seller)): price of best URL usually the one which is most relevant and lower BSR
# - Alerts
#  
# 

# In[20]:


import lxml
import requests
import pandas as pd
import time
import re
from datetime import date
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl import load_workbook

date = date.today().strftime("%d/%m/%Y")
ASIN = 'B06XKMH86J'
url= f"https://www.amazon.sa/-/en/VIVOSUN-Temperature-Hydroponics-Household-Certified/dp/{ASIN}"
url_reviews = f"https://www.amazon.sa/-/en/VIVOSUN-Temperature-Hydroponics-Household-Certified/product-reviews/{ASIN}/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews"

headers = ({'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})

page = requests.get(url, headers=headers)
page2 = requests.get(url_reviews, headers=headers)
print(page.status_code)
soup = BeautifulSoup(page.content, "html.parser")
# Delay before making the request for reviews page
time.sleep(2)  # Adjust delay as needed
soup_reviews = BeautifulSoup(page2.content, "html.parser")

#to add new values to the worksheet 
file_path = r"C:\Users\Test\projects\sample_project_1\Web_Scrapping\Stock_Daily_check.xlsx"
sheet_name='B09GCYH4R6 PH AND TDS METER'


def main(soup, soup_reviews):
    Information = []
    Additional_Information = soup.find("div", {"id":"productDetails_db_sections"}).text.strip()
    # Use regular expression to split by 2 or more spaces
    Additional_Information = re.split(r'\s{2,}', Additional_Information)
    #Title
    Product_title = soup.find("span", {"id":"productTitle"}).get_text(strip=True) #Information.append({"Title": Product_title})
    #BSR
    BSR = int(re.search(r"#(\d+(?:,\d+)*)", Additional_Information[9]).group(1).replace(',', '')) 
    #category
    category = re.search(r"in (.*?) \(", Additional_Information[9]).group(1) 
    #Sub_Category
    Sub_Category = Additional_Information[10].lstrip('#').strip()
    #Normal Price
    Normal_Price = re.sub(r"[^\d.]", "", soup.find("span", {"class":"a-offscreen"}).text.strip())
    Normal_Price = Normal_Price[:Normal_Price.find('.') + 3]  # Slice up to 2 digits after '.'
    #Deal Price
    Deal_Price = re.sub(r"[^\d.]", "", soup.find("span", {"class":"a-price a-text-price"}).text.strip())
    Deal_Price = Deal_Price[:Deal_Price.find('.') + 3]  # Slice up to 2 digits after '.'
    #Review
    review = Additional_Information[4]
    #Latest Review
    latest_review = soup.find("a", {"class":"a-size-base a-link-normal review-title a-color-base review-title-content a-text-bold"}).find_all("span")
    latest_review = latest_review[2].text.strip()
    # Number of Ratings & Reviews
    ratings_text = soup_reviews.find("div", {"class":"a-row a-spacing-base a-size-base"}).text.strip().split()
    Num_ratings = ratings_text[3].replace(",", "")  # Remove commas 
    Num_reviews = ratings_text[0].replace(",", "")  # Remove commas

    
    
    Information.append({
        "Date": date,
        "Title": Product_title,
        "ASIN": ASIN,
        "BSR": BSR,
        "Category": category,
        "Sub Category": Sub_Category,
        "Normal Price": Normal_Price,
        "Deal Price": Deal_Price,
        "Review": review,
        "Latest Review": latest_review,
        "Global Ratings": Num_ratings,
        "Reviews": Num_reviews
        
    })

    return (Information) #this is a list of info

# Create DataFrame
df = pd.DataFrame(main(soup, soup_reviews))
print("the program is running..")
    

#add new values, sheets represent the entire Excel sheet
def add_values(file_path, sheet_name):
    sheets = load_workbook(file_path)
    worksheet = sheets[sheet_name]
    
    for r in dataframe_to_rows(df, index=False, header=False):
        worksheet.append(r)
    
    sheets.save(file_path)    
    
add_values(file_path, sheet_name)  
print("data has been scrapped successfully")

