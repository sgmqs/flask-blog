#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-12-25 20:58:42
# @Author  : org (928758777@qq.com)
# @Link    : ${link}
# @Version : $Id$

from jinja2 import Markup
class momentjs(object):
	"""docstring for momentjs"""
	def __init__(self, timestamp):
		
		self.timestamp = timestamp

	def render(self,format):
		return Markup("<script>\ndocument.write(moment(\"%s\").%s);\n</script>") %(self.timestamp.strftime("%Y-%m-%dT%H:%M:%S Z"),format)

	def format(self,fmt):
		return self.render("format(\"%s\")") % fmt

	def calendar(self):
		return self.render("calendar()")
	def fromNow(self):
		return self.render("fromNow()")