import re, os, random, sys
import requests
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup


# imglist = []
def getTitle(html):
    try:
        soup = BeautifulSoup(html, features="html.parser") # 最好修改html对象内的字符编码为UTF-8
        title = soup.find('span',{'class':'titleTxt'}).getText()
        print ("=== 文件夹名 ===")
        print (title)
        return title
    except Exception as e:
        print(e)

def getImgList(html):
    try:
        imglist = []
        soup = BeautifulSoup(html, features="html.parser") 
        # div_contentImg=soup.find_all('div',{'class':'contentMedia contentPadding'})
        div_contentImg=soup.find_all('div',{'class':'contentImg'})
        for d in div_contentImg:
            imageSrc = d.find('img')['src']
            imglist.append(imageSrc)
        return imglist
    except Exception as e:
        print(e)
        pass

def getPic(url=''):
    # 1. get whole page text, return response object
    print ("######### current url ##########")
    print (url)
    response = requests.get(url)

    # 2. get title and create folder (folder name is title)
    folderName = getTitle(response.text)
    fullPath = '/home/xiaocwan/Pictures/myartical/'+ str(folderName) +'/'
    print (fullPath)
    if not os.path.exists(fullPath): os.makedirs(fullPath)

    # 3. get image src list and download them one by one
    imglist = getImgList(response.text)
    for imgSrc in imglist:
        try:
            number = str(imglist.index(imgSrc)+1)
            f = open(fullPath + number + ".jpg", 'wb') # 这里最好使用threading
            
            headers = {}
            ua = [{'User-Agent':'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0'}]
            ua.append({'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/66.0'})
            ua.append({'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/62.0'})
            ua.append({'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/60.0'})
            headers.update(random.choice(ua))
            headers.update({'Referer': url})

            req = Request(url=imgSrc, headers=headers ) 
            f.write((urlopen(req)).read())
            print('pic %s: ok '%number)
            f.close()
        except Exception:
            pass
    folderName = ''
    print("######### finish current url ##########")



########################### start ###########################

urls = sys.argv[1]
for u in urls.split():
    getPic(u)

print("～～～～～～～～～ ALL Finish! ～～～～～～～～～")
