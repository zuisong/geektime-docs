上一节课，我们讲解了Spring中支持扩展功能的两种设计模式：观察者模式和模板模式。这两种模式能够帮助我们创建扩展点，让框架的使用者在不修改源码的情况下，基于扩展点定制化框架功能。

实际上，Spring框架中用到的设计模式非常多，不下十几种。我们今天就总结罗列一下它们。限于篇幅，我不可能对每种设计模式都进行非常详细的讲解。有些前面已经讲过的或者比较简单的，我就点到为止。如果有什么不是很懂的地方，你可以通过阅读源码，查阅之前的理论讲解，自己去搞定它。如果一直跟着我的课程学习，相信你现在已经具备这样的学习能力。

话不多说，让我们正式开始今天的学习吧！

## 适配器模式在Spring中的应用

在Spring MVC中，定义一个Controller最常用的方式是，通过@Controller注解来标记某个类是Controller类，通过@RequesMapping注解来标记函数对应的URL。不过，定义一个Controller远不止这一种方法。我们还可以通过让类实现Controller接口或者Servlet接口，来定义一个Controller。针对这三种定义方式，我写了三段示例代码，如下所示：

```
// 方法一：通过@Controller、@RequestMapping来定义
@Controller
public class DemoController {
    @RequestMapping("/employname")
    public ModelAndView getEmployeeName() {
        ModelAndView model = new ModelAndView("Greeting");        
        model.addObject("message", "Dinesh");       
        return model; 
    }  
}

// 方法二：实现Controller接口 + xml配置文件:配置DemoController与URL的对应关系
public class DemoController implements Controller {
    @Override
    public ModelAndView handleRequest(HttpServletRequest req, HttpServletResponse resp) throws Exception {
        ModelAndView model = new ModelAndView("Greeting");
        model.addObject("message", "Dinesh Madhwal");
        return model;
    }
}

// 方法三：实现Servlet接口 + xml配置文件:配置DemoController类与URL的对应关系
public class DemoServlet extends HttpServlet {
  @Override
  protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
    this.doPost(req, resp);
  }
  
  @Override
  protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
    resp.getWriter().write("Hello World.");
  }
}
```
<div><strong>精选留言（21）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/6f/b4/4aefe4c0.jpg" width="30px"><span>黄平</span> 👍（0） 💬（1）<div>TransactionAwareCacheDecorator怎么用呢？</div>2020-06-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/47/31/f35367c8.jpg" width="30px"><span>小晏子</span> 👍（22） 💬（1）<div>可以使用FactoryBean接口来实现，如下：
&#47;&#47;StdHttpClient可以理解为已经定义好的一个类，使用builder模式实现。
public class HttpFactoryBean implements FactoryBean&lt;HttpClient&gt;{

private String host;
private int port;


public HttpClient getObject() throws Exception {
    return new StdHttpClient.Builder()
                            .host(host)
                            .port(port)
                            .build();
}

public Class&lt;? extends HttpClient&gt; getObjectType() {
    return StdHttpClient.class;
}

public boolean isSingleton() {
    return true;
}

public void setHost(String host) {
    this.host = host;
}

public void setPort(int port) {
    this.port = port;
}}
添加配置到bean定义：
&lt;beans ...&gt; 
   &lt;bean name=&quot;myHttpClient&quot; class=&quot;HttpFactoryBean&quot;&gt;
       &lt;property name=&quot;port&quot; value=&quot;8080&quot;&#47;&gt;
       &lt;property name=&quot;host&quot; value=&quot;localhost&quot;&#47;&gt;
   &lt;&#47;bean&gt;
