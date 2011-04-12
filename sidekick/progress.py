import sys


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


if __name__ == "__main__":
    import time
    p = Progress(50)
    i = 0
    while i <= 50:
        p.progress(i)
        time.sleep(1)
        i = i+2
    p.finish()

