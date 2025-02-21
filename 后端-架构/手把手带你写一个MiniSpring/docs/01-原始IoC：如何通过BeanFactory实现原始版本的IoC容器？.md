你好，我是郭屹，从今天开始我们来学习手写MiniSpring。

这一章，我们将从一个最简单的程序开始，一步步堆积演化，最后实现Spring这一庞大框架的核心部分。这节课，我们就来构造第一个程序，也是最简单的一个程序，将最原始的IoC概念融入我们的框架之中，**我们就用这个原始的IoC容器来管理一个Bean。**不过要说的是，它虽然原始，却也是一个可以运行的IoC容器。

## IoC容器

如果你使用过Spring或者了解Spring框架，肯定会对IoC容器有所耳闻。它的意思是使用Bean容器管理一个个的Bean，最简单的Bean就是一个Java的业务对象。在Java中，创建一个对象最简单的方法就是使用 new 关键字。IoC容器，也就是**BeanFactory，存在的意义就是将创建对象与使用对象的业务代码解耦**，让业务开发人员无需关注底层对象（Bean）的构建和生命周期管理，专注于业务开发。

那我们可以先想一想，怎样实现Bean的管理呢？我建议你不要直接去参考Spring的实现，那是大树长成之后的模样，复杂而庞大，令人生畏。

作为一颗种子，它其实可以非常原始、非常简单。实际上我们只需要几个简单的部件：我们用一个部件来对应Bean内存的映像，一个定义在外面的Bean在内存中总是需要有一个映像的；一个XML reader 负责从外部XML文件获取Bean的配置，也就是说这些Bean是怎么声明的，我们可以写在一个外部文件里，然后我们用XML reader从外部文件中读取进来；我们还需要一个反射部件，负责加载Bean Class并且创建这个实例；创建实例之后，我们用一个Map来保存Bean的实例；最后我们提供一个getBean() 方法供外部使用。我们这个IoC容器就做好了。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/19/fd/58/1af629c7.jpg" width="30px"><span>6点无痛早起学习的和尚</span> 👍（37） 💬（2）<div>内容讲的很清晰，点赞。
这里有几个建议：
1. 每次代码设计之前，能否通过一个 UML 类图来表示，通过类图感觉更容易懂整个类与类之前的关系
2. 发现课程的内容还是有点偏向 Spring 那种感觉，就是有点类似：啊，Spring 是这样拆分几个类功能，那我们就这样拆分，这个方式感觉还是有点死板
感觉应该是：从一个设计者角度来讲，这样拆分更灵活，扩展性更强，叭叭叭等等，这样才能把读者带入进入课程，产生共鸣。

