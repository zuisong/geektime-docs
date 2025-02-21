你好，我是李兵。

通过前面几节课的学习，我们理解了JavaScript是一门基于对象的语言，它能实现非常多的特性，诸如函数是一等公民、闭包、函数式编程、原型继承等，搞懂了这些特性，我们就可以来打开V8这个黑盒，深入了解它的编译流水线了。

我们知道，当你想执行一段JavaScript代码时，只需要将代码丢给V8虚拟机，V8便会执行并返回给你结果。

其实在执行JavaScript代码之前，V8就已经准备好了代码的运行时环境，这个环境包括了堆空间和栈空间、全局执行上下文、全局作用域、内置的内建函数、宿主环境提供的扩展函数和对象，还有消息循环系统。准备好运行时环境之后，V8才可以执行JavaScript代码，这包括解析源码、生成字节码、解释执行或者编译执行这一系列操作。

![](https://static001.geekbang.org/resource/image/a8/54/a89d747fb614a17e08b1a6b7dce62b54.jpg?wh=2284%2A588)

对运行时环境有足够的了解，能够帮助我们更好地理解V8的执行流程。比如事件循环系统可以让你清楚各种回调函数是怎么被执行的，栈空间可以让你了解函数是怎么被调用的，堆空间和栈空间让你了解为什么要有传值和传引用，等等。

运行时环境涉及到的知识都是非常基础，但又非常容易被忽视的。今天这节课，我们就来分析下这些基础的运行时环境。

![](https://static001.geekbang.org/resource/image/9a/49/9ad5d32bce98aad219c9f73513ac6349.jpg?wh=2284%2A1285)

## 什么是宿主环境？

要聊运行V8的运行时环境，我们不得不聊V8的宿主环境，什么是V8的宿主环境呢？
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTI45zO9GOMqutcVR3NiaicxrKvur4UxStmBkdMYeTMy6HZqpmYLQd6TwGI0mfdp5Upjibr5LiazMDXdPw/132" width="30px"><span>侯不住</span> 👍（28） 💬（5）<div>这个事件循环一直有个点不太明白，事件循环是跑在主线程的，需要不断轮询，它在没有任务的时候是如何保证不卡死的，就像我们随便写一段死循环，cpu都100%了，它是如何做的？</div>2020-04-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ee/44/26ac883e.jpg" width="30px"><span>桃翁</span> 👍（11） 💬（4）<div>老师，有个疑惑希望您能解答，我看您的图：宿主环境和V8的关系 里面堆栈空间是属于 宿主环境的，但是我看很多文章写的都是 堆栈是属于 v8 引擎提供的，不知道哪个是正确的。
我其实比较偏向与是 v8提供的，因为他要进行垃圾回收，如果 v8 来提供可能比较好管理一点。</div>2020-04-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/c0/39/16340f72.jpg" width="30px"><span>zlxag</span> 👍（2） 💬（2）<div>李兵 老师你为什么在文章说。js是基于对象的语言，而不是面向对象语言。”基于“ 和 ‘面向’的的区别是？
面向对象的语言   有唯一性，有状态，且有状态的变化（行为）为对象，这些js都满足。老师的 ”基于“，不知道出于什么考虑</div>2020-04-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/0d/5e/abeeda12.jpg" width="30px"><span>伏枫</span> 👍（1） 💬（1）<div>我有个问题：事件循环和js主执行栈是在同一个线程运行么？如果是一个线程，那么事件循环不会阻碍主执行栈么？</div>2020-04-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ee/44/26ac883e.jpg" width="30px"><span>桃翁</span> 👍（0） 💬（1）<div>老师，执行上下文里的词法环境和变量环境有什么区别呢？后面的课程会讲解吗</div>2020-04-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e6/50/656a0012.jpg" width="30px"><span>王楚然</span> 👍（33） 💬（5）<div>思考题：
1. 作用域是静态的，函数定义的时候就已经确定了。
2. 执行上下文是动态的，调用函数时候创建，结束后还会释放。
不知这样理解对不对</div>2020-04-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/bf/aa/32a6449c.jpg" width="30px"><span>蒋悦</span> 👍（21） 💬（1）<div>作用域是逻辑概念，只要函数确定，作用域就确定了。执行上下文其实就是“栈帧”。作用域和子作用域有从属关系，是静态的。执行上下文是函数的调用关系，是动态的。</div>2020-04-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/fd/90/ae39017f.jpg" width="30px"><span>爱吃锅巴的沐泡</span> 👍（8） 💬（6）<div>老师您好，对于ES5标准文档中规定，
         执行环境包括：词法环境、变量环境、this绑定。
         其中执行环境的词法环境和变量环境组件始终为词法环境对象。当创建一个执行环境时，其词法环境组件和变量环境组件最初是同一个值。在该执行环境相关联的代码的执行过程中，变量环境组件永远不变，而词法环境组件有可能改变。

问题1：变量环境组件永远不变，而词法环境组件有可能改变。 
          这里您给出的解释是说词法环境里会有块级作用域的进入和退出，但这是ES5的规范呀，还没有作用域的概念呀，这里不解？
          变量环境组件为什么永久不变？

问题2：创建执行环境时，变量环境和词法环境最初是同一个值，想知道这个值具体是指什么值？

问题3：我理解的ES5中 变量环境中存储的是提升的变量和函数声明(都是类似var xx=undefined; function funname(){})，所以变量环境是不变的，在执行过程中变量的变化是在词法环境中体现的，词法环境管理着静态作用域的。 到了ES6，有了let和const，是不是就把原来词法环境中变化的变量转移到了变量环境中，把let和const的变化放到了现在的词法环境中。

希望老师能举个例子或者画个图，详细分析一下在ES5中变量环境和词法环境中变量的变化？
ES5和ES6的执行环境的区别是啥？

问题有点多，但是网上写的和规范内容都不一样，感觉不靠谱，请老师解答！</div>2020-04-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（7） 💬（1）<div>作用域是依附执行上下文的，如果执行上下文销毁，那么对应的作用域也会销毁（这里闭包形成的作用域是特例）</div>2020-04-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/6c/e7/c8645b9c.jpg" width="30px"><span>bright</span> 👍（7） 💬（0）<div>执行上下文是用来维护执行当前代码所需要的变量声明、this 指向等。作用域是规定了如何查找变量，也就是确定当前执行代码对变量的访问权限。js采用的是词法作用域，函数的作用域在函数定义的时候就决定了。可以把作用域看作执行上下文中代码对变量的访问权限。</div>2020-04-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/59/ea/38c063d5.jpg" width="30px"><span>OnE</span> 👍（4） 💬（0）<div>V8运行时环境里的栈空间，在操作系统层面，到底是属于进程堆，还是进程栈呢？如果是后者，背后的实现机理是什么样的呢？</div>2020-04-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/d1/81/89ba9d81.jpg" width="30px"><span>大力</span> 👍（3） 💬（9）<div>老师，有个地方我有个疑问：

文中说，“全局执行上下文在 V8 的生存周期内是不会被销毁的，它会一直保存在堆中”。

而文中又另外说到，“在函数调用过程中，涉及到上下文相关的内容都会存放在栈上”。

那究竟全局上下文是放在堆上还是栈上呢？

我的理解是应该都放在栈上，因为总不会函数执行上下文放在栈上，而全局执行上下文放在堆上吧？

还望指正。</div>2020-04-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/92/e4/abb7bfe3.jpg" width="30px"><span>TerryGoForIt</span> 👍（1） 💬（3）<div>老师，我对这个堆栈空间到底是谁怎么分配的，还是不理解。首先v8自身肯定是没有堆栈的，它需要宿主，而浏览器就是宿主。浏览器能分配堆栈吗？浏览器不也是个进程吗？它的堆栈不是操作系统给分配的吗？那是说在操作系统给浏览器分配的堆栈中，浏览器匀了一部分给v8吗？</div>2023-05-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/9e/a4/664a95bb.jpg" width="30px"><span>Chlike</span> 👍（1） 💬（0）<div>作用域是变量的可访问区域，在词法分析阶段已经确定了。
执行上下文会在函数调用时生成，其中的变量环境和词法环境中的可访问变量是依据函数定义时的作用域确定的。
我认为两者的关系是 在生成执行上下文时需要作用域来确定可访问哪些变量</div>2022-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/0f/ba/a2531cf0.jpg" width="30px"><span>彭越</span> 👍（1） 💬（0）<div>词法和文法决定了变量作用域，可以说是静态的，在运行前就决定了。执行上下文则是动态的，运行期创建的，根据JavaScript代码创建执行上下文，包含了VO、Scope chain、thisValue这些根据js代码生成的运行期信息。到了function的执行上下文，则会生成AO，包含了function内部变量、arguments等信息。</div>2020-04-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/bc/25/1c92a90c.jpg" width="30px"><span>tt</span> 👍（1） 💬（0）<div>我认为执行上下文是作用域的实现。</div>2020-04-05</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eoaxy8ibvXITdMcXFfd5O5E7Epq8MG5z1OBhO7MQXTfbcpA0fpcsIxkCHyUZ5ZSrj3spZpAQxEC9GA/132" width="30px"><span>非洲大地我最凶</span> 👍（1） 💬（2）<div>而栈空间是连续的，所以堆空间中的查找速度非常快, 此处应该是栈的查找速度快吧</div>2020-04-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡</div>2024-06-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/4f/d8/2ca8d028.jpg" width="30px"><span>Ivanjzhang</span> 👍（0） 💬（0）<div>老师，一个JavaScript脚本存在同步代码和异步代码，异步代码的回调在主线程的循环里面，那同步代码跑在主线程的哪里呢？</div>2023-09-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/56/08/bd75f114.jpg" width="30px"><span>WGH丶</span> 👍（0） 💬（0）<div>通俗易懂，老师牛逼</div>2023-09-11</li><br/><li><img src="" width="30px"><span>Geek_be4b37</span> 👍（0） 💬（0）<div>这里的执行上下文是否可以理解成栈帧，每次调用一个方法压入一个栈帧(执行上下文)，执行完毕抛出当前栈帧，根据返回值地址，将结果返回给上级栈帧(执行上下文)</div>2023-08-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/7d/67/791d0f5e.jpg" width="30px"><span>清波</span> 👍（0） 💬（0）<div>老师，js执行过程中的系统调用栈，和事件循环系统是包含关系还是并列关系呀？</div>2021-09-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/5b/58/eca3578b.jpg" width="30px"><span>梵鸿</span> 👍（0） 💬（0）<div>执行上下文中包含有至少一个作用域，执行上下文（全局执行上下文除外）也可以被包含在其它作用域内。
作用域为执行上下文提供了变量存储和查找的规则。</div>2021-06-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/e8/43/f9c0faed.jpg" width="30px"><span>小童</span> 👍（0） 💬（0）<div>老师，看到一句话。堆空间和栈空间让你了解为什么要有传值和传引用？这个是为什么，是因为栈空间内存连续而且大小比堆空间小吗？</div>2021-04-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/eb/ea/7a0d0843.jpg" width="30px"><span>迷途羔羊</span> 👍（0） 💬（0）<div>执行上下文: 是词法环境，变量对象，this等函数启动的需要的一些条件，应该可以类比为一个实体，存储在堆栈中
作用域: 管理着变量访问的规则，更类似于一种规定</div>2020-12-23</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/bVxkKaNAduU0WibOMkFIoqV3DzpI8xPL376fn2jBnM3AwWbSGj5zNqTI0D4KyvQmr07OaPD8gWrHM3PxKCoENlA/132" width="30px"><span>Geek_c62c77</span> 👍（0） 💬（0）<div>作用域链是当前执行上下文和上层执行上下文的变量一系列关系</div>2020-11-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/a8/b4/6a818036.jpg" width="30px"><span>zhenzhenChange</span> 👍（0） 💬（0）<div>老师，我有两个问题想请教一下您：
1.本文说到【如果主线程正在执行一个任务，这时候又来了一个新任务，比如 V8 正在操作 DOM，这时候浏览器的[网络线程]完成了一个页面下载的任务】。
这里的网络线程是渲染进程中的线程还是网络进程中的线程呢？
所有的网络请求都是在网络进程里处理的嘛？
2.关于数据存储，假如Number类型或String类型，字节很长很长很大，也是存储在栈中吗？据说Symbol和BigInt类型的数据是存储在堆中的。查看谷歌控制台的堆内存中也发现又Number类型的数据，这个存储的形式应该是根据数据的大小而动态决定的吧？

另：
最后总结那里【而栈空间是连续的，所以[堆]空间中的查找速度非常快】，这里应该是[栈]空间中的查找速度吧？</div>2020-10-30</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eoeOax1CZKbFicWib6Eicl7WHVpFG269qQCes0wbiawJsqPs45B8sAgF7eGyjhJJkibXTjtApNicnmicPh1g/132" width="30px"><span>rookie</span> 👍（0） 💬（0）<div>老师，我有个疑问，关于全局变量和函数内部的局部变量的选取。对于同一个变量，我可以将它作为局部变量，然后当成调用函数的参数进行传递使用。我也可以将它作为全局变量，这样所以函数都能直接访问并操纵它，可以省去函数调用中的参数。这两种方式应该如何选取呢？</div>2020-09-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/cd/b8/14597b01.jpg" width="30px"><span>西门吹雪</span> 👍（0） 💬（0）<div>总结的很好啊</div>2020-06-06</li><br/><li><img src="" width="30px"><span>Geek_177f82</span> 👍（0） 💬（0）<div>我有个疑问，1，队列中任务的极限是多少？2，如果列队中任务足够多的时候，消息队列这个时候是怎么处理的？还可以添加到队列，还是？</div>2020-04-09</li><br/>
</ul>