from random import randrange
from time import time


class Game:
    def __init__(self, files_count):
        self.files = []
        for i in range(files_count):
            self.files.append(File(i))
        self.total_chunks = self.calculate_total_chunks()

    def calculate_total_chunks(self):
        counter = 0
        for file in self.files:
            counter = counter + len(file.chunks)
        return counter

    def get_remaining_chunks_count(self):
        counter = 0
        for file in self.files:
            for chunk in file.chunks:
                if not chunk.is_complete():
                    counter = counter + 1
        return counter

    def get_first_incomplete_chunk(self):
        for file in self.files:
            for chunk in file.chunks:
                if not chunk.started:
                    chunk.started = True
                    chunk.started_time = time()
                    return chunk


class File:
    def __init__(self, id):
        self.chunks = []
        self.id = id
        for i in range(10, randrange(11, 20)):
            self.chunks.append(FileChunk(self.id, i))


class FileChunk:
    def __init__(self, file_id, id):
        self.bytes_size = randrange(1, 10) * 1024 * 1024
        self.bytes_downloaded = 0
        self.id = str(file_id) + '-' + str(id)
        self.started = False
        self.started_time = 0
        self.finished_time = 0
        self.restart_counter = 0

    def is_complete(self):
        if self.bytes_downloaded >= self.bytes_size:
            return True

    def get_bytes_remaining(self):
        return self.bytes_size - self.bytes_downloaded

    def get_percantage_progress(self):
        return round(self.bytes_downloaded/self.bytes_size*100)

    def update_bytes_downloaded(self, bytes):
        self.bytes_downloaded = self.bytes_downloaded + bytes
        if self.is_complete():
            self.finished_time = time()

    def get_current_download_time(self):
        return time() - self.started_time

    def restart(self):
        self.bytes_downloaded = 0
        self.started = False
        self.started_time = 0
        self.finished_time = 0
        self.restart_counter = self.restart_counter + 1
