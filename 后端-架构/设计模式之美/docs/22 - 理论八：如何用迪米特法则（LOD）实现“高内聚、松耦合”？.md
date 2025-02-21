今天，我们讲最后一个设计原则：迪米特法则。尽管它不像SOLID、KISS、DRY原则那样，人尽皆知，但它却非常实用。利用这个原则，能够帮我们实现代码的“高内聚、松耦合”。今天，我们就围绕下面几个问题，并结合两个代码实战案例，来深入地学习这个法则。

- 什么是“高内聚、松耦合”？
- 如何利用迪米特法则来实现“高内聚、松耦合”？
- 有哪些代码设计是明显违背迪米特法则的？对此又该如何重构？

话不多说，让我们开始今天的学习吧！

## 何为“高内聚、松耦合”？

“高内聚、松耦合”是一个非常重要的设计思想，能够有效地提高代码的可读性和可维护性，缩小功能改动导致的代码改动范围。实际上，在前面的章节中，我们已经多次提到过这个设计思想。很多设计原则都以实现代码的“高内聚、松耦合”为目的，比如单一职责原则、基于接口而非实现编程等。

实际上，“高内聚、松耦合”是一个比较通用的设计思想，可以用来指导不同粒度代码的设计与开发，比如系统、模块、类，甚至是函数，也可以应用到不同的开发场景中，比如微服务、框架、组件、类库等。为了方便我讲解，接下来我以“类”作为这个设计思想的应用对象来展开讲解，其他应用场景你可以自行类比。

在这个设计思想中，“高内聚”用来指导类本身的设计，“松耦合”用来指导类与类之间依赖关系的设计。不过，这两者并非完全独立不相干。高内聚有助于松耦合，松耦合又需要高内聚的支持。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/ee/18/65e89d9c.jpg" width="30px"><span>王大喵</span> 👍（20） 💬（2）<div>联系：
“接口隔离原则”是客户端不应该被强迫依赖不需要的接口，和“迪米特法则”中的有限知识异曲同工，接口簇会更加“单一职责”实现方式“基于接口而非实现编程”，达到的目的是高内聚，松耦合。

区别：
1. 各种原则最终的目的是为了实现“高内聚、松耦合”。
2. 单一职责原则 主要是指导类和模块，避免大而全，提高内聚性。
3. 接口隔离和迪米特(最小知识)主要指导“松耦合”，解耦使用方的依赖。
4. 基于接口而非实现编程：主要是解耦接口和实现，是指导思想，提高扩展性。</div>2020-11-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/30/91/5f770e29.jpg" width="30px"><span>戒惜舍得</span> 👍（4） 💬（2）<div>相近的功能。 怎么算相近啊。学晕了。</div>2019-12-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d8/58/1f5f7aed.jpg" width="30px"><span>提姆</span> 👍（3） 💬（2）<div>老师您好，请问一下Document的修改为什么会使用到Factory的方式去产生？我对这一步的修改没有很大的感受，我这里的认知是Document只是单纯对文件的操作，那是不是可以透过HtmlDownloader实现相关取得文件的接口，像是IDownloader之类的名称，并直接回传Document这个类(亦或者对此类做其它的延伸)，未来也可以实现其它像是json等其他格式的downloader，不知道我这个想法是不是可行？</div>2020-07-07</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/6cyOoRd2dROgiblAJkW6RLhUyH1wwU0NNibIIuV930eQ9TiaNT41K61kBSVkvYoDYg7mJtuEoCQY1awBmV0WW6BFg/132" width="30px"><span>大方方</span> 👍（0） 💬（2）<div>我想知道假如 

