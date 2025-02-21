你好，我是LMOS。

在前面的课程里，我们已经知道了CPU是如何执行程序的，也研究了程序的地址空间，这里我们终于到了程序的存放地点——内存。

你知道什么是Cache吗？在你心中，真实的内存又是什么样子呢？今天我们就来重新认识一下Cache和内存，这对我们利用Cache写出高性能的程序代码和实现操作系统管理内存，有着巨大的帮助。

通过这节课的内容，我们一起来看看内存到底是啥，它有什么特性。有了这个认识，你就能更加深入地理解我们看似熟悉的局部性原理，从而搞清楚，为啥Cache是解决内存瓶颈的神来之笔。最后，我还会带你分析x86平台上的Cache，规避Cache引发的一致性问题，并让你掌握获取内存视图的方法。

那话不多说，带着刚才的问题，我们正式进入今天的学习吧！

## 从一段“经典”代码看局部性原理

不知道，你还记不记得C语言打印九九乘法表的代码，想不起来也没关系，下面我把它贴出来，代码很短，也很简单，就算你自己写一个也用不了一分钟，如下所示。

```
#include <stdio.h>
int main(){
    int i,j;
    for(i=1;i<=9;i++){        
        for(j=1;j<=i;j++){
            printf("%d*%d=%2d  ",i,j,i*j);
        }
        printf("\n");
    }
    return 0;
}
```

