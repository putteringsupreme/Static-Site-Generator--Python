import http
import os
import shutil
from textnode import TextType, TextNode
from htmlnode import HTMLNode, LeafNode, ParentNode

#find current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
#go up one level to root of the project
root_dir = os.path.dirname(current_dir)
#static folder path
static_dir = os.path.join(root_dir, "static")
#public folder path
public_dir = os.path.join(root_dir, "public")

def main():
    recreate_public()
    copy_static_recursive(static_dir, public_dir)
    

def recreate_public():
    if os.path.exists(public_dir):
        shutil.rmtree(public_dir)
    os.mkdir(public_dir)

def copy_static_recursive(src_path, dst_path): #copy src folder contents into dst folder
    src_entries = os.listdir(src_path)

    for entry in src_entries:
        src_entry = os.path.join(src_path, entry) #this is the file or directory in the src folder
        dst_entry = os.path.join(dst_path, entry)

        if os.path.isfile(src_entry):
            shutil.copy(src_entry, dst_entry) #copy the file over if it is a file
        else: #if it is not a file this will create a directory in the dst folder and recurse the function
            os.mkdir(dst_entry)
            copy_static_recursive(src_entry, dst_entry)

main()