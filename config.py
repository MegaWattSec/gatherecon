from box import Box, BoxError, BoxList
from pathlib import Path
from ruamel.yaml import RoundTripLoader

class Config:
    configfile = Path.cwd() / "configs" / "gatherecon.yaml"

    def __init__(self):
        try:
            self.box = Box.from_yaml(filename = str(self.configfile), Loader = RoundTripLoader)
        except BoxError as e:
            if "does not exist" in str(e):
                self._create(self.configfile)
                self.box = Box.from_yaml(filename = str(self.configfile), Loader = RoundTripLoader)

    @property
    def db_host(self):
        return self.box.database.host

    @property
    def db_name(self):
        return self.box.database.name

    @property
    def modules(self):
        return self.box.modules.to_list()

    def _create(self, file):
        # define paths with local variables
        _basedir_path = Path.cwd()
        _assets_path = _basedir_path / "assets"
        _tools_path = _basedir_path / "tools"
        _modules_path = _basedir_path / "modules"

        # populate modules based on what's in the modules dir
        _modules = []
        for mod in Path.iterdir(_modules_path):
            _modules.append(str(mod))

        # put default properties into the Box object
        cfg_box = Box({ 
            "paths": {
                "basedir": str(_basedir_path),
                "assets": str(_assets_path),
                "modules": str(_modules_path),
                "tools": str(_tools_path),
            },
            "database": {
                "host": "localhost", 
                "name": "gatherdatabase",
            },
            "modules": _modules,
        })

        # Write Box object to YAML config file
        Box.to_yaml(cfg_box, filename=self.configfile)
        return True