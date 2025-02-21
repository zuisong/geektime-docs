我们先来看一个反常识的例子。

```
int a=0, b=0;

public void method1() {
  int r2 = a;
  b = 1;
}

public void method2() {
  int r1 = b;
  a = 2;
}
```

这里我定义了两个共享变量a和b，以及两个方法。第一个方法将局部变量r2赋值为a，然后将共享变量b赋值为1。第二个方法将局部变量r1赋值为b，然后将共享变量a赋值为2。请问（r1，r2）的可能值都有哪些？

在单线程环境下，我们可以先调用第一个方法，最终（r1，r2）为（1，0）；也可以先调用第二个方法，最终为（0，2）。

在多线程环境下，假设这两个方法分别跑在两个不同的线程之上，如果Java虚拟机在执行了任一方法的第一条赋值语句之后便切换线程，那么最终结果将可能出现（0，0）的情况。

除上述三种情况之外，Java语言规范第17.4小节\[1]还介绍了一种看似不可能的情况（1，2）。

造成这一情况的原因有三个，分别为即时编译器的重排序，处理器的乱序执行，以及内存系统的重排序。由于后两种原因涉及具体的体系架构，我们暂且放到一边。下面我先来讲一下编译器优化的重排序是怎么一回事。

首先需要说明一点，即时编译器（和处理器）需要保证程序能够遵守as-if-serial属性。通俗地说，就是在单线程情况下，要给程序一个顺序执行的假象。即经过重排序的执行结果要与顺序执行的结果保持一致。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/a0/9f/71345740.jpg" width="30px"><span>黑崽</span> 👍（31） 💬（8）<div>请教个问题。刚才有说不会把volatile放到寄存器，但是应该会在栈里面对吧。直接读取主内存，读写的是栈数据，然后利用堆内存和栈上数据是利用写缓存刷新同步的？</div>2018-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0c/2f/54f7f676.jpg" width="30px"><span>Jerry Chan</span> 👍（1） 💬（1）<div>博客在哪里啊？</div>2018-08-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/49/a5/e4c1c2d4.jpg" width="30px"><span>小文同学</span> 👍（7） 💬（6）<div>老师我提个问题。一个共享对象的变量是非volatile的，那么这个变量的写入会先写到寄存器上，再写回内存吗？那么jvm是不是无论如何都不保证啥时候变量的值会写回内存。假如另一个线程加锁访问这个变量，是不是jvm也不保证它能拿到最新数据。</div>2018-08-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5e/ec/70c8d94d.jpg" width="30px"><span>大场镇车王</span> 👍（30） 💬（5）<div>老师 为什么volatile内存屏障不允许所有写操作之前的读操作被重排序到写操作之后？前面不是说volatile的写操作happens before对用一字段的读操作吗</div>2018-08-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a0/47/620308a3.jpg" width="30px"><span>Alex Rao</span> 👍（17） 💬（1）<div>老师，我在一些技术文章里看到说 volatile 的变量是存在工作内存，这个工作内存是一个什么概念？</div>2018-08-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d0/00/9d05af66.jpg" width="30px"><span>加多</span> 👍（11） 💬（2）<div>老师，求讲解下jvm中代码如何实现的内存屏障</div>2018-08-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/3a/cb/97dee373.jpg" width="30px"><span>道法自然</span> 👍（27） 💬（1）<div>老师你好，关于指令重排序有点不太理解，指令重排序的粒度是方法级别的，还是整个源文件级别的。文中说道，b 加了volatile后，能够保证 b=1 先于r1=b ，这个我能理解，但是如何保证不会因为指令重排导致 b=1 先于r2=a发生呢？文中虽然说了，同一个线程中，字节码顺序暗含了r2=a happen before b=1，但是文中也提到了，拥有happen-before关系的两对赋值操作之间没有数据依赖，处理器可以指令重排序。r2=a 和b=1之间没有数据依赖呀！不好意思，这块有点迷糊，老师能给详细解答下不？</div>2018-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e0/9f/9259a6b9.jpg" width="30px"><span>Kyle</span> 👍（11） 💬（1）<div>我个人理解的“JAVA内存模型”应该是包括两部分的内容：
一是运行时数据区，
二是定义了一组内存访问规则。

