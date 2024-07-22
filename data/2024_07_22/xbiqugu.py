import asyncio
import aiohttp
from bs4 import BeautifulSoup

async def fetch(session, url):
    try:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.text()
            else:
                print(f"Failed to fetch {url}: HTTP status {response.status}")
                return None
    except aiohttp.client_exceptions.InvalidURL:
        print(f"Invalid URL: {url}")
        return None
    except aiohttp.client_exceptions.ClientConnectorError:
        print(f"Failed to connect to {url}")
        return None
    except Exception as e:
        print(f"An error occurred while fetching {url}: {e}")
        return None

async def fetch_chapters(base_url, novel_url):
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, novel_url)
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            chapter_links = soup.select('div#list dl dd a')
            return [(base_url + link['href'], link.text) for link in chapter_links]
        else:
            return []

async def fetch_chapter_content(session, chapter_url):
    html = await fetch(session, chapter_url)
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        content = soup.select_one('div#content').get_text(separator='\n', strip=True)
        return content
    else:
        return ""

async def main():
    base_url = "http://www.xbiqugu.net"
    novel_url = "http://www.xbiqugu.net/118/118920/"
    output_file = "大秦逮捕方士，关我炼气士什么事.txt"

    async with aiohttp.ClientSession() as session:
        # 获取章节列表
        chapters = await fetch_chapters(base_url, novel_url)
        if not chapters:
            print("Failed to fetch chapter list.")
            return

        with open(output_file, 'w', encoding='utf-8') as f:
            for chapter_url, chapter_title in chapters:
                print(f"Fetching content for {chapter_title}...")

                # 获取章节内容
                content = await fetch_chapter_content(session, chapter_url)
                if content:
                    f.write(f"{chapter_title}\n")
                    f.write(f"{content}\n\n")
                    print(f"Saved content for {chapter_title}")
                else:
                    print(f"Failed to fetch content for {chapter_title}")

        print(f"All chapters have been saved to {output_file}")

# 运行爬虫
asyncio.run(main())
