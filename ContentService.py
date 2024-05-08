import uuid
from uuid import uuid5

from Content import Content
from ContentLineItemEntity import save_line_item, get_content_line_item_entity_by_id, ContentLineItemEntity


def save_content(content: Content):
    if is_bottom_line_item(content):
        sub_content_ids = []
        line_id = create_id(content.name)
    else:
        sub_content_ids = list(map(save_content, content.sub_contents))
        line_id = create_id(content.name, sub_content_ids)

    line_item_entity = ContentLineItemEntity(
        id=line_id,
        name=content.name,
        sub_content_ids=sub_content_ids)

    id = save_line_item(line_item_entity)
    return id


def read_content_by_id(content_root_id: str):
    root_line_item = get_content_line_item_entity_by_id(content_root_id)
    content_from_root = Content.from_entity(root_line_item)
    return content_from_root


def is_bottom_line_item(content: Content):
    return content.sub_contents == []


def create_id(string, sub_content_ids=[]):
    if sub_content_ids == []:
        return str(uuid5(uuid.NAMESPACE_URL, string))
    else:
        return str(uuid5(uuid.NAMESPACE_URL, string + "|".join(sub_content_ids)))
