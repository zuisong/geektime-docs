在上一节课我们讲到，当创建对象是一个“大工程”的时候，我们一般会选择使用工厂模式，来封装对象复杂的创建过程，将对象的创建和使用分离，让代码更加清晰。那何为“大工程”呢？上一节课中我们讲了两种情况，一种是创建过程涉及复杂的if-else分支判断，另一种是对象创建需要组装多个其他类对象或者需要复杂的初始化过程。

今天，我们再来讲一个创建对象的“大工程”，依赖注入框架，或者叫依赖注入容器（Dependency Injection Container），简称DI容器。在今天的讲解中，我会带你一块搞清楚这样几个问题：DI容器跟我们讲的工厂模式又有何区别和联系？DI容器的核心功能有哪些，以及如何实现一个简单的DI容器？

话不多说，让我们正式开始今天的学习吧！

## 工厂模式和DI容器有何区别？

实际上，DI容器底层最基本的设计思路就是基于工厂模式的。DI容器相当于一个大的工厂类，负责在程序启动的时候，根据配置（要创建哪些类对象，每个类对象的创建需要依赖哪些其他类对象）事先创建好对象。当应用程序需要使用某个类对象的时候，直接从容器中获取即可。正是因为它持有一堆对象，所以这个框架才被称为“容器”。

DI容器相对于我们上节课讲的工厂模式的例子来说，它处理的是更大的对象创建工程。上节课讲的工厂模式中，一个工厂类只负责某个类对象或者某一组相关类对象（继承自同一抽象类或者接口的子类）的创建，而DI容器负责的是整个应用中所有类对象的创建。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/16/ef/5b/ff28088f.jpg" width="30px"><span>郑大钱</span> 👍（25） 💬（1）<div>“初级工程师在维护代码，高级工程师在设计代码，资深工程师在重构代码”
依赖注入框架好牛逼呀！当手把手教我设计一个框架之后，才破除了我对框架的权威和迷信。
自己最开始做业务也是在原有框架上面修修补补，回过头来看，发现自己非常能忍，即使原有的框架很难用，自己也能坚持用下去。
转念一想，那不是能忍，那是懒。懒得去理解框架的原理，懒得让它更易用。
像豌豆公主一样保持自己的敏感，是持续改进的动力。</div>2020-11-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/0a/63/165b0d40.jpg" width="30px"><span>少年锦时</span> 👍（0） 💬（1）<div>beanDefinition.isLazyInit() == false  为什么不直接写成!beanDefinition.isLazyInit() 呢</div>2020-07-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/95/11/eb431e52.jpg" width="30px"><span>沈康</span> 👍（165） 💬（7）<div>默默的掏出了《spring源码深度解析》回顾一番
 1、构造器循环依赖
构造器注入的循环依赖是无法解决的，只能抛出bean创建异常使容器无法启动
如何判断是循环依赖？
把正在创建的bean放入到一个(正在创建的map)中，如果依赖创建bean在此map中存在，则抛出异常。
2、setter方法循环依赖
①单例情况可以解决循环依赖，方法是提前暴露一个返回该单例的工厂方法，让依赖对象可以引用到
②多例不能解决循环依赖，因为多例不需要缓存</div>2020-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/3a/5b/ce1724ca.jpg" width="30px"><span>undefined</span> 👍（66） 💬（2）<div>把本文的示例补全成了可执行代码：
https:&#47;&#47;github.com&#47;plusmancn&#47;learn-java&#47;tree&#47;master&#47;src&#47;main&#47;java&#47;Exercise&#47;di
顺便纠正一个笔误：
BeansFactory 下 createBean 方法中：singletonObjects.contains 应为 singletonObjects. containsKey</div>2020-02-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/44/47/3ddb94d0.jpg" width="30px"><span>javaadu</span> 👍（39） 💬（2）<div>20200218再次复习：
1. 研究了Spring容器中处理循环依赖的知识点：（1）只能处理单例的、setter注入的循环依赖，其他的注入模式无法处理；（2）依赖缓存处理循环依赖，关键思想是，将正在创建中的对象提前暴露一个单例工厂，让其他实例可以引用到
2. 网上一篇比较好的文章：https:&#47;&#47;juejin.im&#47;post&#47;5d0d8f64f265da1b7b3193ac</div>2020-02-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/7a/f5/54a5084b.jpg" width="30px"><span>简单猫</span> 👍（37） 💬（3）<div>不要被这些所谓的专业化名词吓到了 什么三级缓存。a依赖b，b依赖c，c依赖a,d依赖a，b，c什么的，你要解决的核心是不要重复创建。那么你就要把已经创建的对象存起来(map，hashmaps什么的) ，然后再次创建的时候先去缓存map中读取，没有才创建。 创建对象流程：1先反射创建类对象  2然后配置类里面的属性 方法(依赖就在这)。
至于你要怎么利用设计模式解耦 分3级缓存 分别存储完全实例化的对象  未设置属性方法类对象  还是对象工厂  那就看如何好用咯</div>2020-05-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/2f/ed/a87bb8fa.jpg" width="30px"><span>此鱼不得水</span> 👍（23） 💬（0）<div>Spring解决循环依赖的办法是多级缓存。</div>2020-02-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/86/25/25ded6c3.jpg" width="30px"><span>zhengyu.nie</span> 👍（16） 💬（0）<div>基本就是Spring源码大体原型了，委托的BeanFactory在Spring源码里是DefaultListableBeanFactory。循环依赖解决是三级缓存，提前暴露还没有初始化结束的bean。检测是Map存一下过程，aba这样顺序判断，有重复（a出现两次）就是环了。

