import requests
from bs4 import BeautifulSoup
import os,re,time,random
from pymongo import MongoClient

client = MongoClient('mongo', 27017)
db = client['91porn']
posts = db['posts']
flag = 1
max_page = 1
headers = {'Accept-Language':'zh-CN,zh;q=0.9','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36'}

def get_soup(page):
    page_url='http://91porn.com/v.php?next=watch&page='+str(page)
    r = requests.get(url=page_url, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup

# get_info :: page -> items 
def insert_posts_with_page(page):
    soup = get_soup(page)
    items = soup.find_all(class_='listchannel')

    for item in items:
        title_info = item.find_all('div')[0]
        author_info = item.find(target='_parent')
        
        # 链接地址、图片地址
        link = title_info.find('a')['href']
        img_url = title_info.find('img', width=True)['src']
        title = title_info.find('img', width=True)['title']
        author = author_info.string
        author_url = author_info['href']
        # 
        all_texts = re.findall(r'</span>(.+?)[<|\n]', str(item))
        duration = re.sub(r'\s', '' , all_texts[0])
        time = re.sub(r'\s', '' , all_texts[1])
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
        }
        insert_post(post)
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

def insert_test():
    post = {
        'title': '宾馆美女按摩口交服务', 
        'link': 'http://91porn.com/view_video.php?viewkey=f902bbca1f5f5d61ac91&page=1&viewtype=basic&category=mr',
        'author': '男人天生爱风流',
        'duration': '00:00',
        'time': '2小时前',
        'views': '0',
        'favorites': '0',
        'comments': '0',
        'points': '0',
    }
    posts.insert_one(post)
# def download_mp4(url,dir):
#     headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36Name','Referer':'http://91porn.com'}
#     req=requests.get(url=url)
#     filename=str(dir)+'/1.mp4'
#     with open(filename,'wb') as f:
#         f.write(req.content)
# def download_img(url,dir):
#     headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36Name','Referer':'http://91porn.com'}
#     req=requests.get(url=url)
#     with open(str(dir)+'/thumb.png','wb') as f:
#         f.write(req.content)
# def random_ip():
#     a=random.randint(1,255)
#     b=random.randint(1,255)
#     c=random.randint(1,255)
#     d=random.randint(1,255)
#     return(str(a)+'.'+str(b)+'.'+str(c)+'.'+str(d))

# while flag<=100:
    
    # item = items[0]
    # title_info = item.find_all(class_='imagechannelhd')
    # print(title_info)
    # viewkey=re.findall(r'<a target=blank href="http://91porn.com/view_video.php\?viewkey=(.*)&page=.*&viewtype=basic&category=.*?">\n                    <img ',str(get_page.content,'utf-8',errors='ignore'))
    # for key in viewkey:
    #     headers={'Accept-Language':'zh-CN,zh;q=0.9','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36','X-Forwarded-For':random_ip(),'referer':page_url,'Content-Type': 'multipart/form-data; session_language=cn_CN'}
    #     video_url=[]
    #     img_url=[]
    #     base_req=requests.get(url=base_url+key,headers=headers)
    #     video_url=re.findall(r'<source src="(.*?)" type=\'video/mp4\'>',str(base_req.content,'utf-8',errors='ignore'))
    #     title=re.findall(r'<div id="viewvideo-title">(.*?)</div>',str(base_req.content,'utf-8',errors='ignore'),re.S)
    #     img_url=re.findall(r'poster="(.*?)"',str(base_req.content,'utf-8',errors='ignore'))
    #     try:
    #         t=title[0]
    #         title[0]=t.replace('\n','')
    #         t=title[0].replace(' ','')
    #     except IndexError:
    #         pass
        
    #     print('标题：{0} 图片地址：{1} 链接地址:{2}'.format(str(t), str(img_url[0]), video_url[0] ))
        # if os.path.exists(str(t))==False:
        #     try:
        #         os.makedirs(str(t))
        #         print('开始下载:'+str(t))
        #         download_img(str(img_url[0]),str(t))
        #         download_mp4(str(video_url[0]),str(t))
        #         print('下载完成')
        #     except:
        #         pass
        # else:
        #     print('已存在文件夹,跳过')
        #     time.sleep(2)
    # flag=flag+1
    # print('此页已下载完成，下一页是'+str(flag))

if __name__ == '__main__':
    soup = get_soup(1)
    max_page = get_max_page(soup)
    print('共{0}页'.format(max_page))
    # insert_test()
    for page in range(6):
        insert_posts_with_page(page + 1)
        print('插入第{0}页数据完毕'.format(page + 1))
    # get_info(1)
    # insert_test()