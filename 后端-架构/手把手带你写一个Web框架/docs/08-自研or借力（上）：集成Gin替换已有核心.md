你好，我是轩脉刃。

之前我们从零开始研发了一个有控制器、路由、中间件等组件的 Web 服务器框架，这个服务器框架可以说是麻雀虽小，但五脏俱全。上节课我们还介绍了目前最主流的一些框架 Gin、Echo 和Beego。

这里不知道你有没有这些疑问，我们的框架和这些顶级的框架相比，差了什么呢？如何才能快速地把我们的框架可用性，和这些框架提升到同一个级别？我们做这个框架除了演示每个实现细节，它的优势是什么呢？

不妨带着这些问题，把我们新出炉的框架和GitHub上star数最高的[Gin框架](https://github.com/gin-gonic/gin)比对一下，思考下之间的差距到底是什么。

## 和Gin对比

Gin 框架无疑是现在最火的框架，你能想出很多它的好处，但是在我看来，它之所以那么成功，**最主要的原因在于两点：细节和生态**。

其实框架之间的实现原理都差不多，但是生产级别的框架和我们写的示例级别的框架相比，差别就在于细节，这个细节是需要很多人、很多时间去不断打磨的。

如果你的 Golang 经验积累到一定时间，那肯定能很轻松实现一个示例级别的框架，但是往往是没有开源市场的，因为你的框架，在细节上的设计没有经过很多人验证，也没有经过在生产环境中的实战。这些都需要一个较为庞大的使用群体和较长时间才能慢慢打磨出来。
<div><strong>精选留言（12）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/26/b5/74/cd80b9f4.jpg" width="30px"><span>友</span> 👍（2） 💬（2）<div>老师我准备慢下来 我要把 trie树给优化一下 之前写leetcode的时候这种压缩的情况我比较清楚 我可以尝试一下</div>2021-12-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/70/07/bb4e6568.jpg" width="30px"><span>我是熊大</span> 👍（1） 💬（1）<div>看完第六讲时，看到地下的评论，为作者捏了一把汗，直到第八讲，才松了一口气，每个框架都是无数次优化得到完善的，优秀的人的贡献存在才能让社区更强大</div>2022-11-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/b5/74/cd80b9f4.jpg" width="30px"><span>友</span> 👍（1） 💬（2）<div>只有站在巨人的肩膀才能做得更好。 
这个就是吸取前人经验，自己可以站在巨人肩膀上把事情做的更好或许会让这个巨人更高让别人站在自己肩膀上继续增高</div>2021-12-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/b5/74/cd80b9f4.jpg" width="30px"><span>友</span> 👍（1） 💬（1）<div>感觉老师讲解源码让我会看的很入神 </div>2021-12-03</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/1gKhS58rAibx6KHQhgJNL7k1jsiblXbwJwveqNU0zJJUKLTCDX51haJibicMd6ic3KREezXVqpWqTaGo2Gc9jfFGpdw/132" width="30px"><span>Geek_d217a5</span> 👍（0） 💬（1）<div>indices作用是什么？源码是遍历indices数组找到对应的字符，不能直接遍历childnode的path吗？</div>2021-12-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/b5/74/cd80b9f4.jpg" width="30px"><span>友</span> 👍（0） 💬（1）<div>Eloquent ORM 是真的方便好用，laravel框架本身我就觉得是符合创业公司开发的利器。只不过我个人从刚刚学习听过很多php的言论导致 潜移默化的不喜欢php </div>2021-12-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9a/0f/da7ed75a.jpg" width="30px"><span>芒果少侠</span> 👍（10） 💬（1）<div>gin的query方法，通过本地内存cache缓存了请求的query参数。后续每次读query参数时，都会从内存中直接读，减少了每次都要调用request.Query()方法的计算开销。</div>2021-10-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5e/67/133d2da6.jpg" width="30px"><span>Geek_5244fa</span> 👍（4） 💬（0）<div>众人拾柴火焰高，这个课程这么多人学习，可以一起做一个框架。</div>2021-09-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/d0/7f/1ad28cd3.jpg" width="30px"><span>王博</span> 👍（3） 💬（0）<div>前面的读了好几遍了，真的受益匪浅，期待后续</div>2021-09-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/3a/8c/fc2c3e5c.jpg" width="30px"><span>xl666</span> 👍（1） 💬（0）<div>老师请教下，错误拦截的那个底层连接异常，如果服务器异常，不应该都建立不了tcp连接吗，怎么还能在业务代码中拦截呢。</div>2023-03-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/65/b7/058276dc.jpg" width="30px"><span>i_chase</span> 👍（0） 💬（0）<div>a==&gt;b==&gt;c
c打印出了：a==&gt;b==&gt;c
b打印出了：a==&gt;b</div>2022-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/70/67/0c1359c2.jpg" width="30px"><span>qinsi</span> 👍（0） 💬（1）<div>打印堆栈是对本地开发友好的功能，线上不会那么搞。因为通常部署的时候不会把源码一起部署上线，而且一个个去读取源文件开销也大</div>2021-09-29</li><br/>
</ul>