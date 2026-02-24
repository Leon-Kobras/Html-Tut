def main():
    import os
    import sys
    from textnode import TextNode, TextType
    from htmlnode import HTMLNode, LeafNode
    from functions import split_nodes_delimiter, block_to_block_type, markdown_to_blocks, markdown_to_html_node
    from functions import extract_markdown_images, split_nodes_image, text_to_textnodes, split_nodes_link
    from block import BlockType
    from functions2 import copier, extract_title, generate_page, generate_pages_recursive
    Nod = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    Hod = HTMLNode("a", "Click", None, {"href": "https://www.google.com"})
    node = TextNode(
        "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)",
        TextType.TEXT,
    )
    mode = split_nodes_delimiter([node], "**", TextType.BOLD)
    new_nodes = split_nodes_link([node])
    text = "# Test\n\nHere's the deal, **I like Tolkien**."

    nope = markdown_to_html_node(text)
    nodes = text_to_textnodes(text)
    block = markdown_to_blocks(text)
    lock = markdown_to_html_node(text)
    hock = block_to_block_type("# This is a heading")
    generate_pages_recursive("content", "template.html", "docs")
    basepath = "/"
    if sys.argv[0] != "":
        basepath = sys.argv[0]
if __name__ == "__main__":
    main()
