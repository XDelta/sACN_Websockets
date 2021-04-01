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

## Usage
Run `sACN_Websockets.py`<br>
The default configuration will host a websocket server available at `ws://localhost:80/` and listen for sACN Universe 1 on `127.0.0.1:5568`


[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
