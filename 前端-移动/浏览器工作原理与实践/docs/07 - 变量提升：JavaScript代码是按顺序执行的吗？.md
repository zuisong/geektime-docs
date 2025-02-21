讲解完宏观视角下的浏览器后，从这篇文章开始，我们就进入下一个新的模块了，这里我会对JavaScript执行原理做深入介绍。

今天在该模块的第一篇文章，我们主要讲解**执行上下文**相关的内容。那为什么先讲执行上下文呢？它这么重要吗？可以这么说，**只有理解了JavaScrip的执行上下文，你才能更好地理解JavaScript语言本身**，比如变量提升、作用域和闭包等。不仅如此，理解执行上下文和调用栈的概念还能助你成为一名更合格的前端开发者。

不过由于我们专栏不是专门讲JavaScript语言的，所以我并不会对JavaScript语法本身做过多介绍。本文主要是从JavaScript的顺序执行讲起，然后**一步步带你了解JavaScript是怎么运行的**。

接下来咱们先看段代码，你觉得下面这段代码输出的结果是什么？

```
showName()
console.log(myname)
var myname = '极客时间'
function showName() {
    console.log('函数showName被执行');
}
```

使用过JavaScript开发的程序员应该都知道，JavaScript是按顺序执行的。若按照这个逻辑来理解的话，那么：

- 当执行到第1行的时候，由于函数showName还没有定义，所以执行应该会报错；
- 同样执行第2行的时候，由于变量myname也未定义，所以同样也会报错。

然而实际执行结果却并非如此， 如下图：
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/f5/b8/9f165f4b.jpg" width="30px"><span>mfist</span> 👍（204） 💬（11）<div>输出1

编译阶段:
var showName
function showName(){console.log(1)}

执行阶段:
showName()&#47;&#47;输出1
showName=function(){console.log(2)}
&#47;&#47;如果后面再有showName执行的话，就输出2因为这时候函数引用已经变了</div>2019-08-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/84/5f/389cb294.jpg" width="30px"><span>lane</span> 👍（147） 💬（10）<div>老师，head头部引入的js文件，也是先编译的吗？</div>2019-08-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/fd/90/ae39017f.jpg" width="30px"><span>爱吃锅巴的沐泡</span> 👍（106） 💬（6）<div>答案：1

编译阶段:
var showName = undefined
function showName() {console.log(1)}

执行阶段:
showName()        &#47;&#47;输出1
showName = function() {console.log(2)}

分析：首先遇到声明的变量showName，并在变量环境中存一个showName属性，赋值为undefined; 又遇到声明的函数，也存一个showName的属性，但是发现之前有这个属性了，就将其覆盖掉，并指向堆中的声明的这个函数地址。所以在执行阶段调用showName()会输出1;执行showName = function() {console.log(2)}这句话是把堆中的另一个函数地址赋值给了showName属性，也就改变了其属性值，所以如果再调用showName()，那个会输出2. 这是不是体现了函数是对象，函数名是指针。

疑问：如果同名的变量和函数名，变量环境中是分别保存还是如何处理的？

