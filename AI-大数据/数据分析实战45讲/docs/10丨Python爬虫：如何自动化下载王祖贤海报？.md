上一讲中我给你讲了如何使用八爪鱼采集数据，对于数据采集刚刚入门的人来说，像八爪鱼这种可视化的采集是一种非常好的方式。它最大的优点就是上手速度快，当然也存在一些问题，比如运行速度慢、可控性差等。

相比之下，爬虫可以很好地避免这些问题，今天我来分享下如何通过编写爬虫抓取数据。

## 爬虫的流程

相信你对“爬虫”这个词已经非常熟悉了，爬虫实际上是用浏览器访问的方式模拟了访问网站的过程，整个过程包括三个阶段：打开网页、提取数据和保存数据。

在Python中，这三个阶段都有对应的工具可以使用。

在“打开网页”这一步骤中，可以使用 Requests 访问页面，得到服务器返回给我们的数据，这里包括HTML页面以及JSON数据。

在“提取数据”这一步骤中，主要用到了两个工具。针对HTML页面，可以使用 XPath 进行元素定位，提取数据；针对JSON数据，可以使用JSON进行解析。

在最后一步“保存数据”中，我们可以使用 Pandas 保存数据，最后导出CSV文件。

下面我来分别介绍下这些工具的使用。

**Requests访问页面**

Requests是Python HTTP的客户端库，编写爬虫的时候都会用到，编写起来也很简单。它有两种访问方式：Get和Post。这两者最直观的区别就是：Get把参数包含在url中，而Post通过request body来传递参数。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/a3/87/c415e370.jpg" width="30px"><span>滢</span> 👍（63） 💬（2）<div>说明两点问题：
（一）.留言里有人评论说用XPath下载的图片打不开，其原因是定义的下载函数保存路径后缀名为&#39;.jpg&#39;，但是用XPath下载获得的图片url为&#39;https:&#47;&#47;img3.doubanio.com&#47;view&#47;celebrity&#47;s_ratio_celebrity&#47;public&#47;p616.webp&#39;，本身图片为webp格式，所以若保存为jpg格式，肯定是打不开的。
(二).  老师在文章内讲的用XPath下载代码只能下载第一页的内容，并不是全部的数据，不知道大家有没有查看用xpath函数获得的数组，大家留言里的代码似乎和老师的一样，只能得到首页的内容，所以也是需要模拟翻页操作才能获得完整的数据。

