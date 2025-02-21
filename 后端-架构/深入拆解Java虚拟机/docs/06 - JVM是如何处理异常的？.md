你好，我是郑雨迪。今天我们来讲讲Java虚拟机的异常处理。

众所周知，异常处理的两大组成要素是抛出异常和捕获异常。这两大要素共同实现程序控制流的非正常转移。

抛出异常可分为显式和隐式两种。显式抛异常的主体是应用程序，它指的是在程序中使用“throw”关键字，手动将异常实例抛出。隐式抛异常的主体则是Java虚拟机，它指的是Java虚拟机在执行过程中，碰到无法继续执行的异常状态，自动抛出异常。举例来说，Java虚拟机在执行读取数组操作时，发现输入的索引值是负数，故而抛出数组索引越界异常（ArrayIndexOutOfBoundsException）。

捕获异常则涉及了如下三种代码块。

1. try代码块：用来标记需要进行异常监控的代码。
2. catch代码块：跟在try代码块之后，用来捕获在try代码块中触发的某种指定类型的异常。除了声明所捕获异常的类型之外，catch代码块还定义了针对该异常类型的异常处理器。在Java中，try代码块后面可以跟着多个catch代码块，来捕获不同类型的异常。Java虚拟机会从上至下匹配异常处理器。因此，前面的catch代码块所捕获的异常类型不能覆盖后边的，否则编译器会报错。
3. finally代码块：跟在try代码块和catch代码块之后，用来声明一段必定运行的代码。它的设计初衷是为了避免跳过某些关键的清理代码，例如关闭已打开的系统资源。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/f9/9e/833b272e.jpg" width="30px"><span>阿坤</span> 👍（62） 💬（2）<div>如果finally有return语句，catch内throw的异常会被忽略，这个从jvm层面怎么解释呢？</div>2018-09-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/f8/db/c4edf697.jpg" width="30px"><span>曲东方</span> 👍（42） 💬（2）<div>throw exception性能差fillstacktrace除了遍历堆栈以外，如果有inline 代码消除等编译优化发生，是不是要先“去优化”完了再fill？要不然可能出现错误堆栈和代码对不上的情况

throw exception估计也会影响jit的优化，进而影响整体性能

</div>2018-08-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d4/f3/129d6dfe.jpg" width="30px"><span>李二木</span> 👍（14） 💬（2）<div> 	看完今天的文章有几个疑问

   1方法的异常表是包含RuntimeException这种非check类型的异常吧？如果是那么每个方法都有异常表，那么是不是每个异常表中都有像ArrayIndexOutOfBoundsException这类型异常了。这类公共异常是私有还是共享呢

   2像catch自定义异常，也会添加的当前方法的异常表里吗？

   3 我们常常看到的异常调用栈，这里方法调用信息其实就是弹出方法栈帧吗？</div>2018-08-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/fe/59/29913e7b.jpg" width="30px"><span>吴伟</span> 👍（11） 💬（1）<div>检查异常和非检查异常也就是其他书籍中说的编译期异常和运行时异常？</div>2018-08-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/67/1e/40890f8f.jpg" width="30px"><span>李双迎</span> 👍（10） 💬（1）<div>老师，如果异常构造比较耗时，那么能否通过缓存同一位置相同异常的实例，来解决呢？</div>2018-09-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e1/a9/64a2fe3a.jpg" width="30px"><span>子清</span> 👍（5） 💬（1）<div>如果在业务层的代码中使用Assert来判断参数是否有问题，然后在调用方捕捉异常，这样会不会耗性能</div>2018-08-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/22/aa/c7725dd8.jpg" width="30px"><span>Ennis LM</span> 👍（4） 💬（1）<div>Java 虚拟机会忽略掉异常构造器以及填充栈帧的 Java 方法（Throwable.fillInStackTrace），直接从新建异常位置开始算起。
Java 虚拟机还会忽略标记为不可见的 Java 方法栈帧。

