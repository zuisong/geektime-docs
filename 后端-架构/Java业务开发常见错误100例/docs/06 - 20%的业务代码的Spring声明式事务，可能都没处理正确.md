你好，我是朱晔。今天，我来和你聊聊业务代码中与数据库事务相关的坑。

Spring针对Java Transaction API (JTA)、JDBC、Hibernate和Java Persistence API (JPA)等事务API，实现了一致的编程模型，而Spring的声明式事务功能更是提供了极其方便的事务配置方式，配合Spring Boot的自动配置，大多数Spring Boot项目只需要在方法上标记@Transactional注解，即可一键开启方法的事务性配置。

据我观察，大多数业务开发同学都有事务的概念，也知道如果整体考虑多个数据库操作要么成功要么失败时，需要通过数据库事务来实现多个操作的一致性和原子性。但，在使用上大多仅限于为方法标记@Transactional，不会去关注事务是否有效、出错后事务是否正确回滚，也不会考虑复杂的业务代码中涉及多个子业务逻辑时，怎么正确处理事务。

事务没有被正确处理，一般来说不会过于影响正常流程，也不容易在测试阶段被发现。但当系统越来越复杂、压力越来越大之后，就会带来大量的数据不一致问题，随后就是大量的人工介入查看和修复数据。

所以说，一个成熟的业务系统和一个基本可用能完成功能的业务系统，在事务处理细节上的差异非常大。要确保事务的配置符合业务功能的需求，往往不仅仅是技术问题，还涉及产品流程和架构设计的问题。今天这一讲的标题“20%的业务代码的Spring声明式事务，可能都没处理正确”中，20%这个数字在我看来还是比较保守的。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/13/26/38/ef063dc2.jpg" width="30px"><span>Darren</span> 👍（59） 💬（8）<div>AspectJ与lombok，都是字节码层面进行增强，在一起使用时会有问题，根据AspectJ维护者Andy Clement的当前答案是由于ECJ（Eclipse Compiler for Java）软件包存在问题在AspectJ编译器基础结构中包含和重命名。
解决问题可以参考下面连接：
http:&#47;&#47;aspectj.2085585.n4.nabble.com&#47;AspectJ-with-Lombok-td4651540.html
https:&#47;&#47;stackoverflow.com&#47;questions&#47;41910007&#47;lombok-and-aspectj

分享一个使用lombok的坑：
之前为了set赋值方便，在VO或者DTO上使用了@Accessors(chain=true)，这样就可以链式赋值，但是在动态通过内省获取set方法进行赋值时，是获取不到对应的set方法，因为默认的set方法返回值是void，但是加了@Accessors(chain=true)之后，set方法的返回值变成了this，这样通过内省就获取到对应的set方法了，通过去掉@Accessors(chain=true)即可实现，通过内省动态给属性赋值。</div>2020-03-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/19/89/20488013.jpg" width="30px"><span>hanazawakana</span> 👍（47） 💬（4）<div>否则只有定义在 public 方法上的 @Transactional 才能生效。这里一定要用public吗，用protected不行吗，protected在子类中应该也可见啊，是因为包不同吗</div>2020-03-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/06/08/855abb02.jpg" width="30px"><span>Seven.Lin澤耿</span> 👍（46） 💬（1）<div>我还遇到一个坑，就是子方法使用了REQUIRES_NEW，但是业务逻辑需要的数据是来源于父方法的，也就是父方法还没提交，子方法获取不到。当时的解决方法是把事务隔离级别改成RC，现在回想起来，不知道这种解决方法是否正确？</div>2020-03-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/06/08/855abb02.jpg" width="30px"><span>Seven.Lin澤耿</span> 👍（26） 💬（8）<div>老师，可以问一下为啥国内大多数公司使用MyBatis呢？是为了更加接近SQL吗？难倒国外业务不会遇到复杂的场景吗？</div>2020-03-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/bd/da/3d76ea74.jpg" width="30px"><span>看不到de颜色</span> 👍（25） 💬（1）<div>Spring默认事务采用动态代理方式实现。因此只能对public进行增强（考虑到CGLib和JDKProxy兼容，protected也不支持）。在使用动态代理增强时，方法内调用也可以考虑采用AopContext.currentProxy()获取当前代理类。</div>2020-03-29</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/zGUSFibP0OGFW9a3QSic1DZLr5B4kPoNmt3RibzLNYSOxN3mUZibBMkGHpwcYPFYWJ7v61wsMvyIKzpBuQJWD2hVOg/132" width="30px"><span>九时四</span> 👍（19） 💬（8）<div>老师您好，有个数据库事务和spring事务的问题想请教下（我是一个入职半年的菜鸟）。
业务场景：为了实现同一个时间的多个请求，只有一个请求生效，在数据库字段上加了一个字段（signature_lock）标识锁状态。（没有使用redis锁之类的中间件，只讨论数据库事务和Spring的事务，以下的请求理解为同时请求）

