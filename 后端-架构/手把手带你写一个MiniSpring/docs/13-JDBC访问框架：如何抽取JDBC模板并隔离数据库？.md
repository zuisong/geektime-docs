你好，我是郭屹，今天我们继续手写MiniSpring。从这节课开始我们进入MiniSpring一个全新的部分：JdbcTemplate。

到现在为止，我们的MiniSpring已经成了一个相对完整的简易容器，具备了基本的IoC和MVC功能。现在我们就要在这个简易容器的基础之上，继续添加新的特性。首先就是**数据访问的特性**，这是任何一个应用系统的基本功能，所以我们先实现它。这之后，我们的MiniSpring就基本落地了，你真的可以以它为框架进行编程了。

我们还是先从标准的JDBC程序开始探讨。

## JDBC通用流程

在Java体系中，数据访问的规范是JDBC，也就是Java Database Connectivity，想必你已经熟悉或者至少听说过，一个简单而典型的JDBC程序大致流程是怎样的呢？我们一步步来看，每一步我也会给你放上一两个代码示例帮助你理解。

第一步，加载数据库驱动程序。

```plain
	Class.forName("com.microsoft.sqlserver.jdbc.SQLServerDriver");
```

或者直接new Driver();也可以。

这是第一步，因为JDBC只是提供了一个访问的API，具体访问数据库的工作是由不同厂商提供的数据库driver来实现的，Java只是规定了这个通用流程。对同一种数据库，可以有不同的driver，我们也可以自己按照协议实现一个driver，我自己就曾在1996年实现了中国第一个JDBC Driver。
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（7） 💬（1）<div>请教老师几个问题：
Q1：JDBC driver复杂吗？代码规模一般多大？能否以加餐形式讲一下driver？
Q2：JDBC Template还有用吗？
现在一般的开发都是SSM或SSH，不会用JDBC Template。
Q3：JDBC template能支持多大并发？
用JDBC template的话，一个数据库实例，比如一个mysql实例，能支持多大的并发量？200？</div>2023-04-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/f0/5b/791d0f5e.jpg" width="30px"><span>云从</span> 👍（0） 💬（2）<div>如果本地测试能够连接mysql  但是tomcat中可连接不上的话  看看tomcal  lib 下面有没有mysql 的驱动</div>2023-06-21</li><br/><li><img src="" width="30px"><span>马儿</span> 👍（0） 💬（1）<div>实现dml语句如果只是简单的实现就像最初的那一版拼接sql就可以实现了，但是这样的话需要每次更新都手动拼接sql比较麻烦。如果想要传入相应的对象就更新，可以利用本节课的callback来实现将相应的对象字段转换为sql语句的过程。但是这节课的结果可能整体上离最终感知不到sql还比较远，如果需要完全不感知sql应该是用一个类专门负责根据类属性的注解来自动映射。</div>2023-04-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/0b/5a/453ad411.jpg" width="30px"><span>C.</span> 👍（0） 💬（0）<div>前几天有点忙，这次补齐了。https:&#47;&#47;github.com&#47;caozhenyuan&#47;mini-spring.git。请看jdbc1、2、3分支</div>2023-04-27</li><br/>
</ul>