你好，我是陈天。

作为被线上业务毒打过的开发者，我们都对墨菲定律刻骨铭心。任何一个系统，只要运行的时间足够久，或者用户的规模足够大，极小概率的错误就一定会发生。比如，主机的磁盘可能被写满、数据库系统可能会脑裂、上游的服务比如 CDN 可能会宕机，甚至承载服务的硬件本身可能损坏等等。

因为我们平时写练习代码，一般只会关注正常路径，可以对小概率发生的错误路径置之不理；**但在实际生产环境中，任何错误只要没有得到妥善处理，就会给系统埋下隐患**，轻则影响开发者用户体验，重则会给系统带来安全上的问题，马虎不得。

在一门编程语言中，控制流程是语言的核心流程，而错误处理又是控制流程的重要组成部分。

语言优秀的错误处理能力，会大大减少错误处理对整体流程的破坏，让我们写代码更行云流水，读起来心智负担也更小。  
![](https://static001.geekbang.org/resource/image/5b/a0/5bd062993b268ea982708203a4e2a5a0.jpg?wh=2485x1046)

对我们开发者来说，错误处理包含这么几部分：

1. 当错误发生时，用合适的错误类型捕获这个错误。
2. 错误捕获后，可以立刻处理，也可以延迟到不得不处理的地方再处理，这就涉及到错误的传播（propagate）。
3. 最后，根据不同的错误类型，给用户返回合适的、帮助他们理解问题所在的错误消息。

作为一门极其注重用户体验的编程语言，Rust 从其它优秀的语言中，尤其是 Haskell ，吸收了错误处理的精髓，并以自己独到的方式展现出来。
<div><strong>精选留言（14）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/f7/1b/db7a0edc.jpg" width="30px"><span>Marvichov</span> 👍（7） 💬（2）<div>https:&#47;&#47;github.com&#47;dtolnay&#47;thiserror

&gt; Use **thiserror** if you care about designing your own dedicated error type(s) so that the caller receives exactly the information that you choose in the event of failure. This most often applies to library-like code. Use **Anyhow** if you **don&#39;t care** what error type your functions return, you just want it to be easy. This is common in application-like code.</div>2021-12-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/62/e0/d2ff52da.jpg" width="30px"><span>记事本</span> 👍（5） 💬（1）<div>这章比较简单，打卡！</div>2021-10-04</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLBFkSq1oiaEMRjtyyv4ZpCI0OuaSsqs04ODm0OkZF6QhsAh3SvqhxibS2n7PLAVZE3QRSn5Hic0DyXg/132" width="30px"><span>ddh</span> 👍（2） 💬（1）<div>之前看过rust错误处理的知识，不是很清稀，今天完全明朗了， 哈哈</div>2021-11-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/70/67/0c1359c2.jpg" width="30px"><span>qinsi</span> 👍（2） 💬（1）<div>golang 中可用 errors.Errorf 或 (go1.13+)fmt.Errorf 实现错误嵌套。

大致看了下rust中要实现相同的功能的话，也是要先定义自定义的错误类型，然后实现Error trait。这一步可以手动实现，或是使用thiserror来derive。wrap错误时则可以用Box&lt;Error&gt;或anyhow，不过就失去了自定义错误类型的好处。还是通过thiserror来生成From trait的实现为好，这样就可以通过`?`一路&quot;开火车&quot;下去了。

有意思的是上述golang中的errors pkg原本就是为了解决标准库中Error无法嵌套等问题而产生的第三方库，在社区流行开之后就被标准库吸收了其中的思想。rust生态中的错误处理应该也会经历相似的发展阶段吧。
</div>2021-10-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/26/27/eba94899.jpg" width="30px"><span>罗杰</span> 👍（2） 💬（1）<div>第一时间打卡</div>2021-10-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/8e/31/28972804.jpg" width="30px"><span>阿海</span> 👍（1） 💬（1）<div>从这章就可以看出老师平时理解了很多技术领域的东西，很想知道老师有博客之类的的吗</div>2021-10-04</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIDqHQQByGiaXcAk94MdDn3ftupZLXyR6bAKibxOzMxy5h3uBwZ7QiaCiaIfbCMK0cIQfGNax8iawoiaQAg/132" width="30px"><span>nuan</span> 👍（13） 💬（0）<div>晕了几章后，稍稍轻松一下。</div>2022-02-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/62/b1/3d1fc497.jpg" width="30px"><span>三万棵树</span> 👍（1） 💬（1）<div>不黑不吹，讲解真的清晰，对比某些人的专栏，简直是优秀</div>2024-02-22</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eoHxiazYcQJA3J7GBbQtpXgbjl6clYDHdK0H0I0ibNzajNoMq1Xb6mTlzbrAicgRNHB3L9b93icLZWqkw/132" width="30px"><span>Geek_6b6c0a</span> 👍（1） 💬（0）<div>Railroad oriented programming 是我最喜欢的talk之一，没想到在这里看到了哈哈</div>2023-02-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/39/08/2b/7a1fb4ff.jpg" width="30px"><span>David.Du</span> 👍（0） 💬（0）<div>学到了，谢谢！！</div>2023-11-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/31/4c/2f/af2c8d1b.jpg" width="30px"><span>杨学者</span> 👍（0） 💬（0）<div>请教rust如何对错误进行打印traceback？我发现anyhow和traceback-rs可以打印，this error好像不行，不过anyhow粒度太粗了，不知有啥好办法？</div>2023-01-01</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/TusRVU51UggZGpicXMgH64Cb8jek0wyTOpagtUHNAj0EPbhbEv0FJpFU2K3glbtOdJXiaQ9o6QoEfv5PiaIu7rwng/132" width="30px"><span>Geek_a6c6ce</span> 👍（0） 💬（0）<div>咔哒</div>2022-09-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/7b/b4/9efded98.jpg" width="30px"><span>Kurobane</span> 👍（0） 💬（0）<div>&gt; 开发者也可以对其 unwarp() 或者
unwarp() =&gt; unwrap()</div>2022-06-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7d/4d/d98865b2.jpg" width="30px"><span>老实人Honey</span> 👍（0） 💬（0）<div>连接错误超时
命令错误
空间满
</div>2022-01-20</li><br/>
</ul>