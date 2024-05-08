import dataclasses
import json
import sqlite3


@dataclasses.dataclass
class ContentLineItemEntity:
    id: str
    name: str
    sub_content_ids: list


def save_line_item(line_item: ContentLineItemEntity):
    print(f"saving {line_item}")
    with sqlite3.connect('contents.sqlite') as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO content_line_items(id, name, subcontent_ids) VALUES (?, ?, ?) ON CONFLICT (id) DO NOTHING",
            (line_item.id, line_item.name, json.dumps(line_item.sub_content_ids)))
        conn.commit()
    return line_item.id


def get_content_line_item_entity_by_id(content_root_id: str):
    print(f"getting {content_root_id}")
    with sqlite3.connect('contents.sqlite') as conn:
        cursor = conn.cursor()
        cursor.execute("select * from content_line_items where id = ?", (content_root_id,))
        row = cursor.fetchone()
        id, name, sub_content_ids_json = row
        content_line_item = ContentLineItemEntity(id, name, json.loads(sub_content_ids_json))
        return content_line_item
