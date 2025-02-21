世界上存在永远不会出错的程序吗？也许这只会出现在程序员的梦中。随着编程语言和软件的诞生，异常情况就如影随形地纠缠着我们，只有正确处理好意外情况，才能保证程序的可靠性。

Java语言在设计之初就提供了相对完善的异常处理机制，这也是Java得以大行其道的原因之一，因为这种机制大大降低了编写和维护可靠程序的门槛。如今，异常处理机制已经成为现代编程语言的标配。

今天我要问你的问题是，请对比Exception和Error，另外，运行时异常与一般异常有什么区别？

## 典型回答

Exception和Error都是继承了Throwable类，在Java中只有Throwable类型的实例才可以被抛出（throw）或者捕获（catch），它是异常处理机制的基本组成类型。

Exception和Error体现了Java平台设计者对不同异常情况的分类。Exception是程序正常运行中，可以预料的意外情况，可能并且应该被捕获，进行相应处理。

Error是指在正常情况下，不大可能出现的情况，绝大部分的Error都会导致程序（比如JVM自身）处于非正常的、不可恢复状态。既然是非正常情况，所以不便于也不需要捕获，常见的比如OutOfMemoryError之类，都是Error的子类。

Exception又分为**可检查**（checked）异常和**不检查**（unchecked）异常，可检查异常在源代码里必须显式地进行捕获处理，这是编译期检查的一部分。前面我介绍的不可查的Error，是Throwable不是Exception。

不检查异常就是所谓的运行时异常，类似 NullPointerException、ArrayIndexOutOfBoundsException之类，通常是可以编码避免的逻辑错误，具体根据需要来判断是否需要捕获，并不会在编译期强制要求。

## 考点分析

分析Exception和Error的区别，是从概念角度考察了Java处理机制。总的来说，还处于理解的层面，面试者只要阐述清楚就好了。

