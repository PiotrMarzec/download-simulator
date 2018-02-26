from random import randrange


class Cdn:
    def __init__(self, speed, name):
        self.speed = speed
        self.name = name


class CdnList:
    def __init__(self):
        self.list = []

    def add_cdn(self, cdn):
        self.list.append(cdn)

    def get_random(self):
        i = randrange(0, len(self.list))
        return self.list[i];

    def remove(self, cdn):
        if cdn in self.list:
            self.list.remove(cdn)

    def get_count(self):
        return len(self.list)
