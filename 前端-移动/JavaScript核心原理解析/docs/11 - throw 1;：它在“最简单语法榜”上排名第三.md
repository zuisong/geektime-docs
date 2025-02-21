你好，我是周爱民，欢迎回到我的专栏。

今天我将为你介绍的是在ECMAScript规范中，实现起来“最简单”的JavaScript语法榜前三名的JavaScript语句。

标题中的`throw 1`就排在这个“最简单榜”第三名。

> NOTE: 预定的加餐将是下一讲的内容，敬请期待。^^.

## 为什么讲最简单语法榜

为什么要介绍这个所谓的“最简单的JavaScript语法榜”呢？

在我看来，在ECMAScript规范中，对JavaScript语法的实现，尤其是语句、表达式，以及基础特性最核心的部分等等，都可以在对这前三名的实现过程和渐次演进关系中展示出来。甚至基本上可以说，你只要理解了最简单榜的前三名，也就理解了设计一门计算机语言的基础模型与逻辑。

`throw`语句在ECMAScript规范描述中，它的执行实现逻辑只有三行：

> *ThrowStatement* : **throw** *Expression*;  
> 1.**Let** exprRef be the result of evaluating Expression.  
> 2.**Let** exprValue be ? GetValue(exprRef).  
> 3.**Return** ThrowCompletion(***exprValue***).

这三行代码描述包括两个`Let`语句，以及最后一个`Return`返回值。当然，这里的Let/Return是自然语言的语法描述，是ECMAScript规范中的写法，而不是某种语言的代码。
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/89/5b/d8f78c1e.jpg" width="30px"><span>孜孜</span> 👍（1） 💬（1）<div>有一点不太明白，单值表达式` 1 `的result，怎么被转换语句` 1；`的result的？</div>2020-06-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a3/ea/53333dd5.jpg" width="30px"><span>HoSalt</span> 👍（0） 💬（5）<div>老师，块级作用域在实际编码中拿不到，那有什么用，还是说函数调用返回值也是通过这种模式拿到的?</div>2020-05-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/dc/90/c980113a.jpg" width="30px"><span>行问</span> 👍（5） 💬（1）<div>之前阅读本专栏时，也确实遇到没有能够阅读理解，很懵。则去翻看老师的书籍，本专栏结合书的知识点来阅读，会有大大的提高。比如，“值类型”与“引用类型”，在专栏中，我一开始也比较懵的，看书之后再来理解，则是比较清晰。</div>2019-12-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（3） 💬（0）<div>老师讲得挺好的，这个专栏主要是解决这样一个问题：JavaScript 是怎样的一门语言，以及它为什么是这样的一种语言。</div>2019-12-06</li><br/>
</ul>