import dataclasses
import json
import sqlite3
import uuid
from uuid import uuid5


@dataclasses.dataclass
class ContentLineItem:
    id: str
    name: str
    sub_content_ids: list


@dataclasses.dataclass
class Content:
    name: str
    sub_contents: list


# def save(contents: list):
#     content: Content
#     if contents == []:
#         return
#     for content in contents:
#         print(f"saving {content.name}")
#
#         if is_bottom_line_item(content):
#             line_item = ContentLineItem(
#                 id=create_id(content.name),
#                 name=content.name,
#                 sub_content_ids=[])
#             id = save_line_item(line_item)
#             return id
#         else:
#             line_item = ContentLineItem(
#                 id=create_id(content.name),
#                 name=content.name,
#                 sub_content_ids=list(map(save, content.sub_contents))
#             )
#             id = save_line_item(line_item)
#             return id


def save(content: Content):
    if content == []:
        return
    if is_bottom_line_item(content):
        line_item = ContentLineItem(
            id=create_id(content.name),
            name=content.name,
            sub_content_ids=[])
        id = save_line_item(line_item)
        return id
    else:
        sub_content_ids=list(map(save, content.sub_contents))
        line_item = ContentLineItem(
            id=create_id(content.name),
            name=content.name,
            sub_content_ids=sub_content_ids
        )
        id = save_line_item(line_item)
        return id


def save_line_item(line_item: ContentLineItem):
    conn = sqlite3.connect('contents.sqlite')
    cursor = conn.cursor()
    id = str(line_item.id)
    sub_ids = json.dumps(line_item.sub_content_ids)
    name = line_item.name
    print(f"saving {line_item}")
    cursor.execute("INSERT INTO content_line_items(id, name, subcontent_ids) VALUES (?, ?, ?)",
                   (id, name, sub_ids))
    conn.commit()
    return id


def is_bottom_line_item(content: Content):
    return content.sub_contents == []


def create_id(string):
    return uuid5(uuid.NAMESPACE_URL, string)


if __name__ == '__main__':
    contents = [
        Content(
            name="level 1",
            sub_contents=[Content(name="1.1", sub_contents=[]),
                          Content(name="1.2", sub_contents=[])]
        ),
        Content(
            name="level 2",
            sub_contents=[Content(name="2.1", sub_contents=[
                Content(name="2.1.1", sub_contents=[]),
            ]), ]
        )
    ]

    for content in contents:
        save(content)

    print(create_id("abc"))
