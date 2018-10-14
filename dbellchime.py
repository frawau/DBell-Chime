#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Simple Python program that can be used to react to DBell Live alarms and
# play a sound file.
#
# Copyright (c) 2018 François Wautier
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies
# or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR
# IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE

#Set things here
RING = "/home/myhome/sound/ring.ogg"   # The sound file you want to play
BELLADDR = "192.168.1.100"             # The IP address of the DBell Live
MYADDR = "0.0.0.0"                     # The IP address of the machine on which
                                       # this runs. If unsure use 0.0.0.0
PORT = 8181
DELAY = 45 #secs
CMD = "ogg123 \"%s\""%RING
#No serviceable parts below

import datetime as dt
import asyncio

nexttime = dt.datetime.now()

async def handle_connection(reader, writer):
    global nexttime
    thistime = dt.datetime.now()
    address = writer.get_extra_info('peername')
    if thistime > nexttime and address[0] == BELLADDR:
        nexttime = thistime + dt.timedelta(seconds=DELAY)
        writer.write(b'220 DBell Python SMTP 1.1\r\n')
        await writer.drain()
        data = await reader.read(1024)
        writer.write(b'221 Goodbye')
        await writer.drain()
        writer.close()
        process = await asyncio.create_subprocess_shell(
            CMD,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE)
        stdout, stderr = await process.communicate()
    else:
        #print("Go away")
        writer.close()

loop = asyncio.get_event_loop()
coro = asyncio.start_server(handle_connection, MYADDR, PORT, loop=loop)
server = loop.run_until_complete(coro)

# Serve requests until Ctrl+C is pressed
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

# Close the server
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()
