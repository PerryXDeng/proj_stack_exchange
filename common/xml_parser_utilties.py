import xml.etree.ElementTree as ET


class XMLParserUtilies:
    @staticmethod
    def getRows(filename, min_starting_line=0):
        count = 0
        root = None
        # Streaming parse to prevent memory overflow
        for event, elem in ET.iterparse(filename, events=('start', 'end')):
            count += 1
            if root is None:
                root = elem
            if root is not None and count % 50000 == 0:
                print(count)
                root.clear()
            if count >= min_starting_line and elem.tag == 'row' and event == 'end':
                yield elem
                elem.clear()
