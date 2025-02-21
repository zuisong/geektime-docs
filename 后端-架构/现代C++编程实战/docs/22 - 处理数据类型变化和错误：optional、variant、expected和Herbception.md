你好，我是吴咏炜。

我们之前已经讨论了异常是推荐的 C++ 错误处理方式。不过，C++ 里有另外一些结构也很适合进行错误处理，今天我们就来讨论一下。

## optional

在面向对象（引用语义）的语言里，我们有时候会使用空值 null 表示没有找到需要的对象。也有人推荐使用一个特殊的空对象，来避免空值带来的一些问题 \[1]。可不管是空值，还是空对象，对于一个返回普通对象（值语义）的 C++ 函数都是不适用的——空值和空对象只能用在返回引用/指针的场合，一般情况下需要堆内存分配，在 C++ 里会引致额外的开销。

C++17 引入的 `optional` 模板 \[2] 可以（部分）解决这个问题。语义上来说，`optional` 代表一个“也许有效”“可选”的对象。语法上来说，一个 `optional` 对象有点像一个指针，但它所管理的对象是直接放在 `optional` 里的，没有额外的内存分配。

构造一个 `optional<T>` 对象有以下几种方法：

1. 不传递任何参数，或者使用特殊参数 `std::nullopt`（可以和 `nullptr` 类比），可以构造一个“空”的 `optional` 对象，里面不包含有效值。
2. 第一个参数是 `std::in_place`，后面跟构造 `T` 所需的参数，可以在 `optional` 对象上直接构造出 `T` 的有效值。
3. 如果 `T` 类型支持拷贝构造或者移动构造的话，那在构造 `optional<T>` 时也可以传递一个 `T` 的左值或右值来将 `T` 对象拷贝或移动到 `optional` 中。
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/6a/c4/8679ca8a.jpg" width="30px"><span>廖熊猫</span> 👍（2） 💬（1）<div>有的语言里面没有try catch，统一使用类似optional的结局方案，比如Rust里面的Err，Haskell中对应的应该是Either类型，这些都是处理可以恢复的错误，不可恢复的直接就让程序崩了。
lift_optional让我想起来被Haskell支配的恐惧 (Just (+) ) &lt;*&gt;  Just 41 &lt;*&gt; Just 1
不知道老师后面会不会讲到monad😂</div>2020-01-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/bc/25/1c92a90c.jpg" width="30px"><span>tt</span> 👍（2） 💬（2）<div>老师，听了您的课后，觉得现在C++标准提案有很多都是利用C++的语义和语法来写提升编程便利性的模板，是这样么？

还有，一直不知道C++的异常是怎么实现的，还有这里说的异常处理的性能问题，有推荐的比较好阅读的参考文献么？</div>2020-01-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/cf/9e/e695885e.jpg" width="30px"><span>×22</span> 👍（0） 💬（1）<div>&quot;就我们上面的例子而言，obj.index() 即为 1。&quot; 这里应该是0吧</div>2024-03-27</li><br/><li><img src="" width="30px"><span>Geek_7d9f3b</span> 👍（0） 💬（2）<div>C++中是否有关闭异常的方式，实践中经常遇到分配内存时出现了bad_alloc直接让程序terminate掉了，涉及的历史代码又非常多，一个个try catch(...)既耗时又会造成程序性能的下降…</div>2023-09-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/cf/9e/e695885e.jpg" width="30px"><span>×22</span> 👍（0） 💬（1）<div>感觉optional就和rust里面的Option&lt;&gt;一样？</div>2022-09-27</li><br/>
</ul>