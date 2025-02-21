在企业应用软件开发中，Java是毫无争议的主流语言，开放的Java EE规范和强大的开源框架功不可没，其中Spring毫无疑问已经成为企业软件开发的事实标准之一。今天这一讲，我将补充Spring相关的典型面试问题，并谈谈其部分设计细节。

今天我要问你的问题是，谈谈Spring Bean的生命周期和作用域？

## 典型回答

Spring Bean生命周期比较复杂，可以分为创建和销毁两个过程。

首先，创建Bean会经过一系列的步骤，主要包括：

- 实例化Bean对象。
- 设置Bean属性。
- 如果我们通过各种Aware接口声明了依赖关系，则会注入Bean对容器基础设施层面的依赖。具体包括BeanNameAware、BeanFactoryAware和ApplicationContextAware，分别会注入Bean ID、Bean Factory或者ApplicationContext。
- 调用BeanPostProcessor的前置初始化方法postProcessBeforeInitialization。
- 如果实现了InitializingBean接口，则会调用afterPropertiesSet方法。
- 调用Bean自身定义的init方法。
- 调用BeanPostProcessor的后置初始化方法postProcessAfterInitialization。
- 创建过程完毕。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/9e/eb/f68665b6.jpg" width="30px"><span>caoxile</span> 👍（77） 💬（5）<div>@代码狂徒
感觉本篇文章跑题了呢，关于生命周期，只讨论了初始化过程和销毁过程，那么什么时候引发的初始化呢？什么时候触发销毁操作呢？spring容器管理的bean是在容器运行过程中不会被销毁吧？

我来讲讲吧:
首先理解scope:
1. Singleton(单例) 在整个应用中,只创建bean的一个实例
2. Propotype(原型) 每次注入或者通过Spring应用上下文获取的时候,都会创建一个新
的bean实例。
3. Session(会话) 在Web应用中,为每个会话创建一个bean实例。
4. Request(请求) 在Web应用中,为每个请求创建一个bean实例。

他们是什么时候创建的:
1一个单例的bean,而且lazy-init属性为false(默认),在Application Context创建的时候构造
2一个单例的bean,lazy-init属性设置为true,那么,它在第一次需要的时候被构造.
3 其他scope的bean,都是在第一次需要使用的时候创建

他们是什么时候销毁的:
1 单例的bean始终 存在与application context中, 只有当 application 终结的时候,才会销毁
2 和其他scope相比,Spring并没有管理prototype实例完整的生命周期,在实例化,配置,组装对象交给应用后,spring不再管理.只要bean本身不持有对另一个资源（如数据库连接或会话对象）的引用，只要删除了对该对象的所有引用或对象超出范围，就会立即收集垃圾.
3 Request: 每次客户端请求都会创建一个新的bean实例,一旦这个请求结束,实例就会离开scope,被垃圾回收.
4 Session: 如果用户结束了他的会话,那么这个bean实例会被GC.</div>2019-01-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/25/e0/a9b2123c.jpg" width="30px"><span>yao_jn</span> 👍（14） 💬（1）<div>读老师的文章收益很大，希望老师再对框架多讲一些，还有底层原理，毕竟很多时候看源码很费力，提点下会好很多！</div>2018-08-02</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaELZPnUAiajaR5C25EDLWeJURggyiaOP5GGPe2qlwpQcm5e3ybib8OsP4tvddFDLVRSNNGL5I3SFPJHsA/132" width="30px"><span>null</span> 👍（12） 💬（1）<div>老师，IOC 为什么可以实现解耦吖？

在引入 IOC 容器之前，对象 A 依赖于对象 B，则需要 A 主动去创建对象 B，控制权都在 A。

在引入 IOC 容器之后，当对象 A 运行到需要对象 B 的时候，IOC 容器会主动创建一个对象 B 注入到对象 A，控制权在容器。

控制权发生了反转，为什么能降价系统耦合，或者说降低什么之间的耦合？（自己的理解：应该不是降低对象间的耦合，因为不管由 A 还是容器创建 B 对象，A 都是耦合 B 的。感觉自己理解的方向偏了。）

谢谢！

