你好，我是朱涛。在上一节实战课当中，我们算是用Kotlin实践了一把函数式编程的思想。不过，上节课我们其实只是浅尝辄止，也不完全算是函数式编程，咱们只是借鉴了它的思想。

函数式编程（Functional Programming），是一个跟“[面向对象](https://time.geekbang.org/column/article/473349)”类似的概念，它也是软件工程中的一种编程范式，它是声明式编程（Declarative Programming）的一种，而与它相反的，我们叫做命令式编程（Imperative Programming）。

虽然说，Kotlin的函数式编程还不属于主流，但近几年它的关注度也越来越高了，所以今天我们就借着这节加餐，一起来简单聊聊Kotlin的函数式编程，也为上一节实战课做一个延伸。这样，等将来你想深入研究Kotlin函数式编程的时候，有了这节课的认知基础，也会更加轻松。

## 函数式与命令式的区别

那么，在介绍函数式编程之前，我们首先要来看几个编程范式的概念：声明式、命令式，还有四个常见的编程范式：函数式、逻辑式、面向过程、面向对象。它们之间的关系大致如下图所示：

![图片](https://static001.geekbang.org/resource/image/12/6a/12fe0504cd5329b2634a6b3746c0yy6a.jpg?wh=1920x1013)

我们的校园里学习编程的时候，一般都是学的C、Java，它们分别是面向过程语言、面向对象语言的代表，它们都属于“命令式”的范畴。
<div><strong>精选留言（19）</strong></div><ul>
<li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Iofqk26ibmjFxAZKRibgUmwc9p5RDDArr9Jt0NTrwTKOhtPTuuia77OxOwyEUpeqp2fvU5HPpY8sK0vBejJNA3ib3w/132" width="30px"><span>夜月</span> 👍（6） 💬（1）<div>函数式编程更多的是带来方便：
1. 更少地声明临时变量
2.使用库或者标准api更方便
但是我个人觉得，引入大量库后，全局作用域的扩展函数过多时，也会导致ide的函数选择提示过长，容易出错。</div>2022-01-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/86/31/b55a328a.jpg" width="30px"><span>阿辛</span> 👍（4） 💬（1）<div>感觉比慕课的讲得好. 慕课的kotlin讲的比较难</div>2022-02-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/d6/a7/ac23f5a6.jpg" width="30px"><span>better</span> 👍（3） 💬（1）<div>个人感觉，在使用 kt 函数式方法的时候，最好看一下此方法的实现，否则就容易造成时间复杂度更高，比如：在不知不觉中 for 嵌套了（我还在展示，你看代码多简洁哈），这也是一个性能方面的问题吧</div>2022-01-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/07/6d/4c1909be.jpg" width="30px"><span>PoPlus</span> 👍（2） 💬（1）<div>想了解不变性无状态等特点更适合并发编程的原因～</div>2022-01-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/ee/f4/27a5080a.jpg" width="30px"><span>7Promise</span> 👍（1） 💬（1）<div>函数式编程在我理解中和函数单一功能原则有关系，将各个功能分解成尽量少代码的函数，运用在各个可能存在的地方。再加上巧妙运用kotlin自带或者自己编写的高级函数以及拓展函数。</div>2022-01-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a2/df/924756fe.jpg" width="30px"><span>Durian_</span> 👍（0） 💬（1）<div>我有点不太理解这句话：
无副作用的函数，它具有引用透明的特性。
这个透明是什么意思呢？</div>2022-05-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/a2/1b/0a4f9177.jpg" width="30px"><span>vox</span> 👍（0） 💬（2）<div>请问既然函数式和命令式各有优劣，那么在Android日常开发中哪些场景中建议使用函数式的写法呢？</div>2022-04-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/d6/a7/ac23f5a6.jpg" width="30px"><span>better</span> 👍（0） 💬（2）<div>有些地方，比如 list 类型的类成员，如使用函数式，比如：filter 某些，形成新的 list，确实可以避免并发编程的状态问题，但是，每次都fitler成本也是很大的，此时需要取舍了：是弄一个新的成员变量记录 filter 后的 list，还是直接函数式过滤（如果 list 很大，filter 函数式函数经常调用，性能问题，就需要考虑了）</div>2022-01-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/71/7b/4b6079e6.jpg" width="30px"><span>侯金博</span> 👍（0） 💬（1）<div>醍醐灌顶，拨云见日</div>2022-01-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/59/66/e2839938.jpg" width="30px"><span>杨浩</span> 👍（0） 💬（1）<div>才接触kotlin，个人理解如果是Android，kotlin就是生产力值得深耕，绝大多数情况kotlin即可，少数需要高性能的用java。

我的理解如果是用在服务端，kotlin适合高并发、IO类的应用，不适合计算型。</div>2022-01-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/8c/3c/bb79b9d7.jpg" width="30px"><span>Will</span> 👍（0） 💬（1）<div>博采众长，很重要啊，这篇文章，我感觉就挺好。
如果硬是按个别读者的要求，多塞技术难点进去，不见的能起到普传的效果。</div>2022-01-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/9e/4b/bb734fa7.jpg" width="30px"><span>new start</span> 👍（0） 💬（1）<div>这个餐有点少，不够吃</div>2022-01-14</li><br/><li><img src="" width="30px"><span>20220106</span> 👍（0） 💬（1）<div>第一感觉，这种”类函数式编程“仍然是在表面上改变，看到的简洁其背后仍旧是机械化的工作重复，我的意思是这种变化是有限的，即使这种变化很被人接受。就比如如今的AI和人本身还相距甚远。</div>2022-01-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1a/ca/50c1fd43.jpg" width="30px"><span>colin</span> 👍（0） 💬（1）<div>催更啦</div>2022-01-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/93/a6/679b3c6b.jpg" width="30px"><span>Renext</span> 👍（0） 💬（1）<div>详细聊聊 Kotlin 函数式编程在 Compose 当中的体现吧</div>2022-01-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f9/c5/95b97dfa.jpg" width="30px"><span>郑峰</span> 👍（1） 💬（0）<div>只买对的，不买贵的！</div>2022-07-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/91/e6/03582dee.jpg" width="30px"><span>牧名</span> 👍（0） 💬（0）<div>函数式编程的一大重点就是纯函数，那么老师可以说一下集合类的forEach方法的具体使用场景吗？（实际工作中会发现很多同事会使用这个方法来修改外部状态）</div>2025-01-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/db/95/daad899f.jpg" width="30px"><span>Seachal</span> 👍（0） 💬（0）<div>无副作用的函数，它具有引用透明的特性。
无副作用的函数，它具有无状态的特性。  引用透明，无状态，这两个可以具体描述下吗？</div>2023-04-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/13/c5/791d0f5e.jpg" width="30px"><span>大列巴</span> 👍（0） 💬（0）<div>函数编程，函数的实现逻辑依然是命令式编程；在上次调用者的角度，不用关注函数的具体实现，所以看起来函数式编程会跟方便；

在实际开发中，能够使用标准库的情况下，我们使用标准库的函数编程，可以调高我们的开发效率；同时，也需要我们根据自己的业务去扩展或封装一些新的函数，为我们的项目服务。因此还需要使用命令式去开发函数。

我理解的对不？</div>2023-03-06</li><br/>
</ul>