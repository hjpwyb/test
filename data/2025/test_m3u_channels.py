import aiohttp
import asyncio

# 从本地文件读取并解析 M3U 文件
def read_m3u_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    return content

# 提取频道 URL
def parse_m3u_content(content):
    urls = []
    for line in content.splitlines():
        if line.startswith('http'):
            urls.append(line.strip())
    return urls

# 测试频道 URL 是否可访问
async def test_url(session, url):
    try:
        async with session.get(url, timeout=10) as response:
            if response.status == 200:
                return url, True
            else:
                return url, False
    except Exception as e:
        return url, False

# 主程序
async def main():
    file_path = "435.m3u"  # 本地 M3U 文件路径
    m3u_content = read_m3u_file(file_path)

    if not m3u_content:
        print("Failed to read M3U file.")
        return

    urls = parse_m3u_content(m3u_content)
    if not urls:
        print("No URLs found in M3U file.")
        return

    async with aiohttp.ClientSession() as session:
        tasks = [test_url(session, url) for url in urls]
        results = await asyncio.gather(*tasks)

    accessible_channels = [url for url, is_accessible in results if is_accessible]
    inaccessible_channels = [url for url, is_accessible in results if not is_accessible]

    print(f"Total channels: {len(urls)}")
    print(f"Accessible channels: {len(accessible_channels)}")
    print(f"Inaccessible channels: {len(inaccessible_channels)}")

    if accessible_channels:
        print("\nAccessible channels:")
        for url in accessible_channels:
            print(url)

    if inaccessible_channels:
        print("\nInaccessible channels:")
        for url in inaccessible_channels:
            print(url)

# 运行程序
asyncio.run(main())