</div>2018-08-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d2/31/f1bec7fc.jpg" width="30px"><span>汉斯·冯·拉特</span> 👍（6） 💬（1）<div>想不到博主对spring也有深入了解。声明式事务是通过beanPostProcessor来实现的，springioc会用beanPostProcessor的某个方法（具体方法名忘记了，这里假设为方法A）返回结果作为getBean的结果。所以spring的事务模块在方法A中，用代理的方式，在目标方法前后加入一些与事务有关的代码，方法A的返回值就是这个代理类。欢迎拍砖！</div>2018-08-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e5/09/ddabec76.jpg" width="30px"><span>李峰</span> 👍（5） 💬（1）<div>能否分享下你看spring源码的技巧，和方法，我也读了一些其他的源码，感觉spring太全复杂度就很高，看着看着就迷失了</div>2018-08-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/22/89/5757eb43.jpg" width="30px"><span>XiaoYeGe</span> 👍（4） 💬（1）<div>第一次写留言, 看了几个月了,中间有些篇幅关于JVM的介绍,建议去看&lt;&lt;深入理解Java虚拟机&gt;&gt;这本书, 讲的不错, 当然博主总结的也好. 总之, 谢谢博主</div>2018-11-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/8b/b3/c340227c.jpg" width="30px"><span>GL</span> 👍（3） 💬（1）<div>漏了BeanFactoryPostProcessor，在BeanPostProcessor前执行</div>2018-08-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e5/09/ddabec76.jpg" width="30px"><span>李峰</span> 👍（1） 💬（1）<div>老师，请教下，因为我也读了几次spring的源码，相比其他我读过的源码个人觉得spring复杂度很复杂，很多细节看着看着就迷失在他的代码里面了能否分享下你看spring源码的方法，感谢</div>2018-08-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/b7/d4/abb7bfe3.jpg" width="30px"><span>代码狂徒</span> 👍（152） 💬（4）<div>感觉本篇文章跑题了呢，关于生命周期，只讨论了初始化过程和销毁过程，那么什么时候引发的初始化呢？什么时候触发销毁操作呢？spring容器管理的bean是在容器运行过程中不会被销毁吧？</div>2018-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/03/84/791fb8f1.jpg" width="30px"><span>Meteor</span> 👍（44） 💬（0）<div>Spring容器初始化开始:
1.[BeanFactoryPostProcessor]接口实现类的构造器2.[BeanFactoryPostProcessor]的postProcessorBeanFactory方法
3.[BeanPostProcessor]接口实现类的构造器
4.[InstantiationAwareBeanPostProcessorAdapter]构造器
5.[InstantiationAwareBeanPostProcessorAdapter]的postProcessBeforeInstantiation方法(从这里开始初始化bean)
6.[Bean]的构造器
7.[InstantiationAwareBeanPostProcessorAdapter]的postProcessAfterInstantiation
8.[InstantiationAwareBeanPostProcessorAdapter]的postProcessPropertyValues方法
9.[Bean]属性注入，setter方
方法
10.[Bean]如果实现了各种XXXaware接口，依次调用各个setXXX(如BeanNameAware.setBeanName(),BeanFactoryAware.setBeanFactory())
11.[BeanPostProcessor]的postProcessBeforeInitialization方法
12.[InstantiationAwareBeanPostProcessorAdapter]的postProcessBeforeInitialization方法
13.[Bean]自定义的init-method
14.[Bean]如果实现了InitializingBean接口，此时会调用它的afterPropertiesSet方法
15.[BeanPostProcessor]的postProcessAfterInitialization方法(此时bean初始化完成)
16.[InstantiationAwareBeanPostProcessorAdapter]的postProcessInitialization方法(到这里容器初始化完成)
17.业务逻辑bean的使用

Bean的销毁过程:
1.[DisposableBean]的destory方法
2.[Bean]自定义的destory-method方法

说明:如果有多个bean需要初始化，会循环执行5--15。

