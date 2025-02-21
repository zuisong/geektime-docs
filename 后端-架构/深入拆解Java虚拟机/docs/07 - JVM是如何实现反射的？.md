今天我们来聊聊Java里的反射机制。

反射是Java语言中一个相当重要的特性，它允许正在运行的Java程序观测，甚至是修改程序的动态行为。

举例来说，我们可以通过Class对象枚举该类中的所有方法，我们还可以通过Method.setAccessible（位于java.lang.reflect包，该方法继承自AccessibleObject）绕过Java语言的访问权限，在私有方法所在类之外的地方调用该方法。

反射在Java中的应用十分广泛。开发人员日常接触到的Java集成开发环境（IDE）便运用了这一功能：每当我们敲入点号时，IDE便会根据点号前的内容，动态展示可以访问的字段或者方法。

另一个日常应用则是Java调试器，它能够在调试过程中枚举某一对象所有字段的值。

![](https://static001.geekbang.org/resource/image/ce/75/ceeabb2dbdd80577feaecd0879e42675.png?wh=628%2A466)

（图中eclipse的自动提示使用了反射）

在Web开发中，我们经常能够接触到各种可配置的通用框架。为了保证框架的可扩展性，它们往往借助Java的反射机制，根据配置文件来加载不同的类。举例来说，Spring框架的依赖反转（IoC），便是依赖于反射机制。

然而，我相信不少开发人员都嫌弃反射机制比较慢。甚至是甲骨文关于反射的教学网页\[1]，也强调了反射性能开销大的缺点。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/eb/1a/579c941e.jpg" width="30px"><span>志远</span> 👍（116） 💬（7）<div>老师您好，提个建议，您讲课过程中经常提到一些概念名词，您讲课总是预设了一个前提，就是假设我们已经知道那个概念，然而并不清楚。比如本文中被不断提到的内联，什么是内联呢？</div>2018-08-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/37/30/bbf76b79.jpg" width="30px"><span>xiaguangme</span> 👍（62） 💬（1）<div>开发人员日常接触到的 Java 集成开发环境（IDE）便运用了这一功能：每当我们敲入点号时，IDE 便会根据点号前的内容，动态展示可以访问的字段或者方法。&#47;&#47;这个应该是不完全正确的，大部分应该是靠语法树来实现的。</div>2018-08-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/04/9a/f2c0a206.jpg" width="30px"><span>ext4</span> 👍（26） 💬（1）<div>雨迪您好，我有两个问题：

一是我自己的测试结果和文章中有些出入。在我自己的mac+jdk10环境中，v3版本的代码和v2版本性能是差不多的，多次测试看v3还略好一些。从v2的GC log来看for循环的每一亿次iteration中间都会有GC发生，似乎说明这里的escape analysis并没有做到allocation on stack。您能想到这是什么原因么？另有个小建议就是文章中提到测试结果时，注明一下您的环境。

另一个问题是在您v5版本的代码中，您故意用method1和method2两个对象霸占了2个ProfileType的位子，导致被测的反射操作性能很低。这是因为此处invoke方法的inline是压根儿就没有做呢？还是因为inline是依据target1或者target2来做的，而实际运行时发现类型不一致又触发了deoptimization呢？

望解答，谢谢~</div>2018-08-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/03/90/2312c3fb.jpg" width="30px"><span>夜空</span> 👍（16） 💬（3）<div>当某个反射调用的调用次数在 15 之下时，采用本地实现；当达到 15 时，便开始动态生成字节码...
———可以认为第16次反射调用时的耗时是最长的吗？</div>2018-08-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/86/a8/427879a9.jpg" width="30px"><span>搬砖匠</span> 👍（15） 💬（3）<div>请教一个问题，本地实现可以用java来替代c++的实现方式吗？这样就可以避过C++的额外开销？</div>2018-09-08</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTK9RytLsauRVYGjupDIaibibAK5iaicEicONrMFc0O3icAGf5mD1buxoQ2ePPn9YurFhRbuf3AR1qJDy0GQ/132" width="30px"><span>星文友</span> 👍（14） 💬（3）<div>给大家讲个笑话：
我负责的项目中有大量动态生成的类，这些类实例的调用原本都是通过反射去完成，后来我觉得反射效率低，就为每个动态类的每个方法在动态生成一个代理类，这个代理类就是进行类型强转然后直接调用。后来在压测环境进行测试，发现并无卵用，早点开到这篇文章我就不用做这么多无用功了。特么的JVM已经有这个功能了啊</div>2018-11-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/fe/15/ccda05bb.jpg" width="30px"><span>Kisho</span> 👍（14） 💬（1）<div>郑老师，你好,
       “动态实现无需经过Java到C++再到Java的切换”,这句话没太明白，能在解释下么？</div>2018-08-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/70/fc/77f60338.jpg" width="30px"><span>Stephen</span> 👍（12） 💬（1）<div>老师，有三个知识点不太明白，分别是:内联、逃逸分析以及inflation机制</div>2018-11-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/dc/65/3da02c30.jpg" width="30px"><span>once</span> 👍（10） 💬（1）<div>请问老师 是不是本地方法的性能一般都不是很好呢</div>2018-09-07</li><br/><li><img src="" width="30px"><span>Scott</span> 👍（7） 💬（1）<div>有两个问题：
1.v3版本中，确定不逃逸的数组可以优化访问，这个是怎么做的？
2.v5版本中，为啥逃逸分析会失效，明明都封闭在循环里的？</div>2018-08-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/eb/1a/579c941e.jpg" width="30px"><span>志远</span> 👍（7） 💬（1）<div>文章中“一亿次直接调用耗费的时间大约在 120ms。这和不调用的时间是一致的。”这句话是不是病句啊？不调用指的是什么？指的是直接调用吗？</div>2018-08-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（5） 💬（2）<div>老师请教个问题，如果手动修改某个Java字节码文件，如果JVM不重新加载此文件，有什么方式能让JVM识别并执行修改的内容呢？
如果一定需要JVM加载后才能识别并执行，有什么好的手动触发的方法呢？</div>2018-08-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/35/2c/429323f3.jpg" width="30px"><span>姬野用菜刀</span> 👍（3） 💬（1）<div>因此，我们应当避免在热点代码中使用返回 Method 数组的 getMethods 或者 getDeclaredMethods 方法，以减少不必要的堆空间消耗。

这个地方没有太明白，老师能帮忙在细讲一下嘛？</div>2018-08-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/7f/2f/b4a925bd.jpg" width="30px"><span>阿康</span> 👍（3） 💬（1）<div>请问，反射第16次生成字节码的用的什么方式阿？和asm有什么区别呢？</div>2018-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/eb/63/09e7f442.jpg" width="30px"><span>溯雪</span> 👍（2） 💬（1）<div>啊，不知道这么久了，老师还会不会回复

说起变长数组，我发现jdk9新增的Set.of方法重载了许多:

```
static &lt;E&gt; Set&lt;E&gt; of(E e1) {
        return new ImmutableCollections.Set12&lt;&gt;(e1);
    }
static &lt;E&gt; Set&lt;E&gt; of(E e1, E e2) {
        return new ImmutableCollections.Set12&lt;&gt;(e1, e2);
    }
   static &lt;E&gt; Set&lt;E&gt; of(E e1, E e2, E e3) {
        return new ImmutableCollections.SetN&lt;&gt;(e1, e2, e3);
    }

&#47;&#47;&#47;&#47;&#47;一直到10个参数
    static &lt;E&gt; Set&lt;E&gt; of(E... elements) {
        switch (elements.length) { &#47;&#47; implicit null check of elements
            case 0:
                return ImmutableCollections.emptySet();
            case 1:
                return new ImmutableCollections.Set12&lt;&gt;(elements[0]);
            case 2:
                return new ImmutableCollections.Set12&lt;&gt;(elements[0], elements[1]);
            default:
                return new ImmutableCollections.SetN&lt;&gt;(elements);
        }
    }
```
然而ImmutableCollections.SetN又是个变长数组，那么重载的1~10个参数方法是图个啥。。</div>2018-11-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d9/c6/a295275b.jpg" width="30px"><span>o</span> 👍（2） 💬（2）<div>请问，这个15次，他是怎么记录的呢？是否仍然占用jvm的内存，如果占用是属于那个区域呢？麻烦您可以给讲讲吗？谢谢</div>2018-08-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/f6/e3/e4bcd69e.jpg" width="30px"><span>沉淀的梦想</span> 👍（1） 💬（2）<div>在v5版本中，为什么我设置TypeProfileWidth为3，速度并没有变快呢？</div>2018-08-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c0/71/c83d8b15.jpg" width="30px"><span>一个坏人</span> 👍（1） 💬（1）<div>老师好，请教一个问题。当某个反射调用的调用次数在 15 之下时，采用本地实现；当达到 15 时，便开始动态生成字节码...
———可以认为第16次反射调用时的耗时是最长的吗？如果刚好只调用16次是不是就不划算了？</div>2018-08-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/75/65/2a7f8212.jpg" width="30px"><span>小明</span> 👍（26） 💬（3）<div>可以看看这篇博客 有详细的生成动态调用的解释  
http:&#47;&#47;rednaxelafx.iteye.com&#47;blog&#47;548536</div>2018-08-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（25） 💬（2）<div>小结
1:反射机制是Java语言的一个非常重要的特性，通过这个特性，我们能够动态的监控、调用、修改类的行为，许多的框架实现就用到了Java语言反射的机制

2:使用反射挺好的，但它也是不完美的，复杂的操作往往更耗时间和精力，使用反射也是一样，性能低下是她所被人诟病的一个地方，那为什么方法的反射如此耗费性能呐？它的性能耗在那里呢？方法的反射调用会带来不少性能开销，原因主要有三个：变长参数方法导致的 Object 数组，基本类型的自动装箱、拆箱，还有最重要的方法内联。</div>2018-08-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/49/df/abb7bfe3.jpg" width="30px"><span>且听风吟</span> 👍（20） 💬（8）<div>看到inflation这块还是比较有深刻感触的。一次线上环境发现metasapce周期性打爆导致full GC，后来根据dump分析到，由于引入了一些中间件的关系，很多实用代理反射的方式生成了很多字节码，后来把inflation阈值调整到int.max就没问题了</div>2019-10-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/fd/08/c039f840.jpg" width="30px"><span>小鳄鱼</span> 👍（9） 💬（0）<div>不是同个对象，但equal。老师说了，返回的是目标方法的一份拷贝</div>2018-11-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/70/fc/77f60338.jpg" width="30px"><span>Stephen</span> 👍（7） 💬（2）<div>老师，有三个知识点不太明白:内联、逃逸分析以及inflation机制</div>2018-11-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/08/4e/87e40222.jpg" width="30px"><span>Yoph</span> 👍（4） 💬（1）<div>MethodAccessor实例创建在ReflectionFactory中，如下代码：
public class ReflectionFactory {  
    private static boolean noInflation        = false;  
    private static int     inflationThreshold = 15;  
   
    public MethodAccessor newMethodAccessor(Method method) {  
        checkInitted();  
        if (noInflation) {  
            return new MethodAccessorGenerator().  
                generateMethod(method.getDeclaringClass(),  
                               method.getName(),  
                               method.getParameterTypes(),  
                               method.getReturnType(),  
                               method.getExceptionTypes(),  
                               method.getModifiers());  
        } else {  
            NativeMethodAccessorImpl acc =  
                new NativeMethodAccessorImpl(method);  
            DelegatingMethodAccessorImpl res =  
                new DelegatingMethodAccessorImpl(acc);  
            acc.setParent(res);  
            return res;  
        }  
    }  
}  

实际的MethodAccessor实现有两个版本，一个是Java实现的，另一个是native code实现的。</div>2018-11-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/66/75/54bb858e.jpg" width="30px"><span>life is short, enjoy more.</span> 👍（3） 💬（0）<div>总结一下
反射有两种实现方式：

本地方法调用（就是字节码中已经定义好的方法）

动态生成字节码


两者有什么区别？

动态生成字节码（以下简称动态实现），生成字节码的过程很慢（类似于准备工作），但是执行效率高。

本地方法调用，不用生成字节码，直接调用本地方法。所以准备工作几乎没有，很快。但是执行效率就差很多。


JVM如何做决定选择哪种实现方式？

通过反射执行的次数来决定，默认值是15。15次之前直接本地调用，之后动态实现。


JVM为啥分两种实现方式？

本地实现的调用流程复杂。而在执行多次的情况下，复杂意味着性能损耗，所以有一种适合多次执行的解决方案，就是动态生成字节码。

</div>2018-10-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/22/aa/c7725dd8.jpg" width="30px"><span>Ennis LM</span> 👍（2） 💬（0）<div>最后的问题，==是false，equals是true，对性能的影响我不知道怎么看。。。</div>2018-08-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（2） 💬（1）<div>JVM加载了一个Java字节码文件，在不停止JVM的情况下能再次的加载同一个Java字节码文件吗？如果能是覆盖了原来的那个Java字节码文件还是怎么着了呢？
在IDE中是可以直接修改Java源代码的，然后可以手动触发Java源代码的编译和重新加载，请问老师知道IDE是怎么实现的吗？</div>2018-08-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0c/52/f25c3636.jpg" width="30px"><span>长脖子树</span> 👍（1） 💬（0）<div>为什么不用 native 方法, 而使用java代码实现? 
跨越native边界会对优化有阻碍作用，它就像个黑箱一样让虚拟机难以分析也将其内联，于是运行时间长了之后反而是托管版本的代码更快些。
参考: R大博客 http:&#47;&#47;rednaxelafx.iteye.com&#47;blog&#47;548536
</div>2020-05-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/13/8c/c86340ca.jpg" width="30px"><span>巴西</span> 👍（1） 💬（0）<div>有点难啊</div>2019-11-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0c/52/f25c3636.jpg" width="30px"><span>长脖子树</span> 👍（1） 💬（0）<div>经过 polluteProfile 之后的代码
在参数 -XX:TypeProfileWidth=3 -Dsun.reflect.noInflation=true 条件下
jdk 1.8.0_212-release 上最后5次平均 732ms
openjdk11 (build 11+28) 上最后5次平均 269ms 
差距还是很大的, 大家记得认准版本号啊
</div>2019-11-01</li><br/>
</ul>