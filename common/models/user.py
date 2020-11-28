from xml.etree.ElementTree import Element

class User:
    def __init__(self, id: int, ts: str, name: str, rep: int):
        self.id = id
        self.ts = ts
        self.name = name
        self.rep = rep

    def __str__(self):
        return f"user: {{ID : {self.id} , CreationDate : {self.ts} , DisplayName : {self.name} , Reputation : {self.rep}}}"

    @staticmethod
    def parseUserXMLNode(node: Element):
        return User(int(node.get("Id")), node.get("CreationDate"), node.get("DisplayName"), int(node.get("Reputation")))