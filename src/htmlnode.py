class HTMLNode():
    def __init__(self,tag=None, value=None, children=None, props=None):
        self.tag = tag #a string representing the HTML tag name (e.g. "p", "a", "h1", etc...)
        self.value = value #the text inside a paragraph/value of the html tag
        self.children = children #a list of HTMLNode objects representing the children of this node
        self.props = props #a dictionary of key-value pairs representing the attributes of the HTML tag. For example a link (<a> tag) might have a value {"https://so on and so forth"}

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")
    
    def props_to_html(self):
        if self.props == None:
            return ""
        att_string = ""
        for key, value in self.props.items():
            att_string += f' {key}="{value}"'
        
        return att_string
    
    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None , props)
    

    def to_html(self):
        if self.value == None:
            raise ValueError("Invalid HTML: no value")
        if self.tag == None:
            return self.value
        if self.props == None:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode(tag={self.tag}, value={self.value}, props={self.props})"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None,children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("Invalid HTML: no tag")
        if self.children == None:
            raise ValueError("Invalid HTML: no children")
        
        result = f"<{self.tag}{self.props_to_html()}>"
        
        for child in self.children:
            result += child.to_html()
        return f"{result}</{self.tag}>"
        