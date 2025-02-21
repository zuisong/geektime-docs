在一个初创公司成长的过程中，作为工程师的你也许常常会遇到下面这样的情况。

有一天，你看到一个段代码或一个算法，觉得这些代码不大经得起推敲；于是你用 git blame 命令去寻找代码的主人；结果发现，原来作者是如今早就不写代码的 CTO 或 VP。

之后，在一个偶然的机会里，你和他讲起这件事，他会自豪地告诉你：“哦，那时候我们必须在一天之内做出这个产品特性。当时也就我一个程序员吧，一天的时间，这是当时能做出最好的方案了。” 说完，他便陷入了对美好时光的怀念里。

你也可能听说过这样的故事。

有一天你的 CTO 突发奇想，行云流水地提交了一段代码；大家一看很激动啊，很多人跑去观摩大神的代码，结果觉得问题多多，于是在PR（ Pull Request ）上提了一堆评论。

CTO 一看有点傻眼了：“几十条评论……现在代码要这么写啊，好麻烦。”于是他就和一位工程师说：“你把评论里的问题解决下，合并（Merge）到主分支吧”， 然后就开开心心地该干嘛干嘛去了。

这两个小故事是想说明一个道理：一个公司早期的代码会因为各种历史原因不是那么完美，但是，在特定的时间点，这就是当时最优的方案。

随着公司的发展，成品功能不断叠加，代码架构不断优化，系统会经历一些从简到繁，然后再由繁到简的迭代过程，代码的改动也会相当巨大，也许有一天，你会几乎不认识自己当初的作品了。

API 的设计和实现更是如此。在我们的工作中，很少能见到 API 的设计和实现从最开始就完美无瑕疵。一套成熟的 API，很多时候都是需要通过不断演化迭代出来的。今天我就和你聊聊 API 的设计和实现。

首先第一点，我们先从 API 的签名（Signature）说起。

## API 的签名（Signature）

API 的签名，或者叫协议，就是指 API 请求（Request） 和响应（ Response ）支持哪些格式和什么样的参数。

首先，做过 API 的人都知道，一个上线使用的 API 再想改它的签名，会因为兼容性的问题痛苦不堪。因此，API 签名的设计初期，一定要经过反复推敲，尽量避免上线后的改动。

除了一些基本的 RESTful 原则外，签名的定义很多时候是对业务逻辑的抽象过程。一个系统的业务逻辑可能错综复杂，因此 API 设计的时候，就应该做到用最简洁直观的格式去支持所有的需求。

这往往是 API 设计中相对立的两面，我们需要找到平衡。有时候为了支持某一个功能，似乎不得不增加一个很违反设计的接口；而有时候我们为了保证 API 绝对规范，又不得不放弃对某一些功能的直接支持，这些功能就只能通过迭代调用或客户端预处理的方式来实现。

这种设计上的取舍，通常会列出所有可行的方案，从简单的设计到繁杂的设计；然后通过分析各种使用实例的频率和使用某种设计时的复杂度，从实际的系统需求入手，尽可能让常用的功能得到最简单直接的支持；还要一定程度上 “牺牲” 一些极少用到的功能，反复考虑系统使用场景，尽可能获得一个合理的折衷方案。
<div><strong>精选留言（12）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/51/b1/7d6879dc.jpg" width="30px"><span>未设置</span> 👍（11） 💬（0）<div>感觉安姐讲这个「每个工程师都应该了解的」系列，比其他的文章长了三倍都不止，安姐一定是特别喜欢技术类的内容，谈起来洋洋洒洒。技术小白看起来有点难，不过有认真的做笔记。
我还在学习阶段 没有上手做内容 不过感觉api的设计和实现这篇讲了很多细节的问题  十分有帮助 谢谢安姐</div>2017-12-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/93/9d/def1fe22.jpg" width="30px"><span>蓝翔Sean</span> 👍（3） 💬（1）<div>安姐 对于API的RESTful有一些疑问 感觉并不是所有的API都能实现成RESTful的 有很多内容是没办法找到对应资源的 比如说login logout 用户其他的一些动作 对这些API的设计有什么建议吗</div>2017-12-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/46/b7/0b1cf9f4.jpg" width="30px"><span>王岩</span> 👍（3） 💬（0）<div>关于login in&#47;login out，在我现在系统里，就是对于特定授权的创建&#47;删除哈 &#47;auth post和delete</div>2018-02-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/88/c8/6af6d27e.jpg" width="30px"><span>Y024</span> 👍（3） 💬（0）<div>API框架可否推荐简评下呢？</div>2017-12-28</li><br/><li><img src="" width="30px"><span>gggjtg</span> 👍（2） 💬（0）<div>如果有英文版就好了</div>2018-03-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/49/10/eadec2c6.jpg" width="30px"><span>刘剑</span> 👍（2） 💬（0）<div>我们使用Spring Boot构建RESTful风格，我建议用更少的语言实现API以降低系统复杂度，也降低维护成本。</div>2017-12-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/fd/fd/1e3d14ee.jpg" width="30px"><span>王宁</span> 👍（1） 💬（0）<div>建议使用更少的语言创建这样可以通过通用的Aop,日志，限流等功能的实现，对外提供一套统一的api交互方式。
如果实现多语言的实现，可以通过rpc的方式进行封装。

当然如果系统足够复杂也可以通过service mesh的sidecar的方式进行管理。</div>2018-05-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/b1/b2/0a71e6f1.jpg" width="30px"><span>赖晓强</span> 👍（1） 💬（0）<div>还不太能看懂，先做笔记。</div>2018-02-05</li><br/><li><img src="" width="30px"><span>何慧成</span> 👍（0） 💬（0）<div>偏向用更少的语言实现，语言比较集中，减少维护成本，减少对各种技术人员的需求。</div>2020-08-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/4d/7a/106c3745.jpg" width="30px"><span>mikejiang</span> 👍（0） 💬（0）<div>不同的api引入的语言似乎越少越好，可维护性更好，设计风格更容易一致。不过在追求性能与效率的同时，怎么折中就视情况而定了</div>2019-11-12</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJvJDBrTrESPwZhQkoibT0NYdasIia7ZOCbU0oKgY2icrE9flAbzMsI7CZoiblTpqukMEzTfzrQU0ibPBg/132" width="30px"><span>白白白小白</span> 👍（0） 💬（0）<div>认真的读完了，带给我不少工作上的启发，也提供了一些很好的见解！zan</div>2018-05-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4f/0c/bf76644b.jpg" width="30px"><span>VincentJiang</span> 👍（0） 💬（0）<div>想问下Ruby on Rails下写API比较好的Gem是什么？</div>2018-02-06</li><br/>
</ul>