&lt;&#47;beans&gt;
之后你就可以使用StdHttpClient实例了。</div>2020-05-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/68/fe/1353168d.jpg" width="30px"><span>岁月</span> 👍（18） 💬（1）<div>不是做java的看的好累....看源码必须是先知道怎么使用, 然后才看源码, 这样才比较好看懂源码.</div>2020-05-20</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJKj3GbvevFibxwJibTqm16NaE8MXibwDUlnt5tt73KF9WS2uypha2m1Myxic6Q47Zaj2DZOwia3AgicO7Q/132" width="30px"><span>饭</span> 👍（15） 💬（2）<div>越看到后面，越觉得最好的模式就是没有模式，用好并理解基本的面向对象设计就成功一半了。</div>2020-05-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f2/56/c39046c0.jpg" width="30px"><span>Jie</span> 👍（6） 💬（3）<div>这篇内容密度很大，可以看上两天。

另外策略模式那块提到“这两种动态代理实现方式的更多区别请自行百度研究吧”，不是应该用Google搜索么=w=？</div>2020-05-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/f8/21/3fa228e6.jpg" width="30px"><span>悟光</span> 👍（4） 💬（1）<div>尝试了一下，xml配置未找到直接调用build方法的配置，用构造器注入
类：

public class Student {
    private long id;
    private String name;

    private Student(Builder builder) {
        this.id =builder.id;
        this.name = builder.name;
    }

    public String getName() {
        return name;
    }


    public static class Builder {
        private long id;
        private String name;
        public Student build() {
            if (StringUtils.isEmpty(name)){
                throw  new IllegalArgumentException(&quot;name  is empty&quot;);
            }
           return new Student(this);
        }

        public void setId(long id) {
            this.id = id;
        }

        public void setName(String name) {
            this.name = name;
        }
    }
}
配置：
&lt;bean id=&quot;build&quot; class=&quot;cn.gitv.rt.advertisv5.utils.Student.Builder&quot; &gt;
        &lt;property name=&quot;name&quot; value=&quot;aa&quot;&#47;&gt;
        &lt;property name=&quot;id&quot; value=&quot;2&quot;&#47;&gt;
    &lt;&#47;bean&gt;
    &lt;bean id=&quot;student&quot; class=&quot;cn.gitv.rt.advertisv5.utils.Student&quot;&gt;
        &lt;constructor-arg ref=&quot;build&quot;&#47;&gt;
    &lt;&#47;bean&gt;
2、“实际上，我们可以利用是适配器模式对代码进行改造，让其满足开闭原则，能更好地支持扩赞”。 这一句应该 “赞” 敲串行了。
</div>2020-05-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/75/a8/dfe4cade.jpg" width="30px"><span>电光火石</span> 👍（3） 💬（1）<div>&#47;&#47; 通过参考工厂方法来创建BeanId=&quot;zheng&quot;&quot;的Bean

&lt;bean id=&quot;zheng&quot; class=&quot;com.xzg.cd.StudentBuilder&quot; build-method=&quot;build&quot;&gt;
	&lt;property name=&quot;id&quot; value=&quot;1&quot;&gt;&lt;&#47;property&gt;
	&lt;property name=&quot;name&quot; value=&quot;wangzheng&quot;&gt;&lt;&#47;property&gt;
