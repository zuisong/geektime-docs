你好，我是陈天。

一门编程语言的能力，语言本身的设计占了四成，围绕着语言打造的生态系统占了六成。

[之前](https://time.geekbang.org/column/article/411089)我们对比过 Golang 和 Rust，在我看来，Golang 是一门优点和缺点同样突出的语言，Golang 的某些缺点甚至是很严重的，然而，在 Google 的大力加持下，借助微服务和云原生的春风，Golang 构建了一个非常宏大的生态系统。基本上，如果你要做微服务，Golang 完善的第三方库能够满足你几乎所有的需求。

所以，生态可以弥补语言的劣势，**编程语言对外展现出来的能力是语言+生态的一个合集**。

举个例子，由于不支持宏编程，Golang 在开发很多项目时不得不引入大量的脚手架代码，这些脚手架代码如果自己写，费时费力，但是社区里会有一大票优秀的框架，帮助你生成这些脚手架代码。

典型的比如 [kubebuilder](https://github.com/kubernetes-sigs/kubebuilder)，它直接把开发 Kubernetes 下 operator 的门槛降了一大截，如果没有类似的工具，用 Golang 开发 Kubernetes 并不比 Python 来得容易。反之，承蒙在 data science 和 machine learning 上无比优秀且简洁实用的生态系统，Python 才得以在这两个领域笑傲江湖，独孤求败。

那么，Rust 的生态是什么样子呢？我们可以用 Rust 做些什么事情呢？为什么我说 Rust 生态系统已经不错，且潜力无穷、后劲很足呢？我们就聊聊这个话题。
<div><strong>精选留言（16）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/8a/77/8a89d0c9.jpg" width="30px"><span>tr1um7h</span> 👍（7） 💬（1）<div>老师，rust宏编程能有空讲讲吗？</div>2021-10-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/64/a8/ad627315.jpg" width="30px"><span>pk</span> 👍（6） 💬（3）<div>没有提到区块链。貌似 Rust 在区块链也有一席之地？</div>2021-10-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f3/ee/33ef689b.jpg" width="30px"><span>土土人</span> 👍（5） 💬（1）<div>“Rust 支持几乎所有主流的数据库，包括但不限于 MySQL、Postgres、Redis、RocksDB、Cassandra、MongoDB、ScyllaDB、CouchDB 等等。”  Oracle现在属于非主流了么？发现新的工具，基本不支持。</div>2021-11-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/02/22/19585900.jpg" width="30px"><span>彭亚伦</span> 👍（5） 💬（1）<div>由于这段时间各种路上跑, 只能空闲时间把课程粗略刷了一遍.
 
不得不说, 这绝对~绝对~是目前最好的rust课程, 没有之一~ 既有深度又有广度~  

准备回到家再精细精读开刷~

十分期待接下来的内容~~ </div>2021-10-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/08/e1/b4748943.jpg" width="30px"><span>夏洛克Moriaty</span> 👍（1） 💬（1）<div>感谢分享。有个问题平常想要一个功能都是去creates.io上搜索关键词，但是搜索结果总是不尽人意，老师平常是怎么发现这些库的呢</div>2021-10-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a1/0e/b98542f6.jpg" width="30px"><span>黄智勇</span> 👍（1） 💬（2）<div>老师，你关注一些web框架poem，感觉很不错</div>2021-10-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/58/79/266ca68e.jpg" width="30px"><span>LuYoo</span> 👍（0） 💬（1）<div>其实目前主要在区块链应用吧，很多人学习rust也是为了这快吧。</div>2021-12-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/62/e0/d2ff52da.jpg" width="30px"><span>记事本</span> 👍（0） 💬（1）<div>老师,我直接从在Cargo.toml 写 serde = &quot;1.0.130&quot; ,好像没法用,后来我从你的以前教程看到  serde = { version = &quot;1&quot;, features = [&quot;derive&quot;] } 这个才可以编译成功,这个是怎样的一门课啊</div>2021-10-30</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaEIFXDPTbibYhEIAuOX3Dcpk70t82yT45qgyOU1Hl35gFf3TM27EfdWFf0DCnricVReNcwx6RBmicTibgA/132" width="30px"><span>郭士禄</span> 👍（3） 💬（0）<div>lib.rs 也是个好网站</div>2023-02-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f8/ba/d28174a9.jpg" width="30px"><span>Geek_zbvt62</span> 👍（2） 💬（1）<div>之前一年多一直在写operator，看到几十行就写了一个CRD还是挺感慨的。operator理由大量的可以抽象简化的重复代码，费时且容易出bug，受限于golang本身的能力很难做到精简，做到了也不好用。</div>2022-10-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/ec/f7/d33de1ce.jpg" width="30px"><span>柱子</span> 👍（2） 💬（0）<div>rust 最近有一个 egui 的UI库，非常惊艳</div>2022-06-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/61/c1/93031a2a.jpg" width="30px"><span>Aaaaaaaaaaayou</span> 👍（1） 💬（0）<div>希望老师能出一个 Rust WebAssembly 相关的课程</div>2024-02-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/89/62/0777bf4f.jpg" width="30px"><span>xiaoxi666</span> 👍（0） 💬（0）<div>请教大家：如何甄别creates.io上面的库是否稳定？感觉鱼龙混杂。。</div>2023-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/3a/ea/b004210c.jpg" width="30px"><span>华尔街-49</span> 👍（0） 💬（1）<div>老师好记得您有一篇 关于axum 的文章，但是现在搜索不到了，您能分享下地址吗
</div>2022-04-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/13/77/1cd8e04f.jpg" width="30px"><span>Edwin</span> 👍（0） 💬（0）<div>老师，在客户端iOS开发，有什么好的方案吗，目前没有好的binding方案，老师可以给个建议吗</div>2022-02-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/7c/f6/028f80a8.jpg" width="30px"><span>施泰博</span> 👍（0） 💬（0）<div>其实图像领域也可以。我们项目人脸识别之前是python opencv 和 c++。现在用rust实现了下，性能很不错。</div>2022-02-23</li><br/>
</ul>