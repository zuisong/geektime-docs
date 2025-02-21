你好，我是朱晔。今天，我们来聊聊Spring框架中的IoC和AOP，及其容易出错的地方。

熟悉Java的同学都知道，Spring的家族庞大，常用的模块就有Spring Data、Spring Security、Spring Boot、Spring Cloud等。其实呢，Spring体系虽然庞大，但都是围绕Spring Core展开的，而Spring Core中最核心的就是IoC（控制反转）和AOP（面向切面编程）。

概括地说，IoC和AOP的初衷是解耦和扩展。理解这两个核心技术，就可以让你的代码变得更灵活、可随时替换，以及业务组件间更解耦。在接下来的两讲中，我会与你深入剖析几个案例，带你绕过业务中通过Spring实现IoC和AOP相关的坑。

为了便于理解这两讲中的案例，我们先回顾下IoC和AOP的基础知识。

IoC，其实就是一种设计思想。使用Spring来实现IoC，意味着将你设计好的对象交给Spring容器控制，而不是直接在对象内部控制。那，为什么要让容器来管理对象呢？或许你能想到的是，使用IoC方便、可以实现解耦。但在我看来，相比于这两个原因，更重要的是IoC带来了更多的可能性。

如果以容器为依托来管理所有的框架、业务对象，我们不仅可以无侵入地调整对象的关系，还可以无侵入地随时调整对象的属性，甚至是实现对象的替换。这就使得框架开发者在程序背后实现一些扩展不再是问题，带来的可能性是无限的。比如我们要监控的对象如果是Bean，实现就会非常简单。所以，这套容器体系，不仅被Spring Core和Spring Boot大量依赖，还实现了一些外部框架和Spring的无缝整合。
<div><strong>精选留言（23）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/13/26/38/ef063dc2.jpg" width="30px"><span>Darren</span> 👍（107） 💬（7）<div>一、注解区别
@Autowired
	1、@Autowired是spring自带的注解，通过‘AutowiredAnnotationBeanPostProcessor’ 类实现的依赖注入；
	2、@Autowired是根据类型进行自动装配的，如果需要按名称进行装配，则需要配合@Qualifier；
	3、@Autowired有个属性为required，可以配置为false，如果配置为false之后，当没有找到相应bean的时候，系统不会抛错；
	4、@Autowired可以作用在变量、setter方法、构造函数上。

@Inject
	1、@Inject是JSR330 (Dependency Injection for Java)中的规范，需要导入javax.inject.Inject;实现注入。
	2、@Inject是根据类型进行自动装配的，如果需要按名称进行装配，则需要配合@Named；
	3、@Inject可以作用在变量、setter方法、构造函数上。

@Resource
	1、@Resource是JSR250规范的实现，需要导入javax.annotation实现注入。
	2、@Resource是根据名称进行自动装配的，一般会指定一个name属性
	3、@Resource可以作用在变量、setter方法上。

总结：
1、@Autowired是spring自带的，@Inject是JSR330规范实现的，@Resource是JSR250规范实现的，需要导入不同的包
2、@Autowired、@Inject用法基本一样，不同的是@Autowired有一个request属性
3、@Autowired、@Inject是默认按照类型匹配的，@Resource是按照名称匹配的
4、@Autowired如果需要按照名称匹配需要和@Qualifier一起使用，@Inject和@Name一起使用


