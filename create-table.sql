create table if not exists content_line_items(
    id char(36) primary key,
    name text,
    subcontent_ids json default('[]')
);
