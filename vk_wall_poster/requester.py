# -*- coding: utf-8 -*-
__author__ = "spi4kavg"
import os
import requests


class VKRequester(object):
	"""
		class-wrapper for wall-post api
	"""

	# domain name of api
	domain = "https://api.vk.com/method"
	
	def __init__(self, vk_owner_id, vk_access_token):
		"""
			VKRequester contructor
			args:
				vk_owner_id (str) owner id
				vk_access_token (str) access_token
		"""
		self.__vk_owner_id = vk_owner_id
		self.__vk_access_token = vk_access_token
	
	def getWallUploadServer(self):
		url = self._get_url("photos.getWallUploadServer")
		r = requests.post(url, params={
			'group_id': self.__vk_owner_id,
			'access_token': self.__vk_access_token
		})

		return self._get_response(r).get('upload_url')
	
	def wallPost(self, text, attachments, into_group=False):
		url = self._get_url("wall.post")

		r = requests.post(url, params={
			'message': text,
			'owner_id': ('-' if into_group else '') + self.__vk_owner_id,
			'access_token': self.__vk_access_token,
			'from_group': '1' if into_group else '0',
			'attachment': ','.join(attachments)
		})
		
		return self._get_response(r).get('post_id')
	
	def saveWallPhoto(self, srvr, photo, hash):
		url = self._get_url('photos.saveWallPhoto')
		r = requests.post(url, params={
			'server': srvr,
			'photo': photo,
			'hash': hash,
			'group_id': self.__vk_owner_id,
			'access_token': self.__vk_access_token
		})
		
		response = self._get_response(r)
		
		return response[0].get('id') if len(response) else None
	
	def uploadPhotoIntoServer(self, srvr, img):
		r = requests.post(srvr, files={
			'photo': open(img, mode='rb')
		}, params={
			'access_token': self.__vk_access_token
		}).json()
		return r.get('server'), r.get('photo'), r.get('hash')
	
	def _get_url(self, method):
		return os.path.join(self.domain, method)
	
	def _get_response(self, r):
		json = r.json()
		return json.get('response', {})