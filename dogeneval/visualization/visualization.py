from anytree import Node, RenderTree
import os
import matplotlib.pyplot as plt

def build_tree_with_size(path):
    # 创建根节点
    root = Node(path, size=get_folder_size(path))
    stack = [root]

    while stack:
        current_node = stack.pop()
        try:
            for item in os.listdir(current_node.name):
                item_path = os.path.join(current_node.name, item)
                if os.path.isdir(item_path):
                    child_node = Node(item_path, parent=current_node, size=get_folder_size(item_path))
                    stack.append(child_node)
        except PermissionError:
            pass

    return root

def get_folder_size(path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

# 构建层级树
root_path = '/home/junetheriver/datasets/huawei/processed/UNC_20.9.5'
root_node = build_tree_with_size(root_path)

# 可视化层级结构和文件夹大小
def plot_tree(node, depth=0):
    plt.barh(node.name, node.size, color='skyblue')
    for child in node.children:
        plot_tree(child, depth+1)

plt.figure(figsize=(10, 8))
plot_tree(root_node)
plt.xlabel('Folder Size (bytes)')
plt.ylabel('Folder Hierarchy')
plt.title('Folder Structure with Size')
plt.savefig('folder_structure.png')
