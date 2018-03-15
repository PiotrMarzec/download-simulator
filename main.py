import game
import cdn
import downloader
import screen
import optimize
import time

game = game.Game(100)   # Create a game with 100 files, each file will have 11-20 chunks
connection = downloader.InternetConnection(1000 * 1024)  # Create an internet connection in bytes per second

cdn_list = cdn.CdnList()
cdn_list.add_cdn(cdn.Cdn(connection.speed * 0.8, "fast"))       # Fast CDN, with max speed of 80% of our connection
cdn_list.add_cdn(cdn.Cdn(connection.speed * 0.5, "normal"))     # Normal CDN, with max speed of 50% of our connection
cdn_list.add_cdn(cdn.Cdn(connection.speed * 0.2, "slow"))       # Slow CDN, with max speed of 20% of our connection
cdn_list.add_cdn(cdn.Cdn(connection.speed * 0.01, "glacier"))   # Glacier CDN, with max speed of 1% of our connection

downloader = downloader.Downloader(cdn_list, connection, game, 35)      # create downloader
downloader.optimizer = optimize.NaiveMeanChunkDownloadTimeOptimizer()   # add optimizer

screen = screen.Screen(downloader)
screen.start()  # start screen timer

while game.get_remaining_chunks_count():
    bytes = downloader.tick()

    screen.tick(bytes)
    # time.sleep(0.001) # sleep for better presentation

screen.finish()  # print summary