以下是课后练习题：爬取宫崎骏的电影海报， Python3.6 IDLE
&gt;&gt;&gt; import json
&gt;&gt;&gt; import requests as req
&gt;&gt;&gt; from lxml import etree
&gt;&gt;&gt; from selenium import webdriver
&gt;&gt;&gt; import os
&gt;&gt;&gt; request_url = &#39;https:&#47;&#47;movie.douban.com&#47;subject_search?search_text=宫崎骏&amp;cat=1002&#39;
&gt;&gt;&gt; src_xpath = &quot;&#47;&#47;div[@class=&#39;item-root&#39;]&#47;a[@class=&#39;cover-link&#39;]&#47;img[@class=&#39;cover&#39;]&#47;@src&quot;
&gt;&gt;&gt; title_xpath = &quot;&#47;&#47;div[@class=&#39;item-root&#39;]&#47;div[@class=&#39;detail&#39;]&#47;div[@class=&#39;title&#39;]&#47;a[@class=&#39;title-text&#39;]&quot;
&gt;&gt;&gt; driver = webdriver.Chrome(&#39;&#47;Users&#47;apple&#47;Downloads&#47;chromedriver&#39;)
&gt;&gt;&gt; driver.get(request_url)
&gt;&gt;&gt; html = etree.HTML(driver.page_source)
&gt;&gt;&gt; srcs = html.xpath(src_xpath)
&gt;&gt;&gt; print (srcs)  #大家可要看下打印出来的数据是否只是一页的内容，以及图片url的后缀格式
&gt;&gt;&gt; picpath = &#39;&#47;Users&#47;apple&#47;Downloads&#47;宫崎骏电影海报&#39;
&gt;&gt;&gt; if not os.path.isdir(picpath):
	os.mkdir(picpath)
&gt;&gt;&gt; def download(src, id):
	dic = picpath + &#39;&#47;&#39; + str(id) + &#39;.webp&#39;
	try:
		pic = req.get(src, timeout = 30)
		fp = open(dic, &#39;wb&#39;)
		fp.write(pic.content)
		fp.close()
	except req.exceptions.ConnectionError:
		print (&#39;图片无法下载&#39;)
&gt;&gt;&gt; for i in range(0, 150, 15):
	url = request_url + &#39;&amp;start=&#39; + str(i)
	driver.get(url)
	html = etree.HTML(driver.page_source)
	srcs = html.xpath(src_xpath)
	titles = html.xpath(title_xpath)
	for src,title in zip(srcs, titles):
		download(src, title.text)
</div>2019-04-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/64/bd/cbcdc4a6.jpg" width="30px"><span>rOMEo罗密欧</span> 👍（46） 💬（4）<div>老师请问一下：如果是需要用户登陆后才能爬取的数据该怎么用python来实现呢？</div>2019-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/1e/4c/79590513.jpg" width="30px"><span>Bayes</span> 👍（18） 💬（8）<div>老师你这跳过了太多步骤了，表示对于python跟着你前几节课入门的人什么都不会，按着你的代码运行，要不就是没有定义，要不就是没有这个函数。刚开始的人也不知道哪个函数在哪个库，建议老师按照流程来一步一步给代码，要不就在最后给一个完整的代码示例，真的是学的很困难加上想放弃</div>2019-07-30</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/l56HXkqMD4hqDg82yiaTr28GSwB1rCasj7n8M65VbibsJwmDibJnrWpw8o0mYGewH6NeD1wGvU6OGdhDG4nzIa9mA/132" width="30px"><span>LY</span> 👍（16） 💬（1）<div>#环境：Mac Python3
#pip install selenium
#下载chromedriver，放到项目路径下（https:&#47;&#47;npm.taobao.org&#47;mirrors&#47;chromedriver&#47;2.33&#47;）
# coding:utf-8
import requests
import json
import os
from lxml import etree
from selenium import webdriver

query = &#39;张柏芝&#39;
downloadPath = &#39;&#47;Users&#47;yong&#47;Desktop&#47;Python&#47;xpath&#47;images&#47;&#39;

&#39;&#39;&#39; 下载图片 &#39;&#39;&#39;
def download(src, id):
    dir = downloadPath + str(id) + &#39;.jpg&#39;
    try:
        pic = requests.get(src, timeout=10)
    except requests.exceptions.ConnectionError:
    # print &#39;error, %d 当前图片无法下载&#39;, %id
        print(&#39;图片无法下载&#39;)
    if not os.path.exists(downloadPath):
        os.mkdir(downloadPath)
    if os.path.exists(dir):
        print(&#39;已存在:&#39;+ id)
        return
    fp = open(dir, &#39;wb&#39;)
    fp.write(pic.content)
    fp.close()
 
def searchImages():
    &#39;&#39;&#39; for 循环 请求全部的 url &#39;&#39;&#39;
    for i in range(0, 22471, 20):
        url = &#39;https:&#47;&#47;www.douban.com&#47;j&#47;search_photo?q=&#39;+query+&#39;&amp;limit=20&amp;start=&#39;+str(i)
        html = requests.get(url).text    # 得到返回结果
        print(&#39;html:&#39;+html)
        response = json.loads(html,encoding=&#39;utf-8&#39;) # 将 JSON 格式转换成 Python 对象
        for image in response[&#39;images&#39;]:
            print(image[&#39;src&#39;]) # 查看当前下载的图片网址
            download(image[&#39;src&#39;], image[&#39;id&#39;]) # 下载一张图片

def getMovieImages():
    url = &#39;https:&#47;&#47;movie.douban.com&#47;subject_search?search_text=&#39;+ query +&#39;&amp;cat=1002&#39;
    driver = webdriver.Chrome(&#39;&#47;Users&#47;yong&#47;Desktop&#47;Python&#47;xpath&#47;libs&#47;chromedriver&#39;)
    driver.get(url)
    html = etree.HTML(driver.page_source)
    # 使用xpath helper, ctrl+shit+x 选中元素，如果要匹配全部，则需要修改query 表达式
    src_xpath = &quot;&#47;&#47;div[@class=&#39;item-root&#39;]&#47;a[@class=&#39;cover-link&#39;]&#47;img[@class=&#39;cover&#39;]&#47;@src&quot;
    title_xpath = &quot;&#47;&#47;div[@class=&#39;item-root&#39;]&#47;div[@class=&#39;detail&#39;]&#47;div[@class=&#39;title&#39;]&#47;a[@class=&#39;title-text&#39;]&quot;

    srcs = html.xpath(src_xpath)
    titles = html.xpath(title_xpath)
    for src, title in zip(srcs, titles):
        print(&#39;\t&#39;.join([str(src),str(title.text)]))
        download(src, title.text)

    driver.close()

getMovieImages()</div>2019-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ca/1a/9ecbf1bb.jpg" width="30px"><span>伪君子</span> 👍（16） 💬（2）<div>那些用 ChromeDriver 的出现报错的可能是没有安装 ChromeDriver，或者是没给出 ChromeDriver 的路径，具体可以看看下面这篇文章。
https:&#47;&#47;mp.weixin.qq.com&#47;s&#47;UL0bcLr3KOb-qpI9oegaIQ</div>2019-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/87/d3/fe95bda9.jpg" width="30px"><span>飘</span> 👍（9） 💬（3）<div>感谢作者以及评论区的各位大神，终于完成了爬虫代码，总结一下小白编写时遇到的几个问题：
1）获取xpath时，chrome浏览器需要安装插件xpatn-helper；
2）使用python3.7，提前引入模块requests，lxml，selenium，安装这些模块需要更新pip至20版本；
3）模拟用户访问浏览器，需要下载chromedriver.exe,放入python.exe所在目录；
4）图片路径中出现导致编译失败的字符，使用replace替换报错字符。
具体代码如下：
import os
import requests
from lxml import etree
from selenium import webdriver

search_text = &quot;王祖贤&quot;
start = 0
limit = 15
total = 90

def download(img, title):
	dir = &quot;D:\\数据分析\\python test\\query\\&quot; + search_text + &quot;\\&quot; 
	id = title.replace(u&#39;\u200e&#39;, u&#39;&#39;).replace(u&#39;?&#39;, u&#39;&#39;) .replace(u&#39;&#47;&#39;, u&#39;or&#39;)
	if not os.path.exists(dir):
		os.makedirs(dir)
	try:    
		pic = requests.get(img, timeout=10) 
		img_path = dir  + str(id) + &#39;.jpg&#39;   
		fp = open(img_path, &#39;wb&#39;)    
		fp.write(pic.content)    
		fp.close()  
	except requests.exceptions.ConnectionError:    
		print(&#39;图片无法下载&#39;)

def crawler_xpath():
	src_img = &quot;&#47;&#47;div[@class=&#39;item-root&#39;]&#47;a[@class=&#39;cover-link&#39;]&#47;img[@class=&#39;cover&#39;]&#47;@src&quot;
	src_title = &quot;&#47;&#47;div[@class=&#39;item-root&#39;]&#47;div[@class=&#39;detail&#39;]&#47;div[@class=&#39;title&#39;]&#47;a[@class=&#39;title-text&#39;]&quot;
	
	for i in range(start,total,limit):
		request_url = &quot;https:&#47;&#47;search.douban.com&#47;movie&#47;subject_search?search_text=&quot;+search_text+&quot;&amp;cat=1002&amp;start=&quot;+str(i)
		driver = webdriver.Chrome()
		driver.get(request_url)
		html = etree.HTML(driver.page_source)
		imgs = html.xpath(src_img)
		titles = html.xpath(src_title)
		print(imgs,titles)
		for img, title in zip(imgs, titles): 
			download(img, title.text)
if __name__ == &#39;__main__&#39;:
	crawler_xpath()
</div>2020-04-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/67/fb/cd95d624.jpg" width="30px"><span>germany</span> 👍（6） 💬（2）<div>老师：为什么我在豆瓣网查询图片的网址与你不一样？https:&#47;&#47;www.douban.com&#47;search?cat=1025&amp;q=王祖贤&amp;source=suggest  。是什么原因？</div>2019-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f8/99/8e760987.jpg" width="30px"><span>許敲敲</span> 👍（5） 💬（1）<div>要下载所有James 哈登的图片</div>2019-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/37/52/c1c56b6f.jpg" width="30px"><span>Geek_2008d9</span> 👍（4） 💬（3）<div>为什么我总是response=json.loads那一行显示json.decoder.JSONDecoderError:expecting value:line 1 column 1(char 0) 呢，怎么解决啊，各位大佬</div>2019-12-14</li><br/><li><img src="" width="30px"><span>Geek_c45626</span> 👍（3） 💬（7）<div>老师，运行代码总是出错：JSONDecodeError: Expecting value: line 1 column 1 (char 0)，这个怎么解决？</div>2019-12-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/18/d0/49b06424.jpg" width="30px"><span>qinggeouye</span> 👍（3） 💬（1）<div>https:&#47;&#47;github.com&#47;qinggeouye&#47;GeekTime&#47;blob&#47;master&#47;DataAnalysis&#47;10_crawl_xpath.py

import os
import requests
from lxml import etree
from selenium import webdriver

search_text = &#39;王祖贤&#39;
start = 0  # 请求 url 的 start 从 0 开始，每一页间隔 15，有 6 页
total = 90
limit = 15

# 电影海报图片地址
src_xpath = &quot;&#47;&#47;div[@class=&#39;item-root&#39;]&#47;a[@class=&#39;cover-link&#39;]&#47;img[@class=&#39;cover&#39;]&#47;@src&quot;
# 电影海报图片title
title_xpath = &quot;&#47;&#47;div[@class=&#39;item-root&#39;]&#47;div[@class=&#39;detail&#39;]&#47;div[@class=&#39;title&#39;]&#47;a[@class=&#39;title-text&#39;]&quot;

# 保存目录
pic_path = &#39;10&#47;xpath&#39;  # 相对目录
# WebDriver 创建一个 Chrome 浏览器的 drive
driver = webdriver.Chrome(&#39;.&#47;chromedriver&#39;)  # MAC 版本


# 创建图片保存路径
def mk_save_path(pic_path_):
    if not os.path.exists(pic_path_):
        os.makedirs(pic_path_)
    return os.getcwd() + &#39;&#47;&#39; + pic_path_ + &#39;&#47;&#39;


# 下载图片
def download(src, pic_id, save_path_):
    directory = save_path_ + str(pic_id) + &#39;.jpg&#39;
    try:
        pic = requests.get(src, timeout=10)
        fp = open(directory, &#39;wb&#39;)
        fp.write(pic.content)
        fp.close()
    except requests.exceptions.ConnectionError:
        print(&#39;图片如无法下载&#39;)


def get_response_xpath():
    save_path = mk_save_path(pic_path)
    for i in range(start, total, limit):
        requests_url = &#39;https:&#47;&#47;search.douban.com&#47;movie&#47;subject_search?search_text=&#39; + search_text + &#39;&amp;cat=1002&#39; + \
                       &#39;&amp;start=&#39; + str(i)
        driver.get(url=requests_url)
        html = etree.HTML(driver.page_source)
        src_list = html.xpath(src_xpath)
        title_list = html.xpath(title_xpath)
        for src, title in zip(src_list, title_list):
            download(src, title.text, save_path)


if __name__ == &#39;__main__&#39;:
    get_response_xpath()</div>2019-11-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/56/65/22a37a8e.jpg" width="30px"><span>Yezhiwei</span> 👍（3） 💬（1）<div>用Scrapy爬取数据更方便哈，请问老师怎么做一个通用的爬虫呢？比如要爬取文章标题和内容，不同的网站Xpath结构不一样，如果源少的话可以分别配置，但如果要爬取几百上千的网站数据，分别配置Xpath挺麻烦的。请问这个问题有什么解决方案吗？谢谢</div>2019-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/18/d0/49b06424.jpg" width="30px"><span>qinggeouye</span> 👍（2） 💬（2）<div>https:&#47;&#47;github.com&#47;qinggeouye&#47;GeekTime&#47;blob&#47;master&#47;DataAnalysis&#47;10_crawl.py

# coding: utf-8
import os

import requests
import json


# 下载图片
def download(src, pic_id, save_path_):
    directory = save_path_ + str(pic_id) + &#39;.jpg&#39;

    try:
        pic = requests.get(src, timeout=10)
        fp = open(directory, &#39;wb&#39;)
        fp.write(pic.content)
        fp.close()
    except requests.exceptions.ConnectionError:
        print(&#39;图片如无法下载&#39;)


# 获取返回页面内容
def get_resp(query_, limit_, start_):
    url_ = &#39;https:&#47;&#47;www.douban.com&#47;j&#47;search_photo?q=&#39; + query_ + &#39;&amp;limit=&#39; + str(limit_) + &#39;&amp;start=&#39; + str(start_)
    html_ = requests.get(url_).text  # 得到返回结果
    response_ = json.loads(html_, encoding=&#39;utf-8&#39;)  # 将 JSON 格式转换为 Python 对象
    return response_


query = &#39;王祖贤&#39;
limit = 20
start = 0

&#39;&#39;&#39; 获取图片总数量 &#39;&#39;&#39;
total = get_resp(query, limit, start)[&#39;total&#39;]
print(total)

pic_path = &#39;10&#39;  # 相对目录
if not os.path.exists(pic_path):
    os.mkdir(pic_path)
save_path = os.getcwd() + &#39;&#47;&#39; + pic_path + &#39;&#47;&#39;

# 循环 请求全部的 url
for i in range(start, total, limit):
    response = get_resp(query, limit, i)
    for image in response[&#39;images&#39;]:
        print(image[&#39;src&#39;])  # 查看当前下载的图片地址
        download(image[&#39;src&#39;], image[&#39;id&#39;], save_path)  # 下载一张图片
</div>2019-11-05</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJjiaBHJyfAKK02CCcibkqI0jpaHJEcyrTRI4xbrqHCWiaia88WQs4r8zJVmHfibqricUYeUT2ezAZAC7wQ/132" width="30px"><span>爱喝酸奶的程序员</span> 👍（2） 💬（1）<div>有个问题selenium，是用来自动化测试的，他回打开浏览器……我做爬虫是不想让代码打开浏览器，只想要他爬取的动作～要怎么办呢？</div>2019-02-26</li><br/><li><img src="" width="30px"><span>十六。</span> 👍（1） 💬（1）<div>由于python学习是爬虫上手的，爬虫还是会一点的，哈哈，去下一章了ღ( ´･ᴗ･` )</div>2020-03-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4d/49/28e73b9c.jpg" width="30px"><span>明翼</span> 👍（1） 💬（3）<div>我在实践这篇过程中遇到了很多问题，最终解决了，写在我的公众号里面，运行代码有问题的同学可以参考下：
https:&#47;&#47;mp.weixin.qq.com&#47;s?__biz=MjM5OTE4MzcyNA==&amp;tempkey=MTA0MF95UW5FRmVZZURiWVR2ZWZiZVVaUEctS3FhUF90OVljc3RZTEV6eHpKSjF3NlpxMjhMcXdoU2trV2Y1RzdCQXZQamptXzZTODZNbGw0U3ZmMlhzT1BFOWZWeXhaOTM3bHFITjl6dVBLbUxfSlI4ZG15bFpvYnpvUTJienlKOWx2M0V1QURvZWVZUU1rTVRudk96WXZTb01qekdEWmJhaW5zMDd3OFB3fn4%3D&amp;chksm=3f29d0a1085e59b7d37190f6e8580bc03526dca518fc70e844a76ae1a571bc90d88ac52acc88#rd</div>2019-12-21</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/DYAIOgq83eppQqDE6TNibvr3DNdxG323AruicIgWo5DpVr6U7yZVNkbF2rKluyDfhdpgAEcYEOZTAnbrMdTzFkUw/0" width="30px"><span>图·美克尔</span> 👍（1） 💬（1）<div>我更喜欢用bs4美味汤</div>2019-07-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/18/86/3599130b.jpg" width="30px"><span>dany</span> 👍（1） 💬（1）<div>download到哪里去了？不好意思我是菜鸟</div>2019-07-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/dc/ce/03fdeb60.jpg" width="30px"><span>白色纯度</span> 👍（1） 💬（3）<div>网址：豆瓣电影；任务：批量下载赵丽颖电影海报（支持翻页，自定义终止下载量）；python3.X；
浏览器：Google Chrome ；唯一要注意的是webdriver的路径。全都是这门课程里面的知识点
# -*- coding: utf-8 -*-
import requests
from lxml import etree
from selenium import webdriver
import os

name = &#39;赵丽颖&#39;

def download(src, id):
    if not os.path.isdir(&quot;Xpath的翻页图片包&quot;):
        os.mkdir(&quot;Xpath的翻页图片包&quot;)
    dir = os.path.join(&quot;Xpath的翻页图片包&#47;&quot;, str(id) + &#39;.webp&#39;)
    try:
        pic = requests.get(src, timeout = 10)
        with open(dir, &#39;wb&#39;) as d:
            d.write(pic.content)
    except requests.exceptions.ConnectionError:
        print(&quot;图片无法下载&quot;)

def down_load(request_url):
    driver.get(request_url)
    html = etree.HTML(driver.page_source)
    src_xpath = &quot;&#47;&#47;div[@class=&#39;item-root&#39;]&#47;a[@class=&#39;cover-link&#39;]&#47;img[@class=&#39;cover&#39;]&#47;@src&quot;
    title_xpath = &quot;&#47;&#47;div[@class=&#39;item-root&#39;]&#47;div[@class=&#39;detail&#39;]&#47;div[@class=&#39;title&#39;]&#47;a[@class=&#39;title-text&#39;]&quot;
    srcs = html.xpath(src_xpath)


    titles = html.xpath(title_xpath)
    num = len(srcs)
    if num &gt; 15:
        srcs = srcs[1:]
        titles = titles[1:]

    for src, title in zip(srcs, titles):
        if title is None:
            continue
        print(src)
        download(src, title.text)
    print(&#39;OK&#39;)
    print(num)
    if num &gt;= 1:
        return True
    else:
        return False

if __name__ == &#39;__main__&#39;:
    requests_url = &quot;https:&#47;&#47;movie.douban.com&#47;subject_search?search_text=&quot; + name
    driver = webdriver.Chrome(executable_path=r&#39;C:\Users\XXX\AppData\Local\Google\Chrome\Application\chromedriver.exe&#39;)
    driver.get(requests_url)
    html = etree.HTML(driver.page_source)
    print(html)

    base_url = &#39;https:&#47;&#47;movie.douban.com&#47;subject_search?search_text=&#39; + name + &#39;&amp;cat=1002&amp;start=&#39;
    start = 0
    while start &lt; 70:
        request_url = base_url + str(start)
        flag = down_load(request_url)
        if flag:
            start += 15
        else:
            break
    print(&quot;结束&quot;)</div>2019-06-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/02/ce/57c871e0.jpg" width="30px"><span>云深不知处</span> 👍（1） 💬（1）<div>结合老师和精选留言源码，抓取“王祖贤”图片和电影海报，代码在自己环境中调试成功，还挺有趣。</div>2019-06-09</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/4kF5cFK9MN6WX9Dibodh8pWIib06icoSgSPb6pAhGVjO3gpD72R77eicGkCUWfl3feNtn2icEibhUvgWt890rYLYGoqg/132" width="30px"><span>chitanda</span> 👍（1） 💬（1）<div>分享一个可以在专题页面下载茅野爱衣缩略图的脚本，src_xpath = &quot;&#47;&#47;img[@class=&#39;&#39;]&#47;@src&quot;中的class=&#39;&#39; 让我搞了半天，至今不知道为什么不存在class name时必须加一句class=&#39;&#39;，下面是代码
import os
import uuid

from lxml import etree

import requests


def download(src, name=None):
    if not name:
        name = uuid.uuid1()
    if not os.path.isdir(&#39;Kayano&#39;):
        os.mkdir(&#39;Kayano&#39;)
    adir = os.path.join(&#39;Kayano&#47;&#39;, str(name) + &#39;.jpg&#39;)
    try:
        pic = requests.get(src, timeout=10)
        with open(adir, &#39;wb&#39;) as f:
            f.write(pic.content)
    except requests.exceptions.ConnectionError:
        print(&#39;图片无法下载&#39;)


if __name__ == &#39;__main__&#39;:
    
    from selenium import webdriver
    
    request_url = &#39;https:&#47;&#47;movie.douban.com&#47;celebrity&#47;1314532&#47;photos&#47;&#39;
    driver = webdriver.Chrome(executable_path=&#39;chromedriver.exe&#39;)
    driver.get(request_url)
    html = etree.HTML(driver.page_source)
    
    src_xpath = &quot;&#47;&#47;img[@class=&#39;&#39;]&#47;@src&quot;
    srcs = html.xpath(src_xpath)
    for src in srcs:
        download(src)
</div>2019-04-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/b6/43/c7b2a6f9.jpg" width="30px"><span>竹本先生</span> 👍（1） 💬（1）<div># coding:utf-8
import requests as rq
import json
import re
from lxml import etree

# 下载图片
def download(src, title):
	# 过滤非法字符
	rstr = r&quot;[\&#47;\\\:\*\?\&quot;\&lt;\&gt;\|]&quot;
	title = re.sub(rstr, &quot;&quot;, title)
	
	dir = &#39;.&#47;film_pic&#47;&#39; + str(title) + &#39;.jpg&#39;
	
	try:
		pic = rq.get(src, timeout=10)
		with open(dir, &#39;wb&#39;) as fp:
			fp.write(pic.content)
	except rq.exceptions.ConnectionError:
		return False
	else:
		return True

# 获取电影数量
def get_film_amount(performer_name):
	url = &#39;https:&#47;&#47;www.douban.com&#47;j&#47;search?q=&#39; +performer_name+ &#39;&amp;start=0&amp;cat=1002&#39;
	result = rq.get(url)
	result_obj = json.loads(result.text)
	return int(result_obj[&#39;total&#39;])

# 获取电影信息
def get_film_info(query_name):
	# XPath规则
	title_xpath = &quot;&#47;&#47;div[@class=&#39;content&#39;]&#47;div[@class=&#39;title&#39;]&#47;h3&#47;a&quot;
	pic_xpath = &quot;&#47;&#47;div[@class=&#39;pic&#39;]&#47;a[@class=&#39;nbg&#39;]&#47;img&#47;@src&quot;

	titles = []
	pics = []

	film_amount = get_film_amount(query_name)

	for i in range(0, film_amount, 20):
		url = &#39;https:&#47;&#47;www.douban.com&#47;j&#47;search?q=&#39; +query_name+ &#39;&amp;start=&#39;+str(i)+&#39;&amp;cat=1002&#39;
		result = rq.get(url)
		result_obj = json.loads(result.text)
		
		for item in result_obj[&#39;items&#39;]:
			html = etree.HTML(item)
			tmp_titles = html.xpath(title_xpath)
			tmp_pics = html.xpath(pic_xpath)
			
			if &#39;default_small&#39; not in tmp_pics[0]:
				titles.append(tmp_titles[0].text.strip())
				pics.append(tmp_pics[0])
	
	return {&#39;name&#39;: query_name, &#39;amount&#39;: film_amount, &#39;list&#39;: zip(titles,pics)}

query_name_list = [&#39;周润发&#39;,&#39;甄子丹&#39;,&#39;周星驰&#39;,&#39;刘德华&#39;,&#39;王祖贤&#39;,&#39;元彪&#39;,&#39;靳东&#39;,&#39;王凯&#39;,&#39;张铁林&#39;,&#39;段奕宏&#39;,&#39;郑伊健&#39;,&#39;张耀扬&#39;,&#39;陈乔恩&#39;]

for query_name in query_name_list:
	print(query_name + &#39; 共有&#39; + str(get_film_amount(query_name)) + &#39;部电影&#39;)
	film_info = get_film_info(query_name)
	order = 1
	for title,src in film_info[&#39;list&#39;]:
		
		if download(src, query_name +&quot; - &quot;+ title):
			print(str(order).zfill(3) + &#39;. 下载成功：&#39; + title)
		else:
			print(str(order).zfill(3) + &#39;. 下载失败：&#39; + title)
		order += 1</div>2019-01-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/10/df/e4511752.jpg" width="30px"><span>周萝卜</span> 👍（1） 💬（1）<div>下载王祖贤的海报，并且把每张海报的评论保存在MongoDB中，代码如下：
https:&#47;&#47;github.com&#47;zhouwei713&#47;douban&#47;tree&#47;master&#47;wangzuxian_poster
</div>2019-01-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/de/a0/88be6607.jpg" width="30px"><span>Allen</span> 👍（0） 💬（1）<div># Selenium 模拟 下载宫崎骏动画电影海报
import os
import requests
from selenium import webdriver

&#39;&#39;&#39;访问豆瓣电影主页 搜索宫崎骏&#39;&#39;&#39;
query = &#39;宫崎骏&#39;
url = &#39;https:&#47;&#47;movie.douban.com&#47;&#39;
driver = webdriver.Chrome(executable_path=&#39;.&#47;chromedriver&#39;)
driver.get(url)
query_input = driver.find_element_by_xpath(&#39;&#47;&#47;*[@id=&quot;inp-query&quot;]&#39;)
query_input.send_keys(query)
query_input.submit()

&#39;&#39;&#39;下载图片&#39;&#39;&#39;
def download(src, id):
    dir = f&quot;.&#47;{query}&#47;{id}.{src.split(&#39;.&#39;)[-1]}&quot;
    if not os.path.isdir(query):
        os.mkdir(query)
    if os.path.exists(dir):
        return
    try:
        pic = requests.get(src, timeout=10)
        with open(dir, &#39;wb&#39;) as f:
            f.write(pic.content)
    except requests.exceptions.ConnectionError:
        print(&#39;图片无法下载&#39;)
        
&#39;&#39;&#39;查看翻页按钮，实现翻页效果&#39;&#39;&#39;
next_page = driver.find_element_by_xpath(&#39;&#47;&#47;*[@class=&quot;next&quot;]&#39;)

num = 1
while next_page:
    print(f&#39;当前页为 第 {num} 页&#39;)
   # 查看当前页，并保存图片
    srcs = driver.find_elements_by_xpath(&#39;&#47;&#47;div[@class=&quot;item-root&quot;]&#47;a[@class=&quot;cover-link&quot;]&#47;img[@class=&quot;cover&quot;]&#39;)
    titles = driver.find_elements_by_xpath(&#39;&#47;&#47;div[@class=&quot;item-root&quot;]&#47;div[@class=&quot;detail&quot;]&#47;div[@class=&quot;title&quot;]&#47;a[@class=&quot;title-text&quot;]&#39;)
    for src, title in zip(srcs, titles):
        download(src.get_attribute(&#39;src&#39;), title.text)
    next_page = driver.find_element_by_xpath(&#39;&#47;&#47;*[@class=&quot;next&quot;]&#39;)
    next_page.click()
    num += 1
    if num &gt; 5:
        break

driver.quit()        </div>2020-09-21</li><br/><li><img src="" width="30px"><span>不会狗带</span> 👍（0） 💬（3）<div>老师，我的代码报错是no module named requests.  还有大部分内容不知道老师在说什么，是因为自己的问题，还是老师中间跳过了几步呀？LOL。😂 请问老师可不可以把完整的代码公布一下，或者有没有小的视频可以跟着操作呢？</div>2020-03-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/86/32/6a8049eb.jpg" width="30px"><span>李宽</span> 👍（0） 💬（1）<div>试了下，需要添加headers才能成功
不过，下载下来的图片文件为什么打不开呀？</div>2020-01-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4d/49/28e73b9c.jpg" width="30px"><span>明翼</span> 👍（0） 💬（1）<div>模拟浏览器下载图片的可以参考https:&#47;&#47;mp.weixin.qq.com&#47;s&#47;1qAcKbtV2Mr_Q-ieb_8gqg</div>2019-12-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/64/9b/d1ab239e.jpg" width="30px"><span>J.Smile</span> 👍（0） 💬（1）<div>老师，你记录的笔记好漂亮啊</div>2019-11-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/26/16/9de2666e.jpg" width="30px"><span>陳陽</span> 👍（0） 💬（1）<div>不错</div>2019-10-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/65/1a/5f3d7f5f.jpg" width="30px"><span>锦旗小能猫</span> 👍（0） 💬（1）<div>我觉得老师这个步骤就应该写出来 很多人问chromedrive报错和xpath这块，跟着做估计是看不太懂</div>2019-08-20</li><br/>
</ul>