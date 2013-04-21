#!/usr/bin/env python
import webapp2
from handlers import *

app = webapp2.WSGIApplication([
							('/search', Search),
							('/get', Get),
							('.*', Home)
							],
                              debug=True)
