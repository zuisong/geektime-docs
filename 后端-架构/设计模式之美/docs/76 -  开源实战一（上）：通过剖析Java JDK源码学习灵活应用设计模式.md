从今天开始，我们就正式地进入到实战环节。实战环节包括两部分，一部分是开源项目实战，另一部分是项目实战。

在开源项目实战部分，我会带你剖析几个经典的开源项目中用到的设计原则、思想和模式，这其中就包括对Java JDK、Unix、Google Guava、Spring、MyBatis这样五个开源项目的分析。在项目实战部分，我们精心挑选了几个实战项目，手把手地带你利用之前学过的设计原则、思想、模式，来对它们进行分析、设计和代码实现，这其中就包括鉴权限流、幂等重试、灰度发布这样三个项目。

接下来的两节课，我们重点剖析Java JDK中用到的几种常见的设计模式。学习的目的是让你体会，在真实的项目开发中，要学会活学活用，切不可过于死板，生搬硬套设计模式的设计与实现。除此之外，针对每个模式，我们不可能像前面学习理论知识那样，分析得细致入微，很多都是点到为止。在已经具备之前理论知识的前提下，我想你可以跟着我的指引自己去研究，有哪里不懂的话，也可以再回过头去看下之前的理论讲解。

话不多说，让我们正式开始今天的学习吧！

## 工厂模式在Calendar类中的应用

在前面讲到工厂模式的时候，大部分工厂类都是以Factory作为后缀来命名，并且工厂类主要负责创建对象这样一件事情。但在实际的项目开发中，工厂类的设计更加灵活。那我们就来看下，工厂模式在Java JDK中的一个应用：java.util.Calendar。从命名上，我们无法看出它是一个工厂类。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/4a/96/99466a06.jpg" width="30px"><span>Laughing</span> 👍（23） 💬（1）<div>我个人理解是建造者模式的典型实现。虽然只有append方法，但是每个append的参数构造是不同的，从方面也反映出，append的方法可以通过不同的参数构造不同的String。当然该类也不只是只有append的参数，还有例如insert delete参数。以上说明符合建造者模式中所要解决的构建复杂对象的目的。</div>2020-11-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/26/38/ef063dc2.jpg" width="30px"><span>Darren</span> 👍（92） 💬（0）<div>我觉得是，因为StringBuilder的主要方法append，其实就是类似于建造者模式中的set方法，只不过构建者模式的set方法可能是对象的不同属性，但append其实是在一直修改一个属性，且最后没有build(),但StringBuilder出现的目的其实是为了解决String不可变的问题，最终输出其实是String，所以可以类比toString()就是build()，所以认为算是建造者模式。</div>2020-04-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/50/d7/f82ed283.jpg" width="30px"><span>辣么大</span> 👍（25） 💬（0）<div>StringBuilder没有使用建造者模式，只是名字碰巧用了builder这个单词。它只是用来构建可变字符串，仅此而已，别想太多。</div>2020-05-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/47/31/f35367c8.jpg" width="30px"><span>小晏子</span> 👍（11） 💬（1）<div>课后思考：
我的答案是算也不算…，如果按照学院派的思想，stringbuilder和GOF中的对于builder模式的定义完全不同，stringbuilder并不会创建新的string对象，只是将多个字符连接在一起，而builder模式的基本功能是生成新对象，两个本质就不一样了，从这个角度来讲，stringbuilder不能算是builder模式。
那为什么又说算呢？这样从另外一个角度想，stringbuilder得到的字符串是一步一步append出来的，这个builder模式的一步一步set在build的行为很像，因为文中也说了不要太学院派，要灵活使用，那么从这个角度来说可以认为stringbuilder也是属于builder的一种实现，只是它不是典型实现。</div>2020-04-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/17/27/ec30d30a.jpg" width="30px"><span>Jxin</span> 👍（8） 💬（0）<div>回答课后题：

我认为应该算是建造者模式。

拿餐厅类比，对于披萨加番茄，起司等不同配料来定制披萨，这属于建造者模式要解决的问题（实例对象的定制）。而stringbuild的应用场景，更像是对披萨加一个番茄还是两个番茄更或者三个番茄的定制方式（某个字段的定制）。

