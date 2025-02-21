你好，我是黄鸿波。

上一节课，我们对Scrapy框架有了一个整体的了解，也实际地安装了Scrapy库并搭建了一个基础的Scrapy工程。这节课，我们就继续在这个工程的基础上爬取新浪新闻中的数据，并对爬取到的数据进行解析。

## 使用Scrapy框架抓取数据

我们首先打开sina\\sina\\spider下面的sina\_spider.py文件，在这个文件中，Scrapy框架给我们写了一个基础的框架代码。

```
import scrapy
 
class SinaSpiderSpider(scrapy.Spider):
    name = 'sina_spider'
    allowed_domains = ['sina.com.cn']
    start_urls = ['http://sina.com.cn/']
 
    def parse(self, response):
        pass
```

这段代码主要是对整个爬虫程序做了一个简单的定义，定义了爬虫的名字为“sina\_spider”，爬取的域名为“sina.com.cn”，爬取的URL是“[http://sina.com.cn/](http://sina.com.cn/)”。最后它还贴心地帮我们定义了一个解析函数，这个解析函数的入参就是服务器返回的response值。现在，我们要开始分析我们要爬取的内容，并对这个函数进行改写。

### 页面分析

我们先以网易的国内新闻为例来分析一下。我们先看下面这个界面。

![](https://static001.geekbang.org/resource/image/10/c5/105f1037b22ba0d30f68346c39c065c5.png?wh=2412x1391)

我们要分析的是界面里最新新闻这个部分。可以看到这个新闻列表中一共包含了下面这几部分：标题、摘要、时间、关键词。我们还可以看到，时间在1小时之内的会显示为“XX分钟前”，在1小时以上的会显示今天具体的某个时间点。
<div><strong>精选留言（13）</strong></div><ul>
<li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/EaBxhibOicZe9L7z2icbU4W462l543drFWYqibqczTicj4Msyb2g9pDSGmFTiafW9jibwib7jG6hpAdPMcCowdCiaxHaOdA/132" width="30px"><span>Geek_ccc0fd</span> 👍（3） 💬（1）<div>新安装selemium的API变了，而且xpath获取的路径有点问题，我这里获取不到一页的全部内容，我修改了一下：
title = driver.find_elements(By.XPATH, &quot;&#47;&#47;div[@class=&#39;feed-card-item&#39;]&#47;h2&#47;a[@target=&#39;_blank&#39;]&quot;)
time = driver.find_elements(By.XPATH,&quot;&#47;&#47;div[@class=&#39;feed-card-item&#39;]&#47;h2&#47;..&#47;div[@class=&#39;feed-card-a feed-card-clearfix&#39;]&#47;div[@class=&#39;feed-card-time&#39;]&quot;)
然后就是翻页点击那里我这边跑下来也有问题，根据xpath会获取两个a标签,所以需要增加索引：
driver.find_elements(By.XPATH,&quot;&#47;&#47;div[@class=&#39;feed-card-page&#39;]&#47;span[@class=&#39;pagebox_next&#39;]&#47;a&quot;)[0].click()</div>2023-05-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1d/3a/cdf9c55f.jpg" width="30px"><span>未来已来</span> 👍（1） 💬（2）<div>截止到 5月3日，新安装的 selemium 只有 find_elements 方法，老师的代码需改为：
`title = driver.find_elements(By.XPATH, &quot;&#47;&#47;h2[@class=&#39;undefined&#39;]&#47;a[@target=&#39;_blank&#39;]&quot;)`
`time = driver.find_elements(By.XPATH, &quot;&#47;&#47;h2[@class=&#39;undefined&#39;]&#47;..&#47;div[@class=&#39;feed-card-a feed-card-clearfix&#39;]&#47;div[@class=&#39;feed-card-time&#39;]&quot;)`
以此类推</div>2023-05-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/bd/95/882bd4e0.jpg" width="30px"><span>Abigail</span> 👍（0） 💬（1）<div>应该设计一个简单点的例子, python 起码也要用 3.9 啊</div>2023-10-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f7/d3/2bbc62b2.jpg" width="30px"><span>alexliu</span> 👍（0） 💬（1）<div>在运行下一页click()的时候，有可能出现ElementNotInteractableException错误，解决方案：
1、在driver.get(response.url)和click()后添加延时time.sleep(2)
2、保持chrome的窗口大小一致 self.option.add_argument(&quot;--window-size=1960,1080&quot;)
try... except...部分代码如下：
            try:
                _next = driver.find_elements(By.XPATH, &quot;&#47;&#47;div[@class=&#39;feed-card-page&#39;]&#47;span[@class=&#39;pagebox_next&#39;]&#47;a&quot;)
                _next[0].click()
                _time.sleep(2)
            except StaleElementReferenceException as e:
                print(&quot; page failed.&quot;, e)
                _next = driver.find_elements(By.XPATH, &quot;&#47;&#47;div[@class=&#39;feed-card-page&#39;]&#47;span[@class=&#39;pagebox_next&#39;]&#47;a&quot;)
                _next[0].click()
                _time.sleep(2)
            except ElementNotInteractableException as e:
                print(&quot; not found page.&quot;, e)
                break
            except Exception as e:
                print(&quot;unkwon error: &quot;, e)</div>2023-06-01</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/EaBxhibOicZe9L7z2icbU4W462l543drFWYqibqczTicj4Msyb2g9pDSGmFTiafW9jibwib7jG6hpAdPMcCowdCiaxHaOdA/132" width="30px"><span>Geek_ccc0fd</span> 👍（0） 💬（1）<div>我们在parse里面可以直接使用response.xpath获取元素，和使用 driver.find_elements是同样的效果，为什么还要用selenium来做浏览器的操作呢？</div>2023-05-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/56/75/28a29e7c.jpg" width="30px"><span>安菲尔德</span> 👍（0） 💬（1）<div>请问哪有main.py文件呢，没有看到</div>2023-05-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（2）<div>Q3：源码放在什么地方啊？能否把源码集中放到一个公共地方? 比如github等。</div>2023-04-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（3）<div>Q1：第七课，创建环境的最后几步，不停出错，最后一个错误是：执行“scrapy genspider sina_spider sina.com.cn”，报告：lib\string.py&quot;, line 132, in substitute
    return self.pattern.sub(convert, self.template)
TypeError: cannot use a string pattern on a bytes-like object
网上搜了，大意说是python2和python3不匹配导致的。 我是完全按照老师的步骤来安装的，安装的是pythno3，怎么会有python2呢？当然，这个文件还没有解决，进行不下去了，郁闷啊。 
Q2：能否建一个微信群？遇到问题可以协商。 另外，老师能否更及时地回复留言？</div>2023-04-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/23/bb/a1a61f7c.jpg" width="30px"><span>GAC·DU</span> 👍（0） 💬（1）<div>老师，关于代码有些疑惑，第一：为什么parse_namedetail方法不再使用driver发起http请求和获取html标签内容？
第二：desc = response.xpath(&quot;&#47;&#47;div[@class=&#39;article&#39;]&#47;p&#47;text()&quot;).extract()
        desc = selector.xpath(&quot;&#47;&#47;div[@class=&#39;article&#39;]&#47;p&#47;text()&quot;).extract() 
我测试了两个代码都可以使用，那为什么不直接使用response，反而要生成一个selector？</div>2023-04-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/ba/42/5ca553bd.jpg" width="30px"><span>Weitzenböck</span> 👍（1） 💬（1）<div>如果出现这个错误：__init__() got an unexpected keyword argument &#39;chrome_options&#39; 代码里改为 driver = webdriver.Chrome(options=self.option)具体源码是：
class WebDriver(ChromiumDriver):
    &quot;&quot;&quot;Controls the ChromeDriver and allows you to drive the browser.&quot;&quot;&quot;

    def __init__(
        self,
        options: Options = None,
        service: Service = None,
        keep_alive: bool = True,
    ) -&gt; None:
        &quot;&quot;&quot;Creates a new instance of the chrome driver. Starts the service and
        then creates new instance of chrome driver.

        :Args:
         - options - this takes an instance of ChromeOptions
         - service - Service object for handling the browser driver if you need to pass extra details
         - keep_alive - Whether to configure ChromeRemoteConnection to use HTTP keep-alive.
        &quot;&quot;&quot;
        self.service = service if service else Service()
        self.options = options if options else Options()
        self.keep_alive = keep_alive

        self.service.path = DriverFinder.get_path(self.service, self.options)

        super().__init__(
            DesiredCapabilities.CHROME[&quot;browserName&quot;],
            &quot;goog&quot;,
            self.options,
            self.service,
            self.keep_alive,
        )</div>2023-06-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/8b/4b/15ab499a.jpg" width="30px"><span>风轻扬</span> 👍（0） 💬（0）<div>mac系统，爬取过程中，可能会报错：无法打开chromedriver，因为无法验证开发者。
如果是brew安装的chromedriver，可以执行：xattr -d com.apple.quarantine &#47;opt&#47;homebrew&#47;bin&#47;chromedriver进行可信授权。
如果不是brew安装的，需要自己找到chromedriver的安装路径，然后执行xattr -d com.apple.quarantine 你的chromedriver的路径</div>2024-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/67/fe/5d17661a.jpg" width="30px"><span>悟尘</span> 👍（0） 💬（1）<div> # 尝试点击下一页
            try:
                # next_page_link = WebDriverWait(driver, 30).until(
                #     EC.element_to_be_clickable(
                #         (By.XPATH, &quot;&#47;&#47;div[@class=&#39;feed-card-page&#39;]&#47;span[@class=&#39;pagebox_next&#39;]&#47;a&quot;))
                # )
                # next_page_link.click()
                driver.find_elements(By.XPATH, &quot;&#47;&#47;div[@class=&#39;feed-card-page&#39;]&#47;span[@class=&#39;pagebox_next&#39;]&#47;a&quot;)[0].click()
            except Exception as e:
                print(f&quot;Error clicking next page link: {e}&quot;)
                break

打出的异常是：Error clicking next page link: Message: stale element reference: stale element not found

这是因为什么？</div>2023-12-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/67/fe/5d17661a.jpg" width="30px"><span>悟尘</span> 👍（0） 💬（0）<div>为什么我的翻页不起作用呢？
</div>2023-12-12</li><br/>
</ul>