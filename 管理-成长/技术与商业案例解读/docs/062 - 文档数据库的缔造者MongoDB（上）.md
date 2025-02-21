大数据和云计算的风被谷歌吹起来的时候，被谷歌收购的网络广告公司DoubleClick的原CEO和CTO们觉得自己应该蹭上时代的列车，再次创业，然后10gen公司就这样在纽约诞生了。它的创始人分别是DoubleClick的创始人兼CTO德怀特 · 梅里曼（Dwight Merriman）、CEO凯文 · 瑞安（Kevin Ryan），以及工程师埃利特 · 霍洛威兹（Eliot Horowitz）。

公司成立之初，创始人的想法和MongoDB这个产品毫无关系：他们想做一个云计算的服务，并用开源的东西来搭建。然而很遗憾，这几位二次创业的人在开源社区找了一圈，也没有看到一个让人满意的东西。于是，怀着构建伟大云计算服务的梦想，他们决定先把这个事情停一停，先搭一个自己满意的数据库出来。这个数据库就是后来赫赫有名的MongoDB。

MongoDB的名字需要解释一下。国内很多人觉得是“芒果数据库”，其实不是的。在英文里，“芒果”是Mango，而Mongo是humongous的中间部分，在英文里是“巨大无比”的意思。所以MongoDB可以翻译成“巨大无比的数据库”，更优雅的叫法是“海量数据库”。

这几位创始人的梦想就是创建一个和过去关系数据库完全不一样的数据库，使之具有这样一些特点：海量数据库、数据库的模型极其灵活、适合程序员使用。

**大概怀着伟大理想的人都会做出伟大的产品。**MongoDB注定是独特的，在历史上会留下浓重一笔的产品。
<div><strong>精选留言（14）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/5e/61/985f3eb7.jpg" width="30px"><span>songyy</span> 👍（14） 💬（0）<div>想了一下 觉得先吸引人上船，把社区做起来，开源 吸引社区补全产品不足，也是个不算太差的解决方案。

另一种方式，我觉得可以像rails的起家：从一个成功的产品剥离出来，有现实的成功案例，同时文档写好，对新入的开发者足够友好，再考虑靠着它收咨询费的问题</div>2017-10-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/07/8c/0d886dcc.jpg" width="30px"><span>蚂蚁内推+v</span> 👍（8） 💬（0）<div>我们公司今年也废弃 MongoDB ，继续用 MySQL 了</div>2018-11-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/b8/3c/1a294619.jpg" width="30px"><span>Panda</span> 👍（4） 💬（0）<div>听科技公司的发展故事 很有意思 哈哈哈 </div>2018-12-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/b9/a4/4ac55e58.jpg" width="30px"><span>翼吹雪</span> 👍（4） 💬（0）<div>我觉得在一块成熟的市场（数据库发展几十年），切中快速爆发的移动互联网开发市场，提供更好用的解决方案，和Oracle错开竞争战场，最终获得巨大的口碑，可以说是一个完美的开局，也是初创公司非常值得借鉴的。
可惜在后来，没有将优势保持住，在企业版中将数据库一些基本的技术补上。这本来也是很考验创业者的一个地方，即在什么时候进行转型，既能迎合市场，又能进行盈利，而且自己团队还有能力达到，这个点很难把控。</div>2018-05-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/2b/ec/af6d0b10.jpg" width="30px"><span>caohuan</span> 👍（3） 💬（0）<div>再次聆听 飞哥的 MongoDB发展历程，发现 1.它 的存储 是面向 集合，集合中包含大量的文档，不像 关系型数据库 面向表格的形式 2.它的 查询 非基于SQL，而是基于 编程语言和API，都是 它比关系型数据库 让开发人员 能感觉到更友好的使用。

它的 运营 1）赞助MongoDB大会、活动、和MongoDB大学 2）提供良好的技术支持 3）与使用者沟通 4）与大牛合作，把更多数据库使用者 绑到MongoDB产品上。

回答 老师的问题，运营一家工具类的初创公司，应该 寻找 标杆企业 和 行业领头人，为自己背书，就像 文中所说，与大牛互利互惠 ，拉去更多的开发者，找 行业的标杆企业 合作，服务好它，再让企业帮做宣传，最后 从业者多，公司使用者多，二者相互促进，形成循环，做不强都难。</div>2018-11-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/4d/67/a13a2421.jpg" width="30px"><span>奥北北北北北北</span> 👍（2） 💬（0）<div>现在都是这样啊，房子还没修都已经卖完了</div>2019-04-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a8/35/85033228.jpg" width="30px"><span>亚东</span> 👍（1） 💬（0）<div>要么不做，要做就要领先世界，并且高可用。</div>2019-11-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/6f/c9/7e380577.jpg" width="30px"><span>朴荷抹茶仔</span> 👍（1） 💬（0）<div>现在多数还是用sql来做关系表，工具类的新公司，刚开始想的是需要知道客户需求和竞争对手的长处和弊端，而这方面客户都能很好反馈。前期对市场的调查是必要的，先提供其他产品下载和评论获得咨询，后续发展推送自家产品</div>2019-03-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/2b/ec/af6d0b10.jpg" width="30px"><span>caohuan</span> 👍（1） 💬（0）<div>本篇所得，推广一应用产品 包括工具类产品，1.先拉取大量客户 2.根据反馈，优化并让产品更好用 3.方便用户使用 4.技术支持 很友善，客服做到尽心尽责。

读完 飞哥的专栏，看出 MongoDB具有自己的特色，产品上 支持app 和海量数据的非sql文档型数据库，支持程序语言和API查询，开始使用时对技术人员很友善，在营销上 通过 1.资助用户 2.支持 MongoDB的各种会议，尽管 MongoDB还有很多需求未被实现，还有bug和坑需要修复和填补，不过 依然看好MongoDB。</div>2018-11-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/0b/ab/0e2857e5.jpg" width="30px"><span>Coding小先</span> 👍（0） 💬（0）<div>工具类的，首先要面向目标客户友好，简单易用。</div>2019-11-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e4/39/a06ade33.jpg" width="30px"><span>极客雷</span> 👍（0） 💬（0）<div>MongoDB创始人和Oracle创始人有很多共通之处</div>2019-11-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a1/c9/501a1d02.jpg" width="30px"><span>self-discipline</span> 👍（0） 💬（0）<div>作为产品来说核心功能应该过硬,规模到达一定量级后就暴露各种问题的话,没有哪个互联网公司敢用的.公司的宣传,服务支持尽职尽责,对社群的支持和赞助,都做的很到位.但是打铁还需自身硬的,没有好的打铁技术,其他的服务再到位,也有种本末倒置的感觉</div>2019-09-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/cc/de/e28c01e1.jpg" width="30px"><span>剑八</span> 👍（0） 💬（0）<div>核心价值是什么
用户是谁
竞品
壁垒
规划</div>2019-09-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/18/f3/d4c0efd2.jpg" width="30px"><span>程</span> 👍（0） 💬（0）<div>作为一个工具类，不可能满足所有人的需求，但是应该正视自身的产品，给产品明确的定位，明晰产品的优缺点，不应一味吹嘘，忽悠所有人上船。尤其是提供企业级服务，不成熟就意味着隐患，爆发时的损失很难估量</div>2019-03-20</li><br/>
</ul>