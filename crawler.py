#!/usr/bin/env python

import urllib2
from bs4 import BeautifulSoup
import lxml.html
import logging


class StackOverflow:
	@classmethod
	def search(cls, text, page = 0, pages = 10):
		text = text.replace(" ", "+")
		SEARCH_BASE_URL = "http://stackoverflow.com/search?q={0}"
		QUESTION_BASE_URL = "http://stackoverflow.com{0}"

		doc = urllib2.urlopen(SEARCH_BASE_URL.format(text)).read()

		soup = BeautifulSoup(doc)

		urls = []

		for item in soup.findAll("a", "question-hyperlink"):
			if item:
				href = item.attrs['href']
				if href:
					urls.append(QUESTION_BASE_URL.format(href))

		return urls[page : page + pages + 1]

	@classmethod
	def answer(cls, url):
		doc = urllib2.urlopen(url).read()
		content = urllib2.urlopen(url).read()
		doc = lxml.html.fromstring(content)
		title = doc.find_class("question-hyperlink")
		answers = doc.find_class("answer")
		for answer in answers:
			accepted = answer.find_class("vote-accepted-on")
			if accepted:
				text  = answer.find_class("post-text")[0]
				if hasattr(text, "text"):
					return { "title": title[0].text_content(), "content": lxml.html.tostring(text) } 
		return { "title": title[0].text_content(), "content": None }


#url = "http://stackoverflow.com/questions/601166/issues-with-beautifulsoup-parsing"
#print StackOverflow.answer(url)