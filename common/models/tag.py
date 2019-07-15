from xml.etree.ElementTree import Element

class Tag:
    def __init__(self, id, count, name):
        self.id = id
        self.count = count
        self.name = name

    def __str__(self):
       return  f"tag: {{id : {self.id} , count : {self.count} , name : {self.name}}}"
    
    @staticmethod
    def parseTagXMLNode(node: Element):
        return Tag(int(node.get("Id")), int(node.get("Count")), node.get("TagName"))
