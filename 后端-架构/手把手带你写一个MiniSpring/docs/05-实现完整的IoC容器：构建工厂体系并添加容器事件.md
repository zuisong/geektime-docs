你好，我是郭屹。

前面我们已经实现了IoC的核心部分，骨架已经有了，那怎么让这个IoC丰满起来呢？这就需要实现更多的功能，让我们的IoC更加完备。所以这节课我们将通过建立BeanFactory体系，添加容器事件等一系列操作，进一步完善IoC的功能。

## 实现一个完整的IoC容器

为了让我们的MiniSpring更加专业一点，也更像Spring一点，我们将实现3个功能点。

1. 进一步增强扩展性，新增4个接口。

<!--THE END-->

- ListableBeanFactory
- ConfigurableBeanFactory
- ConfigurableListableBeanFactory
- EnvironmentCapable

<!--THE END-->

2. 实现DefaultListableBeanFactory，该类就是Spring IoC的引擎。
3. 改造ApplicationContext。

下面我们就一条条来看。

### 增强扩展性

首先我们来增强BeanFactory的扩展性，使它具有不同的特性。

我们以前定义的AutowireCapableBeanFactory就是在通用的BeanFactory的基础上添加了Autowired注解特性。比如可以将Factory内部管理的Bean作为一个集合来对待，获取Bean的数量，得到所有Bean的名字，按照某个类型获取Bean列表等等。这个特性就定义在ListableBeanFactory中。
<div><strong>精选留言（21）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/29/c0/0c/f726d4d0.jpg" width="30px"><span>KernelStone</span> 👍（9） 💬（1）<div>这一小结其实新增的内容不算多！只是对之前已有的代码进行结构调整。在项目中对DefaultListableBeanFactory生成UML结构图，再进行从上到下的梳理，这样会舒服一些。

0、【接口】BF，Bean工厂
1、【接口】SingletonBeanRegistry，单例Bean仓库
2、DefaultSingletonBeanRegistry，单例Bean仓库默认实现。提供了 1 注册列表 2 单例容器 3 依赖注入管理信息（两个Map，应该是依赖 &amp; 被依赖）
3、【接口】BeanDefinitionRegistry【接口】ListableBF，这两个对照看差异。前者强调对BeanDefinition进行操作，后者强调是对List集合进行操作。
4、【接口】ConfigurableBF，Bean处理器（add &amp; get，没有apply），以及管理依赖信息。
5、【接口】AutowireCapableBF，提供自动装配选项（No、byName、byType），并在初始化前后应用（apply）Bean处理器。
6、【集成接口】ConfigurableListableBF，无内容。
7、【抽象类】AbstractBF，主要是refresh()，invokeInitMethod()，createBean()，构造器注入和属性注入。
8、AbstractAutowireCapableBF，提供成员List&lt;BeanPostProcessor&gt;！也因此它可以通过该成员进行更多的bean处理器操作，即add、get、apply在此有了具体实现。
9、DefaultListableBF，其实没有啥，打开一看只Override了【接口】ListableBF中的4个方法，其余是默认继承。（即沿着类结构往上一堆，上面也说过了）