个人想法，欢迎交流，不知道是不是就我自己有这样感受，还是其他....</div>2023-03-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2e/1b/3c/9c5fc55f.jpg" width="30px"><span>姐姐</span> 👍（20） 💬（4）<div>从最初的简单ApplicationContext拆解成后面的复杂ApplicationContext，我理解起来还是有困难的，努力理解如下，大神勿喷：1 readxml方法从资源文件读取内容并存入beanDefinitions，这件事情有两个地方不确定，资源的来源不同、资源的格式不同，抽象的Resource的接口，它的不同子类从不同的来源读取，但是最终都是以Resource接口的形式提供给外部访问的，这样解决了第一个不确定来源的问题；但是resource接口中被迭代的object又是根据不同格式不同而不同的，element只是xml格式的，所以又定义了BeanDefinitionReader接口，它的不同子类可以读取不同格式的资源来形成beanDefinition 。 2 . instanceBeans方法取消了 。  3. getBean方法功能增强了，不仅是获得bean，对于未创建的bean还要创建bean  4 新的applicationContext负责组装，可以根据它的名字来体现它的组装功能，例如ClassPathXmlApplicationContext  它组装的Resource的实现类是ClassPathXmlResource  ，然后因为是xml的，所以需要BeanDefinitionReader的实现类XmlBeanDefinitionReader来读取并注册进beanFactory，同时ApplicationContext也提供了getBean底层调用beanfactory的实现，提供了registerBeanDefinition  来向底层的beanFactory注册bean。5 beanFactory 提供了registerBeanDefinition和getBean接口，这样无论是applicationContext还是beanDefinitionReader都可以向它注册beanDefinition，只要向它注册了，就可以调用它的getBean方法，我一直很纠结为什么不是beanfactory调用不同的beanDefinitionReader，写完这些，好像有点理解了，这样beanfactory就很专注自己的getBean方法，别的组件要怎么注入，它都不管了。</div>2023-03-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2d/7c/96/079a158d.jpg" width="30px"><span>adelyn</span> 👍（17） 💬（4）<div>请问会不会穿插讲一下用到的设计模式，单独学设计模式总是学不扎实，如果能讲到就太好了</div>2023-03-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/8b/4b/15ab499a.jpg" width="30px"><span>风轻扬</span> 👍（14） 💬（1）<div>说一下自己对思考题的理解。
控制反转。
控制：java对象创建的控制权。
反转：将java对象创建的控制权从程序员手中反转到IOC容器手中。
另外，说一下学完这一讲的感受。直白点说，很激动。我看过Spring这部分的源码，当时感觉挺简单的，并没有往深处想，其实忽略了“Spring为什么要这样写“的问题，现在感觉这才是源码的核心所在，突然有一点融会贯通的感觉，感觉很好。一直知道Spring的扩展性好，今天实实在在看到了。感谢老师传道解惑</div>2023-03-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/b1/d0/8c94d49e.jpg" width="30px"><span>未聞花名</span> 👍（9） 💬（1）<div>给老师个建议，可以点一下为什么类中要放这些属性和方法，突然抽到几个新类感觉过渡有点快，这样对之后自己去设计类也能举一反三，感觉自己平时设计不太好，如果自己实现起来的话比Spring的优雅可读性要差很多。
最后附上dom4j的maven依赖，希望帮助到其他人
```java
&lt;!-- https:&#47;&#47;mvnrepository.com&#47;artifact&#47;dom4j&#47;dom4j --&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;dom4j&lt;&#47;groupId&gt;
            &lt;artifactId&gt;dom4j&lt;&#47;artifactId&gt;
            &lt;version&gt;1.6.1&lt;&#47;version&gt;
        &lt;&#47;dependency&gt;
```</div>2023-03-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/14/45/adf079ae.jpg" width="30px"><span>杨松</span> 👍（8） 💬（3）<div>老师这句话没理解呢：“我们用一个部件来对应 Bean 内存的映像”，文中5边型图片对应的其他4个都能理解</div>2023-03-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/80/0b/7ae52ac0.jpg" width="30px"><span>Unknown</span> 👍（7） 💬（3）<div>getClass().getClassLoader().getResource(filepath)
类加载器获取资源时 此处的filepath 需要放在resource目录里面(手动创建并标识类型为Resource root) </div>2023-03-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/2b/f9/d65d8dfd.jpg" width="30px"><span>周润发</span> 👍（5） 💬（2）<div>首先很感谢老师的课程，内容值得细品。
想请教一个问题，为什么在代码中更多使用全局变量而不在方法中使用成员变量呢？有些全局变量只在某个方法会用到，有什么特别的考虑吗？</div>2023-03-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/0b/5a/453ad411.jpg" width="30px"><span>C.</span> 👍（4） 💬（2）<div>ioc容器5天的版本手敲的，对应章节的代码：https:&#47;&#47;github.com&#47;caozhenyuan&#47;mini-spring.git 点击分支查看对应章节的代码。帮大家跟敲不迷路。</div>2023-03-24</li><br/><li><img src="" width="30px"><span>马儿</span> 👍（4） 💬（1）<div>以前的spring的源码都是散的，希望能通过这个课把这些只是串联起来。希望老师讲的时候可以讲一些设计模式，把创建类所在的包也希望能够说明一下，这样的话更方便大家学习了解类的用途和作用。</div>2023-03-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/36/6f/4e/791d0f5e.jpg" width="30px"><span>浅行</span> 👍（3） 💬（4）<div>有两个问题想请教一下：
1. 请问SimpleBeanFactory 为什么是在getBean时才注册实例，而不是registerBeanDefinition就先注册呢？
2. 请问ClassPathXmlApplicationContext 为什么也要实现BeanFactory呢？</div>2023-03-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/bd/18/2af6bf4b.jpg" width="30px"><span>兔2🐰🍃</span> 👍（1） 💬（1）<div>感谢郭屹老师，
本节完整代码如下，需要的同学可以照着敲。
https:&#47;&#47;gitee.com&#47;rabbit2&#47;mini-spring&#47;commit&#47;1bf7247dd8568b5ce33134078efa2e4824816cf8</div>2023-04-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2d/20/df/55bacf31.jpg" width="30px"><span>Geek_b7449f</span> 👍（1） 💬（1）<div>真的很详细！从零手敲，然后反反复复看几遍终于把我之前自学所学的散的知识串联起来，真的学有收获，比较期待能把设计模式也能给一起串进来呢。
本人是一名在校的学生，这里我将每一步步骤拆分为提交的方式，希望这样可以更适合所学在校的应届生
不洗勿喷哦~：https:&#47;&#47;github.com&#47;HHXiaoFu&#47;mini-spring</div>2023-03-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/b8/dd/37726c34.jpg" width="30px"><span>小马哥</span> 👍（1） 💬（1）<div>回答课后题:
1, 反转: 反转的是对Bean的控制权, 使用&quot;new&quot;的方式是由程序员在代码中主动控制; 使用IOC的方式是由容器来主动控制Bean的创建以及后面的DI属性注入;
2, 反转在代码中的体现: 因为容器框架并不知道未来业务中需要注入哪个Bean, 于是通过配置文件等方式告诉容器, 容器使用反射技术管理Bean的创建, 属性注入, 生命周期等.</div>2023-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/85/ce/df1c7a91.jpg" width="30px"><span>陈小远</span> 👍（1） 💬（3）<div>Spring在Java编程中是事实的标准，这个无需多言，所以对老师的这个专栏也有比较大的兴趣。看了第一节课，也跟着动手撸了些代码，对有些疑惑的点做一简单阐述：
1、老师给的源码地址感觉应该是最终的成品的地址了，不是按照课程一节一节的区分开来，从学习跟随者的角度看，可能不太友好，无法从源码中找到项目从0到1的那种获得感；
2、针对本节中源码的讲述个人感觉还是有点跳跃了，不过本身Spring体系太过庞杂，无法面面俱到，也无法真的能从0去反推出Spring中相关类设计的原因，所以也表示理解。但有些设计意图还是希望老师能尽量多言一些，而不是因为Spring包或类那样设计的就强行往Spring身上靠，感觉有些突然。比如本节中抽象出了BeanFactory后，为什么又突然来一个SimpleBeanFactory，而ClassPathXmlApplicationContext同样也是实现自该接口，那通过SimpleBeanFactory在组合到ClassPathXmlApplicationContext中实现功能是出于什么考虑呢？ 虽然在评论区实际有看到小伙伴的讨论，大概能明白这样设计的意思。</div>2023-03-18</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/8HibfYTXFWaeXsujL7j1ZEulbibhiaMrTxkm3PticiaP9q3fGv8vkp1XHo9zsVE7Bh9HzkNicOnicd9QHFR73cefiaR7Qg/132" width="30px"><span>Ben Guo</span> 👍（1） 💬（1）<div>谢谢老师用心的准备和讲解！关于思考题，控制反转中“反转”的是“object生成&#47;销毁的控制对象”，从代码hardcode 指定对象的类型和创建过程，变成 从配置文件动态指定，然后IOC帮忙管理对象的生命周期。一个小小的建议，文中说了几个包名，但没有说明哪些类该归属哪个包 及为什么，大家可能要参考老师的开源项目才能明白，如果这里做个简单的说明，大家可能就不用去看，且国内访问github很多时候还是麻烦一点！ 谢谢！</div>2023-03-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a6/1e/e168b9e9.jpg" width="30px"><span>我不懂技术</span> 👍（1） 💬（2）<div>老师，有minitomcat的开源地址吗？</div>2023-03-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/36/6f/4e/791d0f5e.jpg" width="30px"><span>浅行</span> 👍（1） 💬（1）<div>反转了Bean的控制权，本来控制权是Java外放给开发人员的，而Spring是回收了这个权限，开发人员只能使用，不能控制Bean的生命周期。所以针对开发人员来说叫控制反转，不知道理解的对不对</div>2023-03-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/12/b0/63f71163.jpg" width="30px"><span>咕噜咕噜</span> 👍（1） 💬（1）<div>控制反转：反转的是对对象的控制权，将对象的管理由业务类交给了spring容器
spring代码中体现：通过反射机制去创建一个类的对象，spring会通过Class.newInstance()或者Constructor.newInstance()去创建一个对象。（具体可以参考org.springframework.beans.BeanUtils里面instantiate相关的方法）</div>2023-03-14</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q3auHgzwzM6mTy6lgnhkKbaWfs1s0siazVLQFnNmU0YLsRsxyC84aoFP5icuo22qricS62EiaibmVdplmtPbwryHHTA/132" width="30px"><span>Geek_5d0074</span> 👍（1） 💬（1）<div>手写SpringBoot有吗？</div>2023-03-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2d/7c/96/079a158d.jpg" width="30px"><span>adelyn</span> 👍（1） 💬（1）<div>控制反转:将对象的管理由业务类交给了spring</div>2023-03-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/f5/97/9a7ee7b3.jpg" width="30px"><span>Geek4329</span> 👍（0） 💬（1）<div>有一个问题 XmlBeanDefinition为什么要有BeanFactory的依赖呢？我理解loadBeanDefinitions 应该返回一个List&lt;BeanDefinition&gt;的集合 在ClassPathXmlApplicationContext 再调用 相关方法注入到BeanFactory中，XmlBeanDefinition的职能应该只是解析相关Resource得到BeanDefinition的集合，而不是应该进行注册的功能。</div>2024-02-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e7/26/1b773620.jpg" width="30px"><span>heyucool</span> 👍（0） 💬（1）<div>赞一个</div>2024-02-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/c6/6c/a400175a.jpg" width="30px"><span>FARO_Z</span> 👍（0） 💬（1）<div>画了下拆分后的 uml 图：
https:&#47;&#47;mermaid-js.github.io&#47;mermaid-live-editor&#47;view#pako:eNq1VMtu00AU_RVrVqkaW3nZiS2rEjQgIUGLmg1C3kzsm2SQPWPZY5SQJhskVixY8AdsWLIHxM9UKjt-gfGjk3HjREIVlmLdmXPPfZx74zXyWQDIQX6I03RM8DzBkUc9qomnuNMeA6ZPsc9ZstLWJeC6hHJIZtiHs7PyyuOnbxkJtATmJBXYGGaEEk4YbeUBdkdtWjueSPrl9A34XJsDzwmtCU8InRfeFziCym9TuSv1PRPZsKjueHFTxkIRSlvg9AKWvLWXlyq3DVmuIGVZ4sP_zTIhURxCg-Ie158LXbelKlspS1qH61Jv72m9c36B4yrUnx8f72Km4h0CV_z-bTYPXAEphyrIef5-ifniVRTeH4HoY8z8LALKtaAyJPIkhAJIGOOVLTG5MVACd-e9th86TlF0vfMrwAEUmyqycF0d9HRnl2gZKH9OD8RpHeCfKNSQ4aDOTVtSyKQydh2UhhTIvdZ1ufolJsnutWE0zkfVQa2wIOxtuOq9v_6uyH-ge-f3t_e3n7-WzMY9cUW-Q-Sbn78kublUNeSjOA6Jj3P-ORP_-yU_VvBxpqPdfP9y--kDaqMIkgiTQHx-i5X2EF-IhfSQI8wAZjgLuYc8uhGuOONssqI-cmY4TKGNsjjAHKovtryNMX3NWO2MnDVaIqc_7Blds9Ppd0x71B1ZZhutkKNbA8MaDHv9kW31LMseWps2eldE6Bi2PTJ74tcd9C2ra27-Aqc3Fxw</div>2023-06-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/de/ca/73f15fe7.jpg" width="30px"><span>老衲</span> 👍（0） 💬（1）<div>IOC翻转的是对对象的创建管理方式，正转就是我们平常使用 new 创建的方式，翻转是将对象的创建交给程序，又程序进行对象的创建。

