import re, os, random, sys
import requests
from urllib.request import Request, urlopen
# from bs4 import BeautifulSoup
from html.parser import HTMLParser


url='http://virt-openshift-05.lab.eng.nay.redhat.com/buildcorp/Runner-v3/'
buildcopr_runners = requests.get(url).text

# soup = BeautifulSoup(buildcopr_runners, features="html.parser") # 最好修改html对象内的字符编码为UTF-8
# title = soup.find('span',{'class':'titleTxt'}).getText()


class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print("Encountered a start tag:", tag)

    def handle_endtag(self, tag):
        print("Encountered an end tag :", tag)

    def handle_data(self, data):
    	if '2020-03-26 12:33' in data:
        	print("Encountered some data  :", data)


parser = MyHTMLParser()
parser.feed(buildcopr_runners)

print(parser)