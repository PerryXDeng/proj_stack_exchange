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
BUFFER_SIZE = 100000

def list_insert_helper(array: List, i, data):
    if len(array) <= i:
        array.extend([None] * (i - len(array) + 1))
    array[i] = data


def get_random_id():
    return uuid.uuid4().int & (1 << 64) - 1

def get_folder_site(folder_path:str) -> str:
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
        connection = pymysql.connect(host='localhost',
                                     user=USERNAME,
                                     password=PASSWORD,
                                     db="main2",
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection.cursor() as cursor:
            site_insert_sql = "INSERT IGNORE INTO `site` (`name`) VALUES (%s)"
            # site_select_sql = "SELECT `siteId` FROM `site` WHERE `name` = %s"
            cursor.execute(site_insert_sql, site_name)
            remote_site_id = cursor.lastrowid

            if remote_site_id == 0:
                print(f"Site '{site_name}' has already been added or partially added!")
                return
            connection.commit()

            buffer = []

            print(f"Adding users from Site '{site_name}'")
            # Users
            users_xml_file = list(filter(lambda x: "Users.xml" in x[1] and x[0] == local_site_id, xmls))[0][1]
            user_insert_sql = "INSERT IGNORE INTO `user` (`id`, `siteId`, `username`, `reputation`, `created`) VALUES (%s, %s, %s, %s, %s)"
            user_data_lambda: Callable[[User], Tuple] = lambda user: (user.id, remote_site_id, user.name, user.rep, user.ts)
            for row in XMLParserUtilies.getRows(users_xml_file):
                buffer.append(User.parseUserXMLNode(row))

                if (len(buffer)) >= BUFFER_SIZE:
                    cursor.executemany(user_insert_sql, map(user_data_lambda, buffer))
                    buffer = []
            if len(buffer) > 0:
                cursor.executemany(user_insert_sql, map(user_data_lambda, buffer))
                buffer = []
            connection.commit()

            # Tags
            print(f"Adding tags from Site '{site_name}'")
            u_tag_id_map: Dict[str, int] = {}
            tag_insert_sql = "INSERT IGNORE INTO `tag` (`u_tagId`,`tagId`, `name`, `count`) VALUES (%s, %s, %s, %s)"
            tag_data_lambda: Callable[[Tag], Tuple] = lambda tag: (tag.uuid, tag.id, tag.name, tag.count)
            tags_xml_file = list(filter(lambda x: "Tags.xml" in x[1] and x[0] == local_site_id, xmls))[0][1]
            for row in XMLParserUtilies.getRows(tags_xml_file):
                tag = Tag.parseTagXMLNode(row)
                buffer.append(tag)

                if (len(buffer)) >= BUFFER_SIZE:
                    cursor.executemany(tag_insert_sql, map(tag_data_lambda, buffer))
                    for i in range(len(buffer)):
                        u_tag_id_map[buffer[i].name] = buffer[i].uuid
                    connection.commit()
                    buffer = []
            if len(buffer) > 0:
                cursor.executemany(tag_insert_sql, map(tag_data_lambda, buffer))
                for i in range(len(buffer)):
                    u_tag_id_map[buffer[i].name] = buffer[i].uuid
                buffer = []
            connection.commit()

            # Posts
            print(f"Adding posts from Site '{site_name}'")
            post_counter = 0
            post_id_map = []
            posts_xml_file = list(filter(lambda x: "Posts.xml" in x[1] and x[0] == local_site_id, xmls))[0][1]
            post_insert_sql = "INSERT IGNORE INTO `post` (`u_postId`, `postId`, `created`, `score`, `title`, `userId`, `siteId`, `body`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            describes_insert_sql = "INSERT IGNORE INTO `describes` (`u_postId`, `u_tagId`) VALUES (%s, %s)"

            post_buffer = []
            describes_buffer = []
            tag_buffer = []

            for row in XMLParserUtilies.getRows(posts_xml_file):
                post: Union[Question, Answer] = Post.parsePostXMLNode(row, remote_site_id)
                post_buffer.append(
                    (get_random_id(), post.id, post.date_created, post.score, post.title, post.owner_id, post.site_id, post.body))

                if type(post) is Question:
                    tag_buffer.append(post.tags)
                else:
                    tag_buffer.append([])

                if len(post_buffer) >= BUFFER_SIZE:
                    print(cursor.executemany(post_insert_sql, post_buffer), len(post_buffer))

                    for i in range(len(post_buffer)):
                        list_insert_helper(post_id_map, post_buffer[i][1], post_buffer[i][0])
                        for tag in tag_buffer[i]:
                            describes_buffer.append((post_buffer[i][0], u_tag_id_map[tag]))
                    cursor.executemany(describes_insert_sql, describes_buffer)
                    connection.commit()
                    post_buffer = []
                    describes_buffer = []
                    tag_buffer = []
            if len(post_buffer) > 0 or len(describes_buffer) > 0:
                print(cursor.executemany(post_insert_sql, post_buffer), len(post_buffer))
                for i in range(len(post_buffer)):
                    list_insert_helper(post_id_map, post_buffer[i][1], post_buffer[i][0])
                    for tag in tag_buffer[i]:
                        describes_buffer.append((post_buffer[i][0], u_tag_id_map[tag]))
                cursor.executemany(describes_insert_sql, describes_buffer)
                connection.commit()
                post_buffer = []
                describes_buffer = []
                tag_buffer = []

            # Posts round 2
            answer_buffer = []
            question_buffer = []
            print(f"Adding qs & as '{site_name}'")
            answer_insert_sql = "INSERT IGNORE INTO `answer` (`u_postId`, `questionId`) VALUES (%s, %s)"
            question_insert_sql = "INSERT IGNORE INTO `question` (`u_postId`, `acceptedId`) VALUES (%s, %s)"
            for row in XMLParserUtilies.getRows(posts_xml_file):
                post: Union[Question, Answer] = Post.parsePostXMLNode(row, remote_site_id)

                if type(post) is Question:
                    question_buffer.append((post_id_map[post.id],
                                            None if post.acceptedId == None or
                                                    post.acceptedId >= len(post_id_map) or
                                                    post_id_map[post.acceptedId] == None
                                            else post_id_map[post.acceptedId]))
                else:
                    answer_buffer.append((post_id_map[post.id],
                                          None if post.questionId == None or
                                                  post.questionId >= len(post_id_map) or
                                                  post_id_map[post.questionId] == None
                                          else post_id_map[post.questionId]))

                if len(question_buffer) >= BUFFER_SIZE or len(answer_buffer) >= BUFFER_SIZE:
                    cursor.executemany(question_insert_sql, question_buffer)
                    cursor.executemany(answer_insert_sql, answer_buffer)
                    connection.commit()

                    answer_buffer = []
                    question_buffer = []

            if len(question_buffer) > 0 or len(answer_buffer) > 0:
                cursor.executemany(question_insert_sql, question_buffer)
                cursor.executemany(answer_insert_sql, answer_buffer)
                connection.commit()

                answer_buffer = []
                question_buffer = []

            # Comments
            print(f"Adding comments from Site '{site_name}'")
            comments_xml_file = list(filter(lambda x: "Comments.xml" in x[1] and x[0] == local_site_id, xmls))[0][1]
            comment_insert_sql = "INSERT IGNORE INTO `comment` (`id`, `score`, `body`, `created`, `userId`, `siteId`, `u_postId`) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            comment_data_lambda: Callable[[Comment], Tuple] = \
                lambda comment: (
                comment.id, comment.score, comment.body, comment.date_created, comment.user_id, remote_site_id,
                post_id_map[comment.post_id])
            for row in XMLParserUtilies.getRows(comments_xml_file):
                buffer.append(Comment.parseCommentXMLNode(row))

                if (len(buffer)) >= BUFFER_SIZE:
                    cursor.executemany(comment_insert_sql, map(comment_data_lambda, buffer))
                    buffer = []
            if len(buffer) > 0:
                cursor.executemany(comment_insert_sql, map(comment_data_lambda, buffer))
                buffer = []
            connection.commit()
    except Exception as ex:
        print(site_name, "failed!")
        print(str(ex))
        raise ex
    print(site_name, "succeeded!")

def main():
    site_id_map, id_site_map = index_site_folders()
    xmls = index_site_xmls(site_id_map)

    site_count = max(xmls, key=lambda x: x[0])[0] + 1

    pool = Pool(processes=1) #Careful with this can lead to mysql deadlock
    arg_list = [(local_site_id, id_site_map[local_site_id], xmls) for local_site_id in range(site_count)]
    pool.starmap(upload_site, arg_list)


if __name__ == '__main__':
    main()
