你好，我是郭屹。

上节课我们通过一系列的操作使XML使配置文件生效，然后实现了Spring中Bean的构造器注入与setter注入，通过引入“早期毛胚Bean”的概念解决了循环依赖的问题，我们还为容器增加了Spring中的一个核心方法refresh()，作为整个容器启动的入口。现在我们的容器已经初具模型了，那如何让它变得更强大，从种子长成一株幼苗呢？

这节课我们就来实现一个增强版的IoC容器，支持通过注解的方式进行依赖注入。注解是我们在编程中常用的技术，可以减少配置文件的内容，便于管理的同时还能提高开发效率。所以这节课我们将**实现Autowired注解，并用这个方式进行依赖注入**。

## 目录结构

我们手写MiniSpring的目的是更好地学习Spring。因此，我们会时不时回头来整理整个项目的目录结构，和Spring保持一致。

现在我们先参考Spring框架的结构，来调整我们的项目结构，在beans目录下新增factory目录，factory目录中则新增xml、support、config与annotation四个目录。

```java
├── beans
│   └── factory
│       ├── xml
│       └── support
│       └── config
│       └── annotation
```
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/36/95/73/1978ddde.jpg" width="30px"><span>一念之间</span> 👍（4） 💬（1）<div>有一个简单的问题 为什么处理器要叫做PostProcessor呢？ 这里的post到底是对于什么动作而言的呢？</div>2023-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/ba/b4/281eb9d0.jpg" width="30px"><span>三太子</span> 👍（4） 💬（1）<div>https:&#47;&#47;github.com&#47;yx-Yaoxaing&#47;minispring&#47;wiki&#47;%E5%85%B3%E4%BA%8Emini-spring
自己写的代码提到github上  每日打卡！ 遇到的基础问题 都写在了wiki</div>2023-03-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/70/79/bb591140.jpg" width="30px"><span>睿智的仓鼠</span> 👍（4） 💬（1）<div>通过这节课真的是感受到Spring设计的巧妙之处了，我目前的理解是，解耦分为两种：设计上的解耦、实现类上的解耦。通过抽取AbstractBeanFactory，把BeanPostProcessor的设计与BeanFactory本身解耦，AutowireCapableBeanFactory再通过定义BeanPostProcessor接口类型的属性，向外提供属性设置的方法，做到了和BeanPostProcessor实现类的解耦，最后在ClassPathXmlApplicationContext中统一注册BeanPostProcessor，再抽取成一个启动方法，非常优雅。AbstractBeanFactory的“接口抽象类”思想也很巧妙。这些思想在学Spring源码时早已听说，当时只觉得这样设计是灵活的，但不知道具体灵活在何处，通过自己手写实现下来真的是越来越清晰了，实属好课！</div>2023-03-21</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJhxtIyXX4icMNAq5zEvchKYS3q7fwZXA3h7yV80iaibCRXniaLW95OnPC8PM2h5Ja5ibpkJ1VJowicqKZA/132" width="30px"><span>Geek_7jwpfc</span> 👍（3） 💬（2）<div>老师：
1. Autowire注入对象B，此时B的beanDefinnition还没有加载进来,会报错！设置lazy = ture 也不行，只能把if( !beanDefinition.isLazyInit() )注释掉, 还有其它方法吗！
2.AutowiredAnnotationBeanPostProcessor#postProcessBeforeInitialization()方法：
                    String fieldName = field.getName();
                    Object autowiredObj = this.getBeanFactory().getBean(fieldName);
这段代码，类的属性字段名要和xml配置的beanId相同，否则找不到！

