from Content import Content
from ContentService import save_content, read_content_by_id

if __name__ == '__main__':
    contents_v1 = \
        Content(name="content_root", sub_contents=[
            Content(name="level 1", sub_contents=[
                Content(name="1.1", sub_contents=[]),
                Content(name="1.2", sub_contents=[])]),
            Content(name="level 2", sub_contents=[
                Content(name="2.1", sub_contents=[
                    Content(name="2.1.1", sub_contents=[]), ])])])

    contents_v1_id = save_content(contents_v1)
    read_content_v1 = read_content_by_id(contents_v1_id)
    print(read_content_v1)

    contents_v2 = \
        Content(name="content_root", sub_contents=[
            Content(name="level 1", sub_contents=[
                Content(name="1.1", sub_contents=[]), ]),
                # Content(name="1.2", sub_contents=[])]) is deleted
            Content(name="level 2", sub_contents=[
                Content(name="2.1", sub_contents=[
                    Content(name="2.1.1", sub_contents=[]), ]), ])])
    contents_v2_id = save_content(contents_v2)
    read_content_v2 = read_content_by_id(contents_v2_id)
    print(read_content_v2)

# v1 read from db
Content(id='dd65c30b-558a-55af-b873-66781f3ab9ed', name='content_root', sub_contents=[
    Content(id='4e37e2e9-a672-5c5f-ae66-6880d4d6bbb9', name='level 1', sub_contents=[
        Content(id='b9a72b5c-6995-5129-9bd8-fd790354dbf8', name='1.1', sub_contents=[]),
        Content(id='e051e297-6e85-5890-ab60-68b15278870e', name='1.2', sub_contents=[])]),
    Content(id='30861b20-4096-57f1-95cc-72c5d8837569', name='level 2', sub_contents=[
        Content(id='07b9983d-7b87-5ee2-8281-e414425c4b28', name='2.1', sub_contents=[
            Content(id='ccb4cd7d-9a7c-5fdb-9ba1-4ef4de6e166a', name='2.1.1', sub_contents=[])])])])
# v2 read from db
Content(id='58d6778d-1222-5fc2-9877-2641c19c68a7', name='content_root', sub_contents=[
    Content(id='57aae1de-5cea-50ec-a9ba-fc6ca1cb826b', name='level 1', sub_contents=[
        Content(id='b9a72b5c-6995-5129-9bd8-fd790354dbf8', name='1.1', sub_contents=[])]),
        #   line with name `1.2` is gone
    Content(id='30861b20-4096-57f1-95cc-72c5d8837569', name='level 2', sub_contents=[
        Content(id='07b9983d-7b87-5ee2-8281-e414425c4b28', name='2.1', sub_contents=[
            Content(id='ccb4cd7d-9a7c-5fdb-9ba1-4ef4de6e166a', name='2.1.1', sub_contents=[])])])])