我们在日常编程中，如何处理好异常是比较考验功底的，我觉得需要掌握两个方面。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/94/db/4e658ce8.jpg" width="30px"><span>继业(Adrian)</span> 👍（422） 💬（9）<div>假如你开车上山，车坏了，你拿出工具箱修一修，修好继续上路（Exception被捕获，从异常中恢复，继续程序的运行），车坏了，你不知道怎么修，打电话告诉修车行，告诉你是什么问题，要车行过来修。（在当前的逻辑背景下，你不知道是怎么样的处理逻辑，把异常抛出去到更高的业务层来处理）。你打电话的时候，要尽量具体，不能只说我车动不了了。那修车行很难定位你的问题。（要补货特定的异常，不能捕获类似Exception的通用异常）。还有一种情况是，你开车上山，山塌了，这你还能修吗？（Error：导致你的运行环境进入不正常的状态，很难恢复）
------------------
思考问题：由于代码堆栈不再是同步调用那种垂直的结构，这里的异常处理和日志需要更加小心，我们看到的往往是特定 executor 的堆栈，而不是业务方法调用关系。对于这种情况，你有什么好的办法吗？
------------------
业务功能模块分配ID，在记录日志是将前后模块的ID进行调用关系的串联，一并跟任务信息，进行日志保存。</div>2018-09-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e4/5d/fccd3913.jpg" width="30px"><span>钱宇祥</span> 👍（107） 💬（2）<div>1.异常：这种情况下的异常，可以通过完善任务重试机制，当执行异常时，保存当前任务信息加入重试队列。重试的策略根据业务需要决定，当达到重试上限依然无法成功，记录任务执行失败，同时发出告警。
2.日志：类比消息中间件，处在不同线程之间的同一任务，简单高效一点的做法可能是用traceId&#47;requestId串联。有些日志系统本身支持MDC&#47;NDC功能，可以串联相关联的日志。</div>2018-05-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f8/ba/d28174a9.jpg" width="30px"><span>Geek_zbvt62</span> 👍（65） 💬（1）<div>先说问题外的话，Java的checked exception总是被诟病，可我是从C#转到Java开发上来的，中间经历了go，体验过scala。我觉得Java这种机制并没有什么不好，不同的语言体验下来，错误与异常机制真是各有各的好处和槽点，而Java我觉得处在中间，不极端。当然老师提到lambda这确实是个问题...
至于响应式编程，我可以泛化为异步编程的概念嘛？一般各种异步编程框架都会对异常的传递和堆栈信息做处理吧？比如promise&#47;future风格的。本质上大致就是把lambda中的异常捕获并封装，再进一步延续异步上下文，或者转同步处理时拿到原始的错误和堆栈信息</div>2018-05-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fc/57/cf335b10.jpg" width="30px"><span>飞云</span> 👍（37） 💬（1）<div>能不能讲下怎么捕捉整个项目的全局异常，说实话前两篇额干货都不多，希望点更实在的干货</div>2018-05-08</li><br/><li><img src="" width="30px"><span>小绵羊拉拉</span> 👍（29） 💬（1）<div>看完文章简单认识一些浅层的意思 但是我关注的 比如try catch源码实现 涉及   以及 文章中提到 try catch 产生 堆栈快照 影响jvm性能等 一笔带过 觉得不太过瘾。只是对于阿里的面试 读懂这篇文章还是不够。还希望作者从面试官的角度由浅入深的剖析异常处理 最后还是 谢谢分享</div>2018-05-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4e/83/88151c5f.jpg" width="30px"><span>Caliven</span> 👍（25） 💬（2）<div>
ClassNotFoundException是在写编码的时候编译器就能告诉你这个地方需要捕获异常，如：你使用Class.forName的时候就必须要你捕获或者throws这个异常。
而NoClassDefFoundError在Javac已经把程序成功的编译成字节码文件了,当JVM进程启动，通过类加载器加载字节码文件，然后由JIT去解释字节码指令的时候，在classpath下找不到对应的类进行加载时就会发生NoClassDefFoundError这个错误。
我也不知道我的理解正确么？</div>2018-07-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/54/31/43efe6b9.jpg" width="30px"><span>Geek_x0htzs</span> 👍（19） 💬（3）<div>个人觉得checked exception &#47; unchecked exception 分别翻译为 检查型异常&#47;非检查型异常 更加好理解。
可检查异常容易被理解为可以不检查。</div>2018-05-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7f/88/c4263c58.jpg" width="30px"><span>五年</span> 👍（15） 💬（1）<div>老师讲的很好 😄 
不过理论讲过之后很容易忘 老师可以开一个github的代码库，将课程的最佳实践还有反例放进去吗</div>2018-05-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a8/bc/9f179054.jpg" width="30px"><span>美猴王</span> 👍（12） 💬（1）<div>提供一种思路：结合项目管理中对风险的分类，与文章的exception和errer做个关系对应。
checked exception（编译期异常）对应已知风险；
unchecked exception（运行时异常）对应可预测异常；
error（严重错误）对应不可预测风险；</div>2019-01-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fa/3e/92d74b38.jpg" width="30px"><span>Attract</span> 👍（11） 💬（1）<div>对于日志里面我们看到的往往是特定 executor 的堆栈，而不是业务方法调用关系这种情况，我在公司推行的是自定义异常，自定义的异常有一个错误码，这个错误码需要细到某个业务的某个方法的某种错，这样排查问题会很方便，但是写的时候就比较麻烦，文档也比较多</div>2018-05-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/32/48/933ba354.jpg" width="30px"><span>不吃老鼠的猫</span> 👍（10） 💬（1）<div>看了整篇文章和留言，大家都提到了不能用异常控制流程，这个我也懂，可是在项目中比如一个serivce方法，会对请求参数做检验，如果请求参数bean有5个属性需要检验，检验不成功，怎么处理？我目前项目中大都是如果检验不成功，就throw一个RuntimeException，如果不用这种抛异常的方式，用其他什么方式让上层调用放知道呢？如果用返回值，是不是要定义好多返回码？</div>2018-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/42/9a/183455ca.jpg" width="30px"><span>先天专治不服</span> 👍（7） 💬（1）<div>同样有一个问题，在spring mvc中，就提供了controllerAdvice注解，在业主流程中抛出相应的异常，在controllerAdvice中通过异常类型，完成相应的message输出。这个本质上也是通过异常完成对流程控制。而且能让业务流程很干净整洁。但是我一直很纠结，按文中说法，这是比较低效的流程控制，请问要如何取舍？</div>2018-05-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fc/66/d7f7ad77.jpg" width="30px"><span>风动静泉</span> 👍（6） 💬（2）<div>&quot;Exception 又分为可检查（checked）异常和不检查（unchecked）异常&quot;这句话本身没问题，但是不够全面吧。查了下&lt;&lt;JAVA核心技术 卷Ⅰ&gt;&gt; 第9版，pp.474  &quot;JAVA语言规范将派生于Error类或RuntimeException类的所有异常称为未检查(unchecked)异常，所有其他的异常称为已检查(checked)异常。&quot;</div>2018-05-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/75/90/ae39bc39.jpg" width="30px"><span>Ccook</span> 👍（5） 💬（2）<div>大佬能介绍下，线程间调用导致异常信息丢失的问题吗</div>2018-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c5/9e/d6fce09c.jpg" width="30px"><span>暴走的🐌</span> 👍（4） 💬（3）<div>业务规则检验是抛异常好还是if return好</div>2018-05-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5c/c5/1231d633.jpg" width="30px"><span>梁中华</span> 👍（4） 💬（1）<div>关于捕获全局异常，可以考虑使用AOP技术在接口入口层统一捕获，特别是使用类似dubbo这样的非springmvc架构的系统非常有用</div>2018-05-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/00/6e/11362a1e.jpg" width="30px"><span>感动超人</span> 👍（3） 💬（1）<div>我看第一条和第二条留言的疑问
java的动态加载和反射
Reflection 是 Java被视为动态（或准动态）语言的一个关键性质
动态加载是java运行期的时候再去加载类,不同于静态加载时编译期获得类的属性与方法,
动态加载通过反射来获取类内部的属性和方法</div>2019-01-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b8/37/98991aeb.jpg" width="30px"><span>不似旧日</span> 👍（2） 💬（1）<div>用户数据一般不输入到日志中,那么不能记录接口的请求参数了?</div>2019-01-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/b5/6c/617c0193.jpg" width="30px"><span>dingsai88</span> 👍（2） 💬（1）<div>物超所值啊  买的很对</div>2018-05-08</li><br/><li><img src="" width="30px"><span>BUGS</span> 👍（2） 💬（1）<div>Spring cloud sleuth不知道是否可以解决调用跟踪问题（包括异常？）</div>2018-05-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ab/10/b812ff3e.jpg" width="30px"><span>Hesher</span> 👍（2） 💬（1）<div>首先说说异常，虽然所有人都不建议一个大try-catch包住整个方法捕获exception，但我还是不放心啊，怎么破？我的做法是对小的代码段try-catch捕获指定的异常，然后在最外面套一个大的try-catch防止遗漏的情况，不知道这样做算不算一个折衷的办法，希望晓峰老师和其他同学多多指教。

