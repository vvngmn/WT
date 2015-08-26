import re, os, time
import requests
import RequestLib, CommonLib, WebtopResponseWrap, Upload, PrefsLib
from Crypto.Cipher import AES
import hashlib

class SessionTokenLib():
	def __getKey(self):
		key = 'This is insecure, change'
		encryptedKey = hashlib.sha512(key).hexdigest()
		encryptedKey = encryptedKey.decode('hex')
		return encryptedKey[0:16]
	
	def __decrypt(self, encrypedToken): 
		obj = AES.new(self.__getKey(), AES.MODE_ECB)
		decode_hex = encrypedToken.decode('hex')
		crypt = obj.decrypt(decode_hex)
		return crypt

	def __encrypt(self, originToken):
		BS = 16
		pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS) 
		#unpad = lambda s : s[0:-ord(s[-1])]
		obj = AES.new(self.__getKey(), AES.MODE_ECB)
		cryptToken = obj.encrypt(pad(originToken))
		return cryptToken.encode('hex')

	def __init__(self,url):
		self.url = url
		self.common = CommonLib.CommonLib(self.url)	
		
	def api_call_emptyfolder(self,**kargs):
		try:
			emptyFolderRes = self.common.request_send(RequestLib.folderempty, kargs)
		except Exception,e:
			if 'AUTHENTICATION_REQUIRED' in e.message:
				return 'AUTHENTICATION_REQUIRED' # both session and token expired, catch authentic error
			else:
				raise e
		if '<mail action="folderempty">' in emptyFolderRes and '<status>ok</status>' in emptyFolderRes:
			domain = re.findall('http://(.*):', kargs['host'])[0]
			originToken = self.common.session.cookies._cookies[domain]['/']['webtoptoken'].value
			token = self.__decrypt(originToken)
			origin_expired_time = re.findall(',([0-9]+),', token)[0]
			return self.common.session.cookies._cookies[domain]['/']['webtopsessionid'].value + ' | ' + origin_expired_time
		else:
			raise Exception('Failed to empty trash folder') 
		
	def make_expired_token(self,**kargs):
		domain = re.findall('http://(.*):', kargs['host'])[0]
		#find original token
		originToken = self.common.session.cookies._cookies[domain]['/']['webtoptoken'].value
		token = self.__decrypt(originToken)
		origin_expired_time = re.findall(',([0-9]+),', token)[0]
		expiry = kargs['expiry']
		#mock token time expired
		moke_expired_time = int(origin_expired_time) - int(expiry)*60*60*1000
		#make a new encrypted token
		newtoken, number = re.subn(',[0-9]+,', ',' + str(moke_expired_time) + ',', token)
		self.common.session.cookies._cookies[domain]['/']['webtoptoken'].value = self.__encrypt(newtoken)
		#print self.common.session.cookies._cookies
		
	def make_expired_session(self,**kargs):
		domain = re.findall('http://(.*):', kargs['host'])[0]
		self.common.session.cookies._cookies[domain]['/']['webtopsessionid'].value = 'invalidsession'
	