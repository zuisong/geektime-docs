你好，我是郝林，今天我分享的内容是：0基础的你，如何开始入门学习Go语言。

## 1. 你需要遵循怎样的学习路径来学习Go语言？

我们发现，订阅本专栏的同学们都在非常积极的学习和讨论，这让我们非常欣慰，并且和你一样干劲十足。不过，我在留言中发现，大家的基础好像都不太一样，大致可以分为这么几类。

- 零基础的同学：可能正准备入行或者刚刚对编程感兴趣，可以熟练操作电脑，但是对计算机、操作系统以及网络方面的知识不太了解。
- 无编程经验或者编程经验较少的同学：可能正在从事其他的技术相关工作，也许可以熟练编写脚本，但是对程序设计的通用知识和技巧还不太了解。
- 有其他语言编程经验的同学：可能已成为程序员或软件工程师，可以用其他的编程语言熟练编写程序，但是对Go语言还不太了解。
- 有一定Go语言编程经验的同学：已有Go语言编程基础，写过一些Go语言程序，但是急需进阶却看不清途径。

基于以上分类，我为大家制定了一份Go语言学习路径。不论你属于上面的哪一类，都可以按照此路径去学习深造。具体请看下面的思维导图。

![](https://static001.geekbang.org/resource/image/c7/b7/c702df29da67be3c4083ecce1d0eadb7.png?wh=1820%2A7490)

（长按保存大图）

## 2. 学习本专栏前，你需要有哪些基础知识储备？

在这个专栏里，我会假设你有一定的计算机基础，比如，知道操作系统是什么、环境变量怎么设置、命令行怎样使用，等等。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/ZZ8uJu2lYR2tBhjeTHGASiaoyOtTydfyTRE8uq99qcILyrHO9qyALJOaNWXqibORaDVCLmtMYdJsvTt3m7rlPDog/132" width="30px"><span>kanxiaojie</span> 👍（38） 💬（1）<div>这些年看了那么多教程，感觉极客这些课程真的是实在的干货😄</div>2018-12-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/4d/f0/45110cac.jpg" width="30px"><span>会哭的鱼</span> 👍（118） 💬（8）<div>老师还是忍不住询问下，之前是PHP的工作，有好几年了，去年底开始接触GO感觉很喜欢，但是现在公司在转Java，因为Java也要耗费很多精力学习，但是又不想放弃Go，请问有什么好的方式呢？期待您的回答</div>2020-04-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/44/47/3ddb94d0.jpg" width="30px"><span>javaadu</span> 👍（13） 💬（1）<div>c++&#47;c,python,java都学过，目前主力是java，也写一点c++。我学go语言的初衷是前公司使用了很多go开发的中间件（etcd、nsq等等），我希望能了解go语言在并发编程方面的特性，最好在必要的时候可以看懂这些中间件的源码
</div>2018-08-20</li><br/><li><img src="" width="30px"><span>随缘03230323</span> 👍（5） 💬（1）<div>会java，学go语言快吗？</div>2018-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/64/05/6989dce6.jpg" width="30px"><span>我来也</span> 👍（5） 💬（1）<div>在看这篇文章前，已经订阅了慕课网上的《go语言第一课》，也在看《go并发编程实战》第二版。
题外话，与慕课网上的郝林头像相比，还是这里的帅，虽然那里也是真实的。</div>2018-08-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/b8/44/d919d889.jpg" width="30px"><span>lik0914</span> 👍（4） 💬（1）<div>go错误机制，一直搞不太明白，工程实践的好方式呢</div>2018-08-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/46/08/ca51bcc4.jpg" width="30px"><span>王小宇丶</span> 👍（2） 💬（2）<div>请问下老师，思维导图在字面量-&gt;值字面量这个分支中，先说 ”整数字面量本身是无类型的“，但是赋值的时候又说”整数字面量的默认类型是int“ 请问这个改怎么理解呢？</div>2019-12-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f0/41/f6153c7a.jpg" width="30px"><span>Dwyane</span> 👍（2） 💬（1）<div>老师你好，请问老师还可以看到留言吗？我是iOS的，有几点问题问老师。
1.go的前景如何. 跟java比，老师是怎么看待的？
2.mac电脑可以开发吗？我的是苹果电脑，如果不行，我只能装虚拟机或者双系统。</div>2019-03-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4f/7d/dd852b04.jpg" width="30px"><span>chon</span> 👍（2） 💬（3）<div>老师，有啥好用的go的开发工具ide推荐？谢谢</div>2018-12-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ac/a1/43d83698.jpg" width="30px"><span>云学</span> 👍（2） 💬（1）<div>有没有关于〃go语言的缺陷和陷阱〃的好资料</div>2018-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/86/3f/54c815eb.jpg" width="30px"><span>Emily</span> 👍（1） 💬（1）<div>Go 语言基础知识的导图，里面几乎包含了入门 Go 语言所需的所有知识点。 看不到图。。。。</div>2019-08-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/f5/d4/5a0a2f8d.jpg" width="30px"><span>火腿</span> 👍（1） 💬（1）<div>非常好。 大图片是什么软件制作的?</div>2019-01-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/9e/cd/947f20ee.jpg" width="30px"><span>李晨</span> 👍（0） 💬（2）<div>请问基础知识列表的图是丢了吗</div>2022-02-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/92/6d/becd841a.jpg" width="30px"><span>escray</span> 👍（0） 💬（1）<div>我自认为不算是零基础，有一点其他语言编程经验，但是对于 Go 来说，基本上还是白丁。

如果看完了《Go语言学习路线》中，老师罗列给零基础和无编程经验同学的书单，那么很可能已经超过了 80% 的程序员了。

我是打算先看这个专栏和隔壁的《Go 语言从入门到实战》，然后参加训练营，同时也会看一些老师推荐的资源，对我来说尽可能多的练习实践才是更关键的。

有一点好奇，为什么中国 Go 语言的爱好者最多？

另外 Go 语言的官网可以正常访问，也是很让人开心的事情。

看了老师给 @会哭的鱼 的回复，真心希望自己也能够通过学习 Go 语言，找到一份喜欢的工作。</div>2021-03-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/fb/4d/c5ac9df5.jpg" width="30px"><span>Vicky~婵娟</span> 👍（0） 💬（1）<div>老师您好，您的课程干货满满
不过对于真正零基础的学者，可能最开始进入正题之前需要看看go语言的基本用法，这样能对后面分章节的内容有个概念</div>2020-03-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f2/56/c39046c0.jpg" width="30px"><span>Jie</span> 👍（0） 💬（5）<div>Go 语言基础知识的导图在Web端看不到了</div>2020-02-14</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/ibL1llXU2FdfxKhobQZGSbiciaDJLSnibqs1XGrkkmuBKAwmTgGVeibvQicmBJU0p8ia2UkPqIYrRIb90iavcibmlVv1gXw/132" width="30px"><span>ggo</span> 👍（0） 💬（1）<div>基础知识列表 的图不能正常显示出来</div>2019-09-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/10/8d/e95fe102.jpg" width="30px"><span>Kosese</span> 👍（0） 💬（1）<div>为什么我访问不到go hackers的社群，能给个链接嘛😂</div>2019-09-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/13/3f/817f380e.jpg" width="30px"><span>June Yuan</span> 👍（0） 💬（1）<div>老师，The Go Programming Language 不值得推荐吗？我换工作时，新公司要用 go, 为作准备买的就是这本书～</div>2018-10-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fb/44/8b2600fd.jpg" width="30px"><span>咖啡色的羊驼</span> 👍（33） 💬（0）<div>郝老师的学习路线图很棒，进阶之路有方向了。之前《The Go Programming Language》来学习go的，看了好几遍，《go并发编程》第二版今天昨天才开始看，确实查缺补漏了一些基础的点。</div>2018-08-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/4b/22/09540b7c.jpg" width="30px"><span>天之草</span> 👍（9） 💬（0）<div>erlang转go，感觉差别不算大，channel和erlang的消息队列mailbox类似，区别比较大的是erlang每个虚拟进程都是独立的内存。而go的是共享内存，要操作和同步这些内存，最好用协程串行化，保证并发安全</div>2018-08-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/00/53/b8ee8918.jpg" width="30px"><span>灬 黑 礼服 ~</span> 👍（8） 💬（3）<div>运维出身的学习下，就会shell。 希望有更多的收获！！！</div>2018-11-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/fa/6b/6afdd2b9.jpg" width="30px"><span>大毛哥</span> 👍（7） 💬（1）<div>仔细看了第二张图，到这里选这门课已经值了，非常棒</div>2018-08-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/86/72/d9950e17.jpg" width="30px"><span>denglitong</span> 👍（5） 💬（0）<div>看完了《Go语言编程》，到新部门正好是用go语言开发，框架初步定了使用国内的beego框架，正需要进阶go，看到这个专栏毫不犹豫的买了，对goroutine并发不是很懂，下一步准备看《Go并发编程实战》</div>2018-08-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/dc/6f/cc935fa3.jpg" width="30px"><span>学习高手song轻松</span> 👍（4） 💬（0）<div>很全面了，谢谢郝老师，我会努力的ヽ(•̀ω•́ )ゝ</div>2018-08-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/0f/57/f65f059f.jpg" width="30px"><span>Diviner.</span> 👍（4） 💬（0）<div>感谢老师的指点，在前进的路上不至于迷茫。</div>2018-08-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f8/81/8b2dd827.jpg" width="30px"><span>galian</span> 👍（3） 💬（0）<div>我知道了。
https:&#47;&#47;golang.google.cn&#47;</div>2019-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/3b/36/2d61e080.jpg" width="30px"><span>行者</span> 👍（3） 💬（0）<div>两张图收下了，真的很棒。第一张对即便是工作4年的我也有帮助，温故而知新。</div>2018-08-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/64/05/6989dce6.jpg" width="30px"><span>我来也</span> 👍（2） 💬（0）<div>看来老师最近恢复的不错.
有时间出新书,还有时间大段的回复留言了.

我最初,跟随者这个专栏入门了go语言,后来特意换了一份golang的工作.现在入职已经有一年多了.
说实话,这个专栏对面试也非常有帮助.
当初就是靠它,混过了面试那一关.

因为我入职之前并没有golang的实战项目经验,仅仅是靠自学,根本就没法接触一些深层次的东西.
但是看了老师的专栏,对一些概念,混了个脸熟,也会有一点了解.
即使现在入职了一年多,但专栏中的很多知识点,在平常工作中也不常接触.
所以最近专栏的结课测试中,也只能过个及格线一点.

现在准备回过头来查漏补缺.
今天在看`32 | context.Context类型`时,在源码中看到struct里面嵌入interface的用法.
```
type Context interface {
	...
}
type cancelCtx struct {
    Context
	...
}
```
对这个知识点有点疑惑,顺便查了一下,感觉这一篇文章对我比较有帮助,在此也推荐给有需要的小伙伴.
[golang的struct里面嵌入interface](https:&#47;&#47;www.jianshu.com&#47;p&#47;a5bc8add7c6e)

-------------------------
当初降薪跳槽,其实就是冲着柴老师(《Go语言高级编程》作者)去的.
当初他就是面试官之一.😁
比较可惜的是,等我一个月后办完离职手续,入职新公司时,柴老师已经离职了.
</div>2020-05-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/91/b1/fb117c21.jpg" width="30px"><span>先听</span> 👍（2） 💬（1）<div>老师，go语言在接收db过来的null的时候会报错。请问针对这一点也没有什么推荐的比简洁舒服的实践方法呢？</div>2018-12-06</li><br/>
</ul>