1.在数据库层面，通过sql语句直接操作数据库，数据库事务隔离级别为可重复读：

-- 请求1
show VARIABLES like &#39;tx_isolation&#39;;
START TRANSACTION;
select * from subscribe_info where id = 29;
-- update语句只有一个请求可以执行，另一个请求在等待
update trade_deal_subscribe_info set signature_lock =1 where id = 1 and signature_lock = 0;
commit;

-- 请求2
show VARIABLES like &#39;tx_isolation&#39;;
START TRANSACTION;
select * from trade_deal_subscribe_info where id = 29;
-- update语句只有一个请求可以执行，另一个请求在等待
update subscribe_info set signature_lock =1 where id = 1 and signature_lock = 0;
commit;

两个请求中只有一个可以执行成功update语句，将signature_lock更新为1。



2.在代码层面按照在数据库层面的逻辑，service层的伪代码如下：
public void test(ParamDto paramDto) {
 &#47;&#47;取数据
 Data data = getByParamDto(paramDto);
 &#47;&#47; 尝试加锁,返回1表示加锁成功
 Integer lockStatus = lockData(paramDto);
 &#47;&#47; 加锁失败直接返回
 if(!Objects.equals(1,lockStatus)){
  return;
 }
 try{
   &#47;&#47; 处理业务代码，大概2到3秒 
   handle();
 }catch(Exception e){
 
 } finally{
   &#47;&#47; 释放锁
   releaseLock(paramDto);
 }
}


按照这样的方式，在方法上面不加注解的情况下，执行结果与在写sql的结果是一致的，两个请求只有一个可以执行成功；加上@Transactional(rollbackFor = Exception.class, propagation = Propagation.REQUIRED)之后，两个请求都可以拿到锁。

疑问是，Spring的事务和数据库的事务有什么关系，加上事务注解后，为什么和数据库的结果不一致。</div>2020-03-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f3/d6/5d55c315.jpg" width="30px"><span>火很大先生</span> 👍（15） 💬（1）<div>    @Transactional
    public int createUserRight(String name) throws IOException {
        try {
            userRepository.save(new UserEntity(name));
            throw new RuntimeException(&quot;error&quot;);
        } catch (Exception ex) {
            log.error(&quot;create user failed because {}&quot;, ex.getMessage());
            TransactionAspectSupport.currentTransactionStatus().setRollbackOnly();
        }
        return userRepository.findByName(name).size();
    }
