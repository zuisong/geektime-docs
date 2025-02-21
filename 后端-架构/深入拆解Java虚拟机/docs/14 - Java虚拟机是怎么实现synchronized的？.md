在Java程序中，我们可以利用synchronized关键字来对程序进行加锁。它既可以用来声明一个synchronized代码块，也可以直接标记静态方法或者实例方法。

当声明synchronized代码块时，编译而成的字节码将包含monitorenter和monitorexit指令。这两种指令均会消耗操作数栈上的一个引用类型的元素（也就是synchronized关键字括号里的引用），作为所要加锁解锁的锁对象。

```
  public void foo(Object lock) {
    synchronized (lock) {
      lock.hashCode();
    }
  }
  // 上面的Java代码将编译为下面的字节码
  public void foo(java.lang.Object);
    Code:
       0: aload_1
       1: dup
       2: astore_2
       3: monitorenter
       4: aload_1
       5: invokevirtual java/lang/Object.hashCode:()I
       8: pop
       9: aload_2
      10: monitorexit
      11: goto          19
      14: astore_3
      15: aload_2
      16: monitorexit
      17: aload_3
      18: athrow
      19: return
    Exception table:
       from    to  target type
           4    11    14   any
          14    17    14   any

```

我在文稿中贴了一段包含synchronized代码块的Java代码，以及它所编译而成的字节码。你可能会留意到，上面的字节码中包含一个monitorenter指令以及多个monitorexit指令。这是因为Java虚拟机需要确保所获得的锁在正常执行路径，以及异常执行路径上都能够被解锁。

你可以根据我在介绍异常处理时介绍过的知识，对照字节码和异常处理表来构造所有可能的执行路径，看看在执行了monitorenter指令之后，是否都有执行monitorexit指令。

当用synchronized标记方法时，你会看到字节码中方法的访问标记包括ACC\_SYNCHRONIZED。该标记表示在进入该方法时，Java虚拟机需要进行monitorenter操作。而在退出该方法时，不管是正常返回，还是向调用者抛异常，Java虚拟机均需要进行monitorexit操作。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（30） 💬（4）<div>恩，今天才补上小结，因为听不明白了，后来反复听以及补上锁的相关知识才有点明白。
我认为雨迪确实应该补上点图，这样才更容易理解，否则确实抽象，另外，我觉得讲解的次序有点小问题。
如果这样讲就更容易理解了（个人见解）
1:讲解一下锁的本质，锁到底是个什么东西？锁的特点容易理解，毕竟都见过摸过用过

2:讲解一下锁的分类和特点，什么表锁、行锁、自旋锁、可重用锁、轻量锁、重量锁、阻塞锁、线程锁、进程锁、分布式锁、偏向锁等等吧！都是站在不同的角度或层级根据锁的特点，为了好区分给锁起的名字

3:讲解一下JVM中的各种锁，讲解一下他们的特点和实现，然后讲解一下咱们本节的主角是属于哪一种或哪几种锁

4:我的理解，锁的本质-在程序世界里是一种保证资源正确竞争的机制，如果没有对同一资源竞争也就没有了锁存在的意义，在计算世界中资源引起竞争的核心基本是空间，有其是计算机的内存空间，当然数据肯定也是一种引起激烈竞争的资源，不过往往会体现到空间上去，因为计算机中的数据必定存于某空间地址之中的