</div>2023-05-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/14/45/adf079ae.jpg" width="30px"><span>杨松</span> 👍（3） 💬（4）<div>老师，请教下关于AutowiredAnnotationBeanPostProcessor的时机问题，为什么不是在处理属性handleProperties的位置，这个方法正好是设置bean实例的属性啊，我一直没弄懂为啥不放在这里？</div>2023-04-14</li><br/><li><img src="" width="30px"><span>马儿</span> 👍（3） 💬（1）<div>ClassPathXmlApplicationContext增加了一个BeanFactoryPostProcessor属性，本文中没有给出定义，看了GitHub源码把这个类拷贝出来。这个类的作用是什么呢？是像对BeanPostProcessor一样对BeanFactory进行特殊处理的吗？</div>2023-03-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/59/c9/f44cb7f3.jpg" width="30px"><span>爪哇夜未眠</span> 👍（2） 💬（2）<div>文章里的代码，AbstractBeanFactory.doCreateBean()方法里，if (!constructorArgumentValues.isEmpty()) 后面少了一个else，里面是无参构造方法创建对象
else {
    obj = clz.newInstance();
}</div>2023-06-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/85/ce/df1c7a91.jpg" width="30px"><span>陈小远</span> 👍（2） 💬（3）<div>跟到第四节了，单纯看文章逻辑来说还能理解一些实现，但是结合github上的源码（对照的是ioc4分支，不知道是否找对），发现源码和文章逻辑叙述的时候同一个类贴的代码实现是不一样的，导致对照学习的时候产生混乱。比如源码中AutowireCapableBeanFactory是直接实现的BeanFactory，但在文章的表述中是继承的AbstractBeanFactory，由此就在此节无法对照源码和文章表述自我参照着来完成注解的功能。看了四节后说说自己的一些看法或观点：
1、源码在github上，因为不是整个分支全克隆下来学习，单独的点击查看某个类的代码比较慢，影响学习效率，如果码云上有学习地址可能会好很多；
2、文章代码和源码不一致的问题不知道是跳跃太大还是个人没找对位置，很多人可能会渐渐的迷乱从而无法继续跟进学习；
3、源码相对于文章来说跳跃性比较大，如果正文中没法完全交代清楚，建议在源码的readme文件尽可能详细的给出一些突然出现的类的说明和设计意图

总的来说，通过老师的引导，再结合Spring的源码，还是有那么点感觉的，不过今天这节课实在没跟下来，可能还需要多花点时间自己琢磨琢磨</div>2023-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7d/b6/abdebdeb.jpg" width="30px"><span>Michael</span> 👍（1） 💬（1）<div>想请教一下老师，那现在是不是SimpleBeanFactory完全没用了？</div>2023-04-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/8b/4b/15ab499a.jpg" width="30px"><span>风轻扬</span> 👍（1） 💬（3）<div>老师，有几个问题请教一下。
1、AutowireCapableBeanFactory类中的addBeanPostProcessor为什么要先remove再add呢？
2、代码里出现异常的时候，老师都是只写一个try，这貌似不行吧，我是java8，这是高版本jdk的新特性吗？
3、AutowireCapableBeanFactory类中的invokeInitMethod方法，您的代码逻辑中，获取Class对象用的是BeanDefinition.getClass()，我理解，应该用Class.forName(BeanDefinition.getClassName())，init方法应该是我们业务类上定义的init方法吧？</div>2023-03-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/14/45/adf079ae.jpg" width="30px"><span>杨松</span> 👍（0） 💬（1）<div>老师请教下，包factory.support和包factory.config划分上有什么依据，不太明白为什么这么划分</div>2023-04-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/41/4d/f6d6d13a.jpg" width="30px"><span>啊良梓是我</span> 👍（0） 💬（3）<div>```
@Override public void registerBeanDefinition(String name, BeanDefinition beanDefinition) { this.beanDefinitionMap.put(name, beanDefinition); this.beanDefinitionNames.add(name); if (!beanDefinition.isLazyInit()) { try { getBean(name); } } }

```
这里我有个问题，就是这个如果在设置BeanDefinition的时候，执行getBean方法，但是如果Bean里面注入了第三方Bean，这时候，有可能这个第三方Bean的BeanDefinition还没有实例化的，很明显不能循环注入Bean的啊？这个应该怎么处理的呢？延迟等待？或者说主动去遍历Resource接口获取资源，当也拿不到的时候，直接报编译器异常？</div>2023-04-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/00/48/55932a4c.jpg" width="30px"><span>追梦</span> 👍（0） 💬（1）<div>老师好，您说在beans.xml配置的bean别名和被@Autowire修饰的属性名必须一样，但是我觉得这样不够完整，我使用了@Autowire自然是希望所有该类型都被注入无论其属性名是什么，我想记录一个属性值映射signleton的hashMap对象来存储，老师觉得这个思路怎么样？或者老师有什么其他看法嘛对于文件中bean的别名和属性名必须相同</div>2023-03-31</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKDfO7wKibzpw4YsoqLRCHUKxX4rYRUh7m7RCdOwzWVaN9QLlhcU5ho3w2Qcpib1O69YPj65ib07xQBQ/132" width="30px"><span>努力呼吸</span> 👍（0） 💬（1）<div>老师，为什么beanDefinitionMap是线程安全的容器；beanDefinitionNames和earlySingletonObject不需要呢？</div>2023-03-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/31/45/3f/e4fc2781.jpg" width="30px"><span>梦某人</span> 👍（0） 💬（2）<div>个人实现地址如下：https:&#47;&#47;github.com&#47;DDreame&#47;myMiniSpring
欢迎其他同学参考以及 Star，根据 Commit history 查看我根据课程内容分割的实现过程。
提问1: applyBeanPostProcessorAfterInitialization 方法在 AbstractFactory 中存在了返回值，有什么存在的必要性，但是， obj 作为一个引用对象，需要返回吗？ 在 AbstractFactory 中也并没有使用到其返回值。（另外方法如果直接为 void 依然有效，我已经测试过。）
提问2: AbstractFactory 这个似乎过于单例了？ 可能是因为 mini 实现的原因？ 因为目前的 AbstractFactory 基本等于修改了 SimpleSingletonFactory。
提问3: 关于 Factory 的 Refres 问题，当我在 ClassPathXmlApplicationContent 的 refresh() 方法中，在 注册前后处理器之前进行了 Refresh, 就会导致 Autowired 无法成功注入，这是因为实例已经建立好了吗？ 那如果想修复这个问题，老师能否提供一定的思路？比如，在 getBean 的时候做一遍属性检查吗？（当然有可能是我个人实现的问题）
由于没看源码，是按照老师给出的代码和讲解实现的，所以可能存在一定理解偏差，希望老师指正一下。

