你好，我是大明，一个专注于中间件研发的开源爱好者。

我们都知道，Go 泛型已经日渐成熟，距离发布正式版本已经不远了。目前已经有很多的开发者开始探索泛型会对 Go 编程带来什么影响。比如说，目前我们比较肯定的是泛型能够解决这一类的痛点：

- 数学计算：写出通用的方法来操作 `int` 、 `float` 类型；
- 集合类型：例如用泛型来写堆、栈、队列等。虽然大部分类似的需求可以通过 `slice` 和 `channel` 来解决，但是始终有一些情况难以避免要设计特殊的集合类型，如有序 `Set` 和优先级队列；
- `slice` 和 `map` 的辅助方法：典型的如 map-reduce API；

但是至今还是没有人讨论 Go 泛型的限制，以及这些限制会如何影响我们解决问题。

所以今天我将重点讨论这个问题，不过因为目前我主要是在设计和开发中间件，所以我会侧重于中间件来进行讨论，当然也会涉及业务开发的内容。你可以结合自己了解的 Go 泛型和现有的编程模式来学习这些限制，从而在将来 Go 泛型正式发布之后避开这些限制，写出优雅的 Go 泛型代码。

话不多说，我们现在开始讨论第一点：Go泛型存在哪些局限。

## Go 泛型的局限

在早期泛型还处于提案阶段的时候，我就尝试过利用泛型来设计中间件。当然，即便到现在，我对泛型的应用依旧提留在尝试阶段。根据我一年多的不断尝试，以及我自己对中间件开发的理解，目前我认为影响最大的三个局限是：
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/87/64/3882d90d.jpg" width="30px"><span>yandongxiao</span> 👍（4） 💬（1）<div>不知道是从哪里看到的。

什么时候要使用泛型？
1. write code do not design types. 先写函数，别着急一上来就写泛型，函数泛型化是比较简单的。
2. Functions that work on slices, maps, and channels of any element type. 那些不在乎容器内的元素类型的函数。
3. general purpose data struct，算法，例如，链表、二叉树等。
4. when a method looks the same for all types。当你发现你不得不实现一段重复的逻辑时，就可以考虑泛型。
</div>2022-04-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/f4/58/383cd3a0.jpg" width="30px"><span>洛书</span> 👍（0） 💬（1）<div>最不可接受的是使用[]作为泛型类型声明,
[] 本身已经作为slice,array,map的索引操作符,而且大多数人都有别的语言开发的经验,下意识会把[]当作下表解释. 这才是心智负担. 而使用&lt;&gt;就没有这个问题.
标新立异?</div>2022-02-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/d4/cb/65cc1192.jpg" width="30px"><span>pike</span> 👍（0） 💬（0）<div>当你要为不同的类型写相同逻辑的代码，泛</div>2022-10-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/f4/58/383cd3a0.jpg" width="30px"><span>洛书</span> 👍（0） 💬（0）<div>
type Vector[T any] []T
type Vector&lt;T any&gt; []T

type Vector[T any] [][]T
type Vector&lt;T any] [][]T

孰优孰劣,不难看出,不明白为什么头铁的采用[]包裹泛型声明, 标新立异?</div>2022-02-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/26/27/eba94899.jpg" width="30px"><span>罗杰</span> 👍（0） 💬（0）<div>看起来限制还是非常多，不过对我而言，泛型几乎都没有使用场景。</div>2022-02-11</li><br/>
</ul>