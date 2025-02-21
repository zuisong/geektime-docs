你好，我是宫文学。

从今天开始呢，我会带着你去考察实际编译器的具体实现机制，你可以从中学习和印证编译原理的基础知识，进而加深你对编译原理的理解。

我们探险的第一站，是很多同学都很熟悉的Java语言，我们一起来看看它的编译器里都有什么奥秘。我从97年就开始用它，算是比较早了。当时，我就对它的“一次编译，到处运行”留下了很深的印象，我在Windows下写的程序，编译完毕以后放到Solaris上就能跑。现在看起来这可能不算什么，但在当年，我在Windows和Unix下写程序用的工具可是完全不同的。

到现在，Java已经是一门非常成熟的语言了，而且它也在不断进化，与时俱进，泛型、函数式编程、模块化等特性陆续都增加了进来。在服务端编程领域，它也变得非常普及。

与此同时，Java的编译器和虚拟机中所采用的技术，也比20年前发生了天翻地覆的变化。对于这么一门成熟的、广泛普及的、又不断焕发新生机的语言来说，研究它的编译技术会带来两个好处：一方面，Java编译器所采用的技术肯定是比较成熟的、靠谱的，你在实现自己的编译功能时，完全可以去参考和借鉴；另一方面，你可以借此深入了解Java的编译过程，借此去实现一些高级的功能，比方说，按需生成字节码，就像Spring这类工具一样。
<div><strong>精选留言（10）</strong></div><ul>
<li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJOBwR7MCVqwZbPA5RQ2mjUjd571jUXUcBCE7lY5vSMibWn8D5S4PzDZMaAhRPdnRBqYbVOBTJibhJg/132" width="30px"><span>ヾ(◍°∇°◍)ﾉﾞ</span> 👍（5） 💬（1）<div>jabel这种让jdk8支持高版本java语法的项目也是用到了编译技术了吧</div>2020-06-24</li><br/><li><img src="" width="30px"><span>minghu6</span> 👍（2） 💬（1）<div>说编译器成熟后就要自举,这绝对是一个槽点太多以至于无处下嘴的迷思,任何脚踏实地的人不应该迷信这种东西.

首先,不管你如何自举,不可能根本摆脱依赖某些原生操作平台上的工具链的支持,当然也不排除有些人通过重新造轮子的方法把这些工具链全部重新实现一遍,但那只是意味着要额外安装一份儿二进制文件.

对于开发团队来讲,他需要额外管理一个boot build的版本机制,对于用户来讲可怕的来了,他需要先安装一份儿预先编译的版本的然后再把它升级,如果不巧没有合适的直接可以用于升级的预编译的版本,那他将不得不做一个人肉递归,从更早的版本甚至自举前的版本开始逐步升级.由于自举造成的麻烦这不知道浪费了多少人的生命在额外的research&amp;&amp;download, 实际上几个激进自举的语言实现比如Go,比如Clozure CL用起来都有些反直觉,让人花费高时间成本,从一个很不舒服的地方开始.

那么好了,自举有实际的好处吗? 并没有,因为对于一个语言关键得是解决某一类领域的问题具有优势, 不管这个优势是开发效率高\性能表现好\还是上手简单招工容易等等. 人们关注得是否有杀手级应用和大公司的背书,而不是它是否完成了自举.

最后, 个人认为自举在国外流行主要是来源于早期部分黑客&quot;非我不用&quot;的这种有宗教狂热色彩的值得商榷的风格的演化,如果一门语言本身就是用系统原生语言比如C或者其他系统级编程语言比如C++&#47;Rust写的,那我不认为有自举的必要.</div>2021-06-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8c/58/abb7bfe3.jpg" width="30px"><span>易昊</span> 👍（2） 💬（1）<div>老师请教一个问题，最近在看Javac的源码中的词法分析部分，其中Tokens.java中，enum Tag定义有一个是NAMED，我不理解这个NAMED Tag是做什么用的，并且看enum TokenKind的定义，似乎仅有assert, 
boolean, byte, char,  double, enum, float, int, long, short, super, this, void, true, false, null, _  是对应的NAMED tag，想弄明白为什么会这样设计。</div>2021-02-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/da/36/ac0ff6a7.jpg" width="30px"><span>wusiration</span> 👍（2） 💬（1）<div>补交作业，没有看下一讲的答案....
​			odStack     opStack      后续运算符

step1: a

step2: a,b              &gt;                  *

step3: a,b,2           &gt;,*               +

step4: a,b*2          &gt;                  +

step5: a&gt;b*2,3      +                  

step6: a&gt;b*2+7 </div>2020-07-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/2d/92/287f99db.jpg" width="30px"><span>lion_fly</span> 👍（1） 💬（1）<div>老师，我在debugJava编译器的代码：
在源码的注释里面出现了这样的内容
Qualident = Ident { DOT [Annotations] Ident }
Java编译器的这种文法是什么文法，感觉不是上下文无关文法</div>2021-01-21</li><br/><li><img src="" width="30px"><span>Apsaras</span> 👍（1） 💬（1）<div>step1: a
step2: a,b  &gt;   *
step3: a,b,2  &gt;,*  +
step4: a,b*2  &gt;,+
step5: a,b*2,3  &gt;,+
step6: a,b*2+3
step7: a&gt;b*2+3</div>2020-06-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e8/1a/cea701bb.jpg" width="30px"><span>冬天里的懒猫</span> 👍（0） 💬（1）<div>原来竟然是这样。。。
用了这么多年的java，从来没有想过编译器是如何实现的。这篇课程非常有用。</div>2020-10-28</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKdzXiawss5gGiax48CJGAJpha4pJksPia7J7HsiatYwjBA9w1bkrDicXfQz1SthaG3w1KJ2ibOxpia5wfbQ/132" width="30px"><span>chris</span> 👍（0） 💬（2）<div>老师能否介绍一下如何建一个ide工程阅读源码？</div>2020-06-23</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/ibb1HJTBX85TuIYRQv3eUxib5Zdc5paH1mULBaLFZf0N6C1WxLrw6ZUc4oiaEPQEdfrQMkIjIYtTib66l8VfgrtHRQ/132" width="30px"><span>Geek_71d4ac</span> 👍（0） 💬（1）<div>交作业
step1: a
step2: a,b           &gt;     *
step3: a,b,2        &gt;,*   +
step4: a,b*2       &gt;      +
step5:a, b*2,3     &gt;,+  
step6:a, b*2+3   &gt;
step7: a &gt;b *2+3</div>2020-06-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/55/bf/d442b55e.jpg" width="30px"><span>mikewt</span> 👍（1） 💬（0）<div>老师 javacc编译器跟这个有啥关系 为啥java不用javacc编译</div>2023-08-04</li><br/>
</ul>