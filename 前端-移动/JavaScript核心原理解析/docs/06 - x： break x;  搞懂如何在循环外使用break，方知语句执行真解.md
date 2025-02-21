你好，我是周爱民。

上一讲的`for`语句为你揭开了JavaScript执行环境的一角。在执行系统的厚重面纱之下，到底还隐藏了哪些秘密呢？那些所谓的执行环境、上下文、闭包或块与块级作用域，到底有什么用，或者它们之间又是如何相互作用的呢？

接下来的几讲，我就将重点为你讲述这些方面的内容。

## 用中断（Break）代替跳转

在Basic语言还很流行的时代，许多语言的设计中都会让程序代码支持带地址的“语句”。例如，Basic就为每行代码提供一个标号，你可以把它叫做“**行号**”，但它又不是绝对物理的行号，通常为了增减程序的方便，会使用“1，10，20…...”等等这样的间隔。如果想在第10行后追加1行，就可以将它的行号命名为“11”。

行号是一种很有历史的程序逻辑控制技术，更早一些可以追溯到汇编语言，或可以手写机器代码的时代（确实存在这样的时代）。那时由于程序装入位置被标定成内存的指定位置，所以这个位置也通常就是个地址偏移量，可以用数字化或符号化的形式来表达。

所有这些“为代码语句标示一个位置”的做法，其根本目的都是为了实现“GOTO跳转”，任何时候都可以通过“GOTO 标号”的语法来转移执行流程。

然而，这种黑科技在20世纪的60~70年代就已经普遍地被先辈们批判过了。这样的编程方式只会大大地降低程序的可维护性，其正确性或正确性验证都难以保障。所以，后面的故事想必你都知道了，半个多世纪之前开始的**“结构化”运动**一直影响至今，包括现在我与你讨论的这个JavaScript，都是“结构化程序设计”思想的产物。
<div><strong>精选留言（27）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/16/50/96/dd23dcb0.jpg" width="30px"><span>不将就</span> 👍（30） 💬（2）<div>老师，问个问题，
{
let a=10
}
这是块级作用域

{
var a=10
}
在外层可以访问到a为未定义，这是不是可以说明{}这对括号里只有出现let&#47;const才算有块级作用域？但是如下
if(1){
let b=10
}
这个if语句有括号而且用了let，老师为什么又说if语句没有块级作用域？
</div>2019-11-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/6f/10/bfbf81dc.jpg" width="30px"><span>海绵薇薇</span> 👍（20） 💬（1）<div>Hello，老师好：）阅读完文章还存在如下问题，期待有解答或方向，感谢：）