这里其实主要讲的是其中的第二部分内容。不知道是不是可以这样总结。</div>2018-08-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/56/43/abb7bfe3.jpg" width="30px"><span>阿巍-豆夫</span> 👍（8） 💬（1）<div>关于Volatile, 我想问下，如果是单个cpu的系统上运行多线程的程序，是不是这个volative就没有效果了？ 因为大家都使用同一个寄存器。</div>2018-12-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/0e/1b/1902d6fa.jpg" width="30px"><span>第9根烟</span> 👍（7） 💬（2）<div>问一下，内存屏障是即时编译器生成本地代码的时候产生的？？那照这个意思岂不是关闭即时编译器就实现不了happen-before原则了？</div>2018-10-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/12/93/3470fc43.jpg" width="30px"><span>Mr.钧👻</span> 👍（4） 💬（1）<div>即时编译在单线程的情况下，根据as if serial 的选择，会是的编译逻辑和程序逻辑相同。

但是，在多线程情况下可能出现编译器重排序导致的数据竞争。这时就需要使用volatile来禁止重排序。

volatile的底层原理，是在字节码中插入内存屏障实现的。

内存屏障会被转化成一条指令，指令具体的效果是强制刷新缓存。
疑问：为什么是强制刷新缓存？是因为happen-before原则，要让后面的程序看到？ 那后面程序看到的就是缓存中的内容吗？

我对寄存器，缓存有不熟悉的地方，希望老师可以指正，指导我该补哪方面的知识，多谢</div>2018-10-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/21/d2/df11e830.jpg" width="30px"><span>浩</span> 👍（3） 💬（1）<div>您好 当工作线程需要的内存特别大 比如超过10m 那工作线程会copy10m的内存数据到工作线程嘛？</div>2018-09-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0d/5d/e50cf9c7.jpg" width="30px"><span>Kenneth</span> 👍（3） 💬（2）<div>同求讲解该问题，谢谢老师！：
啃yi嘴泥
老师你好，关于指令重排序有点不太理解，指令重排序的粒度是方法级别的，还是整个源文件级别的。文中说道，b 加了volatile后，能够保证 b=1 先于r1=b ，这个我能理解，但是如何保证不会因为指令重排导致 b=1 先于r2=a发生呢？文中虽然说了，同一个线程中，字节码顺序暗含了r2=a happen before b=1，但是文中也提到了，拥有happen-before关系的两对赋值操作之间没有数据依赖，处理器可以指令重排序。r2=a 和b=1之间没有数据依赖呀！不好意思，这块有点迷糊，老师能给详细解答下不？
2018-08-24</div>2018-08-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/21/73/4ac5e91c.jpg" width="30px"><span>Geek_05in47</span> 👍（2） 💬（1）<div>我写了个方法按照上面的代码循环执行了9999次，要么是1，0要么是0,2 一直没有出现1,2。这个怎么破？</div>2018-09-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4c/e6cb260a.jpg" width="30px"><span>agilejava</span> 👍（1） 💬（1）<div>文字太多，最好能结合一些图形会更方便理解</div>2018-08-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（63） 💬（5）<div>恩，这节听了好几遍，也读了几遍，最后还是感觉蒙蒙的。
下面说下我的感受：
1:一图胜千言，尤其对于描述复杂的东西，这个建议其他同学也有提议的，希望雨迪采纳一下

2:感觉有些概念没有解释，比如：
2-1:Java内存模型，这节不就是要讲Java内存类型是什么？有什么特点？为什么这么设计嘛？不过我没看到这些内容，当然，特点是讲了的 happens-before 机制
2-2:内存屏蔽，这是什么意思？它怎么就能禁止重排序啦？还有有其引申出的各种屏蔽是怎么回事呢？也没完全明白


3:前面讲 as-if-serial 大概明白什么意思了，多处理器为了提高效率会采用流水线的方式来执行程序指令，但是同时要保证程序执行逻辑的正确性，所以，实际执行程序的指令和代码层面上会有不同，这个是由编译器来保证的，虽然执行逻辑不同但是程序逻辑是没变的，单线程没问题，但是多线程就变得复杂一些了，光靠这种方式保证不了啦，所以引出了下文

4:happens-before，这个概念和作用比较容易理解，线程内有这种关系，线程间更有，这个机制我认为就是为了多线程环境下为了保证程序逻辑正确性的一种方式，不过它的具体实现细节感觉没理解，不清楚他是怎么办到的

