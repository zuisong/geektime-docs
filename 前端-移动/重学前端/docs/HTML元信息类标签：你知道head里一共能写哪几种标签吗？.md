你好，我是winter。

我们在前面的HTML部分的课程中，已经学习了语义标签。这些标签涵盖了我们日常开发用到的多数标签，也是我们编写代码时最常用的一批标签。

但是我们今天要讲的标签，重要性丝毫不弱于语义类标签，这就是页面元信息类标签。

我们可以先来了解一下什么是元信息类标签。所谓元信息，是指描述自身的信息，元信息类标签，就是HTML用于描述文档自身的一类标签，它们通常出现在head标签中，一般都不会在页面被显示出来（与此相对，其它标签，如语义类标签，描述的是业务）。

元信息多数情况下是给浏览器、搜索引擎等机器阅读的，有时候这些信息会在页面之外显示给用户，有时候则不会。

元信息类标签数量不多，我在这里就逐一为你介绍一下。

## head标签

首先我们先来了解一下head标签，head标签本身并不携带任何信息，它主要是作为盛放其它语义类标签的容器使用。

head标签规定了自身必须是html标签中的第一个标签，它的内容必须包含一个title，并且最多只能包含一个base。如果文档作为iframe，或者有其他方式指定了文档标题时，可以允许不包含title标签。

## title标签

title标签表示文档的标题，从字面上就非常容易理解。这里我就讲讲需要注意的地方。
<div><strong>精选留言（21）</strong></div><ul>
<li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83er9YqiaybDPpZMr3ecHDv8P3chyr3dETz5Ljft8s3F47JDN93yOKeOyysxxhaN7MJmXt7ib5X6EgMGQ/132" width="30px"><span>火云邪神0007</span> 👍（203） 💬（6）<div>老师，我家的猫不让我给他剪指甲，怎么办？</div>2019-02-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/93/4a/de82f373.jpg" width="30px"><span>AICC</span> 👍（158） 💬（1）<div>&lt;meta http-equiv=&quot;X-UA-Compatible&quot; content=&quot;IE=edge,chrome=1&quot;&gt;
&lt;!-- 默认使用最新浏览器 --&gt;
&lt;meta http-equiv=&quot;Cache-Control&quot; content=&quot;no-siteapp&quot;&gt;
&lt;!-- 不被网页(加速)转码 --&gt;
&lt;meta name=&quot;robots&quot; content=&quot;index,follow&quot;&gt;
&lt;!-- 搜索引擎抓取 --&gt;
&lt;meta name=&quot;renderer&quot; content=&quot;webkit&quot;&gt;
&lt;meta name=&quot;viewport&quot; content=&quot;width=device-width, initial-scale=1, maximum-scale=1, minimum-scale=1, user-scalable=no, minimal-ui&quot;&gt;
&lt;meta name=&quot;apple-mobile-web-app-capable&quot; content=&quot;yes&quot;&gt;
&lt;!-- 删除苹果默认的工具栏和菜单栏 --&gt;
&lt;meta name=&quot;apple-mobile-web-app-status-bar-style&quot; content=&quot;black-translucent&quot;&gt;
&lt;!-- 设置苹果工具栏颜色 --&gt;</div>2019-02-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/94/56/4b8395f6.jpg" width="30px"><span>CC</span> 👍（38） 💬（2）<div>阅读完今天的文章，才感觉自己其实不懂 meta，之前对 meta 的细节缺少分类和整理。感谢老师。

回到老师的问题，我平时还见过以下三种（组）标签：

1. Open Graph 的标签组，包括 title, type, URL, site_name, description 和 image，是为 Facebook 分享提供信息；

2. Twitter 的标签组，包括 card, title, description 和 image，是为 Twitter 分享提供信息；

3. msapplication 的标签组，包括 TileColor 和 TileImage，是为 Windows 8 以及以上系统识别 favicons 用的。
</div>2019-02-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c6/28/d6f49ec2.jpg" width="30px"><span>MarlboroKay</span> 👍（8） 💬（1）<div>meta基本用法：
  &lt;meta name=application-name content=&quot;lsForums&quot;&gt;