因此，这节课真没什么新东西，不过梳理这个新的工厂体系，倒是很麻烦。。</div>2023-06-02</li><br/><li><img src="" width="30px"><span>马儿</span> 👍（3） 💬（3）<div>请教老师一下,
1.ClassPathXmlApplicationContext和AbstractApplicationContext都有beanFactoryPostProcessors属性，是不是重复了呢？感觉直接复用父类的这个属性和相关方法也是可以的。
2.AbstractAutowireCapableBeanFactory这个类中的beanPostProcessors属性写死了是AutowiredAnnotationBeanPostProcessor，不符合面向接口编程的风格。另外由于没有面向BeanPostProcessor导致DefaultListableBeanFactory需要再实现一遍 SingletonBeanRegistry
3.AbstractBeanFactory实现了BeanFactory又写了两个抽象方法applyBeanPostProcessorsBeforeInitialization和applyBeanPostProcessorAfterInitialization，这里为什么不直接实现AutowireCapableBeanFactory呢？</div>2023-03-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/ed/a0/53b36d89.jpg" width="30px"><span>CSY.</span> 👍（1） 💬（1）<div>老师我有个问题
ConfigurableBeanFactory 中的 dependentBeanMap 等几个方法为什么要使用同级继承在DefaultSingletonBeanRegistry实现，而不在AbstractBeanFactory等中实现？</div>2023-04-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/41/4d/f6d6d13a.jpg" width="30px"><span>啊良梓是我</span> 👍（1） 💬（7）<div>BeanDefinition mbd = this.getBeanDefinition(beanName); Class classToMatch = mbd.getClass();
这里为什么是拿BeanDefinition的Class的?这样子没意义吧?或者我漏掉什么了?
前面存储Bean class 是 BeanDefinition的BeanName 才对.</div>2023-04-03</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/dRrXbUnH82RRrHUSbocrgrIyyLah1Ip1ooDT5sdibn6RhmOMsD9piaiaFwsvU1T7jwU3hF6MHib7ibxqiapBVDoicsOng/132" width="30px"><span>Geek_513706</span> 👍（1） 💬（1）<div>老师，想提个建议，以后添加代码的时候能不能把添加到哪个包里面说清楚</div>2023-03-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/8b/4b/15ab499a.jpg" width="30px"><span>风轻扬</span> 👍（1） 💬（1）<div>思考题：Spring的bean作用域默认是单例的，就是我们的DefaultSingletonBeanRegistry类中持有的那个那个singletons的ConcurrentHashMap，每次获取bean之前，都会先从这个单例map中获取，获取不到才创建。
如果是多线程场景，有竞态条件存在的情况下，可以考虑将bean的作用域改为Prototype类型，对于Prototype类型的bean，Spring会为每次get请求都新建bean，所以每个请求获取到的bean是不一样的，这样就没有并发问题了
除了这两种作用域，还有另外四种作用域，我没怎么接触过，看了一下官方文档了解了一下。
文档地址：https:&#47;&#47;docs.spring.io&#47;spring-framework&#47;docs&#47;5.3.27-SNAPSHOT&#47;reference&#47;html&#47;core.html#beans-factory-scopes
遇到Spring的问题，可以多看看他们的文档，比搜索引擎强多了，写的很清晰
另外，我有一个问题，请教一下老师，ClassPathXmlApplicationContext为啥要实现BeanFactory？感觉他们两个不是一个体系里的吧，一个是上下文，一个是bean工厂</div>2023-03-24</li><br/><li><img src="" width="30px"><span>Geek_03c08d</span> 👍（0） 💬（1）<div>BeanPostProcessor 接口 的 setFactory好像没有什么用</div>2024-02-28</li><br/><li><img src="" width="30px"><span>Geek_03c08d</span> 👍（0） 💬（1）<div>希望老师回答
1. AbstractAutowireCapableBeanFactory 为什么不加一个继承AutowireCapableBeanFactory,这样就不用写抽象方法了
2. AbstractAutowireCapableBeanFactory 为什么是抽象的? 好像所有的功能都实现了</div>2024-02-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/3a/25/33/b98d15ac.jpg" width="30px"><span>Cornicione.</span> 👍（0） 💬（1）<div>ide一直提示DefaultListableBeanFactory没有实现ConfigurableBeanFactory的部分methods。看了github上的代码也是一样的问题。github上的源码ioc5真的是可以运行的吗？</div>2024-01-17</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJhxtIyXX4icMNAq5zEvchKYS3q7fwZXA3h7yV80iaibCRXniaLW95OnPC8PM2h5Ja5ibpkJ1VJowicqKZA/132" width="30px"><span>Geek_7jwpfc</span> 👍（0） 💬（1）<div>ConfigurableBeanFactory定义了getDependentBeans()方法;
ConfigurableBeanFactory的实现类是DefaultListableBeanFactory，但是
DefaultListableBeanFactory没有实现getDependentBeans()方法，居然没有报错！
要是极客时间能发图，我肯定发一个图上来！
我到底错哪儿了！</div>2023-05-30</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJhxtIyXX4icMNAq5zEvchKYS3q7fwZXA3h7yV80iaibCRXniaLW95OnPC8PM2h5Ja5ibpkJ1VJowicqKZA/132" width="30px"><span>Geek_7jwpfc</span> 👍（0） 💬（1）<div>原谅我实在没有看明白
ConfigurableBeanFactory接口, 有一个方法getDependentBeans();
DefaultListableBeanFactory是它的实现类，大师并没有实现getDependentBeans这个方法，表示看的很懵b
</div>2023-05-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/8e/91/f1bb1d06.jpg" width="30px"><span>梦幻之梦想</span> 👍（0） 💬（2）<div>我想问下DefaultListableBeanFactory中的beanDefinitionMap是怎么来的</div>2023-04-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/41/4d/f6d6d13a.jpg" width="30px"><span>啊良梓是我</span> 👍（0） 💬（1）<div>String className = beanDefinition.getClassName();
            Class&lt;?&gt; aClass = null;
            try {
                aClass = Class.forName(className);
            } catch (ClassNotFoundException e) {
                throw new RuntimeException(e);
            }