5:感觉明白可重用锁的实现原理了，这个也是雨迪讲的最细致的一种实现方式，恩，非常感谢🙏</div>2018-09-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/59/c9/f44cb7f3.jpg" width="30px"><span>爪哇夜未眠</span> 👍（24） 💬（1）<div>太抽象了，老师能画点儿图吗……</div>2018-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/9a/68/92caeed6.jpg" width="30px"><span>Shine</span> 👍（18） 💬（2）<div>“当进行解锁操作时，如果当前锁记录（你可以将一个线程的所有锁记录想象成一个栈结构，每次加锁压入一条锁记录，解锁弹出一条锁记录，当前锁记录指的便是栈顶的锁记录）的值为 0，则代表重复进入同一把锁，直接返回即可。”
这种情况也需要弹出当前锁记录的吧？ 不然锁记录一直是0不变了。 如果是我这样理解的话，重复获取同一把锁的话，不是简单地清零，而应该是把0作为一条新的锁记录压入栈顶。
不知道我这样理解对不？请老师指点</div>2018-08-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/cd/e1/368f872c.jpg" width="30px"><span>NEO🍋</span> 👍（13） 💬（1）<div>老师关于偏向锁有个疑问 “它针对的是锁仅会被同一线程持有的情况。” 如果只有一个线程持有锁 还有必要加锁吗？</div>2018-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/04/b5/8bc4790b.jpg" width="30px"><span>Geek_987169</span> 👍（8） 💬（1）<div>老师请教个问题：
1：锁从偏向一直到重量级的过程是&quot;单向不可逆&quot;的，这个&quot;单向不可逆&quot;是限制在对象的整个生命周期，还是在对象到达了某个状态后再次有线程使用其作为锁对象还会继续重复这个过程？从每撤销一次对象的epoch值就会+1，而这个+1代表的就是偏向锁升级为轻量级锁，而每个对象又维护了一个epoch值代表对象撤销次数（偏向锁-&gt;轻量级锁次数），是不是就代表这个锁升级的过程会在不同的时间段重复发生n词？
2：为什么要设置一个最大的撤销次数（epoch值），意义在哪里？</div>2018-10-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/2d/8e/f9a22b2e.jpg" width="30px"><span>唯一</span> 👍（6） 💬（1）<div>老师，问一下加锁实际上都是加在当前线程吗</div>2018-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/0e/b1/aab3759b.jpg" width="30px"><span>何yuan</span> 👍（6） 💬（2）<div>一直认为synchronized是重量锁，是否也不一定？jvm处理的时候是先将当偏向锁处理，然后慢慢膨胀为重量级锁的是吗？</div>2018-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/eb/5d/2467ad6c.jpg" width="30px"><span>木心</span> 👍（5） 💬（6）<div>很多文章说 自旋 是在轻量级锁中发生的 《Java并发编程的艺术》
但是在这里 自旋 是在重量级锁中
这个怎么解释呢?
https:&#47;&#47;www.aimoon.site&#47;blog&#47;2018&#47;05&#47;21&#47;biased-locking&#47;
</div>2019-11-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/61/f2/ca989d6f.jpg" width="30px"><span>Leon Wong</span> 👍（4） 💬（3）<div>老师你好，本课程在介绍轻量级锁的时候，没提及轻量级锁在其他线程占用改锁的的时候，是否会进入自旋状态，我先前的理解是，轻量级锁在被其他线程占用的时候，会进入短暂的自旋状态，当自旋达到一定的阈值后，膨胀为重量级锁，阻塞当前线程，不知道我这么理解是否正确？</div>2018-09-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c9/cb/7b6802cc.jpg" width="30px"><span>贾智文</span> 👍（4） 💬（3）<div>假设当前锁对象的标记字段为 X…XYZ，Java 虚拟机会比较该字段是否为 X…X01。   老师请问这个x……x01是什么，根据什么来的呢？</div>2018-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/03/a3/fa04ae05.jpg" width="30px"><span>林QC</span> 👍（3） 💬（1）<div>当声明 synchronized 代码块时，编译而成的字节码将包含 monitorenter 和 monitorexit 指令。～～老师，标记在方法上也有这两个指令吗？</div>2018-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/3c/5e/6a26a8c4.jpg" width="30px"><span>licht</span> 👍（0） 💬（1）<div>2-2:内存屏障，这是什么意思？它怎么就能禁止重排序啦？还有有其引申出的各种屏蔽是怎么回事呢？也没完全明白。  因为不明白内存屏障，对于空指令的内存屏障很迷惑？希望老师帮忙解答一下，谢谢了。</div>2018-08-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/15/81/2c31cf79.jpg" width="30px"><span>永烁星光</span> 👍（0） 💬（1）<div>“假设当前锁对象的标记字段为 X…XYZ，Java 虚拟机会比较该字段是否为 X…X01。如果是，则替换为刚才分配的锁记录的地址。  ”
这个描述上面的 “加锁操作时，如果不是重量级锁，则在栈上分配一个空间存储锁记录，并将锁对象的标记字段复制到栈记录中” 矛盾啊，还是我没有看懂？</div>2018-08-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/9f/15/05d3ade0.jpg" width="30px"><span>顺子</span> 👍（0） 💬（1）<div>对于轻量级锁，markword本质是一个32位的bit，无锁情况下，末尾是01
加锁过程只是通过CAS把这32位的bit替换为lockrecord的地址，由于lockrecord地址只有30位，所以末尾补齐32后，末尾是00
不知道理解是否正确

