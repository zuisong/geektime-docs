你好，我是朱晔。今天，我们聊聊Spring框架给业务代码带来的复杂度，以及与之相关的坑。

在上一讲，通过AOP实现统一的监控组件的案例，我们看到了IoC和AOP配合使用的威力：当对象由Spring容器管理成为Bean之后，我们不但可以通过容器管理配置Bean的属性，还可以方便地对感兴趣的方法做AOP。

不过，前提是对象必须是Bean。你可能会觉得这个结论很明显，也很容易理解啊。但就和上一讲提到的Bean默认是单例一样，理解起来简单，实践的时候却非常容易踩坑。其中原因，一方面是，理解Spring的体系结构和使用方式有一定曲线；另一方面是，Spring多年发展堆积起来的内部结构非常复杂，这也是更重要的原因。

在我看来，Spring框架内部的复杂度主要表现为三点：

- 第一，Spring框架借助IoC和AOP的功能，实现了修改、拦截Bean的定义和实例的灵活性，因此真正执行的代码流程并不是串行的。
- 第二，Spring Boot根据当前依赖情况实现了自动配置，虽然省去了手动配置的麻烦，但也因此多了一些黑盒、提升了复杂度。
- 第三，Spring Cloud模块多版本也多，Spring Boot 1.x和2.x的区别也很大。如果要对Spring Cloud或Spring Boot进行二次开发的话，考虑兼容性的成本会很高。
<div><strong>精选留言（12）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/13/26/38/ef063dc2.jpg" width="30px"><span>Darren</span> 👍（35） 💬（2）<div>第一个问题：
切入点指示符
Spring AOP 支持10种切点指示符：execution、within、this、target、args、@target、@args、@within、@annotation、bean下面做下简记(没有写@Pointcut(),请注意)：

execution: 用来匹配执行方法的连接点的指示符。
用法相对复杂，格式如下:execution(权限访问符 返回值类型 方法所属的类名包路径.方法名(形参类型) 异常类型)
e.g. execution(public String com.darren.hellxz.test.Test.access(String,String))

权限修饰符和异常类型可省略，返回类型支持通配符，类名、方法名支持*通配，方法形参支持..通配
within: 用来限定连接点属于某个确定类型的类。
within(com.darren.hellxz.test.Test)
within(com.darren.hellxz.test.) &#47;&#47;包下类
within(com.darren.hellxz.test..) &#47;&#47;包下及子包下

this和target: this用于没有实现接口的Cglib代理类型，target用于实现了接口的JDK代理目标类型
举例：this(com.darren.hellxz.test.Foo) &#47;&#47;Foo没有实现接口，使用Cglib代理，用this
实现了个接口public class Foo implements Bar{...}
target(com.darren.hellxz.test.Test) &#47;&#47;Foo实现了接口的情况

args: 对连接点的参数类型进行限制，要求参数类型是指定类型的实例。
args(Long)

@target: 用于匹配类头有指定注解的连接点
@target(org.springframework.stereotype.Repository)

@args: 用来匹配连接点的参数的，@args指出连接点在运行时传过来的参数的类必须要有指定的注解

@Pointcut(&quot;@args(org.springframework.web.bind.annotation.RequestBody)&quot;)  
public void methodsAcceptingEntities() {}

@within: 指定匹配必须包括某个注解的的类里的所有连接点
@within(org.springframework.stereotype.Repository)

@annotation: 匹配那些有指定注解的连接点
@annotation(org.springframework.stereotype.Repository)

bean: 用于匹配指定Bean实例内的连接点，传入bean的id或name,支持使用*通配符

切点表达式组合
使用&amp;&amp;、||、!、三种运算符来组合切点表达式，表示与或非的关系

第二个问题其实不太懂，网上搜了搜，核心应该是这个方法：
org.springframework.util.PropertyPlaceholderHelper#replacePlaceholders(java.lang.String, java.util.Properties)

