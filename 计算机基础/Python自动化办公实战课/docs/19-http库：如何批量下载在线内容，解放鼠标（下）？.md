你好，我是尹会生。

在上节课，我们学习了怎么使用“requests-html”库来批量下载图片，这足以帮你应对大部分需要批量下载互联网资源的场景了。

但是除了批量下载这一典型场景外，还有两种场景“requests-html”工具无法覆盖，其中就包括一些网站的每日签到功能，明明登录网站后点击一个按钮就能领到虚拟货币，但是每次还要手动输入账户和密码，再用鼠标点击领取按钮。相信已经学会了如何用Python访问网页的你，早就想把签到进行自动化了吧。

那么今天，我就以京东自动签到领金豆为例，为你介绍一款比“requests-html”更加强大的浏览器工具“selenium”，通过selenium我将带你实现自动化的用户登录和模拟鼠标点击功能。

## selenium的适用场景

我刚才也提到了，在你把“requests-html”库应用到各种批量下载场景之后，你会发现有两种场景下使用“requests-html”无法实现批量下载。

一种场景是，有的网页为了防止你用工具下载，会对下载工具进行检测。如果你的HTTP客户端不是浏览器，那就不允许你访问该网站下的所有内容。

另一种场景是，一些网页为了更好的交互性，就使用了JavaScript脚本语言。而JavaScript脚本语言需要在浏览器运行，才能获得服务器的数据。所以如果使用“requests-html”来获取这些数据的话，你就必须再编写Javascript脚本。
<div><strong>精选留言（8）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1f/23/8f/ab76ccdf.jpg" width="30px"><span>浮华～</span> 👍（0） 💬（2）<div>关于微信授权的 签到小程序也可以这样弄吗</div>2021-10-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/23/66/413c0bb5.jpg" width="30px"><span>LDxy</span> 👍（4） 💬（2）<div>可以开始研究下上下班的自动签到了</div>2021-03-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/7d/c8/9d046773.jpg" width="30px"><span>Eco</span> 👍（0） 💬（1）<div>用 ChatGPT 结合本课程学习了，发现其中有一个问题：
在Selenium 4及以上版本中，find_element_by_xpath方法已被弃用。你应该使用find_element方法配合By.XPATH来替代。</div>2024-03-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/c3/67/568181d7.jpg" width="30px"><span>Jerry</span> 👍（0） 💬（1）<div>老师，完整代码在哪里下载啊</div>2021-06-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/89/73/2deb24ab.jpg" width="30px"><span>武明</span> 👍（0） 💬（2）<div>不添加请求头，不去除window.navigator.webdriver 好像不行吧，直接出滑块了</div>2021-04-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/06/32/3de6a189.jpg" width="30px"><span>范</span> 👍（1） 💬（0）<div>借助http相关类库，DOM结构，可以模拟浏览器很多操作。</div>2021-04-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡</div>2023-07-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/0f/09/e5221743.jpg" width="30px"><span>David</span> 👍（0） 💬（0）<div>这两节结不就是爬虫的操作嘛，密码、验证码的输入的时间控制，在最小值的基础上上还可以使用个random随机函数吧，这样模仿得更像人工操作一些</div>2021-12-30</li><br/>
</ul>