import http
from textnode import TextType, TextNode
from htmlnode import HTMLNode, LeafNode, ParentNode

def main():
    Testerson = TextNode("Testing TextNode", TextType.BOLD, "this is a url")
    print(Testerson)
    

main()