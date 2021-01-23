import subprocess
import pathlib
import json
import shutil
from component import Component
from config import Config

class GetSubdomains(Component):
    name = "getsubdomains"
    parent = ""
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

    def __init__(self, target, scope, asset_path):
        self.target = target
        self.scope = scope
        self.asset_path = pathlib.Path(asset_path)
        self.all_subdomains = []

        # Open config and get/create paths
        self.cfg = Config()
        self.tools_dir = pathlib.Path(self.cfg.tools_path)
        self.base_dir = pathlib.Path(self.cfg.base_path)
        self.install_dir = pathlib.Path(self.cfg.install_path)

        self.subs_path = self.asset_path / "subs"
        self.subs_path.mkdir(parents=True, exist_ok=True)

        self.wordlist_path = self.asset_path / "wordlist"
        self.wordlist_path.mkdir(parents=True, exist_ok=True)

        self.ips_path = self.asset_path / "ips"
        self.ips_path.mkdir(parents=True, exist_ok=True)

        # Save scope as a file
        ## Make a correct file path in default folder structure
        (pathlib.Path(self._config.assets_path) / self.target).mkdir(parents=True, exist_ok=True)
        p = pathlib.Path(self._config.assets_path) / self.target / f"{self.target}.json"
        with open(p, "w+") as f:
            ## If dictionary then write to file
            if type(self.scope) is dict:
                f.write(f"[{json.dumps(self.scope)}]")
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
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                check=True
            )

            # "https://github.com/gwen001/github-subdomains"
            subprocess.run(
                "GO111MODULE=on go get github.com/gwen001/github-subdomains",
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                check=True
            )

            # "https://github.com/OWASP/Amass"
            subprocess.run(
                "GO111MODULE=on go get github.com/OWASP/Amass",
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                check=True
            )

            # "https://github.com/hakluke/hakrawler"
            subprocess.run(
                "GO111MODULE=on go get github.com/hakluke/hakrawler",
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                check=True
            )

            # "https://github.com/projectdiscovery/shuffledns"
            # go get -u github.com/projectdiscovery/shuffledns/cmd/shuffledns
            subprocess.run(
                "GO111MODULE=on go get github.com/projectdiscovery/shuffledns/cmd/shuffledns",
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                check=True
            )

            # "https://github.com/m8r0wn/subscraper"
            if (self.tools_dir / 'subscraper').exists():
                subprocess.run(
                    f"cd {self.tools_dir / 'subscraper'}; git pull",
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    check=True
                )
            else:
                subprocess.run(
                    f"git clone https://github.com/Cillian-Collins/subscraper.git \
                        {self.tools_dir / 'subscraper'}",
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    check=True
                )
            subprocess.run(
                f"pip3 install -r {self.tools_dir / 'subscraper'}/requirements.txt",
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                check=True
            )

            # "https://github.com/Abss0x7tbh/bass"
            if (self.tools_dir / 'bass').exists():
                subprocess.run(
                    f"cd {self.tools_dir / 'bass'}; git pull",
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    check=True
                )
            else:
                subprocess.run(
                    f"git clone https://github.com/Abss0x7tbh/bass.git \
                        {self.tools_dir / 'bass'}",
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    check=True
                )
            subprocess.run(
                f"pip3 install -r {self.tools_dir / 'bass'}/requirements.txt",
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                check=True
            )

            # "https://github.com/ponderng/nscope"
            if (self.tools_dir / 'nscope').exists():
                subprocess.run(
                    f"cd {self.tools_dir / 'nscope'}; git pull",
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    check=True
                )
            else:
                subprocess.run(
                    f"git clone https://github.com/ponderng/nscope.git \
                        {self.tools_dir / 'nscope'}",
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    check=True
                )
        except subprocess.CalledProcessError as e:
            if e.returncode != 0:
                print("There was a problem with installing a tool... \r\n")
                print(e.output.decode('utf-8'))
                return e.returncode
        return 0

    def check_input(self):
        return 0

    def bass(self):
        r = subprocess.run(
            f"python3 {self.tools_dir}/bass/bass.py \
                -d '{self.target}' \
                -o {self.ips_path}/resolvers.txt",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=True
        )
        return r.returncode

    def subfinder(self):
        r = subprocess.run(
            f"{self.base_dir}/go/bin/subfinder -d '{self.target}' \
                -config {self.base_dir}/gatherecon/configs/subfinder.yaml \
                -o {self.subs_path}/subfinder.txt",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=True
        )
        with open(self.subs_path / "subfinder.txt", 'w+') as output:
            self.all_subdomains += [line.rstrip('\n') for line in output]
        return r.returncode

    def amass(self):
        # "$HOME"/go/bin/amass enum -passive -dir "$SUBS"/amass -d "$DOMAIN" -config "$HOME"/gatherecon/configs/amass.ini -oA "$SUBS"/amass_scan
        r = subprocess.run(
            f"{self.base_dir}/go/bin/amass enum -d '{self.target}' \
                -passive \
                -config {self.base_dir}/gatherecon/configs/amass.ini \
                -dir {self.subs_path}/amass \
                -oA {self.subs_path}/amass_scan",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=True
        )
        with open(self.subs_path / "amass_scan.txt", 'w+') as output:
            self.all_subdomains += [line.rstrip('\n') for line in output]
        return r.returncode

    def hakrawler(self):
        #hakrawler -js -linkfinder -subs -depth 2 -scope subs -url "$DOMAIN" -outdir "$SUBS"/hakrawler
        r = subprocess.run(
            f"{self.base_dir}/go/bin/hakrawler -url {self.target} \
                -js -linkfinder -subs -depth 2 -scope subs \
                -outdir {self.subs_path}/hakrawler",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=True
        )
        # for each hakrawler file, extract the subdomains and save in hakrawler.txt
        files = (pathlib.Path(self.subs_path) / "hakrawler").glob('**/*')
        results = pathlib.Path(self.subs_path) / "hakrawler.txt"
        for file in files:
            with open(file, 'r') as f, open(results, 'w+') as r:
                for line in f:
                    # search for lines with "Host:"
                    if not line.find("Host:"):
                        continue
                    # separate fields
                    fields = line.strip().split()
                    # save the second field into the results file
                    r.write(fields[2])
        with open(self.subs_path / "hakrawler.txt", 'w+') as output:
            self.all_subdomains += [line.rstrip('\n') for line in output]
        return r.returncode

    def subscraper(self):
        # "$TOOLS"/subscraper/subscraper.py -u "$DOMAIN" -o "$SUBS"/subscraper.txt
        r = subprocess.run(
            f"python3 {self.tools_dir}/subscraper/subscraper.py -u {self.target} \
                -o {self.subs_path}/subscraper.txt",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=True
        )
        with open(self.subs_path / "subscraper.txt", 'w+') as output:
            self.all_subdomains += [line.rstrip('\n') for line in output]
        return r.returncode

    def resolve_all(self):
        # sort list of domains and make unique
        self.all_subdomains = sorted(set(self.all_subdomains))

        # combine all subdomains in a text file and run against resolvers
        with open(self.subs_path / "all_subdomains.txt", "w+") as f:
            for item in self.all_subdomains:
                f.write(item + "\n")

        r = subprocess.run(
            f"{self.base_dir}/go/bin/shuffledns -silent -d {self.target} \
                -list {self.subs_path}/all_subdomains.txt \
                -r {self.ips_path}/resolvers.txt \
                -o {self.subs_path}/active_subs.txt",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=True
        )
        with open(self.subs_path / "active_subs.txt", 'w+') as output:
            self.all_subdomains += [line.rstrip('\n') for line in output]
        return r.returncode

    def check_scope(self, url, program):
        # Take a URL as the input
        # then check against the scope file using nscope
        print("Checking scope...")
        print(f"Scope: {self.scope}\nProgram: {program}\nTarget: {url}")
        r = subprocess.run(
            f"python3 {self.tools_dir}/nscope/nscope \
                -d '{self.scope}' \
                -p '{program}' \
                -t '{url}'",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )
        return r.stdout

    def run(self):
        # Execute the component elements and return the stdout
        # The tools should send everything to stdout
        try:
            self.check_input()
            self.bass()
            self.subfinder()
            self.amass()
            self.hakrawler()
            self.subscraper()
            self.resolve_all()
            return self.all_subdomains
        except subprocess.CalledProcessError as e:
            print("\n\nRun Command: " + e.cmd)
            print("\n\nOutput: " + e.output)
            return e.returncode