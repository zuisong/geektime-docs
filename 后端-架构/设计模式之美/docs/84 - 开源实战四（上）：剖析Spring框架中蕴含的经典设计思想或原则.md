在Java世界里，Spring框架已经几乎成为项目开发的必备框架。作为如此优秀和受欢迎的开源项目，它是我们源码阅读的首选材料之一，不管是设计思想，还是代码实现，都有很多值得我们学习的地方。接下来，我们就详细讲讲Spring框架中蕴含的设计思想、原则和模式。因为内容比较多，我分三部分来讲解。

- 第一部分，我们讲解Spring框架中蕴含的经典设计思想或原则。
- 第二部分，我们讲解Spring框架中用来支持扩展的两种设计模式。
- 第三部分，我们总结罗列Spring框架中用到的其他十几种设计模式。

今天，我们就讲下第一部分：Spring框架中蕴含的一些设计思想或原则，这其中就包括：约定大于配置、低侵入松耦合、模块化轻量级等。这些设计思想都很通用，掌握之后，我们可以借鉴用到其他框架的开发中。

话不多少，让我们正式开始今天的学习吧！

## Spring框架简单介绍

考虑到你可能不熟悉Spring，我这里对它做下简单介绍。我们常说的Spring框架，是指Spring Framework基础框架。Spring Framework是整个Spring生态（也被称作Spring全家桶）的基石。除了Spring Framework，Spring全家桶中还有更多基于Spring Framework开发出来的、整合更多功能的框架，比如Spring Boot、Spring Cloud。
<div><strong>精选留言（19）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/18/1f/29/c7a69190.jpg" width="30px"><span>浩浩</span> 👍（0） 💬（4）<div>&quot;模块之间关系，仅有上层对下层的依赖关系，而同层之间以及下层对上层，几乎没有依赖和耦合&quot;前面说“仅有上层对下层的依赖关系”；后面说：“而同层之间以及下层对上层，几乎没有依赖和耦合”
这不前后矛盾了吗？想不明白，求教。


</div>2020-05-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/86/56/509535da.jpg" width="30px"><span>守拙</span> 👍（50） 💬（6）<div>Gson是google出品的Json序列化&#47;反序列化开源框架(相信专栏读者没人没用过吧).

Gson符合&quot;约定优于配置&quot;:

通常情况, 实体类的成员变量名与序列化后的json key是一致的, 无需配置, 算是一种约定.

但实体类的成员变量名和json key也可以不同. 通过@SeriailzedName()注解, 可以配置成员变量与json key的映射关系. 

例:
private String userName;&#47;&#47;序列化后: {&quot;userName&quot; : &quot;xx&quot;}

@SerializedName(&quot;user_name&quot;)
private String userName;&#47;&#47;序列化后: {&quot;user_name&quot;; &quot;xx&quot;}

