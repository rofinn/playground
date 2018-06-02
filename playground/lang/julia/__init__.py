import sys
import os
import shutil
import tempfile
import subprocess
import logging


# logging.basicConfig(format='%(asctime)s %(message)s',level=logging.INFO)



# subprocess.call([
#     bin_path,
#     "-e",
#     "'Pkg.init(); Pkg.add(\"Playground\"); ENV[\"PLAYGROUND_INSTALL\"] = true; Pkg.build(\"Playground\")'"
# ])


class Config(playground.Config):
    """
    julia/
        tmp/
        src/
        bin/    # symlink -> ../bin
        share/  # playgrounds
    """
    def __init__(self, path=None):
        super(Config, self).__init__(path)

    @property
    def path(self):
        super(Config, self).path

    @property
    def tmp(self):
        super(Config, self).path.joinpath('tmp')

    @property
    def src(self):
        super(Config, self).path.joinpath('src')

    @property
    def bin(self):
        super(Config, self).path.joinpath('bin')

    @property
    def share(self):
        super(Config, self).path.joinpath('share')

    def initialize(self):
        playground.Config.initialize(self)

        for p in (self.path, self.tmp, self.src, self.share):
            if not os.path.exists(p):
                os.makedirs(p)

        self.bin.symlink_to(super(Config, self).bin)