你好，我是Tony Bai。

美国时间2022年1月31日，在中国人民欢庆虎年春节之际，Go核心团队发布了[Go 1.18 Beta2版本](https://go.dev/blog/go1.18beta2)。在Go 1.18beta2版本发布的[博文](https://go.dev/blog/go1.18beta2)中，Go核心团队还给出了Go 1.18版本的发布计划：**2022年2月发布Go 1.18RC（release candidate，即发布候选版），2022年3月发布Go 1.18最终版本**。

考虑到Go 1.18版本中引入了Go语言开源以来最大的语法特性变化：**泛型（generic）**，改动和影响都很大，Go核心团队将Go 1.18版本延迟一个月，放到3月发布也不失为稳妥之举。

在Go泛型正式落地之前，我想在这篇加餐中带你认识一下Go泛型，目的是“抛砖引玉”，为你后续系统学习和应用Go泛型语法特性开个头儿。

我们今天将围绕Go为什么加入泛型、泛型设计方案的演化历史、Go泛型的主要语法以及Go泛型的使用建议几个方面，聊聊Go泛型的那些事儿。

首先，我们先来了解一下Go语言为什么要加入泛型语法特性。

## 为什么要加入泛型？

根据近几年的Go官方用户调查结果，在“你最想要的Go语言特性”这项调查中，泛型霸榜多年。你可以看下这张摘自最新的[2020年Go官方用户调查结果](https://go.dev/blog/survey2020-results)的图片：
<div><strong>精选留言（7）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/ba/ce/fd45714f.jpg" width="30px"><span>bearlu</span> 👍（3） 💬（4）<div>老师，GO的实现泛型方式是跟C++一样？编译时进行？</div>2022-02-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4c/12/f0c145d4.jpg" width="30px"><span>Rayjun</span> 👍（2） 💬（1）<div>白老师太强了，能够把复杂的问题通过简单的方式讲述出来，太值得学习了</div>2022-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9d/a4/e481ae48.jpg" width="30px"><span>lesserror</span> 👍（1） 💬（1）<div>Tony bai 老师，有几个小问题：

1. 类型参数是在函数声明、方法声明的 receiver 部分或类型定义的类型参数列表中，声明的（非限定）类型名称。 这里的非限定应该怎么理解呢？我的理解是命名可以随意。

2. 文中：“根据 Go 泛型的实现原理，上面的泛型函数调用 Sort[book]（bookshelf）会分成两个阶段。” 这里（bookshelf）里面有一个链接，但是链接打开的是极客时间首页，不知道这里原意是什么。

3. 用类型参数替换接口类型通常也会让数据存储的更为高效。 这里为什么变高效了？能大致讲讲吗？</div>2023-08-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b5/e6/c67f12bd.jpg" width="30px"><span>左耳朵东</span> 👍（1） 💬（1）<div>1、&quot;没有必要像下面代码中这样使用一个类型参数像调用 Read 方法那样去从一个值中读取数据&quot; 这里没看明白。
2、不考虑使用效果的话，能用泛型的地方好像都能用接口替换，反之也是，有点难以区分。
3、可不可以这样理解，如果某个功能只有一种实现方式，但是可以用在多种数据类型上，就用泛型；如果某个功能有多种实现方式（用不同的数据类型，会导致实现方式有差别），最好用接口。比如 io.Read 要求可以读文件 I&#47;O 也可以读网络 I&#47;O，它们各自的实现方式其实不一样，最好用接口而不是泛型。</div>2023-07-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/42/65/5bfd0a65.jpg" width="30px"><span>coming</span> 👍（1） 💬（1）<div>习惯了C++的泛型, 看着[](), 有点懵</div>2023-02-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/72/65/68bd8177.jpg" width="30px"><span>雪飞鸿</span> 👍（0） 💬（0）<div>go团队没有找安德斯•海尔斯伯格聊聊～</div>2022-09-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/c6/14/cbbdb191.jpg" width="30px"><span>总有刁民想害朕</span> 👍（0） 💬（0）<div>泛型支持依赖注入就好了</div>2022-04-24</li><br/>
</ul>