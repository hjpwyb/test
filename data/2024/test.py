import re

# 定义输入文件名和输出文件名
input_file = '/volume1/docker/python_scripts/bbb/JB/aaa/ITV109.m3u'  # 替换为你的M3U文件的实际路径
output_files = {
    '易视腾': '/volume1/docker/python_scripts/bbb/JB/aaa/output_易视腾.m3u',
    '华数': '/volume1/docker/python_scripts/bbb/JB/aaa/output_华数.m3u',
    '百视通': '/volume1/docker/python_scripts/bbb/JB/aaa/output_百视通.m3u'
}

# 打开输入文件并读取内容
with open(input_file, 'r', encoding='utf-8') as file:
    lines = file.readlines()

# 初始化输出文件内容
output_contents = {key: [] for key in output_files.keys()}

# 遍历每一行，根据结尾文字分类
for i in range(len(lines)):
    line = lines[i].strip()
    if line.startswith('#EXTINF'):
        # 检查下一行是否为链接
        if i + 1 < len(lines) and lines[i + 1].strip().startswith('http'):
            link_line = lines[i + 1].strip()
            # 检查结尾文字
            if '易视腾' in link_line:
                output_contents['易视腾'].append(line + '\n')
                output_contents['易视腾'].append(link_line + '\n')
            elif '华数' in link_line:
                output_contents['华数'].append(line + '\n')
                output_contents['华数'].append(link_line + '\n')
            elif '百视通' in link_line:
                output_contents['百视通'].append(line + '\n')
                output_contents['百视通'].append(link_line + '\n')
            else:
                # 如果没有结尾文字，则复制到所有文件
                for key in output_contents.keys():
                    output_contents[key].append(line + '\n')
                    output_contents[key].append(link_line + '\n')

# 写入到输出文件
for key, content in output_contents.items():
    with open(output_files[key], 'w', encoding='utf-8') as file:
        file.writelines(content)

print("处理完成！生成了以下文件：")
for file in output_files.values():
    print(file)