通过前面6个模块的介绍，我们已经大致知道浏览器是怎么工作的了，也了解这种工作方式对前端产生了什么样的影响。在这个过程中，我们还穿插介绍了一些浏览器安全相关的内容，不过都比较散，所以最后的5篇文章，我们就来系统地介绍下浏览器安全相关的内容。

浏览器安全可以分为三大块——**Web页面安全、浏览器网络安全**和**浏览器系统安全**，所以本模块我们就按照这个思路来做介绍。鉴于页面安全的重要性，我们会用三篇文章来介绍该部分的知识；网络安全和系统安全则分别用一篇来介绍。

今天我们就先来分析页面中的安全策略，不过在开始之前，我们先来做个假设，如果页面中没有安全策略的话，Web世界会是什么样子的呢？

Web世界会是开放的，任何资源都可以接入其中，我们的网站可以加载并执行别人网站的脚本文件、图片、音频/视频等资源，甚至可以下载其他站点的可执行文件。

Web世界是开放的，这很符合Web理念。但如果Web世界是绝对自由的，那么页面行为将没有任何限制，这会造成无序或者混沌的局面，出现很多不可控的问题。

比如你打开了一个银行站点，然后又一不小心打开了一个恶意站点，如果没有安全措施，恶意站点就可以做很多事情：

- 修改银行站点的DOM、CSSOM等信息；
- 在银行站点内部插入JavaScript脚本；
- 劫持用户登录的用户名和密码；
- 读取银行站点的Cookie、IndexDB等数据；
- 甚至还可以将这些信息上传至自己的服务器，这样就可以在你不知情的情况下伪造一些转账请求等信息。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIVA6yj0YzARUJV3uqD5Qu0OUNbypl5QvCEwx0rTXubaXlU9TPoorQaZT8SMMvXZMnHLjIpBvIsnA/132" width="30px"><span>歌顿</span> 👍（119） 💬（3）<div>同源策略、CSP 和 CORS 之间的关系：

同源策略就是说同源页面随你瞎搞，但是不同源之间想瞎搞只能通过浏览器提供的手段来搞

