import os, os.path
import time
import asyncio

class myIO:
    my_io           = None
    cb_func         = None
    max_pkt_size    = -1
    read_thread     = None

    def __init__(self, io_path, cb, s = 1024):
        self.cb_func        = cb
        self.max_pkt_size   = s

        if os.path.exists(io_path):
            os.remove(io_path)

        os.mkfifo(io_path, 0o666)

        self.my_io = io_path

    async def read_loop(self):
        io = os.open(self.my_io, os.O_RDONLY | os.O_NONBLOCK)
        while True:
            data = os.read(io,1024)
            if data:
                await self.cb_func(data.decode('utf-8'))
            await asyncio.sleep(1)

    async def receive(self):
        await self.read_loop()
