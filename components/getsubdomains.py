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