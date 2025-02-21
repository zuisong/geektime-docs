我们经常会遇见Java语言较难表达，甚至是无法表达的应用场景。比如我们希望使用汇编语言（如X86\_64的SIMD指令）来提升关键代码的性能；再比如，我们希望调用Java核心类库无法提供的，某个体系架构或者操作系统特有的功能。

在这种情况下，我们往往会牺牲可移植性，在Java代码中调用C/C++代码（下面简述为C代码），并在其中实现所需功能。这种跨语言的调用，便需要借助Java虚拟机的Java Native Interface（JNI）机制。

关于JNI的例子，你应该特别熟悉Java中标记为`native`的、没有方法体的方法（下面统称为native方法）。当在Java代码中调用这些native方法时，Java虚拟机将通过JNI，调用至对应的C函数（下面将native方法对应的C实现统称为C函数）中。

```
public class Object {
  public native int hashCode();
}
```

举个例子，`Object.hashCode`方法便是一个native方法。它对应的C函数将计算对象的哈希值，并缓存在对象头、栈上锁记录（轻型锁）或对象监视锁（重型锁所使用的monitor）中，以确保该值在对象的生命周期之内不会变更。

## native方法的链接

在调用native方法前，Java虚拟机需要将该native方法链接至对应的C函数上。
<div><strong>精选留言（14）</strong></div><ul>
<li><img src="" width="30px"><span>Scott</span> 👍（6） 💬（3）<div>$ java -Djava.library.path=&#47;PATH&#47;TO&#47;DIR&#47;CONTAINING&#47;libfoo.dylib org.example.Foo
Hello, World
这个地方应该是只写路径，不要把文件名加上</div>2018-10-05</li><br/><li><img src="" width="30px"><span>Scott</span> 👍（3） 💬（1）<div>HotSpot 虚拟机是通过句柄（handle）来完成上述需求的。

句柄是不是只是移动对象时使用，如果每次访问引用都要读内存两次，那性能影响严重</div>2018-10-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/b5/ff/d1f205b0.jpg" width="30px"><span>L</span> 👍（13） 💬（0）<div>JNI 的运行机制：

    1. Java 中的 native 方法的链接方式主要有两种：
        1、自动链接
            按照 JNI 的默认规范命名所要链接的 C 函数，并依赖于 Java 虚拟机自动链接。

        2、主动链接
            另一种则是在 C 代码中主动链接。

    2. JNI 提供了一系列 API 来允许 C 代码使用 Java 语言特性。
        1、映射了 Java ⇋ C 的 基本数据类型 和 引用数据类型          int -&gt; jint ...
        2、异常处理

    3. 防止 C代码 中 引用到的 Java对象被 JVM GC
        在C代码中，可以访问传入的引用类型参数，也可以 通过 JNI API 创建新的 Java 对象。
        Java 虚拟机需要一种机制，来告知垃圾回收算法，不要回收这些 C 代码中可能引用到的 Java 对象。
            -- JNI 的 局部引用（Local Reference）和 全局引用（Global Reference）
            这两者都可以 阻止垃圾回收器 回收 被引用的 Java对象。
            不同的是，局部引用 在 native 方法调用返回之后便会失效。传入参数 以及大部分 JNI API 函数的返回值 都属于 局部引用。

    4. JNI 的额外性能开销
        1、进入 C 函数时，对引用类型参数的句柄化，和调整参数位置（C 调用和 Java 调用传参的方式不一样）
        2、从 C 函数返回时，清理线程私有句柄块</div>2020-07-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/22/7b/be15e8a2.jpg" width="30px"><span>libbylg</span> 👍（7） 💬（0）<div>据说JNI的性能很差，请问这个是否是事实，如果有这个问题，那么是否有提高性能的方法</div>2018-10-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c0/6c/29be1864.jpg" width="30px"><span>随心而至</span> 👍（4） 💬（0）<div> linux下生成文中对应libfoo.so命令如下：
 gcc -I$JAVA_HOME&#47;include -I$JAVA_HOME&#47;include&#47;linux -fPIC -o libfoo.so -shared foo.c
另外：System.load和System.loadLibrary 可以互换。
动手做一下，就明白了。</div>2019-10-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/fd/59/4416b40f.jpg" width="30px"><span>德惠先生</span> 👍（2） 💬（0）<div>老师好像没有提到GC_LOCKER机制，并不是所有引用都会被gc直接略过</div>2020-03-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/66/e9/814d057a.jpg" width="30px"><span>小陈</span> 👍（1） 💬（0）<div>不错，之前不懂的懂了</div>2020-03-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/99/af/d29273e2.jpg" width="30px"><span>饭粒</span> 👍（1） 💬（0）<div>Linux:
# javac -h . org&#47;example&#47;Foo.java
# 
# gcc -I$JAVA_HOME&#47;include -I$JAVA_HOME&#47;include&#47;linux -fPIC -o libfoo.so -shared foo.c
# 
# tree .&#47;
.&#47;
├── foo.c
├── libfoo.so
├── org
│   └── example
│       ├── Foo.class
│       └── Foo.java
└── org_example_Foo.h

2 directories, 5 files
# java -Djava.library.path=. org.example.Foo
Hello, World</div>2019-12-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/08/96/231fdd9e.jpg" width="30px"><span>未知</span> 👍（1） 💬（0）<div>在《深入理解jvm》第二版一书中，2.3.3章节讲述对象访问定位时提到，Hotspot是使用直接指针而不是句柄去访问对象的。是否是Java内部访问时使用的直接指针而native时使用的句柄？？</div>2018-12-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/44/47/3ddb94d0.jpg" width="30px"><span>javaadu</span> 👍（1） 💬（0）<div>（1）JNI中也需要考虑对异常的处理
（2）JNI中通过句柄引用java对象，
（3）垃圾回收器会忽略jni中的局部引用和全局引用</div>2018-10-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/63/14/06eff9a4.jpg" width="30px"><span>Jerry银银</span> 👍（0） 💬（0）<div>两种链接方法分别适用于什么场景？</div>2022-07-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ec/13/49e98289.jpg" width="30px"><span>neohope</span> 👍（0） 💬（0）<div>老师，请问一下，使用JNI的时候，要考虑JDK版本与编译器版本的问题吗？我曾经在Windows下用JNI写过一些库，都是静态编译的，但实际测试时，发现不同版本的JDK，有时候要用不同版本的编译器。没法做到一个lib完全通用，感觉很奇怪。（不是32或64，而是vs2010，vs2015，vs2017这些。）</div>2019-09-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/4b/19/6f037647.jpg" width="30px"><span>东方</span> 👍（0） 💬（1）<div>老师: A类的方法a()调用C++ ，fork一个进程后，在子进程回调A#a()。a()打印了类的id，前后两个进程打印id是一样的。我的问题是，fork进程后，JVM还是同一个实例？

</div>2019-04-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/10/e2/28c09cf5.jpg" width="30px"><span>平淡</span> 👍（0） 💬（0）<div>请问这个JNIENV的参数，是当前执行native函数线程的JNIENV吗？线程的JNIENV是什么时候赋值的呢，找了好久也没找到，谢谢！</div>2018-11-28</li><br/>
</ul>