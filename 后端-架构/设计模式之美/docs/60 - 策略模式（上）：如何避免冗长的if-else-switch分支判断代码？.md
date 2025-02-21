上两节课中，我们学习了模板模式。模板模式主要起到代码复用和扩展的作用。除此之外，我们还讲到了回调，它跟模板模式的作用类似，但使用起来更加灵活。它们之间的主要区别在于代码实现，模板模式基于继承来实现，回调基于组合来实现。

今天，我们开始学习另外一种行为型模式，策略模式。在实际的项目开发中，这个模式也比较常用。最常见的应用场景是，利用它来避免冗长的if-else或switch分支判断。不过，它的作用还不止如此。它也可以像模板模式那样，提供框架的扩展点等等。

对于策略模式，我们分两节课来讲解。今天，我们讲解策略模式的原理和实现，以及如何用它来避免分支判断逻辑。下一节课，我会通过一个具体的例子，来详细讲解策略模式的应用场景以及真正的设计意图。

话不多说，让我们正式开始今天的学习吧！

## 策略模式的原理与实现

策略模式，英文全称是Strategy Design Pattern。在GoF的《设计模式》一书中，它是这样定义的：

> Define a family of algorithms, encapsulate each one, and make them interchangeable. Strategy lets the algorithm vary independently from clients that use it.
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/16/25/1f/8e304ec0.jpg" width="30px"><span>卖火柴的托儿索</span> 👍（9） 💬（3）<div>这个策略和多态有什么区别？感觉用法差不多</div>2020-04-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/10/22/910f705c.jpg" width="30px"><span>改名不换人</span> 👍（3） 💬（3）<div>请问各位一个问题：如果在spring应用中，Map策略表中的对象应该是new创建的，还是用autowired注入？</div>2020-07-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/11/f5/039f003d.jpg" width="30px"><span>宁锟</span> 👍（275） 💬（22）<div>仍然可以用查表法，只不过存储的不再是实例，而是class，使用时获取对应的class，再通过反射创建实例</div>2020-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/62/bb/323a3133.jpg" width="30px"><span>下雨天</span> 👍（86） 💬（3）<div>策略模式和工厂模式区别：

工厂模式
1.目的是创建不同且相关的对象
2.侧重于&quot;创建对象&quot;
3.实现方式上可以通过父类或者接口
4.一般创建对象应该是现实世界中某种事物的映射，有它自己的属性与方法！

策略模式
1.目的实现方便地替换不同的算法类
2.侧重于算法(行为)实现
3.实现主要通过接口
4.创建对象对行为的抽象而非对对象的抽象，很可能没有属于自己的属性。</div>2020-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/73/a3/2b077607.jpg" width="30px"><span>Michael</span> 👍（48） 💬（0）<div>一般而言Java web开发中我们均使用spring框架，可以使用运行时自定义注解给具体的策略类打上注解，将具体的策略类放于spring 容器中，工厂中注入直接根据类型获取即可.不实用spring框架的话，也可以用Java的反射做到获取到具体的策略类</div>2020-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/86/25/25ded6c3.jpg" width="30px"><span>zhengyu.nie</span> 👍（29） 💬（4）<div>查表策略还是挺常见的，搭配java.util.function各种接口挺好用的。

    private final Map&lt;String, Function&lt;String, String&gt;&gt; PHONE_FUN_FACTORY =
        ImmutableMap.of(
            MessageDestination.LEGAL_PERSON.name(), legalPersonPhoneFunc(),
            MessageDestination.ACTUAL_CONTROL.name(), actualPersonPhoneFunc()
        );

