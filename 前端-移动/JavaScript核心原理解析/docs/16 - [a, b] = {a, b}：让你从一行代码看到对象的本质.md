你好，我是周爱民。欢迎回到我的专栏。

接下来的两讲，我要讲的仍然是JavaScript中的面向对象。有所不同的是，今天这一讲说的是JavaScript中的对象本质，而下一讲要说的，则是它最原始的形态（也通常称为原子对象）。

说回今天的话题，所谓的“对象本质”，就是从根本上来问，对象到底是什么？

## 对象的前生后世

要知道，面向对象技术并不是与生俱来、顺理成章就成为了占有率最高的编程技术的。

在早期，面向对象技术其实并不太受待见，因为它的抽象层级比较高，也就意味着它离具体的机器编程比较远，没有哪种硬件编程技术（在当时）是需要所谓的面向对象的。最核心的那部分编程逻辑通常就是写寄存器、响应中断，或者是发送指令。这些行为都是面向机器逻辑的，与什么面向对象之类的都无关。

最早，大概是1967年的时候，艾伦（Alan Kay）提出了这么一个称为“对象”的抽象概念和基于它的面向对象编程（object-oriented programming），这也成为他所发明的Smalltalk这个语言中的核心概念之一。

然而，回顾这段历史，这个所谓的“对象”的抽象概念中，只包含了**数据**和**行为**两个部分，分别称为**状态保存**和**消息发送**，再进一步地说，也就是我们今天讲的“**属性**”和“**方法**”。并且，在这个基础上，有了这些状态（或称为数据）的局部保存、保护和隐藏等概念，也就是我们现在说的**对象成员的可见性问题**。
<div><strong>精选留言（10）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/15/13/7b/74e90531.jpg" width="30px"><span>Astrogladiator-埃蒂纳度斯</span> 👍（11） 💬（1）<div>“有迭代器的对象”在哪些场合中可以替代“索引数组”？
正如文中老师所讲的那样， 究其根本来说，索引数组其实是关联数组的一个特例——被存取的数据所关联的名字就是它的索引。关联数组可以通过实现对象迭代器的接口去实现。所以说有迭代器的对象可以适应于那些键名是非数字的场合。但是索引数组是一组连续的数据在一块内存区间，一般会有初始大小，而用迭代器实现的关联数组是非连续的数据。Map，Set， WeakMap, WeakSet，就是这种关联数组。</div>2019-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/ae/a0/707350ef.jpg" width="30px"><span>穿秋裤的男孩</span> 👍（2） 💬（2）<div>[a, b] = Object.values({a, b})
这个并不能确定a一定等于obj.a吧</div>2020-01-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d4/37/528a43e7.jpg" width="30px"><span>Elmer</span> 👍（1） 💬（1）<div>[a, b] = {a, b}如果从可执行角度可以这样理解吗
本身是个赋值表达式，右侧是个对象字面量，左侧是一个可执行结构？</div>2020-01-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/1b/a6/6373416f.jpg" width="30px"><span>青史成灰</span> 👍（0） 💬（1）<div>老师，有2个问题想问下：
①：对于这段话的描述&gt;而”名字“对应于“找到块”这一目的本身，表达为一个可计算的函数“f()”...
对于这段话，感觉对象（关联数组）和数据结构中的散列表很像，不知道js中的对象和散列表有什么关系？
但是数据接口中的散列表通过hash函数将一个key散列到数值中的索引，底层还是使用数组来实现，也就是说它还是一种连续的数据结构。但是通过文章和老师在评论中的回答，貌似这是一种不连续的数据结构，请问老师这要作何理解？
②：从&gt; Astrogladiator的评论中描述看，老师说索引数组的连续性意义不大。但是在连续的数据结构对于查找效率和缓存都是很友好的，请问老师这又要作何理解？</div>2020-01-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/82/a4/a92c6eca.jpg" width="30px"><span>墨灵</span> 👍（9） 💬（0）<div>这绝对是我今年看过最难的专栏，但也是我顿悟最多的专栏。</div>2020-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/89/5b/d8f78c1e.jpg" width="30px"><span>孜孜</span> 👍（0） 💬（0）<div>我最近在读一本书，Structure and Interpretation of Computer Programs(sicp)，突然感觉和这本课不知道哪里有很多相似。</div>2022-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ee/28/c04a0c83.jpg" width="30px"><span>小炭</span> 👍（0） 💬（0）<div>https:&#47;&#47;juejin.im&#47;post&#47;6844903715078406151
私有字段
我们来看看这个提案中最具争议的部分。 它是如此有争议：

1. 尽管事实上，它已经在Chrome Canary中实现，并且默认情况下公共字段可用，但是私有字段功能仍需额外开启；
2. 尽管事实上，原始的私有字段提案与当前的提案合并，关于分离私有和公有字段的issue一再出现（如：140，142，144，148）；
3. 甚至一些委员会成员（如：Allen Wirfs-Brock和Kevin Smith）也反对它并提供替代方案，但是该提案仍然顺利进入stage 3；
4. 该提案的issue数量最多——当前提案的GitHub仓库为131个，原始提案（合并前）的GitHub仓库为96个（相比BigInt提案的issue数量为126个），并且大多数issue持反对观点；
5. 甚至创建了单独的issue，以便统计总结对它的反对意见；
6. 为了证明这一部分的合理性而创建了单独的FAQ，然而不够强力论据又导致了新的争论（133，136）；</div>2020-11-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b2/e0/bf56878a.jpg" width="30px"><span>kkxue</span> 👍（0） 💬（0）<div>化繁为简，程序原本已成宝典</div>2020-08-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/11/3d/58ac17a0.jpg" width="30px"><span>水木年华</span> 👍（0） 💬（0）<div>周老师关于对象和数组的描述，让我恍然大悟。</div>2020-01-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（0） 💬（0）<div>当需要遍历一个数组的时候，比如for of时，但对其遍历的顺序不是特别敏感时，是可以用可迭代的对象来替代索引数组的。</div>2019-12-22</li><br/>
</ul>