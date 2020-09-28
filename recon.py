import datetime

class ReconSession:
    date = None
    
    def __init__(self):
        self.date = datetime.datetime.now()