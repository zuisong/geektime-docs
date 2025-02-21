你好，我是LMOS。

上节课，我们学习了设计一个CPU所需要的相关基础知识，并带你认识了一些后面将会用到的EDA软件工具。看完课程的讲解，还有上手运行的Demo，你是否对接下来要设计CPU已经蠢蠢欲动了？

哈哈，先别着急，我们在设计CPU之前，还有一些很关键的知识需要补充学习。没错，就是CPU的指令集架构。

指令集可以说是一个CPU的基石，要实现CPU的计算和控制功能，就必须要定义好一系列与硬件电路相匹配的指令系统。所以，在设计CPU之初，工程师就应该清楚CPU应该具有怎样的指令架构。

## 什么是指令集？

在第一节课我们讲历史的时候，曾经提到过，CPU既是程序指令的执行者，又被程序中相关的指令所驱动。不过，我并没有具体说明什么是指令。其实指令就是我们交代CPU要执行的操作。

那到底什么是指令集呢？

我给你打个比方：假如你有一条狗，经过一段时间的训练，它能“听懂”了你对它说一些话。当你对它说“坐下”，它就乖乖地坐在地上；当你对它说“汪汪叫”；它就汪汪汪地叫起来，当你对它说“躺下”，它马上就会躺下来……这里你说的“坐下”、“汪汪叫”、“躺下”这些命令，就相当于计算机世界里的指令。

当然，你还可以继续训练狗，让它识别更多指令，我们把所有的这些指令汇总在一起，就是一个指令集。如果指令集里面没有“上厕所”这个命令，那么即使你对狗下这个命令，它也不会去执行。CPU也一样，必须要有特定的指令集才能工作。
<div><strong>精选留言（16）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/76/3d/8120438b.jpg" width="30px"><span>3.141516</span> 👍（4） 💬（1）<div>Java 虚拟机的指令集也是大同小异，不同于 CPU 基于寄存器的架构，JVM 是基于栈的。从寄存器、内存的操作，转变为局部变量表、操作数栈的操作。</div>2022-08-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/3d/38/6f02a4b9.jpg" width="30px"><span>your problem？</span> 👍（2） 💬（6）<div>不知道有没有同学跟我是一样的问题，其实原理认认真真看也大概能明白，但是有很多的名词和细节都需要去查，我个人不是学计算机出身的，底层的东西都是自己后面自学的，之前看过极客上另一位讲计算机原理的老师，他的课程没有详细的讲到CPU指令的部分，像我这种情况老师是建议继续先跟着学习吗，还是先去补充相关知识呢</div>2022-08-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/6b/2c/b27eefc5.jpg" width="30px"><span>Abcd</span> 👍（1） 💬（1）<div>所以思考题的答案是什么？评论区的回答不在电子上啊，老师问的是有了U指令，为什么还需要J指令，两者除了高20位的立即数的表达方式不同外，指令格式完全相同。难道是想表达 U是高20bit的意思，J是低20bit的意思？那也没有必要调整立即数的比特顺序啊。还是说这个是为了尽量和其他指令格式保持一致？节省RTL工程师的工作量？</div>2022-08-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2e/f6/ef/9d19893f.jpg" width="30px"><span>skyline</span> 👍（1） 💬（2）<div>“JAL 指令的执行过程是这样的。首先，它会把 20 位立即数做符号位扩展，并左移一位，产生一个 32 位的符号数”
请问为啥要左移一位呢？</div>2022-08-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/67/b5/8ad13885.jpg" width="30px"><span>王彬</span> 👍（0） 💬（3）<div>&quot;要满足现代操作系统和应用程序的基本运行，RV32G 指令集或者 RV64G 指令集就够了，注意 RV32G 指令集或者 RV64G 指令集，只有寄存器位宽和寻址空间大小不同，这些指令按照功能可以分为如下几类。&quot; 应该是RV32I和RV64I，一个字母的错误会给小白很大的困扰</div>2023-01-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/eb/bf/8acfeaa6.jpg" width="30px"><span>小傅</span> 👍（0） 💬（1）<div>“它会把 20 位立即数做符号位扩展，并左移一位，产生一个 32 位的符号数” 这句话怎么理解？</div>2022-11-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/21/20/1299e137.jpg" width="30px"><span>秋天</span> 👍（0） 💬（1）<div>老师 请教一下，寄存器的作用时什么 用来执行指令对吧？  那操作数和操作码又怎么理解呢？操作码可以理解为指令吗？这块有点晕</div>2022-09-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/1d/bd/6076df28.jpg" width="30px"><span>郝海波</span> 👍（0） 💬（2）<div>JAL 指令的执行过程是这样的。首先，它会把 20 位立即数做符号位扩展，并左移一位，产生一个 32 位的符号数。然后，将该 32 位符号数和 PC 相加来产生目标地址（这样，JAL 可以作为短跳转指令，跳转至 PC±1 MB 的地址范围内）
这里不太懂
20位左移1位不是21位吗
还有最后的PC +1MB 这个！MB怎么来的

</div>2022-09-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/2c/69/6d1a0c98.jpg" width="30px"><span>vampire</span> 👍（0） 💬（1）<div>简化译码电路</div>2022-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/f8/f2/eafca9cd.jpg" width="30px"><span>让我们看云去</span> 👍（0） 💬（1）<div>老师，请教个问题：imm不是按照寄存器的bit从右往左连续分配，这样做的原因是啥？麻烦举个例子说明下帮助理解</div>2022-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/f8/2c/92969c48.jpg" width="30px"><span>青玉白露</span> 👍（0） 💬（2）<div>直接在寄存器内部调整指令，减少了指令读取事件，大大加快了指令执行的整体效率。</div>2022-08-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/63/1a/367ebeac.jpg" width="30px"><span>Jump</span> 👍（0） 💬（1）<div>JAL指令的目标寄存器rd是怎么用的，为啥为0就是goto， 不为0就是函数调用呢？</div>2022-08-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/a6/ad/e65aec4c.jpg" width="30px"><span>苏流郁宓</span> 👍（0） 💬（2）<div>调整立即数形成新指令格式，就不用和内存交换指令信息（省时间），提高cpu的执行效率！</div>2022-08-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/da/d9/f051962f.jpg" width="30px"><span>浩仔是程序员</span> 👍（0） 💬（0）<div>老师你好，为什么没有硬件访问，IO端口映射的指令呢？是直接映射到内存访问的吗？</div>2023-12-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/2f/7a/ab6c811c.jpg" width="30px"><span>相逢是缘</span> 👍（0） 💬（0）<div>“由于访问寄存器中的数据要比访问存储器的速度快得多，一般每条 RISC-V 指令最多用一个时钟周期执行（忽略缓存未命中的情况），而 ARM-32 或者 x86-32 则需要多个时钟周期执行的指令。因为 ARM-32 只有 16 个寄存器，而 X86-32 仅仅只有 8 个寄存器。”   这句话简单理解是：寄存器越多越好？那为什么arm和x86用这么少的寄存器呢？</div>2023-10-25</li><br/><li><img src="" width="30px"><span>Geek_8852cc</span> 👍（0） 💬（0）<div>请问下，JAL指令的立即数为什么要设置成分成四部分排列呢，而不是按顺序排在指令中呢</div>2023-08-03</li><br/>
</ul>