import requests
from lxml import etree
url_file = []#文件下载链接暂存列表
url_list = []#页面读取链接暂存列表
photo_num=0#图片计数器
html_2=[]#链接缓存
headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36 Edg/87.0.664.52"
}#UA
page = int(input("请输入采集的最后一页"))
#让用户主动选择最后一页
'''
定义全局需要使用的变量
'''
for target_list in range(1,(page+1)):
    url=("https://bing.ioliu.cn/?p="+str(target_list))
    url_list.append(url)
#bing图片页面采用https://bing.ioliu.cn/?p=x 这种格式，通过控制range输出的量实现选择页数搜索，并且存入url_list列表
for _url in url_list:
    bing = requests.get(_url,headers=headers)
    print("返回码:"+str(bing.status_code))
    html_1 = etree.HTML(bing.text)
    html_1=(html_1.xpath('//div[@class="container"]/div[@*]/div[@class="card progressive"]/img/@data-progressive'))
    html_2=html_2+html_1
#利用requests库get到页面信息，并且使用解析出各个图片的img属性，从而获得下载链接，并存入html2
for target_list in html_2:
    digtes=target_list.find("640x480",0)
    url_file.append("http://h2.ioliu.cn/bing"+target_list[23:digtes]+"1920x1080.jpg")
#遇到一个奇怪的问题，etree始终无法解析bing图片的子链接，但是bing所有图片均使用了1920x1080.jpg这条参数，这里通过替换640x480为1920x1080实现获取高清图片链接。
for target_list in url_file:
    r = requests.get(target_list)
    photo_num=photo_num+1
    photo="pohot"+str(photo_num)+".jpg"
    with open(photo, "wb") as code:
        code.write(r.content)
#下载并保存高清图片

input("采集结束，共采集了："+str(photo_num)+"张图片，按任意键退出")
