import re
from enum import Enum

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode():
    def __init__(self, text, text_type, url = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return(
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
            )
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def extract_markdown_images(text): #extracts image links and alt text into a list of paired tuples
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
   

def extraact_markdown_links(text): #extracts links and alt text into a list of paired tuples
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    split_texts = []
    new_nodes = []
    text_texts = []
    for node in old_nodes:
        list_text = re.split( r"[\[\]\(\)]", node.text)
        for i in range(len(list_text)):
            if list_text[i] != '':
                split_texts.append(list_text[i])
                continue
        for i in range(len(split_texts)):
            if i == 0 or i % 3 == 0:
                text_texts.append(split_texts[i])
                continue
    
    if len(split_texts) % 3 != 0:
        raise ValueError("Invalid markdown, formatted section not closed or no alt text provided")
    
    return new_nodes

def split_nodes_link(old_nodes):
    pass