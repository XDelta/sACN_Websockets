from os.path import dirname, join

import toml

from Logging import wssl
import __meta__ as meta

configSpec = 2

class Config(object):

	def __init__(self):
		self.app_dir = dirname(__file__)
		self.version = meta.version

	def setValDefault(self, val, default): #set a default in case the value is missing in the config
		if(val in (None, "")):
			return default
		return val

	def setConfigFile(self, configFile):
		tomlData = toml.load(open(join(self.app_dir, 'config', configFile)))

		self.ws_uri = self.setValDefault(tomlData.get('destination').get('ws_uri'), "ws://localhost")
		self.locally_host = self.setValDefault(tomlData.get('destination').get('locally_host'), True)
		self.local_port = self.setValDefault(tomlData.get('destination').get('local_port'), 80)

		self.sACN_port = self.setValDefault(tomlData.get('dmx').get('sACN_port'), 5568)
		self.sACN_ip = self.setValDefault(tomlData.get('dmx').get('sACN_ip'), "127.0.0.1")
		self.dmx_fps = self.setValDefault(tomlData.get('dmx').get('dmx_fps'), 10)
		self.sACN_universe = self.setValDefault(tomlData.get('dmx').get('sACN_universe'), 1)

		self.getSpec = tomlData.get('debug').get('configSpec')
		if(self.getSpec != configSpec):
			wssl.log("ConfigSpec in "+configFile+" doesn't match this version, your config may be out of date")

config = Config()