所以strbuild的应用场景比传统的建造者模式更细更具体（前者实现字段的定制，后者实现对象的定制）。但字段定制依旧属于对象定制的范涛，所以我认为其依旧算是建造者模式。</div>2020-04-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/86/56/509535da.jpg" width="30px"><span>守拙</span> 👍（5） 💬（0）<div>课堂讨论: 
StringBuilder应用了Builder模式. 其主要方式是append(), 即通过不断append创建复杂对象. 
不同于传统Builder模式的是: 
1. StringBuilder的目的是创建String, 但StringBuilder并不是String的内部类.
2. StringBuilder的创建过程可以断续, 传统的Builder模式一次性填入参数后调用build()方法创建对象.
3. StringBuilder通过内部维护字符数组(char[])的方式实现拼接. </div>2020-04-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/7b/57/a9b04544.jpg" width="30px"><span>QQ怪</span> 👍（5） 💬（0）<div>StringBuilder的append()方法使用了建造者模式，StringBuilder把构建者的角色交给了其的父类AbstractStringBuilder，最终调用的是父类的append（）方法</div>2020-04-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8e/c4/8d1150f3.jpg" width="30px"><span>Richie</span> 👍（4） 💬（1）<div>The intent of the Builder design pattern is to separate the construction of a complex object from its representation. By doing so the same construction process can create different representations.

从StringBuilder的代码实现来看，他通过append方法来设置其value属性，最终使用toString()方法来创建对象。这符合建造者模式的定义。这跟我们平时使用的建造者模式唯一的不同就是他一直设置的是同一个属性，而平时我们会设置多个属性，并最终调用build()方法来创建对象。</div>2020-05-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/44/47/3ddb94d0.jpg" width="30px"><span>javaadu</span> 👍（3） 💬（0）<div>StringBuilder并没有使用构造者模式，从设计意图上看这俩不是一回事—构造者模式得意图是为同一个类生成不同定制需求的对象，而StringBuilder的设计意图是为了实现可变更的字符串来优化内存占用</div>2020-05-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/10/bb/f1061601.jpg" width="30px"><span>Demon.Lee</span> 👍（3） 💬（0）<div>如果说要创建一个复杂的String对象，那么通过StringBuilder的append()方法会非常方便，最后通过toString()方法返回，从这个角度看算建造者模式。
    @Override
    public String toString() {
        &#47;&#47; Create a copy, don&#39;t share the array
        return new String(value, 0, count);
    }</div>2020-04-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/64/9b/d1ab239e.jpg" width="30px"><span>J.Smile</span> 👍（3） 💬（0）<div>总结：
1 工厂模式：简单工厂模式+工厂方法模式
● 简单工厂模式直接在条件判断中根据不同参数将目标对象new了出来。
● 工厂方法模式是将目标对象的创建过程根据参数分类抽取到各自独立的工厂类中，以应对目标对象创建过程的复杂度。条件分支可以使用map来缓存起来！
案例：java.util.Calendar的getInstance() 方法可以根据不同 TimeZone 和 Locale，创建不同的 Calendar 子类对象。

2 建造者模式：
通过内部的Builder类主导目标对象的创建同时校验必选属性之间的依赖关系。

