from recon import ReconSession, SessionList
from probe import Probe
from config import Config

class Project:
    
    def __init__(self, domain, scope):
        self.domain = domain
        self.scope = scope
        self.current_recon = ReconSession(self.domain, self.scope)

    def start_recon(self):
        return self.current_recon

    def start_probe(self):
        self.probe = Probe(self.current_recon)
        return self.probe

    def list_recon(self):
        config = Config()
        return SessionList(self.domain)

    def schedule_recon(self):
        return True