Public class NetworkTransporter { 
   &#47;&#47; 省略属性和其他方法...    
 public Byte[] send(HtmlRequest htmlRequest) {      

   &#47;&#47;...    }}
中的send 方法，必须需要HtmelRequest 才能实现功能呢？ 老师修改后，参数上看起来是不依赖外部对象了，但是在很多其他实际操作时，很有可能还是需要用到外部对象来解决问题。 这种情况是不是需要做类扩展，在扩展中再具体引用HtmlRequest ?</div>2020-06-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/56/c6/0b449bc6.jpg" width="30px"><span>斐波那契</span> 👍（0） 💬（3）<div>老师 我有一个问题：在项目开发中，我写了一个类A 里面定义了一个方法，后来又写了一个类B 发现在B里面要用到A里面定义的那个方法(基本上一模一样)，但是A跟B本身是两个不相关的类 这个时候要怎么解决? PS:这个方法不能算作是工具类，只是一段数据集的处理逻辑 那是否是搞一个抽象类 然后让A和B继承这个抽象类 把那个方法写进抽象类里?</div>2019-12-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/44/54/7e40e592.jpg" width="30px"><span>prowu</span> 👍（0） 💬（2）<div>一直有一个消息结构与程序内部数据结构取舍的问题：程序内部是否直接复用消息协议的结构？比如：通讯消息使用的是protobuf协议，那程序内部的逻辑是直接使用protobuf的数据结构，还是自己在定义一套结构体？如果直接使用protobuf协议，那程序就紧耦合于协议了（这边就是与protobuf绑在一起了），如果自己在定义一套结构体，那就要多一层协议与内部结构的转换。</div>2019-12-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/37/4e/5c3153b2.jpg" width="30px"><span>知行合一</span> 👍（386） 💬（9）<div>目的都是实现高内聚低耦合，但是出发的角度不一样，单一职责是从自身提供的功能出发，迪米特法则是从关系出发，针对接口而非实现编程是使用者的角度，殊途同归。</div>2019-12-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/62/bb/323a3133.jpg" width="30px"><span>下雨天</span> 👍（239） 💬（12）<div>1.单一职责原则	
适用对象:模块，类，接口 
侧重点:高内聚，低耦合	
思考角度:自身

2.接口隔离原则
适用对象:接口，函数	
侧重点:低耦合	
思考角度:调用者

3.基于接口而非实现编程 
适用对象:接口，抽象类	
侧重点:低耦合 
思考角度:调用者

4.迪米特法则	
适用对象:模块，类	
侧重点:低耦合	
思考角度:类关系</div>2019-12-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/4e/d0/d8a5f720.jpg" width="30px"><span>Ken张云忠</span> 👍（58） 💬（0）<div>“高内聚、松耦合”“单一职责原则”“接口隔离原则”“基于接口而非实现编程”“迪米特法则”，它们之间的区别和联系吗？
区别:
高内聚、松耦合:是一个重要的设计思想,能够有效地提高代码的可读性和可维护性,缩小功能改动导致的代码改动范围.
单一职责原则:A class or module should have a single reponsibility.提供的功能上要单一.
接口隔离原则:Clients should not be forced to depend upon interfaces that they do not use.与外部关系上只依赖需要的抽象.
基于接口而非实现编程:Program to an interface, not an implementation.是一条比较抽象、泛化的设计思想,为了提高代码的灵活性&#47;扩展性&#47;可维护性.
迪米特法则:Each unit should have only limited knowledge about other units: only units “closely” related to the current unit. Or: Each unit should only talk to its friends; Don’t talk to strangers.每个单元只该依赖与它关系密切的单元,最少知道,只与关系密切的单一交互.
联系:
职责越单一越容易做到接口隔离,也越容易做到最少知道的迪米特法则.
基于抽象编程抽象的知识越顶层越脱离具体实现,相对知道的内容就越少,也容易实现迪米特法则.
接口隔离原则与迪米特法则都强调只依赖需要的部分,接口隔离原则是相对偏上层来说的,迪米特法则是相对偏具体实现来说的.
单一职责原则&#47;接口隔离原则&#47;基于接口而非实现编程&#47;迪米特法则都以实现代码的&quot;高内聚、松耦合&quot;为目的,提高代码的可读性和可维护性,缩小功能改动导致的代码改动范围,降低风险.</div>2019-12-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/50/d7/f82ed283.jpg" width="30px"><span>辣么大</span> 👍（42） 💬（24）<div>关于LoD，请记住一条：方法中不要使用ChainMethods。

坏的实践：
Amount = customer.orders().last().totals().amount()
和
orders = customer.orders()
lastOders = orders.last()
totals = lastOders.totals()
amount = totals.amount()

上面的例子中，chain中的方法改变会影响很多地方。这里注意区别建造者模式和pipeline管道，这两种的chain中的方法不易改变。

出现这样的代码，需要考虑可能是设计或实现出了问题。

LoD如何使用：
一个类C中的方法只能调用：
1、C中其他实例方法
2、它自己的参数方法
3、它创建对象的方法
4、不要调用全局变量（包括可变对象、可变单例）
例如：
class HtmlDownloader{
  Html html;
  public void downloadHtml(Transporter trans, String url){
    if(checkUrl(url)){&#47;&#47; ok 自己的实例方法
      &#47;&#47; return
    }
    rawData = trans.send(uri);&#47;&#47; ok 参数对象的方法
    Html html = createHtml(rawData); &#47;&#47; ok 它创建的对象
    html.save();&#47;&#47; ok  它创建对象的方法
  )
  private boolean checkUrl(String url){
    &#47;&#47; check
  }
}

参考：
The Pragmatic Programmer 1st edition and 2nd edition
</div>2019-12-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4a/6f/e36b3908.jpg" width="30px"><span>xzy</span> 👍（21） 💬（0）<div>看一遍，真的不行，每次看都有新收获！</div>2020-02-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/dd/98/883c42b4.jpg" width="30px"><span>LiuHu</span> 👍（15） 💬（0）<div>“高内聚、松耦合” 是衡量好代码的标准之一，为了实现这样的目标，我们需要遵循如下原则：
“基于接口而非实现编程”，接口本身就是一层抽象，接口是稳定的，实现是易变的，强调的是基于契约编程，这样能够隔离变化。实现细节代码的变化，不影依赖该接口的对象，到从而达到松耦合的目的。
“迪米特法则”，定义的是发布的接口（类、模块等）能不能依赖，如何依赖的问题。使用者去除不必要的依赖，只依赖必要的接口。这样即使接口一旦发生变化，需要了解这一变化的类就会比较少，达到松耦合的目的。
“接口隔离原则”，从使用者的角度考虑如何设计接口，让使用者只依赖必要的接口，不会被迫依赖不用的接口。这样即使接口一旦发生变化，需要了解这一变化的类就会比较少，这样就能符合 “迪米特法则” 。
“单一职责原则”，针对模块、类、接口的设计，将功能相关性很强的代码抽取到一起，达到高内聚的目标。</div>2019-12-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/ef/5b/ff28088f.jpg" width="30px"><span>郑大钱</span> 👍（9） 💬（0）<div>一不小心就能用到一个牛逼的原则，如果没有这些归纳总结的话，永远都不知道自己究竟有多牛逼。
是不是觉得迪米特法则和之前的原则很像，当然很像了，毕竟他们都是为了实现“高内聚，低耦合”。
【单一职责原则】是从自身功能出发，实现高内聚，低耦合
【接口隔离原则】和【基于接口而非实现编程】是从调用者出发，实现低耦合
【迪米特法则 】是从关系出发，实现低耦合</div>2020-09-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f7/9d/be04b331.jpg" width="30px"><span>落叶飞逝的恋</span> 👍（7） 💬（0）<div>课后讨论：代码的最终目的是高内聚、松耦合的。而为了达到这个目的，就需要利用到迪米特法则。而迪米特法则的实现，又需要利用单一职责将单个类定义职责单一化，并且为了解决多个类之间的关系，又需要用到基于接口编程而非实现编程。这样类与类之间就相当于契约化，也就是不关心类的具体实现。</div>2019-12-23</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/iaByN5IfYbE9jMtWrtTDXtPEIHeV77KW1p7ZkiasiaGgA50VXaibo4fbp5ib2JkFP3iaIe4AUudLibufkEIofu5euCNHg/132" width="30px"><span>小刀</span> 👍（3） 💬（0）<div>高内聚-低耦合
单一职责-自身功能出发
迪米特法则  类与类之间关系
接口而非实现编程-依赖必要的抽象</div>2019-12-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/7b/57/a9b04544.jpg" width="30px"><span>QQ怪</span> 👍（3） 💬（0）<div>老师讲的真棒👍</div>2019-12-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/68/fe/1353168d.jpg" width="30px"><span>岁月</span> 👍（3） 💬（1）<div>如果说高内聚、松耦合等价于&quot;中国特色社会主义&quot;, 那么“单一职责原则”“接口隔离原则”“基于接口而非实现编程”“迪米特法则”这几个原则就像是在说如何才能做到做到这样的社会?  答案就是我们要&quot;倡导富强、民主、文明、和谐, 自由、平等、公正、法治，爱国、敬业、诚信、友善&quot;</div>2019-12-23</li><br/><li><img src="" width="30px"><span>Geek_809561</span> 👍（2） 💬（0）<div>单一职责原则：模块,类，方法等功能要单一。功能越单一的类，对外部依赖越少。高内聚。

接口隔离原则： 调用者调用被调用者的方法或功能的时候，这个方法或者功能的粒度要小，职责要单一。高内聚

单一职责和接口隔离的区别是：一个是偏向于整体的（类，模块，接口的）设计，而接口隔离知识对接口的设计。相同点都是要求单一职责，高内聚。

基于接口而非实现编程：将接口和实现分离。调用者只需要知道被调用者抽象出来的方法或功能，并不需要知道具体的细节是怎么执行的。降低了调用者和被调用者之间的耦合度。更偏向于整体的抽象思想。
接口隔离与基于接口而非实现编程：一个是对具体接口的要求，（单一），一个是要求将具体的行为和功能抽象化，为后续被调用的整体替换做准备。
迪米特法则：又叫做最少知识法则，降低调用者与被调用者之间的耦合度。调用者只关于自己必须知道的知识（没有就实现不了的）。</div>2020-11-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/68/fe/1353168d.jpg" width="30px"><span>岁月</span> 👍（2） 💬（2）<div>感觉NetworkTransporter这个例子举的不好... 
本身获取HTML确实可以通过通过HtmlRequest, 现在非得把他拆成一个地址和content, 那么地址和content分别传入什么呢? 这样做HtmlRequest这个类就没有存在的意义了.
下面document例子我比较认可. 确实document类只要把html字符串传进来即可, 至于谁去加载字符串这个不归他管</div>2020-05-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/37/3f/a9127a73.jpg" width="30px"><span>KK</span> 👍（2） 💬（0）<div>对LOD迪米特法则的形象理解：不要探究朋友的隐私，要与陌生人保持距离。😂</div>2020-04-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/60/16/d1dd4972.jpg" width="30px"><span>ismind</span> 👍（2） 💬（0）<div>前几天没抽出时间，今天补上。
1，感觉还是要做笔记，现在才知道要做一下笔记，不然前面学的基本上只是留个大概的印象，效率低
2，感觉开始有难度了，综合性更高了，开始加速了么？哈哈
课后思考：
1，这五个原则与思想，联系就是：都是为了提高代码的可读性、扩展性、灵活性等，这也是这些原则产生的原因之一，我觉得应该把握这个主要的目的，再去应用这些原则或者设计模式，否则单纯为了使用这些原则，那很可能适得其反，我又想起那句话：“不忘初心方得始终”，学习设计模式也要这样吧。
老师的代码实战二，简单的序列化使用LOD原则，感觉过度设计了，不过一看后面功能变复杂了，觉得设计才合理。
2，区别：应该是关注点不同吧，“高内聚、低耦合”关注的是类，也就是考虑类与类之间的关系；单一职责则是关注前几天没抽出时间，今天补上。
1，感觉还是要做笔记，现在才知道要做一下笔记，不然前面学的基本上只是留个大概的印象，效率低
2，感觉开始有难度了，综合性更高了，开始加速了么？哈哈
课后思考：
1，这五个原则与思想，联系就是：都是为了提高代码的可读性、扩展性、灵活性等，这也是这些原则产生的原因之一，我觉得应该把握这个主要的目的，再去应用这些原则或者设计模式，否则单纯为了使用这些原则，那很可能适得其反，我又想起那句话：“不忘初心方得始终”，学习设计模式也要这样吧。
老师的代码实战二，简单的序列化使用LOD原则，感觉过度设计了，不过一看后面功能变复杂了，觉得设计才合理。
2，区别：应该是关注点不同吧，“高内聚、低耦合”关注的是类，也就是考虑类与类之间的关系；单一职责则是关注某一个类或者函数的功能是否单一；接口隔离则关注不要依赖不需要的接口；基于接口而非实现编程就考虑将实现替换为接口。
自己感觉这些还没有彻底理解，只是大概知道，感觉离掌握与熟悉还有一段距离。</div>2019-12-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/ca/c7/00e544c2.jpg" width="30px"><span>黄林晴</span> 👍（2） 💬（0）<div>打卡
所有的设计原则都相辅相成</div>2019-12-23</li><br/><li><img src="" width="30px"><span>cloydlau</span> 👍（1） 💬（0）<div>用 TS 实现了一下序列化那块的代码：

interface Serializable {
  serialize: (object: object) =&gt; string
}

interface Deserializable {
  deserialize: (text: string) =&gt; object
}

class Serialization implements Serializable, Deserializable {
  serialize (object: object): string {
    return JSON.stringify(object)
  }

  deserialize (text: string): object {
    return JSON.parse(text)
  }
}

class DemoClass1 {
  serializer: Serializable

  constructor (serializer: Serializable) {
    this.serializer = serializer
  }
}

class DemoClass2 {
  deserializer: Deserializable

  constructor (deserializer: Deserializable) {
    this.deserializer = deserializer
  }
}

const demoClass1 = new DemoClass1(new Serialization())
const demoClass2 = new DemoClass2(new Serialization())

console.log(demoClass1.serializer.serialize({}))
console.log(demoClass1.serializer.deserialize(&#39;{}&#39;)) &#47;&#47; TS2551: Property &#39;deserialize&#39; does not exist on type &#39;Serializable&#39;. 

console.log(demoClass2.deserializer.deserialize(&#39;{}&#39;))
console.log(demoClass2.deserializer.serialize({})) &#47;&#47; TS2551: Property &#39;serialize&#39; does not exist on type &#39;Deserializable&#39;.</div>2021-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/83/96/73ff13a0.jpg" width="30px"><span>天亮前说晚安</span> 👍（1） 💬（0）<div>作者的第一个例子，最后的结果就不满足法则。改造后依然问题很大，Document对象可以认为是复杂对象，但是DocumentFactory不应该依赖HtmlDownloder，因为这是具体实现，非接口；第二前面讲到send方法都可能非HtmlRequest，那下载器也可能多个。应该抽离出Downloader接口，DocumentFactory依赖接口。</div>2021-12-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/63/6e/6b971571.jpg" width="30px"><span>Z宇锤锤</span> 👍（1） 💬（0）<div>高内聚，低耦合就是分门别类别掺和。 迪米特法则就是别和陌生人说话，只和熟人说话。调用过程中应该尽量解耦，尽量考虑使用。参考rule of three</div>2021-11-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c7/05/19c5c255.jpg" width="30px"><span>微末凡尘</span> 👍（1） 💬（0）<div>1.单一职责原则
适用对象:模块，类，接口
侧重点:高内聚，低耦合
思考角度:自身

2.接口隔离原则
适用对象:接口，函数
侧重点:低耦合
思考角度:调用者

3.基于接口而非实现编程
适用对象:接口，抽象类
侧重点:低耦合
思考角度:调用者

4.迪米特法则
适用对象:模块，类
侧重点:低耦合
思考角度:类关系</div>2021-01-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/13/45/16c60da2.jpg" width="30px"><span>蔫巴的小白菜</span> 👍（1） 💬（1）<div>感觉上面的代码还是有问题：
1. document就是一个纯粹的文档基类，为什么要依赖html，那么asp，jsp的网页不能解析？？？
</div>2020-03-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/33/d0/962ebe2e.jpg" width="30px"><span>Buring</span> 👍（1） 💬（0）<div>我的理解就是：
高内聚、低耦合：他强调的是不同的方法、类、模块之间的关系网的问题，是以一个上帝视角来观察的
单一职责原则：他强调的是某一个具体方法或者类或者模块，他们主要关注自己本身的实现代码是否相对独立，从而不会“自作多情”的把别人做的事再做一遍
接口隔离原则：在单一职责的基础之上，在给调用者提供api接口时，能让调用者很清晰的知道当前所依赖的接口有哪些接口，好比序列化的调用者只想要看到序列化接口，而不希望反序列化的接口也暴露
迪米特法则：在争哥总结的迪米特里，前者(尽量不依赖)，我觉得在真实业务系统还是很难做到的，因为业务错综复杂，所有的接口都可能被很多地方引用到，但是对于第二点(只依赖必要的接口)，很多时候还是可以尽量满足的，它其实就是接口隔离原则的体现
基于接口而非实现：基于接口而非实现，是上面所有原则的基石！</div>2020-03-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/f8/02/a02d127d.jpg" width="30px"><span>Treasure</span> 👍（1） 💬（0）<div>单一职责原则：一个类，只有一个引起它变化的原因。
接口隔离原则：不应该强迫用户依赖它们不需要的方法。（调用者）
迪米特法则   ：强调类之间的关系，依赖应该最小花。（模块&#47;类 的依赖关系）
基于接口编程而非实现编程：通用原则，一个比较笼统的思想。
都是为了实现高内聚，低耦合。</div>2020-01-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fa/ab/0d39e745.jpg" width="30px"><span>李小四</span> 👍（1） 💬（0）<div>设计模式_22:
# 作业
我认为，“高内聚，松耦合”更加底层，其他的原则更像是不同方向的应用。

# 感想：
“高内聚，松耦合”，好像是每一个学过计算机课程的人都熟记的概念，很多人也会在简历中写这一点，但是不同的人对于原则的理解程度是不同的，这些差异来自与信息量：
今天聊到设计原则是怎么来的，就是来自于之前的实践经验，发现并使用原则真实地解决了当时的问题，然后原则以“高内聚，松耦合”这样极简的文字流传下来，而其他的信息量全部丢失。
我们都有过这样的经历，真正地实践后，犯错后，发现自己真正理解了一个道理，虽然你早已听说过它。

其实实践的过程，就是信息量补充的过程；想要真正地理解这些原则，依然需要经历这些实践，需要这些信息量。</div>2019-12-25</li><br/>
</ul>