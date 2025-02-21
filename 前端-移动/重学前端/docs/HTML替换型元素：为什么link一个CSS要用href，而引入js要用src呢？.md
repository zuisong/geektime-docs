你好，我是winter。我们今天来讲讲替换型元素。

我们都知道一个常识，一个网页，它是由多个文件构成的，我们在之前的课程中，已经学过了一种引入文件的方案：链接。

这节课我们要讲的替换型元素，就是另一种引入文件的方式了。替换型元素是把文件的内容引入，替换掉自身位置的一类标签。

我们首先来看一种比较熟悉的标签：script标签。

## script

我们之所以选择先讲解script标签，是因为script标签是为数不多的既可以作为替换型标签，又可以不作为替换型标签的元素。

我们先来看看script标签的两种用法：

```HTML

<script type="text/javascript">
console.log("Hello world!");
</script>


<script type="text/javascript" src="my.js"></script>

```

这个例子中，我们展示了两种script标签的写法，一种是直接把脚本代码写在script标签之间，另一种是把代码放到独立的js文件中，用src属性引入。

这两种写法是等效的。我想这种等效性可以帮助你理解替换型元素的“替换”是怎么一回事。

这里我们就可以回答标题中的问题了：凡是替换型元素，都是使用src属性来引用文件的，而我们之前的课程中已经讲过，链接型元素是使用href标签的。
<div><strong>精选留言（15）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/15/25/2c/8f61089f.jpg" width="30px"><span>宗麒麟</span> 👍（0） 💬（3）<div>var a = {n: 1}; 
var b = a; 
a.x = a = {n: 2};
a.x  b.x 分别是什么？
老师，能不能把a.x这块的赋值讲一下？</div>2019-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/3a/d6/485590bd.jpg" width="30px"><span>赵健</span> 👍（20） 💬（5）<div>老师好，想请问下，业务场景中需要嵌入公司其他行业线的页面，这种不使用iframe该咋办？</div>2019-04-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1a/e5/6899701e.jpg" width="30px"><span>favorlm</span> 👍（10） 💬（0）<div>早起第一件事，学习</div>2019-04-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a9/06/9811fb65.jpg" width="30px"><span>草剑</span> 👍（9） 💬（0）<div>src 属性支持 http、data、 ftp、file、mailto、smtp、pop、dns、whois、finger、daytime、news、urn 等协议</div>2020-05-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4f/d3/897fc6df.jpg" width="30px"><span>Geeker1992</span> 👍（9） 💬（2）<div>老师，style 既然也可以这么用
&lt;style&gt;css 规则&lt;&#47;style&gt;，
为什么没有 &lt;style src=“”&gt;&lt;&#47;style&gt;？
</div>2019-04-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/35/d0/f2ac6d91.jpg" width="30px"><span>阿成</span> 👍（7） 💬（0）<div>常见的有：http:&#47;&#47;,https:&#47;&#47;,file:&#47;&#47;,data...</div>2019-04-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/1e/c2/edf5dfcb.jpg" width="30px"><span>南墙的树</span> 👍（5） 💬（0）<div>h5的设计稿，完全照办app设计稿，页面顶部的title导航（包括返回按钮），页面主体部分引入外部资源，这种需求，不使用iframe，请问老师该怎么处理？或者说，从一个不懂技术的产品那里开始，这种方案就有问题？</div>2019-04-25</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJDSY5xBJ2PH4lqNtWJqhe1HcYkP7S9ibAXChONgCBX5pJ2gaU3icXhltQgqhzDyML3EzFicxPeE4Tiag/132" width="30px"><span>Geek_0bb537</span> 👍（3） 💬（2）<div>iframe有没有什么好的替代方案 那个导航栏一般都是通用的 我看到淘宝也有iframe</div>2019-04-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/1c/b9/392b94ee.jpg" width="30px"><span>umaru</span> 👍（2） 💬（0）<div>Style元素不能使用css属性，这句话没看懂</div>2019-04-10</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/dgVrmQBbMel7v6mBCm6oWvttx9BGQsCDpbMOhm9Hh8gj8k0NRbo4mmoDZrpuaqxQMIkHSUgq15L83ficyY8leVg/132" width="30px"><span>Geek_de3c35</span> 👍（1） 💬（0）<div>https:&#47;&#47;developer.mozilla.org&#47;zh-CN&#47;docs&#47;Web&#47;HTTP&#47;Headers&#47;Content-Security-Policy&#47;img-src</div>2020-11-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/25/2c/8f61089f.jpg" width="30px"><span>宗麒麟</span> 👍（1） 💬（0）<div>老师还是承接刚才那个问题，
js里  .优先级高于  =，因此:
1、先计算a.x，此时内存地址1多了x
2、计算最右边  =  ，此时a指向了新地址2
3、最后计算左边的=，此时内存地址1的x指向了a
应该是这样的原理，但是我感觉少了一个东西，就是第2步里，a已经指向新地址2了，为什么第三步执行a.x时，a.x还能指向地址1里的x呢？</div>2019-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/54/29/59663398.jpg" width="30px"><span>🐳李小博🐳</span> 👍（1） 💬（2）<div>@Geeker1992
回答你的问题，只有可替换型元素才能用src，元素就是实实在在有内容的东西，不管有没有样式文档都会存在，而css是样式文档，他不是可替换型元素。</div>2019-05-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（1） 💬（0）<div>就说一个经常见到的： blob</div>2019-04-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/80/a5/1a9921de.jpg" width="30px"><span>稚鸿同学</span> 👍（0） 💬（0）<div>winter你好，如果当前页面需要有个区域是当前系统其他页面或者其他系统的，可以不用iframe，还也可以怎么处理？因为可能还有和子页面的交互</div>2019-12-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a7/9c/be5dffb6.jpg" width="30px"><span>AbyssKR</span> 👍（0） 💬（0）<div>style 标签不在替换中元素中，所以不使用 src 属性。&lt;style src=&quot;&quot;&gt; W3C 的回答是从未讨论过，而且看到貌似以前还出现过 link 引入 JavaScript 的想法。</div>2019-04-11</li><br/>
</ul>