</div>2020-05-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/d9/ff/b23018a6.jpg" width="30px"><span>Heaven</span> 👍（11） 💬（0）<div>1.约定优于配置,其实这一点能延伸出很多的东西,约定可以理解为协议,可以说基于接口开发就是基于一种协议,也是遵循的约定优于配置.再者说,约定基于配置,可以延伸出模块化的思想,不改变的情况下,使用默认模块,并且支持模块的替换.是否可以说常见的MVC三层框架就是约定优于配置?
而我的举例,从网络传输协议说就是一种约定优于配置,从MAC层,IP层,TCP&#47;UDP层,HTTP层,应用层,层层划分,交互双方按照相同协议读写,并且我们使用网络通信的时候,无须去手动配置底层的协议,而是有默认的底层协议去传输,让开发者聚焦于业务开发</div>2020-05-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fe/90/19ef108d.jpg" width="30px"><span>techwro</span> 👍（7） 💬（2）<div>1.通过@Bean标记方法生成的bean对象，默认使用方法名作为beanName</div>2020-05-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/f8/21/3fa228e6.jpg" width="30px"><span>悟光</span> 👍（7） 💬（1）<div>一直在用spring，约定优于配置、低侵入，松耦合这些也时常听说但是对这些名词感觉比较陌生，大部分开发都是沿用架构的思路或者原有的代码结构，感觉开发业务挺熟练了，但是细想一些细节还是不太明白那么做的好处，只是觉得确实方便，看完争哥的这篇文章，一下子打通了任督二脉，原来不理解的几点一下串联起来了。从设计思想来看具体实现就能明白好的代码不仅仅在服务一处，还考虑到开发体验、效率。内心挺激动，明白为什么那么写了对项目理解又加深了。</div>2020-05-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/3a/f8/c1a939e7.jpg" width="30px"><span>君哥聊技术</span> 👍（4） 💬（0）<div>1.Jvm定义了一套模版规范，然后让各虚拟机去实现，比如hotspot
2.tomcat模块化思想非常明显，比如连接器分为endpoint,processor,和adaptor三个轻量级模块
</div>2020-05-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/47/31/f35367c8.jpg" width="30px"><span>小晏子</span> 👍（4） 💬（0）<div>spring framework中的controller model view都有约定大于配置的规则。可以参考https:&#47;&#47;docs.spring.io&#47;spring&#47;docs&#47;3.0.0.M3&#47;reference&#47;html&#47;ch16s10.html，写的很清楚。</div>2020-05-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/17/27/ec30d30a.jpg" width="30px"><span>Jxin</span> 👍（4） 💬（1）<div>spring在向后兼容和质量追求上也做得非常好。</div>2020-05-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/70/9e/9337ca8e.jpg" width="30px"><span>jaryoung</span> 👍（3） 💬（0）<div>“约定优于配置”，就是项目中的一些约定，例如，使用mybatis开发查询接口的时候，统一约定查询操作都以query开头，删除使用delete开头，更新使用update开头。
netty，组件化的思想，每个组件都有自己的工作相互配合。每个组件提供相应的扩展点，用户可以扩展，符合开闭原则等等。</div>2020-05-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/32/fc/5d901185.jpg" width="30px"><span>vic</span> 👍（2） 💬（0）<div>java项目工程划分,层级划分,都是按照约定来的, 以及json的序列化, 不管是jackson,gson,fastjson, 都体现了约定大于配置</div>2020-05-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/55/7a/d44df1d6.jpg" width="30px"><span>freesocean</span> 👍（1） 💬（0）<div>java web中的分层，类名等都几乎成为了约定俗称，MybatisPlus就针对于此，做了很多再抽象，再封装，并可以自动生成基础类，提供基本的api，又一次简化了web开发。</div>2021-11-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/02/65/ddb6460e.jpg" width="30px"><span>柯里</span> 👍（0） 💬（0）<div>Mybatis中关于表格的映射</div>2023-11-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/e0/6b/f61d7466.jpg" width="30px"><span>prader26</span> 👍（0） 💬（0）<div>spring框架的核心理念有：约定优于配置，低侵入，松耦合，模块化，轻量级，在封装，再抽象。</div>2023-04-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/40/6d/61caf56b.jpg" width="30px"><span>🚦注意有车              ༽</span> 👍（0） 💬（0）<div>mybatis开源框架：
1、很多的配置比如mapper的xml配置文件，里面的很多标签都是约定好的，也就是定义好了怎么用的
2、里面的插件接口，是低侵入松耦合，扩展性强</div>2022-05-18</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erpYZalYvFGcBs7zZvYwaQAZwTLiaw0mycJ4PdYpP3VxAYkAtyIRHhjSOrOK0yESaPpgEbVQUwf6LA/132" width="30px"><span>Harlan</span> 👍（0） 💬（0）<div>说下mybaitis:
1.作了很多约定，如xml  mapper  entity 等，默认配置 ，默认目录结构
2.目标是提供一套通用框架，屏蔽数据库层</div>2021-01-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f9/aa/3e80212e.jpg" width="30px"><span>龙猫</span> 👍（0） 💬（0）<div>springboot更好的使用了约定大于配置，springboot的自动配置加载中间件，tomcat、mybatis、redis、mq等就是使用了默认参数。
</div>2020-09-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/71/05/db554eba.jpg" width="30px"><span>👽</span> 👍（0） 💬（0）<div>约定优于配置 我认为，其思想应用的面就很广了。
我感觉，HashMap，其实现也是默认实现即可，包括 默认容量，扩容阈值等。直接new HashMap（）就可以用，但是其配置也可以自定义。
</div>2020-08-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/3b/65/7a01c8c8.jpg" width="30px"><span>Nights</span> 👍（0） 💬（1）<div>mybatis-plus默认实现增删改查</div>2020-07-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/1c/8c/3af20a8e.jpg" width="30px"><span>Fitch Kuma</span> 👍（0） 💬（0）<div>Spring Integration DSL中IntegrationFlow的方法名默认读取方法名.input的channel，体现convention over configuration</div>2020-07-07</li><br/>
</ul>