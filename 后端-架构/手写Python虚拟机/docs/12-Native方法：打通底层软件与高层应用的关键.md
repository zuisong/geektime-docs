你好，我是海纳。

在过去的几节课中，我们实现了函数的基本功能。实际上，在 Python 中有很多内建函数，例如，range、print、len 等都是内建函数。这些内建函数往往是使用 C/C++ 在虚拟机内部实现的，所以我们把这些函数也称为 native 函数。

这节课我们就通过实现 len 方法来讲解如何在虚拟机里实现 native 函数。

## 实现内建函数（Builtin Function）

在 Python 开发者看来，内建函数和普通函数是一样。也就是说，开发者使用自定义的函数和使用 len、print 等内建函数时，并不需要感知它们之间有什么不同。

这就决定了，在虚拟机层面，我们希望内建函数与 FunctionObject 所代表的自定义函数也是统一的。所以我们选择继续使用 FunctionObject 来代表内建函数，不同点在于，普通的FunctionObject 是由 MAKE\_FUNCTION 字节码使用 CodeObject 主动创建的。前边两节课，我们重点介绍了这个机制。

但是内建函数并没有对应的字节码，它的所有实现都在虚拟机内部，也就是说，内建函数都是使用 C++ 来实现的。这里需要一种方法把 CALL\_FUNCTION 与虚拟机内部的实现联系起来。我们还是要在 FunctionObject 身上想办法。
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1f/4f/6a/0a6b437e.jpg" width="30px"><span>有风</span> 👍（0） 💬（0）<div>学习到这里，忍不住给海纳老师点个赞。 </div>2025-01-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡</div>2024-10-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/3b/59/44/727b90a8.jpg" width="30px"><span>冯某</span> 👍（0） 💬（0）<div>这里没有留言</div>2024-10-24</li><br/>
</ul>