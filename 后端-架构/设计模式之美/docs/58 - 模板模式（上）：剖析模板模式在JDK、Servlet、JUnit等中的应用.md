上两节课我们学习了第一个行为型设计模式，观察者模式。针对不同的应用场景，我们讲解了不同的实现方式，有同步阻塞、异步非阻塞的实现方式，也有进程内、进程间的实现方式。除此之外，我还带你手把手实现了一个简单的EventBus框架。

今天，我们再学习另外一种行为型设计模式，模板模式。我们多次强调，绝大部分设计模式的原理和实现，都非常简单，难的是掌握应用场景，搞清楚能解决什么问题。模板模式也不例外。模板模式主要是用来解决复用和扩展两个问题。我们今天会结合Java Servlet、JUnit TestCase、Java InputStream、Java AbstractList四个例子来具体讲解这两个作用。

话不多说，让我们正式开始今天的学习吧！

## 模板模式的原理与实现

模板模式，全称是模板方法设计模式，英文是Template Method Design Pattern。在GoF的《设计模式》一书中，它是这么定义的：

> Define the skeleton of an algorithm in an operation, deferring some steps to subclasses. Template Method lets subclasses redefine certain steps of an algorithm without changing the algorithm’s structure.
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="" width="30px"><span>Geek_cead38</span> 👍（4） 💬（3）<div>我觉得即便是使用装饰器还是直接重写method1-4，对于需要子类重写的方法要么抛不支持异常，要么抽象，不然子类察觉不到必须重写，导致模板函数的业务出错</div>2020-11-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4a/96/99466a06.jpg" width="30px"><span>Laughing</span> 👍（1） 💬（2）<div>结尾问题有两种解决方法：
1. 写适配器来转化
2. 提供默认实现不要求强制实现</div>2020-11-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/14/ee/d72a8222.jpg" width="30px"><span>攻城拔寨</span> 👍（233） 💬（16）<div>文末的问题，在 spring 生命周期中，InstantiationAwareBeanPostProcessorAdapter
就是解决这个问题的。
写个适配器，把所有抽象方法默认实现一下，子类继承这个 adapter 就行了。</div>2020-03-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/42/e5/61cfe267.jpg" width="30px"><span>Eclipse</span> 👍（108） 💬（10）<div>可以借鉴AbstractList的addall实现。提供默认的方法method1...method4方法，每个方法直接抛出异常，使用模板方法的时候强制重写用到的method方法，用不到的method不用重写。</div>2020-03-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4c/12/f0c145d4.jpg" width="30px"><span>Rayjun</span> 👍（73） 💬（0）<div>如果两个模版方法没有耦合，可以拆分成两个类，如果不能拆分，那就为每个方法提供默认实现</div>2020-03-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/78/3e/84b18502.jpg" width="30px"><span>最好的狗焕啊</span> 👍（52） 💬（43）<div>争哥，一年前就很崇拜你了，但是现在很迷茫，三年的开发经验了，一直在小公司，做的项目最多的数据量也只是十几万的用户，平常下班每天都会坚持学习两个小时，已经坚持一年半了，看了数据结构和算法，还有认真刷过题，看了网络协议，也看了框架方面的书等等，也认真做了笔记，然后想投递独角兽公司，但是简历都不通过，理由是学历和项目都没有亮点，我是本科毕业，看了网上的一些阿里或者百度这样的公司的面试题，发现自己也会，但是投递的简历都不通过，真的很迷茫，不知道这样的坚持有没有用，现在想回到老家一个二线城市，做着一份养老的工作</div>2020-03-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/bc/25/1c92a90c.jpg" width="30px"><span>tt</span> 👍（28） 💬（0）<div>参考装饰器模式那一课中JAVA IO类库中的做法，引入一个中间父类，实现所有的抽象方法，然后再让业务类去继承这个中间的父类。</div>2020-03-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/54/9a/76c0af70.jpg" width="30px"><span>每天晒白牙</span> 👍（26） 💬（0）<div>提供一个 Base 类，实现 method1 到 method4 的所有抽象方法，然后子类继承 Base 类，一般可以直接复用 Base 类中的 method1 到 method4 方法，如果需要重写，直接重写该方法就好。这样就能省去所有子类实现所有抽象方法

继承抽象方法的基类 Base
public class Base extends AbstractClass {
    @Override
    protected void method1() {
        System.out.println(&quot;1&quot;);
    }

    @Override
    protected void method2() {
        System.out.println(&quot;2&quot;);
    }