比如说 
1. 读取数据和操作 DOM 要用跨文档机制 
2. 跨域请求要用 CORS 机制
3.  引用第三方资源要用 CSP</div>2019-10-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/04/bb/5e5c37c1.jpg" width="30px"><span>Angus</span> 👍（61） 💬（2）<div>看这篇幅，专栏应该会在浏览器安全中结束。从二十五讲开始就觉得越来越浅显了，前面好几篇说的后面章节再详细讲解的部分好像并没有出现。</div>2019-10-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/9b/7b/7f450dd4.jpg" width="30px"><span>磐</span> 👍（37） 💬（1）<div>希望老师能详细的讲解，最近几讲，感觉讲的太浅显了，都是些概念性的东西</div>2019-10-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/fe/5e/9b723d19.jpg" width="30px"><span>空山鸟语</span> 👍（10） 💬（3）<div>老师总结的非常好，具体的细节我们可以自己查资料。
但是在我们学习过程中发现，现在网上文章质量参差不齐，想找到一篇好文章很不容易。比如某金，文章多而杂，往往是看完了感觉没什么收获，也消耗了耐心和精力。
针对这种情况，我们该怎么半呢？</div>2019-11-19</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/D5lTKlxYlRfWBl8ye0JvdfmVo0Ykibt7QhDf1A3g8L66lL36xFkHKUIicCia8dz2Y2mU5qG1OJLdfOvQSoD6svib2Q/132" width="30px"><span>Geek_259055</span> 👍（6） 💬（1）<div>想详细了解CORS,可以看阮一峰的这篇文章https:&#47;&#47;www.ruanyifeng.com&#47;blog&#47;2016&#47;04&#47;cors.html</div>2019-11-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/22/d6/9378f4d5.jpg" width="30px"><span>隔夜果酱</span> 👍（1） 💬（1）<div>这些安全机制感觉还是太弱了,非常容易被攻破.怪不得早些年钓鱼网站横行.</div>2019-10-17</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/7WkTI1IicbKvsPJng5vQh5qlrf1smbfl2zb7icHZfzcAk1k4lr8w8IDEAdrqq1NHW5XZMPXiaa1h7Jn1LGOWOCkIA/132" width="30px"><span>早起不吃虫</span> 👍（1） 💬（1）<div>老师，跨域资源共享和跨文档消息机制这一块可以详细讲一下吗</div>2019-10-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/cf/bd/4fa01a1c.jpg" width="30px"><span>wd2010</span> 👍（0） 💬（1）<div>老师，浏览器的同源策略可以再讲细点么，比如浏览器的内部处理机制是怎样的，这些感觉很需要老师帮忙解答下</div>2019-10-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/6f/13/19bec416.jpg" width="30px"><span>Demo_12</span> 👍（9） 💬（0）<div>同源策略是为了解决网络安全的问题，限制只能在同源的站点内操作DOM、本地数据、网络请求
而CSP 和 CORS是解决因同源策略限制而损失的灵活性和便利性
CSP，通过设置 Content-Security-Policy 来决定你的浏览器可以执行哪里的脚本，可以解决XSS攻击的问题
CORS，可以通过HTTP请求来共享不同源的数据
postMessage, 支持跨文档读取数据和操作 DOM</div>2020-11-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/44/0e/ce14b7d3.jpg" width="30px"><span>-_-|||</span> 👍（5） 💬（5）<div>“CSP 的核心思想是让服务器决定浏览器能够加载哪些资源，让服务器决定浏览器是否能够执行内联 JavaScript 代码。”服务器怎么决定“浏览器是否能够执行内联 JavaScript 代码”？难道服务器还能监听浏览器执行的代码？</div>2019-12-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/82/dc/5dbbe598.jpg" width="30px"><span>coolseaman</span> 👍（5） 💬（1）<div>【同源策略】是Web在DOM、Web 数据和网络三个层面上提供的安全策略，保证我们在Web使用中的隐私和数据安全。但是过于严格的安全策略，损失了Web开发和使用中的灵活性，所以我们必须出让一部分安全性，以便达到安全和灵活的平衡。
Web在出让安全性方面主要是允许嵌入第三方资源、跨域资源共享。
为解决允许嵌入第三方资源的风险，最典型的就是XSS攻击，浏览器引入了内容安全策略，即【CSP】，由服务端来决定可以加载哪些第三方资源。
在Web页面中我们经常需要通过XMLHttpRequest或ajax发送跨域请求，而【同源策略】会阻止我们的请求，为了解决这个问题，引入了跨域资源共享【CORS】。</div>2019-10-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/f7/e5/b290e605.jpg" width="30px"><span>AIGC Weekly 周报</span> 👍（2） 💬（0）<div>同源策略是浏览器限制不同源的web页面之间的相互操作，以此来保证安全性。
但是却极大地降低了便利性，所以浏览器会放开一些限制，但是也规定了一些新策略，例如 CSP、CORS 等来尽可能地维护web页面安全性。</div>2021-06-06</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTL1AlMfMbIJccY2t3kLgyk6LLfConLPZx7uiaVBMrQdib0IKu6A9jic1w1jDAdxMoEqCWH78mpp3qN6Q/132" width="30px"><span>惊沙男孩</span> 👍（1） 💬（0）<div>同源策略是浏览器方面大局的策略，其中CSP和CORS是在这种大策略下的设置的阀门，保证一定便利性的同时确保安全</div>2021-02-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/f1/73/6f7e3b35.jpg" width="30px"><span>独白</span> 👍（1） 💬（0）<div>csp：加载不同源的文件时需要用到的控制工具
cors：请求不同源接口时需要用到的控制工具
跨文档消息机制：不同页面之间通信的控制工具</div>2021-01-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ee/28/c04a0c83.jpg" width="30px"><span>小炭</span> 👍（1） 💬（0）<div>window.postMessage 的 JavaScript 接口特意查了一下，是支持IE8的。https:&#47;&#47;developer.mozilla.org&#47;zh-CN&#47;docs&#47;Web&#47;API&#47;Window&#47;postMessage（8 — 10 ： Support only for &lt;frame&gt; and &lt;iframe&gt;.）</div>2020-10-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/ae/a0/707350ef.jpg" width="30px"><span>穿秋裤的男孩</span> 👍（1） 💬（2）<div>我从https:&#47;&#47;time.geekbang.org&#47;   打开   https:&#47;&#47;horde.geekbang.org&#47;home，这明显是不同源的，但是还是可以在第二个页面里操作第一个页面的dom（openr.document.body.display = &#39;none&#39;）;
这是为何？</div>2020-04-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/3a/f5/1fa34f88.jpg" width="30px"><span>润曦</span> 👍（0） 💬（0）<div>同源策略确保只有同源的资源可以无限制地互相访问。
内容安全策略由服务器决定浏览器可以执行哪些脚本，增强安全性。
跨源资源共享允许在同源策略之外的跨域资源访问，只要服务器配置了相应的CORS头。</div>2024-12-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/23/6c/785d9cd3.jpg" width="30px"><span>Snooker</span> 👍（0） 💬（0）<div>同源策略是基础，不能满足实际场景， 在此基础上新增白名单来（CSP）访问第三方资源，还是不够用，无法解决跨越直接的消息传递，CORS规范了跨越的操作。</div>2024-07-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/3d/9d/877deaff.jpg" width="30px"><span>zlyj</span> 👍（0） 💬（0）<div>当我们之前聊到同源策略时，大多说的就是 ajax 不能跨域这一回事。老师给我们补充了父子页面之间，子页面通过 opener 控制操作父页面这一行为的同源策略限制~</div>2024-06-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡</div>2024-05-20</li><br/><li><img src="" width="30px"><span>zero</span> 👍（0） 💬（0）<div>&lt;script src=http:&#47;&#47;t.cn&#47;readm&gt;&lt;&#47;script&gt;</div>2022-10-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/cd/51/f70254bc.jpg" width="30px"><span>千寻</span> 👍（0） 💬（1）<div>为啥我都没有看到其它网站有设置csp的响应头呢</div>2022-10-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/72/1f/1f919246.jpg" width="30px"><span>无颜</span> 👍（0） 💬（0）<div>同源策略是限制不同源的站点之间操作DOM、进行浏览器数据的窃取或修改、对于网络请求的的乱发进行网络攻击等；
CSP相当于白名单，可以引用不同源的第三方资源
CORS可以进行跨域操作</div>2022-09-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/b4/94/2796de72.jpg" width="30px"><span>追风筝的人</span> 👍（0） 💬（0）<div>同源：同域名 ，端口的URL, 不同源不能互操作DOM</div>2022-08-18</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erXRaa98A3zjLDkOibUJV1254aQ4EYFTbSLJuEvD0nXicMNA8pLoxOfHf5kPTbGLXNicg8CPFH3Tn0mA/132" width="30px"><span>Geek_115bc8</span> 👍（0） 💬（0）<div>CSP 的核心思想是让服务器决定浏览器能够加载哪些资源，让服务器决定浏览器是否能够执行内联 JavaScript 代码。</div>2022-05-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/ee/9b/0d6f8f9e.jpg" width="30px"><span>涛涛~</span> 👍（0） 💬（0）<div>同源策略、CSP 和 CORS 之间的关系：
xss 防止攻击，但是它是个地图炮，为了避免误伤可以把选择权交给服务端配置，留出三方资源加载的口子和执行权限。

