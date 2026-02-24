import os
import shutil
from functions import *

def copier(source, destination, counter=0):
    abssource = os.path.abspath(source)
    absdestin = os.path.abspath(destination)
    filenames = os.listdir(abssource)
    dames = os.listdir(absdestin)
    if counter == 0:
        for dame in dames:
            joined = os.path.normpath(os.path.join(absdestin, dame))
            if os.path.isfile(joined) == True:
                os.remove(joined)
            else:
                shutil.rmtree(joined)
    counter = counter + 1
    for filename in filenames:
        path = os.path.normpath(os.path.join(abssource, filename))
        joined = os.path.normpath(os.path.join(absdestin, filename))
        if os.path.isfile(path) == True:
            shutil.copy(path, joined)
        else:
            joiner = os.path.normpath(os.path.join(source, filename))
            joinee = os.path.normpath(os.path.join(destination, filename))
            os.mkdir(joined)
            copier(joiner, joinee, counter)

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block.startswith("#"):
            bloc = block.lstrip("# ")
            return bloc
    raise Exception("No headings found")

def generate_page(from_path, template_path, dest_path):
    print("Generating page from {from_path} to {dest_path} using {template_path}")
    absfrom_path = os.path.abspath(from_path)
    abstemplate_path = os.path.abspath(template_path)
    f = open(absfrom_path)
    markdown = f.read()
    g = open(abstemplate_path)
    template = g.read()
    marked = markdown_to_html_node(markdown)
    content = marked.to_html()
    Title = extract_title(markdown)
    templated = template.replace("{{ Title }}", f"{Title}")
    templated = templated.replace("{{ Content }}", f"{content}")
    if os.path.exists(dest_path) == False:
        directories = os.path.dirname(dest_path)
        os.makedirs(directories, exist_ok=True)
        with open(dest_path, "w") as s:
            s.write(templated)
    else:
        with open(dest_path, "w") as s:
            s.write(templated)

def generate_pages_recursive(directory, template_path, dest_dir_path):
    filesname = os.listdir(directory)
    for filename in filesname:
        if os.path.isfile(os.path.join(directory, filename)) == True:
            joined = os.path.join(dest_dir_path, filename)
            root, _ext = os.path.splitext(joined)
            if _ext == ".md":
                new_path = root + ".html"
                generate_page(os.path.join(directory, filename), template_path, new_path)
        else:
            generate_pages_recursive(os.path.join(directory, filename), template_path, os.path.join(dest_dir_path, filename))

