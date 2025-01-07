class HTMLNode():
    def __init__(self,tag=None, value=None, children=None, props=None):
        self.tag = tag #a string representing the HTML tag name (e.g. "p", "a", "h1", etc...)
        self.value = value #the text inside a paragraph/value of the html tag
        self.children = children #a list of HTMLNode objects representing the children of this node
        self.props = props #a dictionary of key-value pairs representing the attributes of the HTML tag. For example a link (<a> tag) might have a value {"https://so on and so forth"}

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        att_string = ""
        for key, value in self.props.items():
            att_string += f' {key}="{value}"'
        
        return att_string
    
    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"