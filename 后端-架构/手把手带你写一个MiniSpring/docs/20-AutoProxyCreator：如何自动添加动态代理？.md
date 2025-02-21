你好，我是郭屹，今天我们继续手写MiniSpring，这也是AOP正文部分的最后一节。今天我们将完成一个有模有样的AOP解决方案。

## 问题的引出

前面，我们已经实现了通过动态代理技术在运行时进行逻辑增强，并引入了Pointcut，实现了代理方法的通配形式。到现在，AOP的功能貌似已经基本实现了，但目前还有一个较大的问题，具体是什么问题呢？我们查看aplicationContext.xml里的这段配置文件来一探究竟。

```xml
<bean id="realaction" class="com.test.service.Action1" />
<bean id="action" class="com.minis.aop.ProxyFactoryBean">
    <property type="String" name="interceptorName" value="advisor" />
    <property type="java.lang.Object" name="target" ref="realaction"/>	
</bean>
```

看这个配置文件可以发现，在ProxyFactoryBean的配置中，有个Object类型的属性：target。在这里我们的赋值ref是realactionbean，对应Action1这个类。也就是说，给Action1这个Bean动态地插入逻辑，达成AOP的目标。  
在这里，一次AOP的配置对应一个目标对象，如果整个系统就只需要为一个对象进行增强操作，这自然没有问题，配置一下倒也不会很麻烦，但在一个稍微有规模的系统中，我们有成百上千的目标对象，在这种情况下一个个地去配置则无异于一场灾难。
<div><strong>精选留言（11）</strong></div><ul>
<li><img src="" width="30px"><span>马儿</span> 👍（1） 💬（1）<div>这节课的代码能够做到不需要在beans.xml中额外专门配置来生成代理对象，已经接近spring的雏形了。但是按照之前的代码是跑不起来的，需要对之前的BeanPostProcessor的逻辑修改一下，应该是老师之前讲漏了的部分。主要工作在修改AbstractAutowireCapableBeanFactory类将属性中的beanPostProcessors改为面向接口的列表，其次是修改ClassPathXmlApplicationContext#registerBeanPostProcessors让其可以在配置文件中读到注册的BeanPostProcessors并注册到容器中。最后将我们之前用到的AutowiredAnnotationBeanPostProcessor注册到容器中管理就能够自动发现了。
代码修改可以参考：https:&#47;&#47;github.com&#47;horseLk&#47;mini-spring&#47;commit&#47;7186afebeaf30d622d79b4111970945abca97701</div>2023-04-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（6） 💬（1）<div>问题放在第20课，但问题是关于第19课的：
Q1：Join Point和Pointcut的区别是什么？两个看起来是一回事啊。
Q2：流程方面，Interceptor先拦截，拦截以后再进行增强操作。换一种说法，先是Interceptor工作，然后是Join Point、Pointcut、advice这些登场，对吗？
Q3：19课的总结部分，是这样说的：“Advisor：通知者，它实现了 Advice”。19课的留言解答有这样一句话“advisor则是一个管理类，它包了一个advice，还能寻找到符合条件的方法名进行增强”。 留言的解释很不错，但总结部分，“实现了 Advice”，个人感觉这个措辞不是很合理啊，怎么是“实现”？这个词容易让人理解为接口与实现类的关系。</div>2023-04-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/b5/a4/67d6e3cb.jpg" width="30px"><span>__@Wong</span> 👍（4） 💬（2）<div>补充一个点，这里需要保证AutowiredAnnotationBeanPostProcessor和BeanNameAutoProxyCreator两个BeanPostProcessor的优先级，AutowiredAnnotationBeanPostProcessor要在之前哦，在xml文件里面AutowiredAnnotationBeanPostProcessor的bean要放前面。</div>2023-06-24</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/XWv3mvIFORNgRk9wF8QLb9aXfh1Uz1hADtUmlFwQJVxIzhBf8HWc4QqU7iaTzj8wB5p5QJLRAvlQNrOqXtrg1Og/132" width="30px"><span>Geek_320730</span> 👍（1） 💬（1）<div>可以定义一个注解@Transaction并实现一个MethodMatcher，根据有没有这个注解来判断方法是否匹配，匹配的话，在方法执行前，手动开启事务，方法结束后，手动提交事务，有异常的话回滚事务。那事务方法调用事务方法的时候不知道会不会报错。。。

另外遇到Bean可以一直嵌套代理的问题，比如上一章手动配置的action,本身就是一个ProxyFactoryBean了，但是他的名字依然符合本章的action*的匹配规则，这样就又加了一层代理，注入的时候就会失败。需要在获取类的时候判断一下类型递归返回，或者在bean匹配规则的时候做一下类型判断，如果本身是个ProxyFactoryBean了，就不做操作返回。</div>2023-04-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/b5/a4/67d6e3cb.jpg" width="30px"><span>__@Wong</span> 👍（0） 💬（2）<div>将原有的bean替换成代理后的bean那里，如果遇到循环引用会有问题吧， 引用的还是旧的bean。</div>2023-06-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/0e/dd/4d468ad7.jpg" width="30px"><span>__Alucard</span> 👍（0） 💬（1）<div>完结撒花，谢谢指导</div>2023-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/0e/dd/4d468ad7.jpg" width="30px"><span>__Alucard</span> 👍（0） 💬（2）<div>动态代理失效的根本原因是@Autowired注解解析的时候，取到的spring bean还是没代理的对象； 我的临时解决方案是 在BeanNameAutoProxyCreator的postProcessBeforeInitialization手动把创建后的动态代理对象注入进spring ioc中， beanFactory.registerBean(beanName,proxyFactoryBean);  但是这样会导致BeanFactory又对外暴露了注册bean的接口，void registerBean(String beanName, Object obj);明显不合适，这个有没有更好的办法</div>2023-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/da/d9/f051962f.jpg" width="30px"><span>浩仔是程序员</span> 👍（0） 💬（1）<div>老师你好，怎么github上面这块framework这个包下面有部分代码是重复的呢？建议可以来个代码结构的总结</div>2023-05-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/3a/ff/d2/c1f5334d.jpg" width="30px"><span>dirtychill</span> 👍（0） 💬（0）<div>一步步录入代码完成，可运行的，利用lombok简化了代码，便于学习，可能还有一些bug或者一些扩展，可以来维护https:&#47;&#47;github.com&#47;DirtyBit64&#47;Mini-Spring</div>2024-07-06</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/BBaAkryVSFImaoWL5QcRbSpB8IfUbUZGfzGH4xUz0qicJGU1vREvcFedgWAXJlYX9ibkzG3BlnJEQDzejZ5ibLCGA/132" width="30px"><span>Geek_28bb47</span> 👍（0） 💬（0）<div>已学完，https:&#47;&#47;github.com&#47;ykexc&#47;minispring，每节课对应一个分支，欢迎大家来参考，感觉懂了一点，还需要看完spring源码再继续品味。</div>2024-04-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/2c/68/c299bc71.jpg" width="30px"><span>天敌</span> 👍（0） 💬（0）<div>老师，关于使用 Proxy.newProxyInstance 生成的对象在进行 xml 中 ref 的属性绑定过程中，由于生成的代理对象并没有继承被代理对象的类，导致进行赋值时
IllegalArgumentException: argument type mismatch
这个问题，应该如何解决呢？</div>2023-07-23</li><br/>
</ul>