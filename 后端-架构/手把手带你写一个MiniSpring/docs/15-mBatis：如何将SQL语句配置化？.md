你好，我是郭屹。今天我们继续手写MiniSpring。这节课我们要模仿MyBatis，将SQL语句配置化。

上一节课，在已有的JDBC Template基础之上，我们按照专门的事情交给专门的部件来做的思路，对它做了进一步地拆解，抽取出了数据源DataSource这个部件，然后我们把SQL语句参数的处理独立成了一个ArgumentPreparedStatementSetter，之后对于返回结果，我们提供了两个东西，一个RowMapper和一个RowMapperResultSetExtractor，把一条数据库记录和一个记录集转换成对象和对象列表，便利了上层应用程序。最后为了提高性能，我们还引入了一个简单的数据库连接池。

现在执行的SQL语句本身还是硬编码在程序中的，所以这节课，我们就模仿MyBatis，把SQL语句放到程序外面的配置文件中。

## MyBatis简介

我们先来简单了解一下MyBatis。

> 官方说法：MyBatis is a first class persistence framework with support for custom SQL, stored procedures and advanced mappings. MyBatis eliminates almost all of the JDBC code and manual setting of parameters and retrieval of results. MyBatis can use simple XML or Annotations for configuration and map primitives, Map interfaces and Java POJOs (Plain Old Java Objects) to database records.
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（1）<div>请教老师两个问题啊：
Q1：Mapper配置的几个问题
在“Mapper配置”部分，有一个xml文件的说明：
&lt;mapper namespace=&quot;com.test.entity.User&quot;&gt;
&lt;select id=&quot;getUserInfo&quot; parameterType=&quot;java.lang.Integer&quot; resultType=&quot;com.test.entity.User&quot;&gt;

下面是文字说明：“这个配置中，也同样有基本的一些元素：SQL 类型、SQL 的 id”，
请问：namespace有什么用？文字说明中的“SQL 类型”对应哪个部分？是对应namespace吗？
namespace与resultType相同，是必须相同吗？还是可以不相同？

Q2：没有请求时候访问数据库。
SpringBoot项目，controller中自动注入service，service中自动注入Mapper。请求来了之后，由controller处理，controller调用自动注入的service，service再调用自动注入的Mapper，这是典型的ssm流程。
但是，现在有一个需求：软件启动后，需要访问数据库，此时并没有请求。我现在的实现方法是：controller的构造函数中使用JDBC访问数据库，是成功的。
问题：软件启动后，controller的构造函数执行了，说明controller被实例化了，此时service会自动注入吗？ （项目是两年前做的，当时一开始是尝试还用ssm来访问数据库，但好像失败了；印象中好像是service为null,就是说没有自动注入。）</div>2023-04-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/3a/ff/d2/c1f5334d.jpg" width="30px"><span>dirtychill</span> 👍（0） 💬（0）<div>一个sqlSession对应一个数据库，因此要做一个核心batis的配置文件逻辑</div>2024-06-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/f0/5b/791d0f5e.jpg" width="30px"><span>云从</span> 👍（0） 💬（0）<div>老师这节课在xml 中配置sqlSessionFactory时，使用了init-method，如果我没看漏的话 ，前面代码我们应该没有处理这个属性 需要在XmlBeanDefinitionReader 处理一下</div>2023-10-16</li><br/>
</ul>