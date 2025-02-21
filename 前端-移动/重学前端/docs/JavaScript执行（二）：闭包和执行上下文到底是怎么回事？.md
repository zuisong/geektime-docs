你好，我是winter。

在上一课，我们了解了JavaScript执行中最粗粒度的任务：传给引擎执行的代码段。并且，我们还根据“由JavaScript引擎发起”还是“由宿主发起”，分成了宏观任务和微观任务，接下来我们继续去看一看更细的执行粒度。

一段JavaScript代码可能会包含函数调用的相关内容，从今天开始，我们就用两节课的时间来了解一下函数的执行。

我们今天要讲的知识在网上有不同的名字，比较常见的可能有：

- 闭包；
- 作用域链；
- 执行上下文；
- this值。

实际上，尽管它们是表示不同的意思的术语，所指向的几乎是同一部分知识，那就是函数执行过程相关的知识。我们可以简单看一下图。

![](https://static001.geekbang.org/resource/image/68/52/68f50c00d475a7d6d8c7eef6a91b2152.png?wh=745%2A481)

看着也许会有点晕，别着急，我会和你共同理一下它们之间的关系。

当然，除了让你理解函数执行过程的知识，理清这些概念也非常重要。所以我们先来讲讲这个有点复杂的概念：闭包。

## 闭包

闭包翻译自英文单词closure，这是个不太好翻译的词，在计算机领域，它就有三个完全不相同的意义：编译原理中，它是处理语法产生式的一个步骤；计算几何中，它表示包裹平面点集的凸多边形（翻译作凸包）；而在编程语言领域，它表示一种函数。

闭包这个概念第一次出现在1964年的《The Computer Journal》上，由P. J. Landin在《The mechanical evaluation of expressions》一文中提出了applicative expression和closure的概念。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/15/19/2b/6337e969.jpg" width="30px"><span>麦哲伦</span> 👍（32） 💬（12）<div>老师能解释下这个么？
var b = 10;
(function b(){
b = 20;
console.log(b); &#47;&#47; [Function: b]
})();</div>2019-02-27</li><br/><li><img src="" width="30px"><span>Geek_f51da4</span> 👍（7） 💬（9）<div>老师，闭包我是这样理解的，函数里边的函数，这样的理解对吗</div>2019-06-12</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/lIN14g64kVO1Y8AC5hpKOrpTQiagL9O3zqbgmdDWO8V6FSOZd7ZhqH0v4AQHLy4OWjvMcP2WnUmt7AHzo4cHsLQ/132" width="30px"><span>张祥儒</span> 👍（7） 💬（2）<div>winter大大，我觉得应该用global object，和active object 来解释这个闭包，作用域，执行器上下文。</div>2019-02-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b7/97/1f792153.jpg" width="30px"><span>beilunyang</span> 👍（4） 💬（1）<div>闭包其实是一个绑定了执行环境的函数。
var foo = &#39;foo&#39;;
function printFoo() {
    console.log(foo);
}
printFoo();

所以printFoo这个函数是一个闭包，对吗</div>2019-10-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/6f/10/bfbf81dc.jpg" width="30px"><span>海绵薇薇</span> 👍（1） 💬（1）<div>老师您好，对于 --- JavaScript 中跟闭包对应的概念就是“函数” 这句话我还是理解不够。
说是闭包和执行上下文没关系，但是词法作用域，不就和执行上下文相关吗？用到的标识符在作用域链上，作用域链不是在执行上下文里吗？</div>2019-09-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/dc/08/64f5ab52.jpg" width="30px"><span>陈斌</span> 👍（1） 💬（1）<div>我查看另一篇博客资料：
执行上下文同时包含变量环境组件（VariableEnvironment）和词法环境组件（LexicalEnvironment），这两个组件多数情况下都指向相同的词法环境（Lexical Environment）。
一般情况下一个执行上下文内的Variable Environment和Lexical Environment指向同一个词法环境，之所以要区分两个组件，主要是为了实现块级作用域的同时不影响var声明及函数声明。
和老师您如下介绍的是否有点冲突？
lexical environment：词法环境，当获取变量或者 this 值时使用。
variable environment：变量环境，当声明变量时使用。
我觉得我看了上面的博客之后，理解不了您的意思了？</div>2019-08-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e2/eb/a11560a8.jpg" width="30px"><span>J</span> 👍（0） 💬（1）<div>小白有点懵逼，老师可以解答下几个问题吗

&gt; 
var 把 b 声明到哪里；
b 表示哪个变量；
b 的原型是哪个对象；
let 把 c 声明到哪里；
this 指向哪个对象。

&gt; var b = {} 这样一句对两个域产生了作用
? 两个域是指哪两个

&gt; 分析了一些执行上下文中所需要的信息，并从var、let、对象字面量等语法中，推导出了词法作用域、变量作用域、Realm的设计。
? 执行上下文需要的信息是哪些
? 在哪里推导了，两个作用域在哪里</div>2019-10-30</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKS4a1IwJOrnOGqCVAQSPWQeW6KTAPPGichBa53tyD3aJ3MmMIq8oueVSFLlkSTp2MHStseAkCDtBw/132" width="30px"><span>泡泡</span> 👍（0） 💬（1）<div>老师，已经读了十几篇了，感觉知识讲的太深，专业词汇较多，读起来比较生涩</div>2019-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/32/45/3ac375a1.jpg" width="30px"><span>追梦</span> 👍（0） 💬（1）<div>请问老师，这个例子，是如何得出“可以看到，在 Global function with 三个环境中，b 的值都不一样”这个结论的？
var b;
void function(){
    var env = {b:1};
    b = 1;
    console.log(&quot;In function b:&quot;, b);
    with(env) {
        var b = 1;
        console.log(&quot;In with b:&quot;, b);
    }
}();
console.log(&quot;Global b:&quot;, b);
</div>2019-02-28</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/eEBwOT9gbj3gRtD79LsFQUW0F0Pph3m3RoW0QL5O9fXogicG8xicciaj6qcpvbhwv3iapWe0R7iazDugMzK61v2GNNg/132" width="30px"><span>Geek_56013e</span> 👍（300） 💬（3）<div>老师您的专业知识太强了，文中包含很多专业术语，在介绍某专业术语时带上了其他专业术语，而这些带上的专业术语部分在网上搜也是解释不清，导致很多地方看不懂、看起来比较费劲、只能猜测大意。比如对于「realm」的描述，只提了中文意思是“国度”“领域”“范围”和“包含一组完整的内置对象，而且是复制关系”，看完文章后，在js领域还是不清楚具体「realm」是什么含义，只能大概猜测。希望老师后续文章如果解释某专业术语时带上的其他专业术语时，能以日常常见代码为例解释。</div>2019-02-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/39/ab/42622d70.jpg" width="30px"><span>James Bond</span> 👍（183） 💬（24）<div>说了半天闭包是什么呢？跟普通函数有什么区别呢！</div>2019-03-12</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/s0bx4WXQNkAJ3c3map0g6dlt3sKDgTtN7Ria96YoufjQcVVI8Shv5CN1jnK1ZTImNnlPcibRqvyiaUuhpIvV1TpnQ/132" width="30px"><span>wingsico</span> 👍（59） 💬（2）<div>在JS中，函数其实就是闭包，不管该函数内部是否使用外部变量，它都是一个闭包。如闭包定义的那样，由环境和表达式组成，作为js函数，环境为词法环境，而表达式就是函数本身。而词法环境是执行上下文的一部分，执行上下文包括 this 绑定, 词法环境和变量环境。词法环境是随着执行上下文一起创建的，在函数&#47;脚本&#47;eval执行时创建。

理解闭包，首先需要理解闭包是什么类型的东西，闭包实际上指的是函数，搞清楚问题的对象究竟是谁，而很多人会把环境&#47;作用域等其他的东西当做闭包，是对闭包的概念类型的错误理解。那么知道了闭包是函数，那么闭包应该是什么样的函数呢？也就是含有环境的函数，很明显，在js中，任何一个函数都有着自己的环境，这个环境让我们可以去找到定义的变量内部的this、外部作用域。

很多人认为，要让一个函数能去访问某个应该被回收的内存空间，但由于函数存在对该内存空间的变量的引用而不可回收，这样才形成了闭包。那么试问一下，这里你到底是把这个内存空间当做闭包呢？还是引用这块内存空间的函数当闭包呢？假如是前者，则和把环境当闭包的人犯了同样的错误，假如是后者，现在的这个函数实际上和你定义的普通函数本质上没有区别，都含有自己的环境，只不过这个函数的环境多了一些，但本质没有区别。理解了这点，你才能从上面的错误理解中解脱出来。</div>2020-04-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/2b/d6/945f0d82.jpg" width="30px"><span>_(:з」∠)_</span> 👍（40） 💬（7）<div>let 和 var 都不好用，98%的情况都是用 const</div>2019-04-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/16/06/cffd605d.jpg" width="30px"><span>水瓶瓶盖盖</span> 👍（26） 💬（4）<div>希望讲解能给通俗易懂一些。专业词汇太多，生涩</div>2019-03-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/bb/01/568ac2d6.jpg" width="30px"><span>K4SHIFZ</span> 👍（16） 💬（3）<div>凡是{}包裹的代码都会产生let&#47;const作用域吧？除了文中提到的for等，还有while，do while，代码块等</div>2019-04-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/6c/18/850a0797.jpg" width="30px"><span>Zach</span> 👍（11） 💬（2）<div>老师，关于realm最后一个示例

var iframe = document.createElement(&#39;iframe&#39;)
document.documentElement.appendChild(iframe)
iframe.src=&quot;javascript:var b = {};&quot;
var b1 = iframe.contentWindow.b;
var b2 = {};
console.log(typeof b1, typeof b2); &#47;&#47;object object
console.log(b1 instanceof Object, b2 instanceof Object); &#47;&#47;false true

应该有点问题，typeof b1 的结果在chrome和Firefox中都显示为 undefined object</div>2019-04-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c0/99/259a412f.jpg" width="30px"><span>Geeker</span> 👍（6） 💬（0）<div>老师，可否稍加解释一下执行上下文的分类? 网络上的文章说“ JS 中可执行的代码可分为三种类型：全局代码、函数代码、eval 代码，对应三种执行上下文（全局执行上下文、函数执行上下文、eval 执行上下文），在 ECMAScript 2018 中没有找到这种说法的依据。我的意思是，我不太清楚这些文章的说法是否正确，是否不够全面。</div>2019-04-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/41/a5/16c615cc.jpg" width="30px"><span>乃乎</span> 👍（6） 💬（1）<div>更喜欢 const 哈哈</div>2019-02-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/8d/0e/5e97bbef.jpg" width="30px"><span>半橙汁</span> 👍（5） 💬（0）<div>闭包指的是那些引用了另一个函数作用域中变量的函数，通常是在嵌套函数中实现的。---高程4中的解释
好多问题，结合着书籍来看，就没那么晦涩难懂了~
书中自有黄金屋，书中自有颜如玉~</div>2020-10-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/e7/34/66289bd6.jpg" width="30px"><span>Tokiomi</span> 👍（4） 💬（0）<div>看晕了。。
http:&#47;&#47;www.ruanyifeng.com&#47;blog&#47;2009&#47;08&#47;learning_javascript_closures.html
阮一峰的闭包定义: 
&quot;各种专业文献上的&quot;闭包&quot;（closure）定义非常抽象，很难看懂。我的理解是，闭包就是能够读取其他函数内部变量的函数。
由于在Javascript语言中，只有函数内部的子函数才能读取局部变量，因此可以把闭包简单理解成&quot;定义在一个函数内部的函数&quot;。
所以，在本质上，闭包就是将函数内部和函数外部连接起来的一座桥梁。&quot;
所以Winter大佬的定义和阮一峰的定义哪个对。。。</div>2020-07-15</li><br/><li><img src="" width="30px"><span>比利利</span> 👍（4） 💬（2）<div>我认为在目前的环境下，var已经没有存在的必要了，所有以前用var的情况都可以通过let和const代替，而且let和const更加符合大多数编程语言的习惯，而且现在有babel的话，写ES6语法也非常安全。</div>2019-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/39/1b/bcabd223.jpg" width="30px"><span>Snow同學</span> 👍（4） 💬（5）<div>函数就是闭包，这个理解对吗？</div>2019-03-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/94/56/4b8395f6.jpg" width="30px"><span>CC</span> 👍（4） 💬（0）<div>今天是自己第一次结构性整理清楚 JavaScript 的函数部分。原来它除了函数体之外，还包括了函数所处的环境，而其中的词法环境，其实只是执行上下文七个部分中的的一支。

个人感觉 var 声明在不同的执行上下文中相对 let 更容易出错，同时也会增加冗余的临时变量。比如在 for loop 中，会遇到需要为不同的 loop 声明 i、j、k 变量。

代码不仅是写给机器看，也是写给同行看的。let 会使代码更加简洁易读。
</div>2019-02-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/1e/a2/083412c6.jpg" width="30px"><span>疯羊先生</span> 👍（3） 💬（0）<div>看完评论，我觉得闭包待分成广义的和狭义的了，简直了，婆说婆有理的感觉。。。广义--闭包就是函数函数就是闭包，狭义闭包就是引用另一个函数内部变量的函数。。。懵逼树上懵逼果，懵逼树下你和我</div>2020-12-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/71/69/f7ae97c8.jpg" width="30px"><span>霍光传不可不读</span> 👍（3） 💬（5）<div>仔细看了下维基百科上面闭包的定义：闭包是一个record，它存储了一个函数和它的环境，这个环境存储了该函数的自由变量，js的函数完全符合这个定义，所以说js的函数其实就是闭包。倒是普通函数有点特别，我自己理解，这样的函数才是普通函数：
function(a, b) {
    const c = 10
    return a + b + c;
}
这个函数只访问了自己的函数作用域内部的变量和参数，这样的函数才是所谓的普通函数，不知道这样理解对不对？</div>2019-04-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/9d/59/1c084632.jpg" width="30px"><span>Ron</span> 👍（2） 💬（0）<div>很少见到用void写IIFE，感觉大多时候我们还是需要引用IIFE返回的东西，可以参考一下https:&#47;&#47;developer.mozilla.org&#47;en-US&#47;docs&#47;Glossary&#47;IIFE</div>2019-05-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/8c/d5/398b31fe.jpg" width="30px"><span>木棉</span> 👍（2） 💬（1）<div>var b;
            void function(){
                var env = {b:1};
                b=2;
                console.log(b);
                with(env){
                    var b=3;
                    console.log(b);
                }
            }();
            console.log(b);
这块的执行结果是：2，3，undefined，不懂为什么，希望老是可以详细解答一下。
作用域这块的内容经常被问到，尤其是面试的时候做题，变量提升，闭包，立即执行的函数表达式等不同情况不同输出结果，总是各种被绕晕，希望老师可以帮忙梳理一下，谢谢</div>2019-04-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（2） 💬（5）<div>老师 我这有个问题：对于这段代码；
var b;
void function(){
    var env = {b:1};
    b = 2;
    console.log(&quot;In function start b:&quot;, b);
    with(env) {
        var b = 3;
        console.log(&quot;In with b:&quot;, b);
    }
	console.log(&quot;In function end b:&quot;, b);
}();
console.log(&quot;Global b:&quot;, b);

打印结果是这样的：
In function start b: 2
In with b: 3
In function end b: 2
Global b: 10

不知道是怎得出老师文章中结论的，我看下面有好多评论也是这样的疑问，麻烦老师解答一下呢</div>2019-03-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/01/c3/3b5fe59e.jpg" width="30px"><span>飞鸟</span> 👍（1） 💬（0）<div>任何一个函数都是闭包。当一个函数对象从内部穿透到外部，为了保证满足闭包的要求，引擎就会需要把上级的函数对象环境也保留，使用不当，就可能会导致内存泄漏。</div>2023-01-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/0a/75/aac066a2.jpg" width="30px"><span>张小🐶</span> 👍（1） 💬（0）<div>关于VariableEnvironment和LexicalEnvironment，看了一下标准里的说法（https:&#47;&#47;262.ecma-international.org&#47;11.0&#47;#sec-execution-contexts）：
- LexicalEnvironment： Identifies the Lexical Environment used to resolve identifier references made by code within this execution context.
- VariableEnvironment： Identifies the Lexical Environment whose EnvironmentRecord holds bindings created by VariableStatements within this execution context.
- The LexicalEnvironment and VariableEnvironment components of an execution context are always Lexical Environments.

我的理解是：
1. VariableEnvironment持有var声明的变量
2. LexicalEnvironment持有let、const等声明的变量
3. VariableEnvironment和LexicalEnvironment都是Lexical Environments类型的对象。（Lexical Environments和LexicalEnvironment不是一回事）

但是关于老师讲的：“LexicalEnvironment获取变量时使用，VariableEnvironment声明变量时使用”。还是不太理解。想问一下这个说法在标准里的依据是哪里？可以再深入解读一下吗？

感谢。</div>2021-04-21</li><br/>
</ul>