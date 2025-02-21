你好，我是黄鸿波。

上一节课我们讲解了什么是爬虫以及爬虫的基本原理，从这节课开始，我们就要实际地去爬取一些网络上的内容，为后续推荐系统的使用做准备。

这节课我们来深入了解一下Python中的常见爬虫框架：Scrapy框架。我们将学习什么是Scrapy框架、它的特点是什么以及如何安装和使用它。

## Scrapy框架概览

Scrapy是一个适用于Python的快速、高层次的屏幕抓取和Web抓取框架，用于抓取Web站点并从页面中提取结构化的数据。它也提供了多种类型爬虫的基类，如BaseSpider、Sitemap爬虫等。我们可以很方便地通过 Scrapy 框架实现一个爬虫程序，抓取指定网站的内容或图片。

![](https://static001.geekbang.org/resource/image/67/87/67220e129b726a764fa62f28fb46e587.png?wh=1200x482)

下面是Scrapy框架的架构图。

![](https://static001.geekbang.org/resource/image/02/b8/02ce18db3937d494e05ddcbdd60ee1b8.png?wh=1766x1039)

通过这张图我们可以看到，Scrapy框架总共分成了下面七个部分。

1. Scrapy Engine（Scrapy引擎）。
2. Scheduler（调度器）。
3. Downloader（下载器）。
4. Spiders（爬虫）。
5. Item Pipline（管道）。
6. Downloader Middlewares（下载中间件）。
7. Spider Middlewares（Spider中间件）。

接下来，我们来看看这七个部分的具体含义，以及它们是如何协作的。
<div><strong>精选留言（10）</strong></div><ul>
<li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/dcW6ufIgibXKl5jwrgsIibPxRehZBqN41ZHiamWx3yWNnfCfAOabxjYzLyDKv1HyYbNJOa05dEicobfGtBbJaJmG2w/132" width="30px"><span>Geek_79da7f</span> 👍（3） 💬（2）<div>关于安装ChromeDriver, mac上面一个命令行就解决了： brew install chromedriver</div>2023-09-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f0/5f/25942dfb.jpg" width="30px"><span>地铁林黛玉</span> 👍（1） 💬（4）<div>爬取的这些数据我们需要通过哪些方法知道是不是违法的呢？</div>2023-05-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1d/3a/cdf9c55f.jpg" width="30px"><span>未来已来</span> 👍（1） 💬（2）<div>遇到一个报错：Failure while parsing robots.txt.
解决：把 settings.py 文件的 `ROBOTSTXT_OBEY = True` 改为 `ROBOTSTXT_OBEY = False` 即可</div>2023-05-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（1） 💬（3）<div>请教老师几个问题啊
Q1：网站后端是用Java开发的，可以用Scrapy来抓取数据吗？相当于两种语言的混合使用了。
Q2：Anaconda安装的最后一步提示是“python3.9”,为什么创建虚拟环境的时候python版本是3.7？
Q3：安装的这个Anaconda，是正常的python开发环境吧。比如用来学习python，编码等。
Q4：conda list命令列出的scrapy，其build channel是py37XXX，
其中的37是python版本吗？</div>2023-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/d1/3b/a94459d2.jpg" width="30px"><span>GhostGuest</span> 👍（1） 💬（3）<div>更新建议改为一天一更，现在这节奏太慢了，前摇半天</div>2023-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/ba/42/5ca553bd.jpg" width="30px"><span>Weitzenböck</span> 👍（0） 💬（5）<div>我在执行main函数的时候出现了这个错误&quot;UnicodeDecodeError: &#39;utf-8&#39; codec can&#39;t decode byte 0xc3 in position 93: invalid continuation byte&quot;，是不是https:&#47;&#47;sina.com.cn这个网站没有用utf-8的编码格式啊</div>2023-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/31/8a/be3b7ae6.jpg" width="30px"><span>叶圣枫</span> 👍（2） 💬（0）<div>我的macbook上会报这个错：
urllib3 v2.0 only supports OpenSSL 1.1.1+, currently the &#39;ssl&#39; module is compiled with &#39;OpenSSL 1.0.2u  20 Dec 2019
解决方案是降级urllib3:
pip install urllib3==1.26.6

</div>2024-01-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/67/fe/5d17661a.jpg" width="30px"><span>悟尘</span> 👍（2） 💬（0）<div>chrom 114 版本以上的 下载chromedriver在这里：https:&#47;&#47;registry.npmmirror.com&#47;binary.html?path=chrome-for-testing&#47;</div>2023-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/63/7c/51d07eff.jpg" width="30px"><span>李</span> 👍（0） 💬（0）<div>老师出现这个错误是什么原因</div>2024-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/67/fe/5d17661a.jpg" width="30px"><span>悟尘</span> 👍（0） 💬（1）<div> [scrapy.downloadermiddlewares.redirect] DEBUG: Redirecting (301) to &lt;GET https:&#47;&#47;www.sina.com.cn&#47;&gt; from &lt;GET https:&#47;&#47;sina.com.cn&gt;
 [scrapy.core.engine] DEBUG: Crawled (200) &lt;GET https:&#47;&#47;www.sina.com.cn&#47;&gt; (referer: None)

这算是连上了？</div>2023-12-11</li><br/>
</ul>