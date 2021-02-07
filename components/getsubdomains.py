import subprocess
import pathlib
import shutil
from axiom import Axiom
from component import Component
from config import Config

class GetSubdomains(Component):
    name = "getsubdomains"
    parent = ""
    input = ["primary_domains.txt"]  # input needs to be file with domains to run
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
    axiom_name = "gatherecon-getsubs"
    axiom_limit = None       # Maximum axiom instances that make sense for this component

    def __init__(self, target, scope, _session_path):
        self.scope = scope      # Scope file
        self.target = target    # Handle string in bounty-targets-data for the target company
        self.session_path = pathlib.Path.home() / _session_path      # Path to local session folder
        self.session_path.mkdir(parents=True, exist_ok=True)
        self.all_subdomains = []        # Results from all submodules
        self.output = self.session_path / "active_subs.txt"     # Final output file

        # Setup axiom
        self.axiom = Axiom()

        # Open config and get/create paths
        self.cfg = Config()
        self.tools_dir = pathlib.Path(self.cfg.tools_path)
        self.base_dir = pathlib.Path(self.cfg.base_path)
        self.install_dir = pathlib.Path(self.cfg.install_path)
        self.subs_path = self.session_path / "subs"
        self.subs_path.mkdir(parents=True, exist_ok=True)
        self.wordlist_path = self.session_path / "wordlist"
        self.wordlist_path.mkdir(parents=True, exist_ok=True)
        self.ips_path = self.session_path / "ips"
        self.ips_path.mkdir(parents=True, exist_ok=True)

        # Remote paths for axiom instances
        self.remote_tools_dir = pathlib.Path(self.cfg.remote_tools_path)
        self.remote_base_dir = pathlib.Path(self.cfg.remote_base_path)
        self.remote_session_path = pathlib.Path(self.remote_base_dir / _session_path)
        self.remote_scope = self.remote_session_path / "scope.json"
        print("Session: " + str(_session_path))
        print("Local session path: " + str(self.session_path))
        print("Remote session path: " + str(self.remote_session_path))

    def install(self):
        try:
            # MassDNS prerequisite
            if not (self.tools_dir / 'massdns').exists():
                subprocess.run(
                    f"git clone https://github.com/blechschmidt/massdns.git \
                            {self.tools_dir / 'massdns'} && \
                        cd {self.tools_dir / 'massdns'} && \
                        make && \
                        make install",
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    check=True
                )

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
                "GO111MODULE=on go get -v github.com/OWASP/Amass/v3/...",
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

            # "https://github.com/Cillian-Collins/subscraper"
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
                f"pip install -r {self.tools_dir / 'subscraper' / 'requirements.txt'}",
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

            # Seclists
            if (self.tools_dir / 'SecLists').exists():
                subprocess.run(
                    f"cd {self.tools_dir / 'SecLists'}; git pull",
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    check=True
                )
            else:
                subprocess.run(
                    f"git clone https://github.com/danielmiessler/SecLists.git \
                        {self.tools_dir / 'SecLists'}",
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

    def get_input(self):
        self.input_domains = []
        with open(self.session_path / self.input[0], "w+") as f:
            for line in f:
                self.input_domains += line.strip()
        return self.input_domains

    def bass(self, domain):
        # If there are avialable axiom instances, use one
        if self.axiom.axiom_count > 0:
            r = self.axiom.exec(f"python3 {self.tools_dir}/bass/bass.py \
                    -d '{domain}' \
                    -o {self.ips_path}/resolvers.txt")
            # Decrement the available axiom instance count
            self.axiom.axiom_count -= 1
        else:
            r = subprocess.run(
                f"python3 {self.tools_dir}/bass/bass.py \
                    -d '{domain}' \
                    -o {self.ips_path}/resolvers.txt",
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                check=True
                ).returncode
        return r

    def subfinder(self, domain):
        r = subprocess.run(
            f"{self.base_dir}/go/bin/subfinder -d '{domain}' \
                -config {self.base_dir}/gatherecon/configs/subfinder.yaml \
                -o {self.subs_path}/subfinder.txt",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=True
        )
        with open(self.subs_path / "subfinder.txt", 'w+') as out_file:
            self.all_subdomains += [line.rstrip('\n') for line in out_file]
        return r.returncode

    def amass(self, domain):
        # "$HOME"/go/bin/amass enum -passive -dir "$SUBS"/amass -d "$DOMAIN" -config "$HOME"/gatherecon/configs/amass.ini -oA "$SUBS"/amass_scan
        r = subprocess.run(
            f"{self.base_dir}/go/bin/amass enum -d '{domain}' \
                -passive \
                -dir {self.subs_path}/amass \
                -oA {self.subs_path}/amass_scan",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=True
        )
        with open(self.subs_path / "amass_scan.txt", 'w+') as out_file:
            self.all_subdomains += [line.rstrip('\n') for line in out_file]
        return r.returncode

    def hakrawler(self, domain):
        #hakrawler -js -linkfinder -subs -depth 2 -scope subs -url "$DOMAIN" -outdir "$SUBS"/hakrawler
        r = subprocess.run(
            f"{self.base_dir}/go/bin/hakrawler -url {domain} \
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
        with open(self.subs_path / "hakrawler.txt", 'w+') as out_file:
            self.all_subdomains += [line.rstrip('\n') for line in out_file]
        return r.returncode

    def subscraper(self, domain):
        # "$TOOLS"/subscraper/subscraper.py -u "$DOMAIN" -o "$SUBS"/subscraper.txt
        r = subprocess.run(
            f"python3 {self.tools_dir}/subscraper/subscraper.py -u {domain} \
                -o {self.subs_path}/subscraper.txt",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=True
        )
        with open(self.subs_path / "subscraper.txt", 'w+') as out_file:
            self.all_subdomains += [line.rstrip('\n') for line in out_file]
        return r.returncode

    def resolve_all(self):
        # sort list of domains and make unique
        self.all_subdomains = sorted(set(self.all_subdomains))

        # combine all subdomains in a text file and run against resolvers
        with open(self.subs_path / "all_subdomains.txt", "w+") as f:
            for item in self.all_subdomains:
                f.write(item + "\n")

        r = subprocess.run(
            f"{self.base_dir}/go/bin/shuffledns -silent \
                -list {self.subs_path}/all_subdomains.txt \
                -r {self.ips_path}/resolvers.txt \
                -o {self.subs_path}/active_subs.txt",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=True
        )
        with open(self.subs_path / "active_subs.txt", 'w+') as out_file:
            self.all_subdomains += [line.rstrip('\n') for line in out_file]
        return r.returncode

    def check_scope(self, url, program, instances):
        # Take a URL as the input
        # then check against the scope file using nscope
        print("Checking scope...")
        print(f"Scope: {self.scope}\nTarget: {program}\nDomain: {url}")
        print("Using Instances: " + str(instances))

        # Upload scope file
        self.axiom.send(self.scope, self.remote_scope, instances)

        # Execute check scope on axiom instance
        results = self.axiom.exec(
            f"python3 {self.remote_tools_dir}/nscope/nscope \
                 -d '{self.remote_scope}' \
                 -p '{program}' \
                 -t '{url}'",
            instances
        )
        print("Results: " + str(results))
        return results

    def exec_tool(self, tool, count, *args):
        results = tool(*args, self.axiom.instances[0:count])
        return results

    def run(self):
        # Execute the component elements
        try:
            domains = self.get_input()
            for domain in domains:
                self.exec_tool(self.check_scope, 1, domain, self.target)
                self.bass(domain)
                self.subfinder(domain)
                self.amass(domain)
                self.hakrawler(domain)
                self.subscraper(domain)
            result = self.resolve_all()
            # Copy output from resolve_all into session folder as final output
            shutil.copy(self.subs_path / "active_subs.txt", self.session_path / self.output)
            return result
        except subprocess.CalledProcessError as e:
            print("\n\nRun Command: " + e.cmd)
            print("\n\nOutput: " + e.output.decode("utf-8"))
            return e.returncode