name = application-name 是不是少了 “”
name = &quot;applicaiton-name&quot; ?</div>2019-02-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/db/26/54f2c164.jpg" width="30px"><span>靠人品去赢</span> 👍（5） 💬（1）<div>突然想问一下，老是本尊是不是一个猫奴啊，感觉很喜欢那猫举例子做封面什么的。</div>2019-02-21</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/3XbCueYYVWTiclv8T5tFpwiblOxLphvSZxL4ujMdqVMibZnOiaFK2C5nKRGv407iaAsrI0CDICYVQJtiaITzkjfjbvrQ/132" width="30px"><span>有铭</span> 👍（4） 💬（1）<div>我是说为什么viewport在html标准里找不到，一直很疑惑是从哪里蹦出来的，搞了半天原来不是html标准是行业约定</div>2019-02-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/35/d0/f2ac6d91.jpg" width="30px"><span>阿成</span> 👍（2） 💬（1）<div>常见的还有
format-detection 禁止 iPhone 的自动识别
</div>2019-02-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/84/68/4fc0151c.jpg" width="30px"><span>丘丘</span> 👍（11） 💬（2）<div>上面评论中的
&lt;meta name=&quot;apple-mobile-web-app-capable&quot; content=&quot;yes&quot;&gt;
&lt;!-- 删除苹果默认的工具栏和菜单栏 --&gt;
&lt;meta name=&quot;apple-mobile-web-app-status-bar-style&quot; content=&quot;black-translucent&quot;&gt;
&lt;!-- 设置苹果工具栏颜色 --&gt;
这两条，我试着似乎没有效果。
keywords这个属性，理论上对seo有作用，但是我随便进行了搜索，打开排名第一页的几个网站，都没有这么属性，是不是现在这种简单的seo打法已经被放弃了呢？</div>2019-03-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/15/16/0bde0009.jpg" width="30px"><span>LiH</span> 👍（10） 💬（1）<div>&lt;meta name=&quot;format-detection&quot; content=&quot;telephone=no&quot;&gt;
&lt;meta name=&quot;format-detection&quot; content=&quot;date=no&quot;&gt;
&lt;meta name=&quot;format-detection&quot; content=&quot;address=no&quot;&gt;
&lt;meta name=&quot;format-detection&quot; content=&quot;email=no&quot;&gt;
关闭iOS上的内容识别</div>2019-03-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/6e/dc/9c7dc899.jpg" width="30px"><span>码屁</span> 👍（5） 💬（0）<div>@丘丘 你难道忘了 竞价排名[滑稽]</div>2019-05-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/b3/e8/cbb1ac81.jpg" width="30px"><span>Alen</span> 👍（5） 💬（0）<div>http:&#47;&#47;www.alenqi.site&#47;2018&#47;03&#47;04&#47;complete-tags&#47; 之前总结的</div>2019-05-08</li><br/><li><img src="" width="30px"><span>Geek_fc1551</span> 👍（2） 💬（0）<div> &lt;meta name=&quot;apple-mobile-web-app-status-bar-style&quot; content=&quot;black-translucent&quot; &#47;&gt; 
  &lt;!-- 添加到主屏后的标题 --&gt; 
  &lt;meta name=&quot;apple-mobile-web-app-title&quot; content=&quot;标题&quot; &#47;&gt; 
  &lt;!-- 忽略数字自动识别为电话号码 --&gt; 
  &lt;meta content=&quot;telephone=no&quot; name=&quot;format-detection&quot; &#47;&gt; 
  &lt;!-- 忽略识别邮箱 --&gt; 
  &lt;meta content=&quot;email=no&quot; name=&quot;format-detection&quot; &#47;&gt; 
  &lt;meta name=&quot;apple-itunes-app&quot; content=&quot;app-id=myAppStoreID, 
