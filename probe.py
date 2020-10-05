from recon import ReconSession

class Probe:
    recon_session = None

    def __init__(self, session):
        self.recon_session = session
