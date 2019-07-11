from common.xml_parser_utilties import XMLParserUtilies
# for finding files
import glob
from pathlib import Path, PurePath
import os
# for type hinting
import typing

# have this be the directory that contains the site folders of the xmls
# don't put the data in the repo
WINDOWS = False
RAW_DATA_DIR = renderer"C:\Users\railcomm\Desktop\data\\"
if WINDOWS:
    RAW_DATA_DIR = Path(RAW_DATA_DIR)


def get_folder_site(folder_path:str) -> str:
    """
    splits the path to the folder to get the name of the site
    :param folder_path: path to folder
    :return: name of site
    """
    return PurePath(folder_path).parts[-1]


def index_site_folders() -> typing.Dict[str, int]:
    """
    index the site folders into a dictionary of site_name:site_id
    :return: the dictionary
    """
    dic = {}
    folders = glob.glob(RAW_DATA_DIR + "*/")
    count = 0
    for folder in folders:
        site_name = get_folder_site(folder)
        dic[site_name] = count
        count += 1
    return dic


def index_site_xmls(site_id_map:typing.Dict[str, int]) -> typing.Set[typing.Tuple[int, str]]:
    """
    index all the xmls under subfolders of RAW_DATA_DIR
    :param site_id_map: indexed site names
    :return: a set of tuples of (site_id, file_path)
    """
    xmls = set()
    xml_paths = glob.glob(RAW_DATA_DIR + "*/*.xml")
    for xml_path in xml_paths:
        path_fields = PurePath(xml_path).parts
        site = path_fields[-2]
        site_id = site_id_map[site]
        xmls.add((site_id, xml_path))
    return xmls


def test_file_paths_indexing():
    """
    tests whether the file paths of the xmls can be indexed to site_ids on your computer
    xmls that belong to the same site should have the same site_id
    :return: None
    """
    site_id_map = index_site_folders()
    xmls = index_site_xmls(site_id_map)
    for el in xmls:
        print("Site ID: %d, File Path: %s" % (el[0], el[1]))


def main():
    # for site
        # Users
        # Posts
        # Tags
    # for row in XMLParserUtilies.getRows(renderer"F:\Big Data\askubuntu.com\PostHistory.xml"):
        # print(row)
    test_file_paths_indexing()


if __name__ == '__main__':
    main()
