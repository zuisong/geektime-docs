在[上一篇文章](https://time.geekbang.org/column/article/126339)中我们讲到了什么是作用域，以及ES6是如何通过变量环境和词法环境来同时支持变量提升和块级作用域，在最后我们也提到了如何通过词法环境和变量环境来查找变量，这其中就涉及到**作用域链**的概念。

理解作用域链是理解闭包的基础，而闭包在JavaScript中几乎无处不在，同时作用域和作用域链还是所有编程语言的基础。所以，如果你想学透一门语言，作用域和作用域链一定是绕不开的。

那今天我们就来聊聊**什么是作用域链**，并通过作用域链再来讲讲**什么是闭包**。

首先我们来看下面这段代码：

```
function bar() {
    console.log(myName)
}
function foo() {
    var myName = "极客邦"
    bar()
}
var myName = "极客时间"
foo()
```

你觉得这段代码中的bar函数和foo函数打印出来的内容是什么？这就要分析下这两段代码的执行流程。

通过前面几篇文章的学习，想必你已经知道了如何通过执行上下文来分析代码的执行流程了。那么当这段代码执行到bar函数内部时，其调用栈的状态图如下所示：

![](https://static001.geekbang.org/resource/image/87/f7/87d8bbc2bb62b03131802fba074146f7.png?wh=1142%2A675)

执行bar函数时的调用栈

从图中可以看出，全局执行上下文和foo函数的执行上下文中都包含变量myName，那bar函数里面myName的值到底该选择哪个呢？

也许你的第一反应是按照调用栈的顺序来查找变量，查找方式如下：

1. 先查找栈顶是否存在myName变量，但是这里没有，所以接着往下查找foo函数中的变量。
2. 在foo函数中查找到了myName变量，这时候就使用foo函数中的myName。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/94/82/d0a417ba.jpg" width="30px"><span>蓝配鸡</span> 👍（218） 💬（21）<div>var bar = {
    myName:&quot;time.geekbang.com&quot;,
    printName: function () {
        console.log(myName)
    }    
}
function foo() {
    let myName = &quot; 极客时间 &quot;
    return bar.printName
}
let myName = &quot; 极客邦 &quot;
let _printName = foo()
_printName()
bar.printName()


全局执行上下文：
变量环境：
Bar=undefined
Foo= function 
词法环境：
myname = undefined 
_printName = undefined 

开始执行：
bar ={myname: &quot;time.geekbang.com&quot;, printName: function(){...}}

myName = &quot; 极客邦 &quot;
 _printName = foo() 调用foo函数，压执行上下文入调用栈

foo函数执行上下文：
变量环境： 空
词法环境： myName=undefined
开始执行：
myName = &quot; 极客时间 &quot;
return bar.printName
开始查询变量bar， 查找当前词法环境（没有）-&gt;查找当前变量环境（没有） -&gt; 查找outer词法环境（没有）-&gt; 查找outer语法环境（找到了）并且返回找到的值
pop foo的执行上下文

_printName = bar.printName
printName（）压bar.printName方法的执行上下文入调用栈

bar.printName函数执行上下文：
变量环境： 空
词法环境： 空
开始执行：
console.log(myName)
开始查询变量myName， 查找当前词法环境（没有）-&gt;查找当前变量环境（没有） -&gt; 查找outer词法环境（找到了）
打印&quot; 极客邦 &quot;
pop bar.printName的执行上下文


bar.printName() 压bar.printName方法的执行上下文入调用栈

bar.printName函数执行上下文：
变量环境： 空
词法环境： 空
开始执行：
console.log(myName)
开始查询变量myName， 查找当前词法环境（没有）-&gt;查找当前变量环境（没有） -&gt; 查找outer词法环境（找到了）
打印&quot; 极客邦 &quot;
pop bar.printName的执行上下文




</div>2019-08-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（93） 💬（13）<div>思考题：
这道题其实是个障眼法，只需要确定好函数调用栈就可以很轻松的解答，调用了foo()后，返回的是bar.printName，后续就跟foo函数没有关系了，所以结果就是调用了两次bar.printName()，根据词法作用域，结果都是“极客邦”，也不会形成闭包。
闭包还可以这样理解：当函数嵌套时，内层函数引用了外层函数作用域下的变量，并且内层函数在全局作用域下可访问时，就形成了闭包。</div>2019-08-27</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/ibZVAmmdAibBeVpUjzwId8ibgRzNk7fkuR5pgVicB5mFSjjmt2eNadlykVLKCyGA0GxGffbhqLsHnhDRgyzxcKUhjg/132" width="30px"><span>pyhhou</span> 👍（71） 💬（4）<div>思考题，最后输出的都是 “极客邦”，这里不会产生函数闭包，解释如下：

1. bar 不是一个函数，因此 bar 当中的 printName 其实是一个全局声明的函数，bar 当中的 myName 只是对象的一个属性，也和 printName 没有联系，如果要产生联系，需要使用 this 关键字，表示这里的 myName 是对象的一个属性，不然的话，printName 会通过词法作用域链去到其声明的环境，也就是全局，去找 myName

2. foo 函数返回的 printName 是全局声明的函数，因此和 foo 当中定义的变量也没有任何联系，这个时候 foo 函数返回 printName 并不会产生闭包</div>2019-08-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/fe/0c/f9cb1af4.jpg" width="30px"><span>李艺轩</span> 👍（55） 💬（7）<div>关于闭包的概念：
老师提出的概念：内部函数引用外部函数的变量的集合。
高级程序设计中的概念：闭包是指有权访问另一个函数作用域中的变量的函数。
MDN上的概念：闭包是函数和声明该函数的词法环境的组合。
所以到底哪个是对的。。MDN = 老师 + 高程</div>2019-09-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/4d/04/5e0d3713.jpg" width="30px"><span>李懂</span> 👍（13） 💬（5）<div>本来对这篇文章充满期待,看完后还是有很多疑惑
又翻看了一下小红书
有以下疑问:

1. 最后的分析图是不是有问题,全局上下文中变量环境怎么会有myName
foo上下文中的innerBar是对象,用了函数?

2.闭包是存在调用栈里的,现在的模块化存在大量闭包,那不是调用栈底部存在大量闭包
很容易栈溢出吧
3.看了下chrome中函数对应的[[Scopes]]是个List集合包含了闭包模块,这个是不是文章中的outer

4.闭包是包含了整个变量环境和词法环境,还是只是包含用到的变量</div>2019-08-27</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/7WkTI1IicbKvsPJng5vQh5qlrf1smbfl2zb7icHZfzcAk1k4lr8w8IDEAdrqq1NHW5XZMPXiaa1h7Jn1LGOWOCkIA/132" width="30px"><span>早起不吃虫</span> 👍（11） 💬（1）<div>作为一名前端虽然这些都是早已熟悉的，但是老师讲的确实是好呀，深入浅出，逻辑清晰，期待后面的课程！</div>2019-08-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/d6/35/9b213d2f.jpg" width="30px"><span>hzj.</span> 👍（9） 💬（3）<div>首先两个函数都会打印 : 极客邦
社区中对闭包的定义: 函数执行产生私有作用域, 函数内部返回一个调用的函数, 由于外部会拿到内部函数的返回值, 所以内部函数不会被垃圾回收, 这个私有作用域就是闭包.
闭包的作用有两点: 1. 保护私有变量      2. 维持内部私有变量的状态
但是在 sicp (计算机程序的构造与解释) 中认为:   只要函数调用, 那么就会产生闭包.
所以, 我认为是会产生闭包的
_printName() 输出 极客邦, 因为 _printName拿到了bar.printName, 打印上面的 myName即可.
bar.printName() 输出 极客邦, 因为会直接打印全局的 myName.
最后, 只有在 foo() 函数中有 log, 才会输出 &quot;极客时间&quot;, 因为 这个值是在 foo 函数的私有作用域中的!!!</div>2019-08-27</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJibVeub5HnlS9HgLdrDSnQma6VINyAyf1bTOhKh4MGQkMydoCVs7ofbicePRomxjDM873A56fqx97w/132" width="30px"><span>oc7</span> 👍（7） 💬（1）<div>function foo() {
    var myName = &quot; 极客时间 &quot;
    let test1 = 1
    const test2 = 2
    var innerBar = {
        getName:function(){
            console.log(test1)
            return myName
        },
        setName:function(newName){
            myName = newName
        }
    }
    return innerBar
}
var bar = foo()
bar.setName(&quot; 极客邦 &quot;)
bar.getName()
console.log(bar.getName())