三级缓存源码对应
org.springframework.beans.factory.support.DefaultSingletonBeanRegistry#getSingleton

&#47;**
	 * Return the (raw) singleton object registered under the given name.
	 * &lt;p&gt;Checks already instantiated singletons and also allows for an early
	 * reference to a currently created singleton (resolving a circular reference).
	 * @param beanName the name of the bean to look for
	 * @param allowEarlyReference whether early references should be created or not
	 * @return the registered singleton object, or {@code null} if none found
	 *&#47;
	@Nullable
	protected Object getSingleton(String beanName, boolean allowEarlyReference) {
		Object singletonObject = this.singletonObjects.get(beanName);
		if (singletonObject == null &amp;&amp; isSingletonCurrentlyInCreation(beanName)) {
			synchronized (this.singletonObjects) {
				singletonObject = this.earlySingletonObjects.get(beanName);
				if (singletonObject == null &amp;&amp; allowEarlyReference) {
					ObjectFactory&lt;?&gt; singletonFactory = this.singletonFactories.get(beanName);
					if (singletonFactory != null) {
						singletonObject = singletonFactory.getObject();
						this.earlySingletonObjects.put(beanName, singletonObject);
						this.singletonFactories.remove(beanName);
					}
				}
			}
		}
		return singletonObject;
	}


	&#47;** Cache of singleton objects: bean name to bean instance. *&#47;
	private final Map&lt;String, Object&gt; singletonObjects = new ConcurrentHashMap&lt;&gt;(256);

	&#47;** Cache of singleton factories: bean name to ObjectFactory. *&#47;
	private final Map&lt;String, ObjectFactory&lt;?&gt;&gt; singletonFactories = new HashMap&lt;&gt;(16);

	&#47;** Cache of early singleton objects: bean name to bean instance. *&#47;
	private final Map&lt;String, Object&gt; earlySingletonObjects = new HashMap&lt;&gt;(16);
</div>2020-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/99/3b/791d0f5e.jpg" width="30px"><span>王先森</span> 👍（11） 💬（0）<div>php开发者默默的去瞅laravel的DI容器</div>2020-06-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/18/81/83b6ade2.jpg" width="30px"><span>好吃不贵</span> 👍（9） 💬（1）<div>createBean先用Topology sort看是否有环，然后再按序创建？</div>2020-02-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/64/9b/d1ab239e.jpg" width="30px"><span>J.Smile</span> 👍（9） 💬（0）<div>思考题:
①构造器初始化方式，无法解决循环依赖
②set注入方式初始化，有两种:
第一种，创建的是单例对象，可以解决。
第二种，创建的是原型对象，由于di容器不缓存对象导致无法提前暴露一个创建中的对象，依赖对象就会getbean时创建一个新对象，接着又进去循环依赖创建新对象…依然解决不了。</div>2020-02-14</li><br/><li><img src="" width="30px"><span>Geek_3b1096</span> 👍（8） 💬（1）<div>终于解答了我对于DI的疑惑</div>2020-02-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f1/de/3ebcbb3f.jpg" width="30px"><span>DullBird</span> 👍（7） 💬（3）<div>1. 我理解spring 解决A和B对象的循环引用是这样的流程是这样的，假设先加载A，丢一个A的引用到一个引用map&lt;id, ref&gt;，发现A有一个filed 引用B，就初始化B，丢一个B的引用到Map，初始化发现需要一个A，就从map里面找，找到了一个A，就把A的引用丢给B的属性，然后B加载结束了，A继续加载，拿到map里面的B，加载完成。</div>2020-02-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/36/84/788f0c60.jpg" width="30px"><span>勤劳的明酱</span> 👍（7） 💬（3）<div>思考题：
 构造器注入不好解决
 setter注入：根据BenDefinition创建的bean可以是未完成的bean，就是说bean里面的属性可以是没有填充过的，这个时候bean依然能创建成功，之后属性，postConstruct、InitializingBean、init-method完成之后才能算是一个完整的bean，所以即使出现循环依赖也能解决。</div>2020-02-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/37/3f/a9127a73.jpg" width="30px"><span>KK</span> 👍（6） 💬（1）<div>这里例子，过于限制语言了。对 java 用户友好，对其他用户似乎意义不大。</div>2022-05-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/44/47/3ddb94d0.jpg" width="30px"><span>javaadu</span> 👍（6） 💬（0）<div>关于思考题，对象的依赖关系应该是一个有向无环图（DAG），我倾向于在解析配置文件的时候检测是否存在环，不过这样在大型项目中可能性能不会太好。回头研究下Spring咋做的。</div>2020-02-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/50/d7/f82ed283.jpg" width="30px"><span>辣么大</span> 👍（5） 💬（0）<div>循环依赖的意思是A依赖于B，B依赖于A（Bean A → Bean B → Bean A）出现循环依赖，首先应该考虑设计出了问题，应该重新划分类的职责。如果是老的项目，则可以按照其他小伙伴给出的解决方式。最好的解决方案还是看官方文档：链接在这里https:&#47;&#47;docs.spring.io&#47;spring&#47;docs&#47;current&#47;spring-framework-reference&#47;core.html#beans
