你好，我是傅健。

通过上节课的学习，我们了解了 Spring Data 操作数据库的一些常见问题。这节课我们聊一聊数据库操作中的一个非常重要的话题——事务管理。

Spring 事务管理包含两种配置方式，第一种是使用 XML 进行模糊匹配，绑定事务管理；第二种是使用注解，这种方式可以对每个需要进行事务处理的方法进行单独配置，你只需要添加上@Transactional，然后在注解内添加属性配置即可。在我们的错误案例示范中，我们统一使用更为方便的注解式方式。

另外，补充一点，Spring 在初始化时，会通过扫描拦截对事务的方法进行增强。如果目标方法存在事务，Spring 就会创建一个 Bean 对应的代理（Proxy）对象，并进行相关的事务处理操作。

在正式开始讲解事务之前，我们需要搭建一个简单的 Spring 数据库的环境。这里我选择了当下最为流行的 MySQL + Mybatis 作为数据库操作的基本环境。为了正常使用，我们还需要引入一些配置文件和类，简单列举一下。

1. 数据库配置文件 jdbc.properties，配置了数据连接信息。

```
jdbc.driver=com.mysql.cj.jdbc.Driver

jdbc.url=jdbc:mysql://localhost:3306/spring?useUnicode=true&characterEncoding=UTF-8&serverTimezone=UTC&useSSL=false

jdbc.username=root
jdbc.password=pass
```

2. JDBC 的配置类，从上述 jdbc.properties 加载相关配置项，并创建 JdbcTemplate、DataSource、TransactionManager 相关的 Bean 等。
<div><strong>精选留言（11）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/15/e3/ff/51ea6737.jpg" width="30px"><span>辰砂</span> 👍（31） 💬（0）<div>@Transactional(rollbackFor = Exception.class, noRollbackFor = RuntimeException.class)</div>2021-06-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/9c/7d/774e07f9.jpg" width="30px"><span>study的程序员</span> 👍（2） 💬（0）<div>事务层面默认 publicMethodsOnly=true,所以private或者protected都不生效
强行设置 publicMethodsOnly=false:
@Bean
    @Primary
    @Role(BeanDefinition.ROLE_INFRASTRUCTURE)
    public TransactionAttributeSource mytransactionAttributeSource() {
        return new AnnotationTransactionAttributeSource(false);
    }
之后protected生效,private不生效,aop不能代理private方法&#47;final方法,所以不调用target的方法,所以spring注入的对象为null,所以会报NPE,studentMapper为空</div>2022-11-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/dd/56/0ff82229.jpg" width="30px"><span>陈汤姆</span> 👍（2） 💬（4）<div>学到了，一直以为注解只能对public生效是因为动态代理的原因！</div>2021-06-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/74/2f/638ee1bd.jpg" width="30px"><span>LkS</span> 👍（2） 💬（0）<div>可以使用noRollbackFor
@Transactional(rollbackFor = Exception.class,noRollbackFor = RuntimeException.class)</div>2021-06-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/51/9b/ccea47d9.jpg" width="30px"><span>安迪密恩</span> 👍（1） 💬（0）<div>我觉得可以把注解加在 saveStudent 这个方法上，要更自然一些。</div>2022-03-11</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKWYicxW2TxmZbD80jCQbfs7icgV7fGdOTRWLzN7YSfLicVxU3lorJ3NSlNuzBvABrSiaHIjgibECjAVDg/132" width="30px"><span>qchang</span> 👍（1） 💬（0）<div>思考题：一种是try-catch判断异常类型后，非RuntimeException抛出；另一种可以采用注解@Transactional(noRollbackFor = RuntimeException.class)</div>2021-06-04</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q3auHgzwzM7RKo5N6Y7Hgcr3YicsHul0XuDACAYzIpiaiazOc7LkkOoDlAHTTmX1dlIrhBZ6gP1QFXermLrP8Algg/132" width="30px"><span>小林桑</span> 👍（0） 💬（0）<div>1.Spring事务默认只有runtimeexception和error才会回滚；但是可以通过transactional注解指定回滚的异常类型。
2.对私有方法加transactional注解事务不会回滚。</div>2024-01-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/df/70/f3b8b8a2.jpg" width="30px"><span>番茄</span> 👍（0） 💬（0）<div>讲的非常清晰</div>2023-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/6b/e9/7620ae7e.jpg" width="30px"><span>雨落～紫竹</span> 👍（0） 💬（0）<div>其实就分2类 一类配置问题 一类代理问题</div>2022-06-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/16/5b/83a35681.jpg" width="30px"><span>Monday</span> 👍（0） 💬（0）<div>案例2中，进入doSaveStudent()方法后，抛NPE（studentMapper==null 为true）</div>2021-07-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/fc/18/8e69f7cf.jpg" width="30px"><span>一记妙蛙直拳</span> 👍（0） 💬（0）<div>@Transactional(rollbackFor = Exception.class, noRollbackFor = RuntimeException.class)</div>2021-06-04</li><br/>
</ul>