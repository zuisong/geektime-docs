我在读博士的时候，最怕的事情就是被问有没有新的Idea。有一次我被老板问急了，就随口说了一个。

这个Idea究竟是什么呢，我们知道，设计模式大量使用了虚方法来实现多态。但是虚方法的性能效率并不高，所以我就说，是否能够在此基础上写篇文章，评估每一种设计模式因为虚方法调用而造成的性能开销，并且在文章中强烈谴责一下？

当时呢，我老板教的是一门高级程序设计的课，其中有好几节课刚好在讲设计模式的各种好处。所以，我说完这个Idea，就看到老板的神色略有不悦了，脸上写满了“小郑啊，你这是舍本逐末啊”，于是，我就连忙挽尊，说我是开玩笑的。

在这里呢，我犯的错误其实有两个。第一，我不应该因为虚方法的性能效率，而放弃良好的设计。第二，通常来说，Java虚拟机中虚方法调用的性能开销并不大，有些时候甚至可以完全消除。第一个错误是原则上的，这里就不展开了。至于第二个错误，我们今天便来聊一聊Java虚拟机中虚方法调用的具体实现。

首先，我们来看一个模拟出国边检的小例子。

```
abstract class Passenger {
  abstract void passThroughImmigration();
  @Override
  public String toString() { ... }
}
class ForeignerPassenger extends Passenger {
	 @Override
 	void passThroughImmigration() { /* 进外国人通道 */ }
}
class ChinesePassenger extends Passenger {
  @Override
  void passThroughImmigration() { /* 进中国人通道 */ }
  void visitDutyFreeShops() { /* 逛免税店 */ }
}

Passenger passenger = ...
passenger.passThroughImmigration();
```

这里我定义了一个抽象类，叫做Passenger，这个类中有一个名为passThroughImmigration的抽象方法，以及重写自Object类的toString方法。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/51/96/53ffbb95.jpg" width="30px"><span>啊一大狗</span> 👍（26） 💬（0）<div>这套课很好，谢谢！</div>2018-07-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/fa/29/f1ede67b.jpg" width="30px"><span>Tony</span> 👍（69） 💬（1）<div>同提建议，代码使用英文。刚学java基础时，有老师为了便于理解用中文命名。现在都来学jvm，对java很熟悉了，看到中文不仅不会觉得通俗易懂，反而特别别扭。</div>2018-07-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ec/9d/4d705f03.jpg" width="30px"><span>C_love</span> 👍（25） 💬（1）<div>提个小建议，能否在代码中都使用英文？毕竟使用中文作对象名不值得提倡</div>2018-07-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（18） 💬（2）<div>老师问一个概念性的问题： 虚方法 到底在指什么样的 方法？
也就是什么样的方法，才叫做虚方法？</div>2019-12-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7b/c0/517781b8.jpg" width="30px"><span>左岸🌸开</span> 👍（18） 💬（8）<div>为什么调用超类非私有实例方法会属于静态绑定呢？</div>2018-07-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/31/f4/467cf5d7.jpg" width="30px"><span>MARK</span> 👍（10） 💬（1）<div>没用过中文写代码，居然认为中文会编译错误T﹏T
老师是为了课件方便这样写，自己写作业就改下呗，又没规定要每个字照抄
[root@localhost cqq]# javac Passenger.java 
[root@localhost cqq]# java Passenger
cost time : 1167
cost time : 3156
[root@localhost cqq]# java -XX:CompileCommand=&#39;dontinline,*.exit&#39; Passenger
CompilerOracle: dontinline *.exit
cost time : 3709
cost time : 7557</div>2018-07-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/10/37/6c6b5e32.jpg" width="30px"><span>吾是锋子</span> 👍（9） 💬（2）<div>郑老师，您好。有个具体的问题想请教下，String类里面indexOf(String str)调用的是自己类里面indexOf(String str, int fromIndex)方法，但我自己在测试的时候却发现两个方法的速度有很明显的差异，看字节码也没有发现什么特殊。
不知道是不是我忽略了什么，希望您能抽空点拨下，感谢！</div>2018-08-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/45/91/246c7698.jpg" width="30px"><span>方枪枪</span> 👍（7） 💬（1）<div>一直不能明确一个问题，执行哪个方法，是不是都是在运行的时候确定的，如果是的话，coding的时候，写一个不存在的方法or传入不存在的参数，编译会报错，那这个合法性的检测，是一个什么逻辑？另外关于方法的确定，对于Java来说，是按照传入的形参确定执行哪个重写的方法，对于 groovy 是按照实际类型确定执行哪个方法，这两个区别在JVM层面是如何实现的？</div>2018-08-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/10/44/ee63ca57.jpg" width="30px"><span>万花</span> 👍（3） 💬（2）<div>代码用汉语也挺好的呀。来这都是学jvm的，没有来学编码规范的吧……</div>2018-07-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5e/ff/295bcf2c.jpg" width="30px"><span>vimfun</span> 👍（2） 💬（1）<div>老师，打印耗时的System.out.println 用的太多了吧？</div>2018-07-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/fc/37/ea588860.jpg" width="30px"><span>礼貌</span> 👍（1） 💬（1）<div>汉语编程？</div>2018-07-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/f2/b1/f765cb62.jpg" width="30px"><span>高家祥</span> 👍（0） 💬（1）<div>方法内联  怎么没有说呀</div>2019-12-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/85/d0/56602a43.jpg" width="30px"><span>灵活工作</span> 👍（0） 💬（1）<div>单态的用内联缓存，超多态的劣化为方法表+索引，那多态的呢？</div>2018-08-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0b/76/e5ffbdf1.jpg" width="30px"><span>lxz</span> 👍（29） 💬（1）<div>建议结合java代码及其对应的字节码来讲解，比如常量池，方法表在字节码中对应的位置，干讲一点印象也没有</div>2018-08-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/2f/32/db8e5674.jpg" width="30px"><span>杨军</span> 👍（24） 💬（11）<div>一直不太理解一个问题：“Java的动态类型运行期才可知”，在编译期代码写完之后应该就已经确定了吧，比如A是B的子类，“B b = new B();   b= new A()”这种情况下b的动态类型是A，Java编译器在编译阶段就可以确定啊，为什么说动态类型直到运行期才可知?
诚心求老师解惑，这个问题对我理解Java的动态绑定机制很关键-.-</div>2018-08-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（23） 💬（1）<div>1:虚方法
方法重写的方法，可认为就是虚方法

