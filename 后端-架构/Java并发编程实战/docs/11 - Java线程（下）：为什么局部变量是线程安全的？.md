我们一遍一遍重复再重复地讲到，多个线程同时访问共享变量的时候，会导致并发问题。那在Java语言里，是不是所有变量都是共享变量呢？工作中我发现不少同学会给方法里面的局部变量设置同步，显然这些同学并没有把共享变量搞清楚。那Java方法里面的局部变量是否存在并发问题呢？下面我们就先结合一个例子剖析下这个问题。

比如，下面代码里的 fibonacci() 这个方法，会根据传入的参数 n ，返回 1 到 n 的斐波那契数列，斐波那契数列类似这样： 1、1、2、3、5、8、13、21、34……第1项和第2项是1，从第3项开始，每一项都等于前两项之和。在这个方法里面，有个局部变量：数组 r 用来保存数列的结果，每次计算完一项，都会更新数组 r 对应位置中的值。你可以思考这样一个问题，当多个线程调用 fibonacci() 这个方法的时候，数组 r 是否存在数据竞争（Data Race）呢？

```
// 返回斐波那契数列
int[] fibonacci(int n) {
  // 创建结果数组
  int[] r = new int[n];
  // 初始化第一、第二个数
  r[0] = r[1] = 1;  // ①
  // 计算2..n
  for(int i = 2; i < n; i++) {
      r[i] = r[i-2] + r[i-1];
  }
  return r;
}
```

你自己可以在大脑里模拟一下多个线程调用 fibonacci() 方法的情景，假设多个线程执行到 ① 处，多个线程都要对数组r的第1项和第2项赋值，这里看上去感觉是存在数据竞争的，不过感觉再次欺骗了你。

其实很多人也是知道局部变量不存在数据竞争的，但是至于原因嘛，就说不清楚了。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKTAKspiaW6t3GY9Ht5aWqoJartZYqA3ROTlJgBKK41icia7a5BrcvKnILzzRk4cVBg0DRPhiacl7BgPQ/132" width="30px"><span>uyong</span> 👍（241） 💬（15）<div>栈溢出原因：
因为每调用一个方法就会在栈上创建一个栈帧，方法调用结束后就会弹出该栈帧，而栈的大小不是无限的，所以递归调用次数过多的话就会导致栈溢出。而递归调用的特点是每递归一次，就要创建一个新的栈帧，而且还要保留之前的环境（栈帧），直到遇到结束条件。所以递归调用一定要明确好结束条件，不要出现死循环，而且要避免栈太深。
解决方法：
1. 简单粗暴，不要使用递归，使用循环替代。缺点：代码逻辑不够清晰；
2. 限制递归次数；
3. 使用尾递归，尾递归是指在方法返回时只调用自己本身，且不能包含表达式。编译器或解释器会把尾递归做优化，使递归方法不论调用多少次，都只占用一个栈帧，所以不会出现栈溢出。然鹅，Java没有尾递归优化。</div>2019-03-23</li><br/><li><img src="" width="30px"><span>suynan</span> 👍（78） 💬（12）<div>对于这句话：“ new 出来的对象是在堆里，局部变量在栈里”
我觉得应该是对象在堆里，引用（句柄）在栈里</div>2019-03-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/48/ee/96a7d638.jpg" width="30px"><span>西西弗与卡夫卡</span> 👍（27） 💬（1）<div>因为调用方法时局部变量会进线程的栈帧，线程的栈内存是有限的，而递归没控制好容易造成太多层次调用，最终栈溢出。

