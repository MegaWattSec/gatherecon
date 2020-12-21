from component import Component

class TestCom2(Component):
    name = "test_com_2"
    parent = ""
    modfile = ""
    input = []
    tools = [
    ]
    def __init__(self, target, scope):
        self.target = target
        self.scope = scope
        self.options = f"-d {self.target} -s {self.scope}"