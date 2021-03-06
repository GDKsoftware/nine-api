# NINE Communication API

## What is it

This project provides definitions and a Python client module to send messages between a client and a server using [Protobuf](https://developers.google.com/protocol-buffers/docs/proto3) over UDP.

## Prerequisites

Follow the instructions [here](https://github.com/GDKsoftware/nine-api/blob/main/coral_devboard.md) - on how to setup the Dev Board.

## How does it work

An example on how to use `nine_client.py` can be found in `test_client.py`

1. The client first sends a UDP broadcast message to the server
   - It's assumed the network is `192.168.100.0` and is connected via network interface `usb0`
   - If needed you can change these defaults
2. The server sends a response back so that the client knowns at which IP address the server resides
3. The client can now send other messages to the server

## When updating definitions

If you change `definitions/nine.proto`, you will need to generate the matching python modules (`libnine/nine_pb2.py`) - at the same time it will also generate C++ files in `libcpp`.

You can generate the files by running `make lib` on a Linux machine.

## Testing

* Run `make server` or `python3 test_server.py` to launch a test server, this will respond to basic discovery and other messages

### Notes when testing

* You're not able to use the python environment or caches from the Linux host on the dev board - so you cannot just `mdt push` the host files to the dev board
* To copy the files, follow these steps:
  1. host: `make clean`
  2. host: `mdt push . test`
  3. host: `mdt shell` - to login to the board
  4. board: `cd test`
  5. board: Connect an Ethernet cable to allow for Internet access
  6. board: `make .env/.done`
  7. board: Disconnect Ethernet cable
  8. board: `make client`
* Note: if you connect the Ethernet cable before running mdt shell, you might be connected through the wrong IP, so remove it first so the communication goes through the USB cable