关于课后题：
可以实现，这部分在 Processor 部分进行了解耦合，只要实现相关注解的 Processor，并在 Context 中进行加载，即可。</div>2023-03-29</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/XWv3mvIFORNgRk9wF8QLb9aXfh1Uz1hADtUmlFwQJVxIzhBf8HWc4QqU7iaTzj8wB5p5QJLRAvlQNrOqXtrg1Og/132" width="30px"><span>Geek_320730</span> 👍（0） 💬（1）<div>1.invokeInitMethod(BeanDefinition bd, Object obj) 中 master分支是用的obj.getObject(),ioc4分支中是bd.getObject(),应该是obj.getObject()
2.循环调用postProcessBeforeInitialization或postProcessAfterInitialization那一块,好像是返回的bean为null的时候，中断这个循环调用，返回上次调用结果？是不是应该在调用之前先用另一个变量暂存一下，返回值为null的时候，return变量？按代码逻辑会return null，这样的话，后续应该会空指针异常吧。。。</div>2023-03-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/c0/df/d52e7244.jpg" width="30px"><span>聪聪不匆匆</span> 👍（0） 💬（1）<div>第四节github上面ioc4 branch分支代码 和 文档中相差还是较大的。比如DefaultListableBeanFactory 类文档中并没有提到。再比如ClassPathXmlApplicationContext类中构造函数使用的是AutowireCapableBeanFactory类，但是在github中确是DefaultListableBeanFactory类，这个类怎么来的、什么用处、怎么演进的并没有地方提现到。诸如此类，github中在本次分支中多出来了很多类都在文档中未曾提到。</div>2023-03-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/8b/4b/15ab499a.jpg" width="30px"><span>风轻扬</span> 👍（0） 💬（1）<div>刚学了这么几节课，感觉就收获很大，代码手敲一遍，体会更深。有一个体会是：Spring的代码都是低耦合的，感觉低耦合的优势就是复用性强，扩展性强。扩展性方面，业务逻辑千变万化，Spring不能想到所有的业务情况，所以它就搞抽象，定标准。业务方可以根据自己的实际情况来实现标准，从而完成自己的个性化需求。这个思想很重要，工作中要注意用起来
之前也经常看Spring源码，但因为Spring源码太庞大了，只能先基于一个点看，这就导致无法从整体上了解Spring的运行机制。这门课正好就是从整体理解Spring。把之前学习的点串起来，不错。好课一枚，赞!</div>2023-03-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/80/0b/7ae52ac0.jpg" width="30px"><span>Unknown</span> 👍（0） 💬（1）<div>与spring的autowired byType注入不同，老师实现的autowired是根据beanName注入，所以AbstractBeanFactory里面的两个缓存Map key为小写类名。
测试用例那边是不是有点问题 不应该直接用bbs 应该是用basebaseservice 这样才能创建的到吧
</div>2023-03-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/0b/5a/453ad411.jpg" width="30px"><span>C.</span> 👍（0） 💬（1）<div>我有个疑问，就是为什么BeanDefinition的lazyInit都设置为true，默认懒加载，Spring中不都是默认false吗？</div>2023-03-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/0b/5a/453ad411.jpg" width="30px"><span>C.</span> 👍（0） 💬（2）<div>BeanDefinition这个类的懒加载lazyInit从ioc3版本开始变成了true,之前的false会导致导致AbstractBeanFactory这个类里    
public void registerBeanDefinition(String name, BeanDefinition beanDefinition) {
        this.beanDefinitionMap.put(name, beanDefinition);
        this.beanDefinitionNames.add(name);
        if (!beanDefinition.isLazyInit()) {
            try {
                getBean(name);
            } catch (BeansException e) {
                e.printStackTrace();
            }
        }
    }
