import requests

# GitHub API 的基本 URL
repo_url = "https://api.github.com/repos/hjpwyb/tvbox6/contents"

def find_files(file_types, url):
    files = []
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    
    for item in data:
        if item['type'] == 'file' and item['name'].endswith(tuple(file_types)):
            files.append(item['download_url'])
        elif item['type'] == 'dir':
            files.extend(find_files(file_types, item['url']))
    
    return files

# 获取 JSON 和 TXT 文件
file_types = ['.json', '.txt']
files = find_files(file_types, repo_url)

# 生成新的 JSON 文件
import json

output_data = [{'url': file} for file in files]
with open('all_files.json', 'w') as f:
    json.dump(output_data, f, indent=4)

print(f"总共找到 {len(files)} 个文件。文件已保存为 all_files.json")
