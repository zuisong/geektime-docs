你好，我是傅健。这节课开始，我们聊聊Spring AOP使用中常遇到的一些问题。

Spring AOP是Spring中除了依赖注入外（DI）最为核心的功能，顾名思义，AOP即Aspect Oriented Programming，翻译为面向切面编程。

而Spring AOP则利用CGlib和JDK动态代理等方式来实现运行期动态方法增强，其目的是将与业务无关的代码单独抽离出来，使其逻辑不再与业务代码耦合，从而降低系统的耦合性，提高程序的可重用性和开发效率。因而AOP便成为了日志记录、监控管理、性能统计、异常处理、权限管理、统一认证等各个方面被广泛使用的技术。

追根溯源，我们之所以能无感知地在容器对象方法前后任意添加代码片段，那是由于Spring在运行期帮我们把切面中的代码逻辑动态“织入”到了容器对象方法内，所以说**AOP本质上就是一个代理模式**。然而在使用这种代理模式时，我们常常会用不好，那么这节课我们就来解析下有哪些常见的问题，以及背后的原理是什么。

## 案例1：this调用的当前类方法无法被拦截

假设我们正在开发一个宿舍管理系统，这个模块包含一个负责电费充值的类ElectricService，它含有一个充电方法charge()：
<div><strong>精选留言（22）</strong></div><ul>
<li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eo2GMhevabZrjINs2TKvIeGC7TJkicNlLvqTticuM5KL8ZN80OC2CnrsUyzPcZXO4uptj4Q1S4jT2lQ/132" width="30px"><span>jerry guo</span> 👍（1） 💬（2）<div>这篇太难了 没看懂</div>2022-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/f5/4e/87f4faee.jpg" width="30px"><span>阿璐4r</span> 👍（24） 💬（1）<div>我一点也不聪明</div>2021-12-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/f4/8c/0866b228.jpg" width="30px"><span>子房</span> 👍（9） 💬（0）<div>本质原因是 bean 初始化后被创建为代理 bean ，只有访问代理对象 方法才会被拦截</div>2021-05-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/51/9b/ccea47d9.jpg" width="30px"><span>安迪密恩</span> 👍（5） 💬（1）<div>hi 傅哥， 案例一的解决方案一，需要加@Lazy否则会出现循环依赖。
  @Lazy
  @Autowired private ElectricService electricService;</div>2022-03-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/37/2b/b32f1d66.jpg" width="30px"><span>Ball</span> 👍（5） 💬（0）<div>🤔总结一下，今天以两个 AOP 场景下的问题为线索，深入 Spring 源码探讨了 Spring 的动态代理机制，还分享了 AOP 场景下问题的 debug 技巧。结合问题定位的过程，最终给出了问题的多种解决方案。👍</div>2021-04-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/16/5b/83a35681.jpg" width="30px"><span>Monday</span> 👍（4） 💬（1）<div>案例2：user的命名一会user一会adminUser，不统一啊</div>2021-06-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/4c/dd/c6035349.jpg" width="30px"><span>Bumblebee</span> 👍（2） 💬（0）<div>今日收获（总结的不对的希望老师同学们多多指正）

① JDK 动态代理只能对实现了接口的类生成代理，而不能针对普通类。而 CGLIB 是可以针对类实现代理，主要是对指定的类生成一个子类，覆盖其中的方法，来实现代理对象。

② this调用的当前类方法无法被拦截（可以通过@Autowired、AopContext.currentProxy() 方式解决）；

③ 我们一般不能直接从代理类中去拿被代理类的属性，这是因为除非我们显示设置 spring.objenesis.ignore 为 true，否则代理类的属性是不会被 Spring 初始化的，我们可以通过在被代理类中增加一个方法来间接获取其属性。


总结：我觉得SpringAop生成的代理类是对被代理类的一个包装，代理类对象仅被代理对象方法执行前后进行增强，原始方法的调用还是由被代理对象自己执行；</div>2022-05-30</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q3auHgzwzM7RKo5N6Y7Hgcr3YicsHul0XuDACAYzIpiaiazOc7LkkOoDlAHTTmX1dlIrhBZ6gP1QFXermLrP8Algg/132" width="30px"><span>小林桑</span> 👍（1） 💬（0）<div>这个课好像没见到老师来答疑？ </div>2024-01-14</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJRgMw7FHDF5P9Y0aUAgzstRcm5ic5fS3rQ3dRu2HNgUWtuXw1lmRPlXq56wJNxJNF9P5XGb96mttw/132" width="30px"><span>Geek_930ce1</span> 👍（1） 💬（4）<div>ReflectionFactory reflectionFactory = ReflectionFactory.getReflectionFactory();
        Constructor&lt;AdminUserService&gt; constructor1  = AdminUserService.class.getConstructor();
        Constructor constructor2 = reflectionFactory.newConstructorForSerialization(AdminUserService.class,constructor1);
        AdminUserService adminUserService3 = (AdminUserService)constructor2.newInstance();
        System.out.println(&quot;sun.reflect.ReflectionFactory.newConstructorForSerialization().newInstance()&quot;+adminUserService3);