    @Override
    protected void method3() {
        System.out.println(&quot;3&quot;);
    }

    @Override
    protected void method4() {
        System.out.println(&quot;4&quot;);
    }
}

子类 A 需要重写 method1 方法
public class SubA extends Base {

    &#47;&#47; 只需要重写 method1
    @Override
    public void method1() {
        System.out.println(&quot;重写 method1&quot;);
    }

    public static void main(String[] args) {
        Base A = new SubA();
        A.templateMethod1();
    }
}

输出结果为

重写 method1
2

</div>2020-03-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/40/6a/ab1cf396.jpg" width="30px"><span>小兵</span> 👍（18） 💬（3）<div>父类中不用抽象方法，提供一个空的实现，子类根据需要重写。</div>2020-03-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/62/bb/323a3133.jpg" width="30px"><span>下雨天</span> 👍（10） 💬（0）<div>课后思考：
一. 能修改框架代码情况：
定义一个父类，给不需要调用的抽象方法一个默认实现，子类继承该父类。

二. 如果可以修改框架代码的情况下：
1.templateMethod1与templateMethod2相关：可以将不需要调用的方法修改成protected并提供默认空实现。
2.templateMethod1与templateMethod2不相关：接口隔离原则，考虑将AbstractClass拆分成两个类分别定义两个方法。</div>2020-03-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/11/f5/039f003d.jpg" width="30px"><span>宁锟</span> 👍（6） 💬（1）<div>定义两个抽象类，继承模板类，分别给不需要的方法定义空实现</div>2020-03-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/67/d5/1b26b725.jpg" width="30px"><span>Gopher</span> 👍（5） 💬（0）<div>不会java 所以一下没看懂模版方法模式  看了其他资料才明白 所以记录一下

我们把装修房子这件事比做模版方法，装修房子的大流程事固定不变
把安装水电，收纳柜，电视墙这些细节比做可以被子类实现的抽象方法

我们可以通过重写安装水电，收纳柜，电视墙 这些方法来自定义我们的装修风格，但是不影响整体的装修流程</div>2020-10-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/cb/49/0b9ffc8e.jpg" width="30px"><span>刘大明</span> 👍（3） 💬（0）<div>如果其他的类不考虑复用的话，可以将这些抽取成一个基类，就是两个抽象类。分别给不需要的方法定义空实现。</div>2020-03-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/47/10/2d673601.jpg" width="30px"><span>好饿早知道送外卖了</span> 👍（2） 💬（3）<div>感觉模板模式和抽象类的实现方式和场景相同啊？
他俩有什么区别呢？求大佬们解惑</div>2020-04-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/b6/50/5d9ef58d.jpg" width="30px"><span>付昱霖</span> 👍（2） 💬（0）<div>使用外观模式，用一个新类再次包装，只暴露需要的接口。</div>2020-03-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/4c/6d/c20f2d5a.jpg" width="30px"><span>LJK</span> 👍（2） 💬（0）<div>课后作业的思考：对于必须要子类实现的方法定义为抽象方法或throw Exception，对于变动比较少但是同时也不想失去扩展性的方法添加默认实现，调用时优先获取用户自定义方法，获取不到的情况下使用默认方法</div>2020-03-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/30/50/c9/308f9fcf.jpg" width="30px"><span>Alascanfu</span> 👍（1） 💬（0）<div>课后问题：创建一个  IAdapter 的 Class
&#47;**
 * &lt;p&gt;
 * 适配器接口
 * &lt;&#47;p&gt;
 *
 * @author Fu JIAWEI
 * @since 2023&#47;8&#47;22 16:58
 **&#47;
public class IAdapter extends AbstractClass{
    @Override
    protected void method1() {
        System.out.println(1);
    }
    
    @Override
    protected void method2() {
    
    }
    
    @Override
    protected void method3() {
        throw new UnsupportedOperationException();
    }
    
    @Override
    protected void method4() {
        throw new UnsupportedOperationException();
    }
}
然后再对应具体业务写具体实现类，我觉得是这样子的，不知道对不对
&#47;**
 * &lt;p&gt;
 * 子类套用模板方法类1
 * &lt;&#47;p&gt;
 *
 * @author Fu JIAWEI
 * @since 2023&#47;8&#47;22 16:57
 **&#47;
public class ConcreteClass1 extends IAdapter{
    
    
    @Override
    protected void method4() {
        System.out.println(4);
    }
    
