# Coral Dev Board

## Requirements

* Coral dev board
* A Linux host
* 2 USB-C to USB cables

## Setup

1. Follow the instructions to [Execute the flash script](https://coral.ai/docs/dev-board/reflash/#execute-flash)
2. Follow the instructions to [Install MDT](https://coral.ai/docs/dev-board/get-started/#install-mdt) on your Linux host
3. Execute `mdt devices` to list the connected dev boards
4. Execute `mdt shell` to log in to the connected dev board
5. Once logged into the dev board, use `ip a` to list the available network interfaces
   - You should be connected via `usb0`, note the `link/ether` address for the MAC address so you can identify the board
   - The IP address is randomly chosen and may be different the next time you connect to the board
