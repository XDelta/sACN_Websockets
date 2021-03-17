# sACN_Websockets
Send DMX using sACN over websockets, created for use in virtual lighting rigs.

## Prerequisite
Python 3.8+
A Websocket Server, any server that accepts websockets and will then distribute it to connected clients. 
I've used [Pie Socket](https://www.piesocket.com/) for testing

## Install
Download the [Latest Release](https://github.com/XDelta/sACN_Websockets/releases/latest/).<br>
Install the requirements with
```bash
pip install -r requirements.txt
```
Edit `config.toml` with your Websocket host and network settings

## Usage
Run `sACN_Websockets.py`<br>

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
