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
            self.yaml = YAML()
            self.cfg = self.yaml.load(self.configfile)
        except FileNotFoundError:
            self._create(self.configfile)
            self.cfg = self.yaml.load(self.configfile)

    @property
    def db_host(self):
        return self.cfg["database"]["host"]

    @db_host.setter
    def db_host(self, host):
        self.cfg["database"]["host"] = host
        self.yaml.dump(self.cfg, self.configfile)

    @property
    def db_name(self):
        return self.cfg["database"]["name"]

    @db_name.setter
    def db_name(self, name):
        self.cfg["database"]["name"] = name
        self.yaml.dump(self.cfg, self.configfile)

    def _create(self, cfile):
        try:
            # define paths with local variables
            _basedir_path = Path.home()
            _assets_path = _basedir_path / "assets"
            _tools_path = _basedir_path / "tools"

            # put default properties into the Box object
            newcfg = { 
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
            self.yaml.dump(newcfg, cfile)

            return True
        except:
            return False