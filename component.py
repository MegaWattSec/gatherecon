import json
from pathlib import Path
from subprocess import run, CalledProcessError
from shutil import copyfile
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

    def __init__(self, target, scope):
        self.target = target
        self.scope = scope

    def install(self):
        # Run component's install and verify function
        # components must have '--install' available, which
        # must complete and return a '0' for good result, or error code
        try:
            process = run(
                [self.modfile, '--install'],
                capture_output=True,
                check=True,
                encoding='utf-8'
            )
            return process.returncode
        except CalledProcessError as e:
            print("Return code: " + e.returncode)
            print("Output: " + e.stdout)
            return e.returncode

    def run(self):
        # Save scope as a file
        ## Make a correct file path in default folder structure
        p = Path(self._config.assets_path) / self.target / f"{self.target}.json"
        with open(p, "w+") as f:
            ## If dictionary then write to file
            if type(self.scope) is dict:
                f.write(json.dumps(self.scope))
                # fix scope variable to pass the file later
                self.scope = p
            ## If a file path is given, then save into correct path
            ## only if the path is not correct
            elif self.scope != p:
                copyfile(self.scope, f)

        # Execute the component and return the stdout
        # The components should prefer stdout over stderr
        try:
            process = run(
                [self.modfile, self.options],
                capture_output=True,
                check=True,
                encoding='utf-8'
            )
            return process.stdout
        except CalledProcessError as e:
            print("\n\nRun Command: " + e.cmd)
            print("\n\nOutput: " + e.output)
            return e.returncode