有个小疑问，为什么需要 private List beanNames = new ArrayList&lt;&gt;(); 来存储 beanName ，获取的时候再次判断。这样做的目的是什么？有什么好处？</div>2023-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/db/26/54f2c164.jpg" width="30px"><span>靠人品去赢</span> 👍（0） 💬（1）<div>控制反转，解释控制权反转。什么控制权，是获取生成对象的控制权，之前有程序员去new，现在不用了，交给程序去控制，于是权力反转了。</div>2023-05-23</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/YjMKrDic9p6dgy7icWRegulZlP3wutzicm8EWcWXiashPqx4XiaJ65EYzUZHIoJrBSsI6EKMpg9YpWf8oOJvdX08GZg/132" width="30px"><span>安非他命π</span> 👍（0） 💬（1）<div>1. 看到实例化 bean 时用的是 java 反射 newInstance 方法想到如果要实例化的类只有有参构造要怎么实现？后面应该会引入有参构造类的实例化；
2. 在 SimpleBeanFactory 类中的定义的 singletons 属性，在下面 getBean方法时会发生并发操作吗？还是这里简单处理成使用普通的 HashMap 结构了？</div>2023-05-08</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJhxtIyXX4icMNAq5zEvchKYS3q7fwZXA3h7yV80iaibCRXniaLW95OnPC8PM2h5Ja5ibpkJ1VJowicqKZA/132" width="30px"><span>Geek_7jwpfc</span> 👍（0） 💬（1）<div>SimpleBeanFactory#getBean方法，需要通过两个List的下标获取，个人觉得耦合性比较大，时间复杂度也是N，应该这样写！
public class SimpleBeanFactory implements BeanFactory {
    &#47;&#47; 保存的BeanDefinition信息
    private Map&lt;String,BeanDefinition&gt; beanDefinitions = new HashMap&lt;&gt;();
    