响应式编程接触比较少，没什么经验，笨办法还是有。异常还是那些异常，如果把握不好捕获的位置和方法，不妨前期多加一些日志，把关键参数输出出来，从错误中反向总结异常处理方式。</div>2018-05-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/47/69/abb7bfe3.jpg" width="30px"><span>消失的子弹</span> 👍（1） 💬（1）<div>总结：
1 不要直接catch exception，要补获具体异常
2 不要大段代码catch，实例化异常时会对内存做快照，所以增大了快照开销，应该尽量小颗粒度补获异常
3 性能优化时异常处理也是一个重要关注点</div>2019-01-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/7a/d2/26575723.jpg" width="30px"><span>xxl</span> 👍（1） 💬（1）<div>文中并未明确说异常对性能的影响，看了Throwal中的方法并未提及性能问题，有具体的抛出异常情况与通过返回码返回方式性能差异对比吗？
fillInStackTrace

public Throwable fillInStackTrace()

Fills in the execution stack trace. This method records within this Throwable object information about the current state of the stack frames for the current thread.

If the stack trace of this Throwable is not writable, calling this method has no effect.

Returns:a reference to this Throwable instance.See Also:printStackTrace()</div>2019-01-08</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/KJUOWgZ6tc7j6s3ofibT3WvHH0XhnZB69uT4YNZ3QKC0x2ooSLT2RC59ocp6EHW922ViaW5KlJWuRIfwkqLVRMMw/132" width="30px"><span>sonnyfu</span> 👍（1） 💬（1）<div>捕获了throw或error，为啥就难以保证我们能够正确程序处理 OutOfMemoryError？</div>2018-05-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4a/0b/093f7d9e.jpg" width="30px"><span>YANGFEI</span> 👍（1） 💬（1）<div>Checked Exception 不兼容 functional 编程，如果你写过 Lambda&#47;Stream 代码，相信深有体会。这段话可以详细剖析下吗？</div>2018-05-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b8/37/98991aeb.jpg" width="30px"><span>不似旧日</span> 👍（0） 💬（1）<div>总结: 
exception和error都继承了throwable
exception是程序正常运行中可以预料的意外情况,error会导致程序处于非正常不可恢复状态。
exception分为编译时异常和运行时异常,编译时异常必须捕获,运行时异常可以不捕获
扩展
尽量不要捕获类似Exception这样的通用异常,而是应该捕获特定异学
不要生吞(swallow)异常。所谓生吞异常就是捕获了异常不处理
try-catch代码影响JVM对代码的优化,所以能不用就不用,尽量不要用大的try包装整段代码
不要用异常控制代码流程

内容不够多不够深</div>2019-01-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e6/e7/2c3cf94d.jpg" width="30px"><span>special·D</span> 👍（0） 💬（1）<div>文中老师您提到：error是不检查的是，是throwable，不是exception。到throwable是检查异常，需要在方法上显示定义。
JAVA源码注释：throwable and any subclass of throwable that is not also a subclass of either runtimeException or Error are regard as checked exception。throwable和它的子类，只有runtimeException和Error不是检查异常，其它都是检查异常</div>2018-10-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/78/e3/abb7bfe3.jpg" width="30px"><span>宇坤_</span> 👍（0） 💬（1）<div>try catch 会影响到jvm对代码的优化！我在controller 捕获 service中的业务。 是否会影响到service业务代码被jvm优化</div>2018-09-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/64/52/8cb50037.jpg" width="30px"><span>洺叶</span> 👍（0） 💬（1）<div>Printstacktrace 在稍微复杂一点的生产系统中，很难判断出到底输出到哪里去了，老师能否举例说明下会输出到什么地方？</div>2018-06-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/79/c9/2108e987.jpg" width="30px"><span>韩峰</span> 👍（0） 💬（1）<div>老师，关于异常，我有两点疑惑，第一点一个程序一级级的调用，是应该在在最上级捕获吗，第二点，目前我公司已有的项目自定义大量的业务异常继承自runtimException,比如库存不足异常，这样会不会额外增加开销，这是不是一种不可理的方式</div>2018-05-30</li><br/>
</ul>