然后有一个疑问，升级为重量级锁的时候，10是什么时候修改的?看到的文档都只说把指针修改为mutex，没提到10是怎么来的，是mutex30位地址加上10后CAS替换进去的吗</div>2018-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f6/32/358f9411.jpg" width="30px"><span>梦想启动的蜗牛</span> 👍（0） 💬（1）<div>轻量级锁应该是先通过cas替换锁的标记字段，然后再把标记字段复制到栈中对应的锁记录中把？</div>2018-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/44/47/3ddb94d0.jpg" width="30px"><span>javaadu</span> 👍（0） 💬（1）<div>想看下jvm是怎么实现stream和lambda表达式的</div>2018-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c9/cb/7b6802cc.jpg" width="30px"><span>贾智文</span> 👍（0） 💬（1）<div>果不是 X…X01，那么有两种可能。第一，该线程重复获取同一把锁。此时，Java 虚拟机会将锁记录清零，以代表该锁被重复获取。第二，其他线程持有该锁。此时，Java 虚拟机会将这把锁膨胀为重量级锁，并且阻塞当前线程。
这两个情况怎么区分呢？</div>2018-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/59/57/449e76fb.jpg" width="30px"><span>QlDoors</span> 👍（23） 💬（1）<div>练习试了无数遍，都没有偏向锁，后来上网查才发现需要加-XX:BiasedLockingStartupDelay=0。

http:&#47;&#47;zhizus.com&#47;2018-09-03-%E5%81%8F%E5%90%91%E9%94%81.html

注意：Hotspot虚拟机在开机启动后有个延迟（4s），经过延迟后才会对每个创建的对象开启偏向锁。我们可以通过设置下面的参数来修改这个延迟，或者直接sleep一段时间-XX:BiasedLockingStartupDelay=0</div>2018-11-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8e/e7/abb7bfe3.jpg" width="30px"><span>谢阳</span> 👍（18） 💬（2）<div>如果不是 X…X01，那么有两种可能。第一，该线程重复获取同一把锁。此时，Java 虚拟机会将锁记录清零，以代表该锁被重复获取。第二，其他线程持有该锁。此时，Java 虚拟机会将这把锁膨胀为重量级锁，并且阻塞当前线程。

老师这段不太明白。1 锁记录清零怎么理解？改变锁对象的标记字段吗？2 锁膨胀的时候其他线程还持有锁对象吧，这个时候膨胀会具体做什么操作？如果操作了锁对象的标记字段会影响稍后释放锁的cas吗</div>2018-08-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/16/5b/83a35681.jpg" width="30px"><span>Monday</span> 👍（14） 💬（0）<div>听了N次，仔细读了一遍，还是不够。有同样情况的，赞起</div>2020-07-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c9/cb/7b6802cc.jpg" width="30px"><span>贾智文</span> 👍（6） 💬（1）<div>文中说轻量级锁因为内存对齐所以标识位是00，那么为什么重量级锁的时候，存储内容也是指针，却没有内存对齐呢？</div>2018-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/0e/1b/1902d6fa.jpg" width="30px"><span>第9根烟</span> 👍（4） 💬（0）<div>这边验证了Object.hashCode() 不会关闭该对象的偏向锁。。不知道最后答案是什么？哪里有全篇的课后作业的答案？</div>2019-01-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e4/6e/ef9aece4.jpg" width="30px"><span>ゞ、今生绝恋丶</span> 👍（3） 💬（3）<div>雨迪老师，我有个疑问：假设线程A加锁，CAS将锁对象对象头替换成指向线程A的Lock Record的地址，在这里，原值：对象mark word中的内容，也就是hashcode，期望值：本线程Lock Record地址，对象：锁对象，在替换成功后我们说线程A获得了锁，OK，线程A开始执行同步代码块，在它执行完之前，线程B来获取锁，发现属于轻量级锁标志，于是CAS替换mark word，此时CAS的原值仍然为为锁对象的mark word吧，而此时锁对象mark word中记录的不再是hashcode而是指向线程A的Lock Record的地址，但是对于CAS它管你对象头存的是什么，现在获取到什么，什么就是原值，于是：原值：对象头中指向线程A中LR的地址，期望值：线程B中LR（目前对他来说，是将锁对象中指向线程A中LR的地址存入本线程LR）的地址，目标对象：锁对象，怎么会CAS不成功？于是现在线程B也获取到锁，两个线程都会在执行同步代码块！我觉得我理解的哪块不对？</div>2019-04-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/db/a4/191be6ad.jpg" width="30px"><span>加载中……</span> 👍（3） 💬（0）<div>您好，文章写的挺好，读完有个问题想请教下：
当t1线程获取了某个对象锁（lock1）的偏向锁，还没执行完的时候，另外一个线程t2也尝试获取这个对象锁(lock1)，我看文章上说需要撤销偏向锁，等到达安全点的时候，再将偏向锁替换成轻量级锁。
我有个问题：两个线程同时竞争同一把锁的情况，轻量级锁也解决不了吧，只能用重量级锁解决吧？为什么还要替换成轻量级锁呢？</div>2019-02-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2d/ba/2e/08585f22.jpg" width="30px"><span>程浩乾</span> 👍（2） 💬（0）<div>我的理解：Synchronized锁优化时有三种状态：
1.偏向锁(无锁，乐观地认为只有一个线程)，具体实现：
（1）每个类的标记头中都有个epoch值(代表第几代偏向锁)，初次加锁时将锁对象类中的epoch值复制到创建的锁对象中，并将本线程地址写入锁对象标记字段，且设置标记字段最后三位为101(偏向锁)。
（2）当新线程加锁时，若锁对象标记字段的线程地址非本线程，且epoch值相等，会导致偏向锁撤销，便升级该锁对象为轻量级锁。若epoch值不等，可直接使锁对象偏向自己(写入本线程地址)。
（3）若该类锁对象的总撤销次数超过20次(JVM参数-XX:BiasedLockingBulkRebiasThreshold)，就会使偏向锁失效，会将锁对象类的epoch值加1，并在安全点时赋值到其下所有的锁对象中。
（4）若该类锁对象的总撤销次数超过40次(JVM参数-XX:BiasedLockingBulkRevokeThreshold)，就会认为该类锁对象已经不再适合偏向锁，会撤销掉该类实例的偏向锁，并在下次加锁时直接使用轻量级锁。

