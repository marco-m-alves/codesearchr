#!/usr/bin/env python
import webapp2
from webapp2_extras import jinja2
from crawler import StackOverflow
import json
import datetime
import logging

class BaseHandler(webapp2.RequestHandler):

	@webapp2.cached_property
	def jinja2(self):
		# Returns a Jinja2 renderer cached in the app registry.
		return jinja2.get_jinja2(app=self.app)

	def render_response(self, _template, **context):
		# Renders a template and writes the result to the response.
		rv = self.jinja2.render_template(_template, **context)
		self.response.write(rv)


class Home(BaseHandler):

    def get(self):
        self.redirect('/static/html/index.html')


def dthandler(obj):
	if isinstance(obj, datetime.datetime):
		return obj.isoformat()
	else:
		return obj

class Search(BaseHandler):
    def get(self):
        q = self.request.get("q")
        q = q.replace(" ", "+")
        results = StackOverflow.search(q)

        if self.request.get("callback"):
        	self.response.out.write("{0}({1})".format(self.request.get("callback"), json.dumps(results, default = dthandler))) 
        else:
        	self.response.out.write(json.dumps(results)) 
     
class Get(BaseHandler):
    def get(self):
        q = self.request.get("q")
        q = q.replace(" ", "+")
        logging.info(q)
        results = StackOverflow.answer(q)
        logging.info(results)
        if self.request.get("callback"):
        	self.response.out.write("{0}({1})".format(self.request.get("callback"), json.dumps(results, default = dthandler))) 
        else:
        	self.response.out.write(json.dumps(results))