经过尝试，还是存在成员变量，是为什么</div>2022-06-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/af/b8/458866d3.jpg" width="30px"><span>Bo</span> 👍（0） 💬（0）<div>关于思考题，不知道为什么用老师的AdminUserService就还是会初始化类属性，自定义的类就可以验证不会初始化，后面再关注。

验证代码如下：（参考https:&#47;&#47;blog.csdn.net&#47;Zong_0915&#47;article&#47;details&#47;126512236）
public class Test {
    public final User user = new User(&quot;LJJ&quot;);
    public User user2 = new User(&quot;LJJ&quot;);
    public String name = &quot;Hello&quot;;
    public final String str = &quot;ssss&quot;;
    public Integer a = 12222;
    public final Integer b = 12222;
    public int aa = 1;
    public final int bb = 2;

    public static void main(String[] args) throws Exception {
        ReflectionFactory reflectionFactory = ReflectionFactory.getReflectionFactory();
        Constructor constructor = reflectionFactory.newConstructorForSerialization(Test.class, Object.class.getDeclaredConstructor());
        constructor.setAccessible(true);
        Test t = (Test) constructor.newInstance();
        System.out.println(&quot;final user: &quot; + t.user);
        System.out.println(&quot;user: &quot; + t.user2);
        System.out.println(&quot;final String: &quot; + t.str);
        System.out.println(&quot;String: &quot; + t.name);
        System.out.println(&quot;final Integer: &quot; + t.b);
        System.out.println(&quot;Integer: &quot; + t.a);
        System.out.println(&quot;final int: &quot; + t.bb);
        System.out.println(&quot;int: &quot; + t.aa);
    }
}

