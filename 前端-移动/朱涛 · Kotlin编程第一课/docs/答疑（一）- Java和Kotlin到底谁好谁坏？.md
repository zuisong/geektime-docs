你好，我是朱涛。

由于咱们课程的设计理念是简单易懂、贴近实际工作，所以我在课程内容的讲述上也会有一些侧重点，进而也会忽略一些细枝末节的知识点。不过，我看到很多同学都在留言区分享了自己的见解，算是对课程内容进行了很好的补充，这里给同学们点个赞，感谢你的仔细思考和认真学习。

另外，我看到不少同学提出的很多问题也都非常有价值，有些问题非常有深度，有些问题非常有实用性，有些问题则非常有代表性，这些问题也值得我们再一起探讨下。因此，这一次，我们来一次集中答疑。

## Java和Kotlin到底谁好谁坏？

很多同学看完[开篇词](https://time.geekbang.org/column/article/472129)以后，可能会留下一种印象，就是貌似Java就是坏的，Kotlin就是好的。但其实在我看来，语言之间是不存在明确的优劣之分的。“XX是世界上最好的编程语言”这种说法，也是没有任何意义的。

不过，虽然语言之间没有优劣之分，但在特定场景下，还是会有更优选择的。比如说，站在Android开发的角度上看，Kotlin就的确要比Java强很多；但如果换一个角度，服务端开发，Kotlin的优势则并不明显，因为Spring Boot之类的框架对Java的支持已经足够好了；甚至，如果我们再换一个角度，站在性能、编译期耗时的视角上看，Kotlin在某些情况下其实是略逊于Java的。
<div><strong>精选留言（6）</strong></div><ul>
<li><img src="" width="30px"><span>Paul Shan</span> 👍（9） 💬（2）<div>Java 和Kotlin很难直接比较，因为这两个语言是诞生在不同年代。不过倒是可以从Kotlin的诞生看看两者的区别。Kotlin是Jetbrains公司开发的，Jetbrains是Java的重度使用者，开发跨平台的IDE，这个世界上比Jetbrains公司更擅长Java的公司，怕是不多。Jetbrains选择研发一门新语言本身就说明，现阶段Java不是Jetbrains的最优选择，Jetbrains估计受够了Java的短板，所以才要在Java的基础上迭代。Kotlin在Java的基础上开发的，所以更为简洁顺手。个人觉得将来Kotlin Multiplatform比Kotlin Backend成功的概率更大一些，虽然Kotlin Backend技术上和Kotlin Android没什么差别。这主要是因为Jetbrains是一家精通UI开发的公司，后端开发并非Jetbrains的强项。
Kotlin是Jetbrains俄罗斯团队研发的（Kotlin名字来自于圣彼得堡旁边的小岛），俄乌战争开打以后，Jetbrains就无限期关停了在俄罗斯的研发和销售业务，这给Kotlin Multiplatform等项目蒙上阴影。从Jetbrains的Channel上看，战争开打以来，视频更新明显减少。请问老师，俄乌战争给Kotlin带来的影响会短期过去，还是会成为长期挥之不去的阴影？
</div>2022-03-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/71/c1/cbc55e06.jpg" width="30px"><span>白乾涛</span> 👍（3） 💬（1）<div>Kotlin 舍弃了 Java 中很多容易出错的语法，那为什么引入了 in 却又不支持 6…0 这种写法呢？
这不就是另一个容易出错的语法吗？</div>2022-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/ee/f4/27a5080a.jpg" width="30px"><span>7Promise</span> 👍（3） 💬（1）<div>kotlin中要考虑集合是否可变其实有时候也是麻烦的事情</div>2022-03-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1b/fa/44a3e48a.jpg" width="30px"><span>张国庆</span> 👍（3） 💬（1）<div>使用kotlin是不是包体积会比Java大</div>2022-03-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/3e/ef/4a8d3f89.jpg" width="30px"><span>focus on</span> 👍（2） 💬（2）<div>大佬能多讲讲flow吗，随着flow取代livedata，而且Android上的StateFlow和SharedFlow不好理解</div>2022-03-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/07/6d/4c1909be.jpg" width="30px"><span>PoPlus</span> 👍（1） 💬（1）<div>涛哥，能讲讲 kotlin 中 IntArray、Array&lt;Int&gt; 这些集合的设计缘由吗？</div>2022-04-11</li><br/>
</ul>