我比较喜欢建一个StrategyContext类，简单工厂+策略模式。
Context类存在一个成员变量xxx，new StrategyContext(xxx).apply();
然后StrategyContext内部存放一个表，value是一堆function，通过成员变量查表找对应的func.apply即可</div>2020-05-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/14/ee/d72a8222.jpg" width="30px"><span>攻城拔寨</span> 👍（25） 💬（0）<div>策略模式通常跟工厂一起配合使用。
策略侧重如何灵活选择替换，
工厂侧重怎么创建实例</div>2020-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/70/1a/cf0dbaac.jpg" width="30px"><span>Jasongrass</span> 👍（17） 💬（5）<div>if else 不是必须要解决的问题，如果放在工厂类中，逻辑比较简单，未来的变动也不会很大，就是 OK 的。</div>2020-03-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1d/de/62bfa83f.jpg" width="30px"><span>aoe</span> 👍（16） 💬（2）<div>原来策略模式的精髓就是：用Map代替冗长的if-else&#47;switch分支判断！
哇！</div>2020-07-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d5/8a/7050236a.jpg" width="30px"><span>东征</span> 👍（12） 💬（2）<div>仍然使用查表法，表中存类型和class，根据类型获取对象时，使用class动态创建。或者表中存类型和一个创建函数，根据类型获取对象时，获取到创建函数，调用创建函数创建新对象（java里可以用lambda或者对象代替函数）</div>2020-04-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/68/fe/1353168d.jpg" width="30px"><span>岁月</span> 👍（7） 💬（0）<div>课堂讨论
字典里保存好创建新对象的闭包代码块即可，或者说是回调函数，这样就可以创建出新的对象了，我们项目就是用的这个方法</div>2020-04-01</li><br/><li><img src="" width="30px"><span>Geek_3231cf</span> 👍（6） 💬（1）<div>可以在策略接口中，再抽象出来一个bool switch(T condition)方法，将判断移至具体策略实现类
工厂中getDiscountStrategy()方法中拿到所有策略类，根据condition找到符合的策略
伪代码：
DiscountStrategy getDiscountStrategy(T condition)
{ 
allStartegys.foreach(
if(switch(condition) 
return thisStartegy;
))}
使用起来就是DiscountStrategyFactory.getDiscountStrategy(condition).discount(order);</div>2020-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/17/27/ec30d30a.jpg" width="30px"><span>Jxin</span> 👍（6） 💬（5）<div>1.业务代码少用反射。这个场景和原型模式的应用场景很贴合。依旧是type查表，只是每次使用的都是type对应策略实例的copy对象。详细请参照spring原型模式的实现。

2.往往业务场景里面，往往不是选择策略这一场景，而是编排策略这一场景。即利用type查表拿出一堆要用到的策略，并按顺序去执行。对于这种场景，栏主怎么看？</div>2020-03-20</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/OYQh8KlUgMx0sZ35felqqRlboXkcOFib0qGgRHuvFCNIMzxRzxN8SjZpwtDuS0PGV0L0Pneiak7yzcd043f2efbg/132" width="30px"><span>Geek_78eadb</span> 👍（5） 💬（3）<div>如果我说，这个例子就是工厂模式，并且可以放到工厂方法的那一章，该怎么反驳我？
1. 为什么算法类的实例化就不是对象（工厂解决的是创建对象的问题，算法类难道不是对象吗）？
2. 工厂模式为什么不能用查表法解决，如果可以，为什么不能说工厂模式与策略模式一样（不要说关注角度不一样，我粗俗认为对象和类可以包含任何情况，比如算法类）？</div>2020-11-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/73/a3/2b077607.jpg" width="30px"><span>Michael</span> 👍（4） 💬（0）<div>我觉得结合下Spring中的应用场景讲下，毕竟大家都是依赖Spring开发的</div>2020-03-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1d/13/31ea1b0b.jpg" width="30px"><span>峰</span> 👍（4） 💬（0）<div>就像老师说的，替换麻烦的ifelse本质上靠的是查表法，也就是if 里的条件成立绑定对应的方法地址，所以其实感觉和策略模式本身没有半毛钱关系，只不过在策略模式这个上下文下，每个条件分支是可扩展的策略实现而不是差别很大的功能代码。</div>2020-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/55/7a/d44df1d6.jpg" width="30px"><span>freesocean</span> 👍（3） 💬（0）<div>思考：
工厂模式和策略模式等区别， 学到这里大概理解了一些争哥之前谈到的，模式都是为了应对某些场景，今天这个就很典型，如果只看代码，觉得和简单工厂很像，但是从问题入手，从场景谈起，两者解决的就完全是不同的问题，一个是解决对象创建相关，一个是不同策略不同行为。从这个层面两者又是不同。最近学了设计模式，所以有个毛病就是看一些源码，总是想往某个模式套，心里总是想这里是不是用到了某个模式，但常常又是一脸懵逼，其实是搞错了顺序，应该是看代码这样写时为了解决什么问题，是问题定义了模式，具体到模式名称，其实都不重要了，甚至你完全为了解决某个问题，创造一个新的模式（当然有可能应用场景不多罢了），所以还是见的少，后边继续加强实战，忘记模式，代码合一的境界，那就差不多了</div>2021-10-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/53/ae/a08024b2.jpg" width="30px"><span>Luke</span> 👍（3） 💬（1）<div>想到的一个「策略模式」使用场景是: 根据数据查看权限进行列表筛选。
比如，数据表中有三类数据:
 - 分类 A
 - 分类 B
 - 分类 C
