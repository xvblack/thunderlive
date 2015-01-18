import xmltodict
import requests
import json
import utility

def force_list(obj):
	if not isinstance(obj, list):
		obj = [obj]
	return obj

def find_one_in_list(list, f):
	l = [obj for obj in list if f(obj)]
	if len(l) == 0:
		return None
	return l[0]

def find_one_by_name(list, name):
	return find_one_in_list(list, lambda x: x["name"] == name)

class Dictable:

	def _dict():
		pass

	def __str__(self):
		return json.dumps(self._dict(), indent=4)

	# def __repr__(self):
	# 	return "<statparser.NginxRtmpClientStat %s>" % self["name"]

	def __getitem__(self, name):
		return self._dict()[name]

class NginxRtmpStat(Dictable):

	class DuplicateNameError:
		
		def __init__(self, str):
			self.str = str

		def __str__(self):
			return self.str

	class NginxRtmpApplicationStat(Dictable):

		def __init__(self, dict):
			self.dict = dict

		def _dict(self):
			return self.dict

		def name(self):
			return self["name"]

		def streams(self):
			return [NginxRtmpStat.NginxRtmpStreamStat(d) for d in force_list(self["live"]["stream"])]


	class NginxRtmpStreamStat(Dictable):

		def __init__(self, dict):
			self.dict = dict

		def _dict(self):
			return self.dict

		def name(self):
			return self["name"]

		def uptime(self):
			return self["time"]

		def meta(self):
			return self["meta"]

		def clients(self):
			return [NginxRtmpStat.NginxRtmpClientStat(d) for d in force_list(self.dict["client"])]

	class NginxRtmpClientStat(Dictable):

		def __init__(self, dict):
			self.dict = dict

		def _dict(self):
			return self.dict

		def address(self):
			return self["address"]

		def uptime(self):
			return self["time"]

		def version(self):
			return self["flashver"]

	def __init__(self, dict=None):
		self.dict = dict

	def update_dict(self, dict):
		self.dict = dict

	def _dict(self):
		return self.dict

	def applications(self):
		apps = self.dict["rtmp"]["server"]["application"]
		apps = [NginxRtmpStat.NginxRtmpApplicationStat(app) for app in force_list(apps)]
		return apps

	def application(self, app_name):
		return find_one_by_name(self.applications(), app_name)

class NginxRtmpStatParser:

	def __init__(self, url):
		if url.find("://") == -1:
			url = "http://" + url
		self.url = url
		self.stat = NginxRtmpStat()

	def update_stat(self):
		response = requests.get(self.url)
		strs = response.text
		strs = strs.split("\n")
		strs = strs[2:]
		strs = "\n".join(strs)
		stat = xmltodict.parse(strs)
		self.stat.update_dict(stat)

	def get_stat(self):
		return self.stat

	def print_stat(self):
		print self.stat

def print_url(url):
	parser = NginxRtmpStatParser(url)
	parser.update_stat()
	parser.print_stat()