注意：
- sun.reflect在Java 9以上才引入
- 如果编译报错“package sun.reflect does not exist”，但是在代码里其实可以看到源码，则可以尝试在IDEA设置里搜索Java Compiler，取消勾选 `Use &#39;--release&#39; option for cross-compilation` 选项即可，亲试有效。参考[IntelliJ says the package does not exist, But I can access the package](https:&#47;&#47;stackoverflow.com&#47;questions&#47;40448203&#47;intellij-says-the-package-does-not-exist-but-i-can-access-the-package)——StackOverFlow</div>2023-03-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/55/4c/a3b696fd.jpg" width="30px"><span>饮水偲源</span> 👍（0） 💬（0）<div>第3种构造方式，成员属性不会初始化的代码
       
 ReflectionFactory reflectionFactory = ReflectionFactory.getReflectionFactory();
        Constructor constructor = reflectionFactory.newConstructorForSerialization(AdminUserService.class);
        AdminUserService adminUserService = (AdminUserService) constructor.newInstance();
        System.out.println(adminUserService.adminUser.payNum);

但是
reflectionFactory.newConstructorForSerialization这个方法还有种入参，传入指定构造方法时，其可以完成成员属性初始化。
Constructor&lt;?&gt; newConstructorForSerialization(Class&lt;?&gt; var1, Constructor&lt;?&gt; var2)</div>2022-09-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/34/cf/0a316b48.jpg" width="30px"><span>蝴蝶</span> 👍（0） 💬（0）<div>        Constructor&lt;Object&gt; constructor = Object.class.getDeclaredConstructor();
        Constructor&lt;?&gt; constructor1 = ReflectionFactory.getReflectionFactory()
                .newConstructorForSerialization(Person.class, constructor);

        constructor1.s        Constructor&lt;Object&gt; constructor = Object.class.getDeclaredConstructor();
        Constructor&lt;?&gt; constructor1 = ReflectionFactory.getReflectionFactory()
                .newConstructorForSerialization(Person.class, constructor);

        constructor1.setAccessible(true);
        Person personByReflection = (Person) constructor1.newInstance();
        
        System.out.println(personByReflection);etAccessible(true);
        Person personByReflection = (Person) constructor1.newInstance();
        
        System.out.println(personByReflection);</div>2022-07-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/34/cf/0a316b48.jpg" width="30px"><span>蝴蝶</span> 👍（0） 💬（0）<div>        Constructor&lt;Object&gt; constructor = Object.class.getDeclaredConstructor();
        Constructor&lt;?&gt; constructor1 = ReflectionFactory.getReflectionFactory()
                .newConstructorForSerialization(Person.class, constructor);

        constructor1.setAccessible(true);
        Person personByReflection = (        Constructor&lt;Object&gt; constructor = Object.class.getDeclaredConstructor();
        Constructor&lt;?&gt; constructor1 = ReflectionFactory.getReflectionFactory()
                .newConstructorForSerialization(Person.class, constructor);

        constructor1.setAccessible(true);
        Person personByReflection = (Person) constructor1.newInstance();
                Constructor&lt;Object&gt; constructor = Object.class.getDeclaredConstructor();
        Constructor&lt;?&gt; constructor1 = ReflectionFactory.getReflectionFactory()
                .newConstructorForSerialization(Person.class, constructor);

        constructor1.setAccessible(true);
        Person personByReflection = (Person) constructor1.newInstance();
        11111
        System.out.println(personByReflectio11n);
        System.out.println(personByReflection);) constructor1.newInstance();
        
        System.out.println(personByReflection);</div>2022-07-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/62/d3/791d0f5e.jpg" width="30px"><span>胡同学</span> 👍（0） 💬（0）<div>@@Lookup 也可以实现案例一</div>2022-05-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/51/9b/ccea47d9.jpg" width="30px"><span>安迪密恩</span> 👍（0） 💬（1）<div>hi 傅哥， 那是不是说 private 方法无法被AOP 增强？</div>2022-03-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/06/76/c2d807bf.jpg" width="30px"><span>开卷</span> 👍（0） 💬（1）<div>案例一里，自己引用自己，我报了循环依赖的错误</div>2022-02-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1c/0c/b5b2cd51.jpg" width="30px"><span>豆泥丸</span> 👍（0） 💬（0）<div>案例二，成员变量我如果不声明成final，是不是就可以继承到了啊</div>2021-11-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d4/f3/129d6dfe.jpg" width="30px"><span>李二木</span> 👍（0） 💬（0）<div>String payNum = dminUserService.user.getPayNum(); 有两个拼写错误，dminUserService 不对，应该是adminUserService，adminUserService里属性名是adminUser,不是user</div>2021-11-02</li><br/><li><img src="" width="30px"><span>Geek_5aec96</span> 👍（0） 💬（2）<div>老师 你好 this为什么不是代理对象？</div>2021-07-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/16/5b/83a35681.jpg" width="30px"><span>Monday</span> 👍（0） 💬（1）<div>案例2如果getUser()也被AOP拦截的话，ElectricService中调用adminUserService.getUser()还是会报NPE。我理解AdminUserService的代理类的getUser()方法会调用AdminUserService.getUser()应该会返回非空对象才对啊</div>2021-06-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/fc/18/8e69f7cf.jpg" width="30px"><span>一记妙蛙直拳</span> 👍（0） 💬（1）<div>老师我有个问题注解@EnableAspectJAutoProxy的属性proxyTargetClass默认是false，ElectricService并没有实现接口，为什么还可以创建动态代理对象？</div>2021-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ce/d7/074920d5.jpg" width="30px"><span>小飞同学</span> 👍（0） 💬（0）<div>System.setProperty(DebuggingClassWriter.DEBUG_LOCATION_PROPERTY, &quot;.&#47;cglib&quot;); &#47;&#47;代理类持久化到文件
思考题：
AdminUserServiceSon继承AdminUserService，看起来父类都没有加载。但是为啥还是希望老师解答下
        SunReflectionFactoryInstantiator instantiator = new SunReflectionFactoryInstantiator(AdminUserServiceSon.class);
        System.out.println(instantiator.newInstance());

        Constructor&lt;AdminUserServiceSon&gt; constructor = AdminUserServiceSon.class.getConstructor(null);
        System.out.println(constructor.newInstance().adminUser);

        AdminUserServiceSon adminUserServiceSon = AdminUserServiceSon.class.newInstance();
        System.out.println(adminUserServiceSon.adminUser);</div>2021-04-30</li><br/>
</ul>