2.轻量级锁(乐观地认为多个线程不会同时执行)，具体实现：
（1）加锁时，在当前线程的当前栈帧中划出一块空间作为线程锁记录，将锁对象的标记字段(01结尾的偏向锁)复制到线程锁记录中，并把线程锁记录地址通过CAS操作赋值到锁对象的标记字段内，由于内存对齐的缘故，锁对象的标记字段将会以00(轻量级锁)标记来结尾。
（2）当新线程加锁时，若锁对象标记字段内的线程地址是指向自己，便会将当前栈帧的锁记录清零，以代表该锁被重复获取；若不是指向自己，便直接会膨胀为重量级锁。
（3）解锁时，若当前栈帧的锁记录为0(代表重复获取锁)，就会直接返回；若不是0，便会将当前栈帧的锁记录(01结尾的偏向锁状态)通过CAS操作赋值到锁对象中。(一个线程的所有锁记录是栈结构，加锁时压入一条锁记录，解锁时弹出一条锁记录)

3.重量级锁(多个线程会同时执行)，具体实现：
（1）依靠操作系统来对Java线程进行阻塞和唤醒，涉及系统调用，需从用户态切换到内核态，开销非常大。
（2）为避免昂贵的阻塞和唤醒，在阻塞前会进入短暂的自适应自旋来避免非常短的加锁代码块(在处理器上空跑并且轮询锁是否被释放)，自适应自旋会根据以往的自旋时能否获得锁，来动态调整自旋的时间(数目)。(自适应自旋是不公平的锁竞争，不利于已阻塞的线程获得锁)</div>2022-05-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/44/47/3ddb94d0.jpg" width="30px"><span>javaadu</span> 👍（2） 💬（0）<div>你好，例子运行了，没看出啥不同，只有“fast path lock entries”这个对应的数值不同，slow path lock entries一直是2，其他的都是0。

建议作者给出自己的实验截图，方便我们对比</div>2018-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/70/3a/6b82e940.jpg" width="30px"><span>(^o^)</span> 👍（2） 💬（1）<div>Synchronized某个对象时，这个对象的锁先是偏向锁，后根据具体竞争情况先升级为轻量级锁再升级为重量级锁吗？</div>2018-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/fd/08/c039f840.jpg" width="30px"><span>小鳄鱼</span> 👍（1） 💬（0）<div>个人觉得有一点：强行翻译最为致命。一个“标记字段”硬生生阻碍我对文章的理解。看了N遍，参考了其他博客，翻找了《深入理解Java虚拟机》，才知道原来就是MarkWord。。。内容总体的编排，看起来跟书里差别不大。但是在每个小的知识点上感觉相对混乱。且对于没有一些概念性的术语对于没有相关知识的同学容易造成理解困难</div>2022-07-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/0a/93/a189ec16.jpg" width="30px"><span>Eric</span> 👍（1） 💬（0）<div>https:&#47;&#47;tech.meituan.com&#47;2018&#47;11&#47;15&#47;java-lock.html</div>2021-11-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/7c/ec/c5a414dd.jpg" width="30px"><span>nidafg</span> 👍（1） 💬（0）<div>感觉老师讲的很学院派，如果能有图文或者更多比喻就好了</div>2019-09-10</li><br/>
</ul>