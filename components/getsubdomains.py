import subprocess
import pathlib
import json
import shutil
from component import Component

class GetSubdomains(Component):
    name = "getsubdomains"
    parent = ""
    modfile = "components/getsubdomains.sh"
    input = []
    tools = [
        "bass",
        "subfinder",
        "github-subdomains",
        "Amass",
        "hakrawler",
        "subscraper",
        "shuffledns",
        "nscope",
    ]
    tools_dir = pathlib.Path.home() / "tools"

    def __init__(self, target, scope, asset_path):
        self.target = target
        self.scope = scope
        self.asset_path = asset_path
        self.subdomains_all = []

        self.create_dirs()

        # Save scope as a file
        ## Make a correct file path in default folder structure
        (pathlib.Path(self._config.assets_path) / self.target).mkdir(parents=True, exist_ok=True)
        p = pathlib.Path(self._config.assets_path) / self.target / f"{self.target}.json"
        with open(p, "w+") as f:
            ## If dictionary then write to file
            if type(self.scope) is dict:
                f.write(json.dumps(self.scope))
                # fix scope variable to pass the file later
                self.scope = p
            ## If a file path is given, then save into correct path
            ## only if the path is not correct
            elif self.scope != p:
                shutil.copyfile(self.scope, f)

    def install(self):
        try:
            # "https://github.com/projectdiscovery/subfinder"
            subprocess.run(
                "GO111MODULE=on go get github.com/projectdiscovery/subfinder/v2/cmd/subfinder",
                shell=True,
                stdout=subprocess.STDOUT,
                stderr=subprocess.STDOUT,
                check=True
            )

            # "https://github.com/gwen001/github-subdomains"
            subprocess.run(
                "GO111MODULE=on go get github.com/gwen001/github-subdomains",
                shell=True,
                stdout=subprocess.STDOUT,
                stderr=subprocess.STDOUT,
                check=True
            )

            # "https://github.com/OWASP/Amass"
            subprocess.run(
                "GO111MODULE=on go get github.com/OWASP/Amass",
                shell=True,
                stdout=subprocess.STDOUT,
                stderr=subprocess.STDOUT,
                check=True
            )

            # "https://github.com/hakluke/hakrawler"
            subprocess.run(
                "GO111MODULE=on go get github.com/hakluke/hakrawler",
                shell=True,
                stdout=subprocess.STDOUT,
                stderr=subprocess.STDOUT,
                check=True
            )

            # "https://github.com/projectdiscovery/shuffledns"
            # go get -u github.com/projectdiscovery/shuffledns/cmd/shuffledns
            subprocess.run(
                "GO111MODULE=on go get github.com/projectdiscovery/shuffledns/cmd/shuffledns",
                shell=True,
                stdout=subprocess.STDOUT,
                stderr=subprocess.STDOUT,
                check=True
            )

            # "https://github.com/m8r0wn/subscraper"
            if (self.tools_dir / 'subscraper').exists():
                subprocess.run(
                    f"cd {self.tools_dir / 'subscraper'}; git pull",
                    shell=True,
                    stdout=subprocess.STDOUT,
                    stderr=subprocess.STDOUT,
                    check=True
                )
            else:
                subprocess.run(
                    f"git clone https://github.com/Cillian-Collins/subscraper.git \
                        {self.tools_dir / 'subscraper'}",
                    shell=True,
                    stdout=subprocess.STDOUT,
                    stderr=subprocess.STDOUT,
                    check=True
                )
            subprocess.run(
                f"pip3 install -r {self.tools_dir / 'subscraper'}/requirements.txt",
                shell=True,
                stdout=subprocess.STDOUT,
                stderr=subprocess.STDOUT,
                check=True
            )

            # "https://github.com/Abss0x7tbh/bass"
            if (self.tools_dir / 'bass').exists():
                subprocess.run(
                    f"cd {self.tools_dir / 'bass'}; git pull",
                    shell=True,
                    stdout=subprocess.STDOUT,
                    stderr=subprocess.STDOUT,
                    check=True
                )
            else:
                subprocess.run(
                    f"git clone https://github.com/Abss0x7tbh/bass.git \
                        {self.tools_dir / 'bass'}",
                    shell=True,
                    stdout=subprocess.STDOUT,
                    stderr=subprocess.STDOUT,
                    check=True
                )
            subprocess.run(
                f"pip3 install -r {self.tools_dir / 'bass'}/requirements.txt",
                shell=True,
                stdout=subprocess.STDOUT,
                stderr=subprocess.STDOUT,
                check=True
            )

            # "https://github.com/ponderng/nscope"
            if (self.tools_dir / 'nscope').exists():
                subprocess.run(
                    f"cd {self.tools_dir / 'nscope'}; git pull",
                    shell=True,
                    stdout=subprocess.STDOUT,
                    stderr=subprocess.STDOUT,
                    check=True
                )
            else:
                subprocess.run(
                    f"git clone https://github.com/ponderng/nscope.git \
                        {self.tools_dir / 'nscope'}",
                    shell=True,
                    stdout=subprocess.STDOUT,
                    stderr=subprocess.STDOUT,
                    check=True
                )
        except subprocess.CalledProcessError as e:
            if e.returncode != 0:
                print("There was a problem with installing a tool... \r\n")
                print(e.output.decode('utf-8'))
                return e.returncode
        return 0

    def create_dirs(self):
        _subs_path = self.asset_path / "subs"
        _subs_path.mkdir(parents=True, exist_ok=True)

        _wordlist_path = self.asset_path / "wordlist"
        _wordlist_path.mkdir(parents=True, exist_ok=True)

        _ips_path = self.asset_path / "ips"
        _ips_path.mkdir(parents=True, exist_ok=True)
        return 0

    def check_input(self):
        return 0

    def bass(self):
        return 0

    def subfinder(self):
        return 0

    def github_subdomains(self):
        return 0

    def amass(self):
        return 0

    def resolve_all(self):
        return 0

    def check_scope(self):
        return 0

    def run(self):
        # Execute the component elements and return the stdout
        # The tools should send everything to stdout
        try:
            self.create_dirs()
            self.check_input()
            self.bass()
            self.subfinder()
            self.github_subdomains()
            self.amass()
            self.resolve_all()
            return self.subdomains_all
        except subprocess.CalledProcessError as e:
            print("\n\nRun Command: " + e.cmd)
            print("\n\nOutput: " + e.output)
            return e.returncode