针对这三类数据，是提供给不同角色的人员查看:
 - 角色 1
 - 角色 2
 - 角色 3
通过策略对数据进行筛选，分别是: 
 - 「角色 1」对应 「分类 A」数据
 - 「角色 2」对应 「分类 B」数据
 - 「角色 3」对应 「分类 C」数据
不知道这种方式是否是符合「策略模式」的使用场景。是否还有更好的方式来解耦人员和数据的关系呢？</div>2020-04-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/4e/d0/d8a5f720.jpg" width="30px"><span>Ken张云忠</span> 👍（3） 💬（1）<div>实际上，今天举的例子不用访问者模式也可以搞定，你能够想到其他实现思路吗？
可以使用策略模式.
定义读取策略接口ExtractorStrategy并实现三个策略,再定义一个策略工厂类,以文件类型作为key,以对应策略实现作为value,使用时通过具体的ResourceFile类型获取对应的策略实现类型,然后再调用实现函数.</div>2020-04-08</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/bvj76PmeUvW8kokyu91IZWuRATKmabibDWbzAj2TajeEic7WvKCJOLaOh6jibEmdQ36EO3sBUZ0HibAiapsrZo64U8w/132" width="30px"><span>梦倚栏杆</span> 👍（3） 💬（0）<div>课后问题回答：
在springboot框架下很容易实现。
private final List&lt;DiscountStrategy&gt; strategyList;

spring 的特性会自动将所有的DiscountStrategy实现类注入到strategyList，
然后strategyList.stream().filter(DiscountStrategy::match).findFirst().map(ApplicatonContext::getBean).orElseThrow(()-&gt;new Exception(&quot;找不到合适的策略&quot;));
将每一个DiscountStrategy的实现类的scope注解设置为原型模式。

不过这样两个缺点：
1.每一个策略类都会先创建一个对象，作用仅仅是为了可以调用match方法。
2.像这种每一个都需要一个新的bean场景，一般这种策略也依赖当时的场景参数，但是当时的场景参数却无法通过构造函数传达，只能作为方法的参数
</div>2020-03-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/54/9a/76c0af70.jpg" width="30px"><span>每天晒白牙</span> 👍（3） 💬（3）<div>我们的项目就使用了这种动态的策略模式，减少 if-else</div>2020-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/43/79/18073134.jpg" width="30px"><span>test</span> 👍（3） 💬（0）<div>用查表法缓存clasa</div>2020-03-20</li><br/><li><img src="" width="30px"><span>Geek_1f0e17</span> 👍（2） 💬（0）<div>还是用查表法，工厂方法模式就行，value存工厂，第44讲已经提过了</div>2021-08-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/65/19/9f59254f.jpg" width="30px"><span>小笨瓜</span> 👍（1） 💬（0）<div>所以使用if&#47;else就差别很大？？？</div>2023-06-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/7d/c2/e6332a1b.jpg" width="30px"><span>东方拓睿</span> 👍（1） 💬（0）<div>怎么感觉查表法也是if-else判断的一种，事情是一样做，但是if-else还更直观一点，别人来看代码还要先理解你的策略类，而且随着策略的增多，策略类也增多？</div>2022-06-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/fb/6c/12fdc372.jpg" width="30px"><span>被水淹没</span> 👍（1） 💬（0）<div>有的评论说比较像工厂类，我也有这个疑问，示例中的代码看起来好，

