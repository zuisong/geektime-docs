你好，我是郭屹。

上节课，我们初步实现了一个MiniSpring框架，它很原始也很简单。我们实现了一个BeanFactory，作为一个容器对Bean进行管理，我们还定义了数据源接口Resource，可以将多种数据源注入Bean。

这节课，我们继续增强IoC容器，我们要做的主要有3点。

1. 增加单例Bean的接口定义，然后把所有的Bean默认为单例模式。
2. 预留事件监听的接口，方便后续进一步解耦代码逻辑。
3. 扩展BeanDefinition，添加一些属性，现在它只有id和class两个属性，我们要进一步地丰富它。

## 构建单例的Bean

首先我们来看看如何构建单例的Bean，并对该Bean进行管理。

单例（Singleton）是指某个类在整个系统内只有唯一的对象实例。只要能达到这个目的，采用什么技术手段都是可以的。常用的实现单例的方式有不下五种，因为我们构建单例的目的是深入理解Spring框架，所以我们会按照Spring的实现方式来做。

为了和Spring框架内的方法名保持一致，我们把BeanFactory接口中定义的registryBeanDefinition方法修改为registryBean，参数修改为beanName与obj。其中，obj为Object类，指代与beanName对应的Bean的信息。你可以看下修改后的BeanFactory。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/2e/1b/3c/9c5fc55f.jpg" width="30px"><span>姐姐</span> 👍（36） 💬（5）<div>这节课的类开始爆炸了，一开始看得很没头绪，但是俗话说“书读百遍，其义自见”，俗话很有道理，最后决定从simpleBeanFactory和ClassPathXmlApplicationContext两个角度，总结一下自己的理解和感悟，当做是自己的笔记：1. 从SimpleBeanFactory的角度看，首先理理三个接口BeanFactory、BeanDefinitionRegistry、SingletonBeanRegistry，对于这三个接口，其中BeanFactory、BeanDefinitionRegistry是由SimpleBeanFactory直接实现的，而对于SingletonBeanRegistry，SimpleBeanFactory继承了它的实现类DefaultSingletonBeanRegistry，起初我很疑惑，为什么SimpleBeanFactory不同时声明实现SingletonBeanRegistry并且继承它的默认实现类呢，但是后来想想也许SimpleBeanFactory对外只希望外界知道自己是一个beanFactory和beanDefinitionRegistry，至于singletonBeanRegistry，它只希望作为一种内部的能力来使用，所以继承一个已经实现的类来拥有能力，但是声明接口的时候不声明这个接口。理清了这三个以后，再来看看内部的细节逻辑，SimpleBeanFactory的registerBeanDefinition方法中每注册一个beanDefinition，如果不是懒加载的就立刻调用getBean，而getBean方法会从SimpleBeanFactory继承的DefaultSingletonBeanRegistry能力中判断bean是否存，不存在创建并注册进DefaultSingletonBeanRegistry。2.ClassPathXmlApplicationContext  它的组装逻辑和上一节一样，但是现在XmlBeanDefinitionReader在遍历resource向simplebeanfactory注册的时候，由于simplebeanfactory注册时候会创建非懒bean,所以现在applicationContext启动的时候就会创建所有非懒加载bean，上一节课的容器创建完并不会创建bean,要到获取bean的时候才创建bean，对getBean方法的调用提前到注册beanDefinition的时候了；ClassPathXmlApplicationContext实现了ApplicationEventPublisher，所以可以猜测以后容器不仅是容器，还兼具发布事件的功能。 这节课最大收获是加深了对实现接口和继承类的理解，如果一个类声明它实现了某个接口，那么它偏向于告诉外部它是那个接口，你可以把它当成那个接口来用，如果一个类继承了某个实现类，这时候也可以把它当成这个实现类来用，但是我想它更偏向于获得该实现类的能力，如果它既想获得能力又想对外提供能力，那么它可以同时声明实现接口和继承接口的某些实现类，再自己修改增强某些方法。</div>2023-03-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/12/b0/63f71163.jpg" width="30px"><span>咕噜咕噜</span> 👍（10） 💬（1）<div>构造器注入：适合于强制依赖，适合在创建对象的同时必须要初始化的变量。但是要注入的依赖多了可能构造器会相对臃肿；循环依赖问题无法有效解决，会在启动的时候报错。
setter注入：适合于可选依赖，当没有提供它们时，类应该能够正常工作。相对更加灵活，可以多次调用，循环依赖问题spring可以通过三级缓存解决。</div>2023-03-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/c0/df/d52e7244.jpg" width="30px"><span>聪聪不匆匆</span> 👍（8） 💬（2）<div>老师可以将每一章的各个类之间UML关系提供一下吗 方便学习缕清楚创建过程 和 各个组件依赖关系 谢谢老师</div>2023-03-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/85/ce/df1c7a91.jpg" width="30px"><span>陈小远</span> 👍（7） 💬（2）<div>这节课在内容上能看懂，但是在编码实操的时候有些难受——老师的源码都是完成品，而课件中并没有给出满足当前进度的可运行代码，一些迭代性的改动也并没有顾及会对其它部分实现的影响，比如BeanFactory中registerBean突然没有了，导致跟进课程实操方面有点打脑壳</div>2023-03-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2d/36/1c/adfeb6c4.jpg" width="30px"><span>爱学习的王呱呱</span> 👍（5） 💬（7）<div>老师好，有点没理解 synchronized + ConcurrentHashMap 同时使用的意义。
我理解HashMap在多线程下的问题有两个 1. 不同key但是相同hashcode会造成元素覆盖；2. 死循环。但是ConcurrentHashMap不存在这个问题了，为什么还需要synchronized呢。</div>2023-06-05</li><br/><li><img src="" width="30px"><span>Geek_e298ce</span> 👍（4） 💬（3）<div>有一个问题不太明白, 为什么要有BeanFactory和SingletonBeanRegistry这两个接口呢</div>2023-04-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/1e/58/2bfb3da0.jpg" width="30px"><span>故作</span> 👍（3） 💬（2）<div>感觉代码真的贴的不是很用心，看专栏里的代码，会觉得有些东西莫名其妙，以至于一头雾水，然后去看git上的代码，发现是没有这一看不懂的内容的。蛮气愤的，明明开篇词里说每一小步都是可运行的，结果，从这一章开始，就不行了。能理解无法把所有代码都放里边，但是，因为开篇词里的这句话，导致白白浪费了很多时间。这一章，质量真的很低，很不用心</div>2023-06-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/36/6f/4e/791d0f5e.jpg" width="30px"><span>浅行</span> 👍（3） 💬（1）<div>郭老师，有个地方不太理解，经过前面的一些设计，XmlBeanDefinitionReader构造方法不得不将BeanFactory改为实现类SimpleBeanFactory，这样可扩展性是否就变差了呢？如果实际开发中遇到这种情况有什么好的解决思路吗？请郭老师指点一下，谢谢</div>2023-03-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/b5/a4/67d6e3cb.jpg" width="30px"><span>__@Wong</span> 👍（2） 💬（1）<div>看了两节，这个课程对于缺少基础的人来说有一定的难度。本课程对学习者来说需要对Spring, 设计模式准则以及常用设计模式有一定的基础，并有一定代码设计功底。如果想要通过本课程学习企业Spring开发，不太建议，不如看Spring的书籍更来得有效。如果想要学习下Spring的设计，本课程非常适用。</div>2023-05-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/b1/d0/8c94d49e.jpg" width="30px"><span>未聞花名</span> 👍（2） 💬（1）<div>老师贴代码可以保留下包名，或者脑图里的类可以带上包名，这样可以按着思路写，不用去翻github的代码了</div>2023-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/c0/0c/f726d4d0.jpg" width="30px"><span>KernelStone</span> 👍（1） 💬（1）<div>我找到的一条主线是这样的。beans.xml -&gt; AServiceImpl -&gt; ArgumentValue &amp; PropertyValue -&gt; ArgumentValues &amp; PropertyValues -&gt; BeanDefinition -&gt; BeanDefinitionRegistry -&gt; XmlBeanDefinitionReader -&gt; BeanFactory -&gt; SingletonBeanRegistry -&gt; DefaultSingletonBeanRegistry -&gt; SimpleBeanFactory。主要还是围绕着扩充Bean定义，属性注入去完成的，这个顺序看下来比较好理解。其余的就是ApplicationEvent +ApplicationEventPublisher预留事件监听机制的扩展点、和重新组装ClassPathXmlApplicationContext。

