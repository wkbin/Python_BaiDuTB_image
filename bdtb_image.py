# @Author: Kebin.Wang
# @Date:   2018-06-16 20:12:49
# @Last Modified time: 2018-01-03 14:42:09

"""
功能: 输入百度贴吧帖子的地址就可以爬取贴吧里面所有的图片
测试环境为python3.6.5
"""
import requests
from lxml import etree
import urllib.request
import re
import os

# 获取尾页
def get_num(url):
	r = requests.get(url).text
	s = etree.HTML(r)
	urls = s.xpath('//li[@class="l_reply_num"]/span[2]/text()')
	return urls

def judge_url():
    #设定布尔中间变量
    jude=False
    while not jude :
        url = input("请输入要获取图片的贴吧地址：")
        # https转http
        if(url[4] == 's'):
        	url = url[:4]+url[5:]
        	print(url)
        # 格式化url删除两边的空格
        url = url.strip()
        #判断url是否包含"http://tieba.baidu.com/p/"
        url1 = url[:25]
        url2 = "http://tieba.baidu.com/p/"
        #判断url位数是否大于最低位数
        jude = int(len(url)) >=35 and url1 == url2
        print()
        if not jude:
            print("输入地址有误，请重新输入！")
    # 格式化url，只截取“http://tieba.baidu.com/p/数字 ”部分
    url = url[:35]
    return url

# 以标题存为文件夹名存放图片
def create_folder(url2):
    url=url2
    # 建立图片存放文件夹，以贴吧标题为名
    try:
        # 获取标题
        tile = re.compile('<title>(.*?)_百度贴吧</title>').findall(urllib.request.urlopen(url).read().decode('UTF-8'))
        os.mkdir(str(tile[0]))
        print("成功创建\""+str(tile[0])+"\"  文件夹")
        os.chdir(os.path.join(os.getcwd(), str(tile[0])))
    except UnicodeDecodeError:
        print("找不到标题，请检查地址！")
    except FileExistsError: #文件存在错误异常
        os.chdir(os.path.join(os.getcwd(), str(tile[0])))
        print("\"" + str(tile[0]) + "\"  文件夹已存在，将直接下载到本文件夹")
    except Exception as Error:
        print("获取标题失败，错误原因：" + Error)

def page(url):
    start = 1   #开始页码
    end= int(get_num(url)[0])	#结束页码
    
   
    p=int(start)
    while p<=int(end):
        #添加url页码参数
        url2=url+"?pn="+str(p)
        #获取图片
        fetch_pictures(url2,p)
        p=int(p)+1
#遍历存储图片
def fetch_pictures(url,p):
    html_content = urllib.request.urlopen(url).read()
    try:
        #获取图片地址列表
        picture_url_list=re.compile('class="BDE_Image" (?:[a-zA_Z0-9="^>]+ )*src="(.*?)" ').findall(html_content.decode('UTF-8'))
        #检查是否搜索到图片
        if  len(picture_url_list)==0:
            print("第"+str(p)+"页没有发现图片！")
        else:
            print("正在下载第"+str(p)+"页的图片：")
            # 遍历图片地址列表存储图片
            for i in range(len(picture_url_list)):
                # 设置图片名字为页码数+序号
                picture_name = str(p) + "__" + str(i + 1) + '.jpg'
                try:
                    # 存储图片
                    urllib.request.urlretrieve(picture_url_list[i], picture_name)
                    # 存储爬取成功打印
                    print("成功下载： " + picture_url_list[i])
                except Exception as Error:
                    # 异常失败打印
                    print("下载失败： " + picture_url_list[i])
                    print("异常原因： " + Error)
    except UnicodeDecodeError:
        print("获取图片链接列表失败")
       
def get():
    # 获取地址
    url = judge_url()
    # 建立存放的文件夹
    create_folder(url)
    # 获取页码存储图片
    page(url)

if __name__ == '__main__':
   get()