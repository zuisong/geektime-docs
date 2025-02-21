你好，我是winter。

上一节课我们已经给你介绍了表达式的一些结构，其中关于赋值表达式，我们讲完了它的左边部分，而留下了它右边部分，那么，我们这节课一起来详细讲解。

在一些通用的计算机语言设计理论中，能够出现在赋值表达式右边的叫做：右值表达式（RightHandSideExpression），而在JavaScript标准中，规定了在等号右边表达式叫做条件表达式（ConditionalExpression），不过，在JavaScript标准中，从未出现过右值表达式字样。

JavaScript标准也规定了左值表达式同时都是条件表达式（也就是右值表达式），此外，左值表达式也可以通过跟一定的运算符组合，逐级构成更复杂的结构，直到成为右值表达式。

关于这块的知识，我们有时会看到按照运算符来组织的讲解形式。

这样讲解形式是因为：对运算符来说的“优先级”，如果从我们语法的角度来看，那就是“表达式的结构”。讲“乘法运算的优先级高于加法”，从语法的角度看就是“乘法表达式和加号运算符构成加法表达式”。

对于右值表达式来说，我们可以理解为以左值表达式为最小单位开始构成的，接下来我们就来看看左值表达式是如何一步步构成更为复杂的语法结构。
<div><strong>精选留言（26）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/d6/bc/026ac6b1.jpg" width="30px"><span>windliang</span> 👍（21） 💬（3）<div>-1 &gt;&gt; 1，-1 的补码是 1111 1111 ... 1111 1111 ，32 个 1，有符号右移，高位补 1，所以还是 1111 1111 ... 1111 1111 ，32 个 1，所以答案依旧是 -1。

-1 &gt;&gt;&gt; 1，-1 的补码是 1111 1111 ... 1111 1111 ，32 个 1，无符号右移，高位补 0，所以是 0111 1111... 1111 1111 ,31 个 1，代表 2 ** 31 - 1= 2147483648 - 1 = 2147483647 。

「在 JavaScript 中，二进制操作整数并不能提高性能」我觉得原因就是 js 数字不管整数还是小数都用 IEEE 754 浮点数标准。所以没有所谓的补码之说，也只有在进行位操作的时候，js 进行转换而已。

之前总结了一篇补码的文章，分享一下.

https:&#47;&#47;mp.weixin.qq.com&#47;s&#47;uvcQHJi6AXhPDJL-6JWUkw

</div>2019-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/1a/cd/5009b8f8.jpg" width="30px"><span>冬Don</span> 👍（4） 💬（1）<div>为什么 [undefined] == 0 是 true, [false] == 0是false呢</div>2019-11-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/55/cb/1efe460a.jpg" width="30px"><span>渴望做梦</span> 👍（1） 💬（2）<div>老师，这篇文章里面每个表达式介绍的时候都说是由上一个表达式构成的，对此我不是很理解，比如一元运算表达式是有更新表达式和一元运算符构成的，但是 typeof a 我怎么看也没看出来哪有更新表达式</div>2019-07-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c0/99/259a412f.jpg" width="30px"><span>Geeker</span> 👍（1） 💬（1）<div>比如本章和前一章对应标准中的 “12 ECMAScript Language: Expression”这一章，但有些内容不是很好懂，可能和标准的行文结构和规范有关，希望老师有时间可以稍做调拨，谢谢！</div>2019-04-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a7/9c/be5dffb6.jpg" width="30px"><span>AbyssKR</span> 👍（72） 💬（6）<div>“逻辑与表达式和逻辑或表达式”一节中，第二个例子 false &amp;&amp; undefined; 的结果为 false</div>2019-04-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/35/d0/f2ac6d91.jpg" width="30px"><span>阿成</span> 👍（31） 💬（1）<div>优先级由高到低：
1 ()
2 .&#47;[] 左
2 new MemberExpression Arguments
3 new MemberExpression 右
4 () 函数调用 左
5 ++&#47;--
6 +&#47;-&#47;~&#47;!&#47;delete&#47;typeof&#47;void&#47;await 右
7 ** 右
8 *&#47;&#47;&#47;% 左
9 +&#47;- 左
10 &lt;&lt; &gt;&gt; &gt;&gt;&gt; 左
11 &lt; &gt; &lt;= &gt;= instance of in 左
12 == === != !== 左
13 &amp; 左
14 ^ 左
15 | 左
16 &amp;&amp; 左
17 || 左
18 ?: 右
19 = 右
20 , 左

不过MDN上的一份整理是这样的：https:&#47;&#47;developer.mozilla.org&#47;zh-CN&#47;docs&#47;Web&#47;JavaScript&#47;Reference&#47;Operators&#47;Operator_Precedence