二：循环依赖：
直观解决方法时通过set方法去处理，背后的原理其实是缓存。
主要解决方式：使用三级缓存
singletonObjects： 一级缓存， Cache of singleton objects: bean name --&gt; bean instance
earlySingletonObjects： 二级缓存， Cache of early singleton objects: bean name --&gt; bean instance  提前曝光的BEAN缓存
singletonFactories： 三级缓存， Cache of singleton factories: bean name --&gt; ObjectFactory</div>2020-04-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/87/4b/7f90f912.jpg" width="30px"><span>norman</span> 👍（8） 💬（1）<div>@Resource 和 @Autowired @Inject 三者区别：
1 @Resource默认是按照名称来装配注入的，只有当找不到与名称匹配的bean才会按照类型来装配注入。
2 @Autowired默认是按照类型装配注入的，如果想按照名称来转配注入，则需要结合@Qualifier。这个注释是Spring特有的。
3 @Inject是根据类型进行自动装配的，如果需要按名称进行装配，则需要配合@Named</div>2020-04-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/69/65/eb778125.jpg" width="30px"><span>左琪</span> 👍（7） 💬（1）<div>这里的代理类不是单例么，还是说会在增强逻辑里不断创建被代理类？</div>2020-04-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/10/bb/f1061601.jpg" width="30px"><span>Demon.Lee</span> 👍（4） 💬（1）<div>连接点: 程序执行过程中能够应用通知的所有点；通知（增强）: 即切面的工作，定义了What以及When；切点定义了Where，通知被应用的具体位置（哪些连接点）
----Spring实战（第4版）</div>2020-04-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9d/9a/7f064a9f.jpg" width="30px"><span>龙行秀</span> 👍（3） 💬（3）<div>“架构师一开始定义了这么一个 SayService 抽象类，其中维护了一个类型是 ArrayList 的字段 data，用于保存方法处理的中间数据。每次调用 say 方法都会往 data 加入新数据，可以认为 SayService 是有状态，如果 SayService 是单例的话必然会 OOM”
-----为什么单例就会OOM，多例就不会呢？没看懂</div>2020-09-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a5/f0/8648c464.jpg" width="30px"><span>Joker</span> 👍（3） 💬（1）<div>老师，请教一下，那个sayservice里的data有啥用，那个单例是为了一种重复使用data对吧，那换成每次都生成一个新的bean，那个data还有效果吗。。</div>2020-04-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ce/92/f53c41ee.jpg" width="30px"><span>小学生</span> 👍（1） 💬（3）<div>老师，您好，您讲 的切面执行顺序好像不对啊，我的执行顺序和你说的不一致！
[10:34:11.367] [http-nio-45678-exec-4] [INFO ] [o.g.t.c.s.a.TestAspectWithOrder10:31  ] - TestAspectWithOrder10 @Around before
[10:34:11.377] [http-nio-45678-exec-4] [INFO ] [o.g.t.c.s.a.TestAspectWithOrder10:21  ] - TestAspectWithOrder10 @Before
[10:34:11.377] [http-nio-45678-exec-4] [INFO ] [o.g.t.c.s.a.TestAspectWithOrder20:31  ] - TestAspectWithOrder20 @Around before
[10:34:11.378] [http-nio-45678-exec-4] [INFO ] [o.g.t.c.s.a.TestAspectWithOrder20:21  ] - TestAspectWithOrder20 @Before
[10:34:11.379] [http-nio-45678-exec-4] [INFO ] [o.g.t.c.s.aopmetrics.MetricsAspect:79  ] - 【入参日志】调用 【class org.geekbang.time.commonmistakes.springpart1.aopmetrics.TestController】【public void org.geekbang.time.commonmistakes.springpart1.aopmetrics.TestController.test()】【http:&#47;&#47;localhost:45678&#47;test】 的参数是：【[]】
[10:34:11.379] [http-nio-45678-exec-4] [INFO ] [o.g.t.c.s.aopmetrics.MetricsAspect:88  ] - 【成功打点】调用 【class org.geekbang.time.commonmistakes.springpart1.aopmetrics.TestController】【public void org.geekbang.time.commonmistakes.springpart1.aopmetrics.TestController.test()】【http:&#47;&#47;localhost:45678&#47;test】 成功，耗时：0 ms
[10:34:11.379] [http-nio-45678-exec-4] [INFO ] [o.g.t.c.s.aopmetrics.MetricsAspect:107 ] - 【出参日志】调用 【class org.geekbang.time.commonmistakes.springpart1.aopmetrics.TestController】【public void org.geekbang.time.commonmistakes.springpart1.aopmetrics.TestController.test()】【http:&#47;&#47;localhost:45678&#47;test】 的返回是：【null】
[10:34:11.380] [http-nio-45678-exec-4] [INFO ] [o.g.t.c.s.a.TestAspectWithOrder20:26  ] - TestAspectWithOrder20 @After
[10:34:11.380] [http-nio-45678-exec-4] [INFO ] [o.g.t.c.s.a.TestAspectWithOrder20:33  ] - TestAspectWithOrder20 @Around after
[10:34:11.380] [http-nio-45678-exec-4] [INFO ] [o.g.t.c.s.a.TestAspectWithOrder10:26  ] - TestAspectWithOrder10 @After
[10:34:11.380] [http-nio-45678-exec-4] [INFO ] [o.g.t.c.s.a.TestAspectWithOrder10:33  ] - TestAspectWithOrder10 @Around after
</div>2020-10-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/9a/28/03613c22.jpg" width="30px"><span>track6688</span> 👍（1） 💬（1）<div>老师，请教一个问题，我使用这个注解，@Order(Ordered.HIGHEST_PRECEDENCE)，使用@AfterThrowing这个时，报No MethodInvocation found: Check that an AOP invocation is in progress, and that the ExposeInvocationInterceptor is upfront in the interceptor chain. Specifically, note that advices with order HIGHEST_PRECEDENCE will execute before ExposeInvocationInterceptor!，怎么处理呢？</div>2020-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/bd/da/3d76ea74.jpg" width="30px"><span>看不到de颜色</span> 👍（1） 💬（1）<div>感觉Spring Intercepter的执行顺序和Servlet Filter的执行过程是一样的，一个递归调用栈。
有个疑问想请老师解答一下。采用创建内部类的方式获取默认注解配置，这样不会每调用一次就会在元空间中生成一个c的Class信息吗？</div>2020-05-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/88/70/32534e2d.jpg" width="30px"><span>David Mo</span> 👍（1） 💬（1）<div>@sevice 的坑踩过，代理类一开始不行白，后来说动态创建就懂了。当时是用一个类似工厂类解决的</div>2020-04-30</li><br/><li><img src="" width="30px"><span>Geek_3b1096</span> 👍（1） 💬（1）<div>很有收获谢谢老师</div>2020-04-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/1a/d8/9ae1bdb9.jpg" width="30px"><span>Husiun</span> 👍（17） 💬（0）<div>问题2，循环依赖会抛出异常BeanCurrentlyInCreationException，官网的解决方案是由构造器注入改为setter注入</div>2020-04-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/5e/2b/1c158008.jpg" width="30px"><span>和海明威下棋</span> 👍（8） 💬（0）<div>&#47;&#47;@annotation指示器实现对标记了Metrics注解的方法进行匹配
   @Pointcut(&quot;within(@org.geekbang.time.commonmistakes.springpart1.aopmetrics.Metrics *)&quot;

这里是不是有笔误？我试了下within无法拦截方法的注解，换成@annotation就可以了</div>2020-11-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b3/92/6a20da3f.jpg" width="30px"><span>OneDy</span> 👍（7） 💬（0）<div>关于循环依赖的解决，看到了三种处理方式：
1.使用@Lazy 对其中一个bean懒加载
2. 使用setter属性注入，而并不是构造器注入
3. 使用@PostConstruct在依赖注入后执行初始化
具体可以参考：https:&#47;&#47;www.baeldung.com&#47;circular-dependencies-in-spring</div>2020-08-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/51/23/36bc8745.jpg" width="30px"><span>W</span> 👍（5） 💬（0）<div>MetricsAspect 这个类里面的小技巧学到了</div>2020-04-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/bd/da/3d76ea74.jpg" width="30px"><span>看不到de颜色</span> 👍（4） 💬（1）<div>很干货的文章，收获满满。
使用AOP时确实要注意执行顺序。A_Around-before -&gt; A_Before -&gt; B_Around-before -&gt; B_Before -&gt; B_Around-after -&gt; B_After -&gt; A_Around-after -&gt; A_After

课后答疑：
关于循环依赖，在单例模式下，Spring采用缓存提前暴露后初始化的方式进行解决。但是生产上出现过一次问题，当使用了@Repository注解时，循环依赖是解不了的。SpringBoot中对@Repository做了特殊处理。</div>2020-05-05</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLwTZdUafC5YM7bCASt8icUnoyYfV4hUHulexibDI7B4eaokTxYXHFtoic97DBlCAU9j5Jw4QUuGhyZQ/132" width="30px"><span>Carisy</span> 👍（2） 💬（0）<div>针对楼上做些补充说明：
1、@Resource 注解是通过CommonAnnotationBeanPostProcessor处理的，并且@Resource注解并不是“先去按名字找，找不到再按类型”而是&quot;根据类型筛选，筛选出的所有的bean根据名字获取&quot;
2、循环依赖可以通过@Lazy注解</div>2020-06-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/d7/72/cbef720d.jpg" width="30px"><span>鲁鸣</span> 👍（1） 💬（0）<div>有一个需求，A依赖B中的某个属性，这个属性会通过配置中心变更进来，但是怎么可以做到当B的这个属性初始化完成了，才会对A初始化呢，现在通过注入方式，可能A初始化时用到的B属性是个空值</div>2020-09-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/a9/ea/5bfce6c5.jpg" width="30px"><span>mgs2002</span> 👍（1） 💬（0）<div>项目也写过类似的日志打点切面,学到了一些小技巧，看后续加到项目里面</div>2020-05-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/48/7c/2aaf50e5.jpg" width="30px"><span>coder</span> 👍（0） 💬（0）<div>干货太多了，老师太强了</div>2021-08-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/91/13/009f6a74.jpg" width="30px"><span>Devil May Cry</span> 👍（0） 💬（1）<div>没理解有状态是什么意思,老师可以解答一下吗</div>2021-01-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/08/df/866ed645.jpg" width="30px"><span>xuyd</span> 👍（0） 💬（0）<div>直接在Metrics里边把异常跑出来可以嘛</div>2020-07-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ba/80/2b427c9c.jpg" width="30px"><span>libocz</span> 👍（0） 💬（3）<div>看不懂为什么Controller换成用@Metrics注解后就会与spring的事务发生顺序问题，而不用@Metrics去注解Controller的时候，能与spring的事务正确运行</div>2020-07-05</li><br/>
</ul>