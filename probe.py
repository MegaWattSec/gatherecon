from recon import ReconSession
from gatherdb import GatherDb

class Probe:
    recon_session = None

    def __init__(self, session):
        self.recon_session = session
