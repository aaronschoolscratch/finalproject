from urllib.request import urlopen, Request
from bs4 import BeautifulSoup




##############FOR MACS THAT HAVE ERRORS LOOK HERE################
## https://timonweb.com/tutorials/fixing-certificate_verify_failed-error-when-trying-requests_html-out-on-mac/

############## ALTERNATIVELY IF PASSWORD IS AN ISSUE FOR MAC USERS ########################
##  > cd "/Applications/Python 3.6/"
##  > sudo "./Install Certificates.command"


url = 'https://www.webull.com/quote/us/gainers'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}

		

req = Request(url, headers=headers)

webpage = urlopen(req).read()

soup = BeautifulSoup(webpage, 'html.parser')

print(soup.title.text)

stock_data = soup.findAll("div", attrs= {'class':'table-cell'})


'''
print(stock_data[1].text)
print(stock_data[3].text)
print(stock_data[4].text)
print(stock_data[1+11].text)
print(stock_data[1+22].text)

#print name of company, percentage change, and last price of top 5 companies.
'''


counter = 1



for i in range(5):  # Top 5 companies
    # Adjust the index for the main name (skipping abbreviations)
    company_name = stock_data[i * 11].find("a").text.strip()  # Extract company name from the anchor tag
    percentage_change = stock_data[i * 11 + 3].text.strip()  # Percentage change
    last_price = stock_data[i * 11 + 4].text.strip()  # Last price

    # Append the data as a tuple to the top_5_companies list
    top_5_companies.append((company_name, percentage_change, last_price))

# Print the results
for company in top_5_companies:
    print(f"Company: {company[0]}, Percentage Change: {company[1]}, Last Price: {company[2]}")