请问老师，填充栈帧的 Java 方法和不可见的 Java 方法栈帧，是什么</div>2018-08-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/99/4e/0146807f.jpg" width="30px"><span>兔子</span> 👍（3） 💬（1）<div>老师，您好！java.lang.Error这种错误产生的原因是什么样的？jvm对这种Error的处理方式跟Exception一样的吗？如果程序碰到这种情况为了确保程序还能正常运行加上try catch是否就可以了？谢谢！</div>2019-11-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c9/cb/7b6802cc.jpg" width="30px"><span>贾智文</span> 👍（3） 💬（1）<div>当触发异常的字节码的索引值在某个异常表条目的监控范围内，Java 虚拟机会判断所抛出的异常和该条目想要捕获的异常是否匹配。                        
这里有点没懂，每层方法的监控范围有可能会重叠吧，只用索引判断不会出现多个情况都满足的情况吗？</div>2018-08-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/39/f9/acfb9a48.jpg" width="30px"><span>无言的约定</span> 👍（0） 💬（1）<div>郑老师，问个问题，在执行某个方法时，我不知道在哪会发生异常，这个时候我怎么才能捕获可能产生的异常并存储在日志文件里？</div>2019-12-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/2b/8b/dd02189a.jpg" width="30px"><span>Randy</span> 👍（0） 💬（1）<div>郑老师，请教一下 ，文章中说下面这段代码编译出了3份finally 代码块，请问是怎么看出来的，请帮忙解读一下
public void test() {
    try {
      tryBlock = 0;
    } catch (Exception e) {
      catchBlock = 1;
    } finally {
      finallyBlock = 2;
    }
    methodExit = 3;
  }</div>2019-11-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a1/e6/50da1b2d.jpg" width="30px"><span>旭东(Frank)</span> 👍（0） 💬（1）<div>请问检查式异常的初衷是什么？经常因为检查式异常导致方法重构时，相应方法的封装性被破坏？

如何正确使用这两种异常，有何指导意见？谢谢</div>2018-08-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/51/6f/f33beea5.jpg" width="30px"><span>YIFENG</span> 👍（0） 💬（2）<div>老师，在讲复制finally部分的图中，复制到catch部分的finally右边的黄色虚线指向重新抛出异常，哪种情况会走到这条黄线路径呢？</div>2018-08-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（181） 💬（6）<div>感谢雨迪！
这节让我终于搞清楚了两个疑惑！

1:使用异常捕获的代码为什么比较耗费性能？
因为构造异常的实例比较耗性能。这从代码层面很难理解，不过站在JVM的角度来看就简单了，因为JVM在构造异常实例时需要生成该异常的栈轨迹。这个操作会逐一访问当前线程的栈帧，并且记录下各种调试信息，包括栈帧所指向方法的名字，方法所在的类名、文件名，以及在代码中的第几行触发该异常等信息。
虽然具体不清楚JVM的实现细节，但是看描述这件事情也是比较费时费力的。

2:finally是怎么实现无论异常与否都能被执行的？
这个事情是由编译器来实现的，现在的做法是这样的，编译器在编译Java代码时，会复制finally代码块的内容，然后分别放在try-catch代码块所有的正常执行路径及异常执行路径的出口中。


</div>2018-08-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/67/17/942e5115.jpg" width="30px"><span>wuyong</span> 👍（9） 💬（0）<div>```java
public class Foo {
    private int tryBlock;
    private int catchBlock;
    private int finallyBlock;
    private int methodExit;

    public void test() {
        try {
            tryBlock = 0;
        } catch (Exception e) {
            catchBlock = 1;
        } finally {
            finallyBlock = 2;
        }
        methodExit = 3;
    }
}
```

相当于如下的代码：

```java
public class Foo {
    private int tryBlock;
    private int catchBlock;
    private int finallyBlock;
    private int methodExit;

