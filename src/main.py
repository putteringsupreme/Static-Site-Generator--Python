import http
import os
import shutil
from textnode import TextType, TextNode
from htmlnode import HTMLNode, LeafNode, ParentNode
from markdown_handler import markdown_to_html_node, extract_title

#find current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
#go up one level to root of the project
root_dir = os.path.dirname(current_dir)
#static folder path
static_dir = os.path.join(root_dir, "static")
#public folder path
public_dir = os.path.join(root_dir, "public")
#content folder path
content_dir = os.path.join(root_dir, "content")
#html path
template_path = os.path.join(root_dir, "template.html")
#markdown file path, update the index.md file with your markdown, then run main.sh to generate a site
index_markdown_path = os.path.join(content_dir, "index.md")
#public html index path
public_index_html_path = os.path.join(public_dir, "index.html")


def main():
    recreate_public()
    
    copy_static_recursive(static_dir, public_dir)

    generate_pages_recursive(content_dir, template_path, public_dir)


def recreate_public():
    if os.path.exists(public_dir):
        shutil.rmtree(public_dir)
    os.mkdir(public_dir)

def copy_static_recursive(src_path, dst_path): #copy src folder contents into dst folder can be used for directories other than the "static" dir
    src_entries = os.listdir(src_path)

    for entry in src_entries:
        src_entry = os.path.join(src_path, entry) #this is the file or directory in the src folder
        dst_entry = os.path.join(dst_path, entry)

        if os.path.isfile(src_entry):
            shutil.copy(src_entry, dst_entry) #copy the file over if it is a file
        else: #if it is not a file this will create a directory in the dst folder and recurse the function
            os.mkdir(dst_entry)
            copy_static_recursive(src_entry, dst_entry)

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    with open(from_path, "r") as markdown_file:
        markdown = markdown_file.read()
    
    with open(template_path, "r") as template_file:
        template = template_file.read()
    
    title = extract_title(markdown)

    #create HTMLNodes and convert them into html strings
    html_content_nodes = markdown_to_html_node(markdown)
    html_content = html_content_nodes.to_html()


    #replace the placehodler {{ Title }} and {{ Content }} in our template string
    template = template.replace("{{ Title }}", title).replace("{{ Content }}", html_content)

    #write the new template stringinto the destination file
    with open(dest_path, "w") as dest_file:
        dest_file.write(template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    content_dir_list = os.listdir(dir_path_content)
    for item in content_dir_list:
        item_path = os.path.join(dir_path_content, item)        
        
        if item.endswith(".md") and os.path.isfile(item_path):
            
            # as an example, This would convert "/content/blog/majesty.md" to "/public/blog/majesty.html"
            rel_path = os.path.relpath(item_path, dir_path_content)  # Gets "blog/majesty.md"
            dest_file_path = os.path.join(dest_dir_path, rel_path)  # Joins with public dir
            dest_file_path = os.path.splitext(dest_file_path)[0] + ".html"  # Changes extension

            # Make sure the directory exists
            os.makedirs(os.path.dirname(dest_file_path), exist_ok=True)


            generate_page(item_path, template_path, dest_file_path)
        elif os.path.isdir(item_path):
            #create the corresponding directory in the public folder
            rel_dir_path = os.path.relpath(item_path, dir_path_content)
            dest_subdir_path = os.path.join(dest_dir_path, rel_dir_path)
            os.makedirs(dest_subdir_path, exist_ok=True)

            #recurse into directory
            generate_pages_recursive(item_path, template_path, dest_subdir_path)
        

    


main()