解决思路一是开源节流，即减少多余的局部变量或扩大栈内存大小设置，减少调用层次涉及具体业务逻辑，优化空间有限；二是改弦更张，即想办法消除递归，比如说能否改造成尾递归（Java会优化掉尾递归）</div>2019-03-23</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83er6ADlY3IFt3Rs1aVDyrTO2BiaV8wiabypPwbXhbPcyqicCvnTV9lUYHULVqUab7ww4taX5QbmFyatLQ/132" width="30px"><span>Geek_cc0a3b</span> 👍（26） 💬（9）<div>new 出来的对象是在堆里，局部变量是在栈里，那方法中new出来的对象属于局部变量，是保存在堆里还是在栈里呢？</div>2019-03-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/fe/4c/46eb517a.jpg" width="30px"><span>Xiao</span> 👍（19） 💬（11）<div>如果方法内部又有多线程，那方法内部的局部变量是不是也不是线程安全。</div>2019-03-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4a/45/04a13bf9.jpg" width="30px"><span>bing</span> 👍（16） 💬（1）<div>当遇到递归时，可能出现栈空间不足，出现栈溢出，再申请资源扩大栈空间，如果空间还是不足会出现内存溢出oom。
合理的设置栈空间大小；
写递归方法注意判断层次；
能用递归的地方大多数能改写成非递归方式。</div>2019-03-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/a6/6a/d5cbc4e9.jpg" width="30px"><span>卡西米</span> 👍（9） 💬（1）<div>请教一个问题JAVA的栈跟cpu的栈有什么关系？</div>2019-03-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/67/8a/babd74dc.jpg" width="30px"><span>锦</span> 👍（8） 💬（7）<div>老师我有个问题：有一个方法的参数是引用类型，方法内定义了一个局部变量，在方法内将引用类型的参数赋值给该局部变量，然后再操作该局部变量会不会存在线程安全问题？比如：
void test(account a){
    account b = a;
    b.addMoney(100);
}</div>2019-04-19</li><br/><li><img src="" width="30px"><span>Thong2018</span> 👍（7） 💬（1）<div>看老师讲Java并发编程的知识，让我明白了很多之前在大学里没有学明白的知识点。要是大学的专业课本也能像老师这样讲得通俗易懂而又不失深度就好了，用“大道至简”来形容老师的授课风格再好不过了</div>2019-08-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/57/f9/3eadb0fd.jpg" width="30px"><span>文兄</span> 👍（6） 💬（2）<div>局部变量是线程安全的
对于这句话我的理解是，在方法内创建的变量是线程安全的
那么方法的入参，是否是线程安全的呢
方法的入参是对象的情况下还是否是线程安全的呢

