你好，我是郑晔。

作为程序员，你一定听说过分层，比如，最常见的 Java 服务端应用的三层结构，在《[15 | 一起练习：手把手带你分解任务](http://time.geekbang.org/column/article/78542)》中，我曾提到过：

- 数据访问层，按照传统的说法，叫 DAO（Data Access Object，数据访问对象），按照领域驱动开发的术语，称之为 Repository；
- 服务层，提供应用服务；
- 资源层，提供对外访问的资源，采用传统做法就是 Controller。

这几乎成为了写 Java 服务的标准模式。但不知道你有没有想过，为什么要分层呢？

## 设计上的分解

其实，分层并不是一个特别符合直觉的做法，符合直觉的做法应该是直接写在一起。

在编程框架还不是特别流行的时候，人们就是直接把页面和逻辑混在一起写的。如果你有机会看看写得不算理想的 PHP 程序，这种现象还是大概率会出现的。

即便像 Java 这个如此重视架构的社区，分层也是很久之后才出现的，早期的 JSP 和 PHP 并没有什么本质区别。

那为什么要分层呢？原因很简单，当代码复杂到一定程度，人们维护代码的难度就急剧上升。一旦出现任何问题，在所有一切都混在一起的代码中定位问题，本质上就是一个“大海捞针”的活。

前面讲任务分解的时候，我不断在强调的观点就是，人们擅长解决的是小问题，大问题怎么办？拆小了就好。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/48/ee/96a7d638.jpg" width="30px"><span>西西弗与卡夫卡</span> 👍（78） 💬（3）<div>万维钢有期节目里提到芯片设计时讲到了分层以及模型的概念。分层或模型，实质是因为人的认知能力有限不得已而为之的。学习计算机，我们都知道晶体管，即便早就忘了它的原理。实际上晶体管涉及非常深奥的物理学知识，这是绝大多数人一辈子都不需要了解的物理学。抛开复杂艰深的物理学，晶体管的本质却很简单，它就是一个包含通和不通两个状态的开关，这就是它构建的模型。

在开关的模型基础之上，信息论的创立者香农用一篇硕士论文构建了逻辑门这层。他证明了可以用最简单的开关，实现所有逻辑运算。

逻辑运算层次之上，就是我们所知道的CPU模型。再往上，就是我们所熟悉的信息世界</div>2019-04-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/21/c0/38816c31.jpg" width="30px"><span>春之绿野</span> 👍（13） 💬（1）<div>文章有些地方看不懂，不太懂领域对象什么的</div>2019-09-15</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83ep58epOYWkVaxMIul9hvv0LWWKIYCWAib4ic4nnngvabQMRsP1ials3u4nOYkS8HbsyLvMh7hV0LIsqQ/132" width="30px"><span>desmond</span> 👍（11） 💬（1）<div>学了REST和DDD，感觉两者有相通的地方：两者都以数据（一个是资源，另外一个是领域对象）为中心，并制定一套标准的数据操作（一个是HTTP Verb，另外一个我项目主要用JPA这一套）；而核心是业务建模。
</div>2019-04-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/94/76/aa2202b7.jpg" width="30px"><span>Wei</span> 👍（10） 💬（2）<div>分享一下自己的经历，best practices 其实在不同时期有不同的理解，有时候甚至变化很大，我自己也有迷惑的时候。 我是做ror出身的，rails 就是标准的MVC，再加上一个helper目录；

初入行时候接触的项目，controller都很臃肿，后来，提倡的是 thin controller, fat model, 于是大家又把逻辑搬到model里面；于是model又变得非常臃肿，里面包括了很多业务逻辑，耦合太高，写起测试来非常痛苦；

另外，原本helper只应该放关于view的method， 却很快变成了垃圾桶，很多不是view相关的方法都扔在了helper目录下，甚至很多controller要include 其他controller 对应的helper， 只是因为那里定义了一个可以用到的方法。

再后来，有了presenter的概念，helper目录基本就不用了；每个controller都有对应都presenter，再有，就是建立了service的目录，把业务逻辑从model里面抽离处理； 这样的结构稍微清洁了一点，测试也好写了很多。

但是在我看来，我们项目presenter&#47;services这种分层没有什么标准，有些同事还是把这种分层当作万能垃圾桶，什么都建一个，甚至业务&#47;运算都扔在presenter里面；services 的分层也是一个问题，很多只是根据model的来分，而不是业务； 最近有看了一下elixir对应的phoenix ， 它引入了context的概念，更偏重于业务划分， 我感觉这是一个比rails 更合理的分层。


PS：非常喜欢老师的这个课程，收益良多，能否建立微信群&#47;slack&#47;小密圈 之类的以便课程结束后能继续与老师和各位同行交流。 谢谢</div>2019-04-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/2b/58/11c05ccb.jpg" width="30px"><span>布衣骇客</span> 👍（10） 💬（1）<div>老师提到的直接把第三方类库的字段直接使用，导致bug层出不穷，这个真的是深受其害，线上程序莫名bug，原来是第三方修改或者擅自把字段等出现问题，改来改去，最后还是用类似老师提出那种转化本地对象再使用，最后做了类似一个防腐层那种解决问题。实际才出的坑总结到这么个东西，就是类似老师提出的模型概念</div>2019-04-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/a8/64/965e0d9b.jpg" width="30px"><span>王维</span> 👍（5） 💬（2）<div>老师在这篇文章里其实主要讲的是DDD，文章在讲到Model时，有一个Model，老师没有讲到，那就是ViewModel,即供视图使用的模型。以前我做过总结，模型应该有三种:领域模型(DDD Model)，数据访问模型(Data Access Model)和视图模型(View Model)，请老师指教。</div>2020-03-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/09/d6/5f366427.jpg" width="30px"><span>码农Kevin亮</span> 👍（4） 💬（1）<div>请问老师，在jdk的集合框架中常常会在实现类内部维护一个内部类，比如HashMap内部有个Node内部类，这算领域对象么？</div>2019-09-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/4c/58/25152fa9.jpg" width="30px"><span>kevin</span> 👍（4） 💬（1）<div>从分层一步步说到领域层的设计重要性，学起来很过瘾。文末留言万老师关于晶体管的设计很精彩</div>2019-04-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8e/a3/d7e5fe8a.jpg" width="30px"><span>0xABC</span> 👍（2） 💬（1）<div>目前对DDD还是一头雾水，尤其对领域模型的抽象和划分，郑老师能不能分析一些实际的案例，这样能有一个更直观的体验</div>2019-04-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/2c/e7/3c0eba8b.jpg" width="30px"><span>wuhulala</span> 👍（1） 💬（1）<div>分层 = 抽象，软件系统的横向模块划分，纵向逻辑分层，确实是一种抽象的实际应用</div>2020-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/d6/46/5eb5261b.jpg" width="30px"><span>Sudouble</span> 👍（1） 💬（1）<div>以前总是在追逐优雅的设计方案，全让未估计到为什么要这么设计。静下心来，去看问题的本质，这是我这一节学到的~！</div>2019-04-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/63/bd/80f587ad.jpg" width="30px"><span>丿淡忘</span> 👍（1） 💬（1）<div>老师你好，就是我现在在开发的时候有些困惑，我将界面逻辑层（界面数据显示）
业务逻辑层（具体业务逻辑功能实现）分出来后，但像支持这些业务的一些服务，比如 通讯服务，数据缓存服务，这些算是工具，还是说也可以分为一些单独的层，还有像界面显示的数据我需要给界面单独提供一些界面显示的数据结构，还是直接使用逻辑层里面的数据结构，还是说这些数据结构单独拆分出来也可以作为一层</div>2019-04-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/17/27/ec30d30a.jpg" width="30px"><span>Jxin</span> 👍（1） 💬（1）<div>对项目中变化代码和稳定代码的拆分。按特性归类成变化层和稳定层，中间用门面或适配器对接。针对变化层提炼出抽象层用装饰者模式或抽象工厂实现多态</div>2019-04-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/aa/24/01162b6c.jpg" width="30px"><span>UncleNo2</span> 👍（0） 💬（1）<div>六边形指的是哪六遍？</div>2021-06-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/00/6e/11362a1e.jpg" width="30px"><span>感动超人</span> 👍（0） 💬（1）<div>domain model 翻译成领域模型,总有种是储存数据的 model 的感觉,翻译成 领域层 也是怪怪的
我觉得 业务层 是更好的翻译</div>2020-07-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/5b/08/b0b0db05.jpg" width="30px"><span>丁丁历险记</span> 👍（0） 💬（2）<div>不知道ror 死掉没。。。</div>2019-11-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/d1/81/89ba9d81.jpg" width="30px"><span>大力</span> 👍（0） 💬（1）<div>微服务中的数据访问层，有可能跟访问数据库一点关系都没有，而只是一层调用http请求去访问其他微服务的封装，但它的原理其实跟传统的分层结构应该是一致的。</div>2019-04-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7b/ae/66ae403d.jpg" width="30px"><span>熊猫</span> 👍（0） 💬（3）<div>产品，开发，测试，运维，运营等岗位也属于分层，不同技术栈的人，组成完备技术体系。</div>2019-04-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/41/27/3ff1a1d6.jpg" width="30px"><span>hua168</span> 👍（0） 💬（2）<div>拿java来说，在MVC分层架构中，Controller 和 Service界限是怎么区别的？
我理解是：
M：DAO层，编写数据库连接
C: 控制层，主要是写业务方法，方法中包含对数据库的一些操作
V: 展示层，主要是展示

哪服务层在哪里？服务层=Controller？也不对呀

MVC原理图网上有很多，下面连接的对吗？
http:&#47;&#47;i1.excel99.com&#47;x3edf03d1838280c01dc489d36d78b81a1099d52b.jpg</div>2019-04-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f2/f2/2a9a6e9a.jpg" width="30px"><span>行与修</span> 👍（2） 💬（0）<div>跟过一段时间微软的silverlight，一开始听说是wpf的子集，后来又有人辟谣说除了使用xaml等形似之处外差别很大的。自己也看过两者的源码，就抽象能力和程度看还是正宗wpf强大，虽然不是业务框架，但从开发工具角度来看，它的基于自身定位及领域的体系设计还是值得称道的。曾经有一段时间里java和.net相互diss的厉害，现在看来在道的层面是可以和谐共处的，只是术上各有各的呈现罢了。</div>2019-04-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡</div>2024-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/65/21/101a7075.jpg" width="30px"><span>davix</span> 👍（0） 💬（1）<div>雖然分離傳輸對象和領域對象是應該的，但也有不便之處，就是二者幾乎是相同又做類型轉換時，大量的字段只是簡單的再賦值，很多這種代碼，老師怎麼說？</div>2022-05-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>领域驱动设计DDD</div>2022-04-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/35/a9/5f309b81.jpg" width="30px"><span>ubuntuMax</span> 👍（0） 💬（0）<div>请问老师，像nodejs这种弱类型语言（没有用ts）的项目如何来实践ddd呢？</div>2022-04-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d0/4d/2116c1a4.jpg" width="30px"><span>Bravery168</span> 👍（0） 💬（0）<div>抽象，分层对于降低软件的复杂度确实是一件利器。</div>2021-08-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/51/4d/0aceadde.jpg" width="30px"><span>腾挪</span> 👍（0） 💬（0）<div>受益匪浅，谢谢～</div>2021-04-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/92/6d/becd841a.jpg" width="30px"><span>escray</span> 👍（0） 💬（0）<div>刚刚作为 Ruby 程序员入职一家小公司，感觉 Rails 其实挺适合小公司的，实施起来比较快，成本比较低，但是现在好一点的 Ruby 程序员不好找了（我不是好的 Rubyist）。

MVC 似乎很久以前就有了，最早 .Net 2.0 的时候就有一个关于 Webshop 的官方例子，展示了分层的写法。

Rails 好像是那种只要你写 Rails，基本上就一定满足 MVC 的意思。

当然，我也看到了很多写的不怎么好的代码，比如超过一千行的 Ruby 文件。

有一点好奇，因为在 Rails 里面的 Ruby 类代码会写一堆的 include、has_one、has_many、belongs_to……一屏代码显然是放不下的，把显示器竖起来也不行。那么问题来了，在 Java 中有一个类不超过多少行的说法，那么在 Rails 中有类似的标准么？

之前其实一直想知道郑老师放弃 Rails 的原因，这篇文章多少说了一些。如果我早点看到这篇文章，也许会早点去看隔壁 DDD 的专栏，不过我还是挺喜欢 Ruby 语言和 Rails 框架的。（没有学过 Spring 的菜鸟，没有见过市面……）

构建自己的领域模型的意思是说要成为领域专家，深耕某一个垂直领域么？</div>2020-10-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a1/e6/50da1b2d.jpg" width="30px"><span>旭东(Frank)</span> 👍（0） 💬（0）<div>分层是为了更好的抽象，区分出程序中的不变点与与易变点，集中精力优化抽象不变点，以便更好的复用不变点逻辑。尽可能的快速添加和修改易变逻辑响应业务变更需求

个人认为：分层设计有点像代码设计模式里的模板设计模式。但分层设计更像是代码组织的模板，功能和交互层面的分组的模板。分层设计不但做到代码的分层也促进了分工合作，从而达到快速，简单，高效开发的目的</div>2019-10-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/21/c0/38816c31.jpg" width="30px"><span>春之绿野</span> 👍（0） 💬（0）<div>很多技术都是吧，都是为了把一些通用的基础的功能抽象出来，Robot 框架也是，提供了很多实现基础功能的类库，通过这些基础的关键字可以组成新的关键字，再由关键字组成更复杂的关键字，我们只用关心怎么实现功能，而这些关键字怎么调用，编译，log和结果怎么一层层展示，这些都由框架实现了。</div>2019-09-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c4/e0/eb9f6b80.jpg" width="30px"><span>Rainbow福才</span> 👍（0） 💬（0）<div>分层架构设计的目的：
1. 提炼抽象，构建好领域模型。
2. 降低软件开发和维护成本。
3. 扩展性更好。</div>2019-04-10</li><br/>
</ul>