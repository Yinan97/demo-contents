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


if __name__ == '__main__':
    contents_v1 = [
        Content(
            name="content_root",
            sub_contents=[
                Content(
                    name="level 1",
                    sub_contents=[
                        Content(name="1.1", sub_contents=[]),
                        Content(name="1.2", sub_contents=[])
                    ]
                ),
                Content(
                    name="level 2",
                    sub_contents=[Content(name="2.1", sub_contents=[
                        Content(name="2.1.1", sub_contents=[]),
                    ])]
                )
            ]
        )
    ]

    for content in contents_v1:
        save_content(content)

    print("--------------------")

    contents_v2 = [
        Content(
            name="content_root",
            sub_contents=[
                Content(
                    name="level 1",
                    sub_contents=[
                        Content(name="1.1", sub_contents=[]),
                    ]
                ),
                Content(
                    name="level 2",
                    sub_contents=[Content(name="2.1", sub_contents=[
                        Content(name="2.1.1", sub_contents=[]),
                    ]), ]
                )
            ]
        )
    ]

    for content in contents_v2:
        save_content(content)

    empty_content = [Content(name="content_root", sub_contents=[])]
    for content in empty_content:
        save_content(content)