Circular dependencies
If you use predominantly constructor injection, it is possible to create an unresolvable circular dependency scenario.

For example: Class A requires an instance of class B through constructor injection, and class B requires an instance of class A through constructor injection. If you configure beans for classes A and B to be injected into each other, the Spring IoC container detects this circular reference at runtime, and throws a BeanCurrentlyInCreationException.

One possible solution is to edit the source code of some classes to be configured by setters rather than constructors. Alternatively, avoid constructor injection and use setter injection only. In other words, although it is not recommended, you can configure circular dependencies with setter injection.

Unlike the typical case (with no circular dependencies), a circular dependency between bean A and bean B forces one of the beans to be injected into the other prior to being fully initialized itself (a classic chicken-and-egg scenario).</div>2020-02-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/1b/41/dbb7d785.jpg" width="30px"><span>xk_</span> 👍（4） 💬（5）<div>回答一下课后题：
首先，我们不用spring创建对象去思考一下：
1.构造函数是不可能存在循环依赖的，因为作为参数依赖的对象必须提前存在，参数的创建也需要参数，所以不存在。
2.setter注入，A依赖B，B依赖A，只要最后形成闭环，就不会报错。
3. setter注入，创建A需要B，创建B需要新的A，创建新的A需要新的B…如此循环下去就会栈溢出了。

