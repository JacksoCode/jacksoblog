from enum import Enum


class BlockType(Enum):
    PARAGRAGH = "paragragh"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"


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


def block_to_block_type(blocks):
    new_block_list = []
    for block in blocks:
        buffer_list = []
        ind = 0
        if (
            block[ind] == "#"
            and "# " in block
            and block.count("#") >= 1
            and block.count("#") <= 6
        ):
            buffer_list.append((block, BlockType.HEADING))
        elif block[:3] == "```" and block[-3:] == "```":
            buffer_list.append((block, BlockType.CODE))
        elif block[ind] == ">" and block[ind + 1] == " ":
            buffer_list.append((block, BlockType.QUOTE))
        elif block[ind] == "-" and block[ind + 1] == " ":
            lines = block.split("\n")
            line_bool = True
            for line in lines:
                i = 0
                while i < len(line) and line[i] == "-":
                    i += 1
                    if i + 1 < len(line) and line[i] == " ":
                        line_bool = True
                    else:
                        line_bool = False
            if line_bool:
                buffer_list.append((block, BlockType.UNORDERED_LIST))
            else:
                buffer_list.append((block, BlockType.PARAGRAGH))
        elif block[0].isdigit():
            lines = block.split("\n")
            counter = 1
            line_bool = True
            for line in lines:
                i = 0
                while i < len(line) and line[i].isdigit():
                    i += 1
                    if i + 1 < len(line) and line[i] == "." and line[i + 1] == " ":
                        char_to_int = int(line[0:i])
                        if char_to_int != counter:
                            line_bool = False
                        if char_to_int == counter:
                            counter += 1
                    else:
                        line_bool = False
            if line_bool:
                buffer_list.append((block, BlockType.ORDERED_LIST))
            else:
                buffer_list.append((block, BlockType.PARAGRAGH))
        else:
            buffer_list.append((block, BlockType.PARAGRAGH))
        new_block_list.extend(buffer_list)
    return new_block_list
