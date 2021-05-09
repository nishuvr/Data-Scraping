import os
import csv
import urllib
import urllib.request
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.request import urlretrieve
import numpy as np
print("Scraping Products...")
for j in range(0,8):
    url = "https://www.zalando.co.uk/womens-clothing-tops/"+"?p="+str(j)
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    content=soup.find_all(attrs={'class':'qMZa55 SQGpu8 iOzucJ JT3_zV DvypSJ'})
    for i in content:
        article="https://www.zalando.co.uk"
        tags=i.find('a')
        data=tags.get('aria-label')
        link=tags.get('href')
        article=article+link+'\n'
        f=open("links.txt","a")
        f.write(article)
    f.close()
file=open("links.txt","r")
Lines = file.readlines()
data=[]
d=['Article_no','Brand','Product Details','Price in £']
data.append(d)
print("Downloading Images...")
for line in Lines:
    url = line
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    c=soup.find_all('li',{"class":"LiPgRT DlJ4rT S3xARh"})
    #there is some issue downloading the pack products images so excluding those and the links with outfits have the products of a particular look of the model so excluding that too
    if "pack" not in line and "outfits" not in line :
        for i,j in zip(c,range(len(c))):
            images = i.find('img')
            img=images.attrs['src']
            n=images.attrs['alt'].split('-')[0:5]
            s=""
            nameoffolder = s.join(n)
            tempCheck = img.split('.')
            check = str(tempCheck[len(tempCheck) - 1])
            check = check.split('?')
            check = check[0]
            nameOfFile = images.attrs['alt']+'-'+str(j)
            nameoffolder=nameoffolder.replace("  ","-")
            nameoffolder=nameoffolder[:-1]
            nameOfFile = nameOfFile.replace(" ","")
            if (check == "jpg" or check == "jpeg" or check == "png"):
                if check == "jpg":
                    ImageType = ".jpg"
                elif check == "jpeg":
                    ImageType=".jpeg"
                else:
                    ImageType = ".png"
                folderIndividualName = "ScrapedImages/" + nameoffolder + "/" 
                image_local_path=folderIndividualName + nameOfFile + ImageType
                try:
                    if not os.path.exists(folderIndividualName):
                        os.makedirs(folderIndividualName)
                    urlretrieve(img, image_local_path)
                except Exception as e:
                    continue     
        brand=soup.find('h3',{"class":"OEhtt9 ka2E9k uMhVZi uc9Eq5 pVrzNP _5Yd-hZ"})
        brand=brand.text
        price=soup.find('div',{"class":"_0xLoFW vSgP6A"}).find('span',{"class":"uqkIZw"})
        price=price.text
        product=soup.find('h1',{"class":"OEhtt9 ka2E9k uMhVZi z-oVg8 pVrzNP"})
        product=product.text
        article_no = url.split('/')
        article_no = article_no[-1].split("-")
        article_no = article_no[-2:]
        s="-"
        article_no = s.join(article_no)
        article_no = article_no.split(".")[0].upper()
        d1=[article_no,brand,product,price]
        data.append(d1)
print("Saving product details...")
np.savetxt("details.csv", data, delimiter =",",fmt ='% s')
print("Done")

        