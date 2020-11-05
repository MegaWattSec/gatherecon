from subprocess import run, CalledProcessError

class Module():
    target = ""
    scope = ""
    modfile = ""
    options = ""
    input = []
    depends = ""
    tools = []

    def __init__(self, target, scope):
        self.target = target
        self.scope = scope

    def install(self):
        # Run module's install and verify function
        # Modules must have '--install' available, which
        # must complete and return a '0' for good result, or error code
        try:
            process = run(
                [self.modfile, '--install'],
                capture_output=True,
                check=True,
                encoding='utf-8'
            )
        except CalledProcessError as e:
            print("Return code: " + e.returncode)
            print("Output: " + e.stdout)
        finally:
            return process.returncode

    def run(self):
        # Execute the module and return the stdout
        # The modules should prefer stdout over stderr
        try:
            process = run(
                [self.modfile, self.options],
                capture_output=True,
                check=True,
                encoding='utf-8'
            )
        except CalledProcessError as e:
            print("\n\nRun Command: " + e.cmd)
            print("\n\nOutput: " + e.output)
        finally:
            return process.stdout
