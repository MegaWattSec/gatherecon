import datetime

class ReconSession:
    date = None
    current_session = None
    
    def __init__(self):
        self.date = datetime.datetime.now()

    def compare(self, recon1):
        return True