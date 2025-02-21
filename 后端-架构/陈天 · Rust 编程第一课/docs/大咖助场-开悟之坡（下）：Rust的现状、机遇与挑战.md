你好，我是张汉东。

上篇我们聊了Rust语言的现状和机遇，从语言自身的成熟度、语言的生态和应用场景，以及语言的可持续发展能力这三个方面，比较系统地说明Rust发展相对成熟的现状。

Rust 语言作为一门新生语言，虽然目前倍受欢迎，但是面临的挑战还很多。我们今天就聊一聊这个话题。

挑战主要来自两个方面：

1. **领域的选择**。一门语言唱的再好，如果不被应用，也是没有什么用处。Rust 语言当前面临的挑战就是在领域中的应用。而目前最受关注的是，Rust 进入 Linux 内核开发，如果成功，其意义是划时代的。
2. **语言自身特性的进化**。Rust 语言还有很多特性需要支持和进化，后面也会罗列一些待完善的相关特性。

### Rust For Linux 的进展和预判

从 2020 年 6 月，Rust 进入`Linux` 就开始成为一个话题。`Linux` 创建者 Linus 在当时的开源峰会和嵌入式`Linux` 会议上，谈到了为开源内核寻找未来维护者的问题。

简单跟你讲一讲背景情况。

Linus 提到：“内核很无聊，至少大多数人认为它很无聊。许多新技术对很多人来说应该更加有趣。事实证明，开源内核很难找到维护者。虽然有很多人编写代码，但是很难找到站在上游对别人代码进行 Review 的人选。这不仅仅是来自其他维护者的信任，也来自所有编写代码的人的信任……这只是需要时间的”。
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/52/40/e57a736e.jpg" width="30px"><span>pedro</span> 👍（3） 💬（2）<div>满屏的特性，不禁让我想到当年的c++。
我们真的需要这么多的特性吗，感觉像是中国大厂做APP，一堆Tab页，没几个能用的</div>2021-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/d3/ef/b3b88181.jpg" width="30px"><span>overheat</span> 👍（0） 💬（1）<div>有Rust写Linux Device Driver的例子吗？</div>2021-12-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/6b/c4/2343b1cb.jpg" width="30px"><span>手滑的小熊猫</span> 👍（0） 💬（1）<div>噗哈哈哈哈汉东老师说话是很厚重很慢速的。小编代读的吧</div>2021-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/99/30/231af749.jpg" width="30px"><span>陈小虎</span> 👍（0） 💬（1）<div>东西太多了。。</div>2021-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f8/ba/d28174a9.jpg" width="30px"><span>Geek_zbvt62</span> 👍（1） 💬（0）<div>Try trait那里，有些不明白，为什么关联类型要写成 type Residual = Result&lt;!, E&gt;;（我现在使用的是1.65版本，是Result&lt;convert::Infallible, E&gt;）而不是E?我感觉type Residual = E也可以工作呀？</div>2022-12-02</li><br/>
</ul>