3 装饰器模式：
装饰器模式把每个要装饰的功能放到单独的类中，并让这个类包装它所需要装饰的对象，从而实现对原始类的增强。
案例：java的IO类库比如InputStream和BufferInputStream。还有Collections类。</div>2020-04-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/d6/0e/02f53725.jpg" width="30px"><span>Nano</span> 👍（2） 💬（2）<div>虽然建造者模式有个明确的定义。
但是对于我个人来说，只要是可以一直return this，可以一直.setA().setB().setC()....的我都会把它当做建造者模式来理解。因为每次set都会给这个实例添砖加瓦，添加属性。至于要不要最后build()一下做一些逻辑，按需使用吧。</div>2020-10-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/44/02/791d0f5e.jpg" width="30px"><span>飞翔</span> 👍（2） 💬（1）<div>不是，从源码角度看，构造方法不私有，没有复杂构造逻辑，完全不符合构建这模式定义，唯一关联就是名字里面有一个Builder</div>2020-09-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/aa/49/51790edb.jpg" width="30px"><span>落尘kira</span> 👍（2） 💬（0）<div>StringBuilder本意是创建可变字符串，如果调用toString（）那么就是；如果不调用，那严格意义上不是。但由于出发点是创建可变字符串，理论上其设计的目的就是让使用者最终都会调用toString（）方法，因此我认为他是</div>2020-05-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/d9/ff/b23018a6.jpg" width="30px"><span>Heaven</span> 👍（2） 💬（0）<div>个人认为,是属于建造者模式的,在其中,最主要的append方法,是将其抛给了父类AbstractStringBuilder,然后返回自己,其父类AbstractStringBuilder中维护了一个数组,并且可以动然扩容,在我们最后获取结果的toString()方法中,就是直接new String对象,这种模式其实更像是装饰器模式的实现</div>2020-04-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/44/ca/510a132a.jpg" width="30px"><span>衞嚼爺</span> 👍（1） 💬（0）<div>StringBuilder从命名上看和Builder模式很像，但不算是建造者模式的应用。StringBuilder从实现的功能上看，更像是对字符串String按照装饰器模式进行封装，是一种字符串的功能叠加。</div>2020-05-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/3b/ac/40807e85.jpg" width="30px"><span>无所从来</span> 👍（1） 💬（0）<div>建造者的意图是 “将一个对象的复杂构建与其表示相分离，使得同样的构建过程可以创建不同的表示”。类似的，StringBuilder通过相同的构建过程append方法，创建出不同的String对象。因此，它是典型的建造者模式。</div>2020-04-29</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqZIqY4cs6YKNx0OqeMrbjLIicqiafLNtLYJTN2zTtVPlwXZ7qlJ7xrGQictk1xCq5pEsIyqnkiaCib4zQ/132" width="30px"><span>全炸攻城狮</span> 👍（1） 💬（0）<div>感觉不像建造者。append在StringBuilder的创建过程中不起任何作用，append真正用到的地方是StringBuilder创建好以后，对字符串的拼接。StringBuilder的创建是调用的构造方法</div>2020-04-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0b/a7/6ef32187.jpg" width="30px"><span>Keep-Moving</span> 👍（1） 💬（1）<div>感觉UnmodifiableCollection 更像是 Collection 类的代理类</div>2020-04-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/02/65/ddb6460e.jpg" width="30px"><span>柯里</span> 👍（0） 💬（0）<div>从标准代码格式而言不是，从构造复杂对象的角度，看似乎是的</div>2023-11-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/09/5b/e9ee3b41.jpg" width="30px"><span>音为</span> 👍（0） 💬（0）<div>是建造者模式，方法return this,然后toString()时才真正初始化，避免构造函数无法一次初始化所有字符串的弊端</div>2023-09-12</li><br/><li><img src="" width="30px"><span>Geek_f73a3e</span> 👍（0） 💬（0）<div>StringBuilder的底层是数组  char[] value;  append操作是向数组上添加字符；如果把客户程序看作导演，String看做产品，StringBuilder看做创建者，是可以</div>2023-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/ef/0e/bbc35830.jpg" width="30px"><span>一杯绿绿</span> 👍（0） 💬（0）<div>面向接口编程，有利于利于灵活利用多态，当后续需求变化时，可通过多态来实现低成本的改动。因为调用方感知到的只是接口，并不感知接口的具体实现，所以接口具体实现的变动对调用方是无影响的。</div>2022-03-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/63/6e/6b971571.jpg" width="30px"><span>Z宇锤锤</span> 👍（0） 💬（0）<div>不是工厂，也不是建造者。就是平平凡凡的一个实现类哦</div>2021-12-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/63/6e/6b971571.jpg" width="30px"><span>Z宇锤锤</span> 👍（0） 💬（0）<div>工程模式就是标准化产品，比如成品服装。建造者模式就是私人订制，做很多的细节微调。以成品西装和定制西装为例，定制西装量体裁衣。定制西装量衣而行。</div>2021-12-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7f/ca/ea85bfdd.jpg" width="30px"><span>helloworld</span> 👍（0） 💬（0）<div>我认为StringBuffer没有使用构造者模式. 构造者模式构造的对象是一次性生成的, 生成后不再改变, 而StringBuffer中没有体现出这一点</div>2021-04-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/55/bc/fad0090b.jpg" width="30px"><span>Yeyw</span> 👍（0） 💬（0）<div>类似于builder，但算不上，在为完全设置好字符串的情况下就可能被tostring()，导致对象不是预期状态。</div>2021-04-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/f6/7b/b6abcbbe.jpg" width="30px"><span>否极泰来</span> 👍（0） 💬（0）<div>我觉得算，毕竟他是构建了不可变对象String
不一定只有构建复杂的对象才能使用建造者模式，
StringBuilder这是创建节约内存的建造者，也是使用建造者模式。</div>2021-04-06</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/eLNeJNaEkwGSK7xvtamMibVLMy2MpbIqX3iaEhT7JtSnTRMRTwZ2j4HX7WAapiashbiaBDVriaXKSP0Oeic6ZAEVEXag/132" width="30px"><span>M</span> 👍（0） 💬（0）<div>老师，有个疑问：
前面使用工厂模式，后面一半代码才属于标准的建造者模式，根据 setXXX() 方法设置的参数，来定制化刚刚创建的 Calendar 子类对象。

如果把后半段的代码也改为“工厂模式”可行么？
我感觉也是可以的，都是根据不同的type去创建不同的对象，也都是继承或实现同一父类或接口</div>2021-03-26</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/eLNeJNaEkwGSK7xvtamMibVLMy2MpbIqX3iaEhT7JtSnTRMRTwZ2j4HX7WAapiashbiaBDVriaXKSP0Oeic6ZAEVEXag/132" width="30px"><span>M</span> 👍（0） 💬（0）<div>思考题：我觉得StringBuilder没有用到建造者模式，没有根据不同类型创建定制化的对象，仅仅是一直append拼接而已</div>2021-03-26</li><br/>
</ul>