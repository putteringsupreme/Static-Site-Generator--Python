from htmlnode import *
from textnode import *

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks

def block_to_block_type(markdown_block): #takes a single block(string) of markdown text as input, returns the type as a string
    lines = markdown_block.split("\n")
    if markdown_block.startswith("# ") or markdown_block.startswith("## ") or markdown_block.startswith("### ") or markdown_block.startswith("#### ") or markdown_block.startswith("##### ") or markdown_block.startswith("###### "):
        return "heading"
    
    elif markdown_block.startswith("```") and markdown_block.endswith("```"):
        return "code"
    
    elif all(line.strip().startswith(">") for line in lines):
        return "quote"
    
    elif markdown_block.startswith("* ") or markdown_block.startswith("- "):
        return "unordered_list"
    
    elif markdown_block.strip().startswith("1. "):
        if all(lines[i].strip().startswith(f"{i+1}. ") for i in range(len(lines))):
            return "ordered_list"
    
    else:
        return "paragraph"

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode("img", text_node.text , {"src": text_node.url})
    else:
        raise ValueError(f"Invalid text type: {text_node.text_type}")    

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in text_nodes]
    

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    parent_node = ParentNode("div", [])
    block_nodes = []
    parent_node.children = block_nodes

    for block in blocks:
        match block_to_block_type(block):
            
            case "heading":
                level = len(block) - len(block.lstrip("#"))  # Count the # symbols
                text = block.lstrip("# ")  # Get the text after the # symbols
                children = text_to_children(text)
                heading_node = ParentNode(f"h{level}", children)


                block_nodes.append(heading_node)

            case "paragraph":
                lines =  block.split('\n')
                text = " ".join(lines)
                children = text_to_children(text)
                paragraph_node = ParentNode("p", children)

                block_nodes.append(paragraph_node)

            case "code":
               
                lines = block.split('\n')
               
                code_content = '\n'.join(lines[1:-1])  # skip first and last lines
               
                code_node = LeafNode("code", code_content)
               
                pre_node = ParentNode("pre", [code_node])
               
                block_nodes.append(pre_node)


            case "quote":
                
                lines = block.split("\n")
                new_lines = []
                for line in lines:
                    if not line.startswith(">"):
                        raise ValueError("invalid quote block")
                    new_lines.append(line.lstrip(">").strip())
                content = " ".join(new_lines)
                children = text_to_children(content)
                quote_node = ParentNode("blockquote", children)

                block_nodes.append(quote_node)

            case "unordered_list":
                lines = block.split('\n')
                list_items = []
                for line in lines:
                    line = line.strip()  # remove leading/trailing whitespace
                    line = line[1:]      # remove first character (bullet point)
                    line = line.strip()  # remove any remaining whitespace
                    children = text_to_children(line)
                    item_node = ParentNode("li", children)
                    list_items.append(item_node)
                
                list_node = ParentNode("ul", list_items)
                block_nodes.append(list_node)

            case "ordered_list":
                lines = block.split('\n')
                list_items = []
                for line in lines:
                    line = line.strip() 
                    line = line.split(".", 1)     
                    line = line[1].strip()
                    children = text_to_children(line)
                    item_node = ParentNode("li", children)
                    list_items.append(item_node)
                
                list_node = ParentNode("ol", list_items)
                block_nodes.append(list_node)



    return parent_node


def extract_title(markdown): 
    # takes a string from the markdown file "# " from the markdown file. ie. extract_title("# Hello") should return "Hello"
    lines = markdown.split("\n")
    
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    
    raise Exception("Improper Markdown: No h1 header found")