当然同学们评论很精彩，学到了一些代码细节。再次感谢。

</div>2023-05-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/36/b9/a1/cf741eca.jpg" width="30px"><span>Fiftten2001</span> 👍（1） 💬（1）<div>更改一下我的问题，singleton = Class.forName(beanDefinition.getClassName()).newInstance();这行代码在多线程情况下还是会生成多个对象的吧，这样的话单例是指单例了什么，如果是说get的时候每次都拿到的是同一个singleton，synchronized和concurrent保证了不会在多线程情况下，put或者remove发生导致的运行时崩溃，但是前后两次访问返回的singleton可能并不是同一个吧，这时候是不是应该在synchronized代码块中再次判断是否已经有了beanName对应的singletonObject然后再执行put和add</div>2023-04-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/36/b9/a1/cf741eca.jpg" width="30px"><span>Fiftten2001</span> 👍（1） 💬（2）<div>疑惑的是上一讲中，Bean实例本就是注册进hashMap的，即BeanFactory的singletons中本就由beanDefinition的id和classpath构成key和value，无论加不加synchronized不都是只有一个么...（菜鸡大学生，如果问题太蠢，请轻点嘲笑，望解惑）</div>2023-04-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/be/31/791d0f5e.jpg" width="30px"><span>瓜瓜王几</span> 👍（1） 💬（1）<div>第二章代码看了3天，终于这一波算是看懂理解了，DefaultSingletonBeanRegistry将第一章中SimpleBeanFactory里面保存的singletons拆分出来管理了，用于存储真正的Bean对象(beanName,Object)，SimpleBeanFactory仅保存createBean，containsBean等和Bean操作相关的内容，其余相比第一章就是多了setter注入和构造器注入的内容，老师的代码并不复杂，自己还是要多多努力，认真看还是能看懂滴~~~开心.jpg</div>2023-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/36/6f/4e/791d0f5e.jpg" width="30px"><span>浅行</span> 👍（1） 💬（2）<div>发现了个小问题，配置构造器注入章节下：
与 Setter 注入类似，我们只是把标签换成了标签
这里好像少了点什么</div>2023-03-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/9e/3f/00109670.jpg" width="30px"><span>且将新火试新茶～</span> 👍（0） 💬（1）<div>确实在敲代码过层中遇到了很多阻塞点，要结合作者的代码来看，另外按照作者的步骤来敲，最好是一段就运行一下，缩小问题范围，保证程序能正常运行。不然最后敲完完全没有头绪，不知道从哪里去排查。</div>2024-03-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/9e/3f/00109670.jpg" width="30px"><span>且将新火试新茶～</span> 👍（0） 💬（1）<div>这节主要是：
1. 新增了单例模式。registerBeanDefinition 这个方法把实例放入beanDefinitionMap中，第一次get是从这个map中拿出来的，然后放入单例的map中进行管理了。个人理解SingletonBeanRegistry只是帮我们管理单例的仓库，初始化的时候这个里面是没有值的，感觉它类似于一个缓存
2.BeanDefinition的类属性做了扩展
3. 为构造方法和setter注入属性做了一些准备工作

