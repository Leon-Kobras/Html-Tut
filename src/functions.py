from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType
import re
from block import BlockType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    nodes = []
    for old in old_nodes:
        if old.text_type.value != "text":
            nodes.append(old)
            continue
        spliton = []
        sections = old.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(0, len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                spliton.append(TextNode(sections[i], TextType.TEXT))
            else:
                spliton.append(TextNode(sections[i], text_type))
        nodes.extend(spliton)
    return nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_image(old_nodes):
    nodes = []
    for old in old_nodes:
        if old.text_type.value != "text":
            nodes.append(old)
            continue
        lines = extract_markdown_images(old.text)
        normal = []
        lext = old.text
        node = []
        if len(lines) == 0:
            nodes.append(old)
            continue
        for line in lines:
            node = lext.split(f"![{line[0]}]({line[1]})")
            normal.append(node[0])
            if len(node) > 1:
                lext = node[1]
        for i in range(0, len(lines)):
            node1 = TextNode(normal[i], TextType.TEXT)
            node2 = TextNode(lines[i][0], TextType.IMAGE, lines[i][1])
            nodes.append(node1)
            nodes.append(node2)
        if len(node) > len(lines):
            node3 = TextNode(node[-1], TextType.TEXT)
            nodes.append(node3)
    return nodes

def split_nodes_link(old_nodes):
    nodes = []
    for old in old_nodes:
        if old.text_type.value != "text":
            nodes.append(old)
            continue
        lines = extract_markdown_links(old.text)
        normal = []
        lext = old.text
        if len(lines) == 0:
            nodes.append(old)
            continue
        node = []
        for line in lines:
            node = lext.split(f"[{line[0]}]({line[1]})")
            normal.append(node[0])
            if len(node) > 1:
                lext = node[1]
        for i in range(0, len(lines)):
            node1 = TextNode(normal[i], TextType.TEXT)
            node2 = TextNode(lines[i][0], TextType.LINK, lines[i][1])
            nodes.append(node1)
            nodes.append(node2)
        node3 = None
        if node[-1] != "" and len(node) > len(lines):
            node3 = TextNode(node[-1], TextType.TEXT)
            nodes.append(node3)
    return nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def markdown_to_blocks(markdown):
    docs = markdown.strip("\n\n")
    doc = docs.split("\n\n")
    docd = ""
    newdoc = []
    for dod in doc:
        docd = dod.strip()
        newdoc.append(docd)
    return newdoc

def block_to_block_type(doc):
        if doc.startswith("#"):
            return BlockType.HEADING.value
        elif doc.startswith("```\n") and doc.endswith("```"):
            return BlockType.CODE.value
        elif doc.startswith(">"):
            return BlockType.QUOTE.value
        elif doc.startswith("-"):
            return BlockType.UNORDERED_LIST.value
        elif doc[0].isdigit():
            if doc[1:].startswith(". "):
                return BlockType.ORDERED_LIST.value
        else:
            return BlockType.PARAGRAPH.value

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    hode = []
    counter = 1
    ham = "h" + str(counter)
    for block in blocks:
        kind = block_to_block_type(block)
        if kind == "heading":
            bloc = block.lstrip("# ")
            yell = hellto(bloc)
            node = ParentNode(ham, yell)
            hode.append(node)
            if node == LeafNode(ham, bloc):
                counter += 1
                ham = "h" + str(counter)
            continue
        elif kind == "quote":
            bloc = block.lstrip("> ")
            yell = hellto(bloc)
            node = ParentNode("blockquote", yell)
            hode.append(node)
            continue
        elif kind == "code":
            childs = []
            bloc = block.strip("```")
            child = LeafNode("code", bloc)
            childs.append(child)
            node = ParentNode("pre", childs)
            hode.append(node)
            continue
        elif kind == "unordered_list":
            bloc = block.lstrip("- ")
            blo = bloc.split("\n- ")
            childs = []
            child = None
            for bl in blo:
                yell = hellto(bl)
                child = ParentNode("li", yell)
                childs.append(child)
            node = ParentNode("ul", childs)
            hode.append(node)
            continue
        elif kind == "ordered_list":
            bloc = block.split("\n")
            childs = []
            child = None
            for blo in bloc:
                bl = blo[3:]
                yell = hellto(bl)
                child = ParentNode("li", yell)
                childs.append(child)
            node = ParentNode("ol", childs)
            hode.append(node)
            continue
        elif kind == "paragraph":
            bloc = block.replace("\n", " ")
            yell = hellto(bloc)
            node = ParentNode("p", yell)
            hode.append(node)
            continue
    div = ParentNode("div", hode)
    return div

def hellto(text):
    hell = []
    yell = []
    shell = text_to_textnodes(text)
    hell.extend(shell)
    for hill in hell:
        childnode = hill.text_node_to_html_node()
        yell.append(childnode)
    return yell
