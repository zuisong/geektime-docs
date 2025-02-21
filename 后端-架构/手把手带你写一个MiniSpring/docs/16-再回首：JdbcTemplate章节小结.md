你好，我是郭屹。

恭喜你学完了MiniSpring的第三部分——JdbcTemplate了。JdbcTemplate在Spring 框架里，扮演着非常重要的角色。通过它，我们可以更加便捷地进行数据库操作，缩短了开发周期和开发成本，同时也降低了出错的风险。

它对Spring应用程序的稳定性和性能表现有着至关重要的影响，已经成为开发高效、高质量应用程序的不可或缺的一部分。

为了让你更好地掌握这部分内容，下面我们对这一整章做一个重点回顾。

### JdbcTemplate重点回顾

JdbcTemplate是Spring框架中的一部分，是Spring对数据访问的一个实现，在Spring应用程序中被广泛采用。它这个实现特别好地体现了Rod Johnson对简洁实用的原则的把握。JdbcTemplate封装了JDBC的 API，并提供了更为便捷的访问方式，使得开发人员在不需要编写大量代码的情况下，能够高效、灵活地进行数据库操作。

我们知道，JDBC的程序都是类似的，所以这个部分我们提取出一个JDBC访问的模板，同时引入DataSource概念，屏蔽具体的数据库，就便利了上层应用业务程序员。然后，我们再进行SQL参数的处理，SQL请求带有参数，实现把数据转换成SQL语句所需要的参数格式，对SQL语句执行后的返回结果，又要自动绑定为业务对象。
<div><strong>精选留言（2）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/17/8b/4b/15ab499a.jpg" width="30px"><span>风轻扬</span> 👍（2） 💬（1）<div>读写分离的实现，按照老师的思路，实现了一下。
1、增加sqlType参数。
首先改造MapperNode，增加sqlType参数.

2、注入双数据源。
因为我们配置到applicationContext.xml中的是SqlSessionFactory，所以数据源的注入要在这个类中。
public class DefaultSqlSessionFactory implements SqlSessionFactory {
    ........

    @Autowired
    private DataSource readDataSource;
    @Autowired
    private DataSource writeDataSource;

    @Override
    public SqlSession openSession() {
        .......
        defaultSqlSession.setReadDataSource(readDataSource);
        defaultSqlSession.setWriteDataSource(writeDataSource);
        return defaultSqlSession;
        .......
    }
    ........
}

3、根据sqlType将不同的数据源注入jdbcTemplate中
之后在openSession的时候，塞给SqlSession对象。当用户执行操作的时候，根据操作类型的不同，给JdbcTemplate注入不同的数据源
public class DefaultSqlSession implements SqlSession{
    
    .........

    private DataSource readDataSource;
    private DataSource writeDataSource;

    ....省略readDataSource和writeDataSource的set方法....

    @Override
    public Object selectOne(String sqlId, Object[] args, PrepareStatementCallBack pstmtcallback) throws Exception {
        MapperNode mapperNode = this.sqlSessionFactory.getMapperNode(sqlId);
        if (mapperNode.getSqlType().equals(&quot;3&quot;)) {
            jdbcTemplate.setDataSource(readDataSource);
        }
        return jdbcTemplate.queryObject(mapperNode.getSql(), args, pstmtcallback);
    }

    @Override
    public Integer delete(String sqlId, Object[] args) throws Exception {
        MapperNode mapperNode = this.sqlSessionFactory.getMapperNode(sqlId);
        if (mapperNode.getSqlType().equals(&quot;1&quot;)) {
            jdbcTemplate.setDataSource(writeDataSource);
        }
        return jdbcTemplate.delete(mapperNode.getSql(), args);
    }
    .........
}</div>2023-05-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（1）<div>请教老师几个问题：
Q1：会讲解MiniTomcat吗？
很期望针对Tomcat也出一个类似的专栏。

Q2：MVC会导致低并发吗？
MVC用一个单一的 Servlet 拦截所有请求，这个设计会降低系统的并发吗？</div>2023-04-17</li><br/>
</ul>