这节代码敲完之后，应该保证：
1. 程序能正常启动
2.aService.sayHello(); 方法调用结果是null,null</div>2024-03-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/5e/3b/845fb641.jpg" width="30px"><span>jhren</span> 👍（0） 💬（1）<div>仔细研究了下，Bean的property是没有type的，通过setter的参数推断出类型。
这段代码没有type跟Spring是一致的。
public class PropertyValue {
    private final String name;
    private final Object value;
}
XML里面的type在Spring里是不合法的
&lt;beans&gt;
    &lt;bean id=&quot;aservice&quot; class=&quot;com.minis.test.AServiceImpl&quot;&gt;
        &lt;property type=&quot;String&quot; name=&quot;property1&quot; value=&quot;Hello World!&quot;&#47;&gt;
    &lt;&#47;bean&gt;
&lt;&#47;beans&gt;</div>2024-03-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/6c/a3/7d60e2a0.jpg" width="30px"><span>1184507801</span> 👍（0） 💬（1）<div>老师源码地址进不了</div>2024-01-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/04/7f/c4ce690c.jpg" width="30px"><span>我想我是海</span> 👍（0） 💬（1）<div>老师你好我有一个疑问，此时的DefaultSingletonBeanRegistry中不是有 beanNames 来存储所有bean的名称了吗？ 它被SimpleBeanFactory继承了。 但这节的代码中 SimpleBeanFactory 又自己声明了一个 beanDefinitionNames 也是来存放bean的所有的名称的。 这两个是继承关系，这属性列表功能不重复了吗？</div>2023-05-23</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJhxtIyXX4icMNAq5zEvchKYS3q7fwZXA3h7yV80iaibCRXniaLW95OnPC8PM2h5Ja5ibpkJ1VJowicqKZA/132" width="30px"><span>Geek_7jwpfc</span> 👍（0） 💬（1）<div>看了这节课的代码，设计的构造器和property注入，是不是只设计基本类型，后续会有改动！</div>2023-05-15</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJhxtIyXX4icMNAq5zEvchKYS3q7fwZXA3h7yV80iaibCRXniaLW95OnPC8PM2h5Ja5ibpkJ1VJowicqKZA/132" width="30px"><span>Geek_7jwpfc</span> 👍（0） 💬（1）<div>文稿中ArgumentValues和github上面的不一致，我到底应该相信谁的</div>2023-05-12</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJhxtIyXX4icMNAq5zEvchKYS3q7fwZXA3h7yV80iaibCRXniaLW95OnPC8PM2h5Ja5ibpkJ1VJowicqKZA/132" width="30px"><span>Geek_7jwpfc</span> 👍（0） 💬（1）<div>ArgumentValue有两个构造器，第一个是#ArgumentValue(Object value, String type)，第二个是#ArgumentValue(Object value, String type, String name)，name字段不是必须的？</div>2023-05-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a0/cb/aab3b3e7.jpg" width="30px"><span>张三丰</span> 👍（0） 💬（1）<div>老师请教个问题，
其实SimpleBeanFactory完全没必要告诉外界它也是BeanDefinitionRegistry“仓库”，也就是没必要实现这个接口，它应该告诉外界它就只是一个BeanFactory“工厂”就足够了，然后再将BeanDefinitionRegistry作为SimpleBeanFactory中的一个属性，利用组合关系，放弃继承关系，这样从结构上更容易让人接受，纯属个人理解。</div>2023-04-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/2c/68/c299bc71.jpg" width="30px"><span>天敌</span> 👍（0） 💬（1）<div>Arguments#addArgumentValue(Integer key,ArgumentValue newValue) 这个方法是私有方法但是现在没有地方调用吗？</div>2023-04-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/4b/29/9e5d963b.jpg" width="30px"><span>哇!猪!!</span> 👍（0） 💬（2）<div>public Class getType(String name) { return this.beanDefinitionMap.get(name).getClass(); }这里貌似写错了？应该是 public Class&lt;?&gt; getType(String name) {
        return (Class&lt;?&gt;) this.beanDefinitionMap.get(name).getBeanClass();
    }</div>2023-03-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2e/1b/3c/9c5fc55f.jpg" width="30px"><span>姐姐</span> 👍（0） 💬（1）<div>感谢老师，这个课太用心了，展现了spring从一颗种子成长为大树的过程，才看了两节，已经感觉收获颇多，会继续追下去。</div>2023-03-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/41/4d/f6d6d13a.jpg" width="30px"><span>啊良梓是我</span> 👍（0） 💬（1）<div>public boolean isSingleton(String beanName) {
        return beanDefinitionMap.get(beanName).isSingleton();
    } 
这里好像BeanDefinition 没有定义这个isSingleton()方法吧？哪来的</div>2023-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/92/6d/becd841a.jpg" width="30px"><span>escray</span> 👍（0） 💬（1）<div>继续闷头抄代码，不明觉厉。

https:&#47;&#47;github.com&#47;escray&#47;miniSpring&#47;tree&#47;IoC02

对于思考题，构造器注入是不是相对更死板一些，而 Setter 注入更灵活，可以从配置文件读取。

看到留言里面大家都在纠结 beanNames 和 singletons 的重叠，一方面是实现风格，另外我觉得，提供 beanNames 的情况下是不是可以做到更好的性能？特别是在与只需要判断名字的时候，感觉上 singletons 有可能会变的比较庞大。

另外就是关于代码的 UML 图，在 IDEA 里面可以直接生成项目的 UML 图，虽然不怎么美观，但是该有的要素都是有的。</div>2023-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/21/18/dde59ef9.jpg" width="30px"><span>李小江</span> 👍（0） 💬（1）<div>ArgumentValues中addArgumentValue方法为什么是私有的，也没有调用到。是后面会用到的还是什么设计</div>2023-03-16</li><br/>
</ul>