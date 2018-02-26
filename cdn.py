from random import randrange


class Cdn:
    def __init__(self, speed, name):
        self.speed = speed
        self.name = name
        self.ratio = 1
        self.chunk_counter = 0
        self.chunk_time_sum = 0
        self.chunk_mean_time = 0


class CdnList:
    def __init__(self):
        self.list = []

    def add_cdn(self, cdn):
        self.list.append(cdn)

    def get_random(self):
        i = randrange(0, sum_ratios(self.list))
        cdn = get_by_ratio(self.list, i)

        return cdn

    def remove(self, cdn):
        if cdn in self.list:
            self.list.remove(cdn)

    def get_count(self):
        return len(self.list)


def sum_ratios(list):
    sum = 0
    for cdn in list:
        sum += cdn.ratio

    return sum


def get_by_ratio(list, random):
    sum = 0
    for cdn in list:
        sum += cdn.ratio
        if sum > random:
            return cdn
