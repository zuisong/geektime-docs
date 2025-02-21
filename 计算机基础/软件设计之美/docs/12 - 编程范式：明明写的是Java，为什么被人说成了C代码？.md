你好！我是郑晔。

在上一个小模块，我给你讲了程序设计语言，帮助你重新审视一下自己最熟悉的日常工具。但是，使用程序设计语言是每个程序员都能做到的，可写出的程序却是千差万别的。这一讲，我们就来看看这些差异到底是怎样造成的。

在开始之前，我先给你讲一个小故事。

在一次代码评审中，小李兴致勃勃地给大家讲解自己用心编写的一段代码。这段代码不仅实现了业务功能，还考虑了许多异常场景。所以，面对同事们提出的各种问题，小李能够应对自如。

在讲解的过程中，小李看到同事们纷纷点头赞许，心中不由得生出一丝骄傲：我终于写出一段拿得出手的代码了！讲解完毕，久久未曾发言的技术负责人老赵站了起来：“小李啊！你这段代码从功能上来说，考虑得已经很全面了，这段时间你确实进步很大啊！”

要知道，老赵的功力之深是全公司人所共知的。能得到老赵的肯定，对小李来说，那简直是莫大的荣耀。还没等小李窃喜的劲过去，老赵接着说了，“但是啊，写代码不能只考虑功能，你看你这代码写的，虽然用的是Java，但写出来的简直就是C代码。”

正在兴头上的小李仿佛被人当头泼了一盆冷水，我用的是Java啊！一门正经八百的面向对象程序设计语言，咋就被说成写的是C代码了呢？
<div><strong>精选留言（15）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/48/ee/96a7d638.jpg" width="30px"><span>西西弗与卡夫卡</span> 👍（44） 💬（1）<div>当Bob大叔说出那句，“编程范式本质是从某方面对程序员编程能力的限制和规范”时，真有些振聋发聩</div>2020-06-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f2/13/3ee5a9b4.jpg" width="30px"><span>chenzesam</span> 👍（15） 💬（1）<div>不单止编程范式对程序员的能力做了限制，编程框架也在开始做这一方面的努力了。努力提高程序员的下限。</div>2020-06-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f9/88/cdda9e6f.jpg" width="30px"><span>阳仔</span> 👍（8） 💬（2）<div>主流的编程语言都有结构化编程，面向对象编程，函数编程。纯粹单一的使用某个编程范式在现代编程语言其实会越来越少，现代语言都是吸收了各种编程范式的优点组合编程</div>2020-06-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/92/6d/becd841a.jpg" width="30px"><span>escray</span> 👍（7） 💬（1）<div>看到编程范式，首先想到的是左耳听风专栏里面也有过的“编程范式游记”，不过当时似乎没有认真看，而且也没有音频版本，这次正好可以参照着学习一下。

斯坦福大学公开课中有编程范式，同样只看过前面一两讲。很久以前，我上大学的时候，似乎是没有编程范式这门课的（也可能有老师讲过，但是我逃掉了）。

特意去看了一下专栏的目录，编程范式这部分一共有 8 节课。有一点疑惑，为什么要在编程范式上下这么多功夫？

对我来说，结构化编程可能是用的最多的；面向对象也在用，但可能用的不好，甚至不对；函数式编程基本没怎么接触过。

我能够理解，文中所说“将不同编程范式中的优秀元素综合运用在日常工作中”，但是不知道如何去做。

等专栏的这个模块结束的时候，再来回答“编程范式为什么重要”这个问题。</div>2020-06-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/10/bb/f1061601.jpg" width="30px"><span>Demon.Lee</span> 👍（5） 💬（1）<div>而在每个类具体的接口设计上，采用函数式编程的风格
------
老师，这句话具体如何理解，我脑子里出现的是java8里面的@FunctionalInterface，很多接口中的函数入参都是一个个@FunctionalInterface，比如：
public interface Predicate&lt;T&gt; {
default Predicate&lt;T&gt; and(Predicate&lt;? super T&gt; other) {
        Objects.requireNonNull(other);
        return (t) -&gt; test(t) &amp;&amp; other.test(t);
    }
...
}</div>2020-06-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/17/27/ec30d30a.jpg" width="30px"><span>Jxin</span> 👍（4） 💬（1）<div>以函数式编程为例。
1.我能理解不变性的价值，毕竟在应对并发场景时我也用cow的模式。但很难接受将cow贯彻到每个函数，本能的觉得浪费。
2.我看得到函数式编程在代码上的简洁（可读性高）。但将功能实现成函数式编程的风格，感觉比较难（也可能是我水平不行，毕竟没有刻意练习），而难本身就是成本。（业务逻辑翻译成功能代码，从易到难：面向过程，面向对象，函数式编程）。
3.虽然我理解鸭子理论。但我就想明确的定义接口。因为，当我作为调用方时，我只想知道意图，而没有实现的接口，显然是比较整洁的。
4.虽然我理解函数是一等公民（单方法接口）的定位。但我就喜欢接口下定义多个方法（行为），因为我认为接口是一类事务共同行为的抽象，那么行为很可能是捆绑出现。比如说，对动物行为做抽象，吃和拉必须一起出现，只有吃没有拉，只有拉没有吃都挺尴尬。</div>2020-06-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/7a/9c/a4bc748d.jpg" width="30px"><span>Janenesome</span> 👍（2） 💬（1）<div>一定要把这篇转发出去，中小公司的代码里都是平铺直叙，工作了几年，面向对象是什么都忘记了。</div>2020-10-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/43/e1/b7be5560.jpg" width="30px"><span>sam</span> 👍（1） 💬（1）<div>如果有介绍各种需要编程范式发展和应用的资料就好了，比如Objective-C，Swift等等</div>2020-06-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ea/eb/364735a6.jpg" width="30px"><span>LPY</span> 👍（0） 💬（1）<div>老师讲的条理清晰，引人入胜，像看小说一样过瘾</div>2024-11-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/d4/92/fb61d578.jpg" width="30px"><span>solo</span> 👍（2） 💬（0）<div>小李做的就是用脚蹬电瓶车 ，电瓶车也提供了脚蹬子</div>2021-08-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ea/eb/364735a6.jpg" width="30px"><span>LPY</span> 👍（0） 💬（0）<div>老师讲的条理清晰，引人入胜，像看小说一样过瘾</div>2024-11-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/fd/58/1af629c7.jpg" width="30px"><span>6点无痛早起学习的和尚</span> 👍（0） 💬（0）<div>工作 3 年了，第一次这么系统性的了解编程范式这个内容</div>2023-09-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c8/ee/0624b33d.jpg" width="30px"><span>青萍剑客</span> 👍（0） 💬（0）<div>非结构化，结构化，面向对象，函数式！依次是远离冯计算机执行细节，但是更靠近业务，所以抽象层次是越来越高，如果遇到复杂性能场景的性能调优，也是越来越难。但是并不意味着程序员的要求越来越低，反而可能越高。例如函数式编程是我的最爱，如果想做到高度抽象，还是很复杂</div>2023-05-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习不同的编程范式，将其中优秀的元素运用在日常工作中--记下来，可以实践</div>2022-05-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1d/de/62bfa83f.jpg" width="30px"><span>aoe</span> 👍（0） 💬（0）<div>原来编程范式的另一面是告诉大家不要做什么</div>2021-10-26</li><br/>
</ul>