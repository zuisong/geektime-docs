你好，我是蒋德钧。

咱们课程的“基础篇”已经结束了。在这个模块，我们学习了Redis的系统架构、数据结构、线程模型、持久化、主从复制和切片集群这些核心知识点，相信你已经初步构建了自己的一套基础知识框架。

不过，如果想要持续提升自己的技术能力，还需要不断丰富自己的知识体系，那么，阅读就是一个很好的方式。所以，这节课，我就给你推荐几本优秀的书籍，以及一些拓展知识面的其他资料，希望能够帮助你全面掌握Redis。

## 经典书籍

在学习Redis时，最常见的需求有三个方面。

- 日常使用操作：比如常见命令和配置，集群搭建等；
- 关键技术原理：比如我们介绍过的IO模型、AOF和RDB机制等；
- 在实际使用时的经验教训，比如，Redis响应变慢了怎么办？Redis主从库数据不一致怎么办？等等。

接下来，我就根据这些需求，把参考资料分成工具类、原理类、实战类三种。我们先来看工具类参考资料。

### 工具书：《Redis使用手册》

一本好的工具书，可以帮助我们快速地了解或查询Redis的日常使用命令和操作方法。我要推荐的《Redis使用手册》，就是一本非常好用的工具书。

在这本书中，作者把Redis的内容分成了三大部分，分别是“数据结构与应用”“附加功能”和“多机功能”。其中，我认为最有用的就是“数据结构与应用”的内容，因为它提供了丰富的操作命令介绍，不仅涵盖了Redis的5大基本数据类型的主要操作命令，还介绍了4种扩展数据类型的命令操作，包括位图、地址坐标、HyperLogLog和流。只要这本书在手边，我们就能很轻松地了解和正确使用Redis的大部分操作命令了。
<div><strong>精选留言（16）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/90/8a/288f9f94.jpg" width="30px"><span>Kaito</span> 👍（179） 💬（15）<div>老师推荐的书籍都非常经典，这几本是学习Redis的必读书籍。

如果你觉得这些书读起来困难，我推荐一本之前同事写的《Redis 深度历险：核心原理与应用实践》，这本书很薄，而且最大的特点是讲解接地气，它可以让你对Redis的基础使用、业务场景、原理分析有一个基本的认识和了解，作为入门和进阶非常合适，起码可以让你重新树立起深入学习Redis的信心。

另外，真心建议大家试着去读一下Redis源码，没有想象的那么难，而且Redis的代码质量非常高，由于是单线程的内存数据库，没有多线程运行时的复杂逻辑，读起来非常顺畅！其实很多我们纠结的小问题，不要只靠猜和网上查资料，读一下源码就能快速找到答案。而且现在源码分析的文章非常多，讲解的也很细，结合起来读代码并不难。

只有自己试着去读源码，当遇到问题时，再查资料，学习到的东西才是最深刻的。而且在查资料时，还会发现更大的世界，例如老师文章提到的操作系统知识、分布式系统问题、架构设计的取舍等等，这样我们所学到的知识不再是一个面，而是慢慢形成一个知识网，这样才能够达到融会贯通，举一反三。

</div>2020-08-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/43/79/18073134.jpg" width="30px"><span>test</span> 👍（42） 💬（7）<div>三本书读了两，源码也过了一遍，操作系统导论也看过，推荐《redis5设计与源码分析》讲源码的，很不错。</div>2020-08-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/fe/83/df562574.jpg" width="30px"><span>慎独明强</span> 👍（8） 💬（1）<div>之前组长走的时候留了一本《Redis开发和运维》给我，面试问到redis伸缩容的时候去看了下。后面面试又被问到Redis的数据结构.bitmap，自己就去网上买了《Redis设计与实现》 ，目前也在看。看了老师的建议去阅读源码，没有学过C，阅读起来会有难度吗？上面是自己的学习资料</div>2020-08-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/42/44/d3d67640.jpg" width="30px"><span>Hills录</span> 👍（31） 💬（1）<div>推荐一本书《数据密集型应用系统设计》，一个专栏《分布式数据库30讲》，可以从更高视角看待 redis 的设计</div>2020-09-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5f/e5/54325854.jpg" width="30px"><span>范闲</span> 👍（7） 💬（0）<div>推荐两本书:一本老师已经提到过了:redis设计与实现，另外一本redis深度历险。

