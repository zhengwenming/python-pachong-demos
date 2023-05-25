import os.path
import requests
from lxml import etree

headers = {
    'cookie': 'Hm_lpvt_86200d30c9967d7eda64933a74748bac=1685030963; Hm_lvt_86200d30c9967d7eda64933a74748bac=1685026440',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) '
                  'Version/16.5 Safari/605.1.15'
}

# 爬取一组图片
url = 'https://mm.enterdesk.com/bizhi/64629.html'


def get_one_set(url_str):
    res = requests.get(url=url_str, headers=headers)
    html = etree.HTML(res.text)
    links = html.xpath('//div[@class="arc_pandn"]//a/@src')
    titles = html.xpath('//div[@class="arc_pandn"]//img/@title')
    folder_name = titles[0]

    if not os.path.exists(f'{folder_name}'):
        os.mkdir(f'{folder_name}')
    for num, link in enumerate(links):
        num += 1
        pic_content = requests.get(link, headers=headers)
        with open(f'{folder_name}/{folder_name}_{num}.jpg', 'wb') as f:
            f.write(pic_content)
            print(f'已下载..{folder_name}...第{num}张图片')

        print(link)


# 爬取一页图片
def get_one_group(index_url):
    res = requests.get(index_url, headers=headers)
    html = etree.HTML(res.text)
    links = html.xpath('//dl[@class="egeli_pic_dl"]/dd/a/@href')
    for link in links:
        get_one_set(link)


# 翻页爬取图片
def get_pic_by_page():
    for page in range(2, 11):
        next_page_url = f'https://mm.enterdesk.com/{page}.html'
        get_one_group(next_page_url)


def main():
    get_pic_by_page()


if __name__ == '__main__':
    main()
