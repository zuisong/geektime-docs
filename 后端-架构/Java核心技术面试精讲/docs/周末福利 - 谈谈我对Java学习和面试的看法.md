你好，我是杨晓峰。今天是周末，我们稍微放松一下来聊聊“Java核心技术”之外的内容，正好也借这个机会，兑现一下送出学习奖励礼券的承诺。我在每一讲后面都留下了一道思考题，希望你通过学习，结合自身工作实际，能够认真思考一下这些问题，一方面起到检验学习效果的作用，另一方面可以查漏补缺，思考一下这些平时容易被忽略的面试考察点。我并没有给出这些思考题的答案，希望你通过专栏学习或者查阅其他资料进行独立思考，将自己思考的答案写在留言区与我和其他同学一起交流，这也是提升自己重要的方法之一。

截止到今天，专栏已经更新了15讲，走完了基础模块正式进入进阶模块。现在也正是一个很好的时机停下来回顾一下基础部分的知识，为后面进阶的并发内容打好基础。在这里，我也分享一下我对Java学习和面试的看法，希望对你有所帮助。

首先，有同学反馈说专栏有的内容看不懂。我在准备专栏文章的时候对一些同学的基础把握不太准确，后面的文章我进行了调整，将重点技术概念进行讲解，并为其他术语添加链接。

再来说说这种情况，有人总觉得Java基础知识都已经被讲烂了，还有什么可学的？

对于基础知识的掌握，有的同学经常是“知其然而不知其所以然”， 看到几个名词听说过就以为自己掌握了，其实不然。至少，我认为应该能够做到将自己“掌握”的东西，**准确地表达出来**。
<div><strong>精选留言（20）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/9b/2f/b7a3625e.jpg" width="30px"><span>Len</span> 👍（4） 💬（1）<div>正文中(非留言区)，倒数第二个推荐的读者留言中说:

“所以一般建议在使用 Netty 时开启 XX:+DisableExplicitGC”。

注意，参数前使用的是  + 号，我觉得不对吧！
这就表明 Ststem.gc 变成空调用了，这对于 Netty，如果这么做会导致堆外内存不及时回收，反而更容易 OOM。

是这样吗？
</div>2018-06-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fc/e5/605f423f.jpg" width="30px"><span>肖一林</span> 👍（4） 💬（1）<div>谢谢老师的奖励，每一篇都在看，最近也在组织以前的笔记，放在自己的技术公众号。希望清理技术债务，达到系统学习的目的。结合以前所学，加上老师文章提到的一些底层原理，用自己的方式表达一遍</div>2018-06-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/44/03/460fda52.jpg" width="30px"><span>bills</span> 👍（1） 💬（1）<div>话说今天不更新了吗，大神能不能加快下更新的速度，学习完去面试，战线时间太长有点熬人</div>2018-06-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/77/b3/991f3f9b.jpg" width="30px"><span>公号-技术夜未眠</span> 👍（39） 💬（0）<div>阅读源码的时候，

首先，可通过各种公开的渠道（google、公开文档等）了解代码的总体框架、模块组成及其模块间的关系；

然后，结合源码的注释进行解读，对不是很明白的部分打断点，调试，甚至可按照自己的想法进行修改后再调试；

最后，对于重点核心模块进行详细调试，可以把核心类的功能、调用流程等写下来，好记性总是敌不过烂笔头的。

