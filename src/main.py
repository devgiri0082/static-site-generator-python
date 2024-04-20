import os
import shutil
from textnode import TextNode
from utils import Utils

def remove_everything(dir: str, cur:str = ""):
    if os.path.exists(dir) == False:
        return
    files = os.listdir(os.path.join(dir, cur))
    for file in files:
        file_address = os.path.join(dir, cur, file)
        if os.path.isdir(file_address) == True:
            remove_everything(dir=dir, cur=file)
            os.rmdir(file_address)
        else:
            os.remove(file_address)

def copy_directory(from_dir: str, to_dir: str):
    if os.path.exists(from_dir)  == False:
        raise ValueError("Unable to open from directory")
    if os.path.exists(to_dir) == False:
        os.mkdir(to_dir)
    start_copy(from_dir=from_dir, to_dir=to_dir, cur_path="")

def start_copy(from_dir: str, to_dir: str, cur_path: str = ""):
    files = os.listdir(os.path.join(from_dir, cur_path))
    for file in files:
        isdir = os.path.isdir(os.path.join(from_dir, cur_path, file))
        if isdir == True:
            os.mkdir(os.path.join(to_dir, cur_path, file))
            start_copy(from_dir=from_dir, to_dir=to_dir, cur_path=os.path.join(cur_path, file))
        else:
            shutil.copy(dst=os.path.join(to_dir, cur_path), src=os.path.join(from_dir, cur_path, file))

def generate_pages_recursive(dir_path_content: str, template_path: str, des_dir_path: str, cur_path: str = ""):
    contents = os.listdir(os.path.join(dir_path_content, cur_path))

    for dir in contents:
        path = os.path.join(dir_path_content, cur_path, dir)
        if os.path.isdir(path) == True:
            generate_pages_recursive(dir_path_content=dir_path_content, template_path=template_path, des_dir_path=des_dir_path, cur_path=dir)
        else:
            print(dir)
            if dir.split(".")[1] == "md":
                generate_page(from_path=os.path.join(dir_path_content, cur_path), file_name=dir, dest_path=os.path.join(des_dir_path, cur_path), template_path=template_path)


def generate_page(from_path: str, file_name: str, template_path: str, dest_path:str):
    print(f"Generating page from {os.path.join(dest_path,file_name)} using {template_path}")
    markdown: str = ""
    template : str = ""
    with open(file=os.path.join(from_path, file_name), mode="r") as f:
        markdown = f.read()
    with open(file=template_path, mode="r") as f:
       template = f.read()
    html = Utils.markdown_to_html_node(markdown=markdown).to_html()
    title = Utils.extract_title(markdown=markdown)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    if os.path.exists(dest_path) == False:
        os.mkdir(dest_path)
    with open (os.path.join(dest_path, f"{file_name.split(".")[0]}.html"), "w") as f:
        f.write(template)


if __name__ == "__main__":
    remove_everything(dir="public")
    copy_directory(from_dir="static", to_dir="public")
    # generate_page(from_path="content", file_name="index.md", template_path="template.html", dest_path="public")
    generate_pages_recursive(dir_path_content="content", des_dir_path="public", template_path="template.html")
