def markdown_to_blocks(markdown):
    delimiter = "\n\n"
    block_list = []
    split_mark = markdown.split(delimiter)
    for mark in split_mark:
        buffer_list = []
        strip_mark = mark.strip()
        buffer_list.append(strip_mark)
        filter_buffer = [item for item in buffer_list if item != ""]
        block_list.extend(filter_buffer)
    return block_list