请教老师，我这种写法，控制台打出了Initiating transaction rollback 但是数据库还是存上了数据，没有回滚，是因为findByName 这个查询语句的默认commit给提交了吗</div>2020-04-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d7/cd/6ebfc468.jpg" width="30px"><span>王刚</span> 👍（6） 💬（2）<div>老师问个问题，您说得@Transactional事物回滚，只有是RuntimeException 或error时，才会回滚；
但是我在做测试时，发现@Transactional有一个rollbackFor属性，该属性可以指定什么异常回滚，如果@Transactional 不指定rollbackFor，默认得是RuntimeException？</div>2020-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/24/2a/33441e2b.jpg" width="30px"><span>汝林外史</span> 👍（6） 💬（5）<div>老师，创建主子用户那个业务，应该是子用户创建失败不影响主用户，但是主用户失败应该子用户也要回滚吧？如果是这样，那传播机制是不是应该用Propagation.NESTED</div>2020-03-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/0d/cd/9264c4aa.jpg" width="30px"><span>Yanni</span> 👍（5） 💬（5）<div>要注意，@Transactional 与 @Async注解不能同时在一个方法上使用, 这样会导致事物不生效。</div>2020-04-10</li><br/><li><img src="" width="30px"><span>magic</span> 👍（5） 💬（1）<div>老师能补充下对私有方法事务的代码示例吗？</div>2020-03-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/24/2a/33441e2b.jpg" width="30px"><span>汝林外史</span> 👍（5） 💬（1）<div>很明显，this 调用因为没有走代理，事务没有在 createUserPublic 方法上生效，只在 Repository 的 save 方法层面生效。
createUserPublic这个方法不是本来就一个save操作吗，既然save层面生效了，那这个方法的事务难道不也就生效了吗？</div>2020-03-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/0c/d3/0be6ae81.jpg" width="30px"><span>COLDLY</span> 👍（4） 💬（2）<div>请问如果仅是select语句，需要加事务吗</div>2020-04-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/8d/3c/9025c2ca.jpg" width="30px"><span>张珮磊想静静</span> 👍（4） 💬（2）<div>如果一个事务里面操作了不同的数据库，回滚操作是不是就得自己写补偿的重试了？</div>2020-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/47/65/cce8eb34.jpg" width="30px"><span>nimil</span> 👍（3） 💬（2）<div>前几天还真出现了个事务不生效的问题，于是对着文章仔细review了一下代码，发现也没文中说的那些毛病，最后排查到是事务管理器只配置了一个数据库，而我是在另一个数据库进行的数据操作，所以事务不生效了，最后添加另一个数据库的事务管理器事务就生效了</div>2020-06-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/8d/22/0bf540be.jpg" width="30px"><span>tongzi</span> 👍（3） 💬（1）<div>【问题】
1、员工导入（新手机号），第一次会导入失败，再导入才会成功
【具体场景】
导入excel，解析成员工数据4条，先去注册生成t_user表，生成基本信息
然后在调用，bandCorp，和公司绑定，生成t_corp_user表
但是在调用bandCorp时，需要先去校验这个手机号，是否在t_user表生成数据
【解决】
发现由于事务注解引起的bug，importUserList（导入员工方法）加了事务注解，registerUser没有加事务注解
bandCorp加了事务注解，bandCorp传播级别为Propagation.REQUIRES_NEW，新开了事务
由于线上数据库为可重复读，qa数据库为读已提交，导致数据的不可见，校验失败

老师您好，我这边有个问题，看见springboot的事务隔离级别是default，默认采用数据库的
隔离级别，如果要是springboot的事务隔离级别，和mysql采用不同的隔离级别，是否会导致什么问题？（比如springboot手动设置为  可重复读，而数据库为读已提交）</div>2020-05-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e6/1c/9d3744ee.jpg" width="30px"><span>程序员俊达</span> 👍（3） 💬（2）<div>看完了老师讲的这篇文章，发现自己用@Transation的时候，也只是为了用而用，并不看它的真实效果，就会导致以后的数据不正确，有脏数据。今天把案例中的代码敲一遍，然后再看自己项目中的用法是否正确。</div>2020-03-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/5a/c9/933ee0a8.jpg" width="30px"><span>冉野</span> 👍（2） 💬（1）<div>可是为什么 在subUserService.createSubUserWithExceptionRight(entity);改成 new Thread()线程执行，事务就不会回滚了呢，还提示 SqlSession [org.apache.ibatis.session.defaults.DefaultSqlSession@3f669b54] was not registered for synchronization because synchronization is not active和
JDBC Connection [HikariProxyConnection@1155028039 wrapping com.mysql.jdbc.JDBC4Connection@4f6fcbb3] will not be managed by Spring
 还请老师和同学们帮解答一下
