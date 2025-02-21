你好，我是宫文学。

上一节课，我们用了很简单的方法就实现了语法分析。但当时，我们省略了词法分析的任务，使用了一个Token的列表作为语法分析阶段的输入，而这个Token列表呢，就是词法分析的结果。

其实，编译器的第一项工作就是词法分析，也是你实现一门计算机语言的头一项基本功。今天，我们就来补补课，学习一下怎么实现词法分析功能，词法分析也就是把程序从字符串转换成Token串的过程。

词法分析难不难呢？我们来对比一下，语法分析的结果是一棵AST树，而词法分析的结果是一个列表。直观上看，列表就要比树结构简单一些，所以你大概会猜想到，词法分析应该会更简单一些。

那么，具体来说，**词法分析要用什么算法呢？词法是不是也像语法一样有规则？词法规则又是如何表达的？这一节课，我会带着你实现一个词法分析器，来帮你掌握这些技能。**

在这里，我有个好消息告诉你。你在上一节课学到的语法分析的技能，很多可以用在词法分析中，这会大大降低你的学习难度。好了，我们开始了。

## 词法分析的任务

你已经知道，词法分析的任务就是把程序从字符串转变成Token串，那它该怎么实现呢？我们这里先不讲具体的算法，先来看看下面这张示意图，分析一下，我们人类的大脑是如何把这个字符串断成一个个Token的？  
![图片](https://static001.geekbang.org/resource/image/bb/9d/bb2999fdb744515f715eac0d0eb4559d.jpg?wh=1920x851 "图1：词法分析是把字符串转变为Token串")  
你可能首先会想到，借助字符串中的空白字符（包括空格、回车、换行），把这个字符串截成一段段的，每一段作为一个Token，行不行？
<div><strong>精选留言（13）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1f/cc/12/3d15531b.jpg" width="30px"><span>yjhmelody</span> 👍（3） 💬（1）<div>首先考虑是否有一元运算符-，没有则为整体解析。然后考虑支不支持该运算符的重载，如果有则可能分开解析更好。其他情况均可以，取决于实现者如何看待这个-号</div>2021-08-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/c4/f1/536fcb23.jpg" width="30px"><span>船</span> 👍（0） 💬（1）<div>为什么在用cmd运行这节代码时会出现？
Usage: node D:\craft-a-language\02\play.js FILENAME</div>2021-09-14</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIicr82CnrdEjibibAvyeKRQHszSzIAqoCWxN0kqC442XcjEae6S9j6NDtKLpg4Da4CUQQeUFUicWqiaDw/132" width="30px"><span>有学识的兔子</span> 👍（0） 💬（1）<div>-3作为一个负数字面量，会减少一个减法表达式，从这章的内容看，语法分析过程中会因为回溯会影响效率，减少不必要的规则表达式也是提升效率一种方式。从词法分析上把-3当作一个token识别出来，性能消耗可能并不多。</div>2021-08-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/c2/cc/ca22bb7c.jpg" width="30px"><span>蓝士钦</span> 👍（0） 💬（2）<div>如果要自己实现一个JSON parse、或者PDF parse，只需要识别Token即可，整个过程和写一个有限自动机一样，这些parse比写一门语言要来的简单吧
</div>2021-08-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/b1/17/4e533c1b.jpg" width="30px"><span>王</span> 👍（0） 💬（3）<div>老师，我觉得应该把-3整体当做一个字面量解析。如果解析成一个-和一个3的话，就是减法运算了，减法是需要两个数的。如果非要解析为减法运算，是不是被减数还得默认设置为0</div>2021-08-11</li><br/><li><img src="" width="30px"><span>springXu</span> 👍（0） 💬（1）<div>把-3作为整体，计算机中负数是用补码来表示负数的。这样把字符转换成数字方便了。</div>2021-08-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/7b/2b/848dbded.jpg" width="30px"><span>星小哥</span> 👍（0） 💬（0）<div>建议代码少一点else{} 嵌套，比如 以下的else没有必要
if (this.stream.eof()) {
            return { kind: TokenKind.EOF, text: &quot;&quot; };
        }
        else {}
</div>2023-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡</div>2022-09-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/3c/8a/900ca88a.jpg" width="30px"><span>神经旷野舞者</span> 👍（0） 💬（0）<div>老师能不能把每节课的要求列一下，因为不懂得太多，不知道理解到什么程度可以进入下一节</div>2022-07-03</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/icHMBoxO5zDicEgIOkFsZCsbicMAeaW3zd7e6YjJJKfvwu7Q8E3wtpXojfdClOeCGrPicJ16FBpEMicfpuDiariajibDSg/132" width="30px"><span>Jack_1024</span> 👍（0） 💬（0）<div>这样实现是自举对吗？</div>2022-04-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/09/db/78996b11.jpg" width="30px"><span>Gaollard</span> 👍（0） 💬（0）<div>我觉得都可以，比如 -5 - (20 * 2) 在词法分析阶段中 -5 可以作为一个 token，而后面的 &quot;-&quot; 可以被解析为 unary operator。</div>2022-01-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/02/12/ce3dc4c8.jpg" width="30px"><span>喵咪爱吃肉</span> 👍（0） 💬（0）<div>能否给出一些运行的例子呢？这样运行代码时通过这个例子才更加理解，比如这个章节我大概理解是要干什么，但是没有一个测试用例，感觉有点茫然（可能是我比较笨～</div>2021-10-23</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIicr82CnrdEjibibAvyeKRQHszSzIAqoCWxN0kqC442XcjEae6S9j6NDtKLpg4Da4CUQQeUFUicWqiaDw/132" width="30px"><span>有学识的兔子</span> 👍（0） 💬（3）<div>谁能解释下这是js的什么写法？

var TokenKind;
(function (TokenKind) {
    TokenKind[TokenKind[&quot;Keyword&quot;] = 0] = &quot;Keyword&quot;;
    TokenKind[TokenKind[&quot;Identifier&quot;] = 1] = &quot;Identifier&quot;;
    TokenKind[TokenKind[&quot;StringLiteral&quot;] = 2] = &quot;StringLiteral&quot;;
    TokenKind[TokenKind[&quot;Seperator&quot;] = 3] = &quot;Seperator&quot;;
    TokenKind[TokenKind[&quot;Operator&quot;] = 4] = &quot;Operator&quot;;
    TokenKind[TokenKind[&quot;EOF&quot;] = 5] = &quot;EOF&quot;;
})(TokenKind || (TokenKind = {}));
;</div>2021-08-14</li><br/>
</ul>