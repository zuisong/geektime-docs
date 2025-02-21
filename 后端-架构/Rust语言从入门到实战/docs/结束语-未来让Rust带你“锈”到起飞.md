你好，我是你的老朋友 Mike。

30讲的课程很快就结束了，感谢你一路的支持与陪伴，每一次评论区的互动都能让我感觉到写这门课的重要意义。我看到了你在不断思考中对Rust的理解越来越深，畏难情绪也随之一分分减少，很长一段时间我一起床就会打开评论，看看你有哪些新思考、新困惑，这也成了我每天的动力来源。

看到越来越多的朋友加入学习，逐渐“锈”化，我想我写这门课程最基本的目标达到了——让你以比较轻松的心态去掌握Rust的基础知识，为你以后用Rust去解决生产上的难题打下坚实的基础。

在这几个月里我们了解了Rust很多非常重要的特性，对所有权、Trait、类型还有异步编程和Unsafe编程等重要概念有了更深的理解，此外还转变了对Rust小助手的态度，真正把它当成了我们的好伙伴。这都是我们共同努力的结果。

![图片](https://static001.geekbang.org/resource/image/e4/f6/e47a32cf1b0c9561f2994ff5f04154f6.jpg?wh=6924x4500)

而这最后一节课也同样珍贵，所以我还是想再“唠叨唠叨”，带你回顾我们课程里最重要的一些东西。希望你不仅能够掌握基本的Rust代码应该怎么写，还能理解Rust为什么要这样设计。

## Rust所有权是怎么来的？

要说 Rust 里最重要的东西，一定少不了所有权，都说重要的事情说三遍，在课程中我说了又何止三遍，所以我想用这最后一点点宝贵的时间再来讲一讲所有权从何而来，又何以至此的。我们都知道Rust成长于巨人的肩膀上，所以我们可以从C语言说起。
<div><strong>精选留言（12）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/2b/63/57/b8eef585.jpg" width="30px"><span>小虎子11🐯</span> 👍（2） 💬（0）<div>Mike 老师的公众号：跟着 MT 学 Rust，欢迎关注～</div>2024-01-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/0e/df/a64b3146.jpg" width="30px"><span>长林啊</span> 👍（3） 💬（1）<div>再来个系统性进阶实战课吧</div>2024-01-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/c0/24/01699070.jpg" width="30px"><span>Jack Xin</span> 👍（1） 💬（1）<div>我觉得唐老师有一种特别的能力，rust一些复杂难懂的概念在老师的讲述下，却变得通俗易懂，让人觉得兴趣盎然，谢谢老师，学完老师的课让我喜欢上了rust </div>2024-01-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/3e/e8/3736f3cd.jpg" width="30px"><span>冷石</span> 👍（0） 💬（1）<div>拖延症晚期总于学完啦！啊啊啊</div>2024-05-11</li><br/><li><img src="" width="30px"><span>Geek_042531</span> 👍（0） 💬（1）<div>终于看完了一遍，收获很大，有点意犹未尽。Mike老师，是否可以讲解一些高级点的知识点？比如性能优化相关的东西。</div>2024-02-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/2e/7e/a15b477c.jpg" width="30px"><span>Noya</span> 👍（0） 💬（1）<div>Over!</div>2024-01-12</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/7Q403U68Oy4lXG5sFBPVKLrfwaRzBqpBZibpEBXcPf9UOO3qrnh7RELoByTLzBZLkN9Nukfsj7DibynbZjKAKgag/132" width="30px"><span>superggn</span> 👍（0） 💬（1）<div>问卷里搞了一波关于迭代的看法， 有点长， 希望能看到， 有精力有时间的话可以考虑搞一波（笑）</div>2024-01-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/36/3c/e4/b262e14c.jpg" width="30px"><span>安</span> 👍（0） 💬（1）<div>期待后续,我的老朋友</div>2024-01-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/62/15/c1c4c8d6.jpg" width="30px"><span>倪步烤</span> 👍（0） 💬（1）<div>好像少一讲，显示是35&#47;36</div>2024-01-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/63/57/b8eef585.jpg" width="30px"><span>小虎子11🐯</span> 👍（2） 💬（0）<div>我已经拿到结课证书了，谁有我快～</div>2024-01-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/ed/4d/7df516d5.jpg" width="30px"><span>一带一路</span> 👍（1） 💬（0）<div>太棒了，期待后续课程(◍•ᴗ•◍)</div>2024-01-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/75/bc/89d88775.jpg" width="30px"><span>Calvin</span> 👍（0） 💬（0）<div>缺少的单测和集测如果一并介绍就好了</div>2024-05-09</li><br/>
</ul>