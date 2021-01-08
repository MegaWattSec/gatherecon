import config

class Component():
    _config = config.Config()
    assets = _config.assets_path
    name = ""
    modfile = ""
    input = []
    options = ""
    parent = ""
    tools = []

    def __init__(self, target, scope, resultdir):
        self.target = target
        self.scope = scope
        self.resultdir = resultdir
