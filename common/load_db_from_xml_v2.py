from common.xml_parser_utilties import XMLParserUtilies
# for finding files
import glob
from pathlib import Path, PurePath
import os
# for type hinting
from typing import Dict, Tuple, Set, Callable, Union, List

from common.models.user import User
from common.models.post import Post, Question, Answer
from common.models.tag import Tag
from common.models.comment import Comment
from multiprocessing import Pool
import uuid

import pymysql.cursors
from creds import USERNAME, PASSWORD

# have this be the directory that contains the site folders of the xmls
# don't put the data in the repo
WINDOWS = False
RAW_DATA_DIR = r"F:\Big Data\data\\"

if WINDOWS:
    RAW_DATA_DIR = Path(RAW_DATA_DIR)
BUFFER_SIZE = 25000


def list_insert_helper(array: List, i, data):
    if len(array) <= i:
        array.extend([None] * (i - len(array) + 1))
    array[i] = data


def get_random_id():
    return uuid.uuid4().int & (1 << 64) - 1


def get_folder_site(folder_path: str) -> str:
    """
    splits the path to the folder to get the name of the site
    :param folder_path: path to folder
    :return: name of site
    """
    return PurePath(folder_path).parts[-1]


def index_site_folders() -> Tuple[Dict[str, int], Dict[int, str]]:
    """
    index the site folders into a dictionary of site_name:site_id
    :return: the dictionary
    """
    name_to_id_dict = {}
    id_to_name_dict = {}
    folders = glob.glob(RAW_DATA_DIR + "*/")
    count = 0
    for folder in folders:
        site_name = get_folder_site(folder)
        name_to_id_dict[site_name] = count
        id_to_name_dict[count] = site_name
        count += 1
    return name_to_id_dict, id_to_name_dict


def index_site_xmls(site_id_map: Dict[str, int]) -> Set[Tuple[int, str]]:
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
    site_id_map, id_site_map = index_site_folders()
    xmls = index_site_xmls(site_id_map)
    for el in xmls:
        print("Site ID: %d, File Path: %s" % (el[0], el[1]))


def upload_site(local_site_id, site_name, xmls):
    try:
        # Connect to MySQL DB
        connection = pymysql.connect(host='localhost',
                                     user=USERNAME,
                                     password=PASSWORD,
                                     db="main_v2",
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor,
                                     port=3307)

        with connection.cursor() as cursor:
            # Insert our site into the db
            site_select_sql = "SELECT * FROM `site` WHERE `name` = %s"
            cursor.execute(site_select_sql, site_name)
            rows = cursor.fetchall()

            if len(rows) < 1:
                site_insert_sql = "INSERT INTO `site` (`name`) VALUES (%s)"
                cursor.execute(site_insert_sql, site_name)
                connection.commit()
                remote_site_id = cursor.lastrowid
                min_post_id = 0
            else:
                print("Site has already been created!!!!!")
                remote_site_id = rows[0]['siteId']
                min_post_id_select_sql = "SELECT MAX(`postId`) FROM `post` WHERE `siteId` = %s"
                cursor.execute(min_post_id_select_sql, remote_site_id)
                rows = cursor.fetchall()
                min_post_id = rows[0]['MAX(`postId`)']
                if min_post_id is None:
                    min_post_id = 0
                print(f"Starting @ postId {min_post_id + 1}")

            # create buffer for storing post data to use multiple insert

            buffer = []

            # Posts
            print(f"Adding posts from Site '{site_name}'")

            posts_xml_file = list(filter(lambda x: "Posts.xml" in x[1] and x[0] == local_site_id, xmls))[0][1]
            post_insert_sql = "INSERT IGNORE INTO `post` (`postId`, `siteId`, `dateCreated`, `body`) VALUES (%s, %s, %s, %s)"
            post_buffer = []

            for row in XMLParserUtilies.getRows(posts_xml_file, min_post_id):
                post: Post = Post.parsePostXMLNode(row, remote_site_id)
                if post.id <= min_post_id:
                    continue
                post_buffer.append(
                    (post.id, remote_site_id, post.date_created, post.body)
                )
                if post.id % 5000 == 0:
                    print(f"appending post {post.id} to buffer")

                if len(post_buffer) >= BUFFER_SIZE:
                    # insert posts
                    print(cursor.executemany(post_insert_sql, post_buffer), len(post_buffer))

                    post_buffer = []
                    connection.commit()

            if len(post_buffer) > 0:
                print(cursor.executemany(post_insert_sql, post_buffer), len(post_buffer))
                connection.commit()
                post_buffer = []
                describes_buffer = []
                tag_buffer = []


    except Exception as ex:
        print(site_name, "failed!")
        print(str(ex))
        raise ex
    print(site_name, "succeeded!")


def main():
    site_id_map, id_site_map = index_site_folders()
    xmls = index_site_xmls(site_id_map)

    site_count = max(xmls, key=lambda x: x[0])[0] + 1

    pool = Pool(processes=1)  # Careful with this can lead to mysql deadlock
    arg_list = [(local_site_id, id_site_map[local_site_id], xmls) for local_site_id in range(site_count)]
    pool.starmap(upload_site, arg_list)


if __name__ == '__main__':
    main()
