你好，我是涂伟忠。在上一讲中，我们已经学习了正则中和一些元字符相关的内容。这一节我们讲一下正则中的三种模式，贪婪匹配、非贪婪匹配和独占模式。

这些模式会改变正则中量词的匹配行为，比如匹配一到多次；在匹配的时候，匹配长度是尽可能长还是要尽可能短呢？如果不知道贪婪和非贪婪匹配模式，我们写的正则很可能是错误的，这样匹配就达不到期望的效果了。

## 为什么会有贪婪与非贪婪模式？

由于本节内容和量词相关的元字符密切相关，所以我们先来回顾一下正则中表示量词的元字符。

![](https://static001.geekbang.org/resource/image/2b/c3/2b03098dcc203c648a40f89a0ba77fc3.png?wh=1626%2A950)

在这6种元字符中，我们可以用 {m,n} 来表示 （\*）（+）（?） 这3种元字符：

![](https://static001.geekbang.org/resource/image/38/74/38ceb28add7794fe9ed069e08fb1b374.jpg?wh=1285%2A569)

表示量词的星号（\*）和 加号（+）可能没你想象的那么简单，我用一个例子给你讲解一下。我们先看一下加号（+），使用 a+ 在 aaabb 中查找，可以看到只有一个输出结果：

![](https://static001.geekbang.org/resource/image/2b/08/2b3e3f549e69fdd398c15d6b0bd44e08.png?wh=1038%2A590)

对应的Python代码如下：

```
>>> import re
>>> re.findall(r'a+', 'aaabb')
['aaa']

```

加号应该很容易理解，我们再使用 a* 在 aaabb 这个字符串中进行查找，这次我们看到可以找到4个匹配结果。

![](https://static001.geekbang.org/resource/image/b0/4c/b0c582cbf8ec081bc798296b5471804c.png?wh=1032%2A614)

使用Python示例如下，我们可以看到输出结果，也是得到了4个匹配结果：

```
>>> import re
>>> re.findall(r'a*', 'aaabb')
['aaa', '', '', '']

```

但这一次的结果匹配到了三次空字符串。为什么会匹配到空字符串呢？因为星号（\*）代表0到多次，匹配0次就是空字符串。到这里，你可能会有疑问，如果这样，aaa 部分应该也有空字符串，为什么没匹配上呢？
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1c/fa/4f/4252911a.jpg" width="30px"><span>Geek.S.</span> 👍（46） 💬（9）<div>以前只知道贪婪模式和懒惰模式，原来还有一个独占模式，贪婪和非贪婪都会发生回溯，结合文中给的案例链接，知道了 NFA 和 DFA (这个老师应该在后面讲匹配原理时会讲到)。难怪余晟老师说学会正则后务必要学会克制。

如果只是判断文本是否符合规则，则可以使用独占模式; 如果需要获取匹配的结果，则根据需要使用贪婪或非贪婪。

作业题: (这里需要获取单词，不能使用独占模式)

\w+|“[^”]+”  (注意: 例句中的双引号是中文状态下的)

结果(10 次匹配, 48 步): [&#39;we&#39;, &#39;found&#39;, &#39;&quot;the little cat&quot;&#39;, &#39;is&#39;, &#39;in&#39;, &#39;the&#39;, &#39;hat&#39;, &#39;we&#39;, &#39;like&#39;, &#39;&quot;the little cat&quot;&#39;]


相应的 Python 代码:

&gt;&gt;&gt; import re
&gt;&gt;&gt; text = &#39;&#39;&#39;we found “the little cat” is in the hat, we like “the little cat”&#39;&#39;&#39;  # 注意: 例句中的双引号是中文状态下的
&gt;&gt;&gt; pattern = re.compile(r&#39;&#39;&#39;\w+|“[^”]+”&#39;&#39;&#39;)
&gt;&gt;&gt; pattern.findall(text)
[&#39;we&#39;, &#39;found&#39;, &#39;&quot;the little cat&quot;&#39;, &#39;is&#39;, &#39;in&#39;, &#39;the&#39;, &#39;hat&#39;, &#39;we&#39;, &#39;like&#39;, &#39;&quot;the little cat&quot;&#39;]


示例: https:&#47;&#47;regex101.com&#47;r&#47;l8hkqi&#47;1</div>2020-06-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（17） 💬（5）<div>老师，对于文中的这个语句
regex.findall(r&#39;xy{1,3}+z&#39;, &#39;xyyz&#39;)

这里是独占模式，不进行回溯。这里在尽可能多的匹配第三个 y的时候匹配失败，不应该是直接匹配失败 返回空数组吗？ 怎么是返回 xyyz 呢？ 如果返回 xyyz 不就进行回溯了吗？</div>2020-06-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/fa/f9/8fdde936.jpg" width="30px"><span>BillionY</span> 👍（13） 💬（6）<div>\w+|“[^”]*”   
\w+|“[\w\s]+?
\w+|“.+?”
还有第四种方法吗?</div>2020-06-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1a/66/2d9db9ed.jpg" width="30px"><span>苦行僧</span> 👍（7） 💬（3）<div>w+|“[^”]+”, w+ 看懂了, 但 后面的没看懂?</div>2020-08-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f1/15/8fcf8038.jpg" width="30px"><span>William</span> 👍（5） 💬（1）<div>js版
```javascript
let str = `we found &quot;the little cat&quot; is in the hat, we like &quot;the little cat&quot;`
let re = new RegExp(&#47;&quot;[^&quot;]+&quot;|\w+&#47;, &#39;g&#39;)
let res = str.match(re)
console.log(res)
```</div>2020-06-23</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/ibZVAmmdAibBeVpUjzwId8ibgRzNk7fkuR5pgVicB5mFSjjmt2eNadlykVLKCyGA0GxGffbhqLsHnhDRgyzxcKUhjg/132" width="30px"><span>pyhhou</span> 👍（5） 💬（1）<div>思考题：

&quot;.+?&quot;|[^\s|,]+

关于回溯，是不是就是递归调用函数栈的原理？拿 xy{1,3}z 匹配 xyyz 举例，步骤如下：

1. 正则中的 x 入栈，匹配上 text 的第一个字符 x
2. 正则中的 y 入栈，匹配上 text 中的第二个字符 y
3. 因为这里没有加问号，属于贪婪匹配，正则中的 y 继续入栈，匹配上 text 中的第三个字符 y
4. 正则中的 y 继续入栈，但是这个时候 y 和 z 不匹配，执行回溯，就是当前正则的第三个 y 出栈
5. 用范围量词后的字符 z 继续入栈匹配，匹配上 text 的最后一个字符，完成匹配</div>2020-06-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/07/21/b3394aa2.jpg" width="30px"><span>Robot</span> 👍（4） 💬（1）<div>建议老师统一下正则的运行环境。</div>2020-06-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/71/96/66ad1cd2.jpg" width="30px"><span>飞</span> 👍（3） 💬（2）<div>[a-z]+|“[^“]+”</div>2020-06-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/db/64/06d54a80.jpg" width="30px"><span>中年男子</span> 👍（3） 💬（1）<div>还有就是文章中的例子： xy{1,3}+yz 去匹配 xyyz，我的理解是用y{1,3}尽可能多的去匹配， 也就是 xyy之后，用第三个y 去匹配z，因为不回溯，到这里就失败了， 还没到正则中z前面那个y。
还请解惑。</div>2020-06-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/a6/d4/8d50d502.jpg" width="30px"><span>简简单单</span> 👍（2） 💬（3）<div>老师我有个疑问求解答: 

正则: \w+|“.+?”
字符串 : we found “the little cat” is in the hat, we like “the little cat”

结果的确是把每个单词单独匹配到了, 并且 引号的也当成一个单词了,
那么请问 为什么 \w+ 不会把 引号内的单词匹配到呢, 为什么不会出现 the 与 “the little cat” 共存呢
正则匹配的过程是怎么样的 ?
</div>2020-07-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c4/06/c08eca4c.jpg" width="30px"><span>Zion W.</span> 👍（2） 💬（1）<div>引号是全角还是半角？</div>2020-06-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/33/07/8f351609.jpg" width="30px"><span>JustDoDT</span> 👍（2） 💬（1）<div>我总结一些，正则这东西：
1、掌握基本规则
2、多用，多试验
我的运行环境：MacOS，python 3.6.2
我匹配的英文引号 &quot; 例子
text = &#39;we found &quot;the little cat&quot; is in the hat, we like &quot;the little cat&quot;&#39;
re.findall(r&#39;&quot;(.*?)&quot;&#39;, text)
输出：[&#39;the little cat&#39;, &#39;the little cat&#39;]
中文引号版本 “ ”
text = &#39;we found “the little cat” is in the hat, we like “the little cat”&#39;
re.findall(r&#39;“(.*?)”&#39;, text)
输出：[&#39;the little cat&#39;, &#39;the little cat&#39;]
so easy</div>2020-06-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/db/64/06d54a80.jpg" width="30px"><span>中年男子</span> 👍（2） 💬（2）<div>老师， 我有个问题， 既然是独占模式了， 那{1,3} 这种量词是不是就没什么意义？直接{3}不就行了</div>2020-06-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/83/28/ee3d71cc.jpg" width="30px"><span>蓝猫冬天变肥猫</span> 👍（1） 💬（1）<div>老师，
[a-zA-Z]+|“.+? 匹配出来10个
”但是为什么我用.+|“.+?”把整个句子都匹配上了呢？</div>2021-07-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/c9/23/76511858.jpg" width="30px"><span>洛奇</span> 👍（1） 💬（1）<div>本人仅看这篇文章后，还是不明白为什么“匹配越南店铺名”的例子会有回溯？从正则表达式xy*yz匹配xyz的例子可以大概明白什么是回溯，但是匹配店铺名的例子中，两个符合条件的组合是“或”的关系，而不是xy*yz里的y*和y的前后关系，而且正则头尾已经用^和$包裹了，为什么也会产生回溯呢？</div>2020-07-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/bd/ec/cc7abf0b.jpg" width="30px"><span>L</span> 👍（1） 💬（4）<div>老师我完全没有办法理解这个空白符。
确实将 aaabb 拆成了 空白符+a+空白符+...
可以理解 但是这样做的意义是什么？？？ 
此外 我想问一下对于同一个正则表达式 不同的语言引擎的解释是可以不一样的吗？
一样用这个进行举例。
const regex1 = new RegExp(&#39;a*?&#39;,&#39;g&#39;)
const str1 = &#39;aaabb&#39;
console.log(str1.match(regex1))  &#47;&#47; [&#39;&#39;,&#39;&#39;,&#39;&#39;,&#39;&#39;,&#39;&#39;,&#39;&#39;,&#39;&#39;]

预期的结果不是 a a a b b 吗？
而对于这个结果我做了一个尝试性的解读。
macth返回的不是字符串的子串，而是正则的结果
因此 返回的结果应该为 &#39;&#39;  a aa a*
因此即使是a匹配到了 返回的也是对应的正则的匹配形式 空字符 因为非贪婪模式下并不需要到a就可以返回了
可是这样得话 为什么会多出来一个 空白符 呢？
对于这个空白符 个人的理解是 当输出一个空字符的时候 a* 也是可以匹配成功的，因此需要对这种情况进行处理，那么是在什么时候进行处理的呢？在一开始的时候进行处理的，还是在结尾的时候进行处理的？
老师在讲原理的时候会聊这块吗？
我的问题主要有三点

1、不同的语言对正则的理解是不是可能不一样
2、为什么python要对字符串进行加上空字符的处理
3、为什么JavaScript的match会返回这样的结果

希望老师能给一个解答

还有一个请求
老师在在讲原理的时候，能不能提一下这块</div>2020-06-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/07/21/b3394aa2.jpg" width="30px"><span>Robot</span> 👍（1） 💬（1）<div>课后思考：

&#47;&quot;[^&quot;]+&quot;|[a-z]+&#47;g</div>2020-06-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/10/30/c07d419c.jpg" width="30px"><span>卡尔</span> 👍（1） 💬（1）<div>^([a-zA-Z]+|&quot;[^&quot;]+&quot;)$</div>2020-06-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/fa/4f/4252911a.jpg" width="30px"><span>Geek.S.</span> 👍（1） 💬（1）<div>独占模式是贪婪的，很好奇有没有非贪婪的独占模式？老师可不可以分析一下这个问题？👻</div>2020-06-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/78/62/354b1873.jpg" width="30px"><span>clever_P</span> 👍（1） 💬（1）<div>[a-zA-Z]+|&quot;[a-zA-Z ]+&quot;</div>2020-06-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/90/19/b3403815.jpg" width="30px"><span>Juha</span> 👍（0） 💬（1）<div>老师，这里想请问一下，为什么 aaabb 中使用正则 a* 匹配的结果中，会有3个空字符串，看上去不应该是2个吗，分别是bb来匹配a未匹配到导致的</div>2024-06-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/20/c8/b16eb6ed.jpg" width="30px"><span>程同学</span> 👍（0） 💬（2）<div>老师好，这篇文章我看了很多遍，发现在贪婪模式下的“尽可能多地匹配”，与独占模式下的“尽可能多地匹配”是不一样的，是这样吗</div>2022-03-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/c9/23/76511858.jpg" width="30px"><span>洛奇</span> 👍（0） 💬（1）<div>老师，用&quot;[^&quot;]*?&quot;是否比&quot;.*?&quot;性能更好？因为我认为前者已经先用引号和相应字符比较过了，直觉告诉我前者可能性能更好。</div>2022-01-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/30/67/a1e9aaba.jpg" width="30px"><span>Roway</span> 👍（0） 💬（1）<div>xy{1,3}+yz    改成独占模式 xy{3}yz 不可以吗？</div>2021-12-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/b8/24/039f84a2.jpg" width="30px"><span>咱是吓大的</span> 👍（0） 💬（1）<div>贪婪模式是从多到少进行匹配，非贪婪模式是从少到多进行匹配，如果匹配不成功则回溯
独占模式从多到少进行匹配，且只匹配一次
老师我这么理解对吗？</div>2021-11-11</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/VoOP42bmOhmfaHfacAQc7EesLcmXu2OrEHsQJic1xYPT7elyIIQy6jDBVUtianXcA2ibFQhYj6OUwhYPDkKqQSIaA/132" width="30px"><span>Geek_8hym02</span> 👍（0） 💬（1）<div>作业练习搞了半天终于弄出来了，“(.+?)”|[a-z]{2,}+</div>2021-09-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/db/3a/a9113de0.jpg" width="30px"><span>向死而生</span> 👍（0） 💬（1）<div>a?是贪婪模式还是非贪婪模式</div>2021-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/db/3a/a9113de0.jpg" width="30px"><span>向死而生</span> 👍（0） 💬（1）<div>非贪婪匹配的最后一个例题没懂，”不是也能被.给匹配吗，为什么非贪婪模式下不匹配？</div>2021-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/d7/a9/f341b89c.jpg" width="30px"><span>azurepwq</span> 👍（0） 💬（1）<div>老师，我想了好久，文章来回看了好多遍也不知怎么解决，又不想跳出文章的学习去查资料，毕竟是作业。思考了半小时后，我被自己蠢哭了，我以为要匹配&quot;xxx&quot;里面的xxx, 原来只要匹配&quot;xxx&quot;就可以了。
于是答案不是很明显是: \w+|&quot;[^&quot;]+&quot;。但问题来了，如果我想单独匹配&quot;xxx&quot;里面的xxx怎么办呢？</div>2020-11-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/44/a4/7a45d979.jpg" width="30px"><span>IT蜗壳-Tango</span> 👍（0） 💬（1）<div>打卡学习，每天学习一点点。加油＾０＾~</div>2020-11-11</li><br/>
</ul>