你好，我是轩脉刃，是[《手把手带你写一个Web框架》](https://time.geekbang.org/column/intro/100090601)专栏的作者。

很高兴应编辑邀请，为 Tony Bai 老师的专栏写一篇加餐文章。Tony Bai大佬是我很早在微博关注的一名Go先行者。他的《Gopher Daily》也是我经常学习阅读的Go语言资料之一。很高兴看到Tony Bai老师在极客时间也开了一个专栏，将他的经验分享出来。

这篇加餐，我主要想和你聊一聊Go语言中常用的一些代码优化点。在Go语言中，如果你不断地在一线写代码，一定多多少少都会有一些写代码的套路和经验。这些套路和经验可以帮助你在实际工作中遇到类似问题时，更成竹在胸。

所以这里，我想和你分享一下我个人在开发过程中看到和使用到的一些常用的代码优化点，希望能给你日常编码带来一些帮助。

## 第一点：使用pkg/errors而不是官方error库

其实我们可以思考一下，我们在一个项目中使用错误机制，最核心的几个需求是什么？我觉得主要是这两点：

- 附加信息：我们希望错误出现的时候能附带一些描述性的错误信息，甚至这些信息是可以嵌套的；
- 附加堆栈：我们希望错误不仅仅打印出错误信息，也能打印出这个错误的堆栈信息，让我们可以知道出错的具体代码。

在Go语言的演进过程中，error传递的信息太少一直是被诟病的一点。使用官方的error库，我们只能打印一条简单的错误信息，而没有更多的信息辅助快速定位错误。所以，我推荐你在应用层使用 github.com/pkg/errors 来替换官方的error库。因为使用pkg/errors，我们不仅能传递出标准库error的错误信息，还能传递出抛出error的堆栈信息。
<div><strong>精选留言（6）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/19/93/2a/08675e68.jpg" width="30px"><span>__PlasticMan</span> 👍（0） 💬（2）<div>白老师，边长参数与函数选项模式的结合一般用什么方式？比如一个函数要传入printf风格的参数，还要添加默认参数</div>2024-01-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/cb/38/4c9cfdf4.jpg" width="30px"><span>谢小路</span> 👍（17） 💬（0）<div>Option 写法，在设计模式中有个专用的名词称呼 —— 函数选项模式。</div>2022-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/26/38/ef063dc2.jpg" width="30px"><span>Darren</span> 👍（6） 💬（2）<div>这里面的With方式，感觉和设计模式中的构建者模式很类似</div>2022-01-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/96/47/93838ff7.jpg" width="30px"><span>青鸟飞鱼</span> 👍（6） 💬（3）<div>这总结太棒了，有个疑问，最后一个，既然那么多大括号，可以拆分成几个函数？这样子会不会更好点？</div>2022-01-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1d/dd/95cdb4d8.jpg" width="30px"><span>helloxiaomin</span> 👍（5） 💬（0）<div>手动点赞，很实用👍</div>2022-01-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9d/a4/e481ae48.jpg" width="30px"><span>lesserror</span> 👍（1） 💬（0）<div>学到了，谢谢叶老师。</div>2022-02-02</li><br/>
</ul>