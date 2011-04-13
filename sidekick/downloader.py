# Copyright 2011 Isotoma Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


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