5:volatile 这个关键字之前也学习过，作用是保证内容的修改对所有线程可见，原理是修改后同步更新所有的内容，这是因为内存和处理器直接还是存在距离的，比如：内存-一级缓存-二级缓存-各种寄存器-cpu，如果是内存-cpu，则不会有这种问题了，不过性能也就不行了</div>2018-08-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/80/bf/3041138b.jpg" width="30px"><span>　素丶　　</span> 👍（34） 💬（2）<div>可以配合程晓明大大的《深入理解Java内存模型》
https:&#47;&#47;www.infoq.cn&#47;article&#47;java_memory_model</div>2018-11-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/06/7e/735968e2.jpg" width="30px"><span>西门吹牛</span> 👍（4） 💬（0）<div>如何理解编译优化：
经过编译后的指令，最终是要被cpu执行。cpu 指令执行是采用流水作业的方式，一条指令的执行流程包含取得指令、指令译码、执行指令三个过程。cpu可以一次取一条指令，也可以一次取一个指令包，指令包包含多条执行。而cpu执行指令的时候，并不是等一条指令执行结束在执行下一条指令，往往一条 cpu 指令会被拆分成多个阶段，多个阶段就对应多个流水线。也就是说只要保证一条指令的多个流水线只要在一个cpu时钟周期内完成即可。这就会导致一条指令的数据操作好没写回内存，下一条指令已经开始工作，因此下一条指令读取的数据，不一定是上一条指令执行后的数据。编译优化的目的本质是加快程序运行速度，能让编译后的指令尽可能赶上cpu的执行频率。这种cpu指令的流水线作业，就导致，程序编译后的指令，实际执行的顺序可能不是严格按照编译后的指令顺序而执行。
在单线程执行的时候或者单核执行的时候，cpu在执行有数据依赖的指令的时候，往往通过加入一些空操作no-op来保证指令的执行顺序，对于没有数据依赖的指令，往往采用乱序执行来加快执行效率。
在多线程的情况下或者多核的情况下，对数据操作是并发执行，也就是说，每个线程都会把操作的数据加载到自己的缓存中(本地内存)执行，这就导致，线程之间对数据的操作不可见。java内存模型规定，要保证数据的可见性，必须经过主内存，也就是说，只有当一个线程的操作同步到主内存后，别的线程才能读到更新后的数据。在多线程下，对共享变量操作就会发生数据竞争问题，从而导致并发问题；
如何理解内存屏障禁止指令重排序：
在单线程的情况下，JMM规定了一条HB 规则，在一个线程中，前面的操作 Happens-Before 于后续的任意操作，这就要求，在cpu指令执行的时候，有数据依赖关系的指令，不能被重排序，但是CPU执行指令的时候，为了执行效率采用流水作业，并不是严格按照程序的顺序进行执行。这就要求，在有依赖关系的指令之间插入内存屏障来保证，比如插入空操作no-op，这就保证了，如果写操作指令没有执行完，这是读指令读取数据，那么读取的是内存屏障指令，也就是空操作，只有等写操作指令执行结束，读指令才能读取到最新的数据。从而解决了编译重排序而导致的数据安全问题；
在多线程的情况下，为了解决线程之间缓存导致的可见性问题，JMM规定了一条HB规则，对一个 volatile 变量的写操作Happens-Before 于后续对这个 volatile 变量的读操作。比如 A 线程对变量执行写操作，这时候，B线程想要在A线程写完之后读取数据，因为A 线程的写操作，往往需要多条cpu指令执行，如果写操作的指令还没执行结束，这时候读指令读取到的数据必然是不符合程序本身意愿的。A线程写操作的指令和B线程读操作的指令，在CPU执行的时候，先后顺序完全取决于CPU，CPU不会等A线程写操作指令执行完才执行B线程的读操作指令，这就会引起并发问题，这时候可以通过内存屏障来解决，也就是对共享变量用volatile 修饰，volatile 本质就是通过内存屏障来实现，也就是说用volatile修饰变量，编译后，会生成具体的每次屏障指令，以Lock开头的指令，就是保住A线程对数据的操作结果，会同步到内存中，并且在A线程执行写操作的时候，B线程不可以进行读取操作，只有当A的写操作同步到内存后，B线程才执行度操作，类似锁的功能。通过内存屏障禁止了指令重排序，保证了共享数据在多线程之间的可见性问题。</div>2020-07-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4a/6f/e36b3908.jpg" width="30px"><span>xzy</span> 👍（1） 💬（0）<div>JMM 决定一个 线程对共享变量的写入何时对另一个线程可见。</div>2020-11-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/16/5b/83a35681.jpg" width="30px"><span>Monday</span> 👍（1） 💬（0）<div>以往我认为b设置为volatile后，如代码：标记1则不能重排序优化到标记2后面，若r1=1，则表明顺序肯定能确定有 1,2,3；但是4若在最前面执行了，则可能出现(r1,r2)=(1,2)。
但是现在这个假设已经被老师打破了，而且是我所不能理解了，我太难了......
能不能这样理解，b设置为volatile后，对b的赋值和读取都加了重排序限制，导致1 happen-before 2, 3 happen-before 4。
int a=0;
volatile int b=0;

