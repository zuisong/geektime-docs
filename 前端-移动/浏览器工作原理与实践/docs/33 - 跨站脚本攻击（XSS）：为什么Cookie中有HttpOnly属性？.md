通过[上篇文章](https://time.geekbang.org/column/article/151370)的介绍，我们知道了同源策略可以隔离各个站点之间的DOM交互、页面数据和网络通信，虽然严格的同源策略会带来更多的安全，但是也束缚了Web。这就需要在安全和自由之间找到一个平衡点，所以我们默认页面中可以引用任意第三方资源，然后又引入CSP策略来加以限制；默认XMLHttpRequest和Fetch不能跨站请求资源，然后又通过CORS策略来支持其跨域。

不过支持页面中的第三方资源引用和CORS也带来了很多安全问题，其中最典型的就是XSS攻击。

## 什么是XSS攻击

XSS全称是Cross Site Scripting，为了与“CSS”区分开来，故简称XSS，翻译过来就是“跨站脚本”。XSS攻击是指黑客往HTML文件中或者DOM中注入恶意脚本，从而在用户浏览页面时利用注入的恶意脚本对用户实施攻击的一种手段。

最开始的时候，这种攻击是通过跨域来实现的，所以叫“跨域脚本”。但是发展到现在，往HTML文件中注入恶意代码的方式越来越多了，所以是否跨域注入脚本已经不是唯一的注入手段了，但是XSS这个名字却一直保留至今。

当页面被注入了恶意JavaScript脚本时，浏览器无法区分这些脚本是被恶意注入的还是正常的页面内容，所以恶意注入JavaScript脚本也拥有所有的脚本权限。下面我们就来看看，如果页面被注入了恶意JavaScript脚本，恶意脚本都能做哪些事情。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/f5/b8/9f165f4b.jpg" width="30px"><span>mfist</span> 👍（6） 💬（6）<div>跨站脚本攻击前端和后端7 3分吧。毕竟是在浏览器上面出了问题，前端怎么解释也是自己的锅。
存储型xss和反射型的xss一个原则不要信任前端的输入，任何前端的输入东西都进行编码。这个地方出了问题后端是有责任的
基于dom的xss，传输过程中被篡改，用https之后会防止全部场景吗？ </div>2019-10-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/31/bc/c4f31fa5.jpg" width="30px"><span>杨越</span> 👍（47） 💬（1）<div>内容安全策略( CSP )详细文档：https:&#47;&#47;developer.mozilla.org&#47;zh-CN&#47;docs&#47;Web&#47;HTTP&#47;CSP</div>2020-03-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/23/6c/785d9cd3.jpg" width="30px"><span>Snooker</span> 👍（30） 💬（1）<div>除去架构不谈，就产品、后端、前端、测试而言。
产品：
1.业务逻辑层面安全验证，保证即使被攻击也要尽量避免或减少损失，如：资金转出、敏感信息操作（修改登录密码、支付密码）等
后端：
1.存储型和反射性XSS，后端占比较大，考虑到可以通过接口绕过前端，所以内容编码后端处理比较可靠。
2.重点头信息返回httponly，这也需要后端实现
前端：
1.基于 DOM 的 XSS 攻击，CSP等前端技术运用，这边主要是前端
测试：
1.丰富测试框架，正对输入框：长度、类型、是否为空、是否重复、组成范围外，也应了解学习安全性测试：XSS攻击、Sql注入等攻击类型。
总体而言，个人觉得前端在XSS攻击中责任占比不大。</div>2020-06-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ec/13/49e98289.jpg" width="30px"><span>neohope</span> 👍（17） 💬（1）<div>其实对于跨站攻击，前端应该承担的责任并不高，原因如下：
1、前端的JS代码，在提交表单时，处理特殊字符或处理脚本的函数，完全可以被绕过。所以依赖前端代码彻底解决注入问题，本身就是不可能的，无论如何后端要做好
2、可以通过浏览器插件，进行伪装，随意组织想提交的内容，和前端没有关系
3、网站设置、服务器安全策略，应该是网站运维和安全组的事情，和前端关系也不大
4、测试放过安全bug，也有一定责任
5、其实在框架层，已经做了不少这方面的防范，无论是前端还是后端，所以框架组也要负责
6、如果被注入脚本了，要防止脚本运行，让浏览器按text处理而不是脚本处理，这个前端要负责的。但被注入本身后端责任更大，所以相当于前端背锅了。
</div>2020-07-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/c9/ba/f50e9ea4.jpg" width="30px"><span>潘启宝</span> 👍（10） 💬（0）<div>&lt;meta http-equiv=&quot;Content-Security-Policy&quot; content=&quot;default-src &#39;self&#39;; img-src https:&#47;&#47;*; child-src &#39;none&#39;;&quot;&gt;</div>2019-10-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（8） 💬（0）<div>前端首先要能够意识到有这个攻击的可能性，然后配合后端人员把这些漏洞修复上。其次应该加强测试方的渗透测试，重视安全。</div>2019-10-19</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/7WkTI1IicbKvsPJng5vQh5qlrf1smbfl2zb7icHZfzcAk1k4lr8w8IDEAdrqq1NHW5XZMPXiaa1h7Jn1LGOWOCkIA/132" width="30px"><span>早起不吃虫</span> 👍（6） 💬（7）<div>老师请教一个问题，ＣＳP是可以通过meta标签设置的，如果恶意插入的是关于CSP的meta设置呢？</div>2019-10-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/1e/71/54ff7b4e.jpg" width="30px"><span>3Spiders</span> 👍（5） 💬（5）<div>前端需要负大部分责任，因为如果你只是添加字符串，却使用了添加DOM的操作，这不是给XSS攻击留下机会吗。如果非要添加DOM操作，也应该对script、meta等脚本标签做过滤。至于cookie的窃取，正如老师所说，设置httpOnly就行，我总认为前端操作cookie是一种不安全的手段。</div>2019-10-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e6/39/07fe1fbc.jpg" width="30px"><span>niexia</span> 👍（3） 💬（0）<div>关于 CSP，可以看一下 MDN 的说明 https:&#47;&#47;developer.mozilla.org&#47;zh-CN&#47;docs&#47;Web&#47;HTTP&#47;CSP</div>2019-12-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/fb/30/ba06482a.jpg" width="30px"><span>anthonyliu</span> 👍（2） 💬（4）<div>老师！我有个疑问：“黑客拿到了用户 Cookie 信息之后，就可以利用 Cookie 信息在其他机器上登录该用户的账号”。黑客的服务器拿到用户的cookie信息，怎么在黑客的客户端模拟登录了？是cookie中有用户的登录名和密码吗？我觉得这个不太可能。如果这不可能，那是什么情况下，黑客可以通过cookie来登录？</div>2021-01-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/2d/5f/f648ec62.jpg" width="30px"><span>覃</span> 👍（2） 💬（5）<div>基于dom的攻击，https应该能完全防护吧。</div>2019-10-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/c4/7c/fa60f86f.jpg" width="30px"><span>kelinlawu</span> 👍（1） 💬（0）<div>&lt;script&gt;alert(&#39;你被xss攻击了&#39;)&lt;&#47;script&gt;</div>2022-09-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/ae/c1/76a9237f.jpg" width="30px"><span>昵称</span> 👍（1） 💬（0）<div>前端不主动innerHTML的话，都和前端责任不大。存储型、反射型的源头都是服务端不做过滤、转码。Dom插入攻击是第三方插入的，如wifi路由器、运营商等，这个就没办法了，前端只能通过csp配置一下策略，还有最好就是上https了。</div>2020-07-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ef/a2/6ea5bb9e.jpg" width="30px"><span>LEON</span> 👍（1） 💬（3）<div>请教老师。存储型XSS是不是也可以修改DOM进行攻击。这种方式和DOM型XSS有什么区别？</div>2019-12-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/22/d6/9378f4d5.jpg" width="30px"><span>隔夜果酱</span> 👍（1） 💬（1）<div>比如Chrome扩展，油猴脚本这些应该算基于dom的xss么？对于基于dom的攻击，网站就没有办法了吧。</div>2019-10-19</li><br/><li><img src="" width="30px"><span>jevonli</span> 👍（0） 💬（0）<div>请教李老师一个问题，如果用户用的浏览器本身就是不正规的，比如由黑客修改后的版本，那会发生什么？</div>2024-07-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/67/fa/720f57fa.jpg" width="30px"><span>zer0fire</span> 👍（0） 💬（0）<div>学习打卡</div>2024-06-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡</div>2024-05-21</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/WKgD4vjLMhG5Tb0wFrYQ3prJpMSQgb1iabUNyPEk6cHDVWgHJCOicLVx38Ax3xqB2BrzpIpvlrPMCWjgNL6icXicPg/132" width="30px"><span>过客</span> 👍（0） 💬（0）<div>&lt;script&gt;alert(&#39;你被xss攻击了&#39;)&lt;&#47;script&gt;</div>2023-11-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/1f/14/57cb7926.jpg" width="30px"><span>ShawnWu</span> 👍（0） 💬（0）<div>那段代码怎么跑起来啊</div>2022-08-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/8a/d6/00cf9218.jpg" width="30px"><span>撒哈拉</span> 👍（0） 💬（0）<div>有三种 xss攻击，存储型，反射型，修改dom型

防范方式主要是，

1，从用户输入角度，服务器进行限制

2，从csp，内容安全角度浏览器限制

3，限制 cookie，不能被JavaScript读取</div>2021-11-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/8a/d6/00cf9218.jpg" width="30px"><span>撒哈拉</span> 👍（0） 💬（0）<div>xss 攻击，也叫跨站脚本攻击，主要是插入script标签，执行恶意脚本，获取用户登录数据，发给第三方服务器，然后伪造用户登录信息，进行不法行为。
</div>2021-11-15</li><br/><li><img src="" width="30px"><span>Geek_feca44</span> 👍（0） 💬（0）<div>反射型 XSS 跟存储型 XSS 的区别是：存储型 XSS 的恶意代码存在数据库里，反射型 XSS 的恶意代码存在 URL 里。

DOM 型 XSS 跟前两种 XSS 的区别：DOM 型 XSS 攻击中，取出和执行恶意代码由浏览器端完成，属于前端 JavaScript 自身的安全漏洞，而其他两种 XSS 都属于服务端的安全漏洞。</div>2021-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/10/5e/42f4faf7.jpg" width="30px"><span>天择</span> 👍（0） 💬（0）<div>前端工程师应当假设服务端没有对XSS做防护。</div>2021-08-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/a2/92/6bbcb80b.jpg" width="30px"><span>1979104101ng</span> 👍（0） 💬（0）<div>示例代码里的&lt;%- xss &gt; 的 %- 表示  &lt;%- 输出非转义的数据到模板 ，所以从服务器发送到前端就变成了 script 标签</div>2021-07-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/f6/9c/68b97b7a.jpg" width="30px"><span>不二</span> 👍（0） 💬（0）<div>&lt;script&gt;alert(&#39;你被xss攻击了&#39;)&lt;&#47;script&gt;</div>2021-06-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/23/6c/785d9cd3.jpg" width="30px"><span>Snooker</span> 👍（0） 💬（0）<div>老师好，针对系统内已存在的存储型xss漏洞要如何修复？是需要前端修改页面解析逻辑？
后端修改数据存储逻辑吗？</div>2021-01-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/6f/13/19bec416.jpg" width="30px"><span>Demo_12</span> 👍（0） 💬（0）<div>我觉得前端对产品也需要有主人翁的意识
首先是前端自己可做到的，对于XSS攻击的预防策略，设置CSP，前端提交内容时先经过一层编码处理
其他需要后端的，后端编码处理和设置CORS&#47;cookie http-only 这些可以推动后端去设置
但是，也不能轻易背锅</div>2020-11-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ee/28/c04a0c83.jpg" width="30px"><span>小炭</span> 👍（0） 💬（0）<div>应该负责任的，至少要避免明显的安全问题。有职业追求的人都应该对自己的工作负责。</div>2020-10-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/4d/e8/b94f7438.jpg" width="30px"><span>CaptainJack</span> 👍（0） 💬（0）<div>如果真要说，那么我认为是前端安全占10%，后端占90%，是提供服务的安全性，前端再怎么处理，都很难从根节点去解决安全问题，安全问题的核心，在传输和业务入口，而非前端，前端可以配合来做，提升破解的难度，但是还是那句话，安全的根源，不在前端</div>2020-09-12</li><br/>
</ul>