spring也正好是这样实现的。
对于第二点，spring是用三级缓存来实现的。</div>2020-04-04</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/bFOAzic4EYicm2U3mdHKl67uceibPpgM7QBC8nAGdMCC6PCiamolNIfw9rstzGCEBNiaIWkianFG28VZzOggcehkMic5A/132" width="30px"><span>Geek_d1f952</span> 👍（3） 💬（0）<div>看着有点懵 这一讲对其他语言的同学不是很友好啊</div>2022-05-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f3/5c/8704e784.jpg" width="30px"><span>change</span> 👍（3） 💬（1）<div>工厂模式与DI容器
1、DI容器相当于一个大的工厂类,负责在程序启动,根据配置参数将所需要的对象都创建好,当程序需要时,直接从容器中获取某类对象;
2、工厂类只负责创建某一个或某一组类对象,而DI容器是创建整个应用所有需要的类对象
DI容器的基本功能
1、读取配置文件:配置文件中包含要创建的类对象及创建类对象的必要信息(使用那个构造函数及构造函数的参数列表);
2、创建对象:利用反射机制,动态加载类、创建对象;
3、对象生命周期管理:每次获取都返回新创建的对象(prototype)和每次获取都返回同一个事先创建好的对象(singleton,即单例对象),在单例对象中,还区分是否在程序启动时创建还是需要时创建(init-lazy);
DI容器接口设计
1、BeanConfigParser:解析配置文件
2、BeanFactory:根据解析配置的结果来创建对象;
1、ApplicationContext:DI容器内的上帝类(组装BeanFactory和ConfigParser),也是对外的接口;</div>2020-03-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/cb/38/4c9cfdf4.jpg" width="30px"><span>谢小路</span> 👍（2） 💬（2）<div>羡慕这些学 Java 的，看的清清楚楚，你问问没接触 Java 看的累不？</div>2022-04-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/5f/d5/2fec2911.jpg" width="30px"><span>yu</span> 👍（2） 💬（0）<div>学习spring的时候老师讲过，当时就是背了一下，知道有这么回事儿，这回算是知道了来龙去脉</div>2020-02-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/d7/ab/15c9b94e.jpg" width="30px"><span>Pluto</span> 👍（1） 💬（1）<div>看了留言有些感慨，@Autowired 是什么注入方式？这种方式的循环依赖 Spring 可以自动解决吗？如果可以，哪种场景下可以解决？如果不行，哪种场景下不能解决？真的踩过坑的人才懂</div>2020-05-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/e0/d7/744bd8c3.jpg" width="30px"><span>空白昵称</span> 👍（1） 💬（1）<div>作为一个swifter，我竟然也看懂了这里的demo实例代码。阅读java的能力果然在逐步提高。
关于练习部分，如果单例在创建时发生了环依赖，这时一定是错误的、此时就要检查配置了。如果是非单例参数依赖，个人感觉这里依赖关系设计应该趋向于树的形状，而非设计成有向图。如果发现依赖关系是图的形状，应该考虑调整整体实现代码架构了。不知道我理解对不对。
希望各位大神多多指点🙏</div>2020-03-18</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKZ16iaIia0029oI1Qh5NicibpbTiaBAaCOPYXoLplKHr6uQ2rSVxPZanBvpMcL2NuhwKQYCFnaHP5tedQ/132" width="30px"><span>FIGNT</span> 👍（1） 💬（1）<div>这个争哥的数据结构与算法之美的递归有答案。对象依赖个数可以限制个大小，递归时如果超过该深度就报错。可能有更好的方式，期待老师的答案</div>2020-02-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8a/02/828938c9.jpg" width="30px"><span>Frank</span> 👍（1） 💬（0）<div>什么场景下使用工厂模式判断依据为：当创建对象是一个“大工程”时，一般使用工厂模式来实现，将对象的复杂逻辑封装起来，实现对象的创建和使用分离，使得代码结构更加清晰，类的职责更加单一，也体现了依赖反转原则。“大工程”的判断依据有两个：创建过程涉及复杂的if-else逻辑判断和对象创建需要组装多个其他类对象或者需要复杂的初始化过程。
Spring的IOC容器就是一个典型的工厂，当我们需要Bean时，只要正确的配置了对象创建需要的规则，他们通过IOC容器提供的接口就可以获取对象，实现了控制反转。
对于课堂讨论：会出现堆栈溢出StackOverflowError异常。</div>2020-02-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/16/5b/83a35681.jpg" width="30px"><span>Monday</span> 👍（1） 💬（0）<div>思考题：
1、如果循环依赖的类都是SINGLETON，不会出现堆栈溢出
2、如果循环依赖的类都是PROTOTYPE，本章的代码来看，的确会出现堆栈溢出；解决办法，可以做递归的深度控制。</div>2020-02-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2d/06/a5/0245a2a8.jpg" width="30px"><span>Ben土豆</span> 👍（0） 💬（0）<div>createBean() 的递归逻辑会如果有循环依赖的确会产生栈溢出问题，springboot是通过加入缓存来实现，如果不考虑AOP代理问题的话，使用二级缓存可以解决这个问题，否则需要三级缓存。一级缓存中保存递归中初始化全部完成的bean,二级缓存保存半成品bean,当createBean出现循环依赖时，可以直接在半成品二级缓存中取出依赖bean进行填充。
循环依赖问题可以解决的前提：
1. Bean不是多例，必须是单例，否则每一次createBean()需要创建一个新的object，缓存便不可行
2. 循环依赖必须是setter注入，而非构造器注入，构造器注入在new创建时就会抛出异常</div>2023-04-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/00/d2/d94c4858.jpg" width="30px"><span>iRex</span> 👍（0） 💬（0）<div>BeanDefinition refBeanDefinition = beanDefinitions.get(arg.getArg()); 这个地方get不到吧，key不是id吗</div>2022-11-16</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/90DWsNicbNLJqRBLXWgM0t7AomqD4UpNnGFtkw4CorUg27tfuPfDiaImEMQkesCzzmFNicCPwHtYFjQ16Alf2fxjQ/132" width="30px"><span>小学生的大铁锤</span> 👍（0） 💬（0）<div>通过spring IOC容器讲解了工厂方法模式的应用，明白了通过工厂方法模式隔离变化，隔离复杂的基本处理流程和效果。</div>2022-07-23</li><br/>
</ul>