不过按照我的理解，工厂应该侧重于创建，策略侧重于算法


我看别的策略模式文章一般都有带一个上下文的类，比如Cache就是一个Context，Context中组合了策略类，Cache包含了外部属性（如数据），可以通过Cache来设置策略类（如LRU、LFU），并通过Cache提供的方法来使用策略。让你能够在**同一个上下文**类中切换算法。

</div>2021-12-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/aa/3d/c14e338e.jpg" width="30px"><span>建锋</span> 👍（1） 💬（1）<div>spring环境下，可以通过  @Autowire  Map&lt;String, Strategy&gt; map；实现工厂的功能。其中Key为Bean名称，value为具体的对应策略类
</div>2021-03-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/20/d6/b9513db0.jpg" width="30px"><span>kingcall</span> 👍（1） 💬（0）<div>工厂模式和策略模式有类似的流程，就是对象的创建，但是使用场景是不同的，策略模式的场景是行为切换，而工厂模式是对象创建；或者说是策略模式中使用到了工厂模式</div>2020-04-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/2f/7a/ab6c811c.jpg" width="30px"><span>相逢是缘</span> 👍（1） 💬（0）<div>一、定义（理解）：
定义一族算法类，将每个算法分别封装起来，让它们可以互相替换。策略模式可以使算法的变化独立于使用它们的客户端（这里的客户端代指使用算法的代码）。

二、使用场景：
需要根据情况使用不同的算法类。

三、实现方式：
1、策略类的定义比较简单，包含一个策略接口和一组实现这个接口的策略类。
2、策略的创建由工厂类来完成，封装策略创建的细节。
3、策略模式包含一组策略可选，客户端代码如何选择使用哪个策略，有两种确定方法：编译时静态确定和运行时动态确定。其中，“运行时动态确定”才是策略模式最典型的应用场景。

四、工厂模式和策略模式的区别
工厂模式
1.目的是创建不同且相关的对象
2.侧重于&quot;创建对象&quot;
3.实现方式上可以通过父类或者接口

策略模式
1.目的实现方便地替换不同的算法类
2.侧重于算法(行为)实现
3.实现主要通过接口</div>2020-03-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8a/02/828938c9.jpg" width="30px"><span>Frank</span> 👍（1） 💬（0）<div>打卡 今日学习策略模式，收获如下：
策略模式，理解有多种策略可供使用，怎么使用。文章中提到三部分：策略的定义，策略的创建，策略的使用。定义：需要定义策略接口和一组实现类，使用基于接口而非实现编程可灵活替换不同的类，各个实现类可独立变化。创建： 创建策略类时，为了封装创建细节，
使用简单工厂方法。根据策略类状态特性（可变类与不可变类）来判断是使用可缓存的，还是每次都返回新的。使用：基于两种方式：运行时动态确定和编译时静态确定，前者使用灵活，外界可灵活介入，后者硬编码，存在一定维护成本。
课堂讨论中的问题可通过工厂方法即将不同的折扣策略计算对象的创建在拆分出来形成一个个小工厂，在小工厂里创建折扣策略对象，然后再使用简单工厂模式里面的第二种方式缓存这些小工厂，使用的时候根据类型返回小工厂，进而通过小工厂拿到相应的折扣策略对象。</div>2020-03-21</li><br/>
</ul>