主要不同的地方集中在：
1. 函数调用与New Expression的优先级顺序（上一课文中有一句不是很理解：而 Call Expression 就失去了比 New Expression优先级高的特性，这是一个主要的区分）
2. ++&#47;-- 前置和后置的优先级顺序（MDN上前置后置优先级是不同的）
3. 缺少了 yield&#47;yield*&#47;...这三个运算符
</div>2019-04-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c0/99/259a412f.jpg" width="30px"><span>Geeker</span> 👍（7） 💬（0）<div>标准里有些东西还是看不太懂，如果可以的话，希望老师在答疑的时候稍微讲解一下如何看懂标准</div>2019-04-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c0/99/259a412f.jpg" width="30px"><span>Geeker</span> 👍（4） 💬（0）<div>评论不能发图片，我把不太明白的地方截图发到了语雀：
https:&#47;&#47;cdn.nlark.com&#47;yuque&#47;0&#47;2019&#47;jpeg&#47;119718&#47;1554814331032-assets&#47;web-upload&#47;a51218b6-cd8a-4ac8-b71f-f8f6dbfeab36.jpeg
麻烦老师移步看一下，谢谢。</div>2019-04-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/9a/e2/271e0caf.jpg" width="30px"><span>依韵</span> 👍（3） 💬（2）<div>false &amp;&amp; undefined 值为false</div>2019-07-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/65/3a/48f3f4e8.jpg" width="30px"><span>白嗣</span> 👍（3） 💬（0）<div>false &amp;&amp; undefined; &#47;&#47; false</div>2019-05-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c0/99/259a412f.jpg" width="30px"><span>Geeker</span> 👍（3） 💬（0）<div>老师是在带我们过 ECMAScript标准，讲解很详细，基本能读懂标准了🌝</div>2019-04-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/3f/d8/dfeeecf0.jpg" width="30px"><span>梧桐</span> 👍（2） 💬（0）<div>“逻辑与表达式和逻辑或表达式”一节中，第二个例子 false &amp;&amp; undefined; 的结果为 false</div>2019-09-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/ff/8a/791d0f5e.jpg" width="30px"><span>晴天</span> 👍（2） 💬（0）<div>左移 n 位相当于乘以 2 的 n 次方，右移 n 位相当于除以 2 取整 n 次。
异或运算有个特征，那就是两次异或运算相当于取消。所以有一个异或运算的小技巧，就是用异或运算来交换两个整数的值。</div>2019-05-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/41/a5/16c615cc.jpg" width="30px"><span>乃乎</span> 👍（2） 💬（0）<div>“字符串和 bool 都转为数字再比较”
这点很重要，也很对
</div>2019-04-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/bb/01/568ac2d6.jpg" width="30px"><span>K4SHIFZ</span> 👍（2） 💬（1）<div>老师，在ES5之前版本规范中，会提及JS的可执行代码分为全局、函数、Eval。但是在ES6之后版本规范中，再也不提及可执行代码的概念了，这是为什么呢？</div>2019-04-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/35/d0/f2ac6d91.jpg" width="30px"><span>阿成</span> 👍（2） 💬（0）<div>文中提到：
按位或表达式由按位或运算符（|）连接相等表达式构成，按位或表达式把操作数视为二进制整数，然后把两个操作数按位做或运算。

这里的相等表达式应该是按位异或表达式吧？
（抱歉小编，之前打错了...）</div>2019-04-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/bb/47/b60ae3eb.jpg" width="30px"><span>你好，阳光</span> 👍（1） 💬（0）<div>文稿中说一元更新表达式是一个更新表达式搭配了一个一元运算符。但是从给的例子如+a,-a这些看不出来，能否换一些更恰当的例子？</div>2021-03-30</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIEODRricvc32UpO3PxoPrFBDgmoGXdiagcibNh0outmZicXFg1icV4c5ibSknc4be3PWUPsIa3OjdMmlwA/132" width="30px"><span>study</span> 👍（1） 💬（1）<div>ExponentiationExpression，这个应该是指数表达式，不是乘法表达式吧。</div>2019-05-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/19/4b/c30b6362.jpg" width="30px"><span>周伟</span> 👍（0） 💬（0）<div>更新表达式的介绍部分有点迷，下面表达式中哪里有更新表达式；delete a.b;void a;typeof a;- a;~ a;! a;await a;
</div>2022-02-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/51/9f/1840385e.jpg" width="30px"><span>胡永</span> 👍（0） 💬（0）<div>作业题目可以通过这个里面的看到答案,标准里通过语法规则表述的很明白:https:&#47;&#47;tc39.es&#47;ecma262&#47;#sec-update-expressions</div>2021-05-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/cb/ce/d9e00eb5.jpg" width="30px"><span>undefined</span> 👍（0） 💬（0）<div>
false &amp;&amp; undefined; 结果写错了，或者想写 ｜｜</div>2021-03-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/c5/dd/5a482cab.jpg" width="30px"><span>杜森垚</span> 👍（0） 💬（0）<div>按位异或表达式 BitwiseANDExpression 这里应该是 BitwiseXORExpression</div>2020-10-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/f3/4a/bf32bb28.jpg" width="30px"><span>石头</span> 👍（0） 💬（0）<div>位运算表达式那里应该是：
按位与表达式由按位与运算符（&amp;）连接相等表达式构成
按位异或达式由按位异或运算符（^）连接按位与表达式构成
按位或表达式由按位或运算符（|）连接按位异或表达式构成</div>2020-06-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/87/62/f99b5b05.jpg" width="30px"><span>曙光</span> 👍（0） 💬（1）<div>&quot;条件表达式由逻辑或表达式和条件运算符构成&quot;,这种表述没看懂，condition ? branch1 : branch2并没有包含逻辑或表达式呀</div>2020-04-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/f7/2f/10cbed82.jpg" width="30px"><span>pcxpccccx_</span> 👍（0） 💬（0）<div>长知识了！</div>2020-03-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/b7/22/84f92c04.jpg" width="30px"><span>qqq</span> 👍（0） 💬（0）<div>终于把Javascript部分给看完了，这门编程语言实在是太多BUG了</div>2020-03-13</li><br/>
</ul>