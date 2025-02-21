你好，我是朱晔。今天，我们聊聊Java高级特性的话题，看看反射、注解和泛型遇到重载和继承时可能会产生的坑。

你可能说，业务项目中几乎都是增删改查，用到反射、注解和泛型这些高级特性的机会少之又少，没啥好学的。但我要说的是，只有学好、用好这些高级特性，才能开发出更简洁易读的代码，而且几乎所有的框架都使用了这三大高级特性。比如，要减少重复代码，就得用到反射和注解（详见第21讲）。

如果你从来没用过反射、注解和泛型，可以先通过官网有一个大概了解：

- [Java Reflection API](https://docs.oracle.com/javase/8/docs/technotes/guides/reflection/index.html) &amp; [Reflection Tutorials](https://docs.oracle.com/javase/tutorial/reflect/index.html)；
- [Annotations](https://docs.oracle.com/javase/8/docs/technotes/guides/language/annotations.html) &amp; [Lesson: Annotations](https://docs.oracle.com/javase/tutorial/java/annotations/index.html)；
- [Generics](https://docs.oracle.com/javase/8/docs/technotes/guides/language/generics.html) &amp; [Lesson: Generics](https://docs.oracle.com/javase/tutorial/java/generics/index.html)。

接下来，我们就通过几个案例，看看这三大特性结合OOP使用时会有哪些坑吧。

## 反射调用方法不是以传参决定重载

反射的功能包括，在运行时动态获取类和类成员定义，以及动态读取属性调用方法。也就是说，针对类动态调用方法，不管类中字段和方法怎么变动，我们都可以用相同的规则来读取信息和执行方法。因此，几乎所有的ORM（对象关系映射）、对象映射、MVC框架都使用了反射。

反射的起点是Class类，Class类提供了各种方法帮我们查询它的信息。你可以通过这个[文档](https://docs.oracle.com/javase/8/docs/api/java/lang/Class.html)，了解每一个方法的作用。
<div><strong>精选留言（15）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/13/71/05/db554eba.jpg" width="30px"><span>👽</span> 👍（7） 💬（1）<div>这一讲满满的知识盲区。。。
思考题2：
不可继承，我简单测试了一下。
另外，使用经验上也能说明不可继承。
因为，你想，我们通常的controller类，都会使用controller注解，如果可以被继承的话，Spring就不会只让我们使用Controller注解了，会提供另一种方式注入Controller组件，就是继承BaseController类。</div>2020-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/26/38/ef063dc2.jpg" width="30px"><span>Darren</span> 👍（22） 💬（1）<div>1、内部类会用到，类在JVM是最顶级的，即使是内部类，编译以后，都会存在外部类$1这样的class文件；外部类是能完全访问内部的方法的，即使是private，但编译后编程2个文件了，怎么访问的，就是通过synthetic标识位实现的。
在额外分享两篇R大关于逃逸分析的文章，里面涉及到了synthetic。
http:&#47;&#47;mail.openjdk.java.net&#47;pipermail&#47;hotspot-compiler-dev&#47;2016-September&#47;024535.html
http:&#47;&#47;mail.openjdk.java.net&#47;pipermail&#47;hotspot-compiler-dev&#47;2016-September&#47;024535.html
2、不会被继承，因为我的理解是继承后，RequestMapping对应的在父子类都能找到，处理起来肯定会很麻烦，在加上这几个注解默认都是单例的，所以是不能继承的。</div>2020-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1c/6e/6c5f5734.jpg" width="30px"><span>终结者999号</span> 👍（21） 💬（3）<div>老师您好，我听我们架构师说生产上最好不要使用反射会对性能有影响，有依据吗？</div>2020-04-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a1/e6/50da1b2d.jpg" width="30px"><span>旭东(Frank)</span> 👍（6） 💬（1）<div>java 的泛型真不怎么样，实现没有c#实现的好</div>2020-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/74/8a/d5b0cf30.jpg" width="30px"><span>kyl</span> 👍（6） 💬（1）<div>老师，后续能不能出一个结合项目利用一些高级特性、jdk新特性、设计模式实现高质量编码的课程，感觉工作中写的代码质量不够高又不知道如何快速提高。</div>2020-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e3/72/754314c2.jpg" width="30px"><span>Jackson</span> 👍（3） 💬（3）<div>老师，我使用了getDeclaredMethods，但是父类还是输出了两次，我用stream流的debug发现，子类其实还是有两个方法一个是String一个是Object，我也看了getDeclaredMethods这个方法其实是不包含父类的。
including public, protected, default (package)
  * access, and private methods, but excluding inherited methods</div>2020-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/24/2a/33441e2b.jpg" width="30px"><span>汝林外史</span> 👍（1） 💬（1）<div>findAllMergedAnnotations(AnnotatedElement element, Class&lt;A&gt; annotationType)
getAllMergedAnnotations(AnnotatedElement element, Class&lt;A&gt; annotationType)
老师，这两个方法除了名字不一样，我看入参，出参，描述都是一样的，那区别在哪呢？</div>2020-04-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/98/2a/ebf0e3fd.jpg" width="30px"><span>Blackwaltz</span> 👍（1） 💬（1）<div>老师，子类foo方法本身并没有通过继承获得MyAnnotation注解，而使用了AnnotatedElementUtils.findMergedAnnotation(child.getClass().getMethod(&quot;foo&quot;), MyAnnotation.class)之后，只是拿到了父类MyAnnotation注解为自己所用，而本身依然没有在程序运行的任何时段获得MyAnnotation注解，能这样理解吗？</div>2020-04-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/ae/f5/27227856.jpg" width="30px"><span>远山</span> 👍（0） 💬（1）<div>写的很棒，很喜欢</div>2023-05-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/05/81/9d3907f4.jpg" width="30px"><span>Rhinos HiL.</span> 👍（0） 💬（1）<div>第一个问题，采用sonar计算单元测试代码覆盖率的时候，用会java探针技术插入。</div>2020-07-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e3/72/754314c2.jpg" width="30px"><span>Jackson</span> 👍（4） 💬（0）<div>我查了一下除了内部类会生成synthetic，还有一个是使用了assert 关键字的class类。</div>2020-04-26</li><br/><li><img src="" width="30px"><span>Geek_3b1096</span> 👍（3） 💬（0）<div>谢谢老师期待21讲</div>2020-04-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/72/89/1a83120a.jpg" width="30px"><span>yihang</span> 👍（1） 💬（0）<div>思考题1:
方法重写时支持子类【重写方法的返回值类型】是父类【重写方法的返回值类型】的子类型，如父类方法返回List而子类方法返回arraylist，这时会需要并由编译器产生桥接方法

思考题2:spring那几个注解不能继承

另外想起一个相关的问题，dubbo用来发布服务的注解@service 最开始没加继承，导致spring这边用cglib生成的子类上扫描不到，后来修复了</div>2020-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2d/e1/22/bfb6b044.jpg" width="30px"><span>Mr.G@o</span> 👍（0） 💬（0）<div>老师你好！
问题2：我使用jdk8测试了下，运行出来的结果就是正确的答案呐，貌似不存在你说的那种，会反射出两个类型不同的Method(String和Object)。这是什么原因呢</div>2022-06-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e7/20/4f78c4e4.jpg" width="30px"><span>easy-cloud</span> 👍（0） 💬（0）<div>关于泛型我有一点疑问，假如泛型参数用于的是抽象方法，或者接口中的方法，则何如？</div>2020-05-23</li><br/>
</ul>