</div>2019-08-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8b/1d/8756d3bf.jpg" width="30px"><span>he</span> 👍（81） 💬（10）<div>函数提升要比变量提升的优先级要高一些，且不会被变量声明覆盖，但是会被变量赋值之后覆盖。</div>2019-08-21</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/cEiadV2uaZmhwu19Xcft9Qg0MsjmFlwzYbqbBJSwgKrmwOSaUZ6OibQZAEolxvbUH4M6NXAkC9NprpBXl4MO1iavQ/132" width="30px"><span>shezhenbiao</span> 👍（62） 💬（6）<div>老师好，请教您一个问题。
debugger;
(function(){
    console.log(g)
    if(true){
        console.log(&#39;hello world&#39;);
        function g(){ return true; }
    }
})();
这个函数步进调试时，发现打印g时值是undefined而不是提示not defined，说明if中g函数确实是提升了，但是为何不是g()而是undefined？然后走完function g(){ return true; }这一步后 console.log(g)中的g才变为g()。这里条件声明函数的变量提升有点搞不明白。</div>2019-08-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f1/15/8fcf8038.jpg" width="30px"><span>William</span> 👍（40） 💬（11）<div>老师，如果把两个函数调换个儿。那么先声明function，然后把 showName 赋值 undefined，undefined不会覆盖函数声明。这是为什么？

console.log(showName.toString())
function showName() {
    console.log(1)
}
var showName = function() {
  console.log(2)
}

打印的是函数体，而非undefined，证明 undefined 不会覆盖函数声明！！</div>2019-08-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/22/7b/f8736786.jpg" width="30px"><span>林展翔</span> 👍（29） 💬（1）<div>老师，可以请教下吗，在编译完成之后是单单生成了字节码，再到执行过程中变成对应平台的机器码？ 还是编译过程已经生成了对应平台的机器码， 执行阶段就直接去执行相应的机器码？</div>2019-08-20</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqXKSvfaeicog2Ficx4W3pNeA1KRLOS7iaFy2uoxCDoYpGkGnP6KPGecKia6Dr3MtCkNGpHxAzmTMd0LA/132" width="30px"><span>Geek_East</span> 👍（25） 💬（3）<div>lexical scope发生在编译阶段，会产生变量提升的效果；
JavaScript的Dynamic Scope发生在执行阶段，会产生this binding, prototype chaining search的过程；
变量提升只提升声明(left hand）不提升赋值(right hand)
function的声明主要有: function declaration, function expression
其中function declaration会将方法体也提升，而function expression同变量提升一样，只会提升声明；
变量提升在有let或者const的block中会出现Temporal Dead Zone Error, 效果好似没有提升；
另外要注意block内部的var变量能够穿透block提升到global scope.

更多JS请了解：
https:&#47;&#47;geekeast.github.io&#47;jsscope.html</div>2019-11-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/63/5a/4ec96cfe.jpg" width="30px"><span>林高鸿</span> 👍（25） 💬（1）<div>老师，ES6 后不用 var，所以可否理解 Hoisting 为“权宜之计&#47;设计失误”呢？</div>2019-08-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/33/2f/84f7d587.jpg" width="30px"><span>YBB</span> 👍（23） 💬（4）<div>老师我想问下，一段javascript代码进入编译阶段是会对函数体内的代码也进行编译，还是只是将函数体的代码存储在堆，在执行中遇到该函数再去编译？</div>2019-08-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/14/b3/b6e1817a.jpg" width="30px"><span>趁你还年轻233</span> 👍（13） 💬（3）<div>var showName;
function showName() {
    console.log(1)
}
showName();
showName = function() {
    console.log(2)
};

这样声明没有问题，可以正常输出1。

为什么下面的代码会报错呢：Uncaught TypeError: showName is not a function

var showName = undefined;
function showName() {
    console.log(1)
}
showName();
showName = function() {
    console.log(2)
};</div>2019-11-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/22/7b/f8736786.jpg" width="30px"><span>林展翔</span> 👍（7） 💬（4）<div>x = 10 + 20;
console.log(x);
若对 x 未进行定义, 直接赋值, 可以输出
若按照课程理解并假设
编译阶段会有一个
x = undefine
但是
console.log(x);
x = 10 + 20;
console.log(x);
会出现报错  x is not defined
在这个地方 我的理解有什么问题吗 还是说 原来就没有 x = undefine 操作, 只是在 x = 10 + 20; 给 x 赋值了一下.</div>2019-08-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e9/e9/1f95e422.jpg" width="30px"><span>杨陆伟</span> 👍（3） 💬（3）<div>showName()
function showName(){
    console.log(1)
}
var showName=function(){
    console.log(2)
}
showName()

第二个showName打印为2，为什么这个showName找的是变量而不是函数，或者此时变量环境中已经没有了showName函数，只有showName变量？谢谢</div>2019-08-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/c4/f5/f64e30d8.jpg" width="30px"><span>Lester</span> 👍（2） 💬（1）<div>如果变量和函数同名，那么在编译阶段，变量的声明会被忽略，执行的时候还是后面的是什么就是什么，而不会因为同名，就一定是函数。</div>2019-11-13</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/AcJM5WNhE05rzaVzeL9ia4QSnibd0ibbKNdIbySj2ibhj2xFRHibdhOX9fBEB5HMS1bbOt0tXcxwKur2gPdVaZpcIZw/132" width="30px"><span>子非鱼</span> 👍（2） 💬（1）<div>老师我有个问题，正常情况domcontentloaded事件是在浏览器下载并解析完html才触发，如果有内嵌外部js文件，也要等到js加载并执行完才触发。但如果页面是被二次访问并且html和引入的外部js都命中了缓存，则是否也要等到js被完全执行才触发呢？</div>2019-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/0e/8b/036e9f7c.jpg" width="30px"><span>iven～zf</span> 👍（1） 💬（1）<div>老师，您的图片是用什么画图工具了。感觉好友爱。</div>2019-09-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/8e/e4/f126ef1b.jpg" width="30px"><span>芬兰湖边小画匠</span> 👍（1） 💬（1）<div>9.10　刚好看到这里。老师，节日快乐。祝好</div>2019-09-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c0/5c/10111544.jpg" width="30px"><span>张峰</span> 👍（1） 💬（1）<div>showName函数的编译是在什么时候呢</div>2019-08-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/da/67/73a0c754.jpg" width="30px"><span>gallifrey</span> 👍（1） 💬（1）<div>一、
showName()
var showName = function() {
    console.log(2)
}
function showName() {
    console.log(1)
}
编译阶段，第一个showName存入变量环境中，自动赋值undefined
第二个showName函数体也存入了变量环境中，但是是一个完整的函数声明赋值
执行阶段，Javacript引擎从变量环境中查找到showName函数体直接执行
输出结果：1</div>2019-08-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/da/67/73a0c754.jpg" width="30px"><span>gallifrey</span> 👍（1） 💬（3）<div>二、
showName()
function showName(){
    console.log(1)
}
var showName=function(){
    console.log(2)
}
showName()
编译阶段，showName函数体存入变量环境
showName变量存入变量环境，赋值undefined
执行阶段，第一个showName()查找到函数体直接执行
输出结果：1
执行到第二个showName()时，showName变量已经赋值了function(){console.log(2)}
输出结果：2</div>2019-08-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/44/0e/ce14b7d3.jpg" width="30px"><span>-_-|||</span> 👍（0） 💬（2）<div>&#39;先是生成字节码，然后解释器可以直接执行字节码，输出结果。&#39;我记忆中V8引擎好像比以前的更快一些，直接二进制</div>2019-12-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/7d/74/791d0f5e.jpg" width="30px"><span>断了线的风筝</span> 👍（0） 💬（1）<div>chrome浏览器如果出现6个请求pending,第7个请求会pending吗</div>2019-09-17</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKOASyV1lpdkW6It8WQltNGj9021PTibqOwRUTccaSUEM1GmQThOTIRp9Eu7XNZZFfGGNveLbUSw9Q/132" width="30px"><span>tick</span> 👍（0） 💬（2）<div>变量环境中的同名函数替换是怎么替换呢？函数定义保存在执行堆中，那么函数定义怎么替换呀，会不会出现溢出什么的，还是说只是指向执行堆的指针值换掉，那么是不是在执行堆中就有两份函数定义呢？老师，这个能详细说吗？</div>2019-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/8c/d5/398b31fe.jpg" width="30px"><span>木棉</span> 👍（0） 💬（1）<div>showName()
function showName(){
    console.log(1)
}
var showName=function(){
    console.log(2)
}
showName()
首先：变量提升：var showName = undefined;
                        function showName(){console.log(1)}
其次：执行阶段：变量showName被赋值成为一个函数，这个函数会把变量环境里的那个showName覆盖掉，所以第二次showName()执行的时候就变成了2。
老师，这样理解对吗？
我的疑问是现在变量环境里只剩下了showName函数吗？
             </div>2019-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（0） 💬（1）<div>老师，想查看编译阶段生成的字节码，有什么工具可以查看吗？</div>2019-08-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/c3/ce/4e78783b.jpg" width="30px"><span>王家麦子</span> 👍（0） 💬（3）<div>请教老师，前端是否可以自己实现插件，占用独立的浏览器进程呢？用什么方式实现？</div>2019-08-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/22/7b/f8736786.jpg" width="30px"><span>林展翔</span> 👍（0） 💬（1）<div>老师可以问几个问题吗:
1. 编译过程中, 会生成对应的执行上下文以及执行代码, 若在执行代码中对变量的操作是会对执行上下文进行修改吗?
2. 编译与执行 JS 过程中可能会存在需要优化的地方, 那这个优化过程是处于执行之前还是在执行之后?</div>2019-08-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（0） 💬（1）<div>在ES6中，let const 声明变量，不允许在声明前使用，会形成暂时性死区。</div>2019-08-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（0） 💬（1）<div>老师这一节讲得很好，虽然是很基础的内容，但是文中的配图确实很不错。
指出老师朗读的一个问题，就是undefined的发音。
跟着老师一起精进。</div>2019-08-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/c4/4f/fdd51040.jpg" width="30px"><span>小锅锅</span> 👍（0） 💬（2）<div>                showName()&#47;&#47;输出1
		var showName = function() {
		    console.log(2)
		}
		function showName() {
		    console.log(1)
		}
		showName();&#47;&#47;输出2
这里第二个函数体为什么不会覆盖第一个由变量赋值的函数呢？</div>2019-08-20</li><br/>
</ul>