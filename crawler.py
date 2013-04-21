#!/usr/bin/env python

import urllib2
from bs4 import BeautifulSoup
import logging


class StackOverflow:
	@classmethod
	def search(cls, text, page = 0, pages = 10):
		doc = cls._fetch_result_url(text);
		return cls._parse_results(doc, page, pages) 

	#Fetches the the page of results for a given query string
	@classmethod
	def _fetch_result_url(cls, text):
		text = text.replace(" ", "+")
		SEARCH_BASE_URL = "http://stackoverflow.com/search?q={0}"
		doc = urllib2.urlopen(SEARCH_BASE_URL.format(text)).read()
		return doc

	#Parse the StackOverflow results page
	@classmethod
	def _parse_results(cls, doc, page = 0, pages = 10):
		QUESTION_BASE_URL = "http://stackoverflow.com{0}"
		soup = BeautifulSoup(doc)
		urls = []

		anchors = soup.select('.result-link > span > a') 
		
		for anchor in anchors:
			if anchor:
				href = anchor.attrs['href']
				if href:
					urls.append(QUESTION_BASE_URL.format(href))
		
		return urls[page : page + pages + 1]

	
	@classmethod
	def answer(cls, url):
		import lxml.html
		# doc = urllib2.urlopen(url).read()
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
		

