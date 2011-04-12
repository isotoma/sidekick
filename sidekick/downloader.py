import sys
import urllib

from sidekick.progress import Progress

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
    d = Download("http://archive.ubuntu.com/ubuntu/pool/main/h/hello/hello_2.5.orig.tar.gz", "/home/john/hello.test")
    d.download()

