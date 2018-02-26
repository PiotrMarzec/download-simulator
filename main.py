import game
import cdn
import downloader
import screen
import optimize

game = game.Game(20)
connection = downloader.InternetConnection(1000 * 1024)

cdn_list = cdn.CdnList()
cdn_list.add_cdn(cdn.Cdn(connection.speed * 0.8, "fast"))
cdn_list.add_cdn(cdn.Cdn(connection.speed * 0.5, "normal"))
cdn_list.add_cdn(cdn.Cdn(connection.speed * 0.2, "slow"))
cdn_list.add_cdn(cdn.Cdn(connection.speed * 0.01, "glacier"))

downloader = downloader.Downloader(cdn_list, connection, game, 10)
downloader.mean_chunk_download_time_optimizer = optimize.MeanChunkDownloadTimeOptimizer()

screen = screen.Screen(downloader)
screen.start()

while game.get_remaining_chunks_count():
    bytes = downloader.tick()

    screen.tick(bytes)
    # time.sleep(0.001)

screen.finish()