重要说明:欢迎拍砖，欢迎拍，欢迎，欢，……</div>2018-08-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/11/93/8b41390b.jpg" width="30px"><span>虞飞</span> 👍（31） 💬（1）<div>声明式事务其实说白了是一种特殊的aop应用，它其实包括两种advice，一种是around，另外一种是after-throwing。利用around advice在方法执行前，先关闭数据库的自动提交功能，然后设定一个标志符。根据业务代码实际的情况，对标志符赋不同的值，如果数据更新成功赋true，否则false。在业务方法执行完之后的部分对标志符进行处理。如为true，则提交数据库操作，否则就进行回滚。
另外还会使用after-throwing，对出错的信息进行记录。然后再将错误抛出至上层。</div>2018-08-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/59/c9/f44cb7f3.jpg" width="30px"><span>爪哇夜未眠</span> 👍（19） 💬（2）<div>Advice 的时序图的before,after画反了吗</div>2018-08-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/6b/27/b56f524c.jpg" width="30px"><span>拟梦</span> 👍（14） 💬（0）<div>讲springbean的生命周期，不介绍spring后置处理器的文章都是没有灵魂的</div>2019-06-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/b5/26/d635d8d3.jpg" width="30px"><span>铁拳阿牛</span> 👍（9） 💬（0）<div>可以按照课程丢些demo到一个github项目里，配合章节理论，这样有理论有代码可能对课程，和对学员更有帮助！不过对老师的成本也提高了。</div>2018-08-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/70/12/aa74da82.jpg" width="30px"><span>arebya</span> 👍（6） 💬（1）<div>加上jdk本身的@PostConstruct 和@PreDestroy分析整个生命周期会更好</div>2018-12-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7a/03/c9b43b21.jpg" width="30px"><span>BewhY</span> 👍（4） 💬（0）<div>我来替作者回答下下面提出的问题吧
什么时候引发初始化呢？初始化就是项目启动时就开始初始化了，将xml配置信息解析成BeanDefanition，存放在IOC容器中(所谓IOC容器就是一个Map集合)，上面老师讲的是Bean创建阶段了，不是Bean的初始化阶段。
不管是单例Bean还是原型Bean，都会被解析成BeanDefanition存放在IOC容器中，只不过Spring不处理原型Bean的循环依赖</div>2019-09-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/16/20/77d41677.jpg" width="30px"><span>皓月冷千山</span> 👍（3） 💬（0）<div>首先理解scope:
1. Singleton(单例) 在整个应用中,只创建bean的一个实例
2. Propotype(原型) 每次注入或者通过Spring应用上下文获取的时候,都会创建一个新
的bean实例。
3. Session(会话) 在Web应用中,为每个会话创建一个bean实例。
4. Request(请求) 在Web应用中,为每个请求创建一个bean实例。

他们是什么时候创建的:
1一个单例的bean,而且lazy-init属性为false(默认),在Application Context创建的时候构造
2一个单例的bean,lazy-init属性设置为true,那么,它在第一次需要的时候被构造.
3 其他scope的bean,都是在第一次需要使用的时候创建

