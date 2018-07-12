from zc.buildout.download import Download
import zc.buildout.easy_install
import ConfigParser
import multiprocessing as mp
import sys
import pkg_resources


__author__ = 'Jagadeesh N Malakannavar <mnjagadeesh@gmail.com>'


class Download_eggs():
    def __init__(self, buildout, name, options={}):
        self.url = options.get('pkgurl')
        if not self.url.endswith('/'):
            self.url += '/'
        self.dc = options.get('cache-folder')
        self.files = options.get('files-list')
        self.versions = options.get('versions-files')
        self.ed = options.get('eggs-directory')
        self.index = options.get('index', self.url)
        self.ws = zc.buildout.easy_install.Installer(dest=self.dc,
                                                     index=self.index)

    def read_versions(self):
        urls = []
        config = ConfigParser.ConfigParser()
        config.readfp(open(self.versions))
        urls = [[i[0] + '==' + i[1]] for i in config.items('versions')]
        return urls

    def mp_download(self, spec):
        req = pkg_resources.Requirement.parse([spec])
        a = self.ws._obtain(req)
        if a.location:
            download = Download(cache=self.dc)
            download(a.location)

    def install(self):
        urls = self.read_versions()
        processes = [mp.Process(target=self.mp_download,
                                args=(x,)) for x in urls]
        for p in processes:
            p.daemon = True
            p.start()

        for p in processes:
            p.join()

        return None
    update = install


if __name__ == '__main__':
    Download_eggs()
