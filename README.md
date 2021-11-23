# sACN_Websockets
Send DMX using sACN over websockets, created for use in virtual lighting rigs.

## Prerequisite
* Python 3.8+
* A Websocket Relay Server
* Any lighting software that supports sACN

By default, a websocket server will be run locally at `ws://localhost:80/` but you can use any server that accepts websockets and can then distribute it to connected clients.<br>
I've tested with [Pie Socket](https://www.piesocket.com/) as a websocket relay server and it requires very little to get running.

## Install
Download the [Latest Release](https://github.com/XDelta/sACN_Websockets/releases/latest/).<br>
Install the requirements with
```bash
pip install -r requirements.txt
```
Edit `config.toml` with your Websocket host and network settings

## Config

### [destination]
`ws_uri = "ws://localhost"`<br>
Websocket relay host, by default, this will attempt to connect to a locally hosted websocket server.
<br>

`locally_host = true`<br>
Hosts a websocket relay server on localhost when set to 'true', will need to be changed to 'false' if you want to use a different/external relay server.
<br>

`local_port = 80`<br>
Websocket port when hosting locally. Ignored when locally host is set to false.
<br>

### [dmx]
`sACN_port = 5568`<br>
Port for sACN, shouldn't need to be changed
<br>

`sACN_ip = "127.0.0.1"`<br>
IP address to listen for sACN on, in this case it is the local device. Depending on the lighting software you use, you may need to enable sending sACN to Applications on the same device. In MagicQ, this is in Setup>Network.<br>
![settings image in magicq](https://user-images.githubusercontent.com/7883807/142968817-314039d3-89af-43f8-a940-47fe17f4e953.png)
<br>

`sACN_universe = 1`<br>
sACN universe to listen to, most small setups won't need to be change this. If you need to send multiple universes, multiple copies of the application can be used but you will need to have separate config files made.
<br>

`dmx_fps = 10`<br>
DMX Sending rate can be anything between 1 and 48, this defines the maximum rate but if there isn't new DMX data to send, less packets will be sent to match.

## Usage
Run `sACN_Websockets.py`<br>
The default configuration will host a websocket server available at `ws://localhost:80/` and listen for sACN Universe 1 on `127.0.0.1:5568`


[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
