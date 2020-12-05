from subprocess import run, CalledProcessError

class Component():
    name = ""
    modfile = ""
    input = []
    options = ""
    assets = ""
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
        except CalledProcessError as e:
            print("Return code: " + e.returncode)
            print("Output: " + e.stdout)
        finally:
            return process.returncode

    def run(self):
        # Execute the component and return the stdout
        # The components should prefer stdout over stderr
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