应该是这样子获取BeanDefinition定义的Bean类型才对?</div>2023-04-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/41/4d/f6d6d13a.jpg" width="30px"><span>啊良梓是我</span> 👍（0） 💬（2）<div>
package com.minis.beans.factory.config;
import com.minis.beans.factory.ListableBeanFactory;
public interface ConfigurableListableBeanFactory 
        extends ListableBeanFactory, AutowireCapableBeanFactory, 
ConfigurableBeanFactory {
}

这里是伪代码？ AutowireCapableBeanFactory按照流程下来，这里是一个Class的来哦。。。怎么可以用interface继承他的呢</div>2023-04-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/94/0a/7f7c9b25.jpg" width="30px"><span>宋健</span> 👍（0） 💬（1）<div>老师好，我想问几个小问题：
1. 请问postProcessBeanFactory这个抽象方法的作用是什么呢？
2.  我是不是可以在 registerBeanPostProcessors 中添加自己额外自定义的 BeanPostProcessor 来实现其他的注解解释器？</div>2023-04-03</li><br/><li><img src="" width="30px"><span>Geek_83a70c</span> 👍（0） 💬（1）<div>老师好，为什么ListableBeanFactory和ConfigurableBeanFactory、AutowiredCapableBeanFactory都要继承beanFacotry()接口，如果按照接口隔离思想，不是越隔离越好吗？例如以上3个接口根本其实无需涉及beanFactory中的getBean()这个最主要的方法</div>2023-04-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（1）<div>请教老师几个问题：
Q1：ApplicationEvent 类中定义的“serialVersionUID = 1L”有什么用？如果有用，为什么有的类没有定义serialVersionUID？(对于serialVersionUID，以前好像有一篇博客讲过，但一直没在意过，没有用过，好像也没有什么问题)
Q2：文中提到的“设计模式”属于23种设计模式吗？
文中提到“Spring 的这个设计模式值得我们学习，采用抽象类的方式来解耦，为用户提供了极大的扩展性的便利”，这里提到的“设计模式”，应该不是常说的23种设计模式吧。
Q3：beans.xml文件必须放在Resource目录下面吗？老师的工程，Resource目录与src目录是平级，但我以前建的工程，resource目录在src&#47;main目录下面,main下面有两个目录，java和resource，这两个平级。 这两种目录结构都可以吗？
Q4：系统有自己缺省的处理类，系统启动过程也是固定的。用户怎么利用扩展性？比如，用户想修改或增加某个功能，怎么实现？</div>2023-03-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/10/bb/f1061601.jpg" width="30px"><span>Demon.Lee</span> 👍（0） 💬（0）<div>终于把 ioc 章节撸完了一版（ https:&#47;&#47;github.com&#47;LeoDemon&#47;mini-spring&#47;tree&#47;ioc ），请教老师一个问题：

为什么 AbstractBeanFactory 中的 beanDefinitionMap 定义成并发容器（ConcurrentHashMap），而 beanDefinitionNames 和 earlySingletonObject 用的又是普通容器？另外，按理说如果有并发风险，那么 AbstractBeanFactory#getBean 方法应该使用 synchronized 之类关键词修饰才行呀。谢谢老师。</div>2024-07-15</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIJzTTCtibjCPYQE3voz3sukJ79ibtHnRticRUqyIqhnp24Yfk9ztZ2cZ1VqA6wceCnsCppl7YVbgH0w/132" width="30px"><span>Geek_99cd2f</span> 👍（0） 💬（0）<div>git上的IOC5的第70行 Class&lt;?&gt;clz = bd.getClass();写错了应该是 Class&lt;?&gt;clz = obj.getClass()；</div>2024-04-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/3a/25/33/b98d15ac.jpg" width="30px"><span>Cornicione.</span> 👍（0） 💬（0）<div>这一节的DefaultSingletonBeanRegistry也要同步修改，不然会出现未能impements的报错</div>2024-01-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/8a/e3/be7a46db.jpg" width="30px"><span>美芳</span> 👍（0） 💬（1）<div>请问下有能跑通的git代码吗？我都不知道错哪里了，一直报空指针</div>2023-08-02</li><br/>
</ul>