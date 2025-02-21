在开始今天的学习前，我建议你先复习一下[专栏第6讲](http://time.geekbang.org/column/article/7489)有关动态代理的内容。作为Java基础模块中的内容，考虑到不同基础的同学以及一个循序渐进的学习过程，我当时并没有在源码层面介绍动态代理的实现技术，仅进行了相应的技术比较。但是，有了[上一讲](http://time.geekbang.org/column/article/9946)的类加载的学习基础后，我想是时候该进行深入分析了。

今天我要问你的问题是，有哪些方法可以在运行时动态生成一个Java类？

## 典型回答

我们可以从常见的Java类来源分析，通常的开发过程是，开发者编写Java代码，调用javac编译成class文件，然后通过类加载机制载入JVM，就成为应用运行时可以使用的Java类了。

从上面过程得到启发，其中一个直接的方式是从源码入手，可以利用Java程序生成一段源码，然后保存到文件等，下面就只需要解决编译问题了。

有一种笨办法，直接用ProcessBuilder之类启动javac进程，并指定上面生成的文件作为输入，进行编译。最后，再利用类加载器，在运行时加载即可。

前面的方法，本质上还是在当前程序进程之外编译的，那么还有没有不这么low的办法呢？

你可以考虑使用Java Compiler API，这是JDK提供的标准API，里面提供了与javac对等的编译器功能，具体请参考[java.compiler](https://docs.oracle.com/javase/9/docs/api/javax/tools/package-summary.html)相关文档。
<div><strong>精选留言（15）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/0c/49/d71e939d.jpg" width="30px"><span>三口先生</span> 👍（71） 💬（1）<div>将资源消耗的这个实例，用动态代理的方式创建这个实例动态代理对象，在动态代理的invoke中添加新的需求。开始使用代理对象，不开启则使用原来的方法，因为动态代理是在运行时创建。所以是零消耗。</div>2018-06-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f3/9f/3e4e8d46.jpg" width="30px"><span>tyson</span> 👍（59） 💬（4）<div>可以考虑用javaagent+字节码处理拦截方法进行统计：对httpclient中的方法进行拦截，增加header或者转发等进行统计。开启和关闭只要增加一个javaagent启动参数就行</div>2018-07-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/da/c4/270db3ad.jpg" width="30px"><span>ZoQ-tans</span> 👍（16） 💬（2）<div>老师，您这个专栏完结了还会不会出其他专栏，你的每一篇我起码要听三四遍，我都是咬文嚼字的听，非常有用，非常好的内功心法</div>2018-06-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/dd/b6/fcf322a7.jpg" width="30px"><span>antipas</span> 👍（15） 💬（1）<div>无痕埋点原理就是这样。像注解类框架也用到了比如retrofit</div>2018-06-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/0c/e1/e54540b9.jpg" width="30px"><span>冯宇</span> 👍（12） 💬（1）<div>还可以基于JVM实现各种动态语言。比如groovy就是使用java开发的动态脚本语言</div>2018-09-30</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/JooolCyKac0KOswuGiavSmiaOYYHemuGv3JgVGmnOQpcwgVe9akTMdibrtSR9vS8f64vRbYJKMrnibMmOBxCxibhfzg/132" width="30px"><span>胡馥春</span> 👍（4） 💬（1）<div>所有用到java反射的地方，底层都是采用了字节码操纵技术，老师，这么理解对吗？</div>2018-07-05</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIicRlf8vZguE6KpS8FEjpaheGbB3UZojKWTn501r2KLe3I3F7NlpSSpMZpaCcs5PBtR1nCHMHYcrA/132" width="30px"><span>mojo</span> 👍（2） 💬（2）<div>请问老师，使用classloader动态加载的外部jar包，应该如何正确的卸载？已经加载到systemclassloader……通过反射urlclassloader的addurl方法加进去的</div>2018-07-17</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTI163RiaQQTh7PJY0ic03rKicwKSWAomD5xjcYAzFYrTSZmZL6OpvW8WeRVaZvnGCWBzwpar9EVuIDBg/132" width="30px"><span>rivers</span> 👍（6） 💬（0）<div>希望作者能详细的讲下，javaassist等其他代理模式的使用，砍掉了很多内容，尽量考虑下水平有限的读者</div>2018-07-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/ba/ec/2b1c6afc.jpg" width="30px"><span>李飞</span> 👍（2） 💬（0）<div>越来越底层了，也越来越吃力，看来需要反复阅读才能吃透了</div>2020-05-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/75/88/fd024a11.jpg" width="30px"><span>朱震震</span> 👍（2） 💬（0）<div>为什么需要动态加载，这个部分对系统有没有影响，会带来什么好处和坏处，痛点在哪，这些需要思考清楚。
好处解耦，实现动态的载入和卸载，监控等。缺点就是整体系统维护复杂度增高。这个技术通俗的理解就是使用了封装jvm识别的指令，然后生成字节码，然后使用加载类的方式加载，生成。具体细节还要详细研究</div>2020-03-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/07/8c/0d886dcc.jpg" width="30px"><span>蚂蚁内推+v</span> 👍（2） 💬（0）<div>老师在讲一些知识的时候，会提及到前面相关的章节，觉得特别赞，可以提醒我们去复习前面的章节，不至于学了后面忘了前面~~老师时不时可以来一些这样的提醒😁</div>2019-04-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/76/48/5ab89daa.jpg" width="30px"><span>护爽使者</span> 👍（1） 💬（0）<div>反射，动态代理等</div>2020-03-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0b/34/f41d73a4.jpg" width="30px"><span>王盛武</span> 👍（1） 💬（0）<div>老师好, 请问&quot;newProxyInstance 生成代理类实例的时候&quot;,  这里是用 hard-code生成字节码,
为何您这里选用的是ASM的例子呢?  上文提到了JDK里ASM是用在LamdaFrom, 不是newProxyInstance里哦</div>2019-11-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a5/85/eeb5b42f.jpg" width="30px"><span>多格</span> 👍（1） 💬（0）<div>1. Proxy.newProxyInstance
2. Class&lt;?&gt; cl = getProxyClass0(loader, interfaces);
3.     private static final WeakCache&lt;ClassLoader, Class&lt;?&gt;[], Class&lt;?&gt;&gt;
        proxyClassCache = new WeakCache&lt;&gt;(new KeyFactory(), new ProxyClassFactory());
4.value = Objects.requireNonNull(valueFactory.apply(key, parameter));
5.interfaceClass = Class.forName(intf.getName(), false, loader);
6.Verify that the Class object actually represents an interface [限制只能是接口]
7.             byte[] proxyClassFile = ProxyGenerator.generateProxyClass(
                proxyName, interfaces, accessFlags);
8.return defineClass0(loader, proxyName,
                                    proxyClassFile, 0, proxyClassFile.length);
</div>2019-04-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/14/b1/7d974f0a.jpg" width="30px"><span>黄明恩</span> 👍（1） 💬（0）<div>所谓零开销是指哪部分开销，做个统计的开关逻辑不就好了，硬套动态代理来实现感觉有点</div>2018-07-28</li><br/>
</ul>