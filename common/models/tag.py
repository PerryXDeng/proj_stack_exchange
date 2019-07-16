from xml.etree.ElementTree import Element
import uuid

def get_random_id():
    return uuid.uuid4().int & (1 << 64) - 1

class Tag:
    def __init__(self, uuid, id, count, name):
        self.uuid = uuid
        self.id = id
        self.count = count
        self.name = name

    def __str__(self):
       return  f"tag: {{id : {self.id} , count : {self.count} , name : {self.name}}}"
    
    @staticmethod
    def parseTagXMLNode(node: Element):
        return Tag(get_random_id(), int(node.get("Id")), int(node.get("Count")), node.get("TagName"))