    &#47;&#47; 保存的BeanDefinition对应的所有实例对象
    private Map&lt;String, Object&gt; singletons = new HashMap&lt;&gt;();

    public DefaultBeanFactory() {
    }

    @Override
    public Object getBean(String beanName) throws BeansException {
        Object singleton = singletons.get(beanName);
        if( singleton == null){
            BeanDefinition beanDefinition = beanDefinitions.get(beanName);
            if(beanDefinition == null){
                throw new BeansException(&quot;&quot;);
            }else {
                Object lazyBean;
                try {
                    lazyBean = Class.forName(beanDefinition.getBeanName()).newInstance();
                } catch (InstantiationException e) {
                    throw new RuntimeException(e);
                } catch (IllegalAccessException e) {
                    throw new RuntimeException(e);
                } catch (ClassNotFoundException e) {
                    throw new RuntimeException(e);
                }
                singletons.put(beanName, lazyBean);
                return lazyBean;
            }
        }
        return singleton;
    }

    @Override
    public void registerBeanDefinition(BeanDefinition beanDefinition) {
        this.beanDefinitions.put(beanDefinition.getBeanId(), beanDefinition);
    }
}</div>2023-04-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/15/44/59f5e984.jpg" width="30px"><span>胡多多</span> 👍（0） 💬（1）<div>老师太棒了，送爱心</div>2023-04-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/c0/0c/f726d4d0.jpg" width="30px"><span>KernelStone</span> 👍（0） 💬（1）<div>两三天时间，这节课内容断续思考和动手。终于算清楚了。用户“姐姐”总结得的很好！我尝试做额外的补充。

