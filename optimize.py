class MeanChunkDownloadTimeOptimizer:
    def __init__(self):
        self.chunk_mean_time = 0
        self.chunk_counter = 0
        self.chunk_time_sum = 0

    def on_chunk_complete(self, chunk):
        chunk_time = chunk.finished_time - chunk.started_time
        self.chunk_counter = self.chunk_counter + 1
        self.chunk_time_sum = self.chunk_time_sum + chunk_time
        self.chunk_mean_time = self.chunk_time_sum / self.chunk_counter

    def tick(self, downloader):
        for thread in downloader.threads:
            if thread.is_empty():
                self.optimize(downloader)
                return

    def optimize(self, downloader):
        for thread in downloader.threads:
            if not thread.is_empty() and thread.chunk.get_current_download_time() > self.chunk_mean_time:
                # make sure to not remove the last CDN
                if downloader.cdn_list.get_count() > 1:
                    downloader.cdn_list.remove(thread.cdn)

                # restart each chunk only once
                if thread.chunk.restart_counter == 0:
                    thread.restart()
