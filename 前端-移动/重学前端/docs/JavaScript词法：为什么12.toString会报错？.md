你好，我是winter。

在前面的文章中，我们已经从运行时的角度了解过JavaScript的知识内容，在接下来的几节课，我们来了解一下JavaScript的文法部分。

文法是编译原理中对语言的写法的一种规定，一般来说，文法分成词法和语法两种。

词法规定了语言的最小语义单元：token，可以翻译成“标记”或者“词”，在我的专栏文章中，我统一把token翻译成词。

从字符到词的整个过程是没有结构的，只要符合词的规则，就构成词，一般来说，词法设计不会包含冲突。词法分析技术上可以使用状态机或者正则表达式来进行，我们的课程主要是学习词法，关于它们实现的细节就不多谈了。

## 概述

我们先来看一看JavaScript的词法定义。JavaScript源代码中的输入可以这样分类：

- WhiteSpace 空白字符
- LineTerminator 换行符
- Comment 注释
- Token 词
  
  - IdentifierName 标识符名称，典型案例是我们使用的变量名，注意这里关键字也包含在内了。
  - Punctuator 符号，我们使用的运算符和大括号等符号。
  - NumericLiteral 数字直接量，就是我们写的数字。
  - StringLiteral 字符串直接量，就是我们用单引号或者双引号引起来的直接量。
  - Template 字符串模板，用反引号`` ` `` 括起来的直接量。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/16/55/4d/66acf5a3.jpg" width="30px"><span>Nandy</span> 👍（11） 💬（4）<div>十进制的number的小数点前后的内容可以省略，但是不能同时省略
        .01 = 0.01    10. = 10
12.toString() 12.被当做了一个整体，所以会报错， 
加入空格 12 .toString() 这样.就成为了一个单独的token

嘻嘻~请winter老师表扬我学的认真(#^.^#)</div>2019-07-25</li><br/><li><img src="" width="30px"><span>lsy</span> 👍（11） 💬（2）<div>&#39;敏\u200d感词&#39;.length === 4 &#47;&#47; true</div>2019-07-10</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJZO3Xkicd9Cy76GXln7hRGda3NBEjibEdQUXqj4MbukxqVqRKAlSxe7hApUTibCGJ6wQq6VjCKBur0w/132" width="30px"><span>大海</span> 👍（1） 💬（10）<div>为什么parseInt(12).toString()就不会报错呢，parseInt(12)返回的不也是一个数值吗</div>2019-06-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/f8/d0/ecc68a4f.jpg" width="30px"><span>🐻🔫🐸</span> 👍（54） 💬（1）<div>为啥不支持直接回复呢？

这里讨论一下@Snow同学的问题 别忘了JS是允许直接写小数的，也就说12.toString() 他无法分辨你是想要创建一个小数位为toString()的数 还是创建一个12 然后调用toString()这种情况。也就说 JS里面的. 是拥有两种含义的 一种是小数点 一种是方法调用。 你可以试试12..toString() 这样就可以消除这种歧义</div>2019-03-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/51/f3/f1c3ea02.jpg" width="30px"><span>曾侃</span> 👍（43） 💬（2）<div>之前没有接触过零宽字符，学完这节课后网上搜了下零宽字符的应用，看到了这篇文章《[翻译]小心你复制的内容：使用零宽字符将用户名不可见的插入文本中》，受益匪浅。自己用这个思路实现了一样的给字符串添加水印的功能。
代码地址：https:&#47;&#47;github.com&#47;zengkan0703&#47;text-watermark，有不对的地方请同学们指正。</div>2019-04-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/13/3e/f350a41b.jpg" width="30px"><span>田野的嘴好冰</span> 👍（42） 💬（2）<div>零宽空格
var a = &#39;\uFEFF&#39;,b = &#39;b&#39;, c = &#39;c&#39;, d = (b+a+c);
console.log(d); &#47;&#47;bc
console.log(d.length); &#47;&#47;3
console.log(d.indexOf(a)); &#47;&#47;1</div>2019-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/b8/d1/5a216db5.jpg" width="30px"><span>是零壹呀</span> 👍（20） 💬（0）<div>12.toString() 会被解析成 12.（数字字面量） 和 toString()。
所以正常的写法是12..toString()才是正常的</div>2019-04-24</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q3auHgzwzM5zYwcmyicWJYl9ztB5picuicoXKjgial4oU4TRggOLHg3TWoGjVTMxSCKdEDCYIv9HNua8CdXY0gRxXA/132" width="30px"><span>王益</span> 👍（15） 💬（1）<div>(12).toString()也可以</div>2020-03-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/26/22/dd505e6d.jpg" width="30px"><span>Yully</span> 👍（12） 💬（0）<div>原来零宽空格和零宽连接符、零宽非连接符还有妙用， 隐形水印、加密信息分享和逃脱关键词匹配。</div>2020-05-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/8e/7f/4ff4472f.jpg" width="30px"><span>CaveShao</span> 👍（5） 💬（0）<div>js 中 . 有两种含义，一种是代表一个小数，一种是调用方法。12.toString() 中的 12. 会被浏览器解析为一个省略了小数后面部分的数字。一个数字后面直接写一个方法，就像 333toString 一样，肯定会报错。
Invalid or unexpected token</div>2019-05-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/78/51/4790e13e.jpg" width="30px"><span>Smallfly</span> 👍（4） 💬（1）<div>${} 的括号中完全可以出现 } 符号呀，老师你别骗人哦。

`${function(){console.log(1)}}`

 输出：

&quot;function(){console.log(1)}&quot;
</div>2019-10-17</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/s0bx4WXQNkAJ3c3map0g6dlt3sKDgTtN7Ria96YoufjQcVVI8Shv5CN1jnK1ZTImNnlPcibRqvyiaUuhpIvV1TpnQ/132" width="30px"><span>wingsico</span> 👍（3） 💬（0）<div>全文大概阐述了js中的词法分析中得到的不同类型的token，以及针对js语言特性的一些特殊token（需要根据语法分析来回传递标志来判断具体如何分词），也说了一些零宽空白符号等。但感觉实际使用时，这方面属于比较偏的方面了，但有助于我们去理解编译原理中的词法分析和一些特殊处理，以及对一些特殊场景的错误可以知其原因。</div>2020-04-13</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqYLIk6CAiaQQN9NVQUFuWyMz5ZsEvLcbWgibXSBXPiaYrqpggVgIRHMtoa8qCmoe4oSvico6sriaT4iaMg/132" width="30px"><span>Geek_666</span> 👍（3） 💬（1）<div>文中的&lt;ZWNBSP&gt;(旧称&lt;BOM&gt;) 字符 BOM的全称应该是&quot;byte-order mark&quot;而不是 &quot;bit order mark”吧</div>2020-03-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/04/4b/e639ce42.jpg" width="30px"><span>商志远🤪</span> 👍（3） 💬（1）<div>【理论上，“ ${ } ”内部可以放任何 JavaScript 表达式代码，而这些代码是以“ } ” 结尾的，也就是说，这部分词法不允许出现“ } ”运算符。】
这段话没理解</div>2019-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/89/2c/10febc6c.jpg" width="30px"><span>起风了</span> 👍（1） 💬（0）<div>零宽空格（zero-width space, ZWSP）用于可能需要换行处。
    Unicode: U+200B  HTML: &amp;#8203;
零宽不连字 (zero-width non-joiner，ZWNJ)放在电子文本的两个字符之间，抑制本来会发生的连字，而是以这两个字符原本的字形来绘制。
    Unicode: U+200C  HTML: &amp;#8204;
零宽连字（zero-width joiner，ZWJ）是一个控制字符，放在某些需要复杂排版语言（如阿拉伯语、印地语）的两个字符之间，使得这两个本不会发生连字的字符产生了连字效果。
    Unicode: U+200D  HTML: &amp;#8205;
左至右符号（Left-to-right mark，LRM）是一种控制字符，用于计算机的双向文稿排版中。
    Unicode: U+200E  HTML: &amp;lrm; &amp;#x200E; 或&amp;#8206;
右至左符号（Right-to-left mark，RLM）是一种控制字符，用于计算机的双向文稿排版中。
    Unicode: U+200F  HTML: &amp;rlm; &amp;#x200F; 或&amp;#8207;
字节顺序标记（byte-order mark，BOM）常被用来当做标示文件是以UTF-8、UTF-16或UTF-32编码的标记。
    Unicode: U+FEFF</div>2021-05-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/54/0a/9a002ad5.jpg" width="30px"><span>Adam Lau</span> 👍（1） 💬（0）<div>InputElementRegExpOrTemplateTail这玩意相关的四种情况相当不理解，为啥要组合4种情况，两个不相关的事情，词法解析该调用谁就调用谁，有冲突不是语法解析会告诉词法是哪种情况吗，既然告诉了调对应的解析方法就好了，为啥组合出4种情况？</div>2021-02-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/a0/1c/385a4983.jpg" width="30px"><span>oxygen</span> 👍（1） 💬（0）<div>零宽空格&amp;#8203我遇到的就是自己从头写的HTML页面在浏览器显示出来总是会带这玩意</div>2020-06-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/0e/ea/16291abc.jpg" width="30px"><span>better man</span> 👍（1） 💬（3）<div>转义字符&#39;  产生字符为&quot;是什么意思？？？没看懂，有没有理解的人举个例子解惑下</div>2019-08-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（1） 💬（1）<div>@商志远🤪
你可以尝试一下在控制台输入：`test } ${}`  看看会发生什么？

Uncaught SyntaxError: Unexpected token }</div>2019-03-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（1） 💬（0）<div>正则表达式冲突，这时候对词法分析来说，其实是没有办法处理的，所以 JavaScript 的解决方案是定义两组词法，然后靠语法分析传一个标志给词法分析器，让它来决定使用哪一套词法。

对于这句活我有个疑问，不是先进行词法分析，然后在进行语法分析吗？

难道这里是词法分析分析出来两种，然后在语法分析的选择其中的一种？？？？？</div>2019-03-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/9f/86/f733e828.jpg" width="30px"><span>Lee Chen</span> 👍（0） 💬（0）<div>零宽空格、零宽连接符和零宽非连接符是 Unicode 字符，它们在视觉上是不可见的，但在计算机处理文本时会有特殊的作用。这些字符可以用来做一些有趣的事情，比如在文本中隐藏信息。

下面是一个简单的例子，我们使用零宽空格和零宽非连接符来编码二进制信息：

```javascript
function encodeBinaryToZeroWidthChars(binary) {
    return binary.replace(&#47;0&#47;g, &#39;\u200B&#39;).replace(&#47;1&#47;g, &#39;\u200C&#39;);
}

function decodeZeroWidthCharsToBinary(zeroWidthStr) {
    return zeroWidthStr.replace(&#47;\u200B&#47;g, &#39;0&#39;).replace(&#47;\u200C&#47;g, &#39;1&#39;);
}

&#47;&#47; 使用示例
let secretMessage = &#39;Hello, world!&#39;;
let binaryMessage = secretMessage.split(&#39;&#39;).map(char =&gt; char.charCodeAt(0).toString(2)).join(&#39; &#39;);
let encodedMessage = encodeBinaryToZeroWidthChars(binaryMessage);

console.log(&#39;Encoded message:&#39;, encodedMessage);

let decodedBinary = decodeZeroWidthCharsToBinary(encodedMessage);
let decodedMessage = decodedBinary.split(&#39; &#39;).map(binary =&gt; String.fromCharCode(parseInt(binary, 2))).join(&#39;&#39;);

console.log(&#39;Decoded message:&#39;, decodedMessage);
```

这段代码首先将一个字符串转换为二进制表示，然后使用零宽空格代替二进制中的 &quot;0&quot;，使用零宽非连接符代替 &quot;1&quot;。解码时，我们只需要做相反的操作即可。

这种方法可以用来在文本中隐藏信息，因为零宽字符在视觉上是不可见的，所以隐藏的信息不会影响正常的文本阅读。</div>2023-08-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/3c/88/6bef27d6.jpg" width="30px"><span>大神博士</span> 👍（0） 💬（0）<div>往后多看一位不行吗？</div>2023-05-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/5e/d6/87189c9d.jpg" width="30px"><span>shark</span> 👍（0） 💬（0）<div>老师，请教个问题，词法分析阶段不是直接解析代码生成token吗？至于token是否符合语法规范，符合那种语法不是在在语法分析阶段通过语法产生式来判断吗？js为什么要使用多套词法呢？像文章中说的除法和正则的冲突，两者在语法上还是有比较大的区别，为什么不在语法阶段去识别而是在词法阶段去识别？</div>2021-06-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e3/6c/b51e0234.jpg" width="30px"><span>blank</span> 👍（0） 💬（0）<div>转义字符是 &#39;，为什么产生字符是 &quot;</div>2021-03-11</li><br/><li><img src="" width="30px"><span>Geek_a55251</span> 👍（0） 💬（0）<div>12.toString() 会把 12. 解析成一个整体 12 .toString() 会把12解析成一个整体
然后按道理可以12..toString() 就可以输出&quot;12&quot;了</div>2020-04-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/77/9b/c18f4047.jpg" width="30px"><span>Geek_8rfqh9</span> 👍（0） 💬（0）<div>零宽空格和零宽连接符、零宽非连接符...感觉打开了新世界的大门。。。。</div>2020-01-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/8f/8d/5b82d3f7.jpg" width="30px"><span>小细胞</span> 👍（0） 💬（0）<div>查到了一篇文章是用零宽空格，零宽非连接符和零宽连接符来抓信息泄露源头的</div>2019-12-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/c5/2b/85b9048c.jpg" width="30px"><span>小飒</span> 👍（0） 💬（0）<div>打卡</div>2019-08-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/eb/98/a0269f25.jpg" width="30px"><span>伍二娃</span> 👍（0） 💬（0）<div>function f(){
    console.log(arguments);
}

var a = &quot;world&quot;
f`Hello ${a}!`; &#47;&#47; [[&quot;Hello &quot;, &quot;!&quot;], &quot;world&quot;]
</div>2019-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c0/99/259a412f.jpg" width="30px"><span>Geeker</span> 👍（0） 💬（0）<div>@Snow同學 
--------------------------------
只有我看完，还是不知道12.toString()为什么会报错嘛？
--------------------------------

我的理解是，12.toString() 前面的“12.”（注意有点）对于引擎来讲是有歧义的，这到底是代表浮点数，还是代表要转为数字的包装对象，然后调用 toString 方法呢？引擎默认代表是浮点数，这个时候如果要调用 toString 方法，需要再加一个点，像这样：12..toString()。
顺便说一句，中文也有很多歧义呢。</div>2019-04-14</li><br/>
</ul>