他们是什么时候销毁的:
1 单例的bean始终 存在与application context中, 只有当 application 终结的时候,才会销毁
2 和其他scope相比,Spring并没有管理prototype实例完整的生命周期,在实例化,配置,组装对象交给应用后,spring不再管理.只要bean本身不持有对另一个资源（如数据库连接或会话对象）的引用，只要删除了对该对象的所有引用或对象超出范围，就会立即收集垃圾.
3 Request: 每次客户端请求都会创建一个新的bean实例,一旦这个请求结束,实例就会离开scope,被垃圾回收.
4 Session: 如果用户结束了他的会话,那么这个bean实例会被GC.</div>2020-11-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d5/41/99b90510.jpg" width="30px"><span>孟老师</span> 👍（2） 💬（0）<div>一直没明白为什么spring和springMVC有父子容器的关系？这么设计的目的是什么？求老师解答</div>2018-11-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/12/6e/3a0b4930.jpg" width="30px"><span>FiRerOUNd</span> 👍（1） 💬（0）<div>泛泛而谈谁都会，细微之处见真章。</div>2022-06-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/61/90/de8c61a0.jpg" width="30px"><span>dongge</span> 👍（1） 💬（0）<div>接下来，我们再来看依赖注入。依赖注入跟控制反转恰恰相反，它是一种具体的编码技巧。依赖注入的英文翻译是 Dependency Injection，缩写为 DI。对于这个概念，有一个非常形象的说法，那就是：依赖注入是一个标价 25 美元，实际上只值 5 美分的概念。也就是说，这个概念听起来很“高大上”，实际上，理解、应用起来非常简单。 这是 https:&#47;&#47;time.geekbang.org&#47;column&#47;article&#47;177444 设计模式课程说法。这节课是是不是把 IOC 和 DI 搞错了</div>2020-07-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b1/81/ae0277f1.jpg" width="30px"><span>白</span> 👍（1） 💬（0）<div>拜读第二遍。</div>2018-09-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/42/4f/ff1ac464.jpg" width="30px"><span>又双叒叕是一年啊</span> 👍（1） 💬（0）<div>这么给力多讲了老师一共多少讲啊</div>2018-08-07</li><br/><li><img src="" width="30px"><span>sars</span> 👍（1） 💬（0）<div>能否介绍一下热加载，还有目前第三方软件，class，jar都可以热加载。</div>2018-08-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/b1/67/1d3c2f25.jpg" width="30px"><span>青玄</span> 👍（0） 💬（0）<div>根据实验 Bean 自身定义的 init 方法在 after PropertiesSet方法之前被调用</div>2022-11-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/2e/92/e1c38ca6.jpg" width="30px"><span>KamTo  Hung</span> 👍（0） 💬（0）<div>主要分为三个阶段讲:创建实例，属性注入，初始化Bean（都在AbstractAutowiredcapableBeanFactory的doCreateBen方法上）。</div>2021-04-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/a0/f4/7e122a67.jpg" width="30px"><span>之渊</span> 👍（0） 💬（0）<div>spring aop 可以查看这篇博客https:&#47;&#47;blog.csdn.net&#47;qq_32331073&#47;article&#47;details&#47;80596084
对advice的执行顺序总结得很好，还有图</div>2020-08-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/ba/ec/2b1c6afc.jpg" width="30px"><span>李飞</span> 👍（0） 💬（0）<div>二刷，深入理解</div>2020-07-15</li><br/><li><img src="" width="30px"><span>地表十进制</span> 👍（0） 💬（0）<div>spring security也是比较重要的，比较不好弄明白的一个模块</div>2020-04-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/90/e9/87f2956a.jpg" width="30px"><span>hi兵哥</span> 👍（0） 💬（0）<div>请教老师一个实际使用中的问题解决方案，多个jar包中有相同路径的相同class,如何让jvm加载制定包下的class?springcloud中有时引入了多个依赖，譬如引入的包使用@bean 生成了 restTemplate，而我自己项目中同样有要生restTemplate的需求，两个处理逻辑有区别，而我想基于robbin去实现负载均衡。基于上面我大致知道可以通过类加载，classScan方式去做一些处理，请问老师能否给出一些具体的可操作的解决方案，谢谢。</div>2019-10-26</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKYfReHXMbPaxO890ib9GvY9iciclPIUvaAYMYON4scP7ElXCPVzicghF0SH5HN2LqibYOrdrppC7DuSpw/132" width="30px"><span>static</span> 👍（0） 💬（1）<div>老师好，在学习spring的过程中我遇到了一个ioc的一个疑问，刚好看到老师这篇文章又想起之前没有解决的疑惑，希望老师可以帮我解惑，感谢！背景：在ioc容器refresh方法的末尾会初始化所有单例bean，之后会在实例化bean之前先寻找bean的所有依赖bean并循环对依赖的bean调用getBean方法。问题：如果此时依赖的bean是原型的作用域，是否此时的getBean此原型bean是没有用浪费时间的一个过程呢？在我目前的理解感觉如果bean是单例才会将实例存放在ioc容器中，如果是原型就不会存下来，因为我一直找不到原型bean存放在哪里，所以对这个过程产生疑惑，觉得这样轮询依赖bean的过程如果bean为原型是在浪费时间去getBean。感谢老师抽空看完！</div>2018-11-23</li><br/>
</ul>