    public void test() {
        try {
            tryBlock = 0;
            finallyBlock = 2;
        } catch (Exception e) {
            catchBlock = 1;
            finallyBlock = 2;
        } catch (Throwable e) {
            finallyBlock = 2;
            throw e;
        }
        methodExit = 3;
    }
}
```</div>2020-08-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/11/cd/0e06bd0f.jpg" width="30px"><span>Krloy</span> 👍（5） 💬（2）<div>关于try catch的疑问

如果for里面中写 try catch 一百条数据中有1条数据异常 程序正常执行 会返回99条数据
如果for里面不写 try catch写外面 程序正常执行 但是数据返回0 

try catch 异常实例构造非常昂贵，因为虚拟机会生成改异常的栈轨迹，改操作会逐一访问改线程栈帧，并记录下各种调试信息。

那么如果我在for中写try catch 的话 会不会每次循环都生成一个异常实例？
上面两种写try catch的方法 哪种要更好点</div>2018-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/69/3d/abb7bfe3.jpg" width="30px"><span>Geek_8ra72c</span> 👍（3） 💬（2）<div>捕捉异常代码性能差是因为需要生成该异常的栈轨迹，就算不捕捉，也会打印该异常的的栈轨迹啊，那性能本来就差啊，何来捕捉异常性能差之说？</div>2019-04-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b7/37/36ce456f.jpg" width="30px"><span>王小臭</span> 👍（3） 💬（0）<div>辛苦老师了，这么早更新</div>2018-08-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4e/60/0d5aa340.jpg" width="30px"><span>gogo</span> 👍（2） 💬（2）<div>老师您好，请教一个问题，在spring项目中使用了统一异常处理，在service层做一些校验，校验失败时抛出异常，在统一异常处理逻辑里封装异常信息返回给客户端，这种场景自定义异常集成RuntimeException是不是比较好呢？</div>2019-09-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/d0/42/6fd01fb9.jpg" width="30px"><span>我已经设置了昵称</span> 👍（2） 💬（0）<div>对于实践环节表示看不懂字节码代码，无法理解，老师能不能在后篇解释下前篇遗留的问题</div>2019-03-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0d/bf/c8f343a3.jpg" width="30px"><span>南城风戈</span> 👍（2） 💬（0）<div>沙发</div>2018-08-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/30/c5/7d/38a7f6f2.jpg" width="30px"><span>spring~</span> 👍（1） 💬（0）<div>老师请问  代码监视器监视的不是 try的覆盖范围吗？  是不是可能编译后分为多个监视器 监视同一try{}块里的异常</div>2022-11-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/16/5b/83a35681.jpg" width="30px"><span>Monday</span> 👍（1） 💬（0）<div>动手实践最美丽：
Compiled from &quot;Foo.java&quot;
public class Foo {
  public Foo();
    Code:
       0: aload_0
       1: invokespecial #1                  &#47;&#47; Method java&#47;lang&#47;Object.&quot;&lt;init&gt;&quot;:()V
       4: return

  public void test();
    Code:
       0: aload_0
       1: iconst_0
       2: putfield      #2                  &#47;&#47; Field tryBlock:I
       5: aload_0
       6: iconst_2
       7: putfield      #3                  &#47;&#47; Field finallyBlock:I
      10: goto          35
      13: astore_1
      14: aload_0
      15: iconst_1
      16: putfield      #5                  &#47;&#47; Field catchBlock:I
      19: aload_0
      20: iconst_2
      21: putfield      #3                  &#47;&#47; Field finallyBlock:I
      24: goto          35
      27: astore_2
      28: aload_0
      29: iconst_2
      30: putfield      #3                  &#47;&#47; Field finallyBlock:I
      33: aload_2
      34: athrow
      35: aload_0
      36: iconst_3
      37: putfield      #6                  &#47;&#47; Field methodExit:I
      40: return
    Exception table:
       from    to  target type
           0     5    13   Class java&#47;lang&#47;Exception
           0     5    27   any
          13    19    27   any
}
</div>2020-07-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/13/56/6a062937.jpg" width="30px"><span>gentleman♥️</span> 👍（1） 💬（0）<div>就是checked异常 一直不try catch ，jvm会怎么个处理流程呢</div>2019-01-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/53/ab/587173ca.jpg" width="30px"><span>编程的德彪</span> 👍（1） 💬（0）<div>这一篇是看的明白的的一篇。😂</div>2018-11-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/04/b5/8bc4790b.jpg" width="30px"><span>Geek_987169</span> 👍（1） 💬（0）<div>老师，请教您一个问题，jvm在执行字节码指令的过程中，在什么情况下会由顺序执行变为跳转执行？</div>2018-09-12</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erk8f6IVErdbicJhx7p9VrbrGNpIcVUXyxQnSX529LicF9YX9AUQvnrTTRjibk1R7LVXfNd7oxbsFR8Q/132" width="30px"><span>苦酒入喉吨吨吨</span> 👍（0） 💬（0）<div>在编译期，带有try-catch的方法编译为字节码，会有如下的处理：
    - 在方法字节码最后，增加一个异常表，异常表每一项都有：from、to、target、异常类型，from和to表示该处理器负责的字节码行号范围，target 表示异常处理器（如catch块）的起始位置（字节码行号），异常类型表示这个项能处理哪些类型的异常；
    - 每个catch都会对应一个表项，target 指向的是catch代码块，异常类型也是一个确定的Exception名字。
    - finally也会生成一个表项，不过finally的表项很特殊：from-to的范围覆盖了整个try + catch块，target 指向的是插入的finally块，异常类型是any。为什么finally 也要生成一个表项？ 因为catch块也可能抛异常，这时就需要这个表项来处理了；
    - 为了保证finally块一定被执行，编译器会把finally代码块，插入到所以可能的路径出口处，也就意味着finally代码块越长，这个方法里额外增加的字节码就越多。
运行时，如果抛出异常，JVM 处理过程如下：
    - 先去异常表里查询，如果from-to符合、异常类型也符合，则跳转到 target 的字节码
    - 如果是 catch 的表项，那么就不会向外抛异常了；
    - 如果所有的 catch的表项都不符合条件，或者catch 也抛异常了，就会跳到finally 的表项处理：跳到插入的finally块并执行，然后向外抛异常


</div>2023-05-26</li><br/><li><img src="" width="30px"><span>Geek_9c691e</span> 👍（0） 💬（0）<div>有一个疑问：为什么主动catch住的异常，处理之后不会继续抛出。而编译器帮助添加的any异常条目，处理完finally之后，会继续抛出异常呢？这2中异常条目在jvm层面的处理不一样吗？</div>2023-05-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/4c/dd/c6035349.jpg" width="30px"><span>Bumblebee</span> 👍（0） 💬（0）<div>今日收获

①  抛异常的方式分为显示抛异常（程序中使用throw关键字进行抛异常）与隐式抛异常（Java虚拟机在运行中碰到无法继续的异常状态自动抛出，例如数组越界异常）；

②  Java中所有异常都是Throwable类或其子类的实例；

③  Throwable有两大直接子类，第一类是Error（涵盖程序不能捕获的异常，当触发Error时执行状态已经无法恢复需要中断当前线程甚至是虚拟机）第二类是Exception（典型的代表是RuntimeException异常，表示程序虽然被中断但是还可以进行挽救）；

④  RuntimeException与Error在Java属于非检查异常（抛异常的所在方法可以不进行throws关键字申明），其他属于受检查异常（需要在抛异常的方法声明throws关键字将异常抛出）；

⑤  异常实例的构造非常昂贵（因为在构造异常实例时Java虚拟机会逐一访该线程的Java栈帧并记录调用链上的详细信息，包括栈帧所指的方法名字方法所在的类名文件名以及抛异常的代码行数）；
当然，在生成栈轨迹时，Java 虚拟机会忽略掉异常构造器以及填充栈帧的 Java 方法（Throwable.fillInStackTrace），直接从新建异常位置开始算起。此外，Java 虚拟机还会忽略标记为不可见的 Java 方法栈帧；

⑤  Java虚拟机是如何捕获异常的？
      1）进行了异常捕获的代码在生成字节码后，方法会携带一个异常表，异常表中每个条目代表一个异常处理器，每个异常处理器包含（from，to，target指针，以及捕获的异常类型所组成）

      2）from，to，target这些指针是字节码索引，用以定位字节码（from与to指针指向try代码块的起始位置，target指向异常处理器的起始位置，catch代码块的起始位置）；
      3）代码示例；
源码：
public class Test {
    public static void main(String[] args) {
        try {
            int try_i =1;
        } catch (RuntimeException e) { }
    }
}
反编译字节码：
Compiled from &quot;Test.java&quot;
public class org.example.nio.test.Test {
  public org.example.nio.test.Test();
    Code:
       0: aload_0
       1: invokespecial #1                  &#47;&#47; Method java&#47;lang&#47;Object.&quot;&lt;init&gt;&quot;:()V
       4: return

  public static void main(java.lang.String[]);
    Code:
       0: iconst_1
       1: istore_1
       2: goto          6
       5: astore_1
       6: return
    Exception table:
       from    to  target type
           0     2     5  </div>2022-05-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/a6/9f/3c60fffd.jpg" width="30px"><span>青阳</span> 👍（0） 💬（0）<div>不记得在哪看过一句，程序运行时抛出RuntimeException，都是和代码逻辑错误有关系，所以抛出这个异常的时候要修复代码了</div>2021-04-25</li><br/>
</ul>