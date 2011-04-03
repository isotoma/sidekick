import os
import sys
import urllib


class Progress(object):

    self.bar_size = 75

    def __init__(self, upperbound):
        self.upperbound = upperbound
        self.pos = 0

    def progress(self, progress):
        pos = min((progress * self.bar_size) /self.upperbound, self.bar_size)
        if pos != self.pos:
            self.pos = pos
            self.draw()

    def draw(self):
        sys.stdout.write("[%s%s]\r" % ("=" * self.pos, " " * (self.upperbound-self.pos)))
        sys.stdout.flush()

    def finish(self):
        sys.stdout.write("\n")
        sys.stdout.flush()


class Download(object):

    def __init__(self, url, destination):
        self.url = url
        self.destination = destination

    def feedback(self, numblocks, blocksize, totalsize):
        if not self.pb:
            self.pb = Progress(totalsize)

        self.pb.progress(numblocks * blocksize)

    def download(self):
        cb = None
        if sys.stdout.isatty():
            cb = self.feedback

        urllib.urlretrieve(self.url, self.destination, cb)


