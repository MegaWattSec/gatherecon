from config import Config
import subprocess

class Module():

    def __init__(self, module):
        self.module = module

    def check(self):
        # Run module's install and verify function
        # Modules must have '--install' available, which
        # must complete and return a '0' for good result, or error code
        process = subprocess.run(
            [self.module, '--install'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        # print("Return code: " + str(process.returncode))
        # if process.returncode is not 0:
        #     print("Output: " + str(process.stdout))
        return process.returncode
