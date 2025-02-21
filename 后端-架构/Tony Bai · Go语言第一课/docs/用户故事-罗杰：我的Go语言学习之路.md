你好，我是罗杰，目前在一家游戏公司担任后端开发主程。今天，我想跟你分享一下我学习Go的一些经历，如果你还是一个Go新人，希望我的这些经历，能给你带来一些启发和帮助。

说起来，我接触Go语言已经很久了，但前面好多次都没真正学起来。

我第一次接触 Go 语言是在 2010 年，当时我还在读大二，一个学长建议我了解一下 Go 语言，毕竟是谷歌出的一门语言，可能未来比较有发展前景。所以我当时下载并安装了Go的开发环境，还写了个 “hello world”，但是由于没有中文的教程，也没有人一起学习，学习 Go 语言这件事情很快就被我抛在脑后了。

我第二次接触Go是在 2015 年。当时我跟在豆瓣工作的发小聊天，我说最近想学 Python，他却坚定地告诉我学 Go。因为他们团队无法忍受 Python 总是半夜异常导致全站挂掉，正在往 Go 迁移。但我当时并没有给予足够的重视，没有学半个月又去玩了。

第三次接触Go语言是在 2017 年。我当时的技术栈只有 C++，对于 Web 服务这块，几乎没有任何经验，而且我们组的其他成员也没有相关经验。我就在想，总不能 Web 服务这一块总是向其他项目组“借”个 PHP 的同学过来协助吧？

于是，我开始再次尝试学习使用 Go 语言，并且因为一篇《[Go语言TCP Socket编程](https://tonybai.com/2015/11/17/tcp-programming-in-golang/)》的博客认识了 Tony Bai 老师。当时我考虑把原本用 C++ 写的游戏服务改成用 Go 来实现，但当时能用中文搜索到的与 TCP 网络编程的文档非常有限，而Tony Bai 老师的文章写得非常详细，使我对 Go 是如何做这一部分有了基本的了解。
<div><strong>精选留言（16）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/1d/de/62bfa83f.jpg" width="30px"><span>aoe</span> 👍（10） 💬（6）<div>原来是 C++ 大佬！
感谢分享 gin 不然我也会天真的认为要什么框架，直接写 web 不行吗？
谢谢分享了很多优秀资源
这个专栏是我第三次学 Go 了，感觉要学会了</div>2022-01-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/ea/7a/d857723d.jpg" width="30px"><span>Vfeelit</span> 👍（9） 💬（1）<div>这个同学就讲得很好 我也学习过很多门语言 go是我最喜爱的 没有之一</div>2022-01-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/8a/89/8940ea1e.jpg" width="30px"><span>小戈</span> 👍（2） 💬（2）<div>游戏服务器开发怎么学</div>2022-01-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d7/bf/a200e7a7.jpg" width="30px"><span>和白白</span> 👍（2） 💬（2）<div>杰哥🐮，本文提到的方法这段时间学习专栏感受很深，确实要复习，阶段总结，不然就成了走马观花，很容易忘个光。
所以这段时间课程中的代码我都尽可能都敲一遍，发现很多看似简单的代码实际动手了还是没有思路。不过一定要切记不能抄代码，可以先列出注释，然后照着注释动手，有些过去的知识点也可以在写代码过程中有意识的融合进去，加深自己的理解。</div>2021-12-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/90/23/5c74e9b7.jpg" width="30px"><span>$侯</span> 👍（2） 💬（2）<div>老师可以催更吗，无聊开始二刷了哈哈</div>2021-12-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/33/9a/f295dea5.jpg" width="30px"><span>李正g</span> 👍（1） 💬（1）<div>第二次学，希望能有所成就</div>2023-03-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/34/01/30ca98e6.jpg" width="30px"><span>arronK</span> 👍（1） 💬（1）<div>分享学习方法
1. 拆分大的知识内容为小的知识模块
2. 专注刻意练习每个模块
3. 构建知识体系（建立知识之间的联系）
4. 用起来或教别人
5. 间隔性的检索（不是看着书复习，而是什么都不看，能不能像给人上课一样把整个知识体系全盘托出，如果不能请回到 2 重复）</div>2022-04-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/b8/d8/f81b5604.jpg" width="30px"><span>hcyycb</span> 👍（1） 💬（1）<div>罗杰同学优秀啊，学习</div>2021-12-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/2e/ca/469f7266.jpg" width="30px"><span>菠萝吹雪—Code</span> 👍（0） 💬（1）<div>和优秀的人在一起！</div>2022-08-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/ef/4d/83a56dad.jpg" width="30px"><span>Z.</span> 👍（0） 💬（1）<div>初次接触go，感觉真的很难，希望能坚持下去
</div>2022-07-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c9/10/65fe5b06.jpg" width="30px"><span>J²</span> 👍（0） 💬（1）<div>我叫李杰，希望有一天也能像罗杰一样优秀。😄</div>2022-03-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/7b/bd/ccb37425.jpg" width="30px"><span>进化菌</span> 👍（0） 💬（1）<div>不刻意去练习，真的太容易忘记以及放弃了。系统去学习go，用go~</div>2021-12-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/46/af/c20a8244.jpg" width="30px"><span>南极熊</span> 👍（0） 💬（1）<div>罗杰同学优秀，向罗杰学习</div>2021-12-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/b1/54/6d663b95.jpg" width="30px"><span>瓜牛</span> 👍（6） 💬（0）<div>说下我为什么购买此课程吧，之前搜grpc问题搜到过作者的博客，阅读下来感觉很好，能感受到作者功力深厚，写文章抽丝剥茧，娓娓道来，于是就购买课程支持一下。之前也买过极客时间另一个go课程，作者的语言表达能力真是不敢恭维，总是自创一些词汇，看得十分吃力，能把人当场说晕过去。（当时也吐槽了一下，没想到主编还给我退钱了😢）最后说下学习方法，学习这么多年了，每个人应该都有自己的学习方法，适合自己的才是最好的。</div>2022-04-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/dd/7d/5d3ab033.jpg" width="30px"><span>不求闻达</span> 👍（0） 💬（0）<div>谢谢分享学习心得，谢谢分享很多优秀资源。</div>2023-04-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/30/67/a1e9aaba.jpg" width="30px"><span>Roway</span> 👍（0） 💬（0）<div>怎样加罗杰？</div>2022-07-08</li><br/>
</ul>