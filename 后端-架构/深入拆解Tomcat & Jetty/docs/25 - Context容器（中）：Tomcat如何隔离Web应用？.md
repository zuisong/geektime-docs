我在专栏上一期提到，Tomcat通过自定义类加载器WebAppClassLoader打破了双亲委托机制，具体来说就是重写了JVM的类加载器ClassLoader的findClass方法和loadClass方法，这样做的目的是优先加载Web应用目录下的类。除此之外，你觉得Tomcat的类加载器还需要完成哪些需求呢？或者说在设计上还需要考虑哪些方面？

我们知道，Tomcat作为Servlet容器，它负责加载我们的Servlet类，此外它还负责加载Servlet所依赖的JAR包。并且Tomcat本身也是一个Java程序，因此它需要加载自己的类和依赖的JAR包。首先让我们思考这一下这几个问题：

1. 假如我们在Tomcat中运行了两个Web应用程序，两个Web应用中有同名的Servlet，但是功能不同，Tomcat需要同时加载和管理这两个同名的Servlet类，保证它们不会冲突，因此Web应用之间的类需要隔离。
2. 假如两个Web应用都依赖同一个第三方的JAR包，比如Spring，那Spring的JAR包被加载到内存后，Tomcat要保证这两个Web应用能够共享，也就是说Spring的JAR包只被加载一次，否则随着依赖的第三方JAR包增多，JVM的内存会膨胀。
3. 跟JVM一样，我们需要隔离Tomcat本身的类和Web应用的类。
<div><strong>精选留言（29）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/15/14/98/0251b8fd.jpg" width="30px"><span>Cy190622</span> 👍（41） 💬（2）<div>
老师好，您讲个很通透。还有一点问题请教一下：
1.线程上下文的加载器是不是指定子类加载器来加载具体的某个桥接类。比如JDBC的Driver的加载。
2.每个Web下面的java类和jar(WEB-INF&#47;classes和WEB-INF&#47;lib),都是WebAppClassLoader加载吗？
3.Web容器指定的共享目录一般是在什么路径下
</div>2019-07-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1c/c2/adba355c.jpg" width="30px"><span>王之刚</span> 👍（38） 💬（5）<div>最后的问题没有想明白，有人能详细解释一下吗？</div>2019-07-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1e/3a/5b21c01c.jpg" width="30px"><span>nightmare</span> 👍（14） 💬（1）<div>老师，上下文加载器是不是比如说我在加载spring的线程设置为webappclassloader那么就算spring的jar是由shared classloader加载的，那么spring加载的过程中也是由webappclassloader来加载，而用完设置回去，是因为我只需要跨classloader的时候才需要线程上下文加载器</div>2019-07-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a8/e2/f8e51df2.jpg" width="30px"><span>Li Shunduo</span> 👍（12） 💬（1）<div>Tomcat 9中只有这些目录了: conf,	logs,	bin, lib, temp, work, webapps.
并没有下面这些类加载器对应的common&#47;shared&#47;server目录，是需要自己手工创建吗？
CommonClassLoader对应&lt;Tomcat&gt;&#47;common&#47;*
CatalinaClassLoader对应 &lt;Tomcat &gt;&#47;server&#47;*
SharedClassLoader对应 &lt;Tomcat &gt;&#47;shared&#47;*
WebAppClassloader对应 &lt;Tomcat &gt;&#47;webapps&#47;&lt;app&gt;&#47;WEB-INF&#47;*目录
</div>2019-07-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/53/86/7c6476bc.jpg" width="30px"><span>大漠落木</span> 👍（12） 💬（1）<div>找不到 CommonClassLoader CatalinaClassLoader SharedClassLoader 这三个类

public class WebappClassLoader extends WebappClassLoaderBase

public abstract class WebappClassLoaderBase extends URLClassLoader</div>2019-07-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1e/3a/5b21c01c.jpg" width="30px"><span>nightmare</span> 👍（7） 💬（2）<div>老师我今天做了试验，在tomcat下和conf同级建立shared目录，然后把两个项目的spring的jar包放到shared目录下，然后webapp&#47;class下的spring的jar包删除，启动报找不到spring的jar包，tomcat版本为7.x，是不是还需要配置什么啊，请老师帮忙指导一下</div>2019-07-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e1/3e/a617ae38.jpg" width="30px"><span>每天一点点</span> 👍（5） 💬（1）<div>课后思考题
先切换 WebAppClassLoader 是因为 tomcat 的加载机制，需要先加载 web 的类，然后在共享类等
老师，对么？</div>2019-08-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/87/be/7466bf26.jpg" width="30px"><span>清风</span> 👍（3） 💬（2）<div>看代码，CommonClassLoader,CatalinaClassLoader,SharedClassLoader引用了同一个对象，这样的话，是怎么做到类空间隔离的呢</div>2019-07-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a0/a4/04dfe530.jpg" width="30px"><span>一颗苹果</span> 👍（3） 💬（1）<div>老师请问下，如果tomcat的不同应用引用了不同版本的spring依赖，sharedClassloader 怎么区分不同版本呢 </div>2019-07-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/a0/a3/8da99bb0.jpg" width="30px"><span>业余爱好者</span> 👍（3） 💬（2）<div>之前做了一个项目，在tomcat下面部署了两个springboot打的war，这两个war都依赖了同一个数据访问用的jar包，tomcat在启动第二个war项目时，报什么datasource已经实例化的一个错误，导致第二个项目启动失败。后来查了下资料，在application.yml里禁用了jmx解决。

虽然问题解决了，但却不明就里，不知道是不是web应用没有做隔离的缘故。不知道这样理解对不对。。</div>2019-07-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/b2/b3/798a4bb2.jpg" width="30px"><span>帽子丨影</span> 👍（1） 💬（1）<div>老师好，有个疑问。既然不同的类加载器实例加载的类是不同的，那如果Tomcat给每一个context使用各自的AppClassLoader实例来加载，那不是也可以达到应用隔离的目标了吗</div>2019-09-25</li><br/><li><img src="" width="30px"><span>玉芟</span> 👍（1） 💬（1）<div>老师，您好：
我对Thread.currentThread().setContextClassLoader(ClassLoader cl)用法一直有个疑问：
- setContextClassLoader以后是不是只能显示地通过getContextClassLoader获取ClassLoader后调用loadClass(String name, boolean resolve)方法加载类才能是自定义加载器加载的(验证方法：打印obj.getClass().getClassLoader())？
- setContextClassLoader以后通过Class.forName(String name)方法等反射得到的类是不是就只能是AppClassLoader加载的？
我做了个实验：
自定义类加载器：
public class DIYClassLoader extends URLClassLoader {
    public DIYClassLoader(URL[] urls) { super(urls); }
    &#47;**
     * 策略很简单：
     * 1)、首先尝试ExtClassLoader|BootstrapClassLoader加载
     * 2)、之后尝试自己加载
     * 3)、最后尝试真正父加载器加载
     *&#47;
    @Override
    protected Class&lt;?&gt; loadClass(String name, boolean resolve) throws ClassNotFoundException {
        Class&lt;?&gt; c = findLoadedClass(name);
        ClassLoader parent = getParent();
        if (parent != null) {
            ClassLoader ecl = parent;
            while (ecl.getParent() != null)&#47;&#47; 找ExtClassLoader
                ecl = ecl.getParent();
            try {
                c = ecl.loadClass(name);
            } catch (ClassNotFoundException e) { }
            if (c == null) {
                try {
                    c = findClass(name);&#47;&#47; DIYClassLoader自己来
                } catch (ClassNotFoundException e) {}
                if (c == null) {
                    &#47;&#47; 尝试真正父加载器加载，多半是AppClassLoader
                    c = parent.loadClass(name);
                }
            }
        }else {
            &#47;&#47; 直接自己尝试加载
            c = findClass(name);
        }
        if (resolve)
            resolveClass(c);
        return c;
    }
}
main方法：
URL url = Main.class.getClassLoader().getResource(&quot;.&quot;);
DIYClassLoader scl = new DIYClassLoader(new URL[] {url});
Thread.currentThread().setContextClassLoader(scl);
Class clazz = Class.forName(&quot;xx.xx.Xxx&quot;);
&#47;&#47; sun.misc.Launcher$AppClassLoader@18b4aac2
clazz = scl.loadClass(&quot;xx.xx.Xxx&quot;);
&#47;&#47; xx.xx.DIYClassLoader@682a0b20
不知道我把问题描述清楚了吗？还望老师解答</div>2019-07-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ad/27/5556ae50.jpg" width="30px"><span>Demter</span> 👍（0） 💬（1）<div>老师，spring的依赖类具体是指哪些啊</div>2019-08-22</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/6LaITPQ4Lk5fZn8ib1tfsPW8vI9icTuSwAddiajVfibPDiaDvMU2br6ZT7K0LWCKibSQuicT7sIEVmY4K7ibXY0T7UQEiag/132" width="30px"><span>尔东橙</span> 👍（0） 💬（1）<div>老师，JVM判断两个class实例相不相同，一个是看类加载器，另一个是看全路径名？那么如果全限定名不一样的servlet，为什么不能同时被一个加载器加载？</div>2019-08-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/7a/0a/0ce5c232.jpg" width="30px"><span>吕</span> 👍（0） 💬（2）<div>今天把springboot打成的多个war包放到tomcat，并且设置了host，但是无法访问到静态资源，而放到Root下就可以，实在搞不懂了</div>2019-07-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/a4/9c/b32ed9e9.jpg" width="30px"><span>陆离</span> 👍（0） 💬（1）<div>项目有用到切换数据源。
先创建多个DataSource实例，然后put到AbstractRoutingDataSource的继承类targetDataSources这个map中，最后通过线程的threadlocal带的key值切换。
这个和今天讲的classloader 有关吗？</div>2019-07-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/26/38/ef063dc2.jpg" width="30px"><span>Darren</span> 👍（4） 💬（0）<div> CommonClassLoader CatalinaClassLoader SharedClassLoader这3个类加载器，其实都是 java.net.URLClassLoader；

