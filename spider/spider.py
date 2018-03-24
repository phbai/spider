import requests
from bs4 import BeautifulSoup
import os,re,time,random
from pymongo import MongoClient
import time

def random_ip():
    a=random.randint(1,255)
    b=random.randint(1,255)
    c=random.randint(1,255)
    d=random.randint(1,255)
    return(str(a)+'.'+str(b)+'.'+str(c)+'.'+str(d))

client = MongoClient('mongo', 27017)
db = client['91porn']
posts = db['posts']
flag = 1
max_page = 1
insert_count = 0
headers = {'Accept-Language':'zh-CN,zh;q=0.9','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36'}

def get_page_content(page):
    page_url = 'http://91porn.com/v.php?next=watch&page='+str(page)
    return get_soup(page_url, headers)

def get_soup(url, headers):
    r = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup

def insert_posts_with_page(page):
    global insert_count
    page_url='http://91porn.com/v.php?next=watch&page=' + str(page)
    soup = get_page_content(page)
    items = soup.find_all(class_='listchannel')

    # 从最后一个item开始解析
    for item in reversed(items):
        title_info = item.find_all('div')[0]
        author_info = item.find(target='_parent')
        
        # 链接地址、图片地址
        link = title_info.find('a')['href']

        sub_page_headers = {'Accept-Language':'zh-CN,zh;q=0.9','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36','X-Forwarded-For':random_ip(),'referer':page_url,'Content-Type': 'multipart/form-data; session_language=cn_CN'}
        # 子页面抓取描述和时间
        sub_page_soup = get_soup(link, sub_page_headers)
        description = sub_page_soup.find_all(class_='more')[0].get_text(strip=True)
        time = sub_page_soup.find_all('span', class_='title')[1].string

        # 检测是否已经存入数据库
        link_result = posts.find_one({"link": link})
        # 数据库中已经存在 直接跳过
        if (link_result):
            continue

        img_url = title_info.find('img', width=True)['src']
        title = title_info.find('img', width=True)['title']
        author = author_info.string
        author_url = author_info['href']
        # 
        all_texts = re.findall(r'</span>(.+?)[<|\n]', str(item))
        duration = re.sub(r'\s', '' , all_texts[0])
        views = re.sub(r'\s', '' , all_texts[2])
        favorites = re.sub(r'\s', '' , all_texts[3])
        comments = re.sub(r'\s', '' , all_texts[4])
        points = re.sub(r'\s', '' , all_texts[5])
        # print(all_texts)

        post = {
            'title': title, 
            'link': link, 
            'author': author, 
            'author_url': author_url, 
            'thumbnail': img_url, 
            'duration': duration, 
            'time': time, 
            'views': views, 
            'favorites': favorites, 
            'comments': comments, 
            'points': points,
            'description': description,
        }
        insert_post(post)
        insert_count = insert_count + 1
        # print('标题：{0} 链接：{1} 作者：{2}'.format(title, link, author))
        # print('时长：{0} 时间：{1} 查看：{2} 收藏：{3} 评论：{4} 积分：{5}'.format(duration, time, views, favorites, comments, points))
    # print(time, views, comments, points)
    # print('标题 链接 时长 作者\n 时长')
    # print('{0} {1} {2}'.format(href, img_url, title))

def get_max_page(soup):
    form = soup.find_all('form')[2]
    page = form.find_all('a')[-2].string
    return int(page)

def insert_post(post):
    posts.insert_one(post)

def initial_crawler_task():
    soup = get_page_content(1)
    max_page = get_max_page(soup)
    print('共{0}页'.format(max_page))
    for page in reversed(range(max_page)):
        print('正在处理第{0}页数据...'.format(page + 1))
        insert_posts_with_page(page + 1)
    print("共插入{0}条数据".format(insert_count))

def update_task():
    while True:
        insert_posts_with_page(1)
        time.sleep(60)

if __name__ == '__main__':
    initial_crawler_task()
    update_task()
    # get_info(1)
    # insert_test()