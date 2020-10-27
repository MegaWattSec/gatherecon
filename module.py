from config import Config
import subprocess
from ruamel.yaml import YAML

class Module():

    def __init__(self, module):
        self.module = module

        # Get module details from YAML file
        # config = Config()
        # module_details = config.modules["get_subdomains"]
        yaml = YAML()
        with open("configs/gatherecon.yaml") as fp:
            data = yaml.load(fp)
        
        self.input = data["modules"]["get_subdomains"]["input"]

    def check(self):
        # Run module's install and verify function
        # Modules must have '--install' available, which
        # must complete and return a '0' for good result, or error code
        process = subprocess.run(
            [self.module, '--install'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        if process.returncode is not 0:
            print("Return code: " + str(process.returncode))
            print("Output: " + process.stdout.decode("utf-8"))
        return process.returncode
