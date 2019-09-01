# coding=utf-8
# Author:Tommy_Sea
# Time:2019-8
'''
--------------使用爬虫去网上下载图片---------------
#########将找到的图片保存为一个列表，然后返回。####
#########运行之中如果文件目录下已经存在‘pic’#####
#########相同名字的文件夹，将会出错。         #####
#########需要将其删除。                      #####
'''
import urllib.request as urlr
import os
import time#通过延迟一定时间可以有效应对反爬

#保存图片在本地
def save_imgs(img_addrs):
    for each in img_addrs:
        print(each)
        filename = each.split('/')[-1]
        with open(filename, 'wb') as f:#使用with不用特别注意close files
            img = url_open('http:'+ each)#之前得到的图片地址是“//”开头的，直接使用无法访问
            time.sleep(2)               #两秒的睡眠，应对反爬
            f.write(img)
#访问网页
def url_open(url):
    'In order to reduce the codes we done this part'
    req = urlr.Request(url)#建立一个Request类
    req.add_header('User-Agent',
                   'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36')
    response = urlr.urlopen(url)#访问网页
    html = response.read()#读取网页
    print(url)
    return html
#查找图片地址
def find_imgs(page_url):
    html = url_open(page_url).decode('utf-8')
    img_addrs = []#空的列表用于存放图片地址
    a = html.find('img src=')#没找到为-1

    while a != -1:          #如果找到图片地址
        b = html.find('.jpg', a, a+255)#从开始直到255个字符
        if b != -1:#如果找到了
            img_addrs.append(html[a+9:b+4])
        else:
            b = a + 9
        a = html.find('img src=', b)

    for each in img_addrs:
        print(each)
    return img_addrs
#捕获页面
def get_page(url):
    html = url_open(url).decode('utf-8')#解码

    a = html.find('current-comment-page')+23#一直查询到‘[’符号
    b = html.find(']',a)#找到右边的‘]’
    return html[a:b]#返回中间的数值

def download_pic(floder='pic',pages=13):
    os.mkdir(floder)#创建文件夹
    os.chdir(floder)#进入文件夹

    url = 'http://jandan.net/pic/'
    page_num = int(get_page(url))
    print(page_num)
    for i in range(pages):
        page_num -= i
        page_url = url + 'page-' + str(page_num) + '#comments'#拼凑出一个新的地址
        img_addrs = find_imgs(page_url)#图片的地址
        save_imgs(img_addrs)


if __name__ == '__main__':
    download_pic('pic',13)