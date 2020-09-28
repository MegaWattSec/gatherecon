from recon import ReconSession
from gatherecon_db import GatherreconDb

class Project:
    db = None
    current_recon = None
    
    def __init__(self, domain, scope):
        self.domain = domain
        self.scope = scope
        self.db = GatherreconDb()

    def start_recon(self):
        self.current_recon = ReconSession()
        return self.current_recon

    def start_probe(self):
        return True

    def list_recon(self):
        return True

    def schedule_recon(self):
        return True

    def compare_recon(self):
        return True