public void method1() {
  int r2 = a; 	&#47;&#47;标记1
  b = 1;  	  	&#47;&#47;标记2
}

public void method2() {
  int r1 = b;	&#47;&#47;标记3
  a = 2;		&#47;&#47;标记4
}
</div>2020-07-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0c/52/f25c3636.jpg" width="30px"><span>长脖子树</span> 👍（1） 💬（0）<div>测试用例 [6] 中实际测试后会发现, 有一部分的 object 尚未初始化
问题出在 new 操作上，我们以为的 new 操作应该是：
	分配一块内存 M；在内存 M 上初始化 Singleton 对象；然后 M 的地址赋值给 instance 变量。
 但是实际上优化后的执行路径却是这样的：
		 分配一块内存 M；将 M 的地址赋值给 instance 变量；最后在内存 M 上初始化 Singleton 对象。
所谓的单例模式, 就是安全发布的问题
(部分来自专栏 java并发编程实战)</div>2019-11-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ce/73/cded8343.jpg" width="30px"><span>believe me</span> 👍（1） 💬（0）<div>即时编译器才会重排序，解释执行是不是就没有这个问题了？</div>2019-06-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/12/51/f309515c.jpg" width="30px"><span>冬末未末</span> 👍（1） 💬（1）<div>happen-before 在这里不能理解成在什么之前发生，它和时间没有任何关系。个人感觉解释成“生效可见于” 更准确。</div>2018-09-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f8/0e/de697f9b.jpg" width="30px"><span>熊猫酒仙</span> 👍（1） 💬（0）<div>老师，既然有写缓存，是不是也有读缓存呢？强制刷新写缓存，无效化相应的内存数据，那么这些内存数据的读缓存也就失效了，需要重新加载最新数据，是否可以这样理解？

另外强制刷新写缓存是否也有粒度一说？就是我们加的锁也有粒度之分，那么所触发的强制刷新写缓存的区域可能不一样？</div>2018-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/e1/82/1c5d285d.jpg" width="30px"><span>(￣o￣) . z Z</span> 👍（0） 💬（0）<div>为什么不是先总再细节的方式讲解，这一上来就举例、讲细节，对这块基础差一点的，比较难理解啊</div>2022-08-27</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLLniccwC1Mootc7IQsRGUTX3ZkkCKPc7lYV0g8CAqscWtAjd8xkHYcY3UFbYvicm42FXuAO5bZP6WQ/132" width="30px"><span>Geek_417e74</span> 👍（0） 💬（0）<div>老师，请问用 volatile 修饰对象（list，map，数组，自定义java对象，那(list#add、map#put、数组[idx]=xxx、java#setter 还有比如 list里面的java对象#setter)  算对volatile 对象的写操作么？这个时候会强制刷新写缓存么。也就是volatile 修饰对象，能保证整个对象的可见性么？谢谢老师</div>2022-02-27</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLLniccwC1Mootc7IQsRGUTX3ZkkCKPc7lYV0g8CAqscWtAjd8xkHYcY3UFbYvicm42FXuAO5bZP6WQ/132" width="30px"><span>Geek_417e74</span> 👍（0） 💬（0）<div>老师，想问一个问题：线程池executor.submit(task)；task里执行xxx.method(Object 1); 如果submit提交后把task放队列，那这个Object 1 对线程池中已存在的线程不可见么？比如我在主线程里对Object 1 的属性做了修改，然后sumbit，先放入队列，然后很快被一个线程执行了，这个线程是不是可能读到 Object 1 修改前的属性值呢？这时候就用 volatile 解决么？</div>2022-02-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/28/6d/d776d35a.jpg" width="30px"><span>大漠</span> 👍（0） 💬（0）<div>happens-before 这个概念理解起来感觉有点别扭 😂</div>2021-05-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/07/36/d677e741.jpg" width="30px"><span>黑山老妖</span> 👍（0） 💬（0）<div>Java内存模型的主要目标是定义程序中各个变量的访问规则，即在虚拟机中将变量存储到内存和从内存中取出变量这样的底层细节</div>2021-03-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/58/9f/abb7bfe3.jpg" width="30px"><span>小龙的城堡</span> 👍（0） 💬（0）<div>volatile 字段可以看成一种轻量级的、不保证原子性的同步，其性能往往优于（至少不亚于）锁操作。然而，频繁地访问 volatile 字段也会因为不断地强制刷新缓存而严重影响程序的性能。

老师您好，这里是否是要改成，对Volatile字段的修改才会编译出lock，导致频繁的锁总线，导致性能下降呢？谢谢</div>2021-03-09</li><br/>
</ul>