我们当然不是为了研究代码本身，这个代码非常简单，这里我们主要是观察这个结构，代码的结构主要是**顺序、分支、循环**，这三种结构可以写出现存所有算法的程序。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1e/f7/ad/4fd4d867.jpg" width="30px"><span>数学汤家凤</span> 👍（19） 💬（2）<div>程序代码优化 基于csapp做的整理 https:&#47;&#47;blog.csdn.net&#47;u013570834&#47;article&#47;details&#47;117635229?utm_source=app&amp;app_version=4.9.2
1. gcc 编译器优化很蠢并不会猜测程序员编码的意图，只会做非常保守的优化
2.循环对于具有很好的时间局部性，所以我们尽量避免 goto 与非本地跳转
3. 数组在内存中行优先排列，所以数组的遍历方式对cache的命中率影响极大
4. 分支预测失败虽然会带来极大的惩罚，但这不是我们关注的重点，我们应该关注的如何能用条件传送的方式避免分支判断
5. 根据阿姆达尔定律，加速大的部分永远比加速小的要有效，所以我们可以根据对程序的分析来做具体的优化</div>2021-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ec/13/49e98289.jpg" width="30px"><span>neohope</span> 👍（271） 💬（10）<div>如何写出让 CPU 跑得更快的代码？可以从以下几方面入手：
1、遵从80-20法则，程序80%的时间在运行20%或更少的代码，针对热代码进行优化，才容易产出效果；
2、遵从数据访问的局部性法则，按数据存放顺序访问内存效率远高于乱序访问内存效率，也就是尽量帮助CPU做好数据Cache的预测工作。同样根据Cache大小，做好数据结构的优化工作，进行数据压缩或数据填充，也是提升Cache效率的好方式；
3、遵从指令访问的局部性法则，减少跳转指令，同样是尽量帮助CPU做好数据Cache的预测工作；现代CPU都有一些预测功能【如分支预测】，利用好CPU的这些功能，也会提升Cache命中率；
4、避免计算线程在多个核心之间漂移，避免缓存重复加载，可以绑定核心【物理核即可，不用到逻辑核】，提高效率；
5、去除伪共享缓存：在多核环境下，减少多个核心对同一区域内存的读写并发操作，减少内存失效的情况的发生；
===开始跑题===
6、合理提高进程优先级，减少进程间切换，可以变相提供Cache提速的效果
7、关闭Swap，可以变相提供内存提速、Cache提速的效果；
8、使用Intel自家的编译器，开启性能优化，很多时候可以提速运算效率；
9、使用C语言，而不是更高级的语言，很多时候可以提速运算效率；
10、直接使用昂贵的寄存器作为变量，可以变相提供加速效果；</div>2021-05-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/62/b5/4159fa05.jpg" width="30px"><span>zhanyd</span> 👍（25） 💬（1）<div>我以前写过一篇关于缓存局部性原理的文章，有兴趣的同学可以看看：
https:&#47;&#47;blog.csdn.net&#47;zhanyd&#47;article&#47;details&#47;102631248</div>2021-05-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/52/40/e57a736e.jpg" width="30px"><span>pedro</span> 👍（62） 💬（15）<div>在CSAPP第六章对存储器层次架构有详细的探讨，感兴趣的同学可以查阅一下，这里我简单总结一下当做思考题答案。
一个编写良好的计算机程序尝尝具有良好的局部性，这被称为局部性原理，对硬件和软件都有极大的影响。
局部性可分为两种，1.程序数据引用局部性;2.指令局部性。
CPU对数据和指令都存在高速缓存，当缓存中的数据大面积命中时，则该代码拥有良好的空间局部性;当缓存中的指令大面积命中时，也该代码拥有良好的时间局部性。
别忘了，CPU对于指令和数据的操作都需要花时间，那如果二者如果都大面积的缓存命中，可以减少非常多的内存访问操作，对于CPU来说，内存访问就是性能瓶颈所在。
因此编写高速缓存友好的代码是必要的，高手与小白往往只有一步之遥！
基本方法大致如下:
1.让最常见的情况运行得快，核心函数中的核心部分，是影响性能的关键点，它们占据了程序的大部分运行时间，所以要把注意力放在它们身上。
2.尽量减少每个循环内部的缓存不命中数量，循环是缓存工作的重点，一个循环容易带来性能问题，而它恰好也容易被优化成空间、时间局部性良好的代码。
欢迎大家一起交流指正~</div>2021-05-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a6/43/cb6ab349.jpg" width="30px"><span>Spring</span> 👍（107） 💬（9）<div>补充一下MESI协议，MESI分别代表了高速缓存行的四种状态：
最开始只有一个核读取了A数据，此时状态为E独占，数据是干净的，
后来另一个核又读取了A数据，此时状态为S共享，数据还是干净的，
接着其中一个核修改了数据A，此时会向其他核广播数据已被修改，让其他核的数据状态变为I失效，而本核的数据还没回写内存，状态则变为M已修改，等待后续刷新缓存后，数据变回E独占，其他核由于数据已失效，读数据A时需要重新从内存读到高速缓存，此时数据又共享了</div>2021-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/1f/1f/968bc567.jpg" width="30px"><span>aa</span> 👍（20） 💬（4）<div>恍然大悟，原来这就是要求我们写高复用性代码的原因，针对经常会用到的功能封装成通用函数或库，供整个程序调用，这些通用函数装载入cache后，因为其高复用性长久的存在于cache中，cpu自然就跑得更快。</div>2021-09-13</li><br/><li><img src="" width="30px"><span>K菌无惨</span> 👍（11） 💬（1）<div>1.  减少使用带有jmp指令的代码，提高指令cache的局部性（不过cpu貌似有分支预测器来优化jmp指令带来的性能损耗）
2. 对于需要连续访问的数据，可以将其放在一块以提高数据cache的局部性
3. 对于需要被多个CPU执行写操作的多个数据，可以根据cache line的大小对这些数据进行padding操作，来降低缓存一致性协议带来的读写内存频率</div>2021-06-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/2e/44/b6f5b1fd.jpg" width="30px"><span>园园</span> 👍（9） 💬（1）<div>提高Cache的命中率可以从优化指令布局和优化数据布局两个方面开展。比如减少频繁的跳转，数据集中连续存放等。</div>2021-05-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/3e/e7/261711a5.jpg" width="30px"><span>blentle</span> 👍（8） 💬（6）<div>回答一下思考题. 因为缓存行是固定的，32或64个字节，只能在写入内存的数据上尽量补齐，比如一个int 占4个字节(java),32位系统的对象头占8个字节，这样再多写5个int就对齐一个缓冲行了，jdk也提供了一个 annotation 即@Commented来解决，另外内存队列disruptor也用同样的方式优化了同样的问题，但是如此这数据，势必会造成资源浪费，如何权衡这2者还请老师分享一下经验</div>2021-05-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/05/bf/94675989.jpg" width="30px"><span>88</span> 👍（6） 💬（2）<div>《深入理解计算机系统》
6.2 局部性
局部性分为：1. 时间局部性 2. 空间局部性
int sumvec(int v[N])
{
    int i, sum = 0;
    &#47;&#47; sum在每次循环迭代中被引用一次，因此对于sum来说，有好的时间局部性；另一方面因为sum是标量，对于sum来说，没有空间局部性
    for (i = 0; i &lt; N; i++)
    {
        sum += v[i];
        &#47;&#47; 向量v的元素是被顺序读取的，因此对于变量v，函数有很好的空间局部性；但是时间局部性很差，因为每个向量元素只被访问一次
    }
    return sum;
}
&#47;&#47; 所以可以说：以被重复访问的次数衡量时间局部性，以访问是否有序、步长大小衡量空间局部性</div>2021-08-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/4c/05/5cc06ae8.jpg" width="30px"><span>宇宙的琴弦</span> 👍（5） 💬（2）<div>尽量让程序少跳转，比如在if else分支结构中，提高if的条件成立的可能性。在循环需要对变量操作时，应尽量考虑到这些变量的空间存储位置，还有尽量使用局部变量？</div>2021-05-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/eb/28/6786205e.jpg" width="30px"><span>山不厌高，海不厌深</span> 👍（4） 💬（1）<div>二级、三级缓存是冯诺依曼结构，一级缓存是哈佛结构。这样的理解对吗？</div>2021-10-24</li><br/><li><img src="" width="30px"><span>springXu</span> 👍（4） 💬（2）<div>我认为是不是可以尽量加载cache line为单位的数据从内存中，然后进行操作和运算，再放回内存中？ 本质就是减少内存的读与写。像blowfish对一组数据操作时，就可以采取这样的方式。但有像sse,avx512这种指令也是这种理念吧。SIMD单指令多数据流。</div>2021-05-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/cb/ce/d9e00eb5.jpg" width="30px"><span>undefined</span> 👍（4） 💬（1）<div>摩拳擦掌，跃跃欲试。</div>2021-05-24</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLnOMtoDG4yLzicECekHvP0wRmcrfVHOGUHJx4mo89xfRibOvrbOG9Ub2yDrxwHYbZGXbC9fib8R4Elw/132" width="30px"><span>学呀学呀学</span> 👍（3） 💬（2）<div>请问，地址空间中，决定哪些地址给内存，哪些地址给显存，哪些地址给设备IO，这个是由操作系统决定，还是由bios决定呢？</div>2021-07-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/60/81/38b00111.jpg" width="30px"><span>Feen</span> 👍（3） 💬（1）<div>开始有一点点感觉了，个人理解本章的内容背后的本质就是尽量能让CPU执行的操作次数接近o(1)，不管是通过内存管理的优化，还是CPU执行优化，或者cache的策略，都是为了一次执行即可得到有效操作。不要搞多次来回存取数据的事儿。局部性原理用的百分比越高越好。</div>2021-06-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ba/4d/7ba09ff0.jpg" width="30px"><span>郑童文</span> 👍（3） 💬（5）<div>请教老师一个问题：文中说：“中断向量表是由BIOS设置的”。 我理解的中断向量表类似一个包含中断处理程序入口地址的数组，但中断处理程序应该是由操作系统提供的。而BIOS在初始化硬件的时候还没有加载操作系统，那BIOS怎么知道这些中断服务程序的入口地址呢？</div>2021-05-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/92/16/425cf451.jpg" width="30px"><span>深深深</span> 👍（2） 💬（1）<div>结合这个动画可以比较好理解MESI:
https:&#47;&#47;www.scss.tcd.ie&#47;Jeremy.Jones&#47;VivioJS&#47;caches&#47;MESIHelp.htm</div>2022-02-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/3c/8a/900ca88a.jpg" width="30px"><span>神经旷野舞者</span> 👍（2） 💬（1）<div>有没有什么模拟器之类都，可以看到cpu 内存 缓存的情况</div>2021-10-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/f2/f5/b82f410d.jpg" width="30px"><span>Unknown element</span> 👍（2） 💬（1）<div>Cache 和内存交换数据的最小单位是一行
这一行有多少字节就说明计算机的字长是多少吗 比如一行有32字节那么计算机字长就是32？</div>2021-06-02</li><br/><li><img src="" width="30px"><span>Paul Shan</span> 👍（2） 💬（1）<div>如果写出代码对内存的使用单位是和Cache行相一致，这样可以优化Cache调度，是一种用空间换时间的思路。</div>2021-05-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/39/d2/845c0e39.jpg" width="30px"><span>送过快递的码农</span> 👍（2） 💬（3）<div>1.回答思考题
可以参考Java 实现的高性能队列 Disruptor  框架 ，充分利用缓存行的特性，将每个对象包装成64byte的倍数，避免伪共享。尽可能按照连续内存的方式来存储，确保能被缓存加载。
2.我的疑问
1.关于超线程技术  是不是 超线程在同一个物理的核心下的两个逻辑核心，应该是用同个缓存吧？他们是不同的寄存器，对应同一个原子钟？
2.msei协议是不是硬件为了确保数据一致性，对我们不可知的一种行为？Java的volatile关键字是不是也依赖于此？</div>2021-05-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/50/d5/73334a95.jpg" width="30px"><span>doos</span> 👍（1） 💬（1）<div>cpu的缓存感觉和文件系统的缓存很想都是为了弥补性能上的差距，比如cpu比内存快那么，cpu和内存弄一个缓存来弥补速度之差，内存又比磁盘快所以也是弄的buff和cache来弥补这个差距，老师不知道我这样理解对吗</div>2022-04-20</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/q2HwchogzNiavKhIB4GfAxH6B88NhSoC7B7keVEUqiaP6JPokDUNJLYehocOyqYqrhA3iaxywyRXLYkYJjDUQESZw/132" width="30px"><span>残天噬魂</span> 👍（1） 💬（1）<div>有种讲到点到为止的感觉，以MESI协议为例，首先老师讲了这是四种状态，是为了维护cache中的数据一致性，但看了四个状态的说明我反而有些迷糊了，这个状态是什么的状态？[数据只在当前cache中存在]这个说法感觉没有让我加深理解…</div>2021-11-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/b8/3c/1a294619.jpg" width="30px"><span>Panda</span> 👍（1） 💬（1）<div>提高程序的 CPU 亲和性</div>2021-06-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/60/a1/45ffdca3.jpg" width="30px"><span>静心</span> 👍（1） 💬（1）<div>老师能详细解释一下局部性原理和代码怎么结合应用的吗？</div>2021-06-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/3d/8b/47bcc851.jpg" width="30px"><span>何同一</span> 👍（1） 💬（1）<div>在数据布局方面，提高 Cache 命中率除了数据集中连续存放，应该还包括同一块数据集中计算，跨页存放的数据尽量不要放在同一时间块计算。</div>2021-05-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/eb/24/0e54b5dc.jpg" width="30px"><span>瑞兴</span> 👍（1） 💬（1）<div>迟到补卡</div>2021-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/3e/e7/261711a5.jpg" width="30px"><span>blentle</span> 👍（1） 💬（2）<div>一直有个疑问，三级缓存里的数据是何时刷到内存的，是不是有类似超时时间或者最大量限制或者二者都有.</div>2021-05-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/65/32/36c16c89.jpg" width="30px"><span>Geek_osqiyw</span> 👍（1） 💬（1）<div>慢慢有点感觉了</div>2021-05-24</li><br/>
</ul>