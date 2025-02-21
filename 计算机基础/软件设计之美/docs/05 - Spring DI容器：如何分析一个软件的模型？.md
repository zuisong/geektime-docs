你好！我是郑晔。

在上一讲中，我们讨论了如何了解一个软件的设计，主要是从三个部分入手：模型、接口和实现。那么，在接下来的三讲中，我将结合几个典型的开源项目，告诉你如何具体地理解一个软件的模型、接口和实现。

今天这一讲，我们就先来谈谈了解设计的第一步：模型。如果拿到一个项目，我们怎么去理解它的模型呢？

**我们肯定要先知道项目提供了哪些模型，模型又提供了怎样的能力。**这是所有人都知道的事情，我并不准备深入地去探讨。但如果只知道这些，你只是在了解别人设计的结果，这种程度并不足以支撑你后期对模型的维护。

在一个项目中，常常会出现新人随意向模型中添加内容，修改实现，让模型变得难以维护的情况。造成这一现象的原因就在于他们对于模型的理解不到位。

我们都知道，任何模型都是为了解决问题而生的，所以，理解一个模型，需要了解在没有这个模型之前，问题是如何被解决的，这样，你才能知道新的模型究竟提供了怎样的提升。也就是说，**理解一个模型的关键在于，要了解这个模型设计的来龙去脉，知道它是如何解决相应的问题。**

今天我们以Spring的DI容器为例，来看看怎样理解软件的模型。

## 耦合的依赖

Spring在Java世界里绝对是大名鼎鼎，如果你今天在做Java开发而不用Spring，那么你大概率会被认为是个另类。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqia9gfbDeu8RqUlSozxmnzr6micGefNs5QGehBBl23xH6V82GxYwjgFgCKIA9n6iafFVKFoxVw5fHWw/132" width="30px"><span>Moonus</span> 👍（24） 💬（9）<div>我觉得最根本原因是大多数开发不写测试，所以不会考虑依赖问题，大多数方法都是面向实现而不是接口，使用DI容器反而增加了工作量。
目前所在小组偏向于外包，代码只有一层，不是单列，就是静态方法；为了达到快速交付，基本没有设计，不管怎么说这都是不合理的。是前人挖，后人跳。</div>2020-06-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f9/88/cdda9e6f.jpg" width="30px"><span>阳仔</span> 👍（18） 💬（1）<div>理解软件设计中模型首先要理解模型解决的核心问题是什么，然后抽丝剥茧了解模型的来龙去脉，深入理解模型解决问题的过程。
spring中的di模型是为了解决对象的创建和组装的问题。
那为什么创建对象和组装要用di来解决？
一个重要的原因是为了解耦。分离接口与实现的强依赖，也就是软件设计第一步分离关注点。
而这个恰恰就是为了可测试性，当一个代码是可测的，其实就是说明它是比较灵活的，修改起来不会牵一发而动全身，提高开发的体验，减少因修改引入的额外问题</div>2020-06-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/04/41/082e2706.jpg" width="30px"><span>keep_curiosity</span> 👍（13） 💬（2）<div>为什么不建议使用静态方法？如果只是简单的模型转换，用静态方法不是更好吗？</div>2020-06-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/82/42/8b04d489.jpg" width="30px"><span>刘丹</span> 👍（10） 💬（7）<div>container.bind(Connection.class).to(connection);
container.bind(ArticleReposistory.class).to(DBArticleRepository.class);
container.bind(ArticleService.class).to(ArticleService.class)
请问这3行代码的具体含义是啥？</div>2020-06-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/51/08/4b2d2499.jpg" width="30px"><span>JohnnyB0Y</span> 👍（9） 💬（3）<div>回答作业：
1，Java有反射，其他语言不一定有；
2，Java生态比较完善，大神比较多，有模版可以学；
3，前端开发集中在UI界面和数据解析，需求变更快，用DI容器去做有点吃力；（UI大多是包含的方式，很难把子控件拎出来初始化）
4，DI容器的AOP可能更适合后端，突如其来的统计、归档之类的需求。而前端的应用生命周期和页面生命周期都由UI框架提供了，AOP自然用的少。