在org.apache.catalina.startup.Bootstrap#initClassLoaders中
private void initClassLoaders() {
        try {
            commonLoader = createClassLoader(&quot;common&quot;, null);
            if (commonLoader == null) {
                &#47;&#47; no config file, default to this loader - we might be in a &#39;single&#39; env.
                commonLoader = this.getClass().getClassLoader();
            }
            catalinaLoader = createClassLoader(&quot;server&quot;, commonLoader);
            sharedLoader = createClassLoader(&quot;shared&quot;, commonLoader);
        } catch (Throwable t) {
            handleThrowable(t);
            log.error(&quot;Class loader creation threw exception&quot;, t);
            System.exit(1);
        }
    }
最终调用的是:
org.apache.catalina.startup.ClassLoaderFactory#createClassLoader(java.util.List&lt;org.apache.catalina.startup.ClassLoaderFactory.Repository&gt;, java.lang.ClassLoader)
该方法返回的其实就是：
new URLClassLoader()

</div>2020-11-18</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTI4akcIyIOXB2OqibTe7FF90hwsBicxkjdicUNTMorGeIictdr3OoMxhc20yznmZWwAvQVThKPFWgOyMw/132" width="30px"><span>Chuan</span> 👍（2） 💬（4）<div>老师，请教下：这节课中我们说到WebAppClassLoader的父加载器是SharedClassLoader，上节课我们说的是AppClassLoader，我刚才也去看了WebAppClassLoader，它的loadClass()方法里检查完系统缓存后也是交给ExtClassLoader的，找不到再find()，然后交给AppClassLoader。那请问下SharedClassLoader是在哪里被用到的啊，您说了WebAppClassLoader找不到类，会交给SharedClassLoader，是在什么地方有这个逻辑呢？（求老师翻个牌子^ _ ^）</div>2020-03-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/83/c8/5ce842f6.jpg" width="30px"><span>maybe</span> 👍（1） 💬（0）<div>1、
tomcat类加载器有commonClassloader、CatalinaClassloader、sharedClassloader、webappClassloader。
webappClassloader加载web应用的类，tomcat为每个应用都创建一个webappclassloader实例，这样就达到了隔离web应用。
sharedClassloader加载器加载web应用之间公用的类。
CatalinaClassloader加载器加载tomcat本身的类，与web应用隔离。
commonClassloader加载器加载tomcat和web应用公用的类。
2、
spring当作公用类库用sharedClassloader加载时，spring加载业务类就通过线程上下文加载器进行加载。线程上下文加载器保留在线程私有数据中，同一个线程一旦设置了线程上下文加载器，在后续线程执行过程中就可以取出来使用了。
tomcat为每个应用创建一个webappclassloader实例，然后启动的时候设置上线文加载器，spring启动的时候就会把这个上下文加载器取出来。
3、
思考题：优先加载web应用的类，当加载完了再改回原来的。</div>2020-08-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/64/86/f5a9403a.jpg" width="30px"><span>yang</span> 👍（1） 💬（0）<div>老师 我每次看完一篇之后 都很有收获 觉得好兴奋 可能是因为我太激动了 就有点不求甚解了 说真的 很希望老师再出一个专栏   老师再出一个专栏 必定大卖!</div>2019-08-21</li><br/><li><img src="" width="30px"><span>Geek_41941f</span> 👍（0） 💬（0）<div>老师好，请问一个tomcat下运行多个web应用时，有什么办法可以分析每个web应用的资源占用情况，如内存？</div>2024-03-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/cd/f1/9616295e.jpg" width="30px"><span>陌上桑</span> 👍（0） 💬（0）<div>用完就没用了，但是又让再次使用的时候不要违反常理，所以恢复一下</div>2021-04-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ce/b8/92178ccd.jpg" width="30px"><span>ECHO</span> 👍（0） 💬（0）<div>老是你好，“这样 Spring 在启动时就将线程上下文加载器取出来，用来加载 Bean”这个能展开说详细点吗？</div>2020-07-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/86/f4/331f33a7.jpg" width="30px"><span>anchor</span> 👍（0） 💬（0）<div>实际发布大家还都是一个应用一个tomcat的吧 没有去发多个 分包吧</div>2020-04-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/fb/40/f78cc00a.jpg" width="30px"><span>鲁瑶</span> 👍（0） 💬（0）<div>讲的很清楚</div>2020-03-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/10/bb/f1061601.jpg" width="30px"><span>Demon.Lee</span> 👍（0） 💬（0）<div>老师，请教下，我把spring-boot相关的jar都放在 &lt;Tomcat &gt;&#47;shared&#47;下面，个别spring包（比如spring-boot-starter-data-rest-1.4.3.RELEASE.jar，spring-data-rest-core-2.5.6.RELEASE.jar，spring-data-rest-webmvc-2.5.6.RELEASE.jar等3个jar包）还在&lt;Tomcat &gt;&#47;webapps&#47;&lt;app&gt;&#47;WEB-INF&#47;lib&#47;下，因为只有个别app才用得到这几个jar，但是现在启动报错，Caused by: java.lang.NoClassDefFoundError: org&#47;springframework&#47;data&#47;rest&#47;webmvc&#47;config&#47;RepositoryRestConfigurerAdapter；所以，我就没完全理解类加载的顺序了。请老师答复下。</div>2020-01-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/10/bb/f1061601.jpg" width="30px"><span>Demon.Lee</span> 👍（0） 💬（0）<div>老师，请教下，我用的spring-boot，把相关spring的包都放在了xx&#47;tomcat8.5.50&#47;shared下面，其中有2个是redis相关的jar包（jedis-2.9.0.jar,spring-data-redis-1.8.7.RELEASE.jar）, 业务代码存数据到redis时是setObject(String key, Object value)，其中value是一个业务对象实例如Student（这个类在webapp&#47;WEB-INF&#47;classes下面）， 运行没有问题，但是取数据时，解析报错，Student对象找不到：
org.springframework.data.redis.serializer.SerializationException: Cannot deserialize; nested exception is org.springframework.core.serializer.support.SerializationFailedException: Failed to deserialize payload. Is the byte array a result of corresponding serialization for DefaultDeserializer?; nested exception is org.springframework.core.NestedIOException: Failed to deserialize object type; nested exception is java.lang.ClassNotFoundException: com.xxx.xxx.domain.Student
	at org.springframework.data.redis.serializer.JdkSerializationRedisSerializer.deserialize(JdkSerializationRedisSerializer.java:82)
	at org.springframework.data.redis.core.AbstractOperations.deserializeValue(AbstractOperations.java:318)
	at org.springframework.data.redis.core.AbstractOperations$ValueDeserializingRedisCallback.doInRedis(AbstractOperations.java:58)
	at org.springframework.data.redis.core.RedisTemplate.execute(RedisTemplate.java:207)
	at org.springframework.data.redis.core.RedisTemplate.execute(RedisTemplate.java:169)
	at org.springframework.data.redis.core.AbstractOperations.execute(AbstractOperations.java:91)
	at org.springframework.data.redis.core.DefaultValueOperations.get(DefaultValueOperations.java:43)

所以我理解是SharedClassLoader无法加载webAppClassLoader加载的类，那该如何解决这个问题呢，因为业务代码暂时不能改。</div>2019-12-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/05/7f/a7df049a.jpg" width="30px"><span>Standly</span> 👍（0） 💬（0）<div>老师，想到个问题，tomcat加载自身类的时候为什么不能用一个单独的WebAppClassLoader实例来加载，这样不仅不会和web应用的类加载冲突，而且还能把CatalinaClassLoader、CommonClassLoader这俩加载器都省了，简单明了。</div>2019-11-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/76/a0/1a6db8ac.jpg" width="30px"><span>无心水</span> 👍（0） 💬（0）<div>蓝色部分就是JVM的类加载器分层结构。Tomcat在JVM的基础上又加了三层。线程上下文类加载器，打破了双亲委托机制。</div>2019-09-24</li><br/>
</ul>