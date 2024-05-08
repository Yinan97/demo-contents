import dataclasses

from ContentLineItemEntity import ContentLineItemEntity, get_content_line_item_entity_by_id, save_line_item


@dataclasses.dataclass
class Content:
    id: str
    name: str
    sub_contents: list

    def __init__(self, name, sub_contents, id=None):
        self.id = id
        self.name = name
        self.sub_contents = sub_contents

    @staticmethod
    def from_entity(content_line_item_entity: ContentLineItemEntity):
        if content_line_item_entity.sub_content_ids is None:
            sub_contents = []
        else:
            sub_content_line_items = list(
                map(get_content_line_item_entity_by_id, content_line_item_entity.sub_content_ids))
            sub_contents = list(map(Content.from_entity, sub_content_line_items))
        return Content(
            id=content_line_item_entity.id,
            name=content_line_item_entity.name,
            sub_contents=sub_contents
        )

    # todo cyclic reference error!
    # def to_entity(self):
    #     if is_bottom_line_item(self):
    #         sub_content_ids = []
    #         line_id = create_id(self.name)
    #     else:
    #         sub_content_ids = list(map(ContentService.save_content, self.sub_contents))
    #         line_id = create_id(self.name, sub_content_ids)
    #
    #     line_item_entity = ContentLineItemEntity(
    #         id=line_id,
    #         name=self.name,
    #         sub_content_ids=sub_content_ids)
    #     return line_item_entity


