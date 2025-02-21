你好，我是周爱民。欢迎回到我的专栏。

相信上一讲的迭代过程已经在许多人心中留下了巨大的阴影，所以很多人一看今天的标题，第一个反应是：“又来！”

其实我经常习惯用**同一个例子**，或者**同类型示例的细微不同**去分辨与反映语言特性上的核心与本质的不同。如同在[第2讲](https://time.geekbang.org/column/article/165198)和[第3讲](https://time.geekbang.org/column/article/165985)中都在讲的连续赋值，看起来形似，却根本上不同。

同样，我想你可能也已经注意到了，在[第5讲](https://time.geekbang.org/column/article/167907)（for (let x of \[1,2,3]) ...）和[第9讲](https://time.geekbang.org/column/article/172636)（(...x)）中所讲述的内容是有一些相关性的。它们都是在讲循环。但第5讲主要讨论的是语句对循环的抽象和如何在循环中处理块。而第9讲则侧重于如何通过函数执行把（类似第5讲的）语句执行重新来实现一遍。事实上，仅仅是一个“循环过程”，在JavaScript中就实现了好几次。这些我将来都会具体地来为你分析。

至于今天，我还是回到函数的三个语义组件，也就是“参数、执行体和结果”来讨论。上一讲本质上讨论的是对“执行体”这个组件的重造，今天，则讨论对“参数和结果”的重构。

## 将迭代过程展开

通过上一讲，你应该知道迭代器是可以表达为一组函数的连续执行的。那么，如果我们要把这一组函数展开来看的话，其实它们之间的相似性是极强的。例如上一讲中提到的迭代函数`foo()`，当你把它作为对象x的迭代器符号名属性，并通过对象x来调用它的迭代展开，事实上也就相当于只调用了多次的return语句。
<div><strong>精选留言（10）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/15/37/e1/0953c506.jpg" width="30px"><span>授人以摸鱼</span> 👍（11） 💬（1）<div>我忽然想明白为啥会有迭代器的next需要支持传入参数这样的功能了……以前一直没想明白来着……
其实就是作为生成器函数的一个应用实例，co模块需要这个功能，需要把yield返回的promise like对象的then方法传回的值从next给生成器函数传回去，这个需求抽象一下，就成了“外部执行环境会需要根据yield传出的结果进行变换后用next传入”这样的通用需求了。
所以我同时也就理解了，为啥说async await是生成器函数的语法糖了，而且这糖真甜wwwww</div>2020-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/53/fd/db2cac71.jpg" width="30px"><span>红白十万一只</span> 👍（5） 💬（3）<div>老师，最近遇到个问题
    if (true) {
        a = 5
        function a() { }
        a = 1
        console.log(a)
    }
    console.log(a)
    1
    5
外部的a变成了5，内部的a变成了1
我查了资料说：
function a() { }的函数提升只提升到了if的代码块顶部，但也有一个var声明被悬挂到了全局中值为undefined
之后在a=5时if内部的变量a从函数被修改为了5
function a() { }这步计算函数声明时，函数对象被分配给函数作用域变量。因为被修改为5，所以此时外部的a也被改变成了5
之后在a=1时if内部的变量a从5被修改为了1
最后输出1 5
我的理解是
函数提升只提升到代码块顶部，但是为了符合函数作用域的规则在最近的函数作用域创建了一个同名变量且值为undefined。
之后再执行到声明语句时将这个函数对象转换为值赋值给这个函数作用域同名变量。
老师有更详细的解释么？我找了ES规范没有发现对这里解释。
</div>2020-03-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（5） 💬（1）<div>如果遇到 yield* 就将当前的yield执行权交到 yield* 里面，yield* 里面return的值，将返回给外层的x  = yield* xxx 中的x</div>2019-12-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ad/b4/ce3964a1.jpg" width="30px"><span>.Alter</span> 👍（4） 💬（2）<div>老师好，我想问一下生成器这个挂起和调用栈移动的机制是协程吗?</div>2019-12-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/c5/e9/4013a191.jpg" width="30px"><span>阿鑫</span> 👍（3） 💬（1）<div>我的理解就是 tor 这个句柄其实就是包含了这个迭代器的一切，包括上下文 context 和执行函数。每次执行 tor.next() 就是把 context 压入栈顶，然后执行执行函数？</div>2019-12-04</li><br/><li><img src="" width="30px"><span>油菜</span> 👍（2） 💬（1）<div>老师，从返回结果比较，“迭代器函数”和“生成器函数”的作用是一样的，都是通过迭代器或生成器的.next()方法，一次调用获取一个值。</div>2020-11-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a3/ea/53333dd5.jpg" width="30px"><span>HoSalt</span> 👍（2） 💬（1）<div>「如果用户代码——通过任意的手段——试图挂起这惟一的执行上下文，那么也就意味着整个的 JavaScript 都停止了执行」
老师，这是什么意思？唯一的执行上下文指全局上下文？</div>2020-05-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/dc/90/c980113a.jpg" width="30px"><span>行问</span> 👍（1） 💬（2）<div>x = yield x

首先，yield 是向函数外发送 x 的值

其次，yield 接收外部传入的参数并赋值给 x

解惑了之前理解 yield 是一个“等待”的过程，没有往“挂起”去构思

时不时会用到 async await 来写并行的 Promise, 但 yield 只知其知识点和应用，还没有开发中实际使用过

</div>2019-12-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/69/20/5cba0aa5.jpg" width="30px"><span>静坐常思己过，闲谈莫论人非</span> 👍（0） 💬（1）<div>如果我能搞懂这些就不是初级前端了，学路漫漫感谢爱民老师</div>2020-09-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/18/65/35361f02.jpg" width="30px"><span>潇潇雨歇</span> 👍（0） 💬（0）<div>先看看yield再来</div>2019-12-04</li><br/>
</ul>