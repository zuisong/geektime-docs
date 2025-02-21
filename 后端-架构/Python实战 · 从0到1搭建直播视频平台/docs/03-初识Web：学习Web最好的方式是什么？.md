你好，我是Barry。

我们每个人都浏览过无数个Web网页，只要打开浏览器里面就有无数网站，每一个网站又由很多个网页组成。

网页的起源要追溯到1989年，CERN（欧洲粒子物理研究所）的一个小组提交了一个针对Internet的新协议和一个使用该协议的文档系统，该小组将这个新系统命名为World Wide Web，它的目的是让全球的科学家能够利用Internet交流自己的工作文档。

![](https://static001.geekbang.org/resource/image/f5/ec/f5688dec5f1c321feeacdc18818cf6ec.jpg?wh=2084x1267)

这个新系统允许Internet上任意一个用户，从众多文档服务计算机的数据库中搜索和获取文档。1990年末，这个新系统的基本框架已经在CERN的一台计算机上开发实现了。1991年，这个系统移植到了其他计算机平台并正式发布。

经历了几十年的发展，网页的功能越来越丰富和强大，对于互联网企业来说，网页更是必不可少的。像企业的官网、网页端项目、公司内部管理系统都是常见的网页项目。

想要学习网页前端开发，就需要学习一些前端相关的技术和知识。前端必知必会的核心技术大致可以分为五大块，分别是：

- HTML
- CSS
- JavaScript
- 框架：Vue、React等
- 打包工具：Webpack、Vite等

## 前端核心技术模块

**1. HTML**  
网页最核心的技术就是HTML了。我们看到的网页其实就是由HTML这种编程语言描述出来的。
<div><strong>精选留言（12）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/29/04/3c/9f97f7bd.jpg" width="30px"><span>一米</span> 👍（3） 💬（1）<div>思考题：
&lt;!DOCTYPE html&gt;
&lt;html&gt;
&lt;head&gt;
    &lt;meta charset=&quot;utf-8&quot;&gt;
    &lt;title&gt;动效小测试&lt;&#47;title&gt;
&lt;&#47;head&gt;
&lt;body&gt;
    &lt;p&gt;变化前-1&lt;&#47;p&gt;
    &lt;button&gt;文本变换&lt;&#47;button&gt;
&lt;&#47;body&gt;
&lt;script&gt;

    const but = document.querySelector(&#39;button&#39;);
    const p1 = document.querySelector(&#39;p&#39;);
    but.addEventListener(&#39;click&#39;, change);

    function change() {
        if (p1.textContent === &quot;变化前-1&quot;) {
            p1.textContent = &quot;变化前-2&quot;;
        } else {
            p1.textContent = &quot;变化前-1&quot;;
        }
    }
&lt;&#47;script&gt;
&lt;&#47;html&gt;</div>2023-04-28</li><br/><li><img src="" width="30px"><span>Geek_6634a6</span> 👍（0） 💬（1）<div>&lt;!DOCTYPE html&gt;
&lt;html&gt;
&lt;head&gt;
    &lt;meta charset=&quot;utf-8&quot;&gt;
    &lt;title&gt;动效小测试&lt;&#47;title&gt;
&lt;&#47;head&gt;
&lt;body&gt;
&lt;p id=&quot;myParagraph&quot;&gt;变化前-1&lt;&#47;p&gt;
&lt;button onclick=&quot;changeText()&quot;&gt;文本变换&lt;&#47;button&gt;

&lt;script&gt;
    function changeText() {
        document.getElementById(&quot;myParagraph&quot;).innerHTML = &quot;变化后-2&quot;;
    }
&lt;&#47;script&gt;

&lt;&#47;body&gt;
&lt;&#47;html&gt;
</div>2024-07-28</li><br/><li><img src="" width="30px"><span>银角大王</span> 👍（0） 💬（1）<div>&lt;!DOCTYPE html&gt;
&lt;html&gt;
&lt;head&gt;
&lt;meta charset=&quot;utf-8&quot;&gt;
&lt;title&gt;动效小测试&lt;&#47;title&gt;
&lt;&#47;head&gt;
&lt;body&gt;
&lt;p id=&quot;text&quot;&gt;变化前-1&lt;&#47;p&gt;
&lt;button onclick=&quot;changetext()&quot;&gt;文本变换&lt;&#47;button&gt;
&lt;&#47;body&gt;

&lt;script&gt;
var p1 = document.getElementById(&quot;text&quot;)
function changetext(){
  if (p1.textContent === &quot;变化前-1&quot;) {
    p1.textContent = &quot;变化前-2&quot;;
  } else {
    p1.textContent = &quot;变化前-1&quot;;
  }
}

&lt;&#47;script&gt;
&lt;&#47;html&gt;</div>2023-12-20</li><br/><li><img src="" width="30px"><span>Geek_6c0b90</span> 👍（0） 💬（1）<div>老师，没有视频课程吗？</div>2023-12-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/f5/72/8cbc5cb3.jpg" width="30px"><span>好困啊</span> 👍（0） 💬（1）<div>&lt;!DOCTYPE html&gt;
&lt;html lang=&quot;en&quot;&gt;

&lt;head&gt;
    &lt;meta charset=&quot;UTF-8&quot;&gt;
    &lt;meta name=&quot;viewport&quot; content=&quot;width=device-width, initial-scale=1.0&quot;&gt;
    &lt;title&gt;文本变换示例&lt;&#47;title&gt;
&lt;&#47;head&gt;

&lt;body&gt;

&lt;!-- p标签，显示默认的文本 --&gt;
&lt;p id=&quot;text&quot;&gt;变化前 - 1&lt;&#47;p&gt;

&lt;!-- 按钮，点击后触发文本变换 --&gt;
&lt;button onclick=&quot;changeText()&quot;&gt;文本变换&lt;&#47;button&gt;

&lt;!-- JavaScript代码，用于实现文本变换功能 --&gt;
&lt;script&gt;
    function changeText() {
        &#47;&#47; 获取p标签元素
        var textElement = document.getElementById(&#39;text&#39;);
        &#47;&#47; 更改p标签的文本内容
        textElement.innerHTML = &quot;变化后 - 2&quot;;
    }
&lt;&#47;script&gt;

&lt;&#47;body&gt;
&lt;&#47;html&gt;</div>2023-08-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/58/9d/91d795cf.jpg" width="30px"><span>ZENG</span> 👍（0） 💬（1）<div>思考题

&lt;!DOCTYPE html&gt;
&lt;html&gt;
&lt;head&gt;
	&lt;meta charset=&quot;utf-8&quot;&gt;
	&lt;meta name=&quot;viewport&quot; content=&quot;width=device-width, initial-scale=1&quot;&gt;
	&lt;title&gt;动效小测试&lt;&#47;title&gt;
&lt;&#47;head&gt;
&lt;body&gt;
	&lt;p&gt;变换前 -1&lt;&#47;p&gt;
	&lt;button id=&#39;btn&#39;&gt;文本变换&lt;&#47;button&gt;

	&lt;script&gt;
		let num = -1
		p = document.querySelector(&#39;p&#39;)
		btn = document.querySelector(&quot;#btn&quot;)

		btn.onclick = function() {
			if (num == -1) {
				p.innerText = &#39;变换后 -2&#39;
				return num = -2
			}

			if (num == -2) {
				p.innerText = &#39;变换前 -1&#39;
				return num = -1
			}
		}
	&lt;&#47;script&gt;
&lt;&#47;body&gt;
&lt;&#47;html&gt;</div>2023-06-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/0d/5a/e60f4125.jpg" width="30px"><span>camel</span> 👍（0） 💬（1）<div>请问前端开发应该用什么idea？可能会介绍前端开发环境的搭建吗？</div>2023-05-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（1）<div>请教老师两个问题：
Q1: PyCharm自身没有python解释器吗？我用PyCharm创建了一个工程，interpreter是本机上安装的Anaconda的python.exe。

Q2：前端开发IDE是用VSCode吗？</div>2023-05-02</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTI7Bm7xdbwqoWPaDwqn6WESYL5QY8X8r3Q1P7UEIeDWictxJWEIJLluhIDHF7b0wFpbiav3gYToBBYg/132" width="30px"><span>Geek_840593</span> 👍（0） 💬（1）<div>思考题
&lt;!DOCTYPE html&gt;
&lt;html&gt;
&lt;head&gt;
&lt;meta charset=&quot;utf-8&quot;&gt;
&lt;title&gt;动效小测试&lt;&#47;title&gt;
&lt;script&gt;
    function displayDate(){
        document.getElementsByTagName(&quot;p&quot;)[0].innerHTML=&quot;变化后-2&quot;;
    }
&lt;&#47;script&gt;
&lt;&#47;head&gt;
&lt;body&gt;
&lt;p&gt;变化前-1&lt;&#47;p&gt;
&lt;button type=&quot;button&quot; onclick=&quot;displayDate()&quot;&gt;文本变换&lt;&#47;button&gt;
&lt;&#47;body&gt;
&lt;&#47;html&gt;</div>2023-04-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/23/bb/a1a61f7c.jpg" width="30px"><span>GAC·DU</span> 👍（0） 💬（2）<div>&lt;!DOCTYPE html&gt;
&lt;html lang=&quot;en&quot;&gt;
&lt;head&gt;
    &lt;meta charset=&quot;UTF-8&quot;&gt;
    &lt;title&gt;动效小测试&lt;&#47;title&gt;
&lt;&#47;head&gt;
&lt;body&gt;
    &lt;p&gt;变化前-1&lt;&#47;p&gt;
    &lt;button&gt;文本变换&lt;&#47;button&gt;
    &lt;script&gt;
        const btn = document.querySelector(&quot;button&quot;)
        const p = document.querySelector(&quot;p&quot;)
        btn.onclick = function () {
            p.innerText = &quot;变化后-2&quot;
        }
    &lt;&#47;script&gt;
&lt;&#47;body&gt;
&lt;&#47;html&gt;</div>2023-04-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0a/a4/828a431f.jpg" width="30px"><span>张申傲</span> 👍（0） 💬（0）<div>第3讲打卡~</div>2024-07-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（1）<div>请教老师两个问题：
Q1: PyCharm自身没有python解释器吗？我用PyCharm创建了一个工程，interpreter是本机上安装的Anaconda的python.exe。

Q2：前端开发IDE是用VSCode吗？</div>2023-05-02</li><br/>
</ul>