    public static void main(String[] args) {
        ConcreteClass1 concreteClass1 = new ConcreteClass1();
        
        concreteClass1.method1(); &#47;&#47; 可以重写也可以不重写的方法
        
        concreteClass1.method2(); &#47;&#47; 可以重写也可以不重写的方法
        
&#47;&#47;        concreteClass1.method3();&#47;&#47; 报错 Exception in thread &quot;main&quot; java.lang.UnsupportedOperationException
        
        concreteClass1.method4(); &#47;&#47; 有具体的实现 输出 4
    
        &#47;&#47; 输出 1 4 1 第一个 1 是不重写直接调用 method1 在适配器中的实现 ,
        &#47;&#47; 4 是 是具体业务重写的方法
        &#47;&#47; 第 2 个 1 是相当于模板方法调用 1 的适配器进行实现的
        &#47;&#47; 第 2 个 4 是相当于模板方法调用 4 的具体业务实现重写的方法 method4
        concreteClass1.templateMethod1();
    }
}
</div>2023-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7b/f7/21fb7574.jpg" width="30px"><span>朱刚</span> 👍（1） 💬（0）<div>模板方法中定义的抽象方法，意味着， 被调用时，此方法必须被实现，如果不被调用，子类就没必要去实现。所以 定义AdapterClass作为AbstractClass的直接功能子类，功能表现为 throw new UnsupportedOperationException();   业务子类继承 AdapterClass， 对要被调用的方法进行业务实现即可。</div>2023-03-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/a8/7a/f6185463.jpg" width="30px"><span>风疾aiq</span> 👍（1） 💬（0）<div>老师，能不能把你某些章节下面留的问题，做个答案分享啊。下面的留言区都是一些读者的理解，有些说的根本就不对。</div>2023-01-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4e/8d/34e0f6f3.jpg" width="30px"><span>江小田</span> 👍（1） 💬（0）<div>我以前这样写过，终于知道，原来这也是个模式</div>2022-08-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/5d/78/f011d586.jpg" width="30px"><span>遇见阳光</span> 👍（1） 💬（0）<div>缺省适配器模式可以解决该问题.</div>2022-07-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/0d/f2/3865fe28.jpg" width="30px"><span>李金鹏</span> 👍（1） 💬（0）<div>用组合代替继承</div>2021-07-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/52/32/bb570f48.jpg" width="30px"><span>向往的生活</span> 👍（1） 💬（2）<div>个人感觉这里的复用和扩展都是一回事呢。核心思想就是将不变和可变进行分离。</div>2020-07-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/7b/74/9b88e040.jpg" width="30px"><span>柏油</span> 👍（1） 💬（0）<div>可以提供一个adapter默认实现所有方法，子类重写需要的方法即可，比如Spring的InstantiationAwareBeanPostProcessorAdapter就是给所有方法提供默认实现，不过jkd1.8在接口中可以使用default默认实现，在InstantiationAwareaBeanPostProcessor接口中提供了默认实现，也就不需要在用Adapter 了</div>2020-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/a9/96/6d517a06.jpg" width="30px"><span>自来也</span> 👍（1） 💬（1）<div>Es框架里，abstractrunable是属于包装者还是模板。感觉更像包装者。不管啥了，总之觉得这样挺好用的。父类public就好了，就能解决没必要强制重写了。</div>2020-03-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8d/ed/ea2cbf3a.jpg" width="30px"><span>Sinclairs</span> 👍（1） 💬（0）<div>如果项目中多次用到这个类的话, 可以单独实现一个基类来继承这个模版类, 将不需要的扩展方法进行默认实现.
项目开发中直接使用基类方法就好.</div>2020-03-16</li><br/><li><img src="" width="30px"><span>冼莹莹</span> 👍（0） 💬（0）<div>想问一下使用模板模式时候，如果有的方法可以并行实现，那么templatemethod要怎么实现？.</div>2024-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/24/53/e9965fe1.jpg" width="30px"><span>丶诸葛</span> 👍（0） 💬（0）<div>Python中的unittest、Django、logging</div>2024-12-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/3a/96/e2/290b601b.jpg" width="30px"><span>活氵发</span> 👍（0） 💬（0）<div>两个思路：
1.剥离出两个接口定义，实现根据自己情况去实现对应的接口
2.抽象方法给出默认实现（空方法&#47;抛出unSupport异常）</div>2024-08-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/02/65/ddb6460e.jpg" width="30px"><span>柯里</span> 👍（0） 💬（0）<div>拆分，or默认实现，如果不行就是单存写个啥也干的子类</div>2023-11-22</li><br/>
</ul>