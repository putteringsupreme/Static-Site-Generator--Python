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
   

def extract_markdown_links(text): #extracts links and alt text into a list of paired tuples
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    result = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            result.append(old_node)
            continue
        text = old_node.text
        image_tuples = extract_markdown_images(text)    
        if not image_tuples:
            result.append(TextNode(text, TextType.TEXT))
            continue
        
        for alt, url in image_tuples:
            image_markdown = f"![{alt}]({url})"
            sections = text.split(image_markdown, 1)

            if sections[0]:
                result.append(TextNode(sections[0], TextType.TEXT))

            result.append(TextNode(alt, TextType.IMAGE, url))   

            text = sections[1]
        if text:
            result.append(TextNode(text, TextType.TEXT))
                
    return result

def split_nodes_link(old_nodes):
    result = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            result.append(old_node)
            continue
    
        text = old_node.text
        link_tuples = extract_markdown_links(text)    
        if not link_tuples:
            result.append(TextNode(text, TextType.TEXT))
            continue
        
        for alt, url in link_tuples:
            link_markdown = f"[{alt}]({url})"
            sections = text.split(link_markdown, 1)

            if sections[0]:
                result.append(TextNode(sections[0], TextType.TEXT))

            result.append(TextNode(alt, TextType.LINK, url))   

            text = sections[1]
        if text:
            result.append(TextNode(text, TextType.TEXT))
                
    return result

def text_to_textnodes(text): #takes a string of markdown and returns a list of textnodes in order
    nodes = [TextNode(text, TextType.TEXT)]

    image_split = split_nodes_image(nodes)

    link_split = split_nodes_link(image_split)

    bold_split = split_nodes_delimiter(link_split, "**", TextType.BOLD)

    italics_split = split_nodes_delimiter(bold_split, "*", TextType.ITALIC)

    code_split = split_nodes_delimiter(italics_split, "`", TextType.CODE)

    return code_split