上节课，我带你剖析了利用职责链模式和动态代理模式实现MyBatis Plugin。至此，我们已经学习了三种职责链常用的应用场景：过滤器（Servlet Filter）、拦截器（Spring Interceptor）、插件（MyBatis Plugin）。

今天，我们再对MyBatis用到的设计模式做一个总结。它用到的设计模式也不少，就我所知的不下十几种。有些我们前面已经讲到，有些比较简单。有了前面这么多讲的学习和训练，我想你现在应该已经具备了一定的研究和分析能力，能够自己做查缺补漏，把提到的所有源码都搞清楚。所以，在今天的课程中，如果有哪里有疑问，你尽可以去查阅源码，自己先去学习一下，有不懂的地方，再到评论区和大家一起交流。

话不多说，让我们正式开始今天的学习吧！

## SqlSessionFactoryBuilder：为什么要用建造者模式来创建SqlSessionFactory？

在[第87讲](https://time.geekbang.org/column/article/239239)中，我们通过一个查询用户的例子展示了用MyBatis进行数据库编程。为了方便你查看，我把相关的代码重新摘抄到这里。

```
public class MyBatisDemo {
  public static void main(String[] args) throws IOException {
    Reader reader = Resources.getResourceAsReader("mybatis.xml");
    SqlSessionFactory sessionFactory = new SqlSessionFactoryBuilder().build(reader);
    SqlSession session = sessionFactory.openSession();
    UserMapper userMapper = session.getMapper(UserMapper.class);
    UserDo userDo = userMapper.selectById(8);
    //...
  }
}
```

针对这段代码，请你思考一下下面这个问题。

之前讲到建造者模式的时候，我们使用Builder类来创建对象，一般都是先级联一组setXXX()方法来设置属性，然后再调用build()方法最终创建对象。但是，在上面这段代码中，通过SqlSessionFactoryBuilder来创建SqlSessionFactory并不符合这个套路。它既没有setter方法，而且build()方法也并非无参，需要传递参数。除此之外，从上面的代码来看，SqlSessionFactory对象的创建过程也并不复杂。那直接通过构造函数来创建SqlSessionFactory不就行了吗？为什么还要借助建造者模式创建SqlSessionFactory呢？
<div><strong>精选留言（17）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1d/70/9f/741cd6a4.jpg" width="30px"><span>Henry</span> 👍（4） 💬（1）<div>SqlSessionFactoryBuilder 需要根据复杂配置才能构建出可用的SqlSessionFactory，符合builder模式的设计思想。SqlSessionFactory 设计意图用于生产SqlSession，也符合factory模式的思想；</div>2020-11-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/44/47/3ddb94d0.jpg" width="30px"><span>javaadu</span> 👍（54） 💬（9）<div>课后思考：我理解这就是mybatis的代码写得烂，不符合最小惊奇原则</div>2020-05-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/85/49/585c69c4.jpg" width="30px"><span>皮特尔</span> 👍（22） 💬（0）<div>可能是这个项目刚开始写的时候没想到会火，作者就不怎么在意代码质量，随随便便就写了；后来发现问题想改的时候，又因为历史原因不能改了</div>2020-06-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/d9/ff/b23018a6.jpg" width="30px"><span>Heaven</span> 👍（19） 💬（0）<div>设计思想比设计模式更重要,只要符合其设计的本意,没什么大不了的</div>2020-05-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/47/31/f35367c8.jpg" width="30px"><span>小晏子</span> 👍（12） 💬（1）<div>我认为非典型的建造者和工厂模式挺好的，我们并不是学院派，没必要追求典型的代码实现，既然这么做也可以简化开发并满足那些设计原则，那么就可以了。</div>2020-05-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/17/27/ec30d30a.jpg" width="30px"><span>Jxin</span> 👍（7） 💬（0）<div>前者隐藏的是初始化的细节，后者隐藏的选择的回话类型的细节。前者感觉建造者模式有点牵强，更像是初始化的配置类。后者工厂模式倒是没什么毛病，虽然不是标准的工厂模式。但我确实通过不同的选择，拿到了不同功能的对象。至于这些对象是同个父类的子类的对象，还是同个类不同参数的对象，我觉得只是实现方式的问题，场景上这个工厂模式并无不妥。</div>2020-05-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/70/9e/9337ca8e.jpg" width="30px"><span>jaryoung</span> 👍（6） 💬（0）<div>个人还是喜欢大而全的玩意：
引用文章的一句话：
实际上，这两个类的作用只不过是为了创建 SqlSession 对象，没有其他作用。所以，我更建议参照 Spring 的设计思路，把 SqlSessionFactoryBuilder 和 SqlSessionFactory 的逻辑，放到一个叫“ApplicationContext”的类中。让这个类来全权负责读入配置文件，创建 Congfiguration，生成 SqlSession。

修改前：
public class MyBatisDemo {
  public static void main(String[] args) throws IOException {
    Reader reader = Resources.getResourceAsReader(&quot;mybatis.xml&quot;);
    SqlSessionFactory sessionFactory = new SqlSessionFactoryBuilder().build(reader);
    SqlSession session = sessionFactory.openSession();
    UserMapper userMapper = session.getMapper(UserMapper.class);
    UserDo userDo = userMapper.selectById(8);
    &#47;&#47;...
  }

}

修改后：
public class MyBatisDemo {
  public static void main(String[] args) throws IOException {
    ApplicationContext applicationContext = new ApplicationContext(&quot;test-config.xml&quot;);
    SqlSession session = applicationContext.openSession();
    UserMapper userMapper = session.getMapper(UserMapper.class);
    UserDo userDo = userMapper.selectById(8);
    &#47;&#47;...
  }

}

使用越简单，背后逻辑越复杂，也可能是封装的必要性吧。
public class ApplicationContext {

    private Reader reader;

    public ApplicationContext(String path) {
        try {
            reader = Resources.getResourceAsReader(path);
        } catch (IOException e) {
            e.printStackTrace();
        }
        Assert.that(reader == null, &quot;reader can&#39;t null&quot;);
    }

    public ApplicationContext() {
        this(&quot;mybatis-config.xml&quot;);
    }
    public SqlSession openSession() {
        SqlSessionFactory sessionFactory = new SqlSessionFactoryBuilder().build(reader);
        return sessionFactory.openSession();
    }
}
</div>2020-05-27</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/ibcRNslcyp7dwIR3TIwvloCibMd7Ew2TB3MU0wISFXEolyuHRtfIriagm6PMX5zQHicmc78BrBcxA6vQ5qnTPCev9A/132" width="30px"><span>jiangjing</span> 👍（4） 💬（0）<div>软件开发是个迭代的过程，一开始是足够好用，设计没有求全求美；后面则不断优化和增强功能。 然后就是大家都熟悉怎么用了，有点小瑕疵但无关大局的代码就这么保留着吧，提供确定性</div>2020-05-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/50/d7/f82ed283.jpg" width="30px"><span>辣么大</span> 👍（3） 💬（0）<div>这两个源码倒是很容易读。在github上看了他们10年前的这两个类的代码，重载了一些函数，但结构是一样的。我想应该是命名的习惯吧。当时也没考虑那么多。</div>2020-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/fa/f7/91ac44c5.jpg" width="30px"><span>Mq</span> 👍（2） 💬（0）<div>理解设计模式适用范围跟使用方式的也能理解这个代码，不理解的，也能通过名称理解代码的意图，思想到位就行了，也不一定每个人都理解得那么多规则</div>2020-05-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/55/bc/fad0090b.jpg" width="30px"><span>Yeyw</span> 👍（1） 💬（0）<div>感觉是历史代码，在很多项目都有应用，不好做变更</div>2021-04-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/dd/60/a6a4f79a.jpg" width="30px"><span>笨鸟</span> 👍（1） 💬（0）<div>思想正确,过程可以稍加不同</div>2021-02-04</li><br/><li><img src="" width="30px"><span>Geek_7e0e83</span> 👍（0） 💬（0）<div>命名不统一，这个看作者的想法了。因人而异 无关对错。重要的是 符合 设计原则和设计思想，这样就能写出高质量代码。而设计模式，只是实现的一个方式。可以不用太抠实现是否标准</div>2022-11-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7d/95/dd73022c.jpg" width="30px"><span>我是曾经那个少年</span> 👍（0） 💬（0）<div>我们写在所学的设计模式，只不过是上个世纪90年代由Erich Gamma、Richard Helm、Raplh Johnson和Jonhn Vlissides四个人总结提炼出来的。

他是一个哲学观，具体到实践我们只要做到我们的代码分层简单，高内聚，低耦合就可以了。</div>2021-12-12</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/FqWrN8aNrlXEfo2YeDeCRuWMZ57VzsNC0aibkEIdiaNBdUVPjlBXrg9F4Eb8uMFYckuSgmXQ49vT6SHoicAjeEGdA/132" width="30px"><span>Geek_558387</span> 👍（0） 💬（0）<div>设计模式的精髓就是编码思想, 本子来说就相当于内功心法，并没有固定招式，实际上是可以照着心法自由发挥，唯一不变的就是变化, 是一套没有招式的武功，跟张无忌学太极一回事主要靠意会 ...</div>2020-09-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/1b/41/dbb7d785.jpg" width="30px"><span>xk_</span> 👍（0） 💬（0）<div>课后思考：SqlSessionFactoryBuilder只是SqlSessionFactory的默认实现，这么看感觉命名规则还行把。

想问一下，后面的是动态代理来创建SqlSession：
  private SqlSessionManager(SqlSessionFactory sqlSessionFactory) {
    this.sqlSessionFactory = sqlSessionFactory;
    this.sqlSessionProxy = (SqlSession) Proxy.newProxyInstance(
        SqlSessionFactory.class.getClassLoader(),
        new Class[]{SqlSession.class},
        new SqlSessionInterceptor());
  }

这里SqlSessionFactory.class.getClassLoader()有什么特别的地方吗？用别的类getClassLoader()可以吗？</div>2020-06-01</li><br/><li><img src="" width="30px"><span>Geek_3b1096</span> 👍（0） 💬（0）<div>给我们读源码起很大帮助</div>2020-05-29</li><br/>
</ul>