&lt;&#47;bean&gt;
把factory-method改成build-method</div>2020-05-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/d9/ff/b23018a6.jpg" width="30px"><span>Heaven</span> 👍（3） 💬（0）<div>对象的初始化有两种实现方式。一种是在类中自定义一个初始化函数，并且通过配置文件，显式地告知 Spring，哪个函数是初始化函数
</div>2020-05-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/50/2b/2344cdaa.jpg" width="30px"><span>第一装甲集群司令克莱斯特</span> 👍（2） 💬（0）<div>一看就会，一写就废！</div>2022-11-11</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/pCUrja4Z78P36FkdXQFFwnsmnicUjTsY7ickbR1xxAEp9yD1JebIafWiaXJLMvW7Ptn7Z6r6z3BiadQHHBhk1icYovw/132" width="30px"><span>牛凡</span> 👍（2） 💬（0）<div>在Spring中没有找到AnnotationMethodHandlerAdapter，应该是RequestMappingHandlerAdapter吧</div>2021-12-14</li><br/><li><img src="" width="30px"><span>Geek_3b1096</span> 👍（1） 💬（0）<div>信息量很大慢慢消化谢谢老师</div>2020-05-25</li><br/><li><img src="" width="30px"><span>Geek_f73a3e</span> 👍（0） 💬（0）<div>关于适配器模式，adaptee角色是谁呢？</div>2023-08-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/e0/6b/f61d7466.jpg" width="30px"><span>prader26</span> 👍（0） 💬（0）<div>实现接口+ 组合类，实现装饰器模式</div>2023-04-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/b6/06/cd1eaa49.jpg" width="30px"><span>小王在努力</span> 👍（0） 💬（0）<div>坚持！</div>2022-06-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/40/6d/61caf56b.jpg" width="30px"><span>🚦注意有车              ༽</span> 👍（0） 💬（2）<div>看了开头老师讲的适配器模式，跟策略模式好像差不多，总觉得适配器模式就是策略模式；两者该怎么具体区分呢</div>2022-05-19</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTItudDLPfbZabQLjk1NE8NSibQocdRy88rerQdxHFKx4KzUyaEnSLPbszcKAaPX8NgG3sHbZXib41aQ/132" width="30px"><span>Mirss.zhao</span> 👍（0） 💬（1）<div>在mapping中保存adapter的时候不需要if else.判断是哪种controller的adapter吗</div>2022-01-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/6f/b4/4aefe4c0.jpg" width="30px"><span>黄平</span> 👍（0） 💬（1）<div>将缓存的写操作和数据库的写操作，放到同一个事务中，要么都成功，要么都失败，这个问题只是说了用了装饰器设计模式，最后如何解决呢？</div>2022-01-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/47/18/293cd24d.jpg" width="30px"><span>o0oi1i</span> 👍（0） 💬（0）<div>打卡86</div>2020-11-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/02/2a/90e38b94.jpg" width="30px"><span>John(易筋)</span> 👍（0） 💬（0）<div>这两种动态代理实现方式的更多区别请自行Google</div>2020-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/1b/41/dbb7d785.jpg" width="30px"><span>xk_</span> 👍（0） 💬（0）<div>public class Builder {
    private String id;
    private String name;
    private String age;

    public void setId(String id) {
        if (id == null)
            throw new RuntimeException(&quot;id can&#39;t be null&quot;);
        this.id = id;
    }

    public void setName(String name) {
        if (name == null)
            throw new RuntimeException(&quot;name can&#39;t be null&quot;);
        this.name = name;

    }
    public void setAge(String age) {
        if (age == null)
            throw new RuntimeException(&quot;age can&#39;t be null&quot;);
        this.age = age;

    }
    ...getter...
}
public class Student {
    String id;
    String name;
    String age;

    Student(Builder builder) {
        id = builder.getId();
        name = builder.getName();
        age = builder.getAge();
    }
}

&lt;bean id=&quot;build&quot; class=&quot;com.aaa.Builder&quot; &gt;
        &lt;property name=&quot;name&quot; value=&quot;aa&quot;&#47;&gt;
        &lt;property name=&quot;id&quot; value=&quot;2&quot;&#47;&gt;
        &lt;property name=&quot;age&quot; value=&quot;2&quot;&#47;&gt;
    &lt;&#47;bean&gt;
    &lt;bean id=&quot;student&quot; class=&quot;com.aaa.Student&quot;&gt;
        &lt;constructor-arg ref=&quot;build&quot;&#47;&gt;
    &lt;&#47;bean&gt;</div>2020-05-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/a5/98/a65ff31a.jpg" width="30px"><span>djfhchdh</span> 👍（0） 💬（0）<div>Bean 的xml的配置&lt;constructor-arg ref=&#39;Builder类&#39;&gt;，即构造函数的入参是builder类（引用类型），BeanFactory中会使用递归，构造完Builder类对象之后，再构造你想要的Bean</div>2020-05-25</li><br/>
</ul>