2:JVM怎么执行虚方法
通过方法表，一个二维表结构，标示出类的类型、虚方法的序号。当调用虚方法的时候，先确定类型，再根据类型找方法
</div>2018-07-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/79/a2/18815f9c.jpg" width="30px"><span>J</span> 👍（11） 💬（0）<div>win10:
java -XX:CompileCommand=dontinline,*.exit Passenger     这样是对的
java -XX:CompileCommand=‘dontinline,*.exit’ Passenger   这样是错的</div>2018-12-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/e7/88/c8b4ad9c.jpg" width="30px"><span>没有昵称</span> 👍（9） 💬（0）<div>JVM本身比较抽象，建议老师多用图形和示例描述，单纯的文字容易造成感觉明白了，但实际没有深入理解的情况。</div>2020-01-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/e2/58/8c8897c8.jpg" width="30px"><span>杨春鹏</span> 👍（9） 💬（1）<div>关于单态内联缓存中的记录，hotspot采用了超多态。也就是如果该调用者的动态类型不是缓存中的类型的话，直接通过基于方法表来找到具体的目标方法。那么内联缓存中的类型是永久不变，一直是第一次缓存的那个调用者类型吗？</div>2018-07-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e4/cd/5363c8fa.jpg" width="30px"><span>Rain</span> 👍（5） 💬（4）<div>一直不太理解一个问题：“Java的动态类型运行期才可知”，在编译期代码写完之后应该就已经确定了吧，比如A是B的子类，“B b = new B(); b= new A()”这种情况下b的动态类型是A，Java编译器在编译阶段就可以确定啊，为什么说动态类型直到运行期才可知?
诚心求老师解惑，这个问题对我理解Java的动态绑定机制很关键-.-


@杨军，我的理解是，假设C是B的另外一个子类，你的上述两句代码有可能运行在多线程环境中。假设第二行代码运行之后切换到了另外一个线程中，且b = new C()
这个情况下，线程再切换到你的那两行代码后面的时候就不一定是A了，刘必须要在运行过程中才能确定了。</div>2019-01-14</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eo7gP4Nibo4m4MOvbqd4yuK1Bf4ULQeSb3d37zyw5nKAHlHze89yTp4NWRLEbq72iaiaO8NKpOUnHw3g/132" width="30px"><span>加久</span> 👍（4） 💬（2）<div>任何方法调用除非被内联，否则都会有固定开销。这些开销来源于保存程序在该方法中的执行位置，以及新建、压入和...