有个问题没搞明白
在return innerBar的时候 bar.setName(&quot; 极客邦 &quot;)和bar.getName()这两个函数还没有执行 为什么会执行词法作用域的分析 之前不是说只有函数调用时才创建这个函数的执行作用域和可执行代码</div>2019-09-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/02/81/489e1cd4.jpg" width="30px"><span>忘忧草的约定</span> 👍（6） 💬（3）<div>老师我想请教一个问题：函数执行上下文是在函数执行前的编译阶段存入执行栈的、那么执行上下文中的outer也是在编译阶段通过分析函数声明的位置来赋值的吗？</div>2019-08-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/60/40/e6d4c1b4.jpg" width="30px"><span>ChaoZzz</span> 👍（4） 💬（1）<div>不会产生闭包，函数在被创建的时候它的作用域链就已经确定了，所以不论是直接调用bar对象中的printName方法还是在foo函数中返回的printName方法他们的作用域链都是[自身的AO, 全局作用域]，自身的AO中没有myName就到全局中找，找到了全局作用域中的myName = &#39; 极客邦 &#39;，所以两次打印都是“极客邦”啦~</div>2019-08-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ba/bd/6f2f078c.jpg" width="30px"><span>Marvin</span> 👍（3） 💬（4）<div>请问
console.log(a)
{
  function a(){}
}
为何会log一个undefined？目测function的变量提升会受到块的影响，这是标准浏览器的特性造成的，还是IE6时代就是这样呢？</div>2019-08-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/f5/b8/9f165f4b.jpg" width="30px"><span>mfist</span> 👍（3） 💬（1）<div>1. _printName是一个全局函数，执行的话 不会访问到内部变量。输出全局变量的myName 极客邦
2. bar.printName 同样输出是极客邦