affiliate-data=myAffiliateData, app-argument=myURL&quot; &#47;&gt; </div>2019-12-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/48/3da605c6.jpg" width="30px"><span>July</span> 👍（2） 💬（0）<div>老师好，keywords 现在对seo还有用吗？</div>2019-02-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/30/bc/0233b519.jpg" width="30px"><span>老纪程序</span> 👍（1） 💬（0）<div>style script  link  平时还看到有这几个</div>2021-12-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/55/cb/1efe460a.jpg" width="30px"><span>渴望做梦</span> 👍（1） 💬（0）<div>&lt;meta name=&quot;renderer&quot; content=&quot;webkit|ie-comp|ie-stand&quot;&gt;
对于多核浏览器，控制浏览器以哪种类型内核来显示，好像是 360 浏览器首先主导的</div>2019-07-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/06/ca/7699f593.jpg" width="30px"><span>周姑娘</span> 👍（1） 💬（0）<div>为什么我有的看不懂，不知道怎么学习</div>2019-04-03</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83epcs6PibsP9vEXv4EibUw3bhQPUK04zRTOvfrvF08TwM67xPb1LBh2uRENHQwo2VqYfC5GhJmM7icxHA/132" width="30px"><span>蹦哒</span> 👍（0） 💬（0）<div>加上这样的meta，页面依然可以缩放，目前还没有发现能够成功禁止缩放的浏览器，是这个过时了不被浏览器支持了吗？

&lt;meta name=&quot;viewport&quot; content=&quot;width=device-width,initial-scale=1,minimum-scale=1,maximum-scale=1,user-scalable=no&quot;&gt;</div>2022-09-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ed/94/5058c24f.jpg" width="30px"><span>疯狂的石头</span> 👍（0） 💬（0）<div>看了MDN，meta标签支持网站提供可使用的特定信息，如Facebook编写的元数据协议，Twitter自己的元数据协议
```
&lt;meta property=&quot;og:image&quot; content=&quot;https:&#47;&#47;developer.mozilla.org&#47;static&#47;img&#47;opengraph-logo.png&quot;&gt;
&lt;meta property=&quot;og:description&quot; content=&quot;The Mozilla Developer Network (MDN) provides
information about Open Web technologies including HTML, CSS, and APIs for both Web sites
and HTML5 Apps. It also documents Mozilla products, like Firefox OS.&quot;&gt;
&lt;meta property=&quot;og:title&quot; content=&quot;Mozilla Developer Network&quot;&gt;

```
</div>2022-07-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f7/95/c3a2ad6e.jpg" width="30px"><span>　Burning</span> 👍（0） 💬（0）<div>禁止百度转码
  &lt;meta http-equiv=&quot;Cache-Control&quot; content=&quot;no-transform&quot; &#47;&gt;
  &lt;meta http-equiv=&quot;Cache-Control&quot; content=&quot;no-siteapp&quot; &#47;&gt;

申明页面适配那一端
&lt;meta name=&quot;applicable-device&quot; content=&quot;mobile&quot;&gt;</div>2020-04-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/31/bc/c4f31fa5.jpg" width="30px"><span>杨越</span> 👍（0） 💬（1）<div>&lt;head&gt;
&lt;base href=&quot;http:&#47;&#47;www.w3school.com.cn&#47;i&#47;&quot; &#47;&gt;
&lt;base target=&quot;_blank&quot; &#47;&gt;
&lt;&#47;head&gt;

&lt;body&gt;
&lt;img src=&quot;eg_smile.gif&quot; &#47;&gt;
&lt;a href=&quot;http:&#47;&#47;www.w3school.com.cn&quot;&gt;W3School&lt;&#47;a&gt;
&lt;&#47;body&gt;

https:&#47;&#47;www.w3school.com.cn&#47;tags&#47;tag_base.asp
老师，这个教程里用了两个base标签也没事啊？</div>2020-03-26</li><br/><li><img src="" width="30px"><span>Geek_fc1551</span> 👍（0） 💬（0）<div>老是通常我们用的比较多的时哪些，给个模板贴了就能的，必不可少的</div>2019-12-04</li><br/>
</ul>