希望有大手子答疑</div>2019-12-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/dd/5e/ddbdde5a.jpg" width="30px"><span>邢宇超</span> 👍（4） 💬（3）<div>CPU 的堆栈寄存器和栈帧什么关系  老师  求你回答一下我一个问题吧  我的问题你都没回答过</div>2019-07-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/fa/d8/7c2b6c0b.jpg" width="30px"><span>闲人</span> 👍（3） 💬（1）<div>老师，有两个疑问求解答：
1.程序计数器和CPU栈寄存器是一回事吗？
2.线程切换会导致CPU堆栈寄存器来回刷新吗？</div>2019-12-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/e9/0b/1171ac71.jpg" width="30px"><span>WL</span> 👍（3） 💬（1）<div>请教一下老师, 在静态方法中的局部变量是线程安全的吗, 静态方法的执行机制能不能也讲一下, 这里不是很理解.</div>2019-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/50/da/ed4803cb.jpg" width="30px"><span>CCC</span> 👍（3） 💬（2）<div>参数和局部变量一样都是线程私有的吧，我有点不理解如果引用类型的参数被传入时，多线程同时修改这个引用类型的参数不就直接对这个参数引用的堆内存对象并发修改了嘛？</div>2019-03-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/87/c4/50c8a490.jpg" width="30px"><span>早起的鸟儿</span> 👍（2） 💬（1）<div>老师请问如果一个局部变量的引用是指向一个全局容器里面的某个可变对象，那么该局部变量还是线程安全的吗？</div>2019-08-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/26/1f/91f980cc.jpg" width="30px"><span>Tuberose</span> 👍（2） 💬（3）<div>还有一点就是 静态方法是否是线程安全的？j</div>2019-03-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/4a/35/16861bf8.jpg" width="30px"><span>蒋波</span> 👍（1） 💬（1）<div>徐老师您好，局部变量都是线程私有，但是变量指向的数据是同一条数据，或者对象是同一个对象，我们应该怎么思考这个问题呢？我是不是也应该考虑并发问题，但是应该在获取这个数据或者对象阶段考虑并发问题，是吗，希望老师给指点迷津，没有共享就没有并发问题，这句话具体落到实处应该怎么思考太迷惑了</div>2021-09-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/2f/ce/c72d4c67.jpg" width="30px"><span>movesan</span> 👍（1） 💬（1）<div>我的理解是 JVM 也是内存中规划出来的结构吧，也是属于内存的一部分，所以说 JVM 中的调用栈应该都是存在于内存中；
但是最终都会被编译成计算机指令，CPU 调用的时候是依赖于自己寄存器中的栈结构。
请问老师，我这样理解对吗？如果对的话，方法参数和局部变量也会被编译到寄存器中吗，那这样应该放不下吧，CPU 寄存器中的栈和 JVM 中的方法栈是否有联系呢？感谢老师回答</div>2020-02-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/74/3c/da79d2a1.jpg" width="30px"><span>朕爱吾妃</span> 👍（1） 💬（1）<div>每一次递归到一个方法上时，就会在有一个入栈的操作，当方法执行结束，就会有出栈，当递归过多的时候，就会有很多入栈的操作而没有出栈的操作，造成栈容量越来越大，而栈内每一个变量引用都是需要占用内存的，也就说明栈是有大小的，所以，当超出了栈最大容量的时候，就会造成栈溢出的情况的，这就是原因所在。</div>2019-11-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/15/03/c0fe1dbf.jpg" width="30px"><span>考休</span> 👍（1） 💬（2）<div>递归调用如果没有结束条件，或者结束条件永远达不到，则会造成永久循环调用，而每次递归调用都是创建一个新的栈帧，会造成栈帧数超过系统最大值，造成栈溢出。在Java中会抛出以下错误：Exception in thread &quot;main&quot; java.lang.StackOverflowError</div>2019-11-05</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erQ5LXNgaZ3ReArPrY4YeT5mNVtBpiazFEQzNuUXxzdLOWtMliaGicNCpjaOezRISARHXPibkA4ACgib1g/132" width="30px"><span>JensonYao</span> 👍（1） 💬（1）<div>非常形象的解释了堆和栈的区别，又带着复习了一遍基础知识，每一次看都有不一样的认知！谢谢老师！</div>2019-04-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/07/8c/0d886dcc.jpg" width="30px"><span>蚂蚁内推+v</span> 👍（1） 💬（1）<div>线程封闭：jdbcConnection 如何保证线程封闭这块方便老师具体讲解下吗~</div>2019-03-24</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erTlRJ6skf7iawAeqNfIT1PPgjD7swUdRIRkX1iczjj97GNrxnsnn3QuOhkVbCLgFYAm7sMZficNTSbA/132" width="30px"><span>senekis</span> 👍（1） 💬（1）<div>感动！老师讲的太好了，每次的新文章，都解答了我在以前学习中所留下的许多疑问！
</div>2019-03-24</li><br/><li><img src="" width="30px"><span>Geek5530</span> 👍（0） 💬（1）<div>老师，有个问题请教下，这里的局部变量是不是不区分是基本数据类型还是引用型</div>2022-06-04</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTI5eicXFWltiaF9ibsEh2nNC80OYoHibhhE0X1hPHZ5KuAtY4Yxp5dQ4LsciaDxUHFBPlJM7kgQwkspzsQ/132" width="30px"><span>官宝儿</span> 👍（0） 💬（1）<div>又看完一章老老实实回答问题，分享所得，老师文章所述，程序运行中在jvm内部会有方法调用栈，在方法被调用时会创建栈帧，递归的过程中会不停的调用方法，不停的递归以为这栈帧不停的增长，达到栈的上限时，就会发生堆栈溢出异常了。</div>2021-10-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4a/96/99466a06.jpg" width="30px"><span>Laughing</span> 👍（0） 💬（1）<div>递归创建的调用栈太多的原因，尤其递归方法内有大量内部变量时。一方面，尽量减少栈内部的变量占用；另一方面，对调用递归的条件作出限制，防止无限递归或太多层次的递归。</div>2021-03-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4d/90/25b6f544.jpg" width="30px"><span>马文龙</span> 👍（0） 💬（1）<div>王老师，您好！
数据库连接池通过线程封闭技术，保证一个 Connection 一旦被一个线程获取之后，在这个线程关闭 Connection 之前的这段时间里，不会再分配给其他线程，从而保证了 Connection 不会有并发问题
用什么技术实现的，代码示例能举例吗？</div>2021-02-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/1d/f0/59702429.jpg" width="30px"><span>idea</span> 👍（0） 💬（1）<div>调用层数过深，会导致我们创建栈一直在增加而没有弹出释放，每个线程所分配的栈空间都是有限的，当调用次数超过瓶颈的时候就会爆出栈溢出的问题。而且同理可以推断，当我们的参数变量过多的时候，栈帧的空间会不足而出现异常。 老师我的这个理解正确吗？</div>2020-07-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/81/e6/6cafed37.jpg" width="30px"><span>旅途</span> 👍（0） 💬（1）<div>老师问个问题 您说new出来的对象在堆里  但是在方法里new 出来的变量  应该是在堆里 但是应该不会产生线程安全问题吧  </div>2020-02-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d1/29/1b1234ed.jpg" width="30px"><span>DFighting</span> 👍（0） 💬（1）<div>栈溢出的原因是没限制最大深度，在一个有限大小的栈空间中，每次就算申请微小的栈帧，早晚也会爆炸，解决思路有两个吧：
1、治标：预防溢出，可以限制深度，备忘录等
2、治本：用非递归的代码来实现递归的思路
最后有个问题，局部变量不存在并发问题，好像和Fork&#47;Join思路蛮相似的，都是在无关共享资源的前提下实现并发，没用共享，也就没用太多的问题了。</div>2019-09-19</li><br/>
</ul>