命中内联缓存后，不用开辟新的栈帧了？？</div>2019-01-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/bd/06/a0b1cfb3.jpg" width="30px"><span>哎呦，不错哦</span> 👍（3） 💬（0）<div>建议举个经典虚拟机实现中方法表对应的具体数据结构等，只有总结出来的文字没有实际代码为证，很难深入了解你的意思</div>2019-01-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/40/6a/ab1cf396.jpg" width="30px"><span>小兵</span> 👍（2） 💬（0）<div>对于接口的方法表有点疑惑，如果一个子类实现多个接口，那么子类的方法表的索引和接口方法表的索引还是相同的吗？不同接口的方法表的索引不会重复吗？</div>2020-02-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/63/6b/34b89fae.jpg" width="30px"><span>男朋友</span> 👍（2） 💬（2）<div>suxiansen@suxiansendeMacBook-Pro:~&#47;geektime&#47;demo&#47;src&#47;main&#47;java|
⇒  java -XX:CompileCommand=&#39;dontinline,*.passThrouguImmigration&#39; com.example.demo.Passenger
CompilerOracle: dontinline *.passThrouguImmigration
70
97
99
99
98
95
97
96
98
96
124
119
123
122
124
125
126
126
126
120
suxiansen@suxiansendeMacBook-Pro:~&#47;geektime&#47;demo&#47;src&#47;main&#47;java|
⇒  java -XX:CompileCommand=&#39;inline,*.passThrouguImmigration&#39; com.example.demo.Passenger
CompilerOracle: inline *.passThrouguImmigration
75
98
93
101
105
101
102
102
100
98
127
124
126
128
126
124
123
128
127
119
suxiansen@suxiansendeMacBook-Pro:~&#47;geektime&#47;demo&#47;src&#47;main&#47;java|
我的怎么看起来没啥区别</div>2019-11-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/6e/8e/5d309a85.jpg" width="30px"><span>拯救地球好累</span> 👍（2） 💬（0）<div>动态绑定：根据调用者的动态类型，来确定虚方法调用的目标方法（JVM中通过方法表定位目标方法）
方法表创建时间：链接时的准备阶段
方法表数据结构：数组（每个数组元素指向一个当前类及其祖先类中非私有的实例方法）
动态绑定过程：在解析过程中，访问栈上的调用者-&gt;读取调用者的实际类型-&gt;读取该类型的方法表-&gt;读取方法表中某个索引值所对应的目标方法
内联缓存：通过缓存调用者的动态类型和该类型对应的目标方法以期加快动态绑定</div>2019-09-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/6b/55/2b0f219b.jpg" width="30px"><span>Geek_42f729</span> 👍（1） 💬（0）<div>哈哈哈，22年才来学JVM。</div>2022-03-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/86/06/72b01bb7.jpg" width="30px"><span>美美</span> 👍（1） 💬（0）<div>这个单态和多态是《深入理解java虚拟机》那本书说的单分派和多分派的意思嘛</div>2020-06-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/de/6b/adee88bb.jpg" width="30px"><span>宿臾洛城</span> 👍（1） 💬（0）<div>这篇比较好理解，感觉就是和Map一个道理，单个值的时候查找很快，多个值查找对应的value性能就会下降了</div>2020-06-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e8/6b/0b48c0f9.jpg" width="30px"><span>Arjen</span> 👍（1） 💬（0）<div>还可以扩展一下，Passenger c = (i &lt; 1_000_000_000) ? a : b;这行的条件改成(i % 2) == 0，模拟两个不同类型的对象轮流调用，也就是文中说的内联缓存只有写开销没有使用到的最坏情况。
自己测试下来这种情况下关闭内联缓存确实要比开启内联缓存要快。</div>2020-03-11</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eou1BMETumU21ZI4yiaLenOMSibzkAgkw944npIpsJRicmdicxlVQcgibyoQ00rdGk9Htp1j0dM5CP2Fibw/132" width="30px"><span>寥若晨星</span> 👍（1） 💬（0）<div>我也建议老师变量名使用英文，因为习惯了，看到中文变量觉得别扭，反而增加了写入大脑缓存的时间哈哈哈</div>2019-03-13</li><br/>
</ul>