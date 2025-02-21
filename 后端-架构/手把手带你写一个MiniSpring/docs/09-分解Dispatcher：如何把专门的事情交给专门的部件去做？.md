你好，我是郭屹。今天我们继续手写MiniSpring。

经过上节课的工作，我们已经实现了IoC与MVC的结合，还定义了Dispatcher与WebApplicationContext两个相对独立又互相关联的结构。

这节课我们计划在已有的ApplicationConfigWebApplicationContext 和DispatcherServlet基础上，把功能做进一步地分解，让Dispatcher只负责解析request请求，用Context 专门用来管理各个Bean。

## 两级ApplicationContext

按照通行的Web分层体系，一个程序它在结构上会有Controller和Service 两层。在我们的程序中，Controller由DispatcherServlet负责启动，Service由Listener负责启动。我们计划把这两部分所对应的容器进行进一步地切割，拆分为XmlWebApplicationContext和AnnotationConfigWebApplicationContext。

首先在 DispatcherServlet 这个类里，增加一个对WebApplicationContext 的引用，命名为parentApplicationContext。这样，当前这个类里就有了两个对WebApplicationContext 的引用。
<div><strong>精选留言（10）</strong></div><ul>
<li><img src="" width="30px"><span>马儿</span> 👍（11） 💬（1）<div>总结一下：
1. Listener初始化的时候将交给Ioc管理的Bean初始化
2.Servlet初始化的时候将controller相关的bean初始化
这两步初始化将bean的管理从DispatcherServlet剥离交给了第一章创建的Ioc容器
3.将具体的url和对象+方法的管理从Servlet交给HandlerMapping来处理
4.将具体的方法执行剥离到HandlerAdapter
这两步将DispatcherServlet变得更抽象了，利用serviece方法可以同时处理不同类型的请求
一点建议：
1. DispatcherServlet中的controller相关bean的初始化已经交给AnnotationConfigWebApplicationContext管理了，它的init方法不用在调用initController了</div>2023-04-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/51/6e/757d42a0.jpg" width="30px"><span>lmnsds</span> 👍（5） 💬（1）<div>在github代码的geek_mvc3分支找了半天 这节课的 DispatcherServlet，原来不是在web包下改的原有类，而是在web.servlet包下新增了个DispatcherServlet！浪费了好多时间！给后来人提个醒吧。</div>2023-05-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/8b/4b/15ab499a.jpg" width="30px"><span>风轻扬</span> 👍（4） 💬（2）<div>思考题:我的想法是模仿SpringMVC,在RequestMapping注解上增加一个HttpMethod的属性(当前方法允许的请求方式)。在解析RequestMapping注解的时候改动一下,拿到RequestMapping注解上的HttpMethod,将其放到HandlerMethod中,然后将HandlerMathod对象放进MappingRegistry的一个map中,key:path,value:HandlerMethod。用户发起请求时,doDispatch方法中,获取到HttpServletRequest对象中的请求方式和MappingRegistry中存储的HandlerMethod上的请求方式进行比较,如果符合就可以访问,否则就报出方法类型不匹配
另外，有两个问题请教一下老师。
1、问题一:
DefaultListableBeanFactory beanFactory;
DefaultListableBeanFactory bf = new DefaultListableBeanFactory();        
this.beanFactory = bf;
我看老师在很多地方都是这样写的，为啥不直接给成员变量赋值呢?this.beanFactory = = new DefaultListableBeanFactory();