总结：我觉得AOP可能才是开发者爱用DI的主要原因，加上Java生态的繁荣最终流行起来。（个人看法）</div>2020-06-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/05/92/b609f7e3.jpg" width="30px"><span>骨汤鸡蛋面</span> 👍（7） 💬（1）<div>接触spring 七八年， 一直在学习BeanFactory 和 ApplicationContext 上打转，今天才算对容器这个概念有一个直觉性的认识，感谢老师！</div>2020-06-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/9e/3d/928b41f1.jpg" width="30px"><span>六一王</span> 👍（5） 💬（1）<div>我是一个两年的前端程序媛，不太了解 java。面向对象编程时，你只想要一颗树，却得到整个森林，于是有些人就觉得面向对象编程是不好的，所以认为函数式编程的方式更好，不过文章提到的组件创建和组合放入到一个容器中，也就是说将所有依赖都放入都一个地方，提供业务需要的接口，而不写到业务中，那么为啥没有在前端火起来呢？函数式编程是不是就是面向接口编程的一种呢？</div>2020-06-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/a0/a3/8da99bb0.jpg" width="30px"><span>业余爱好者</span> 👍（5） 💬（2）<div>一个框架的流行根本原因不是它简化了开发，而是导致了问题的简化的那个开发模型。像spring 提供的di 模型，你甚至感受不到它的存在。它更像是一种理念，而这是一个模型的最高级形态。在di的核心模型之上，又出现了starter,auto configuration 等理念，这就是spring boot 的模型创新。在springboot 之上，又有springcloud.....

