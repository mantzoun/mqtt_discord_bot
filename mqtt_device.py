import time

class Device:
    name = "Unnamed"
    status = "off"
    user_on = None
    user_off = None
    on_time = 0
    off_time = 0
    msg = None

    def set_on(self, user):
        self.status = "on"
        self.user_on = user
        self.on_time = time.time()

    def set_off(self, user):
        self.status = "off"
        self.user_off = user
        self.off_time = time.time()

    def get_last_on_duration(self):
        return (self.off_time - self.on_time)/60

    def get_name(self):
        return self.name

    def set_msg(self, msg):
        self.msg = msg

    def get_msg(self):
        return self.msg

    def __init__(self, name):
        self.name = name
