你好，我是白明（英文名：Tony Bai），欢迎你和我一起学习Go语言。

我现在在一家初创企业东软睿驰工作，是一名车联网平台的架构师，同时我也是技术博客tonybai.com的博主、GopherChina大会讲师。

从2011年开始我便关注了Go语言，是Go语言在国内的早期接纳者。那个时候，离Go开源还不过两年，没有人想到它会成长到今天这样，成为后端开发的主流语言之一。

在对Go长达十年的跟随和研究中，我沉淀了很多个人的经验和思考。我也希望通过这门课，跟你分享我学习和使用Go语言的一些心法。

## 我与Go的这十年

2011年，一次偶然的机会，我非常幸运地看到了Go语言之父Rob Pike的Go语言课程[幻灯片](https://www.cs.cmu.edu/afs/cs.cmu.edu/academic/class/15440-f11/go/doc/GoCourseDay1.pdf)。当时我正经受着C语言内存管理、线程调度和跨平台运行等问题的折磨，看到Go语言的语法清新简洁，还支持内存垃圾回收、原生支持并发，便一见钟情。

我是个对编程语言非常“挑剔”的人，这跟我从事的方向有关。十多年来，我一直在电信领域从事高并发、高性能、大容量的网关类平台服务端的开发，这两年也进入了智能网联汽车行业。由于长期从事后端服务开发，我涉猎过很多后端编程语言。

我曾深入研究过C++，短暂研究过Java、Ruby、Erlang、Haskell与Common Lisp，但都因为复杂度、耗资源、性能不够、不适用于大规模生产等种种原因放弃了。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/27/52/40/db9b0eb2.jpg" width="30px"><span>自由</span> 👍（47） 💬（1）<div>Tony Bai 老师，你好，我接触 go 目前已经 3 个月了。在接触 go 一个月后，我就选择跳槽去了一家 go 的公司，我对 go 的发展是坚定不移的肯定，相信它会越来越好。

我的问题是，阅读完该专栏，我是否可以得到 go 风格的代码编写风格、优雅的 go 编程姿势？</div>2021-10-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5c/da/0a8bc27b.jpg" width="30px"><span>文经</span> 👍（36） 💬（0）<div>白老师，Go 实现自举具体是什么意思，是不是用Go语言开发的工具链来编译和执行Go源代码？这个具体是一个什么样的过程，Go语言为什么到了1.5版本才实现自举，是因为这个过程很难吗，为什么自举对Go来说是一个重要的节点？</div>2021-10-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1d/de/62bfa83f.jpg" width="30px"><span>aoe</span> 👍（21） 💬（9）<div>学习Go是因为VS Code的Copilot插件支持Go但不支持Java，AI插件写代码不是一般的强</div>2021-10-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/1b/ba/16f2017d.jpg" width="30px"><span>老韩</span> 👍（19） 💬（1）<div>老师，什么样的人适合学 Go 语言，我目前是Java工程师，在一家小公司里。</div>2021-10-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9d/a4/e481ae48.jpg" width="30px"><span>lesserror</span> 👍（12） 💬（2）<div>很早就关注老师的微博了，看到老师几乎每天都在分享关于Go的知识。

关于Go的入门课程看过很多了，目前认为普遍存在的问题有以下几个：要么过于侧重理论，脱离了实践；要么泛泛而谈，重点内容也没有说清楚；要么就是基于以前的gopath项目管理去讲解的；要么没有结合动态语言的特性来对比Go语言的不同，不能让动态语言的开发者很好的转变过来思维......

另外，文中这样说：“Goroutine 等并发原语是 Go 应用运行时并发设计的基础，而接口则是 Go 推崇的面向组合设计的抓手，这一动一静共同构成了 Go 应用程序的骨架。”

怎么理解这里的一动一静呢？</div>2021-10-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/d3/ef/928f6340.jpg" width="30px"><span>jimmyd</span> 👍（8） 💬（2）<div>老师 请问go在机器学习算法包括工程这一块 前景如何</div>2021-10-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/0f/00/f0a497ce.jpg" width="30px"><span>1900</span> 👍（7） 💬（3）<div>请问中小公司中的Go语言技术栈的岗位多吗？</div>2021-10-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/2d/ca/02b0e397.jpg" width="30px"><span>fomy</span> 👍（5） 💬（2）<div>我是Java开发者，没有系统学习过Go语言，希望老师能说一下Java和Go的区别。</div>2021-10-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/76/93/2e9bf8ab.jpg" width="30px"><span>arch</span> 👍（5） 💬（1）<div>tony老师，文中提及go GC很多次，期待补充些golang GC相关的文章哈</div>2021-10-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/64/80/61107e24.jpg" width="30px"><span>快乐就好</span> 👍（4） 💬（2）<div>运维转go开发，有机会入门吗  </div>2022-07-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/ea/05/9976b871.jpg" width="30px"><span>westfall</span> 👍（3） 💬（2）<div>刚开始学这个课程，不知道老师还会不会回复，就是好奇地想问一下，为什么那些跟云相关的项目，比如 docker k8s 等等都选择用 go 来开发？</div>2022-05-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/cb/df/e72646dd.jpg" width="30px"><span>多喝热水</span> 👍（3） 💬（1）<div>老师辽宁人吧</div>2021-10-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/0b/09/202a0483.jpg" width="30px"><span>JS</span> 👍（3） 💬（1）<div>之前自己的基础比较薄弱，有时候遇到一些问题，不太知道如何处理，这次就权当复习了</div>2021-10-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e5/d6/37a1be71.jpg" width="30px"><span>凡</span> 👍（2） 💬（1）<div>目前是2023年1月，想从客户端iOS转Go，不知道是否可行？</div>2023-02-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/50/2b/2344cdaa.jpg" width="30px"><span>第一装甲集群司令克莱斯特</span> 👍（2） 💬（1）<div>Java开发者，最近学习了Golang和Python，了解了这2种语言的设计思想，语法结构，融会贯通！</div>2022-07-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/9b/a7/440aff07.jpg" width="30px"><span>风翱</span> 👍（2） 💬（2）<div>老师对比说说go和rust</div>2022-05-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fb/6a/03aabb63.jpg" width="30px"><span>Alexhuihui</span> 👍（2） 💬（1）<div>记得大二的时候看过Go 的语法，现在已经作为Java工程师工作2年了，重学Go ing</div>2021-10-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/80/25/fd8dea38.jpg" width="30px"><span>Geek_75htmr</span> 👍（2） 💬（1）<div>看这个专栏还是用最新稳定版的 Go 语言讲解的，先给老师点个赞，会好好跟着学的</div>2021-10-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/2e/ca/469f7266.jpg" width="30px"><span>菠萝吹雪—Code</span> 👍（1） 💬（1）<div>二刷开始，记笔记，敲代码，打卡</div>2022-09-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a3/ea/bd83bd4f.jpg" width="30px"><span>麦芽糖</span> 👍（1） 💬（1）<div>go 在性能和开发效率上取得了平衡。 如 C++ 性能好但是开发效率低，python 开发效率高但是性能差 。

推荐 go 的理由
● 对初学者足够友善，能够快速上手。
● 生产力和性能的最佳结合。
● 职业选择有利。有钱。

路线
● 建立对 go 的认同
● 扎实基础
● 应用和设计意识
● 实战</div>2022-01-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0a/a4/828a431f.jpg" width="30px"><span>张申傲</span> 👍（1） 💬（1）<div>最近由于工作原因，需要从 Java 转向 Go。希望借助这么课打下坚实的 Go 语言基础。很多人都说 Go 语言是未来，那我倒要看看未来长成什么样子。</div>2021-12-01</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaEK5icO2A4K7HYTYfQoagTz7VbtgxfS2ibBqLnKVWwQZgsePibZWFvFJEhPT8BtpQSaFx9IEodyp6c0dw/132" width="30px"><span>Geek_jg3r26</span> 👍（1） 💬（1）<div>go和golang是一回事吧老师</div>2021-11-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/7b/bd/ccb37425.jpg" width="30px"><span>进化菌</span> 👍（1） 💬（1）<div>这一次，golang真的不能中途停止学习了</div>2021-10-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/26/27/eba94899.jpg" width="30px"><span>罗杰</span> 👍（1） 💬（1）<div>Tony 老师的粉丝来啦！</div>2021-10-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/55/a0/65833509.jpg" width="30px"><span>吉祥</span> 👍（1） 💬（1）<div>从0开始学起来</div>2021-10-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/bb/db/f8c74599.jpg" width="30px"><span>学了忘</span> 👍（1） 💬（1）<div>已买，一定要坚持看下去啊！！！</div>2021-10-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/2a/ff/a9d72102.jpg" width="30px"><span>BertGeek</span> 👍（0） 💬（1）<div>之前由于是否确定学习go，通过复读老师专栏建议，IT行业趋势，这次一定把go 学好，作出体现能力增值的平台！先给自己加油！</div>2024-01-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/ba/c2/791d0f5e.jpg" width="30px"><span>ltq</span> 👍（0） 💬（2）<div>目前老师有两本书籍和这个专栏 ，有其他开发语言的基础，准备开始学习go语言
问题 是否学习两本书籍包含了这个专栏的类容，还是都学，如果都学，学习顺序是怎样的，希望老师给个建议，谢谢</div>2023-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/2a/ff/a9d72102.jpg" width="30px"><span>BertGeek</span> 👍（0） 💬（2）<div>目前处于运维岗位devops，对于继续学习python还是全量转go ，希望老师给点建议，非常感谢！

暂时工作岗位没有用到开发语言，只是平时写脚本多些

1. 因为想做自动化运维，前几年培训过python语言，只是后来没做项目，也淡忘了

2. 当下devops或者自动化运维学习go是否可行和推荐

3. 如果go 能为未来职业增值，go 为主，python为辅 这样的发展路线是否正确</div>2023-02-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/fd/47/499339d1.jpg" width="30px"><span>新味道</span> 👍（0） 💬（1）<div>Go语言精进之路，写得不错，谢谢。</div>2022-06-02</li><br/>
</ul>