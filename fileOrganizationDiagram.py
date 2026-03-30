import os

def should_exclude(item):
    # Add more conditions if needed to exclude other files or directories
    return item.startswith('.') or item == '__pycache__'

def generate_file_tree(directory, indent=0):
    items = sorted(os.listdir(directory))
    for item in items:
        if should_exclude(item):
            continue
        
        item_path = os.path.join(directory, item)
        if os.path.isdir(item_path):
            print('    ' * indent + f'📁 {item}')
            generate_file_tree(item_path, indent + 1)
        else:
            print('    ' * indent + f'📄 {item}')

if __name__ == "__main__":
    root_directory = os.path.dirname(os.path.abspath(__file__))
    print(f'📂 {root_directory}')
    generate_file_tree(root_directory)
