import asyncio, sys, socket, traceback

import websockets
import sacn, requests
from packaging.version import parse as parse_version

from Config import config
from Logging import wssl

try:
	config.setConfigFile('config.toml')
except Exception:
	wssl.log(traceback.format_exc())
	wssl.log("Error opening config")
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
except Exception:
	wssl.log(traceback.format_exc())
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
	wssl.log("Exited local server")

async def remoteSender(): #connect to external ws server
	while True:
		wssl.log(("Connecting to {0}").format(config.ws_uri))
		async with websockets.connect(config.ws_uri) as websocket:
			await dmxSender(websocket)
			wssl.log("Lost connection to remote host")

async def dmxSender(websocket):
	running = True
	global hasDataToSend
	dmx_fps = config.dmx_fps

	while running:
		if hasDataToSend:
			try:
				data = lastDMX()
				hasDataToSend = False
				await websocket.send(data)
				await asyncio.sleep(1/dmx_fps)
			except Exception:
				wssl.log(traceback.format_exc())
				wssl.log("Failed on send")
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

except KeyboardInterrupt:
	wssl.log("Closed by console interrupt")
except socket.gaierror:
	#should no longer be reachable
	wssl.log(traceback.format_exc())
	wssl.log("Unable to connect to websocket host, likely invalid name")
except Exception:
	wssl.log(traceback.format_exc())

receiver.stop()
