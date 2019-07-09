from common.xml_parser_utilties import XMLParserUtilies
# for finding files
import glob
from pathlib import Path, PurePath
import os
# for type hinting
from typing import Dict, Tuple, Set, Callable, Union
from common.models.user import User
from common.models.post import Post, Question, Answer
from common.models.tag import Tag
from common.models.comment import Comment

import pymysql.cursors
from creds import USERNAME, PASSWORD

# have this be the directory that contains the site folders of the xmls
# don't put the data in the repo
WINDOWS = False
RAW_DATA_DIR = r"C:\Users\railcomm\Desktop\data\\"
if WINDOWS:
    RAW_DATA_DIR = Path(RAW_DATA_DIR)
BUFFER_SIZE = 100

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

def main():
    site_id_map, id_site_map = index_site_folders()
    xmls = index_site_xmls(site_id_map)

    site_count = max(xmls, key=lambda x: x[0])[0]

    connection = pymysql.connect(host='localhost',
                                 user=USERNAME,
                                 password=PASSWORD,
                                 db="main",
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    with connection.cursor() as cursor:
        for local_site_id in range(site_count):
            # TODO insert site into DB
            site_insert_sql = "INSERT IGNORE INTO `site` (`siteId`, `name`) VALUES (%s, %s)"
            cursor.execute(site_insert_sql, (id_site_map[local_site_id]))
            remote_site_id = cursor.lastrowid

            buffer = []


            # Users
            users_xml_file = next(filter(lambda x: "Users.xml" in x[1] and x[0] == remote_site_id, xmls))[1]
            user_insert_sql = "INSERT IGNORE INTO `user` (`id`, `siteId`, `username`, `reputation`, `created`) VALUES (%s, %s, %s, %s, %s)"
            user_data_lambda: Callable[[User], Tuple] = lambda user: (user.id, remote_site_id, user.name, user.rep, user.ts)
            for row in XMLParserUtilies.getRows(users_xml_file):
                buffer.append(User.parseUserXMLNode(row))

                if(len(buffer)) >= BUFFER_SIZE:
                    cursor.executemany(user_insert_sql,  map(user_data_lambda, buffer))
                    buffer = []
            if len(buffer) > 0:
                cursor.executemany(user_insert_sql, map(user_data_lambda, buffer))
                buffer = []


            # Tags
            u_tag_id_map: Dict[str, int] = {}
            tag_insert_sql = "INSERT IGNORE INTO `tag` (`tagId`, `name`, `count`) VALUES (%s, %s, %s)"
            tag_data_lambda: Callable[[Tag], Tuple] = lambda tag: (tag.id, tag.name, tag.count)
            tags_xml_file = next(filter(lambda x: "Tags.xml" in x[1] and x[0] == remote_site_id, xmls))[1]
            for row in XMLParserUtilies.getRows(tags_xml_file):
                tag = Tag.parseTagXMLNode(row)
                buffer.append(tag)

                if (len(buffer)) >= BUFFER_SIZE:
                    cursor.executemany(tag_insert_sql, map(tag_data_lambda, buffer))
                    for i in range(len(buffer)):
                        u_tag_id_map[buffer[i].name] = cursor.lastrowid - len(buffer) + i + 1
                    buffer = []
            if len(buffer) > 0:
                cursor.executemany(tag_insert_sql, map(tag_data_lambda, buffer))
                for i in range(len(buffer)):
                    u_tag_id_map[buffer[i].name] = cursor.lastrowid - len(buffer) + i + 1
                buffer = []


            # Posts
            post_id_map = {}
            posts_xml_file = next(filter(lambda x: "Posts.xml" in x[1] and x[0] == remote_site_id, xmls))[1]
            post_insert_sql = "INSERT IGNORE INTO `post` (`postId`, `created`, `score`, `title`, `userId`, `siteId`, `body`) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            answer_insert_sql = "INSERT IGNORE INTO `answer` (`u_postId`, `questionId`) VALUES (%s, %s)"
            question_insert_sql = "INSERT IGNORE INTO `question` (`u_postId`, `questionId`) VALUES (%s, %s)"
            describes_insert_sql = "INSERT IGNORE INTO `describes` (`u_postId`, `u_tagId`) VALUES (%s, %s)"
            for row in XMLParserUtilies.getRows(posts_xml_file):
                post: Union[Question, Answer] = Post.parsePostXMLNode(row, remote_site_id)
                cursor.execute(post_insert_sql, (post.id, post.date_created, post.score, post.title, post.owner_id, post.site_id, post.body))
                u_postId = cursor.lastrowid
                post_id_map[post.id] = u_postId

                if type(post) is Question:
                    cursor.execute(question_insert_sql, (u_postId, post.acceptedId))
                    for tag in post.tags:
                        cursor.execute(describes_insert_sql, (u_postId, u_tag_id_map[tag]))
                else:
                    cursor.execute(answer_insert_sql, (u_postId, post.questionId))

            # Posts round 2
            questions_update_sql = "UPDATE `question` WHERE `u_postId` = %s SET questionId = %s"
            answers_update_sql = "UPDATE `answer` WHERE `u_postId` = %s SET acceptedId = %s"
            for row in XMLParserUtilies.getRows(posts_xml_file):
                post: Union[Question, Answer] = Post.parsePostXMLNode(row, remote_site_id)

                if type(post) is Question:
                    cursor.execute(questions_update_sql, (post.id, post_id_map[post.acceptedId]))
                else:
                    cursor.execute(answers_update_sql, (post.id, post_id_map[post.questionId]))

            # Comments
            comments_xml_file = next(filter(lambda x: "Comments.xml" in x[1] and x[0] == remote_site_id, xmls))[1]
            comment_insert_sql = "INSERT IGNORE INTO `comment` (`id`, `score`, `body`, `created`, `userId`, `siteId`, `u_postId`) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            comment_data_lambda: Callable[[Comment], Tuple] = \
                lambda comment: (comment.id, comment.score, comment.body, comment.date_created, comment.user_id, remote_site_id, post_id_map[comment.id])
            for row in XMLParserUtilies.getRows(comments_xml_file):
                print(Comment.parseCommentXMLNode(row))

                if (len(buffer)) >= BUFFER_SIZE:
                    cursor.executemany(comment_insert_sql, map(comment_data_lambda, buffer))
                    buffer = []
            if len(buffer) > 0:
                cursor.executemany(comment_insert_sql, map(comment_data_lambda, buffer))
                buffer = []



if __name__ == '__main__':
    main()
