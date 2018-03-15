from random import randrange
from random import shuffle


class InternetConnection:
    def __init__(self, speed):
        self.speed = speed


class Downloader:
    def __init__(self, cdn_list, internet_connection, game, threads_count):
        self.cdn_list = cdn_list
        self.connection = internet_connection
        self.game = game
        self.threads = []
        self.ticks = 0
        self.total_progress = 0

        self.optimizer = None

        for i in range(0, threads_count):
            self.threads.append(Thread(i))

    def tick(self):
        max_bytes = self.get_tick_max_bytes()
        bytes = 0
        current_threads = 0

        shuffle(self.threads)

        # tick existing threads
        for thread in self.threads:
            if thread.is_empty():
                thread.chunk = self.get_next_chunk()
                thread.cdn = self.get_cdn()

            if thread.is_complete():
                self.on_chunk_complete(thread.chunk)
                thread.chunk = self.get_next_chunk()
                thread.cdn = self.get_cdn()

            thread_bytes = thread.tick(max_bytes) # tick thread

            max_bytes -= thread_bytes # decrease remaining bytes in tick
            bytes += thread_bytes # total bytes in tick
            current_threads += 1

        self.ticks += 1
        self.total_progress = round(
            100 -
            self.game.get_remaining_chunks_count() /
            self.game.calculate_total_chunks() * 100
        )

        if self.optimizer:
            self.optimizer.tick(self)

        return bytes

    def get_tick_max_bytes(self):
        return round((randrange(70, 100) / 100) * self.connection.speed)

    def get_next_chunk(self):
        return self.game.get_first_incomplete_chunk()

    def get_cdn(self):
        return self.cdn_list.get_random()

    def on_chunk_complete(self, chunk):

        if self.optimizer:
            self.optimizer.on_chunk_complete(self, chunk)


class Thread:
    def __init__(self, id):
        self.chunk = None
        self.cdn = None
        self.id = id

    def tick(self, max_bytes):
        if self.is_empty():
            return 0

        bytes_downloaded = round((randrange(20, 100)/100) * self.cdn.speed)

        # we can't download more than remaining bytes in the given tick
        if bytes_downloaded > max_bytes:
            bytes_downloaded = max_bytes

        # we can't download more then remaining bytes in the chunk
        if bytes_downloaded > self.chunk.get_bytes_remaining():
            bytes_downloaded = self.chunk.get_bytes_remaining()

        # update chunk downloaded bytes
        self.chunk.update_bytes_downloaded(bytes_downloaded)

        return bytes_downloaded

    def get_current_download_time(self):
        return self.chunk.get_current_download_time()

    def restart(self):
        self.chunk.restart()
        self.chunk = None
        self.cdn = None

    def is_complete(self):
        if not self.chunk:
            return False

        return self.chunk.is_complete()

    def is_empty(self):
        return self.chunk == None

