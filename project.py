from recon import ReconSession
from gatherdb import GatherDb, SessionList
from probe import Probe

class Project:
    db = None
    current_recon = None
    
    def __init__(self, domain, scope):
        self.domain = domain
        self.scope = scope
        self.db = GatherDb()

    def start_recon(self):
        self.current_recon = ReconSession()
        return self.current_recon

    def start_probe(self):
        self.probe = Probe(self.current_recon)
        return self.probe

    def list_recon(self):
        return SessionList()

    def schedule_recon(self):
        return True

    def compare_recon(self):
        return True