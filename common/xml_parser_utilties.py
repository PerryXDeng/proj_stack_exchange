import xml.etree.ElementTree as ET


class XMLParserUtilies:
    @staticmethod
    def getRows(filename):

        # Streaming parse to prevent memory overflow
        for event, elem in ET.iterparse(filename, events=('end',)):
            if elem.tag == 'row':
                yield elem
                elem.clear()

