在[上篇文章](https://time.geekbang.org/column/article/119046)中，我们讲到了，当一段代码被执行时，JavaScript引擎先会对其进行编译，并创建执行上下文。但是并没有明确说明到底什么样的代码才算符合规范。

那么接下来我们就来明确下，哪些情况下代码才算是“一段”代码，才会在执行之前就进行编译并创建执行上下文。一般说来，有这么三种情况：

1. 当JavaScript执行全局代码的时候，会编译全局代码并创建全局执行上下文，而且在整个页面的生存周期内，全局执行上下文只有一份。
2. 当调用一个函数的时候，函数体内的代码会被编译，并创建函数执行上下文，一般情况下，函数执行结束之后，创建的函数执行上下文会被销毁。
3. 当使用eval函数的时候，eval的代码也会被编译，并创建执行上下文。

好了，又进一步理解了执行上下文，那本节我们就在这基础之上继续深入，一起聊聊**调用栈**。学习调用栈至少有以下三点好处：

1. 可以帮助你了解JavaScript引擎背后的工作原理；
2. 让你有调试JavaScript代码的能力；
3. 帮助你搞定面试，因为面试过程中，调用栈也是出境率非常高的题目。

比如你在写JavaScript代码的时候，有时候可能会遇到栈溢出的错误，如下图所示：

![](https://static001.geekbang.org/resource/image/0c/70/0c9e2c4f7ee8ca59cfa99a6f51510470.png?wh=1142%2A490)

栈溢出的错误

那为什么会出现这种错误呢？这就涉及到了**调用栈**的内容。你应该知道JavaScript中有很多函数，经常会出现在一个函数中调用另外一个函数的情况，**调用栈就是用来管理函数调用关系的一种数据结构**。因此要讲清楚调用栈，你还要先弄明白**函数调用**和**栈结构**。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/8e/fc/6c3dbc46.jpg" width="30px"><span>黄晓杰</span> 👍（37） 💬（2）<div>老师，我有一个疑问，调用栈是后进先出，那么当存在闭包时，某个函数的执行上下文还存在，那么其他函数的出栈是否受影响？</div>2019-09-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/f5/b8/9f165f4b.jpg" width="30px"><span>mfist</span> 👍（20） 💬（12）<div>1. 改成尾递归调用（需要在严格模式下面生效）
function runStack (n, result=100) {
  if (n === 0) return result;
  return runStack( n- 2, result);
}
runStack(50000, 100)
2. 改成循环调用，不使用递归函数，就不存在堆栈溢出</div>2019-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（10） 💬（5）<div>关于调用栈的大小，不用的平台，比如浏览器，nodejs 怎么查看设置的，还是硬编码的？</div>2019-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/30/57/29266196.jpg" width="30px"><span>心飞扬</span> 👍（8） 💬（3）<div>addAll函数中的result并不在变量环境中，而是执行完add后才被放在this中</div>2019-11-14</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/ibZVAmmdAibBeVpUjzwId8ibgRzNk7fkuR5pgVicB5mFSjjmt2eNadlykVLKCyGA0GxGffbhqLsHnhDRgyzxcKUhjg/132" width="30px"><span>pyhhou</span> 👍（8） 💬（1）<div>思考题当中的函数，如果输入参数是正偶数，那么不管数值多大，最后结果都是 100，除此之外，如果输入参数是负数或者是正奇数，甚至说是浮点数，那么使用递归方式调用会导致栈溢出，使用循环方式去实现会导致死循环，如果仅仅是基于当前的输入参数（50000）改写的话：
function runStack (n) {
  return 100;
}
runStack(50000);

当然也可以把递归改成循环的写法，但是要注意的是这时的输入参数仅限定于正偶数，否则会死循环：
function runStack (n) {
  while (n !== 0) {
    n -= 2;
  }

  return 100;
}
runStack(50000);</div>2019-08-23</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKYicHMnUdXqWMiaxqe3L3C20UTh2FgKpOyBwpZVVLYf7Z6gaCLoh6e0bgXQcH162IYVvUAiaXKJ53iaQ/132" width="30px"><span>Claire</span> 👍（7） 💬（1）<div>运用尾递归，其实尾递归也会产生栈溢出问题，但是查资料看，很多编译器已经优化了尾递归，当编译器检测到一个函数调用是尾递归的时候，它就覆盖当前的活动记录而不是在栈中去创建一个新的</div>2019-08-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（7） 💬（5）<div>将递归改成迭代就好了，还可以使用尾递归优化。感觉老师这道题改成斐波那契数列会更好。

function runStack (n) {
  while (n &gt; 0) {
    n -= 2
  }
  return 100
}
runStack(50000)</div>2019-08-22</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqXKSvfaeicog2Ficx4W3pNeA1KRLOS7iaFy2uoxCDoYpGkGnP6KPGecKia6Dr3MtCkNGpHxAzmTMd0LA/132" width="30px"><span>Geek_East</span> 👍（4） 💬（1）<div>执行上下问的本质是一个object吗</div>2019-12-06</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKOASyV1lpdkW6It8WQltNGj9021PTibqOwRUTccaSUEM1GmQThOTIRp9Eu7XNZZFfGGNveLbUSw9Q/132" width="30px"><span>tick</span> 👍（3） 💬（2）<div>老师，我可不可以这样理解，您所说的调用栈并不是严格意义上的栈，因为在addAll中调用add时，add的函数代码还是在全局上下文中，即此时栈中有全局上下文，addAll上下文，但此时还需要去访问栈底的全局上下文中取出add的函数代码，这样是不是不算是严格意义上的栈？</div>2019-08-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/fd/90/ae39017f.jpg" width="30px"><span>爱吃锅巴的沐泡</span> 👍（3） 💬（1）<div>老师，有两个问题：
1、老师在文中写到“首先，从全局执行上下文中，取出 add 函数代码。”，这里是取到函数的引用，还是整个函数代码，函数的存储是怎样的？
2、声明带参的函数并调用的编译过程是怎样的，参数应该是和arguments有关吧，老师能详细说一下编译过程嘛？</div>2019-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/22/7b/f8736786.jpg" width="30px"><span>林展翔</span> 👍（1） 💬（2）<div>老师, 可以问一下, 除了去捕获异常以外,  有没有什么办法能够跳过异常语句去执行剩下的 JS 语句.</div>2019-08-22</li><br/><li><img src="" width="30px"><span>Jim</span> 👍（1） 💬（1）<div>老师，您的执行上下文图里都会有一个变量环境和词法环境，可是为什么词法环境没有东西呢？请问变量环境和词法环境的区别是什么呢？</div>2019-08-22</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLHOZjqhVkWgUrUibLnXkiaFkhJdfWT2BZP3LldE3tArIoHASlhTSp8tiatiamLbQOjKeMcYHkAexoyCg/132" width="30px"><span>江霖</span> 👍（0） 💬（1）<div>
var a = 2
function add(b,c){
  return b+c
}
function addAll(b,c){
var d = 10
result = add(b,c)
return  a+result+d
}
addAll(3,6)
老师这段代码的result是不是应该在全局的context下</div>2019-11-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f0/61/68462a07.jpg" width="30px"><span>无名</span> 👍（0） 💬（2）<div>看文中的代码表达式中大部分结尾都没有加“;”号；JS规范中建议加还是不加“;”号？</div>2019-08-29</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/ExHHyMiauDKhjmy4n8rgA1e3IVRd8vegMAnOFC7u6p9aiaefEJEZKa2Pu5rARLbeNicuz9NFicpF5YXEFf35gNn2vQ/132" width="30px"><span>阿段</span> 👍（0） 💬（1）<div>算法经典思想：循环消除尾递归</div>2019-08-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/c9/ba/f50e9ea4.jpg" width="30px"><span>潘启宝</span> 👍（0） 💬（2）<div>有一个词叫函数尾优化</div>2019-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/4d/04/5e0d3713.jpg" width="30px"><span>李懂</span> 👍（0） 💬（1）<div>想知道js原始类型和引用类型怎么创建的，存储在什么位置？变量对引用类型保存的是内存地址么？</div>2019-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（0） 💬（1）<div>老师你好，如果函数中有闭包，那执行上下文就不会被弹出了，这是一种什么情况？
栈的大小具体是多大，哪里可以看？
老师的图画得很好，用的是什么软件？</div>2019-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/eb/09/ba5f0135.jpg" width="30px"><span>Chao</span> 👍（0） 💬（1）<div>递归是比较好理解的一种方式。 

runstack 目的是否最后能被减为0  return 100。
或者直接改循环  递减 </div>2019-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/c7/1c/3bec7786.jpg" width="30px"><span>徐承银</span> 👍（93） 💬（17）<div>不进栈，就不会栈溢出了。function runStack (n) {
  if (n === 0) return 100;
  return setTimeout(function(){runStack( n- 2)},0);
}
runStack(50000)</div>2019-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/80/7a/02fdf1a2.jpg" width="30px"><span>FreezeSoul</span> 👍（34） 💬（1）<div>评论比文章更丰富系列</div>2020-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/d9/c6/8be8664d.jpg" width="30px"><span>ytd</span> 👍（32） 💬（4）<div>改成循环不会栈溢出了，不过就有可能陷入死循环：
&#47;&#47; 优化
function runStack(n) {
    while (true) {
        if (n === 0) {
            return 100;
        }

        if (n === 1) { &#47;&#47; 防止陷入死循环
            return 200;
        }

        n = n - 2;
    }
}

console.log(runStack(50000));</div>2019-08-22</li><br/><li><img src="" width="30px"><span>Geek_8476da</span> 👍（31） 💬（9）<div>我测试出了栈的深度为12574</div>2019-09-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/df/30/95743ba5.jpg" width="30px"><span>黄榆</span> 👍（17） 💬（0）<div> https:&#47;&#47;kangax.github.io&#47;compat-table&#47;es6&#47;  这个网站可以看到各平台对作为es6特性的尾调用优化的支持情况，表格里面显示：桌面浏览器中只有safari 12 支持尾调用优化。我自己使用safari 12测试，严格模式下运行作者代码能正常得出结果。https:&#47;&#47;node.green&#47;#ESNEXT-strawman--stage-0--syntactic-tail-calls 这个网站则显示，目前版本的node.js不支持尾递归优化</div>2019-09-03</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/uqaRIfRCAhJ6t1z92XYEzbVf8eoPm5Tsu5Zgl0rKdYNFiaGKOOOn79rMClvWGoOJKRJgvrTCGD3ZK4JiaZic72wicrG72I5APGB4/132" width="30px"><span>yetta_xy</span> 👍（16） 💬（5）<div>老师您好，有个疑问。
addAll函数中的result变量没有用var声明，直接赋值的，这个变量应该存在于全局上下文的环境变量对象中吧？</div>2019-09-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/93/4a/de82f373.jpg" width="30px"><span>AICC</span> 👍（7） 💬（0）<div>老师会在什么地方讲解每节内容留下的思考题？比如像这节的尾调用问题，是否存在尾调用优化，至少目前看到的尝试方式在chrome上都会出现栈溢出，有说是v8移除了TCO,即尾调用优化，参考：https:&#47;&#47;stackoverflow.com&#47;questions&#47;42788139&#47;es6-tail-recursion-optimisation-stack-overflow
还有目前google提供的优化方式，但在chrome上目前还不支持，如下
function factorial(n, acc = 1) {
  if (n === 1) return acc;
  return continue factorial(n - 1, acc * n)
}</div>2019-08-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/4b/b9/2449c7b7.jpg" width="30px"><span>‏5102</span> 👍（6） 💬（0）<div>   思考题：基于迭代、模拟栈、异步的解决方案

    &#47;&#47; 使用迭代循环来代替栈
    function runStack(n) {
      while (n !== 0) n -= 2;
      return console.log(100) &amp;&amp; 100;
    }
    &#47;&#47; 使用数组来模拟栈
    function runStack(n) {
      const stack = [n]
      while (n !== 0) {
        n -= 2
        if (n !== 0) {
          stack.push(n)
        } else {
          return console.log(100) &amp;&amp; 100;
        }
      }
    }
    &#47;&#47; 使用异步来分块处理，注意异步队列也有上限，分块粒度不能太细
    function runStack(n, count = 0) {
      if (n === 0) return console.log(100) &amp;&amp; 100;
      if (count &gt; 5000) return setTimeout(runStack, 0, n - 2);
      return runStack(n - 2, count + 1)
    }
    runStack(50000)
    至于尾递归，很多浏览器都不支持，不然可以直接使用尾递归</div>2020-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/9f/1d/ec173090.jpg" width="30px"><span>melon</span> 👍（6） 💬（2）<div>老师没有提函数的入参和返回值，函数的入参和返回值是不是也在函数上下文的变量环境里呢？</div>2019-10-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/83/52/d67f276d.jpg" width="30px"><span>轩爷</span> 👍（6） 💬（0）<div>亲测，Chrome【版本 77.0.3865.75（正式版本）（64 位）】和Firefox【67.0.4 (64 位)】都不支持尾调用优化，只有Safari【版本 12.1.2 (14607.3.9)】支持</div>2019-09-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/cc/8b/0060a75c.jpg" width="30px"><span>tomision</span> 👍（5） 💬（2）<div>加入定时器的方法来把当前任务拆分为其他很多小任务：

function runStackPromise(n) {
  if (n === 0) return Promise.resolve(100)
  return Promise.resolve(n - 2).then(runStackPromise)
}

runStackPromise(500000).then(console.log)</div>2020-02-09</li><br/>
</ul>