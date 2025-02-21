上一节课我们学习了桥接模式，桥接模式有两种理解方式。第一种理解方式是“将抽象和实现解耦，让它们能独立开发”。这种理解方式比较特别，应用场景也不多。另一种理解方式更加简单，类似“组合优于继承”设计原则，这种理解方式更加通用，应用场景比较多。不管是哪种理解方式，它们的代码结构都是相同的，都是一种类之间的组合关系。

今天，我们通过剖析Java IO类的设计思想，再学习一种新的结构型模式，装饰器模式。它的代码结构跟桥接模式非常相似，不过，要解决的问题却大不相同。

话不多说，让我们正式开始今天的学习吧！

## Java IO类的“奇怪”用法

Java IO类库非常庞大和复杂，有几十个类，负责IO数据的读取和写入。如果对Java IO类做一下分类，我们可以从下面两个维度将它划分为四类。具体如下所示：

![](https://static001.geekbang.org/resource/image/50/05/507526c2e4b255a45c60722df14f9a05.jpg?wh=1823%2A503)

针对不同的读取和写入场景，Java IO又在这四个父类基础之上，扩展出了很多子类。具体如下所示：

![](https://static001.geekbang.org/resource/image/50/13/5082df8e7d5a4d44a34811b9f562d613.jpg?wh=2285%2A2546)

在我初学Java的时候，曾经对Java IO的一些用法产生过很大疑惑，比如下面这样一段代码。我们打开文件test.txt，从中读取数据。其中，InputStream是一个抽象类，FileInputStream是专门用来读取文件流的子类。BufferedInputStream是一个支持带缓存功能的数据读取类，可以提高数据读取的效率。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/1f/66/59e0647a.jpg" width="30px"><span>万历十五年</span> 👍（60） 💬（4）<div>代理模式体现封装性，非业务功能与业务功能分开，而且使用是透明的，使用者只需要关注于自身的业务，在业务场景上适用于对某一类功能进行加强，比如日志，事务，权限。
装饰器模式体现多态性，优点在于避免了继承爆炸，适用于扩展多个平行功能。在场景上，这些扩展的功能可以像火车厢一样串起来，使原有的业务功能不断增强。
具体到“缓存”这个单个问题，两种模式都可以，主要还是看设计者的目的，如果是为了新增功能的隐藏性，就使用代理模式；如果设计者不仅要增加“缓存”功能，还要增加“过滤”等功能，就更适于装饰器模式。</div>2020-11-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/4a/e7/6c16af5d.jpg" width="30px"><span>汉江</span> 👍（2） 💬（2）<div>有个疑问 既然代码结构是一样的  那在于怎么叫了  我可以叫做代理模式 也可以叫做装饰器模式？</div>2020-08-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4f/13/5197f8d2.jpg" width="30px"><span>永旭</span> 👍（1） 💬（1）<div>按照本节讲的内容, java io例子里
原始类: InputStream
共同父类: FileInputStream
装饰器类: BufferedInputStream ,  DataInputStream
是这关系吗 ? 因为InputStream本身是FileInputStream的父类 有点绕来着 . </div>2020-05-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/8d/a7/2176bbc5.jpg" width="30px"><span>Giacomo</span> 👍（0） 💬（3）<div>能不能把BufferedInputStream这些可以叠加的功能做成interface，然后定义一些内部的类</div>2020-07-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/62/bb/323a3133.jpg" width="30px"><span>下雨天</span> 👍（571） 💬（36）<div>你是一个优秀的歌手，只会唱歌这一件事，不擅长找演唱机会，谈价钱，搭台，这些事情你可以找一个经纪人帮你搞定，经纪人帮你做好这些事情你就可以安稳的唱歌了，让经纪人做你不关心的事情这叫代理模式。
你老爱记错歌词，歌迷和媒体经常吐槽你没有认真对待演唱会，于是你想了一个办法，买个高端耳机，边唱边提醒你歌词，让你摆脱了忘歌词的诟病，高端耳机让你唱歌能力增强，提高了基础能力这叫装饰者模式。</div>2020-02-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/47/31/f35367c8.jpg" width="30px"><span>小晏子</span> 👍（341） 💬（10）<div>对于添加缓存这个应用场景使用哪种模式，要看设计者的意图，如果设计者不需要用户关注是否使用缓存功能，要隐藏实现细节，也就是说用户只能看到和使用代理类，那么就使用proxy模式；反之，如果设计者需要用户自己决定是否使用缓存的功能，需要用户自己新建原始对象并动态添加缓存功能，那么就使用decorator模式。</div>2020-02-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/17/27/ec30d30a.jpg" width="30px"><span>Jxin</span> 👍（160） 💬（12）<div>今天的课后题：
1.有意思，关于代理模式和装饰者模式，各自应用场景和区别刚好也想过。

1.代理模式和装饰者模式都是 代码增强这一件事的落地方案。前者个人认为偏重业务无关，高度抽象，和稳定性较高的场景（性能其实可以抛开不谈）。后者偏重业务相关，定制化诉求高，改动较频繁的场景。

2.缓存这件事一般都是高度抽象，全业务通用，基本不会改动的东西，所以一般也是采用代理模式，让业务开发从缓存代码的重复劳动中解放出来。但如果当前业务的缓存实现需要特殊化定制，需要揉入业务属性，那么就该采用装饰者模式。因为其定制性强，其他业务也用不着，而且业务是频繁变动的，所以改动的可能也大，相对于动代，装饰者在调整（修改和重组）代码这件事上显得更灵活。</div>2020-02-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/86/56/509535da.jpg" width="30px"><span>守拙</span> 👍（100） 💬（3）<div>补充关于Proxy Pattern 和Decorator Pattern的一点区别:

Decorator关注为对象动态的添加功能, Proxy关注对象的信息隐藏及访问控制.
Decorator体现多态性, Proxy体现封装性.

reference:
https:&#47;&#47;stackoverflow.com&#47;questions&#47;18618779&#47;differences-between-proxy-and-decorator-pattern</div>2020-02-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/88/b9/af5db174.jpg" width="30px"><span>andi轩</span> 👍（65） 💬（9）<div>对于为什么必须继承装饰器父类 FilterInputStream的思考：
装饰器如BufferedInputStream等，本身并不真正处理read()等方法，而是由构造函数传入的被装饰对象：InputStream（实际上是FileInputStream或者ByteArrayInputStream等对象）来完成的。
如果不重写默认的read()等方法，则无法完成如FileInputStream或者ByteArrayInputStream等对象所真正实现的read功能。
所以必须重写对应的方法，代理给这些被装饰对象进行处理（这也是类似于代理模式的地方）。
如果像DataInputStream和BufferedInputStream等每个装饰器都重写的这些方法话，会存在大量重复的代码。
所以让它们都继承FilterInputStream提供的默认实现，可以减少代码重复，让装饰器只聚焦在它自己的装饰功能上即可。</div>2020-04-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/82/83/8f168e4e.jpg" width="30px"><span>rammelzzz</span> 👍（36） 💬（2）<div>对于无需Override的方法也要重写的理解：
虽然本身BufferedInputStream也是一个InputStream，但是实际上它本身不作为任何io通道的输入流，而传递进来的委托对象InputStream才能真正从某个“文件”（广义的文件，磁盘、网络等）读取数据的输入流。因此必须默认进行委托。</div>2020-02-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/66/3c/2d563488.jpg" width="30px"><span>Yo nací para quererte.</span> 👍（34） 💬（4）<div>对于为什么中间要多继承一个FilterInputStream类，我的理解是这样的：
假如说BufferedInputStream类直接继承自InputStream类且没有进行重写，只进行了装饰
创建一个InputStream is = new BufferedInputStream(new FileInputStream(FilePath));
此时调用is的没有重写方法(如read方法)时调用的是InputStream类中的read方法，而不是FileInputStream中的read方法，这样的结果不是我们想要的。所以要将方法再包装一次，从而有FilterInputStream类，也是避免代码的重复，多个装饰器只用写一遍包装代码即可。</div>2020-02-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fa/ab/0d39e745.jpg" width="30px"><span>李小四</span> 👍（18） 💬（0）<div>设计模式_50:
# 作业

正如文中所说，装饰器是对原有功能的扩展，代理是增加并不相关的功能。
所以问题就变成使用者认为“缓存”是否扩展了原功能
- 比如说需要把想把所有的网络信息都加上缓存，提高一些查询效率，这时候应该使用代理模式；
- 如果我在设计网络通信框架，需要把提供“缓存”作为一种扩展能力，这时应该用装饰器模式；

现实中，大部分的网络缓存都以代理模式被实现。

另外，缓存(Cache)与缓冲(Buffer)是不同的概念，这里也可以区分一下。

# 感受
到了具体模式的课程，有一个明显的特点：一句话感觉看懂了，反复读才能发现有更多的信息在里面，坦白讲，很多模式编程中没有用过，与单纯地读原理和特征相比，我想真正用的时候才能理解更深入的东西。</div>2020-03-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/a5/4f/592d00f2.jpg" width="30px"><span>岁月神偷</span> 👍（14） 💬（1）<div>我觉得应该用代理模式，当然这个是要看场景的。代理模式是在原有功能之外增加了其他的能力，而装饰器模式则在原功能的基础上增加额外的能力。一个是增加，一个是增强，就好比一个是在手机上增加了一个摄像头用于拍照，而另一个则是在拍照这个功能的基础上把像素从800W提升到1600W。我觉得通过这样的方式区分的话，大家互相沟通起来理解会统一一些。</div>2020-02-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1a/f3/41d5ba7d.jpg" width="30px"><span>iLeGeND</span> 👍（10） 💬（7）<div>
&#47;&#47; 代理模式的代码结构(下面的接口也可以替换成抽象类)
public interface IA {
  void f();
}
public class A impelements IA {
  public void f() { &#47;&#47;... }
}
public class AProxy impements IA {
  private IA a;
  public AProxy(IA a) {
    this.a = a;
  }
  
  public void f() {
    &#47;&#47; 新添加的代理逻辑
    a.f();
    &#47;&#47; 新添加的代理逻辑
  }
}

&#47;&#47; 装饰器模式的代码结构(下面的接口也可以替换成抽象类)
public interface IA {
  void f();
}
public class A impelements IA {
  public void f() { &#47;&#47;... }
}
public class ADecorator impements IA {
  private IA a;
  public ADecorator(IA a) {
    this.a = a;
  }
  
  public void f() {
    &#47;&#47; 功能增强代码
    a.f();
    &#47;&#47; 功能增强代码
  }
}

老师 上面代码结构完全一样啊 不能因为 f() 中写的 逻辑不同  就说是两种模式吧  </div>2020-02-26</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIaOAxRlZjFkGfRBn420LuAcyWkMrpq5iafGdqthX5icJPjql0ibZOAdafaqbfvw4ZpVzDmsaYglVXDw/132" width="30px"><span>唐朝农民</span> 👍（8） 💬（3）<div>订单的优惠有很多种，比如满减，领券这样的是不是可以使用decorator 模式来实现</div>2020-02-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/6d/4e/347c3e8f.jpg" width="30px"><span>楚小奕</span> 👍（6） 💬（1）<div>我觉得不要纠结代理和装饰吧， 自己清楚设计意图就好</div>2021-01-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/e1/32/671b3d70.jpg" width="30px"><span>思君满月</span> 👍（5） 💬（1）<div>可以从两方面区分：
功能：装饰器强调对现有功能的强化，代理强调对其他功能的补充。比如高赞回答“歌手”的例子——经纪人帮歌手处理洽谈、报价等一些运营工作，这是歌手不具备的能力，即代理；高端耳机帮助歌手更好的演唱，这是歌手已具备的能力，是锦上添花，即装饰。
用户关注：代理的功能往往是用户不关注而系统关注的；而装饰器的功能往往是用户关注的。比如，歌迷不关心经纪人的工作，却希望歌手唱的更好。对于用户不关注的东西要默默地做，比如Spring框架常常使用的动态代理。因为不是用户关注的焦点，所以要让用户更少的接入或不介入。

不过，它们的区别真的有这么重要吗？

不知道大家有没有跟我一样的疑问：明明Spring和JDK中用到了大量的设计模式，为什么却很少在类名上体现出来呢？比如BufferedInputStream为啥不叫BufferedInputStreamDecrator呢？

我以前用设计模式经常这么干——比如我写单例，就叫XxxSingleton；我写策略，就叫XxxStrategy；我写装饰器，就叫XxxDecrator。我恨不得告诉所有人，我用了设计模式。

但是随着代码写的越来越多，我逐渐放弃这么干。主要原因有三：
1. 保持类名简单，这个没什么好说的。
2. 保持类名更有语义。将模式名写到类名上，可能促使我写出UserStrategy这样的代码。“用户策略”，用户的什么策略呢？将你把“Strategy”从类名移除后，你就会发现这个名字起的有多离谱——我们应该更加关注类本身的职责，而不是用了什么模式。
3. 给未来的扩展留有余地。

第三点我们单独拿出来说。比如，开始我们有一个XxxDecrator类，现在我们想对它进行扩展。可是我们加的这段代码不是装饰器的职责，而是代理的职责。这个时候你就不能直接把代码加到Decrator中，这叫挂羊头卖狗肉。这时候你可能会说，我再写一个XxxProxy不就得了——当你尝试用一个设计模式，去填另一个设计模式的坑时，你自己可能就掉进了坑里。

设计模式本身就是用复杂度换扩展性，我们需要在引入设计模式之前，考虑引入复杂度的必要性。

回到上面第三点，难道我们不引入XxxProxy我们就解决不了这个问题了吗？当然能，把类名中的Decrator去掉不就得了，既然要去掉那干脆定义的时候就别加上。

疾风剑豪说过：“模式存于心，而非流于行”。设计模式只是手段而不是目的，设计原则才是核心。我们只是在践行“组合优于继承”这个原则。

“我可没说我是装饰器，代理吗？也不一定哦。什么，你问我是什么？嗯......你说我是什么，我就是什么”。</div>2023-04-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c6/37/8d22be0a.jpg" width="30px"><span>木头</span> 👍（5） 💬（0）<div>看业务场景，如果只是针对某个类的某一个对象，添加缓存，那么就使用装饰模式。如果是针对这个类的所有对象，添加缓存。那么就使用代理模式</div>2020-02-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/e7/07/0e9d85c3.jpg" width="30px"><span>年轻的我们</span> 👍（4） 💬（2）<div>个人理解：装饰者模式就是代理模式中的静态代理模式，装饰类对于需要新增附加功能的方法，新增附加功能，对应不需要实现定制化功能的方法，继承和组合方式调用原始类功能即可</div>2020-03-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/42/76/256bbd43.jpg" width="30px"><span>松花皮蛋me</span> 👍（4） 💬（0）<div>通过将原始类以组合的方式注入到装饰器类中，以增强原始类的功能，而不是使用继承，避免维护复杂的继承关系。另外，装饰器类通常和原始类实现相同的接口，如果方法不需要增强，重新调用原始类的方法即可。
</div>2020-02-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/60/63/d2c91e2b.jpg" width="30px"><span>JoeyforJoy</span> 👍（3） 💬（1）<div>代理模式和装饰器模式的区别要从类的调用者的角度来看。
对于代理模式，调用者不需要知道代理类中有哪些额外的功能模块，直接调用代理类即可。正如我们找别人“代理”办事一样，我不需要知道代理人为我们多做了哪些事，我们只关心我们交代的事情有没有办好。
而对于装饰器模式，调用者则需要知道装饰类提供的额外的功能，来满足定制化的服务。就好比买手机时的套餐服务，我们不仅关心手机的好坏，我们还关心提不提供保修、送不送充电器等额外的服务。
回过头来回答课后问题，对于类的设计者来说，如果设计者认为“缓存”功能对于调用者来说在任何时刻都是必要的，那么则选择代理模式；如果设计者认为“缓存”功能对调用者来说是可有可无的，希望调用者根据自己的需要来定制的，那么则选择装饰器模式</div>2021-04-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4f/13/5197f8d2.jpg" width="30px"><span>永旭</span> 👍（3） 💬（2）<div>读了第三遍了 , JAVA IO 用例才理解透 ~~</div>2020-07-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8a/02/828938c9.jpg" width="30px"><span>Frank</span> 👍（3） 💬（0）<div>打卡 设计模式-装饰器模式
装饰器模式是一种类似于代理模式的结构型模式。主要意图是增强原始类的功能，可以实现多个功能的增强（即不同的功能单独一个类维护，使用该模式将其功能组合起来）。该模式主要是为了解决为了实现某些功能导致子类膨胀的问题。个人觉得主要体现了单一职责、组合优先于继承原则。主要应用场景有Java IO 流设计。但是有个疑惑，在Reader和Writer体系结构的设计中，并没有像InputStream和OutputStream那样设计一个过滤流类，而BufferedReader等直接继承了Reader。按照作者本文的分析，字符输入流直接跳过了使用中间类来继承的步骤，这样的设计又该如何理解？
对于课堂讨论，我觉得应该使用装饰器模式，因为“添加缓存”这个功能跟原始功能是由直接关系的。而代理模式所面向主要是将框架代码与业务代码解耦合。</div>2020-02-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f5/01/5389295c.jpg" width="30px"><span>查理</span> 👍（2） 💬（5）<div>还是不太懂代理模式和装饰器模式的区别，感觉他们太像了，只不过人为规定，代理模式新增的是与原始类不相关的功能，装饰器模式是对原始功能的增强，但是他们在代码类结构上是相同的。</div>2020-09-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/df/1e/cea897e8.jpg" width="30px"><span>传说中的成大大</span> 👍（2） 💬（0）<div>关于思考题 我觉得首先还是总结一下 代理模式和装饰器模式的区别
代理模式 主要是外部增强功能
装饰器模式主要是内部增强功能
首先从i&#47;o来看  他增加缓存的目的在于 提高效率 避免 不停的内存和硬盘之间的切换 是增强了读取功能
而代理模式 可能增加缓存是为了检查或者验证 或者写日志查看操作内容 这种外部功能的话 就应该用代理模式</div>2020-03-04</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/F5Srwp8IibOU9PDCDgmpdIZF9UXQZzfPKzNseHW5GR0WmusGfrkmzQ6wq32omW3uTtl8aXjkudYSA0NEmibxAcnw/132" width="30px"><span>嘿泥鳅</span> 👍（2） 💬（0）<div>添加缓存这个功能与父类或者接口定义的功能无关应该使用代理模式。</div>2020-03-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/86/56/509535da.jpg" width="30px"><span>守拙</span> 👍（2） 💬（0）<div>如果仅添加缓存一个功能, 使用Proxy好一些, 如果还有其他需求, 使用Decorator好一些.
如果让我选择的话, 我宁愿选择Decorator, 方便扩展, 符合开闭原则. </div>2020-02-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/82/3d/356fc3d6.jpg" width="30px"><span>忆水寒</span> 👍（2） 💬（0）<div>如果只是需要对所有 对象的缓存功能进行增强（相当于缓存是新的功能了），则可以使用代理模式。
如果只是对某一类对象进行增强，而这类对象有共同的接口或父类，则可以使用装饰模式。</div>2020-02-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/84/9e/d4c0e2c4.jpg" width="30px"><span>Broadm</span> 👍（1） 💬（0）<div>感觉装饰器模式,更像是多重代理, 在一个代理的基础上,继续代理</div>2022-06-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/97/81/c457def1.jpg" width="30px"><span>鹤涵</span> 👍（1） 💬（0）<div>代理模式无侵入的增加跟业务无关功能。
装饰器模式增强原类，与业务相关。</div>2020-12-28</li><br/>
</ul>