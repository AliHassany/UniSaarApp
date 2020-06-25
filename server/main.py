from source.networking.UniAppServer import UniAppServer
from source.networking.RequestHandler import RequestHandler
from source.networking.NetworkManager import NetworkManager
import threading
from source.Constants import MENSA_UPDATE_THRESHOLD, MAP_UPDATE_THRESHOLD, NEWSFEED_UPDATE_THRESHOLD, \
    HELPFUL_NUMBERS_THRESHOLD, SERVER_ADDRESS, SERVER_PORT, ERROR_SLEEP_INT
import time
import argparse


def reportError(e, loc):
    pass

class UpdateMensaThread(threading.Thread):
    def __init__(self, server: UniAppServer, verbose: bool):
        threading.Thread.__init__(self)
        self.server = server
        self.verbose = verbose

    def run(self):
        while True:
            try:
                self.server.updateMensa()
            except Exception as e:
                reportError(e, "mensa")
                time.sleep(ERROR_SLEEP_INT)
                continue
            if self.verbose:
                print('updated mensa')
            time.sleep(MENSA_UPDATE_THRESHOLD.total_seconds())


class UpdateNewsFeedThread(threading.Thread):
    def __init__(self, server: UniAppServer, verbose: bool):
        threading.Thread.__init__(self)
        self.server = server
        self.verbose = verbose

    def run(self):
        while True:
            try:
                self.server.updateNewsFeed()
            except Exception as e:
                reportError(e, "newsfeed")
                time.sleep(ERROR_SLEEP_INT)
                continue
            if self.verbose:
                print('updated newsfeed')
            time.sleep(NEWSFEED_UPDATE_THRESHOLD.total_seconds())


class UpdateMapThread(threading.Thread):
    def __init__(self, server: UniAppServer, verbose: bool):
        threading.Thread.__init__(self)
        self.server = server
        self.verbose = verbose

    def run(self):
        while True:
            try:
                self.server.updateMap()
            except Exception as e:
                reportError(e, "map")
                time.sleep(ERROR_SLEEP_INT)
                continue
            if self.verbose:
                print('updated map')
            time.sleep(MAP_UPDATE_THRESHOLD.total_seconds())


class UpdateHelpfulNumbersThread(threading.Thread):
    def __init__(self, server: UniAppServer, verbose: bool):
        threading.Thread.__init__(self)
        self.server = server
        self.verbose = verbose

    def run(self):
        while True:
            try:
                self.server.updateHelpfulNumbers()
            except Exception as e:
                reportError(e, "helpful numbers")
                time.sleep(ERROR_SLEEP_INT)
                continue
            if self.verbose:
                print('updated helpful numbers')
            time.sleep(HELPFUL_NUMBERS_THRESHOLD.total_seconds())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='UniSaarApp Server. '
                                                 'See the README on the Github for more information.')
    parser.add_argument('-v', '--verbose', action="store_true", help='Prints update messages.')
    args = parser.parse_args()

    nm = NetworkManager()
    server = UniAppServer((SERVER_ADDRESS, SERVER_PORT), RequestHandler, nm)
    mensaUpdateThread = UpdateMensaThread(server, args.verbose)
    newsFeedUpdateThread = UpdateNewsFeedThread(server, args.verbose)
    mapUpdateThread = UpdateMapThread(server, args.verbose)
    helpfulNumbersUpdateThread = UpdateHelpfulNumbersThread(server, args.verbose)
    mensaUpdateThread.start()
    newsFeedUpdateThread.start()
    mapUpdateThread.start()
    helpfulNumbersUpdateThread.start()
    server.serve_forever()
