from common.xml_parser_utilties import XMLParserUtilies
import time

def main():
    # for site
        # Users
        # Posts
        # Tags
    for row in XMLParserUtilies.getRows(r"F:\Big Data\askubuntu.com\PostHistory.xml"):
        print(row)

if __name__ == '__main__':
    main()
