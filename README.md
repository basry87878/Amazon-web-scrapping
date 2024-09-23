Amazon Product Scraper

scrapping amazon data and saving it into excel file

![amazonscrapping](https://github.com/user-attachments/assets/f2f974fd-d2b9-45c1-a9b0-cff833d7000e)



This Python project scrapes product details from Amazon, including title, pricing, reviews, and sub-category information, using BeautifulSoup and Requests. It also fetches the Best Seller URL for the product's sub-category.
Features:

    Scrapes product details such as Title, ASIN, Best Seller Rank (BSR), Category, Sub Category, Normal Price, Deal Price, and the latest Review.
    Retrieves the number of Global Ratings and Reviews.
    Extracts the Best Seller URL based on the product's sub-category.
    Returns a comprehensive DataFrame of the scraped data.

Technologies Used:

    Requests: To send HTTP requests for product and review pages.
    BeautifulSoup: For HTML parsing and extracting information from the Amazon page.
    lxml: Used with XPath to retrieve specific sub-category links.
    pandas: For handling and structuring the extracted data in a DataFrame.
