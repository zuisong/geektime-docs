你好，我是郭屹，今天我们继续手写MiniSpring，探讨Bean的依赖注入。

上节课，我们定义了在XML配置文件中使用setter注入和构造器注入的配置方式，但同时也留下了一个悬念：这些配置是如何生效的呢？

## 值的注入

要理清这个问题，我们要先来看看**Spring是如何解析 `<property>` 和 `<constructor-arg>` 标签。**

我们以下面的XML配置为基准进行学习。

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<beans>
    <bean id="aservice" class="com.minis.test.AServiceImpl">
        <constructor-arg type="String" name="name" value="abc"/>
        <constructor-arg type="int" name="level" value="3"/>
        <property type="String" name="property1" value="Someone says"/>
        <property type="String" name="property2" value="Hello World!"/>
    </bean>
</beans>
```
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/54/9a/76c0af70.jpg" width="30px"><span>每天晒白牙</span> 👍（32） 💬（3）<div>回复BattleMan1994

老师这个用了两个缓存，spring多一个创建bean实例工厂缓存，详细如下


三级缓存机制包括以下三个缓存：

1. singletonObjects：用于存储完全创建好的单例bean实例。

2. earlySingletonObjects：用于存储早期创建但未完成初始化的单例bean实例。即老师说的毛坯

3. singletonFactories：用于存储创建单例bean实例的工厂对象。

当Spring发现两个或更多个bean之间存在循环依赖关系时，它会将其中一个bean创建的过程中尚未完成的实例放入earlySingletonObjects缓存中，然后将创建该bean的工厂对象放入singletonFactories缓存中。接着，Spring会暂停当前bean的创建过程，去创建它所依赖的bean。当依赖的bean创建完成后，Spring会将其放入singletonObjects缓存中，并使用它来完成当前bean的创建过程。在创建当前bean的过程中，如果发现它还依赖其他的bean，Spring会重复上述过程，直到所有bean的创建过程都完成为止。

需要注意的是，当使用构造函数注入方式时，循环依赖是无法解决的。因为在创建bean时，必须先创建它所依赖的bean实例，而构造函数注入方式需要在创建bean实例时就将依赖的bean实例传入构造函数中。如果依赖的bean实例尚未创建完成，就无法将其传入构造函数中，从而导致循环依赖无法解决。此时，可以考虑使用setter注入方式来解决循环依赖问题。</div>2023-03-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/33/0b/fd18c8ab.jpg" width="30px"><span>大胖子呀、</span> 👍（13） 💬（1）<div>个人感觉循环依赖是一种非常糟糕的设计，往往意味着写出这段代码的程序员没有理清层级关系，没有设计好上下层的依赖，是一种非常明显的坏味道。
Spring对于循环依赖的支持，反而导致了程序员写出了坏味道代码而不自知，或许从一开始Spring就不该支持循环依赖。
所以Spring官方也建议大家使用构造器注入，一个是避免写出这种层级依赖不清晰的糟糕代码，二是也方便了后续单元测试的编写。</div>2023-04-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/54/9a/76c0af70.jpg" width="30px"><span>每天晒白牙</span> 👍（10） 💬（3）<div>思考题
Spring支持一个Bean构造器注入另一个Bean，工作中也都是尽量通过构造器注入，有很多优点

通过属性注入的方式能解决循环依赖的问题，原理是通过缓存的方式解决的，这里的关键点是属性注入是在bean创建后注入的

而构造器注入不能解决循环依赖问题
因为需要在创建bean时就需要将依赖的bean传入到构造函数中，如果依赖的bean尚未创建完成，就不能传入到构造函数中，循环依赖就不能解决</div>2023-03-17</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/XWv3mvIFORNgRk9wF8QLb9aXfh1Uz1hADtUmlFwQJVxIzhBf8HWc4QqU7iaTzj8wB5p5QJLRAvlQNrOqXtrg1Og/132" width="30px"><span>Geek_320730</span> 👍（9） 💬（1）<div>loadBeanDefinitions结束的时候会registerBeanDefinition，看代码中registerBeanDefinition又会根据这个Bean是否是单例来判断要不要getBean。如果getBean的话：如果这个Bean有依赖的Bean,会继续getBean,如果xml中 这个被依赖的Bean定义在这个Bean后面，那么后面被依赖的Bean的BeanDefintion还没有被loadBeanDefinitions，createBean的时候就会报错。</div>2023-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/2a/b8/dc924db4.jpg" width="30px"><span>木  昜</span> 👍（5） 💬（2）<div>您好，目前所写的逻辑是加载一个BeanDefinition，然后放入Map，同时判断是否为懒加载，不是的话就创建该bean，然后加载下一个bean定义。
如果xml在a的bean定义在b之前，并且a依赖了b。
此时 加载a的定义，创建a，发现a依赖b，就去getBean（b），但是此时b的定义还没有加载进map，就会抛出异常。
是否可以改为加载完全部的bean定义之后再进行bean的创建。把两步骤分开？</div>2023-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/8b/4b/15ab499a.jpg" width="30px"><span>风轻扬</span> 👍（4） 💬（1）<div>老师，我看其他同学提了这个问题。就是如果xml中A定义在前，依赖B，但是B定义在后。此时会因为beanDefinitionMap中不存在beanDefinition而报错。我看您给你的解决方案是先将beanDefinition对象一次性全部加载完成。那是不是将SimpleBeanFactory类中的方法registerBeanDefinition中的以下逻辑去掉就可以了。
if (!bd.isLazyInit()) {
            getBean(name);
        }
我试了试，这样是ok的，因为ClassPathXmlApplicationContext中的refresh方法会执行到getBean</div>2023-03-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/00/48/55932a4c.jpg" width="30px"><span>追梦</span> 👍（3） 💬（2）<div>老师好，这个反射构造器和反射setXXX()方法这样写有点硬编码的味道，有没有简洁的写法，如何不硬编码解决基本类型的反射问题</div>2023-03-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/f1/4a/bcba0456.jpg" width="30px"><span>康Geek</span> 👍（2） 💬（1）<div>文稿中 ClassPathXmlApplicationContext 这个类的构造方法中 isRefresh 有个错误：
if (!isRefresh) { this.beanFactory.refresh(); } 这个 if 的条件中时取反的，但是在老师 github 仓库中 geek_ioc3 分支的 ClassPathXmlApplicationContext.java 构造方法中是没有取反的：
if (isRefresh) { this.beanFactory.refresh();}
</div>2023-04-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/9f/12/58b5609f.jpg" width="30px"><span>塵</span> 👍（2） 💬（3）<div>createBean从哪里冒出来的，上面的课程里面SimpleBeanFactory类里没有看到</div>2023-04-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2e/da/09/a0359f6b.jpg" width="30px"><span>Jackwey</span> 👍（1） 💬（2）<div>老师，Cbean依赖的是A的毛坯实例，那A的属性岂不是没有被Cbean依赖了？</div>2023-06-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/8b/06/fb3be14a.jpg" width="30px"><span>TableBear</span> 👍（1） 💬（1）<div>思考题回答：
在Spring中Bean构造器注入另一个Bean是支持，但是看上面MinSpring的实现好像不支持。
但是，Bean构造器注入没法用earlySingletonObjects解决循环依赖。
不知道正不正确😂</div>2023-03-17</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/mfZXPlpx5a7Y3oAWlpFJQxLwlQG2cVEdQ15cNibHEMxQRYlKZVRaGich4uCz9S64kK4UfjU3DBtXn3wVxp6icFBog/132" width="30px"><span>Geek_94fbda</span> 👍（0） 💬（1）<div>BeanDefinition 里面要把lazyInit 的值改成True，这个在文章里没有提到。 否则的话是运行不了的</div>2024-02-02</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/mfZXPlpx5a7Y3oAWlpFJQxLwlQG2cVEdQ15cNibHEMxQRYlKZVRaGich4uCz9S64kK4UfjU3DBtXn3wVxp6icFBog/132" width="30px"><span>Geek_94fbda</span> 👍（0） 💬（1）<div>else { &#47;&#47;is ref, create the dependent beans
    				try {
						paramTypes[0] = Class.forName(pType);
					} catch (ClassNotFoundException e) {
						e.printStackTrace();
					}
    				try {
						paramValues[0] = getBean((String)pValue);
					} catch (BeansException e) {
						e.printStackTrace();
					}
    			}
isRef的类定义 是没有value这个值 的那pValue不是null么？</div>2024-02-01</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJhxtIyXX4icMNAq5zEvchKYS3q7fwZXA3h7yV80iaibCRXniaLW95OnPC8PM2h5Ja5ibpkJ1VJowicqKZA/132" width="30px"><span>Geek_7jwpfc</span> 👍（0） 💬（1）<div>老师写的很清晰，让我对spring有了更清楚的认识了，但是spring为什么要有第三个缓存，我还是没明白！别人博客解释，是代理的对象的原因，需要三级缓存；我的疑惑是，把代理对象直接放入第一个缓存中，不就行了吗？</div>2023-05-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/d1/17/5f525662.jpg" width="30px"><span>Robert Tsai</span> 👍（0） 💬（1）<div>其实解决循环依赖的问题，就是一个办法：把创建bean的过程分成两阶段，第一阶段是一个毛胚的bean，第二阶段补齐属性。所有的毛胚bean都是提前创建出来的，后面面对循环依赖的时候，拿到的是这个提前准备好的毛胚bean。
---
老师，我对这个过程还有一点不解。ABean 依赖 BBean，BBean 又依赖 CBean，而 CBean 反过来还要依赖 ABean，此时CBean拿到的却是毛坯的“ABean”，但是拿到这个毛坯Bean其实并不影响整体ABean的创建，因为最终完成创建后，从IOC中getBean()时候就是一个完成的ABean。不知理解是否正确？</div>2023-05-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/71/4c/50718389.jpg" width="30px"><span>人老实话不多</span> 👍（0） 💬（1）<div>在属性注入之前，我们不能都把用到的Bean实例化吗？反正都是单例的，到最后所有的属性都会赋完值的，是吧老师？这样会有什么问题吗？还是说这样违背了Spring管理Bean生命周期的理念？</div>2023-04-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/9f/14/b9505789.jpg" width="30px"><span>彬清</span> 👍（0） 💬（1）<div>完全创建好bean后，没有把毛胚bean从earlySingletonObjects中移出？</div>2023-04-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/9a/a6/29ac6f6a.jpg" width="30px"><span>XXG</span> 👍（0） 💬（1）<div>问题：Spring Bean支持循环依赖吗

From ChatGPT：Spring Bean支持循环依赖，但是只支持Singleton的setter循环依赖，即@Autowired形式，不支持构造器注入的循环依赖。如果存在循环依赖A -&gt; B -&gt; A，且都是通过构造函数依赖的，无法支持循环依赖。如果是prototype作用域的bean，则Spring是不支持相关的循环依赖的。</div>2023-03-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/b1/d0/8c94d49e.jpg" width="30px"><span>未聞花名</span> 👍（0） 💬（1）<div>构造器注入不能解决循环依赖，因为缺失bean，对象在实例化就会失败，setter方法可以成功在于先有对象，属性是循环依赖中对方的引用，可以是不完全赋值的对象，也就是文章中的毛坯。

public ClassPathXmlApplicationContext(String fileName, boolean isRefresh)
老师，这里为什么要判断isRefresh，理论上容器只会启动一次吧，不太明白为什么这么设计。</div>2023-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a6/56/abb7bfe3.jpg" width="30px"><span>云韵</span> 👍（0） 💬（1）<div>老师 这个代码对应分支是哪个 拉下代码来 没找到对应的分支</div>2023-03-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/0b/5a/453ad411.jpg" width="30px"><span>C.</span> 👍（0） 💬（1）<div>getBean那个地方，为什么要用pValue?xml 里对应的property 里只有type和ref没有value啊？有点不理解。</div>2023-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（1）<div>前几天看文章，今天看代码，有一个问题请老师指教：
 ioc2目录，有一个问题：
接口BeanFactory中，有多个方法，其中方法getBean有红色下划线，提示“Overridden methods are not annotated with @Override”。
类SimpleBeanFactory中，方法getBean有红色下划线，错误提示：“missing @Overrid annotation on getBean”。不过Test1.java中的main方法能正常运行。

接口BeanFactory中有一个方法getType，此方法在SimpleBeanFactory中的实现函数加了@Override。
请问：
1 getType方法加了@Override，而getBean方法没有加，为什么？忘记加了吗？
2 继承接口，实现接口中的方法，我记得是不用加@Override，现在提示错误，为什么？
    是因为不同的JDK版本或编译器版本吗？</div>2023-03-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/36/6f/4e/791d0f5e.jpg" width="30px"><span>浅行</span> 👍（0） 💬（1）<div>```Java
 PropertyValue propertyValue = propertyValues.getPropertyValueList().get(i);                String pType = propertyValue.getType();                String pName = propertyValue.getName();                Object pValue = propertyValue.getValue();                Class&lt;?&gt;[] paramTypes = new Class&lt;?&gt;[1];               if (&quot;String&quot;.equals(pType) || &quot;java.lang.String&quot;.equals(pType)) {                    paramTypes[0] = String.class;                } else if (&quot;Integer&quot;.equals(pType) || &quot;java.lang.Integer&quot;.equals(pType)) {                    paramTypes[0] = Integer.class;                } else if (&quot;int&quot;.equals(pType)) {                    paramTypes[0] = int.class;                } else { &#47;&#47; 默认为string                    paramTypes[0] = String.class;                }                Object[] paramValues = new Object[1];                paramValues[0] = pValue;
```
这一段代码测试的时候发现，如果`AsServiceImpl`里面写了个set方法参数是Integer类型的，会报错`argument type mismatch`。 需要和构造器一样处理，每一种类型都要单独转换。</div>2023-03-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（2）<div>IoC等于“依赖注入”吗？从文中的描述，好像老师是认为这两个概念是一回事，是描述同一个东西，而且“依赖注入”比“IoC”更贴切。我很早以前学过这两个概念，当时好像是把这两个术语当做不同的概念来理解的。</div>2023-03-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/53/dc/11615706.jpg" width="30px"><span>BattleMan1994</span> 👍（0） 💬（3）<div>为什么老师这里用一个缓存就可以解决循环依赖，而Spring却要用三级缓存呢？看很多博客都有点似懂非懂</div>2023-03-17</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q3auHgzwzM6mTy6lgnhkKbaWfs1s0siazVLQFnNmU0YLsRsxyC84aoFP5icuo22qricS62EiaibmVdplmtPbwryHHTA/132" width="30px"><span>Geek_5d0074</span> 👍（0） 💬（6）<div>Spring中的循环依赖，实际工作中真的会用到吗？好多面试题都说这个，但是没有一个能讲明白。每个答案都不同</div>2023-03-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/0c/4c/2bbb7c9e.jpg" width="30px"><span>读多多</span> 👍（0） 💬（0）<div>有个问题，按照这样执行构造器方式注入时，xml的构造器参数的顺序必须要和构造器的参数顺序一致吧？</div>2024-12-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/3b/75/0b/8a22f70d.jpg" width="30px"><span>楚风</span> 👍（0） 💬（0）<div>在本地课程的Demo工程中存在两个问题：
1. 依赖问题。即：ABean 依赖BBean, 但是在xml中优先配置的是ABean,则存在报错!
2. 循环依赖问题。即： ABean依赖BBean, 但是BBean又依赖ABean, 同样会报错!

不过解决的方法都殊途同归。只需要在原有Demo的基础上做一点点小的改动即可! (改动思路如本文中所描述的，优先构造毛坯实例，再对该实例中的Property属性进行初始化即可)

改动点如下：
1. 屏蔽SimpleBeanFactory::registerBeanDefinition()方法中对createBean()方法的调用, 其registerBeanDefinition()方法仅实现本方法应该实现的内容,即BeanDefinition的注册;

2. 修改SimpleBeanFactory::createBean(), 使其依次按照如下步骤进行：
     1) 调用doCreateBean() 创建毛坯实例;
     2) 从BeanDefinition中获取该Bean的dependsOn(依赖Bean), 并依次创建依赖Bean的毛坯实例;
     3) 调用handleProperties()方法对毛坯实例的Property属性进行初始化;

说明：上面方案并不能解决通过构造函数进行子对象(依赖Bean)的初始化的场景!!!</div>2024-05-27</li><br/><li><img src="" width="30px"><span>edward</span> 👍（0） 💬（0）<div>请问老师 构造器参数和属性参数中的Integer和int这2种类型可以不区分 一起处理吗？</div>2024-05-19</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJhxtIyXX4icMNAq5zEvchKYS3q7fwZXA3h7yV80iaibCRXniaLW95OnPC8PM2h5Ja5ibpkJ1VJowicqKZA/132" width="30px"><span>Geek_7jwpfc</span> 👍（0） 💬（0）<div> BaseBaseService这个类，如果属性是Aservice，是一个接口的话，会在SimpleBeanFactory#handleProperties()的method = clz.getMethod(methodName, paramTypes)这行，改成实际的类就行; 
不过不算什么大问题，这门课重点是spring的思路；</div>2023-05-21</li><br/>
</ul>