随着专栏的推进，发现看一遍文章的时间一直在增长。发现了很多的知识盲区，很多内容只是知道，不知道底层原理。

今日得到：作用域链如何选择，闭包如何形成</div>2019-08-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/d9/c6/8be8664d.jpg" width="30px"><span>ytd</span> 👍（2） 💬（1）<div>不会产生闭包，都打印极客邦。printName函数定义时的执行上下文是全局，所以会在全局词法环境和变量环境下找myName。</div>2019-08-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/99/7c/fddb4261.jpg" width="30px"><span>程力辛</span> 👍（1） 💬（2）<div>所以变量环境是动态的，根据函数调用关系。词法环境是静态的，根据函数定义时的状态？</div>2019-08-27</li><br/><li><img src="" width="30px"><span>vianem</span> 👍（0） 💬（2）<div>老师，词法环境和词法作用域不是一个东西吧？</div>2019-11-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/db/0b/f0ded153.jpg" width="30px"><span>江谢木</span> 👍（0） 💬（1）<div>老师没太明白“如果引用闭包的函数是全局变量”这句，按文章的理解一个函数在另一个函数内部声明才会产生闭包，那如果一个函数是全局变量那他就不会产生闭包啊？</div>2019-11-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/bc/29/c248bfd1.jpg" width="30px"><span>肥嘟嘟左卫门</span> 👍（0） 💬（1）<div>好开心，感觉我终于理解闭包了，我是不是膨胀了#捂脸# 这个专栏真的超赞👍</div>2019-09-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/3a/93/d7be8a1a.jpg" width="30px"><span>晓小东</span> 👍（0） 💬（1）<div>词法作用域(与之对应动态作用域)，发生在编译器编译阶段，与代码书写位置相关，编译器要求当前作用域声明变量, 供引擎执行代码阶段查找，编译器_引擎_作用域  扩展阅读，《你不知道JavaScript 上》第一章</div>2019-08-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/cf/3e/5c684022.jpg" width="30px"><span>朱维娜🍍</span> 👍（0） 💬（1）<div>在讲闭包的时候，一会讨论调用闭包的函数是全局变量还是局部变量；一会又讨论闭包本身是局部变量还是全局变量，感觉有点蒙。
另外，我也觉得最后的图里有错误</div>2019-08-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（0） 💬（1）<div>文章中 变量环境中的 outer， 是不是就是当前执行上文中的this 值？</div>2019-08-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b3/26/cc28a05a.jpg" width="30px"><span>悬炫</span> 👍（0） 💬（1）<div>function foo() {
    var myName = &quot; 极客时间 &quot;
    let test1 = 1
    const test2 = 2
    var innerBar = {
        getName:function(){
            console.log(test1)
            return myName
        },
        setName:function(newName){
            myName = newName
        }
    }
    return innerBar
}
var bar = foo()
bar.setName(&quot; 极客邦 &quot;)
bar.getName()
console.log(bar.getName())
闭包的这个例子中，全局执行环境中应该是没有‘myName’这个变量的，我去控制台断点验证过</div>2019-08-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/eb/09/ba5f0135.jpg" width="30px"><span>Chao</span> 👍（0） 💬（1）<div>思考题 引入了如何变更执行上下文的问题。 </div>2019-08-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/e7/d9/83d1346c.jpg" width="30px"><span>Lx</span> 👍（0） 💬（2）<div>闭包的理解是不是应该说内部仍访问外部函数变量？至于外部函数返回一般对象和函数都一样</div>2019-08-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/a1/b6/7fa10b2a.jpg" width="30px"><span>加油</span> 👍（17） 💬（2）<div>只需记住一句话，作用域是由代码中函数声明的位置来决定的</div>2020-02-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/aa/62/78b45741.jpg" width="30px"><span>Morty</span> 👍（10） 💬（0）<div>根据标准，outer 属于词法环境：https:&#47;&#47;262.ecma-international.org&#47;11.0&#47;#sec-lexical-environments

