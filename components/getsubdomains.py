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

    def __init__(self, target, scope):
        self.target = target
        self.scope = scope
        self.options = f"-d {self.target} -s {self.scope}"
        self.subdomains_all = []

    def install(self):
        return 0

    def create_dirs(self):
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

    def get_subs(self):
        return self.subdomains_all