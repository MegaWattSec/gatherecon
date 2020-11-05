from module import Module

class GetSubdomains(Module):

    def __init__(self, target, scope):
        self.target = target
        self.scope = scope
        self.modfile = "modules/getsubdomains.sh"
        self.options = f"-d {self.target} -s {self.scope}"
        self.input = []
        self.depends = ""
        self.tools = ["bass",
                    "subfinder",
                    "github-subdomains",
                    "Amass",
                    "hakrawler",
                    "subscraper",
                    "shuffledns",
                    "nscope",
                    ]
        