首先是设计模式方面的问题，看评论区有同学在纠结。如果先前看过相关的资料，应该可以反应过来这里是工厂方法，其目的就是将创建和使用两部分代码解耦分离。这是大前提。而内容后半段，抽取出了XmlBeanDefinitionReader，其实是出于“单一职责”的设计思想。这样有利于代码可读，也有利于可复用。

之所以取名为SimpleBeanFactory，而不是什么XmlBeanFactory，因为它的主要职责是不区分Resource，只提供getBean()和registerBeanDefinition()这两个方法。这一点结合BeanDefinition和beans.xml文件去看，会发现，id其实是“对象的名称”，而class其实是“生成该对象的模板”，二者共同存储在一个HashMap中。两行重要的代码如下：
1 singleton=Class.forName(`bd.getClassName()`).newInstance();
2 singletons.put(`bd.getId()`,singleton);

总而言之，我们是通过id，找到class这个单例的。id就像是引用，接口作为引用，class就是具体实现，生成单例的模板。

话说回来，BeanFactory不区分Resource，那对各种不同Resource的处理，就应该放在XXXApplicationContext上下文和XXXBeanDefinitionReader读取器中。就是具体资源的上下文，以及具体资源的读取器，才需要负责具体资源的注入。这也很合理。

----

个人理解，可能有误，不过这么整理下来，感觉内容就很清晰了，没有一开始看的时候感觉那么多！anyway谢谢老师。我继续加油往后学习</div>2023-04-19</li><br/>
</ul>