getBean执行，导致beanDefinitionMap中bean的定义信息没加载完，导致的找不到bean的定义信息导致的No bean.</div>2023-03-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/36/71/d0/2ccddb0c.jpg" width="30px"><span>心中有花</span> 👍（0） 💬（1）<div>记录自己写错的点，只用了一个List&lt;String&gt; beanName,这个list，不需要在添加registerSingleton  singletons.put的时候再添加一遍，不然就会报错，继续加油，争取成功上岸</div>2023-03-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（2）<div>请教老师几个问题：
Q1：AbstractBeanFactory中，
earlySingletonObjects = new HashMap&lt;&gt;(16);，
如果16不够用，会自动扩展吗？印象中好像不会；如果不会，会发生什么？
Q2：除了名称匹配，还有什么匹配方法？
Q3：会存在两个BeanFactory吗？一个是AutowireCapableBeanFactory，保存有注解的，另外一个保存没有注解的。</div>2023-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/36/71/d0/2ccddb0c.jpg" width="30px"><span>心中有花</span> 👍（0） 💬（2）<div>老师想问下，被@Autowire修饰的类，它的name是什么时候放入AutowireCapableBeanFactory beanFactory; 的 ，我get不到，麻烦老师解答下 感谢</div>2023-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/36/71/d0/2ccddb0c.jpg" width="30px"><span>心中有花</span> 👍（0） 💬（1）<div>@Autowire 不是byType注入的吗？</div>2023-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/37/e6/96/e7f430c1.jpg" width="30px"><span>十画生</span> 👍（1） 💬（2）<div>老师，现阶段代码是不是没有解决autowired装配属性的循环依赖问题啊
</div>2023-07-17</li><br/><li><img src="" width="30px"><span>edward</span> 👍（0） 💬（0）<div>此外，handleProperties方法中的Class clz, Object obj 这2个参数的信息是不是冗余了？毕竟clz=obj.getClass()。</div>2024-06-28</li><br/><li><img src="" width="30px"><span>edward</span> 👍（0） 💬（0）<div>老师，为什么要有populateBean这个方法呢，直接用handleProperties方法不就好了吗？</div>2024-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/9e/3f/00109670.jpg" width="30px"><span>且将新火试新茶～</span> 👍（0） 💬（0）<div>打卡：https:&#47;&#47;github.com&#47;sugar-orange666&#47;MiniSpring</div>2024-04-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/37/99/02/791d0f5e.jpg" width="30px"><span>要叫秀妍呀</span> 👍（0） 💬（0）<div>老师好，在 AbstractBeanFactory 类中，handleProperties 方法中，分类型处理时没有把属性的 value 转换成对应的类型，这点是错误的吧。会导致后续在执行 setter 方法时，例如原本是一个 int 类型，传入的却是 String 类型， 这样的错误。

测试过程如下：
在 AServiceImpl 类中添加一个 private int age; 属性，在 beans.xml 文件中添加 &lt;property type=&quot;int&quot; name=&quot;age&quot; value=&quot;22&quot; &#47;&gt; 的标签。执行代码后，会报错 违法的参数(貌似是这个 IllegalMethodArgument) 的异常 

解决办法就是 handleProperties() 方法中添加把 String 类型转换成对应类型的代码，例如 int 类型中 paramValues[0]=Integer.valueOf((String) pValue);
</div>2023-09-08</li><br/>
</ul>