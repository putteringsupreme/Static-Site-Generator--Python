import re

def extract_markdown_images(text): #extracts image links and alt text into a list of paired tuples
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
   

def extraact_markdown_links(text): #extracts links and alt text into a list of paired tuples
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    