Spring 这个框架，真的是，，，牛逼(找不到合适的词了）</div>2020-06-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/13/34/abb7bfe3.jpg" width="30px"><span>小鱼儿</span> 👍（4） 💬（3）<div>放下历史长河之中去看问题，比如 现在去看几年前甚至10年前的代码，才知道这样做的好处，分离关注点，可测试性是多么需要，不然真的改不动。</div>2020-06-04</li><br/><li><img src="" width="30px"><span>Geek_3b1096</span> 👍（4） 💬（1）<div>你只是在了解别人设计的结果... 这就是我最欠缺的
</div>2020-06-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/ab/19/829f321f.jpg" width="30px"><span>迈步</span> 👍（3） 💬（2）<div>我的理解，IoC是一种思想，就像OOP、AOP一样都是思想。而DI是技术实现，是IoC的最常见以及最合理的实现方式。按照老马（Martin Fowler）的意思，可以使用DI代替掉IoC。因为DI就基本能够体现出IoC的意思了。省得搞混淆了。

另外对于静态方法，在日常开发中，老师的建议是什么呀？推荐使用吗？在什么场景下可以推荐使用？</div>2020-06-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/48/ee/96a7d638.jpg" width="30px"><span>西西弗与卡夫卡</span> 👍（3） 💬（1）<div>多半因为Java在企业级应用里独占鳌头，所以Java的DI更为人所知，也因为更早地出现了容器级的DI，Java才这么流行</div>2020-06-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/d5/3e/7f3a9c2b.jpg" width="30px"><span>Jaising</span> 👍（2） 💬（1）<div>跳出软件设计领域，像家具装潢（比如买沙发）等传统行业是可以找到对应概念的，但是相比软件设计复杂多；
客户期望只关注产品功能（对应模型），然而企业销售产品时往往揉入了很多客户并不想了解的产品实现细节比如加工工艺、材料源头等（杂糅模型和实现）；
这也算是造就了程序员的单纯吧😓</div>2020-06-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/96/63/7eb32c9b.jpg" width="30px"><span>捞鱼的搬砖奇</span> 👍（2） 💬（3）<div>文中说“静态方法满天飞”是为了在实例方法中调用别的方法所以改为静态方法，是这样的意思吗</div>2020-06-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/56/90/be01bb8d.jpg" width="30px"><span>Asanz</span> 👍（2） 💬（1）<div>DI是模型？我理解的DI是一种实现，IoC是模型😂</div>2020-06-03</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/69KUCz9tfaImVeVjOY4zVvWx2VDd77D9dcNicEcPY2yxUDTAMPeCudbCFAl0yuOHcMu3A5RoH58ZX1iaouF9EG7g/132" width="30px"><span>Geek_8c790c</span> 👍（1） 💬（1）<div>&quot;我们肯定要先知道项目提供了哪些模型，模型又提供了怎样的能力。这是所有人都知道的事情，我并不准备深入地去探讨。&quot;确实不懂项目提供了哪些模型，有大佬解释下吗</div>2020-12-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/79/69/5960a2af.jpg" width="30px"><span>王智</span> 👍（1） 💬（1）<div>我觉得是因为Java面向对象，更多的是使用组合解决问题，使用组合那就避免不了对象的依赖，加上接口实现分离，就更加依赖于DI，而像其他的语言，像面向过程全程使用函数来解决问题，貌似有点用不到对象的组合和创建。我的一点小理解，也不知道有没有问题。</div>2020-06-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/0c/37/913de94f.jpg" width="30px"><span>keys头</span> 👍（0） 💬（1）<div>那么，有没有什么方式可以更快更好的去理解一个模型的来龙去脉呢？</div>2024-12-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1d/de/62bfa83f.jpg" width="30px"><span>aoe</span> 👍（0） 💬（1）<div>原来DI容器解决的是组件创建和组装的问题！终于明白了！老师的课程内容非常优秀，就是课程名字没有《设计模式之美》拉风，比较偏学术风格，吓的我不敢看，以为会枯燥乏味，所以购买很久都没看。无意间看了一下，内容精彩，停不下来，收货很大！感谢老师！</div>2021-10-21</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/rRCSdTPyqWcW6U8DO9xL55ictNPlbQ38VAcaBNgibqaAhcH7mn1W9ddxIJLlMiaA5sngBicMX02w2HP5pAWpBAJsag/132" width="30px"><span>butterfly</span> 👍（0） 💬（1）<div>我了解需要面向接口编程，编码时很少写过DAO层的interface：ArticleRepository， 常常是直接写实现. 如果DAO层使用的底层是确定的，是否需要先写接口，再写该实现?
</div>2020-08-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f2/f2/2a9a6e9a.jpg" width="30px"><span>行与修</span> 👍（0） 💬（1）<div>我觉得可能是用的太浅吧，或者把发挥的空间就留给了一小部分人，所谓的上手快，形成的优质案例不多影响也不大。编程思想是跨语言层面的，比如说java实现的用其它高级语言也能实现，要我说都是用的人的问题。人的因素很大，比如C++也可以不写成多继承啊，不能因为语言层面没有禁止就说是语言设计的不好是吧～</div>2020-06-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/17/27/ec30d30a.jpg" width="30px"><span>Jxin</span> 👍（79） 💬（6）<div>1.斟酌再三，虽说直接说spring di容器好像也没啥毛病，但个人觉得这描述并不是很准确，故阐述下自己的认知。

2.我认为spring提供的这个编程模型应该叫ioc（控制反转和响应式编程有点像）而不是di。因为最开始被提出来的是ioc（好莱坞原则），而且最早的实现也不是spring，jdk和ejb都有对ioc的实现，spring才是后来者。但是di确实好像是在spring上被流行起来，且长期主流的（spring di容器没毛病的原因）。不过spring对ioc的实现，除了di还有依赖查找，在我眼里ioc是模型，依赖查找和依赖注入是功能，所以我认为应该是spring提供了ioc的编程模型，利用ioc容器+di的功能简化了开发。

3.依赖注入相对于依赖查找，透明度更好，调用方对ioc容器的api和具体接口实现的查表获取被隐藏了（技术与业务的解耦最终都该透明无感）。但依赖查找在需要动态选择策略时依旧有其用武之地。

4.回答课后题： 对于py和go这类函数式编程语言，函数是一等公民，是可以作为参数传递的。那么直接改变所传的函数就可以实现mock和函数替换（使用和创建天然解耦）。  为什么java会流行？我认为有个原因，是因为java是单分派的语言，编译期方法和参数类型是绑定死的（强类型），运行期走哪个bean的方法是动态决定的。如此就引出了面向接口编程的多态实现方案，才会有后面ioc的诉求。</div>2020-06-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f5/b9/888fe350.jpg" width="30px"><span>不记年</span> 👍（3） 💬（0）<div>郑老师你好,文中模型感觉和我理解的模型不一样, 我觉得模型是软件内在的东西,是其独有的东西,是对问题域的建模.
拿spring DI来说,问题域是如何自动化对象的创建和组装
对问题域建模后,我们的模型由哪几部分组成,各部分之间怎么交互的,我认为这个是模型.至于文中提到的编程模型,我觉得理解成接口更加合适.
</div>2020-06-04</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/F7I06BSAsrkqVdz1gNogToKO1fria5iagU7icR6vM6qZDpz8wDHK6gFLXBgUKuI2QCZv39ylgmibZJw53hcK4LdeGQ/132" width="30px"><span>Geek_f091d5</span> 👍（2） 💬（0）<div>也许是我理解有误，标题是模型的设计，内容怎么说起了依赖注入的实现，我认为也许应该从某一简单的业务着手，讲解针对该业务的错误的模型设计和正确的模型设计。
</div>2020-07-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/92/6d/becd841a.jpg" width="30px"><span>escray</span> 👍（2） 💬（0）<div>其实很早就听说过 Inversion of Control 和 Dependency Injection，但是似乎一直没有搞明白其中的概念，也没有机会有意识的去使用 DI（也许是用了，但是没有意识到）。

重读了 Martin Fowler 的长（旧）文，有一个疑惑，专栏里面的 Spring DI 是属于哪一种类型的 IoC，看上去比较像 type 1，Constructor Injection。

但是在 Martin Fowler 的文章里面说道 Spring 的开发者更推荐使用 Setter Injection（Spring 框架应该是同时支持这两种依赖注入方式的），不知道是因为框架的进展，改用了 Constructor Injection，或者只是局限于作者的这个例子。

结合专栏的内容，简单的了解了一下 Spring 中的 DI。

在 Ruby 中可以使用 dry-rb 实现依赖倒置 https:&#47;&#47;medium.com&#47;@Bakku1505&#47;introduction-to-dependency-injection-in-ruby-dc238655a278

但是 DHH 也说过，Dependency injection is not a virtue https:&#47;&#47;dhh.dk&#47;2012&#47;dependency-injection-is-not-a-virtue.html</div>2020-06-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（1） 💬（1）<div>我感觉 老师文中讲的是 编程模型不是 一个项目的功能模型（功能建模或者 DDD领域建模）。 我认为在熟悉一个项目的时候，领域模型是首先要看的， 编程模型的选择只是为了 接口 或者 实现  提供基础 </div>2020-06-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/79/69/5960a2af.jpg" width="30px"><span>王智</span> 👍（1） 💬（0）<div>读第二遍：模型和模型设计，按照上面所说，Spring DI容器就是一个模型，那好的模型是不是就可以说是一个模型设计呢？按照现在的理解，模型确实不是早期脑海中的类了，早期就觉得类就是模型，从现在看看远远不足呀，模型的具体定义有点模糊了，希望能一直跟下去，看完之后再过一边可能会学到更多的东西。</div>2020-06-04</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eoOGZ6lbHiboIZMN9USbeutnmCWBahVLtSlKlIENKvrZQCUQzpzeZQOxTntIkBUeDk6qZUPdqmfKrQ/132" width="30px"><span>宝宝太喜欢极客时间了</span> 👍（1） 💬（1）<div>还是感觉模型是个很虚得东西，只可意会不可言传，能不能通过一种方式把他表现出来呢？比如图形？</div>2020-06-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/fd/58/1af629c7.jpg" width="30px"><span>6点无痛早起学习的和尚</span> 👍（0） 💬（0）<div>留言：看了课程内容+留言评论，有一些问题讨论和分享
1. 理解少用静态方法要解决的问题，代码可测试性
2. 郑大讲的思路：思考一个设计来龙去脉和解决问题。这个思路有时候给他人讲技术方案的时候也可以这样，让对方更能明白。</div>2023-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/4d/b2/a04f6f15.jpg" width="30px"><span>张宁</span> 👍（0） 💬（0）<div>DI和IOC难道不是都在说一个东西吗？</div>2023-01-16</li><br/>
</ul>