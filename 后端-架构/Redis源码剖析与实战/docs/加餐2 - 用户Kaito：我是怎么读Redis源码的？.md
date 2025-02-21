你好，我是Kaito，也是两季Redis课程的课代表。今天，我想来和你分享一下我读源码的经验，希望能助力你更好地学习Redis源码。

首先，一提到读源码，很多人都会比较畏惧，认为读源码是高手才会做的事情。可能遇到问题时，他们更倾向于去找别人分享的答案。但往往很多时候，自己查到的资料并不能帮助解决所有问题，尤其是比较细节的问题。

那么从我的实践经验来看，遇到这种情况，通常就需要去源码中寻找答案了，因为在源码面前，这些细节会变得一览无余。而且我认为，掌握读源码的能力，是从只懂得如何使用Redis，到精通Redis实现原理的成长之路上，必须跨越的门槛。可是，**面对庞大复杂的项目，我们怎样读源码才能更高效呢？**

所以下面，我就来和你聊一聊我在读源码时的经验和心得。

## 找到地图

很多开源项目的源码，代码量一般都比较庞大，如果在读代码之前，我们没有制定合理的方法，就一头扎进去读代码，势必会把自己搞晕。

所以，我在拿到一个项目的代码之后，并不会马上着手去读，而是会先对整个项目结构进行梳理，划分出项目具体包含的模块。这样，我就对整个项目有了一个宏观的了解。

因为读代码就好比去一个陌生城市旅行，这个旅途过程充满着未知。如果在出发之前，我们手里能有一张地图，那我们对自己的行程就可以有一个非常清晰的规划，我们就知道，如果想要到达目的地，需要从哪里出发、经过哪些地方、通过什么方式才能到达，**有了地图就有了行进方向**，否则很容易迷失。
<div><strong>精选留言（8）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/90/8a/288f9f94.jpg" width="30px"><span>Kaito</span> 👍（32） 💬（5）<div>很荣幸，能在第二季继续给大家带来加餐文章，分享我学习Redis的经验。

这篇文章和大家分享我阅读源码的经验和心得，当然，文章里提到的方法是「通用」的，不仅限于读Redis代码，读任何项目的源码都可以按这个思路来，希望我的分享能够帮助到大家！</div>2021-09-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/52/f7/9b77fadb.jpg" width="30px"><span>Bruis.</span> 👍（3） 💬（3）<div>Kaito大哥，如何对Redis源码进行编译，并能在开发工具上进行debug调试呢？光看源码不debug运行感觉很多细节是没法读懂的啊。</div>2021-09-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/dc/96/9501cd87.jpg" width="30px"><span>无痕之意</span> 👍（1） 💬（0）<div>感谢大佬分享，冲呀，我要学习，加油！！！</div>2022-02-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f3/cf/851dab01.jpg" width="30px"><span>Milittle</span> 👍（1） 💬（0）<div>这个专栏可以说是有两个老师。</div>2021-09-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/9e/39/139f3ee9.jpg" width="30px"><span>fkc_zyk</span> 👍（0） 💬（1）<div>redis是使用C语言写的，采用哪种编译器启动和读源码比较好？</div>2023-05-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e2/97/dfadcc92.jpg" width="30px"><span>Kang</span> 👍（0） 💬（0）<div>没有开发经验也可以这样看吗</div>2021-09-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/7e/5a/da39f489.jpg" width="30px"><span>Ethan New</span> 👍（0） 💬（0）<div>感谢Kaito大佬的分享，向大佬学习</div>2021-09-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/25/7f/473d5a77.jpg" width="30px"><span>曾轼麟</span> 👍（0） 💬（0）<div>感谢Kaito同学的分享，这段时间受益良多</div>2021-09-18</li><br/>
</ul>