除此之外，个人觉得最最重要的是:看源码的时候要有&quot;静气&quot;。</div>2018-06-09</li><br/><li><img src="" width="30px"><span>whhbbq</span> 👍（34） 💬（0）<div>老师的招人标准，学习了，很实用，看了也很有感触。你能填上别人填不上的坑，就成功了。工作中大多数时候的任务目标并不清晰，特别当你是一个团队的小leader时，没人告诉你后面的方向，要做成什么样，很考验能力。</div>2018-06-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/95/96/0020bd67.jpg" width="30px"><span>夏洛克的救赎</span> 👍（13） 💬（0）<div>看评论都能涨知识，希望评论提供交互功能</div>2018-06-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/36/6c/7d5b797e.jpg" width="30px"><span>vash_ace</span> 👍（10） 💬（0）<div>感谢杨老师的鼓励，在受宠若惊之余，我觉得这篇“课外阅读”的参考价值不输于任何一篇技术分享。因为文中提到的这些努力或坚持的方向，确实是对个人职场生涯有着巨大的影响和帮助(亲测有效)。
其实道理大家都懂，但很多时候想当架构相做技术大牛的我们就是会以各种理由(项目忙，赶进度，不想加班...)不去对一个bug或一次线上故障做刨根问底的努力，又或者是放弃原本是对的坚持(比如，技术笔记，技术阅读与分享...)；
那这个时候的你所需要的鸡汤或兴奋剂不再是XXX的成功，而是想象一下自己的个人价值。往大了说，你对技术圈做了什么贡献？影响了多少人？影响越大成就感越满足。成就感是个好东西，你越享受就越会上瘾；往俗了说，就是看看自己的收入在行业内处于什么样的水平？工资多少不一定能完全体现一个人的真实水平，但至少绝大部分公司和猎头都能根据你上一家公司的收入来定位你属于哪一个level。</div>2018-06-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（8） 💬（0）<div>看源码之前，建议补一下数据结构和算法，老师的这个专栏给我莫大的鼓励，感谢，坚持。</div>2018-12-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/36/dc/36b306a2.jpg" width="30px"><span>WWR</span> 👍（7） 💬（0）<div>看源码的时候要“静气”，真的说到点儿了……</div>2018-09-13</li><br/><li><img src="" width="30px"><span>Paul Shan</span> 👍（6） 💬（0）<div>老师招人标准总结起来是能思考，能填坑，能独当一面。</div>2019-11-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/15/02/66f65388.jpg" width="30px"><span>雷霹雳的爸爸</span> 👍（5） 💬（0）<div>意外，感谢，更重要的是也复盘下这段学习过程中发现的自己的各种不足，再接再厉！</div>2018-06-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1a/f3/41d5ba7d.jpg" width="30px"><span>iLeGeND</span> 👍（3） 💬（0）<div>我们应该面向接口编程，面向规范编程，在单纯的开发中，使jdk或者框架，应该以其api文档为参考，如果有问题就看源码，那岂不是面子实现编程了，不同的版本，其实现不见得一样，我们的代码用不能一直改吧</div>2018-06-09</li><br/><li><img src="" width="30px"><span>Paul Shan</span> 👍（2） 💬（0）<div>输入，消化，输出，是学习的不二之选，长期而言我们只是在回答输入哪些内容，如何输入，如何消化，如何输出。阅读书籍，看别人代码，听专栏等是输入。分析思考是消化。总结成文档，用自己的语言表达出来，与人讨论，教别人等是输出，输出可以小到写下思考的一个结果，大到写一本书。这里输出是关键，围绕着输出，输入也更有目的性，输出让消化的好坏也得到检验，而且可以不断迭代分析思考的结果，满足感得以产生，能力得到提升！</div>2019-11-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/a0/a3/8da99bb0.jpg" width="30px"><span>业余爱好者</span> 👍（2） 💬（0）<div>知识不等于能力。重要的是能力而非知识。一些必要的理论知识是解决问题所必须的，但光是学一大堆理论不去应用实践，也是鸡肋。</div>2019-09-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/01/5e/95f7d928.jpg" width="30px"><span>Hidden</span> 👍（1） 💬（0）<div>我在阅读源码的时候，只能勉强理解一半，剩下那一半 再怎么也理解不了，很是奇怪，</div>2018-06-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fe/3c/13175251.jpg" width="30px"><span>Miaozhe</span> 👍（1） 💬（0）<div>感谢杨老师分享，这次学习收获很大，特别是认真阅读了HashMap的源码，桶的设计和Hash的位运算正的设计很妙。以前没有看懂，这次参考老师的&quot;死磕&quot;，终于看懂了。</div>2018-06-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1a/f3/41d5ba7d.jpg" width="30px"><span>iLeGeND</span> 👍（1） 💬（0）<div>我们应该面向接口编程，面向规范编程，在单纯的开发中，使jdk或者框架，应该以其api文档为参考，如果有问题就看源码，那岂不是面子实现编程了，不同的版本，其实现不见得一样，我们的代码用不能一直改吧</div>2018-06-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/53/9b/d0a21378.jpg" width="30px"><span>时代先锋</span> 👍（0） 💬（0）<div>语言的学习是一个漫长并不断渐进的过程，加油😊</div>2020-03-19</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/6LaITPQ4Lk5fZn8ib1tfsPW8vI9icTuSwAddiajVfibPDiaDvMU2br6ZT7K0LWCKibSQuicT7sIEVmY4K7ibXY0T7UQEiag/132" width="30px"><span>尔东橙</span> 👍（0） 💬（0）<div>老师，能不能讲讲设计模式、系统设计这些，面试问这些没项目经验很头大</div>2019-07-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/38/2c/d98e9a46.jpg" width="30px"><span>Zoe.Li</span> 👍（0） 💬（0）<div>谢谢杨老师的分享</div>2018-06-12</li><br/>
</ul>