2、问题2
为什么Spring要搞出两个容器来呢?
我从StackOverFLow上搜了一下相关解释:https:&#47;&#47;stackoverflow.com&#47;questions&#47;18578143&#47;about-multiple-containers-in-spring-framework
看上面的解释是:
这样分开更清晰,Dispatcher驱动的子容器专门用来处理controller组件,ContextLoaderListener驱动的父容器专门用来处理业务逻辑组件以及持久化组件。
除了这个原因,Spring搞2个容器还有其他原因吗?</div>2023-04-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/b9/53/a72bebcc.jpg" width="30px"><span>赵欣</span> 👍（1） 💬（1）<div>有几个文件跟原来版本相比也有些变化了，大家注意下，一个是AbstractBeanFactory.java一个是DefaultListableBeanFactory.java文件。</div>2024-03-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/70/79/bb591140.jpg" width="30px"><span>睿智的仓鼠</span> 👍（0） 💬（1）<div>不可多得的好课，跟到现在学到很多</div>2023-06-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/31/45/3f/e4fc2781.jpg" width="30px"><span>梦某人</span> 👍（0） 💬（1）<div>首先以个人理解回答课后题，目前的请求并不分 get 或者 post，主要是以请求的路径进行区分，如果想要处理 post 请求，
需要构建新的 HandlerAdapter，对 Request 中的 post body 内容进行额外的解析和处理，然后操作方法。当然可能还需要构建 HandlerMapping 来处理请求路径，但是个人没想到什么 get 和 post 区别很大的地方。
第二和第三点是个人跟写的时候遇到的一些问题，给其他同学一点参考。
第二个， 
```
&#47;&#47; getBeanDefinitionNames 方法中
return (String[]) this.beanNames.toArray(); 
&#47;&#47;替换成
 return this.beanNames.toArray(new String[0]); 
```
可以减少一些类型转换异常，特别是当 ArrayList 里面只有一个 String 元素的时候。
第三个，BeanDefinition 中的部分 get 方法应该增加运算符 防止返回 Null 而不是 empty，导致空指针异常。例如：
```
  public ArgumentValues getArgumentValues() {
        return argumentValues == null? new ArgumentValues(): argumentValues;
    }
```
第四点是课程个人理解了：两级的 WebApplicationContext 第一级在 Listener 的时候加载，加载了 beans.xml (或者 Application.xml ) 中的 bean， 然后作为 第二级 AnnotationConfigWebApplicationContext 的父级， 第二级别通过 mvc.xml 提供的扫包路径进行扫包加载 bean，同时注册带有注解的方法。 当路由请求来的时候，先从第二级的 WebApplicationContext 获取 bean 和其方法进行处理，所以这个两级在最后的时候以 Controller 和 Service 来进行讲解，不是真的 Controller 和 Service， 而是说 第二级处理事物的触发逻辑比第一级更早，加载的逻辑则比他更晚，就好像 请求先到 Controller 后到 Service 一样。

最后的最后，，，看着老师文稿给的代码来吵，已经是和 GitHub 中的代码差别越来越大了， Debug 起来更加费时，但是好处是理解加深了。</div>2023-04-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/0b/5a/453ad411.jpg" width="30px"><span>C.</span> 👍（0） 💬（1）<div>出去玩了两天，今天把这章也结束掉了。代码运行一切正常。</div>2023-04-03</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/XWv3mvIFORNgRk9wF8QLb9aXfh1Uz1hADtUmlFwQJVxIzhBf8HWc4QqU7iaTzj8wB5p5QJLRAvlQNrOqXtrg1Og/132" width="30px"><span>Geek_320730</span> 👍（0） 💬（2）<div>1. 课后题：重写service后不是Get 和Post都能处理吗？
2.扫描的包里有接口，接口应该是不能实例化的，我过滤了下接口类型才能启动起来，对比了下老师的代码，好像并没有处理。
3.尝试了下在HelloWorldBean里注入parentApplicationContext中创建的Bean，发现了个小问题，AbstractBeanFactory#getBean方法中如果获取不到BeanDefinition 应该返回个null，而不是抛出异常，否则不会去父类查找。对构造器注入参数和set注入参数增加null校验</div>2023-04-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（2）<div>请教两个问题：
DispatcherServlet 这个类里，有两个WebApplicationContext对象：private WebApplicationContext webApplicationContext;
private WebApplicationContext parentApplicationContext;
请问，这两个对象是同一个对象吗？？
Q2：文中的controller和service是业务层的吗？
文中有这样的描述：“按照通行的 Web 分层体系，一个程序它在结构上会有 Controller 和 Service 两层。在我们的程序中，Controller 由 DispatcherServlet 负责启动，Service 由 Listener 负责启动。”
程序员写业务代码的时候，会按照controller、service、dao来写。
请问，文中的controller和service是业务层的controller、service吗？（即程序员写的controller、service）</div>2023-04-01</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83ep9YJC0GnicC7TDcrGFsfAZ6ATQLO29icXSKvntKcAcJGGJN6IibLrzHyp35Lia36fVlpSE8HsicIyOQyw/132" width="30px"><span>Geek_149cde</span> 👍（0） 💬（0）<div>不明白 AnnotationConfigWebApplicationContext 文件里 loadBeanDefinitions 加载的时候不应该把 AService 接口也加载进去了吗？创建 Bean 的时候不是就报错了</div>2023-07-03</li><br/>
</ul>