参考链接：https:&#47;&#47;www.jianshu.com&#47;p&#47;5fecf71024af</div>2020-04-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/79/01/e71510dc.jpg" width="30px"><span>hellojd</span> 👍（8） 💬（1）<div>我也经常看框架源码，但缺失了老师的演示及溯源过程，学习到了。</div>2020-04-28</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/bvj76PmeUvW8kokyu91IZWuRATKmabibDWbzAj2TajeEic7WvKCJOLaOh6jibEmdQ36EO3sBUZ0HibAiapsrZo64U8w/132" width="30px"><span>梦倚栏杆</span> 👍（6） 💬（1）<div>1. 配置优先级的问题，理解热加载的时候仔细的看过，知道有这么回事，老师举得这个例子：开发和运维都设置了配置，然后运维的把开发的覆盖了，这种问题如果遇到了怎么查呢？如果是同一个人统一管理还好说，不同的人谁知道谁设置了什么呢？
2. 切面不成功的内容，我卡在了切面上。切面怎么用还不太了解。</div>2020-04-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/12/b2/3fb9a4a1.jpg" width="30px"><span>招财</span> 👍（1） 💬（3）<div>老师，我现在项目中遇到了一个问题，就是用springboot的全局异常处理时，响应出去的信息，编码格式都是ISO-8859-1，试过了在配置文件中设置spring.http.encoding.charset=utf-8和过滤器中给response去setCharacterEncoding为utf-8，但是还是不行。正常响应的数据是不乱码的，只有全局异常处理出去的响应有乱码，这个应该怎么解决呀</div>2020-05-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/81/e6/6cafed37.jpg" width="30px"><span>旅途</span> 👍（1） 💬（1）<div>老师 问两个问题
1.第一个例子 去掉ribbon依赖后 ApacheHttpClient注册了bean 所以@FeignClient这里面直接就使用的ApacheHttpClient的bea 不走那个new 的代码了是吗 ？
2.第二个例子. ConfigurationPropertySourcesPropertySourcess这个类实际上一个代理 查询的走的还是其他的配置源 这么做的意义是什么?</div>2020-05-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d6/60/f21b2164.jpg" width="30px"><span>jacy</span> 👍（0） 💬（1）<div>有个疑问，思考与讨论二中的真实数据库密码放哪呢？</div>2021-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f9/aa/3e80212e.jpg" width="30px"><span>龙猫</span> 👍（12） 💬（0）<div>这节课有点难度啊</div>2020-06-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/24/2a/33441e2b.jpg" width="30px"><span>汝林外史</span> 👍（11） 💬（0）<div>感觉就在等最后的解决方案，然后戛然而止了。。。</div>2020-04-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7e/bb/947c329a.jpg" width="30px"><span>程序员小跃</span> 👍（3） 💬（0）<div>源码之下无秘密，但是看源码挑战了一个程序员的心境，需要耐心，细心，恒心，给自己加油</div>2020-07-23</li><br/><li><img src="" width="30px"><span>Geek_8b92bf</span> 👍（1） 💬（0）<div>within(feign.Client+) 为什么是切入execute方法，不是切人api方法，这个不太明白</div>2022-06-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f5/57/ce10fb1b.jpg" width="30px"><span>天天向上</span> 👍（1） 💬（0）<div>老师好，对于Spring aop中的args表达式我有疑问：
1.args可以对连接点的参数类型进行限制，要求参数类型是指定类型的实例，用法是args(类型的全限定名)。
2.也可以用来访问目标方法的参数，用法是args(变量名)。
这两种用法目前没看到在同一个地方讲到的。我想知道这两种用法对应的args是同一个args吗（虽然都叫做args）。如果是同一个的话，那spring是如何知道需要用到的是哪种用法呢？</div>2021-01-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/32/b6/cd785ef7.jpg" width="30px"><span>9jay</span> 👍（0） 💬（0）<div>对FeignClient进行Around 切面后，拿到Response的body 字节流无法重复读取。
导致在切面的时候读取了返回值字节流后，Feign再去反序列化时对象就为空。
这个有好的方法解决吗？</div>2021-12-23</li><br/>
</ul>