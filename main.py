import dataclasses
import json
import sqlite3
import uuid
from pprint import pprint
from uuid import uuid5


@dataclasses.dataclass
class ContentLineItem:
    id: str
    name: str
    sub_content_ids: list


@dataclasses.dataclass
class Content:
    id = None
    name: str
    sub_contents: list

    def __init__(self, id, name, sub_contents):
        self.id = id
        self.name = name
        self.sub_contents = sub_contents

    @staticmethod
    def from_entity(content_line_item: ContentLineItem):
        if content_line_item.sub_content_ids is None:
            return Content(
                id=content_line_item.id,
                name=content_line_item.name,
                sub_contents=[]
            )
        else:
            sub_content_line_items = list(map(get_content_line_item, content_line_item.sub_content_ids))
            print(sub_content_line_items)
            return Content(
                id=content_line_item.id,
                name=content_line_item.name,
                sub_contents=list(map(Content.from_entity, sub_content_line_items))
            )


def save_content(content: Content):
    if is_bottom_line_item(content):
        sub_content_ids = []
        line_id = create_id(content.name)
    else:
        sub_content_ids = list(map(save_content, content.sub_contents))
        line_id = create_id(content.name, sub_content_ids)

    line_item = ContentLineItem(
        id=line_id,
        name=content.name,
        sub_content_ids=sub_content_ids)

    id = save_line_item(line_item)
    return id


def save_line_item(line_item: ContentLineItem):
    print(f"saving {line_item}")
    with sqlite3.connect('contents.sqlite') as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO content_line_items(id, name, subcontent_ids) VALUES (?, ?, ?) ON CONFLICT (id) DO NOTHING",
            (line_item.id, line_item.name, json.dumps(line_item.sub_content_ids)))
        conn.commit()
    return line_item.id


def is_bottom_line_item(content: Content):
    return content.sub_contents == []


def create_id(string, sub_content_ids=[]):
    if sub_content_ids == []:
        return str(uuid5(uuid.NAMESPACE_URL, string))
    else:
        return str(uuid5(uuid.NAMESPACE_URL, string + "|".join(sub_content_ids)))


def get_content_line_item(content_root_id: str):
    print(f"getting {content_root_id}")
    with sqlite3.connect('contents.sqlite') as conn:
        cursor = conn.cursor()
        cursor.execute("select * from content_line_items where id = ?", (content_root_id,))
        row = cursor.fetchone()
        id, name, sub_content_ids_json = row
        content_line_item = ContentLineItem(id, name, json.loads(sub_content_ids_json))
        print(content_line_item)
        return content_line_item


if __name__ == '__main__':
    root_line_item = get_content_line_item("58d6778d-1222-5fc2-9877-2641c19c68a7")
    print(root_line_item)
    content_from_root = Content.from_entity(root_line_item)
    pprint(content_from_root)

    root_line_item = get_content_line_item("dd65c30b-558a-55af-b873-66781f3ab9ed")
    print(root_line_item)
    content_from_root = Content.from_entity(root_line_item)
    pprint(content_from_root)

# if __name__ == '__main__':
#     contents_v1 = [
#         Content(
#             name="content_root",
#             sub_contents=[
#                 Content(
#                     name="level 1",
#                     sub_contents=[
#                         Content(name="1.1", sub_contents=[]),
#                         Content(name="1.2", sub_contents=[])
#                     ]
#                 ),
#                 Content(
#                     name="level 2",
#                     sub_contents=[Content(name="2.1", sub_contents=[
#                         Content(name="2.1.1", sub_contents=[]),
#                     ])]
#                 )
#             ]
#         )
#     ]
# 
#     for content in contents_v1:
#         save_content(content)
# 
#     print("--------------------")
# 
#     contents_v2 = [
#         Content(
#             name="content_root",
#             sub_contents=[
#                 Content(
#                     name="level 1",
#                     sub_contents=[
#                         Content(name="1.1", sub_contents=[]),
#                     ]
#                 ),
#                 Content(
#                     name="level 2",
#                     sub_contents=[Content(name="2.1", sub_contents=[
#                         Content(name="2.1.1", sub_contents=[]),
#                     ]), ]
#                 )
#             ]
#         )
#     ]
# 
#     for content in contents_v2:
#         save_content(content)
# 
#     empty_content = [Content(name="content_root", sub_contents=[])]
#     for content in empty_content:
#         save_content(content)