A Lexical Environment consists of an Environment Record and a possibly null reference to an outer Lexical Environment.</div>2021-04-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/af/b3/3486dea2.jpg" width="30px"><span>gigot</span> 👍（8） 💬（15）<div>var a=0;
if(true){
 a = 1;
 function a(){};
 a=21;
 console.log(a)
}
console.log(a)
老师，在 chrome 中，这里的 if 块语句有 a 函数，形成块级作用域了，所以函数 a 的声明被提升到 a = 1 之前；但是接下执行 function a() {} 的时候，全局的 a 的值却改变成 1 了， 导致最终输出为 21 和 1。想问下老师，这里面全局 a 是怎么改变的</div>2019-10-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ba/0f/9789c2cc.jpg" width="30px"><span>Andy Jiang</span> 👍（4） 💬（0）<div>Local–&gt;Closure(foo)–&gt;Global，是不是表示setName执行时的执行上下文中的outer是指向闭包的？闭包中是否有outer指向全局执行上下文？</div>2019-10-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/33/2f/84f7d587.jpg" width="30px"><span>YBB</span> 👍（3） 💬（0）<div>有几个问题，还想请老师解惑：
1. 返回的内部函数在运行时，由于其外部函数的执行上下文已经出栈，其执行上下文中的outer指向何处？
2. 如果函数嵌套产生多个闭包，是否也是类似于作用域链一样的机制，提供内部函数按序在闭包中查找变量？</div>2019-09-18</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJiaWQI7tUfDVmScfCgZIur1B511eHdNsQyjTzQucAOJZrnJfYrEyA1dGOcnZUoqYRzwsbNjlftGhQ/132" width="30px"><span>Geek_21be37</span> 👍（2） 💬（1）<div>我觉得讲的有问题。闭包内部函数词法环境里的外部引用，是在外部函数执行时候创建的。
而不是js全局编译时候产生</div>2021-07-03</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqXKSvfaeicog2Ficx4W3pNeA1KRLOS7iaFy2uoxCDoYpGkGnP6KPGecKia6Dr3MtCkNGpHxAzmTMd0LA/132" width="30px"><span>Geek_East</span> 👍（2） 💬（0）<div>如果从定义拓展来看，可不可以说闭包是在作用域层面的，因为对象本身并不构成作用域，所以最后留的问题，其实是产生了闭包，不过变量是来自于global scope的。</div>2019-12-08</li><br/>
</ul>