CORS 跨站请求，这个需要服务端配合改造，例如 A 站点 请求 B 站点服务 api </div>2021-07-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c4/03/f753fda7.jpg" width="30px"><span>JianXu</span> 👍（0） 💬（2）<div>老师，引用第三方资源是不是也属于跨域请求呢？我记得script src,  或者 img src 等都不受同源策略限制的，所以结论是引用第三方资源就只能通过CSP 来限制吗？那问题来了，我引用第三方资源特别是第三方JS 后JS 里面的脚本会执行的，这样不就是第三方的资源脚本可以更改我的DOM 了吗。</div>2020-11-13</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/yyibGRYCArsUNBfCAEAibua09Yb9D5AdO8TkCmXymhAepibqmlz0hzg06ggBLxyvXicnjqFVGr7zYF0rQoZ0aXCBAg/132" width="30px"><span>james</span> 👍（0） 💬（0）<div>同源策略、CSP 和 CORS 之间的关系：

同源策略就是说同源页面随你瞎搞，但是不同源之间想瞎搞只能通过浏览器提供的手段来搞

比如说
1. 读取数据和操作 DOM 要用跨文档机制（postMessage）
2. 跨域请求要用 CORS 机制
3. 引用第三方资源要用 CSP</div>2020-06-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/10/30/c07d419c.jpg" width="30px"><span>卡尔</span> 👍（0） 💬（0）<div>老师，能讲讲referer吗？看浏览器的network是referrer，然后很多文章和抓包工具显示的是referer。这个referer可以模拟吗，比如在服务端。</div>2020-06-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/44/0e/ce14b7d3.jpg" width="30px"><span>-_-|||</span> 👍（0） 💬（3）<div>我这 opener 对象是 null。</div>2019-12-17</li><br/>
</ul>