# edit message data as you see fit
class RestrictedMessage:
	class _channel:
		def __init__(self) -> None:
			self.id:int = 13241234
			self.name:str = 'channel name'

	class _guild:
		def __init__(self) -> None:
			self.id:int = 13241234
			self.name:str = 'guild name'

	class _user:
		def __init__(self) -> None:
			self.id:int = 13241234
			self.name:str = 'author name'
			self.display_name:str = 'author display name'

	def __init__(self,**kwargs):
		self.id:int = 13241234
		self.channel = self._channel()
		self.guild = self._guild()
		self.author = self._user()
		self.timestamp:float = 1620198608
		self.content:str = 'wow, this is an example message, you can change it in RestrictedMessage.py!'