建议阅读Redis源码，从基础数据结构看，再到db，再到网络部分，整体内容都很清晰明了。</div>2020-08-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5f/e5/54325854.jpg" width="30px"><span>范闲</span> 👍（4） 💬（1）<div>另外再补充下setinel选主的过程是用的Gossip协议吧。redis的选主过程没有raft里面那种明显的角色划分</div>2020-08-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/5c/44/d07c0865.jpg" width="30px"><span>Geek_d960af</span> 👍（3） 💬（2）<div>巧了 都下载了</div>2020-09-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/c2/fe/038a076e.jpg" width="30px"><span>阿卧</span> 👍（3） 💬（0）<div>看了《redis设计与实现》和《redis深度历险：核心原理与应用实践》，源码内容还没有接触过，需要再看看源码。缓存的设计基本可以串起来形成知识网，但是有些细节知识还需要打磨学习</div>2020-08-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d4/f3/129d6dfe.jpg" width="30px"><span>李二木</span> 👍（3） 💬（0）<div>之前就觉得哨兵选主机制像raft</div>2020-08-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/92/6d/becd841a.jpg" width="30px"><span>escray</span> 👍（2） 💬（0）<div>三本书《Redis 使用手册》、《Redis设计与实现》、《Redis开发与运维》

官方网站

阅读源码，动手实践

拓展阅读《操作系统导论》、《大规模分布式存储系统：原理解析与架构实战》

还有 Kaito 大神推荐的《Redis 深度历险：核心原理与应用实践》

有一点好奇，为什么推荐的 Redis 的书大多是中文的？

另外一点，最近也在学习 Elastic 相关的内容，Elastic 有自己的宇宙——全文检索、日志审计、安全分析，而 Redis 似乎要“单纯”一些。

目前手里并没有和 Redis 直接相关的项目，所以估计暂时也只能是把专栏先过一遍，如果后续有需要，再按图索骥，深入学习。

另外，蒋德钧老师在极客时间有一个两天的 Redis 集训班，应该也很值得推荐。</div>2021-03-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/66/34/0508d9e4.jpg" width="30px"><span>u</span> 👍（1） 💬（0）<div>www.redis.cn也不错</div>2020-10-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/16/5b/83a35681.jpg" width="30px"><span>Monday</span> 👍（1） 💬（0）<div>没看过一本的举个爪。
以前只是在某网站下载了一套redis视频，学习了几遍，敲了些命令。</div>2020-08-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/41/13/bf8e85cc.jpg" width="30px"><span>树心</span> 👍（0） 💬（0）<div>看到评论区有人推荐《数据密集型应用系统设计》，之前也看到过这本书，单看书名觉得可能会比较生涩，但也许会像评论里面说的那样可以从更高视角看待redis。</div>2022-01-06</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTITcwicqBDYzXtLibUtian172tPs7rJpqG1Vab4oGjnguA9ziaYjDCILSGaS6qRiakvRdUEhdmSG0BGPKw/132" width="30px"><span>大饶Raysir</span> 👍（0） 💬（0）<div>都是好书！</div>2020-10-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/5e/b3/e35e5d3c.jpg" width="30px"><span>..e</span> 👍（0） 💬（0）<div>redis单机，aof中有散列表写入记录没有删除记录，但是散列表丢失，访问key不存在。请问有什么排查思路？</div>2020-08-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d4/f3/129d6dfe.jpg" width="30px"><span>李二木</span> 👍（0） 💬（0）<div>视频资料话可以去B站搜搜看，适合入门</div>2020-08-28</li><br/>
</ul>