import os
from jupyterhub.spawner import LocalProcessSpawner

from traitlets import Unicode
from traitlets import default

class NativeProcessSpawner(LocalProcessSpawner):

    home_dir = Unicode(help="The home directory for the user")

    @default('home_dir')
    def _default_home_dir(self):
        return self.notebook_dir.format(username=self.user.name)

    def make_preexec_fn(self, name):
        home = self.home_dir

        def preexec():
            try:
                os.makedirs(home, 0o755, exist_ok=True)
                os.chdir(home)
            except Exception as e:
                self.log.exception("Error in preexec for %s", name)

        return preexec

    def user_env(self, env):
        env['USER'] = self.user.name
        env['HOME'] = self.home_dir
        env['SHELL'] = '/bin/bash'
        return env

    def move_certs(self, paths):
        """No-op for installing certs"""
        return paths
