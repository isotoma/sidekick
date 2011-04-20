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

import os, hashlib, zipfile, tarfile

import magic

from sidekick.downloader import Download

class ImageRegistry(object):

    download_dir = os.path.join(os.environ.get('XDG_CACHE_HOME', os.path.expanduser('~/.cache/')), "sidekick", "downloads")
    image_dir = os.path.join(os.environ.get('XDG_DATA_HOME', os.path.expanduser('~/.local/share')), "sidekick", "base_images")

    def __init__(self):
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)
        if not os.path.exists(self.image_dir):
            os.makedirs(self.image_dir)

    def download_image(self, uri):
        new_uri = os.path.join(self.download_dir, hashlib.sha1(uri).hexdigest())
        print new_uri

        if not os.path.exists(new_uri):
            d = Download(uri, new_uri)
            d.download()

        return new_uri

    def unpack_image(self, unpacker, uri):
        new_uri = os.path.join(self.image_dir, os.path.basename(uri))
        print new_uri

        if not os.path.exists(new_uri):
            os.makedirs(new_uri)

        if len(os.listdir(new_uri)) == 0:
            unpacker.extractall(new_uri)

        # If the unpacked folder just contains a single folder then return *that* fodler
        contents = os.listdir(new_uri)
        if len(contents) == 1 and os.path.isdir(os.path.join(new_uri, contents[0])):
            new_uri = os.path.join(new_uri, contents[0])

        return new_uri

    def unpack_tarred_image(self, uri):
        return self.unpack_image(tarfile.open(uri), uri)

    def unpack_zipped_image(self, uri):
        return self.unpack_image(zipfile.open(uri), uri)

    def get_image(self, uri):
        if uri.startswith("http://") or uri.startswith("https://"):
            uri = self.download_image(uri)

            ms = magic.open(magic.MAGIC_MIME)
            ms.load()
            mtype = ms.file(uri)

            if mtype.startswith("application/zip"):
                uri = self.unpack_zipped_image(uri)
            elif mtype.startswith("application/x-bzip2") or mtype.startswith("application/x-gzip") or mtype.startswith("application/x-tar"):
                uri = self.unpack_tarred_image(uri)
            else:
                print uri, mtype

        return uri


