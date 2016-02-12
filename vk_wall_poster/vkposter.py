# -*- coding: utf8 -*-
__author__ = "spi4kavg"
import os
import re
import requests
from PIL import Image
from cStringIO import StringIO
from requester import VKRequester


class VKPoster(object):
	"""
		class for send wall posts for vk
	"""
	domain = "https://api.vk.com/method"
	
	def __init__(self, requester):
		"""
			VKPoster constructor
			args:
				requester (VKRequester) VKRequester object
		"""
		self.req = requester

	def post(self, post, into_group=False):
		"""
			VKPoster method to send message
			args:
				post (dict) dictionary with data
					example:
						{
							'images': ['http://example.com/static/qwe.jpg', /home/user/1.png],
							'link': 'http://example.com/some-page.html',
							'text': 'hello world'
						}
				into_group (Boolean) if publicate post in group set True else False
		"""
		compiled_attachments = []
		if post.get('images'):
			srvr = self.req.getWallUploadServer()
			for image in post.get('images'):
				photo = self._upload_wall_photo(srvr, image)
				compiled_attachments.append(photo)
		if post.get('link'):
			compiled_attachments.append(post.get('link'))

		r = self.req.wallPost(
			post.get('text'),
			compiled_attachments,
			into_group=into_group
		)
		
		return r
	
	def _upload_wall_photo(self, srvr, img):
		"""
			VKPoster method that provides to uploading image
		"""
		if self._is_url(img):
			photo = requests.get(img).content
			image = Image.open(StringIO(photo))
			image.save(os.path.basename(img))
			image = os.path.basename(img)
		
		s, p, h = self.req.uploadPhotoIntoServer(srvr, image)

		if self._is_url(img):
			os.remove(os.path.basename(img))
		
		return self.req.saveWallPhoto(s, p, h)
	
	def _is_url(self, img):
		""" Checks if path is url """
		return bool(re.compile("http\:\/\/|www\.|https\:\/\/").match(img))
