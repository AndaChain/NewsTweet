import requests
from bs4 import BeautifulSoup


requ = requests.get("https://www.bbc.com/news/")
soup = BeautifulSoup(requ.text, "lxml")

data = open("C:/Users/s6201012620279/Desktop/NEWS2.txt","w")
data.write( str(soup) )
data = open("C:/Users/s6201012620279/Desktop/NEWS2.txt","r")

raw_data = soup.find("div",{"class":"nw-c-most-read__items gel-layout gel-layout--no-flex"})
using_1 = raw_data.find_all("li",{"class":"gel-layout__item gs-o-faux-block-link gs-u-mb+ gel-1/2@m gs-u-float-left@m gs-u-clear-left@m gs-u-float-none@xxl"})
using_2 = raw_data.find_all("li",{"class":"gel-layout__item gs-o-faux-block-link gs-u-mb+ gel-1/2@m"})

for i in using_1:
    print("Title: "+i.find("span",{"class":"gs-o-media"}).find("a").text,end="\n\n")
    print("Link: https://www.bbc.com"+i.find("span",{"class":"gs-o-media"}).find("a")["href"],end="\n\n\n")

# ref https://medium.com/equinox-blog/%E0%B8%A5%E0%B8%AD%E0%B8%87%E0%B8%97%E0%B8%B3-web-scraping-%E0%B8%94%E0%B9%89%E0%B8%A7%E0%B8%A2-beautifulsoup-%E0%B8%81%E0%B8%B1%E0%B8%99%E0%B9%80%E0%B8%96%E0%B8%AD%E0%B8%B0-b58dc0e1775a