#!/usr/bin/python
# coding: utf-8
'''
This is not for commercial, only for learning and self using
'''

import requests, os, time, sys, urlparse
from bs4 import BeautifulSoup


class getBook():
	def __init__(self, url):
		self.url = url

	def __get_page_text(self, url):
		web_data = requests.get(url)
		web_data.encoding = "GBK"
		return web_data.text

	def _get_page_soup(self, url):
		""" The code returned by this function need .decode('utf-8')"""
		web_data_text = self.__get_page_text(url)
		soup = BeautifulSoup(web_data_text)
		return soup

	def _get_page_soup_html(self, url):
		""" This function rewrite '.' for using html tag """
		web_data_text = self.__get_page_text(url)
		soup = BeautifulSoup(web_data_text, 'html.parser')
		return soup

	def get_book_title(self, url):
		soup = self._get_page_soup(url)
		book_title= str(soup.find("title")).split(">")[1].split("- 小说")[0]
		return book_title		

	def get_book_short_intro(self, url):
		soup = self._get_page_soup_html(url)
		contents = soup.tbody.contents[3].td.contents
		intro_title = contents[0].contents[0]
		intro_content = contents[2]
		return  '\n\n' + intro_title + '\n' + intro_content + '\n\n'

	def get_chapter_url_id(self, url):
		soup = self._get_page_soup(url)
		chapter_table = soup.find_all("tr", bgcolor="#ffffff")
		chapter_url_id = []
		for lines in chapter_table:
			for chapter in lines.find_all("td"):
				try:
					line_td = str(chapter).split('href="')[1].split('"')[0]
					chapter_url_id.append(line_td)
				except: continue
		return chapter_url_id
		
	def get_chapter_title_and_content(self, chapter_url):
		soup = self._get_page_soup(chapter_url)

		## get page title
		chapter_title= str(soup.find("font")).split(">")[1].split("<")[0]
		
		## get page content
		td= soup.find("td", width="820")
		td_tag=list(td)[1]
		for tag in td_tag.find_all('br'):
		    tag.replaceWith('')
		chapter_content = str(td_tag).replace('<p>','').replace('</p>','')		

		return '\n\n\n\n' + chapter_title + '\n\n' + chapter_content + '\n\n'

	def get_book_chapters_content(self, chapterUrlList):
		content = ""
		i = 0
		for chapter_url in chapterUrlList:
			print 'getting Chapter ' + str(i)
			print chapter_url
			content = content + str(self.get_chapter_title_and_content(chapter_url))
			i = i + 1
		return content


if __name__ == '__main__':
	## This book is scraped from http://www.kanunu8.com/ 
	## bookUrl is only the param stands for book id from url.
	bookUrl = sys.argv[1]
	book = getBook(bookUrl)
	bookName  = book.get_book_title(book.url)

	f = open(bookName, 'w')
	print "Book path: " + os.getcwd() +'/'+ bookName
	f.write(bookName)

	try:
		bookIntro = book.get_book_short_intro(book.url)
		f.write(bookIntro.encode('utf-8'))
	except: pass

	chapterUrlIds = book.get_chapter_url_id(book.url)
	chapterUrlList = [urlparse.urljoin(bookUrl,url) for url in chapterUrlIds]
	bookContent = ""
	bookContent = bookContent + "\n\n" + book.get_book_chapters_content(chapterUrlList)

	f.write(bookContent)
	f.close()
