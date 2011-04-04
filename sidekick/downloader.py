import os
import sys
import urllib


class Progress(object):

    bar_size = 75

    def __init__(self, upperbound):
        self.upperbound = upperbound
        self.scale = float(self.bar_size) / upperbound
        self.pos = -1

    def progress(self, progress):
        pos = int(min(progress * self.scale, self.bar_size))
        if pos != self.pos:
            self.pos = pos
            self.draw()

    def draw(self):
        sys.stdout.write("[%s%s]\r" % ("=" * self.pos, " " * (self.bar_size-self.pos)))
        sys.stdout.flush()

    def finish(self):
        sys.stdout.write("\n")
        sys.stdout.flush()


class Download(object):

    def __init__(self, url, destination):
        self.url = url
        self.destination = destination
        self.pb = None

    def feedback(self, numblocks, blocksize, totalsize):
        if not self.pb:
            self.pb = Progress(totalsize)

        self.pb.progress(numblocks * blocksize)

    def download(self):
        cb = None
        if sys.stdout.isatty():
            cb = self.feedback

        urllib.urlretrieve(self.url, self.destination, cb)
        self.pb.finish()

if __name__ == "__main__":
    import time
    #p = Progress(50)
    #i = 0
    #while i <= 50:
    #    p.progress(i)
    #    time.sleep(1)
    #    i = i+2
    #p.finish()

    d = Download("http://archive.ubuntu.com/ubuntu/pool/main/h/hello/hello_2.5.orig.tar.gz", "/home/john/hello.test")
    d.download()

