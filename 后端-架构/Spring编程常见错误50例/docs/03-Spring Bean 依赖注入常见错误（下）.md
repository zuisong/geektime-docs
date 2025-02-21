你好，我是傅健，这节课我们接着聊Spring的自动注入。

上一讲我们介绍了3个Spring编程中关于依赖注入的错误案例，这些错误都是比较常见的。如果你仔细分析的话，你会发现它们大多都是围绕着@Autowired、@Qualifier的使用而发生，而且自动注入的类型也都是普通对象类型。

那在实际应用中，我们也会使用@Value等不太常见的注解来完成自动注入，同时也存在注入到集合、数组等复杂类型的场景。这些情况下，我们也会遇到一些问题。所以这一讲我们不妨来梳理下。

## 案例1：@Value没有注入预期的值

在装配对象成员属性时，我们常常会使用@Autowired来装配。但是，有时候我们也使用@Value进行装配。不过这两种注解使用风格不同，使用@Autowired一般都不会设置属性值，而@Value必须指定一个字符串值，因为其定义做了要求，定义代码如下：

```
public @interface Value {

   /**
    * The actual value expression &mdash; for example, <code>#{systemProperties.myProp}</code>.
    */
   String value();

}
```

另外在比较这两者的区别时，**我们一般都会因为@Value常用于String类型的装配而误以为@Value不能用于非内置对象的装配，实际上这是一个常见的误区**。例如，我们可以使用下面这种方式来Autowired一个属性成员：

```
@Value("#{student}")
private Student student;
```
<div><strong>精选留言（15）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/13/16/5b/83a35681.jpg" width="30px"><span>Monday</span> 👍（50） 💬（0）<div>思考题：
方法一：添加@Order(number)注解，number越小优先级越高，越靠前
方法二：声明Student这些Bean时将id=2的Student提到id=1之前

</div>2021-06-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/37/2b/b32f1d66.jpg" width="30px"><span>Ball</span> 👍（8） 💬（0）<div>今天的课程给出的问题直击业务痛点！我们非常方便的使用依赖注入的特性时，必须要思考🤔对象从哪里注入、怎么创建、为什么是注入这一个对象的。虽然编写框架的目的是让开发人员无需关心太多底层细节，能专心业务逻辑的开发，但是作为开发人员不能真的无脑去使用框架。
另外，我还得学会注入集合等高级用法，之前业务上都是用的注入单个对象的简单用法，必须有所提升。</div>2021-04-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7d/31/fd301a35.jpg" width="30px"><span>笨鱼</span> 👍（6） 💬（4）<div>StudentController构造函数上不需要加@Autowired注解吗？</div>2021-04-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（2） 💬（0）<div>不错，学习了</div>2021-11-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/4f/26/f21afb83.jpg" width="30px"><span>暖色浮余生</span> 👍（2） 💬（4）<div>发现一个问题。通过收集模式获取。比如我得 StudentController 类中通过 @Bean 的方式声明一个 bean 的时候，收集模式并不会收集到当前声明的这个 Student bean。当我的 @Bean 标注的方法为 static 的时候，收集模式此时收集到的是 3 个 bean. 感觉大概是当我的 bean 实例化完成之后才会调用 @Bean 标注的非静态方法，因为实例化未完成无法调用。 而静态方法并不依赖 bean 实例化。没找到具体的代码</div>2021-05-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/c6/ce/c1376d80.jpg" width="30px"><span>qlmmys</span> 👍（2） 💬（0）<div>思考题
spring按照bean声明的顺序加载bean，并顺序保存。所以想让学生2优先输出，主需要优先声明学生2即可</div>2021-04-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ce/d7/074920d5.jpg" width="30px"><span>小飞同学</span> 👍（2） 💬（1）<div>思考题：
收集装配风格：只能通过实体类实现Ordered接口 getOrder方法中指定一个顺序
直接装配方式：除了上述方式，还可以@Order 、@Priority注解指定顺序。</div>2021-04-26</li><br/><li><img src="" width="30px"><span>Geek7319</span> 👍（1） 💬（0）<div>针对问题1，是否可以可以使用@PropertySource配置文件路径呢。 从固定配置文件路径抽取value值，就无需考虑多个配置文件命名冲突问题</div>2021-12-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/6c/67/07bcc58f.jpg" width="30px"><span>虹炎</span> 👍（1） 💬（2）<div>控制spring bean加载顺序：
1，Bean上使用@Order注解，如@Order(2)。数值越小表示优先级越高。默认优先级最低。
2，@DependsOn    使用它，可使得依赖的Bean如果未被初始化会被优先初始化。</div>2021-05-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/84/8f/a305cc1e.jpg" width="30px"><span>otakuhuang</span> 👍（0） 💬（0）<div>声明 Bean 的位置靠前或使用 @Order 注解</div>2024-02-18</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q3auHgzwzM7RKo5N6Y7Hgcr3YicsHul0XuDACAYzIpiaiazOc7LkkOoDlAHTTmX1dlIrhBZ6gP1QFXermLrP8Algg/132" width="30px"><span>小林桑</span> 👍（0） 💬（0）<div>课后总结：
1.@Value使用：
@Value(&quot;abc&quot;) &#47;&#47;注入常量
@Value(&quot;${spring.datasource.password}&quot;);&#47;&#47;注入环境变量,这里不止是Spring的环境变量，还可以注入系统变量，Spring会扫描多个配置“源”，直至找到变量名就立即返回，所以使用环境变量时需要考虑是否和其他系统的参数名重复，导致加载到的属性值不是预期的值
@Value(&quot;#{user}&quot;) @Value(&quot;#{user.id}&quot;) @Value(&quot;#{1+2}&quot;);&#47;&#47;注入spring容器中的bean信息，包括bean实例bean的属性值，也可以使用表达式@Value(&quot;#{1+2}&quot;) = @Value(&quot;#{3}&quot;) 
2.关于注入集合的场景，分为：收集装配和直接装配（混合使用则默认使用收集装配）
区别：收集装配会自动收集容器中对应类型的所有实例
直接装配：定义一个集合对象，集合中存放相关元素，使用@Autowired或者构造函数注入
</div>2024-01-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/99/c3/e4f408d4.jpg" width="30px"><span>陌兮</span> 👍（0） 💬（0）<div>@Value这个点是之前从来没有考虑到的</div>2022-08-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/bf/3e/cdc36608.jpg" width="30px"><span>子夜枯灯</span> 👍（0） 💬（0）<div>添加@Order(number)注解，number越小优先级越高，越靠前</div>2022-01-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/76/93/2e9bf8ab.jpg" width="30px"><span>arch</span> 👍（0） 💬（3）<div>StudentController构造函数上应该需要加@Autowired注解</div>2021-05-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/60/10/2c533d89.jpg" width="30px"><span>陈越</span> 👍（0） 💬（0）<div>order注解
实现ordered接口</div>2021-04-26</li><br/>
</ul>