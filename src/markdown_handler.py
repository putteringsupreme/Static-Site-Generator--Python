from htmlnode import *

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

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    
    pass