try { 

​	1

} finally {

​	console.log(&#39;finally&#39;)

​	2

}

输出：

&gt; finally

&gt; 1

1. try finally 语句输出的Result 是{type: normal, value: 1}。但是最后一个语句是finally中的2，value不应该是2吗？

try {

​	throw 1

} catch(ex) {

​	2

}

这里确实输出了2。


function foo() {

​	aaa: try {

​		return 1;

​	} finally {

​		break aaa;

​	}

}

return 1   Result是{type: return, value: 1}
break      Result是{type: break, value: empty, target: aaa}

2. 这里finally中语句的结果却覆盖了try中语句的结果，这是一个特例吗？</div>2019-11-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d4/37/528a43e7.jpg" width="30px"><span>Elmer</span> 👍（10） 💬（3）<div>觉得函数执行应该是语句执行的一部分或者一个特例，返回值都已经统一为文中的result。
只不过函数执行具体实现了本身的上下文创建与回收，并用额外的栈来记录当前执行状况。
两者都是流程控制的一种形式。关系应为语句执行包含函数执行。
不知道理解的对不对。</div>2019-12-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/52/36/18f5d218.jpg" width="30px"><span>zcdll</span> 👍（9） 💬（1）<div>返回 Empty 的语句，是不是还有 单独的一个 分号，和  if 不写大括号，或者大括号中为空？</div>2019-11-22</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/bOFMGebia5L9r0srOd8lblaoWHNSATQrAabGQgcL6MnvAP7V1QqU8sjwdnZib4Hsia5Kv8ozex7KDcYRKrrhiaQLqg/132" width="30px"><span>Geek_q04ku5</span> 👍（6） 💬（2）<div>尝试完整地对比函数执行与语句执行的过程：

·操作返回值：
函数执行：在函数体的最后进行一次返回值的赋值
语句执行：在每句后更新返回值

如下所示：
function foo() {
    1 + 1;
    return 1; &#47;&#47;函数的执行结果为1 赋值动作仅有一次
}

foo();


{
    1 + 1; &#47;&#47;整个块语句的执行结果更新为2
    2 + 2; &#47;&#47;整个块语句的执行结果更新为4
}

·堆栈顺序
函数执行与语句执行类似 是先入后出的堆栈

如下所示：

function bar() {
    return;
}

function foo() {
    1 + 1;
    bar()
    return 1; &#47;&#47;函数的执行结果为1 赋值动作仅有一次
}

foo();

&#47;&#47;开始执行foo-&gt;开始执行bar-&gt;bar执行结束-&gt;foo执行结束

{
    1 + 1; &#47;&#47;整个块语句的执行结果更新为2
    2 + 2; &#47;&#47;整个块语句的执行结果更新为4
}


&#47;&#47;开始执行块语句{}-&gt;执行1+1-&gt;1+1执行结束-&gt;执行2+2-&gt;2+2执行结束-&gt;块语句执行结束

·操作Result的对象
函数：getValue(ref)||ref传递给上一层表达式使用
语句：Completion传递给引擎进行使用</div>2020-04-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/07/36/d677e741.jpg" width="30px"><span>黑山老妖</span> 👍（5） 💬（1）<div>1、传统习惯上过来的开发人员会把“if () { ... }”理解成一个语句，而在JavaScript中，这是两个语句。
2、在try{}块中使用return语句，那么在return之前会执行到finally{}块，而finally{}执行完之后，还会回到try{}块里的return语句来返回。所以最终“完成并退出”整个try语句的，还是try块。
3、·操作Result的对象
函数：getValue(ref)||ref传递给上一层表达式使用
语句：Completion传递给引擎进行使用  
4、所谓“可中断语句”其实只有两种，包括全部的循环语句，以及 swtich 语句。
5、1、执行结果方面：

JavaScript 是一门混合了函数式与命令式范型的语言，对函数和语句的不同处理，正是两种语言范型根本上的不同抽象模型带来的差异。

本质上所有 JavaScript 的执行都是语句执行（包括函数执行），语句执行的过程因语句类型而异，但结果都返回的是一个“完成”结果。

但【函数语句执行】和【普通语句（非函数）执行】的区别在于：函数语句执行返回的“完成”结果是值或者引用（未报异常的情况下），而普通语句执行返回的是一个完成状态（Completion）。


2、执行过程方面：

总体来讲，

JavaScript 的执行机制包含两部分：【执行权（逻辑）】和【数据资源（数据）】

JavaScript的执行（运行）环境：是一个后入先出的栈，栈顶就是当前“执行权”拥有者所持有的那一帧数据，运行环境通过函数的 CALL&#47;RETURN 来模拟“数据帧”（也称上下文环境或作用域）在栈上的入栈和出栈过程。

但&quot;break labelName&quot;这一语法跟上面不同，它表达一个位置的跳转，而不是一个数据帧的进出栈。

另外，各种类型的语句执行过程（内部逻辑）也可能有差异：

2.1 函数执行过程
2.2 break 执行过程
2.3 case 执行过程
2.4 switch 执行过程
2.5 循环语句执行过程
2.6 try...catch 执行过程


【仍旧未解的疑问】

1、函数执行和语句执行返回的都是一个完成状态？还是函数执行返回的只能是值或引用？亦或是其他说法？表达式执行（包括函数执行），本质上都是求值运算，所以它们应当只返回值。但是事实上所有的执行——包括函数、表达式和语句也都“同时”是可以返回完成状态，这样才能在表达式中向外抛异常，因为异常抛出就是一个完成状态。

但是ECMAScript对所有在表达式层面上返回的“完成状态”做了处理，相当于在语言层面上“消化了”这些状态。所以绝大多数情况下，你认为表达式执行返回的Result是值或引用就好了。稍有例外的是，函数调用返回的是一个type为Return的完成状态，只不过它在内部方法Call处理之后，也已经变成了值而已。


1、可以理解为函数中return的设计是为了传递函数的状态，break的设计则是为了传递语句的状态么？可以
2、可以认为break;只可以中断语句，不能用在函数中，break label;可以用在函数中，它返回了上一行语句的完成状态并作为所在函数的返回值？. 不太对。break labelName只与“块”相关，与函数没直接关系。语句的“块”也是有返回值的，因为JavaScript里面存在“语句执行是有值的”这个设定。

注意有许多语句是有“块（块级作用域）”的，而不仅仅是块语句（也就是一对大括号，它称为Block语句）。

函数执行啊，其实是表达式执行的特例。它会通过完成记录来返回return语句返回结果。

但是，在内部过程Call()的调用中它会取出值，而不是直接返回“Return类型的完成类型”。所以在“函数调用作为表达式的操作数”时，运算处理的还是“Result&#47;Value值”，而不是“完成记录”。

由于函数调用会“从完成记录中取出值”，所以它不能返回“引用（规范类型）”


在js中，语句执行跟表达式执行是分开的，是两种不同概念的东西。而函数执行其实是表达式执行的一种，其中函数名（亦即是函数）是运算数，而一对括号是运算符。——这是确实的，并且这个称为“函数调用运算符”的括号也是有优先级的，你可以直接在MDN里面查到。

表面来看，函数就是一堆语句，但其实“函数执行”时的返回值是由return来决定的，对吧。而语句执行却不是，语句执行的结果值是由“最后一个有效语句”来决定的。当你使用eval()来执行一批语句时，就可以看到这个结果值了。——并且，这也是语句执行要被拿出来讨论的原因，亦即是“动态执行”执行的是语句，而不是函数，也不是表达式。
</div>2022-01-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/ae/a0/707350ef.jpg" width="30px"><span>穿秋裤的男孩</span> 👍（5） 💬（6）<div>所谓“可中断语句”其实只有两种，包括全部的循环语句，以及 swtich 语句。

老师，那forEach不属于循环语句吗？为什么break不可以在forEach中使用呢</div>2019-11-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c2/49/6d68160e.jpg" width="30px"><span>Real Aaron</span> 👍（4） 💬（2）<div>【学习方式大变化】

前5讲看下来，主要有两个感觉：

1、课程的内容非常深入而且重要，经常中间看到一段文字，就有一种“原来如此“的体验。
2、逻辑顺序看不懂，看完一讲之后，好像学到一些零碎知识，但串不一起来。

今天凑巧看到了加餐中的”学习这门课的正确姿势“，原来老师用心良苦，没有将知识点清晰的串起来是希望大家自己能主动理清思路，串出逻辑。

参考加餐中的方法，今天换了一种学习方式：一边学习内容，一边将关键词和疑惑（dots）写在本子上，反复琢磨其中的来龙去脉。最终写满了两页纸，然后将其中的各个点串起来（connecting the dots），形成了下面的笔记。

【本讲的一些记录和归纳】

1、执行结果方面：

JavaScript 是一门混合了函数式与命令式范型的语言，对函数和语句的不同处理，正是两种语言范型根本上的不同抽象模型带来的差异。

本质上所有 JavaScript 的执行都是语句执行（包括函数执行），语句执行的过程因语句类型而异，但结果都返回的是一个“完成”结果。

但【函数语句执行】和【普通语句（非函数）执行】的区别在于：函数语句执行返回的“完成”结果是值或者引用（未报异常的情况下），而普通语句执行返回的是一个完成状态（Completion）。


2、执行过程方面：

总体来讲，

JavaScript 的执行机制包含两部分：【执行权（逻辑）】和【数据资源（数据）】

JavaScript的执行（运行）环境：是一个后入先出的栈，栈顶就是当前“执行权”拥有者所持有的那一帧数据，运行环境通过函数的 CALL&#47;RETURN 来模拟“数据帧”（也称上下文环境或作用域）在栈上的入栈和出栈过程。

但&quot;break labelName&quot;这一语法跟上面不同，它表达一个位置的跳转，而不是一个数据帧的进出栈。

另外，各种类型的语句执行过程（内部逻辑）也可能有差异：

2.1 函数执行过程
2.2 break 执行过程
2.3 case 执行过程
2.4 switch 执行过程
2.5 循环语句执行过程
2.6 try...catch 执行过程


【仍旧未解的疑问】

1、函数执行和语句执行返回的都是一个完成状态？还是函数执行返回的只能是值或引用？亦或是其他说法？

希望老师能解答一下，非常感谢。</div>2019-12-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/2d/44/0a209c31.jpg" width="30px"><span>桔右</span> 👍（4） 💬（1）<div>1、可以理解为函数中return的设计是为了传递函数的状态，break的设计则是为了传递语句的状态么？
2、可以认为break;只可以中断语句，不能用在函数中，break label;可以用在函数中，它返回了上一行语句的完成状态并作为所在函数的返回值？</div>2019-11-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d4/37/528a43e7.jpg" width="30px"><span>Elmer</span> 👍（3） 💬（1）<div>求函数执行与语句执行的过程对比。</div>2019-12-26</li><br/><li><img src="" width="30px"><span>Geek8740</span> 👍（2） 💬（3）<div>老师，try finaly中return的执行机制到底是怎样的？我下面几个例子彻底弄懵了

&#47;&#47; 测试样例1：try里有return finally里没有return
let x = 0;
function f (){
    try {
        console.log(&quot;try start:&quot;,x)
        x = 1
        console.log(&quot;try end:&quot;,x)
       return x;
    } catch(e){
    }
    finally{
        console.log(&quot;finally: start&quot;,x)
        x = 3;
        console.log(&quot;finally: end&quot;,x)
    }
    console.log(&quot;return:&quot;,x)
    return x;
}
console.log(f())
&#47;* 输出结果：
try start: 0
try end: 1
finally: start 1
finally: end 3
1

&#47;&#47;疑问：既然finally里的x和try是同一个，且赋值是后执行，为啥最后return的x值还是1呢？
*&#47;

&#47;&#47; 测试样例2：如果在finally里也加个return语句
let x = 0;
function f (){
    try {
        console.log(&quot;try start:&quot;,x)
        x = 1
        console.log(&quot;try end:&quot;,x)
       return x;
    } catch(e){
    }
    finally{
        console.log(&quot;finally: start&quot;,x)
        x = 3;
        console.log(&quot;finally: end&quot;,x)
        return x
    }
    console.log(&quot;return:&quot;,x)
    return x;
}
console.log(f())
&#47;* 输出结果：
try start: 0
try end: 1
finally: start 1
finally: end 3
3
*&#47;

&#47;&#47; 测试样例3：如果finally和try语句块里都没有return语句
let x = 0;
function f (){
    try {
        console.log(&quot;try start:&quot;,x)
        x = 1
        console.log(&quot;try end:&quot;,x)
    } catch(e){
        x = 2;
        return x;
    }
    finally{
        console.log(&quot;finally: start&quot;,x)
        x = 3;
        console.log(&quot;finally: end&quot;,x)
    }
    console.log(&quot;return:&quot;,x)
    return x;
}
console.log(f())
&#47;* 输出结果：
try start: 0
try end: 1
finally: start 1
finally: end 3
3
*&#47;</div>2022-05-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/cb/ce/d9e00eb5.jpg" width="30px"><span>undefined</span> 👍（1） 💬（1）<div>我又来了…

原文 ↓

如果在 try 或 try..except 块中使用了 return

应该是

try...finally
</div>2021-04-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/25/0c/d2ad7cb7.jpg" width="30px"><span>王美红</span> 👍（1） 💬（1）<div>老师，想问下，函数不就是语句构成的，为什么要说 函数执行和语句执行的结果不一样呢？不太懂为啥要这样分开讨论？</div>2021-03-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/89/5b/d8f78c1e.jpg" width="30px"><span>孜孜</span> 👍（1） 💬（1）<div>表达式的result引用和语句的result有联系吗？</div>2020-06-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/3a/93/d7be8a1a.jpg" width="30px"><span>晓小东</span> 👍（1） 💬（2）<div>老师有一个表达式执行让我感到困惑， 我在做位运算符的时候碰到这么一个现象
let n = 2;
    let c1 = n != 0;
    let c2 = (n &amp; (n - 1)) === 0;
    let c3 = n &amp; (n - 1) === 0;
    console.log(c1, c2, c3);  

打印： true true 0   
c3 结果为什么变成了0  按照表达式 左右操作数的逻辑</div>2019-11-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/6d/70/25ba4287.jpg" width="30px"><span>明月</span> 👍（0） 💬（1）<div>基于对“语句”的不同理解，JavaScript 设计了一种全新方法，用来清除这个跳转所带来的影响（也就是回收跳转之前的资源分配）。而这多余出来的设计，其实也是上述收益所需要付出的代价。
有个地方有疑惑还希望获得老师的解答：块语句存在块级作用域的，当块语句中执行到break中断语句后，块级作用域会如何（没有break中断语句时块级作用域是出栈的）</div>2022-08-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/08/43/90edecba.jpg" width="30px"><span>ayu</span> 👍（0） 💬（1）<div>eval( &#39;aaa: {     1+2;     bbb: {      void 7;      break aaa;     }   }&#39;) &#47;&#47; NaN

老师能解释下返回 NaN 而不是 undefined 的原理吗</div>2022-01-11</li><br/><li><img src="" width="30px"><span>Sam</span> 👍（0） 💬（1）<div>function testBlock () {
    let t = 1;
    try {
        t = 2;
        return t;
    }
    finally {
        t = 3
    }
}
console.log(testBlock()) &#47;&#47;输出为2
想请教下老师：
1. 如果finally块，是在try的块中return语句执行前执行话，怎么返回的变量t是try块中赋的值
2. 在try和finally中的t变量与外部let定义的t是同一个吗？</div>2021-07-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/9a/e8/37163caf.jpg" width="30px"><span>爱呀顶呀</span> 👍（0） 💬（1）<div>
&#47;&#47; 在if语句的两个分支中都可以使用break；
&#47;&#47; （在分支中深层嵌套的语句中也是可以使用break的）
aaa: if (true) {
   ...
}
else {
  ...
  break aaa;
}
 
&#47;&#47; 在try...catch...finally中也可以使用break;
bbb: try {
  ...
}
finally {
  break bbb;
}


能详细解释下吗？ 看不懂呀</div>2020-07-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/10/30/c07d419c.jpg" width="30px"><span>卡尔</span> 👍（0） 💬（2）<div>函数执行，语句执行，表达式执行。后两者是什么关系？</div>2020-06-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a3/ea/53333dd5.jpg" width="30px"><span>HoSalt</span> 👍（0） 💬（1）<div>aaa: if (true) {
  ...
} else {  
  ...  
  break bbb;
}
这惹人应该是break aaa 吧</div>2020-05-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/ea/05/9976b871.jpg" width="30px"><span>westfall</span> 👍（1） 💬（0）<div>第一次看到标签化语句，请问老师，标签化语句除了用来 break，在实际的开发中还有哪些应用场景?</div>2019-11-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/45/da/71b7599d.jpg" width="30px"><span>antimony</span> 👍（0） 💬（0）<div>因为从没用过标签语句所以一开始看这篇文章时有些难以理解，有相同问题的同学可以先在mdn上了解一下标签的使用https:&#47;&#47;developer.mozilla.org&#47;en-US&#47;docs&#47;Web&#47;JavaScript&#47;Reference&#47;Statements&#47;label。</div>2020-02-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/c5/e9/4013a191.jpg" width="30px"><span>阿鑫</span> 👍（0） 💬（0）<div>居然还有标签语句，涨见识了</div>2019-12-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/cf/14/384258ba.jpg" width="30px"><span>Wiggle Wiggle</span> 👍（0） 💬（0）<div>我觉得函数执行与语句执行的区别就是：函数调用涉及到入栈出栈，语句执行不涉及。</div>2019-11-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/1f/86/3a7eeac4.jpg" width="30px"><span>leslee</span> 👍（0） 💬（0）<div>这篇看来要看很多次了……</div>2019-11-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/49/f6/ef3e5c81.jpg" width="30px"><span>shengsheng</span> 👍（0） 💬（0）<div>03年我在学vb的时候，并没有提到goto有学，不过后面越来越多资料指出goto问题。</div>2019-11-22</li><br/>
</ul>