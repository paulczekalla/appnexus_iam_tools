import requests
import json

class HttpHandler:
	
	def __init__(self, baseUrl = None, proxies = None, service = None, token = None):
		self._token = token
		self._proxies = proxies
		self._baseUrl = baseUrl
		self._service = service
		
	def setToken(self, token):
		self._token = token
		
	def getToken(self):
		return self._token

	def getRequest(self, service=None, params=None):
		if service is None:
			service = self._service
		
		url = self._baseUrl + "/" + service
		
		if params is not None:
			url += "?"
			for k,v in params.items():
				url += k + "=" + v + "&"
		print("GET " + url)
				
		if self._token is not None:
			auth = 'authorization:'+self._token
			header = {'authorization':self._token}
			return requests.get(url, headers=header, proxies=self._proxies)
		else:
			print("No Authorization Token is set")
		
	def getRequestPage(self, paginationStartNumer, service=None, params=None):
		if service is None:
			service = self._service
		
		url = self._baseUrl + "/" + service + "?start_element=" + str(paginationStartNumer)

		if params is not None:
			for k,v in params.items():
				url += "&" + k + "=" + v

		print("GET " + url)
				
		if self._token is not None:
			auth = 'authorization:'+self._token
			header = {'Authorization':self._token}
			return requests.get(url, headers=header, proxies=self._proxies)
		else:
			print("No Authorization Token is set")
		
	def postRequest(self, payload, service=None, params=None):
		if service is None:
			service = self._service
			
		url = self._baseUrl + "/" + service

		if params is not None:
			first_param = params.popitem()
			url += "?{0}={1}".format(first_param[0], first_param[1])
			
			for k,v in params.items():
				url += "&" + k + "=" + v

		print("POST " + url)
		
		if self._token is not None:
			header = {'Authorization':self._token}
			return requests.post(url, headers=header, data=json.dumps(payload))
		
		return requests.post(url, data=json.dumps(payload))


	def putRequest(self, payload, service=None, params=None):
		if service is None:
			service = self._service
			
		url = self._baseUrl + "/" + service

		if params is not None:
			first_param = params.popitem()
			url += "?{0}={1}".format(first_param[0], first_param[1])
			
			for k,v in params.items():
				url += "&" + k + "=" + v

		print("PUT " + url)
		
		if self._token is not None:
			header = {'Authorization':self._token}
			return requests.put(url, headers=header, data=json.dumps(payload))

		
	def deleteRequest(self, service=None, params=None):
		if service is None:
			service = self._service
			
		url = self._baseUrl + "/" + service

		if params is not None:
			first_param = params.popitem()
			url += "?{0}={1}".format(first_param[0], first_param[1])
			
			for k,v in params.items():
				url += "&" + k + "=" + v

		print("DELETE " + url)
		
		if self._token is not None:
			header = {'Authorization':self._token}
			return requests.delete(url, headers=header)
