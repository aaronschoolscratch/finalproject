# pip install requests (to be able to get HTML pages and load them into Python)
# pip install bs4 (for beautifulsoup - python tool to parse HTML)


from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

##############FOR MACS THAT HAVE CERTIFICATE ERRORS LOOK HERE################
## https://timonweb.com/tutorials/fixing-certificate_verify_failed-error-when-trying-requests_html-out-on-mac/

##############FOR PCs THAT HAVE CERTIFICATE ERRORS LOOK HERE################
## https://support.chainstack.com/hc/en-us/articles/9117198436249-Common-SSL-Issues-on-Python-and-How-to-Fix-it

############## ALTERNATIVELY IF PASSWORD IS AN ISSUE FOR MAC USERS ########################
##  > cd "/Applications/Python 3.6/"
##  > sudo "./Install Certificates.command"



url = 'https://www.worldometers.info/coronavirus/country/us'
# Request in case 404 Forbidden error
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}

req = Request(url, headers=headers)

webpage = urlopen(req).read()

soup = BeautifulSoup(webpage, 'html.parser')



#SOME USEFUL FUNCTIONS IN BEAUTIFULSOUP
#-----------------------------------------------#
# find(tag, attributes, recursive, text, keywords)
# findAll(tag, attributes, recursive, text, limit, keywords)

#Tags: find("h1","h2","h3", etc.)
#Attributes: find("span", {"class":{"green","red"}})
#Text: nameList = Objfind(text="the prince")
#Limit = find with limit of 1
#keyword: allText = Obj.find(id="title",class="text")

print(soup.title.text)

table_rows = soup.findAll("tr")

#print(table_rows[1])

state_death_ratio = ""
state_best_testing = ""
state_worst_testing = ""
highest_death_ratio = 0.0
best_test_ratio = 0.0
worst_test_ratio = 1000.0

for row in table_rows[2:53]:
    td = row.findAll("td")
    state = td[1].text.strip('\n')

    # Additional code to calculate death ratio and test ratio
    try:
        total_cases = int(td[2].text.strip().replace(',', ''))
        total_deaths = int(td[4].text.strip().replace(',', ''))
        total_tests = int(td[10].text.strip().replace(',', ''))
        population = int(td[12].text.strip().replace(',', ''))

        # Calculate death ratio
        death_ratio = (total_deaths / total_cases) * 100 if total_cases > 0 else 0

        # Calculate test ratio
        test_ratio = (total_tests / population) * 100 if population > 0 else 0

        # Print state with death and test ratios
        print(f"{state}: Death Ratio = {death_ratio:.2f}%, Test Ratio = {test_ratio:.2f}%")

        # Track the highest death ratio
        if death_ratio > highest_death_ratio:
            highest_death_ratio = death_ratio
            state_death_ratio = state

        # Track the best and worst testing ratios
        if test_ratio > best_test_ratio:
            best_test_ratio = test_ratio
            state_best_testing = state

        if test_ratio < worst_test_ratio:
            worst_test_ratio = test_ratio
            state_worst_testing = state

    except ValueError:
        print(f"Data missing or invalid for {state}")

# Final output
print(f"\nState with the highest death ratio: {state_death_ratio} ({highest_death_ratio:.2f}%)")
print(f"State with the best testing ratio: {state_best_testing} ({best_test_ratio:.2f}%)")
print(f"State with the worst testing ratio: {state_worst_testing} ({worst_test_ratio:.2f}%)")
