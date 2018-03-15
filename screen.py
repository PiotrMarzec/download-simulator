import time
import os
from operator import attrgetter


class Screen:
    def __init__(self, downloader):
        self.downloader = downloader
        self.timer = 0
        self.start_time = None
        self.finish_time = None

    def start(self):
        self.start_time = time.time()

    def finish(self):
        self.finish_time = time.time()
        print("TOTAL TICKS: {}".format(
            self.downloader.ticks
        ))

    def tick(self, bytes):
        t = time.time()

        if t - self.timer > 0.1:
            clear()
            self.draw(bytes)
            self.timer = time.time()

    def draw(self, bytes):
        threads = sorted(self.downloader.threads, key=attrgetter('id'))

        draw_threads(threads)
        draw_summary(self.downloader, bytes)

        if self.downloader.optimizer:
            print('----- OPTIMIZER: {} -----'.format(self.downloader.optimizer.name))
            self.downloader.optimizer.draw(self.downloader, bytes)


def clear():
    os.system('clear')


def get_percentage_bar(p):
    bar_length = 20
    bar = '['

    for i in range(bar_length):
        if i / bar_length > p / 100:
            bar = bar + " "
        else:
            bar = bar + "="

    bar = bar + ']'

    return bar


def draw_threads(threads):
    for thread in threads:

        if thread.chunk:
            print(
                "Thread#{:<2} chunk:{:<7} cdn:{:<10} bytes_remaining:{:<9} {}".format(
                    thread.id,
                    thread.chunk.id,
                    thread.cdn.name,
                    thread.chunk.get_bytes_remaining(),
                    get_percentage_bar(thread.chunk.get_percantage_progress())
                )
            )
        else:
            print(
                "Thread#{:<2} empty".format(
                    thread.id,
                )
            )


def draw_summary(downloader, bytes):
    print("Chunks remaining:{:<5} Speed:{:<5} ({:<2}%)".format(
        downloader.game.get_remaining_chunks_count(),
        bytes,
        round(bytes / downloader.connection.speed * 100)
    ))
