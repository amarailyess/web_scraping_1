import requests
from bs4 import BeautifulSoup
import json

def getPageNumber(url,index):
    return url + str(index)

def getPromotionLink(promotion):
    return "https://www.automobile.tn" + promotion['href']

def getRequestResult(url):
    source = requests.get(url)
    return source

def getSoupResult(urlpage):
    source = getRequestResult(urlpage)
    soup = BeautifulSoup(source.text, features="lxml")
    return soup

def getTitle(soup,promotionDetails):
    titleClass = "page-title"
    title = soup.find('h3', class_=titleClass)
    promotionDetails['title'] = title.text
    return promotionDetails
def getPhone(soup,promotionDetails):
    phoneClass = "btn-main-phone"
    phone = soup.find('button', class_=phoneClass)
    promotionDetails['phone'] = phone.text.replace(" ", "")
    return promotionDetails
def getRegistrationDate(soup,promotionDetails):
    registrationDateTag = "Insérée le : "
    registrationDate = soup.find('label', text=registrationDateTag)
    promotionDetails[registrationDateTag.split(" ")[0]] = registrationDate.nextSibling.text
    return promotionDetails
def getGovernorate(soup,promotionDetails):
    governorateTag = "Gouvernorat : "
    previousGovernorateElement = soup.find('label', text=governorateTag)
    promotionDetails[governorateTag.split(" ")[0]] = previousGovernorateElement.nextSibling.text
    return promotionDetails
def getPrice(soup, promotionDetails):
    priceTageClass = "floating-infos"
    PreviousPriceElement = soup.find('div', class_=priceTageClass)
    promotionDetails["prix"] = PreviousPriceElement.find_next_sibling("div", class_="buttons").findChild("div",recursive=False).findChild("span").text
    return promotionDetails

def hasShop(soup, promotionDetails):
    shopTag = "member-details-widget"
    shop = soup.find('div', class_=shopTag)
    if (shop):
        promotionDetails["shop"] = True
    else:
        promotionDetails["shop"] = False
    return promotionDetails

def getPromotionDetails(promotion, promotion_number):
    soup = getSoupResult("https://www.automobile.tn" + promotion['href'])
    promotionDetails = {}
    promotionDetails['id'] = promotion_number
    promotionDetails = getTitle(soup, promotionDetails)
    promotionDetails = getPhone(soup, promotionDetails)
    promotionDetails = getRegistrationDate(soup, promotionDetails)
    promotionDetails = getGovernorate(soup, promotionDetails)
    promotionDetails = getPrice(soup, promotionDetails)
    promotionDetails = hasShop(soup, promotionDetails)
    return promotionDetails

def getDataPage(promotions, promotion_number, data):
    for promotion in promotions:
        promotionDetails = getPromotionDetails(promotion, promotion_number)
        data.append(promotionDetails)
        promotion_number += 1
    return data, promotion_number

def getpromotions(url, i):
    urlpage = getPageNumber(url, i)
    soup = getSoupResult(urlpage)
    promotions = soup.findAll("a", {"class": "details-container"})
    return promotions

def toJson(data):
    with open('data_results.json', 'w') as outfile:
        json.dump(data, outfile)

def getDataFromAutomobile(url, start_page_number, end_page_number):
    promotion_number = 1
    data = []
    for i in range(start_page_number,end_page_number+1):
        print("page",i,"...")
        promotions =  getpromotions(url,i)
        data, promotion_number = getDataPage(promotions, promotion_number, data)
    toJson(data)

start_page_number = 1
end_page_number = 1
url = "https://www.automobile.tn/fr/occasion/"
getDataFromAutomobile(url, start_page_number, end_page_number)