</div>2021-01-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/95/52/ad190682.jpg" width="30px"><span>Mr wind</span> 👍（2） 💬（2）<div>期待老师的回答，假如是在一个长流程的操作里，比如查询表1，更新表2，查询表3，更新表3...类似这种业务里数据量又大，各个表之间有业务关联都需要更新，耗时很长。这种情况应该加事务吗？如果加在流程顶部肯定会是长事务非常不好。感觉这种情况是否只有从业务角度来改变，不知道老师怎么看。</div>2020-10-12</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83ep3sqfTQey7eKYgGibLnAvaNj9k8gVvIYKVADicOA3DxmXZcDrAkeM8iaJLruiblmEVUr3q2LOVLvYicTw/132" width="30px"><span>郑先生</span> 👍（2） 💬（3）<div>有个问题 默认只回滚RuntimeException和Error的异常，按照异常继承关系：Error和Exception都继承自Throwable，如果指定rollbackFor=Exception.class，那不是Error的异常不会回滚了？</div>2020-06-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/73/a3/2b077607.jpg" width="30px"><span>Michael</span> 👍（2） 💬（3）<div>老师，有个问题，请教下：一个操作，里面涉及往nas盘写数据和数据库更新数据，当二者都成功才OK，但是会出现写入nas盘成功但是写入数据库失败的情况，这种如何回滚，nas盘的数据这时候不是有效的了，如何回滚清理</div>2020-04-08</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/mZrw2nVk1Aw8eYh5GPWpI9OHVBhXdFpMZx9mDyAHJuSZlpXCfKcOUxSUTewtibW8KBb0d9ftNl9F0n6ptudxBwQ/132" width="30px"><span>Geek_fb74a8</span> 👍（2） 💬（1）<div>老师，实际开发中是不是一般都将异常交给Controller层来处理或者由拦截器统一处理异常，从而保证需要事务支持的方法在执行过程中发生异常时能够保证回滚？</div>2020-03-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/16/5b/83a35681.jpg" width="30px"><span>Monday</span> 👍（2） 💬（2）<div>本节的三个坑，老师总结得很到位，我也理解原理了。但是让我自己看源码，就理不清思绪了。不知道从哪条线哪个类入手。</div>2020-03-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/0c/b3/7e13920b.jpg" width="30px"><span>🎓Dream-seeker</span> 👍（1） 💬（1）<div>在catch代码块中再抛出异常，应该也是可以回滚事物的吧</div>2020-08-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/64/9b/d1ab239e.jpg" width="30px"><span>J.Smile</span> 👍（1） 💬（2）<div>总结:
① 事务不生效的情况，事务注解加在private方法上、事务方法中调用的是内部this调用的方法而不是self    
②事务生效却出异常不回滚的情况，事务异常没有被传播出注解方法而是被捕获了、被事务注解的方法抛出的是受检异常导致不回滚
③主方法提交，子方法出错不提交的做法:
子方法上注解加上 propagation = Propagation.REQUIRES_NEW 来设置 REQUIRES_NEW 方式的事务传播策略，也就是执行到这个方法时需要开启新的事务，并挂起当前事务</div>2020-04-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/4d/b3/85828cc4.jpg" width="30px"><span>f</span> 👍（1） 💬（1）<div>第三遍看 又有收获</div>2020-04-11</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJfyOHapA4aYyichD5mfPicyX9cxVfYLexuZhYoc7VQOrRFL7SvKxevmb0VorVkcRZVRd8pO5KF5niag/132" width="30px"><span>李浩然</span> 👍（0） 💬（1）<div>写的很好</div>2020-12-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/9a/91/3bd41811.jpg" width="30px"><span>Pluto</span> 👍（0） 💬（1）<div>老师，您举的第一个例子，这个类没有实现接口， 默认不是使用 cglib 来生成代理吗</div>2020-08-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/8d/22/0bf540be.jpg" width="30px"><span>tongzi</span> 👍（0） 💬（1）<div>【问题】
1、员工导入（新手机号），第一次会导入失败，再导入才会成功
【具体场景】
导入excel，解析成员工数据4条，先去注册生成t_user表，生成基本信息
然后在调用，bandCorp，和公司绑定，生成t_corp_user表
但是在调用bandCorp时，需要先去校验这个手机号，是否在t_user表生成数据
【解决】
发现由于事务注解引起的bug，importUserList（导入员工方法）加了事务注解，registerUser没有加事务注解
bandCorp加了事务注解，bandCorp传播级别为Propagation.REQUIRES_NEW，新开了事务
由于线上数据库为可重复读，qa数据库为读已提交，导致数据的不可见，校验失败

老师你好，感谢回答这个问题；
还有个疑问是，当时临时解决的办法是，将最外层的importUserList（导入员工方法事务去除）；
我们可不可以手动将importUserList方法的@Transactional，隔离级别设置读已提交，来解决这个问题？
这种业务场景怎么解决比较好？谢谢老师</div>2020-05-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/64/9b/d1ab239e.jpg" width="30px"><span>J.Smile</span> 👍（0） 💬（3）<div>    @Autowired(required=false)
    private UserMapper userMapper;

    @Autowired
    private UserService self;


    public int createUserWrong1(String name) {
        try {
            self.createUserPrivate(new User(name));
        } catch (Exception ex) {
            logger.error(&quot;create user failed because {}&quot;, ex.getMessage());
        }
        return userMapper.getByName(name).size();
    }

    @Transactional
    public void createUserPrivate(User user) {
        userMapper.addUser(user);
        if (user.getName().contains(&quot;test&quot;))
            throw new RuntimeException(&quot;invalid username!&quot;);
    }
----------------------------------------------
将this换位self了，但是事务依然没有生效，http:&#47;&#47;localhost:8080&#47;user&#47;wrong1?name=test访问后，数据库还是插入了test这条记录呢？</div>2020-04-28</li><br/>
</ul>