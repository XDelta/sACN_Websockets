import asyncio, sys, socket

import websockets
import sacn, requests
from packaging.version import parse as parse_version

from Config import config
from Logging import wssl

try:
	config.setConfigFile('config.toml')
except Exception as e:
	wssl.log("Error opening config")
	wssl.log(str(e))
	sys.exit()

# update check
try:
	response = requests.get("https://api.github.com/repos/XDelta/sACN_Websockets/releases/latest")
	cver = parse_version(config.version)
	rver = parse_version(response.json()["name"])

	if rver > cver:
		wssl.log("New version available [" + str(rver) + "], Current [" + str(cver) +"]")
	elif rver < cver:
		wssl.log("Ahead of Remote [" + str(rver) + "], Current [" + str(cver) +"]")
	else:
		wssl.log("Up to date [" + str(rver) + "]")
except Exception as e:
	wssl.log(str(sys.exc_info()))
	wssl.log("Unable to check for update")

hasDataToSend = True
LastPacket = tuple(0 for _ in range(512))
receiver = sacn.sACNreceiver(config.sACN_ip, config.sACN_port)
receiver.start()

def lastDMX():
	pre = ''.join(format(x, '02x') for x in LastPacket)
	return pre

async def localServer(websocket, path):
	await dmxSender(websocket)

async def remoteSender(): #connect to external ws server
	async with websockets.connect(config.ws_uri) as websocket:
		await dmxSender(websocket)

async def dmxSender(websocket):
	running = True
	global hasDataToSend
	dmx_fps = config.dmx_fps

	while running:
		if hasDataToSend:
			try:
				data = lastDMX()
				await websocket.send(data)
				hasDataToSend = False
				await asyncio.sleep(1/dmx_fps)
			except Exception as e:
				wssl.log(str(e))
				running = False
		else:
			await asyncio.sleep(1/dmx_fps)

@receiver.listen_on('universe', universe=config.sACN_universe)
def callback(packet):
	global LastPacket
	global hasDataToSend
	LastPacket = packet.dmxData
	hasDataToSend = True

wssl.log(("Listening on {0}:{1}").format(config.sACN_ip, config.sACN_port))
receiver.join_multicast(config.sACN_universe)

try:
	if config.locally_host:
		start_server = websockets.serve(localServer, "localhost", config.local_port)
		asyncio.get_event_loop().run_until_complete(start_server)
		wssl.log(("Sending locally on ws://localhost:{0}").format(config.local_port))
		asyncio.get_event_loop().run_forever()
	else:
		wssl.log(("Sending on {0}").format(config.ws_uri))
		asyncio.get_event_loop().run_until_complete(remoteSender())

except KeyboardInterrupt as e:
	wssl.log("Closed by console interrupt")
except socket.gaierror as e:
	wssl.log("Unable to connect to websocket host")
	wssl.log(str(sys.exc_info()))
except Exception as e:
	wssl.log(str(sys.exc_info()))
	wssl.log(str(e))

receiver.stop()
