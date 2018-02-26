class NaiveMeanChunkDownloadTimeOptimizer:
    """
    Calculate mean chunk download time across all CDNs during download.

    When we reach the end of the download (first empty thread) start removing CDNs below
    the mean chunk download time. Also make sure not to remove all CDNs
    """

    def __init__(self):
        self.name = 'MeanChunkDownloadTimeOptimizer'
        self.chunk_mean_time = 0
        self.chunk_counter = 0
        self.chunk_time_sum = 0

    def on_chunk_complete(self, downloader, chunk):
        chunk_time = chunk.get_total_download_time()
        self.chunk_counter += 1
        self.chunk_time_sum += chunk_time
        self.chunk_mean_time = self.chunk_time_sum / self.chunk_counter

    def tick(self, downloader):
        for thread in downloader.threads:
            # if we have an empty thread start optimizing
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

    def draw(self, downloader, bytes):
        print('Mean Chunk Download Time: {}'.format(
            self.chunk_mean_time
        ))


class NaiveLiveCdnRatioByMeanChunkTime:
    """
    Calculate the mean chunk download time for each CDN separately.

    Once any CDN reaches some arbitrary limit (5 chunks completed) start adjusting the CDN ratios
    """

    def __init__(self):
        self.name = 'LiveCdnRatioByMeanChunkTime'

    def tick(self, downloader):
        chunk_counter = get_max_cdn_chunk_count(downloader.cdn_list.list)

        if chunk_counter > 10:
            self.optimize(downloader)

    def on_chunk_complete(self, downloader, chunk):
        cdn = find_cdn_by_chunk(downloader, chunk)
        cdn.chunk_counter += 1
        cdn.chunk_time_sum += chunk.get_total_download_time()
        cdn.chunk_mean_time = round(cdn.chunk_time_sum / cdn.chunk_counter, 5)

    def optimize(self, downloader):
        for cdn in downloader.cdn_list.list:
            if cdn.chunk_counter == 0:
                cdn.ratio = 0
            else:
                cdn.ratio = 100 - round(
                    cdn.chunk_mean_time / sum_cdn_mean_times(downloader.cdn_list.list) * 100
                )
        pass

    def draw(self, downloader, bytes):
        for cdn in downloader.cdn_list.list:
            print(
                "{:7} mean_chunk_time:{:<9} chunk_count:{:<4} ratio:{:<7}".format(
                    cdn.name,
                    cdn.chunk_mean_time,
                    cdn.chunk_counter,
                    cdn.ratio
                )
            )


def find_cdn_by_chunk(downloader, chunk):
    for thread in downloader.threads:
        if thread.chunk == chunk:
            return thread.cdn


def get_min_cdn_chunk_count(cdn_list):
    min = None
    for cdn in cdn_list:
        if not min:
            min = cdn.chunk_counter
        elif cdn.chunk_counter < min:
            min = cdn.chunk_counter
    return min


def get_max_cdn_chunk_count(cdn_list):
    max = 0
    for cdn in cdn_list:
        if cdn.chunk_counter > max:
            max = cdn.chunk_counter
    return max


def sum_cdn_mean_times(cdn_list):
    sum = 0
    for cdn in cdn_list:
        sum += cdn.chunk_mean_time
    return sum
