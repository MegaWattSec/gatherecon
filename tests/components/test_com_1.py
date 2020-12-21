from component import Component

class TestCom1(Component):
    name = "test_com_1"
    parent = ""
    modfile = ""
    input = []
    tools = [
    ]
    def __init__(self, target, scope):
        self.target = target
        self.scope = scope
        self.options = f"-d {self.target} -s {self.scope}"