from pathlib import Path
from ruamel.yaml import YAML

class Config:
    configpath = Path.cwd() / "configs"
    configfile = configpath / "gatherecon.yaml"
    default_host = "localhost"
    default_name = "gatherdatabase"

    def __init__(self):
        try:
            self.configpath.mkdir(exist_ok=True)
            self._yaml = YAML()
            self._cfg = self._yaml.load(self.configfile)
        except FileNotFoundError:
            self._create(self.configfile)
            self._cfg = self._yaml.load(self.configfile)

    @property
    def db_host(self):
        return self._cfg["database"]["host"]

    @db_host.setter
    def db_host(self, host):
        self._cfg["database"]["host"] = host
        self._yaml.dump(self._cfg, self.configfile)

    @property
    def db_name(self):
        return self._cfg["database"]["name"]

    @db_name.setter
    def db_name(self, name):
        self._cfg["database"]["name"] = name
        self._yaml.dump(self._cfg, self.configfile)

    @property
    def tools_path(self):
        return self._cfg["paths"]["tools"]

    def _create(self, cfile):
        try:
            # define paths with local variables
            _basedir_path = Path.home()
            _assets_path = _basedir_path / "assets"
            _tools_path = _basedir_path / "tools"

            # put default properties into the Box object
            _new_cfg = { 
                "paths": {
                    "basedir": str(_basedir_path),
                    "assets": str(_assets_path),
                    "tools": str(_tools_path),
                },
                "database": {
                    "host": self.default_host, 
                    "name": self.default_name,
                },
            }

            # Write YAML config file
            self._yaml.dump(_new_cfg, cfile)

            return True
        except:
            return False