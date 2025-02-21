在[上篇文章](https://time.geekbang.org/column/article/136895)中，我们介绍了怎么使用Promise来实现回调操作，使用Promise能很好地解决回调地狱的问题，但是这种方式充满了Promise的then()方法，如果处理流程比较复杂的话，那么整段代码将充斥着then，语义化不明显，代码不能很好地表示执行流程。

比如下面这样一个实际的使用场景：我先请求极客邦的内容，等返回信息之后，我再请求极客邦的另外一个资源。下面代码展示的是使用fetch来实现这样的需求，fetch被定义在window对象中，可以用它来发起对远程资源的请求，该方法返回的是一个Promise对象，这和我们上篇文章中讲的XFetch很像，只不过fetch是浏览器原生支持的，并有没利用XMLHttpRequest来封装。

```
fetch('https://www.geekbang.org')
      .then((response) => {
          console.log(response)
          return fetch('https://www.geekbang.org/test')
      }).then((response) => {
          console.log(response)
      }).catch((error) => {
          console.log(error)
      })
```

从这段Promise代码可以看出来，使用promise.then也是相当复杂，虽然整个请求流程已经线性化了，但是代码里面包含了大量的then函数，使得代码依然不是太容易阅读。**基于这个原因，ES7 引入了async/await，这是JavaScript异步编程的一个重大改进，提供了在不阻塞主线程的情况下使用同步代码实现异步访问资源的能力，并且使得代码逻辑更加清晰**。你可以参考下面这段代码：
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/f5/b8/9f165f4b.jpg" width="30px"><span>mfist</span> 👍（118） 💬（20）<div>1. 首先在主协程中初始化异步函数foo和bar，碰到console.log打印script start；
2. 解析到setTimeout，初始化一个Timer，创建一个新的task
3. 执行bar函数，将控制权交给协程，输出bar start，碰到await，执行foo，输出foo，创建一个 Promise返回给主协程
4. 将返回的promise添加到微任务队列，向下执行 new Promise，输出 promise executor，返回resolve 添加到微任务队列
5. 输出script end
6. 当前task结束之前检查微任务队列，执行第一个微任务，将控制器交给协程输出bar end
7. 执行第二个微任务 输出 promise then
8. 当前任务执行完毕进入下一个任务，输出setTimeout</div>2019-09-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4e/94/0b22b6a2.jpg" width="30px"><span>Luke</span> 👍（39） 💬（2）<div>generator 函数是如何暂停执行程序的？
答案是通过协程来控制程序执行。
generator 函数是一个生成器，执行它会返回一个迭代器，这个迭代器同时也是一个协程。一个线程中可以有多个协程，但是同时只能有一个协程在执行。线程的执行是在内核态，是由操作系统来控制；协程的执行是在用户态，是完全由程序来进行控制，通过调用生成器的next()方法可以让该协程执行，通过yield关键字可以让该协程暂停，交出主线程控制权，通过return 关键字可以让该协程结束。协程切换是在用户态执行，而线程切换时需要从用户态切换到内核态，在内核态进行调度，协程相对于线程来说更加轻量、高效。
async function实现原理？ 
async function 是通过 promise + generator 来实现的。generator 是通过协程来控制程序调度的。
​在协程中执行异步任务时，先用promise封装该异步任务，如果异步任务完成，会将其结果放入微任务队列中，然后通过yield 让出主线程执行权，继续执行主线程js，主线程js执行完毕后，会去扫描微任务队列，如果有任务则取出任务进行执行，这时通过调用迭代器的next(result)方法，并传入任务执行结果result，将主线程执行权转交给该协程继续执行，并且将result赋值给yield 表达式左边的变量，从而以同步的方式实现了异步编程。
所以说到底async function 还是通过协程+微任务+浏览器事件循环机制来实现的。</div>2019-09-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/18/77/d665f258.jpg" width="30px"><span>EmilyLucky</span> 👍（34） 💬（6）<div>1.首先执行console.log(&#39;script start&#39;);打印出script start
2.接着遇到定时器，创建一个新任务，放在延迟队列中
3.紧接着执行bar函数，由于bar函数被async标记的，所以进入该函数时，JS引擎会保存当前调用栈等信息，然后执行bar函数中的console.log(&#39;bar start&#39;);语句，打印bar start。
4.接下来执行到bar函数中的await foo();语句，执行foo函数，也由于foo函数被async标记的，所以进入该函数时，JS引擎会保存当前调用栈等信息，然后执行foo函数中的console.log(&#39;foo&#39;);语句，打印foo。
5.执行到await foo()时，会默认创建一个Promise对象
6.在创建Promise对象过程中，调用了resolve()函数，且JS引擎将该任务交给微任务队列
7.然后JS引擎会暂停当前协程的执行，将主线程的控制权交给父协程，同时将创建的Promise对象返回给父协程
8.主线程的控制权交给父协程后，父协程就调用该Promise对象的then()方法监控该Promise对象的状态改变
9.接下来继续父协程的流程，执行new Promise()，打印输出promise executor，其中调用了 resolve 函数，JS引擎将该任务添加到微任务队列队尾
10.继续执行父协程上的流程，执行console.log(&#39;script end&#39;);，打印出来script end
11.随后父协程将执行结束，在结束前，会进入微任务检查点，然后执行微任务队列，微任务队列中有两个微任务等待执行，先执行第一个微任务，触发第一个promise.then()中的回调函数，将主线程的控制权交给bar函数的协程，bar函数的协程激活后，继续执行后续语句，执行 console.log(&#39;bar end&#39;);，打印输出bar end
12.bar函数协程执行完成后，执行微任务队列中的第二个微任务，触发第二个promise.then()中的回调函数，该回调函数被激活后，执行console.log(&#39;promise then&#39;);，打印输出promise then
13.执行完之后，将控制权归还给主线程，当前任务执行完毕，取出延迟队列中的任务，执行console.log(&#39;setTimeout&#39;);，打印输出setTimeout。

故：最终输出顺序是：script start =&gt; bar start =&gt; foo =&gt; promise executor =&gt; script end =&gt; bar end =&gt; promise then =&gt; setTimeout
</div>2020-05-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（10） 💬（0）<div>感谢老师的分享，懂了，生成器+Promise+自动迭代器=async&#47;await。</div>2019-09-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/ae/a0/707350ef.jpg" width="30px"><span>穿秋裤的男孩</span> 👍（9） 💬（8）<div>以前一直以为promise.then就是添加微任务，原来真的的微任务是promise.resolve&#47;reject。then函数只是resolve&#47;reject执行的副产品</div>2020-04-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/39/08/09055b47.jpg" width="30px"><span>淡</span> 👍（8） 💬（6）<div>你好，这还有个小疑问：
就是foo函数被标记上async后，会隐式生成一个promise，然后在await foo（）处，await本身又会生成一个promise_，这两个promise是什么关系？</div>2019-09-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/82/a4/a92c6eca.jpg" width="30px"><span>墨灵</span> 👍（7） 💬（0）<div>直到现在才构建起一个比较完整的异步编程范式的体系，真是深入浅出。</div>2020-03-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f9/c0/20b4a205.jpg" width="30px"><span>啊哈哈</span> 👍（4） 💬（2）<div>那也就是说，await之后的行为，全部作为promise.then()的微任务加入进微任务队列中了。最后在本轮宏任务执行完成后才执行当前宏任务下的微任务队列。</div>2021-01-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/fe/8e/895f05a2.jpg" width="30px"><span>A LETTER</span> 👍（2） 💬（0）<div>awiat会向父协程传递创建的promise_,并执行resolve(result)，该方法会被放入微任务队列中执行，之后在赋值前通过yield跳出该协程，转到父协程，然后父协程通过调用promise_.then方法来监听这个promise的变化，当父协程执行结束之前，到达检查点，去执行微任务队列时，执行到之前注册的resolve(result)时，会调用之前then注册的回调函数，在该回调函数中通过next(result)来进入子协程，并将result的值，赋值给await等式左边的变量，然后继续执行该子协程的代码，就相当于在之前的then中注册的回调函数里执行一样，实现了同步的方式来进行异步操作。</div>2021-10-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/46/ea/b86667b8.jpg" width="30px"><span>王玄</span> 👍（2） 💬（0）<div>老师 可以否按照mfist这种流程详细讲解一下练习题</div>2021-04-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/04/13/84d35588.jpg" width="30px"><span>张萌</span> 👍（2） 💬（0）<div>最新的 node 14 已经支持顶层 await 了</div>2020-05-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/94/45/7ea3dd47.jpg" width="30px"><span>开开之之</span> 👍（1） 💬（0）<div>首先执行console.log(&#39;script start&#39;)
然后执行setTimeout，由于setTimeout是宏任务，因此会把它的回调函数放入消息队列中。
执行bar(): 启动bar协程，这个时候会执行 console.log(&#39;bar start&#39;)。
然后执行await foo()，这个时候会执行console.log(&#39;foo&#39;), 并且创建一个promise对象, 把resolve放入微任务队列中。
new Promise((resolve, reject()) =&gt; {
    resolve()
})
&#47;&#47; 在主协程中创建一个promise.then函数，用于把协程控制权返回给bar协程
promise._then(() =&gt; {
   &#47;&#47; 启动foo协程
})
执行new Promise，执行 console.log(&#39;promise executor&#39;)，并把resolve()放入微任务队列中
执行console.log(&#39;script end&#39;)
这个时候主函数执行完毕，开始执行微任务，由于先进先出，会先执行bar协程创建的promise对象的resolve任务，因此下一步是触发bar协程，继续执行完 console.log(&#39;bar end&#39;)。
继续执行微任务队列，执行下一个promise的resolve函数，并触发执行其then函数
console.log(&#39;promise then&#39;)
微任务执行完毕，继续执行下一个宏任务 console.log(&#39;setTimeout&#39;)</div>2022-10-15</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/MYShyjtRtib2GIQiaK4hV3ZP9pQ1qiaS74DA4K4YHY4SIiaFDfsCKgiaMWwm9zFsSn3bt5pawp5Kdn5MWgiaw5909nug/132" width="30px"><span>Geek_aa1c31</span> 👍（1） 💬（0）<div>
async function foo() {
    console.log(1)
    let a = await 100
    console.log(a)
    console.log(2)
}
console.log(0)
foo()
console.log(3)
相当于:
function* foo() {
  console.log(1);
  const a = yield new Promise(resolve =&gt; {
    resolve(100);
  });
  console.log(a);
  console.log(2);
}
console.log(0);
const gen = foo();
gen.next().value.then(v =&gt; {
  gen.next(v);
});
console.log(3);

=================================

async function foo() {
    console.log(&#39;foo&#39;)
}
async function bar() {
    console.log(&#39;bar start&#39;)
    await foo()
    console.log(&#39;bar end&#39;)
}
console.log(&#39;script start&#39;)
setTimeout(function () {
    console.log(&#39;setTimeout&#39;)
}, 0)
bar();
new Promise(function (resolve) {
    console.log(&#39;promise executor&#39;)
    resolve();
}).then(function () {
    console.log(&#39;promise then&#39;)
})
console.log(&#39;script end&#39;)
相当于:
function* foo() {
  console.log(&#39;foo&#39;);
}

function* bar() {
  console.log(&#39;bar start&#39;);
  yield new Promise(resolve =&gt; {
    resolve(foo().next());
  });
  console.log(&#39;bar end&#39;);
}
console.log(&#39;script start&#39;);

setTimeout(() =&gt; {
  console.log(&#39;setTimeout&#39;);
}, 0);

const genBar = bar();
genBar.next().value.then(v =&gt; {
  genBar.next(v);
});

new Promise(resolve =&gt; {
  console.log(&#39;promise executor&#39;);
  resolve();
}).then(() =&gt; {
  console.log(&#39;promise then&#39;);
});
console.log(&#39;script end&#39;);</div>2022-02-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/6c/d4/85ef1463.jpg" width="30px"><span>路漫漫</span> 👍（1） 💬（0）<div>好文，看了许久和配合es6的文档才看明白的，收获极大</div>2022-02-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/f7/e5/b290e605.jpg" width="30px"><span>AIGC Weekly 周报</span> 👍（1） 💬（0）<div>具体步骤如下，并不严谨，欢迎指教：
1. 输出 “script start”。
2. 执行 setTimeout，将其加入到定时消息队列(宏任务)。
3. 执行 bar()，以协程的角度，创建一个 bar 协程，首先输出 “bar start”，执行到 await 后，调用 foo (创建一个foo协程)，输出 “ foo”，并新建一个Promise实例传递给父协程，父协程将其添加到当前宏任务的微任务队列(微任务队列元素+1)。
4. 执行新建 Promise 实例，输出 “promise executor”，执行 resolve() 添加到微任务队列中(微任务队列元素+1)。
5. 输出 “script end”。
6. 当前宏任务执行完毕，开始检查微任务队列，按照添加的先后顺序，首先输出 “bar end”，再次输出 “promise then”。
7. 消息队列中的任务在下一次事件循环中执行，输出 “ setTimeout”。</div>2021-04-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/66/dc/fdffbc96.jpg" width="30px"><span>🍃</span> 👍（1） 💬（8）<div>如果已经到了检查点，await后面的内容还没有resolve，会出现什么情况呢</div>2021-03-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4c/4f/858a8a70.jpg" width="30px"><span>o.O君程</span> 👍（1） 💬（0）<div>老师，请问一下，协程能通过performance去查看吗？这道题目的图还是有点难画，老师能给个答案吗？</div>2021-01-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/15/9c/575cca94.jpg" width="30px"><span>LearnAndTry</span> 👍（1） 💬（1）<div>有个问题没看懂，父协程和gen协程切换调用栈那块。是不是本质上还是gen协程执行上下文进出栈？？“切换”两个字让我感觉是有指针指向两个执行上下文</div>2020-05-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fa/84/b91ee3a9.jpg" width="30px"><span>stone</span> 👍（1） 💬（3）<div>&#47;&#47; 老师, node本地执行 promise then先执行 
&#47;&#47; node本地执行  
&#47;&#47; 1 script start
&#47;&#47; 2 bar start
&#47;&#47; 3 foo
&#47;&#47; 4 promise executor
&#47;&#47; 5 script end
&#47;&#47; 6 promise then
&#47;&#47; 7 bar end
&#47;&#47; 8 setTimeout

&#47;&#47; 浏览器执行
&#47;&#47; 1 script start
&#47;&#47; 2 bar start
&#47;&#47; 3 foo
&#47;&#47; 4 promise executor
&#47;&#47; 5 script end
&#47;&#47; 6 bar end
&#47;&#47; 7 promise then
&#47;&#47; 8 setTimeout
</div>2020-03-10</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/xRYuVOluJxeuRtmKPjwwkSibKeeHEia1fVyiaK14JQtdM3bLqHShGTSvF3yRY4Mp81gz2hLw6BZoY02AXSFHZiaBxg/132" width="30px"><span>bobi</span> 👍（1） 💬（2）<div>&#47;&#47;foo 函数
function* foo() {
    let response1 = yield fetch(&#39;https:&#47;&#47;www.geekbang.org&#39;)
    console.log(&#39;response1&#39;)
    console.log(response1) &#47;&#47; 这里为什么是undefined
    let response2 = yield fetch(&#39;https:&#47;&#47;www.geekbang.org&#47;test&#39;)
    console.log(&#39;response2&#39;)
    console.log(response2) &#47;&#47; 这里为什么是undefined
}
老师，在你举的生成器和Promise结合的例子中，为什么执行器里面取不到接口的值啊？
</div>2019-09-21</li><br/><li><img src="" width="30px"><span>Geek_f74777</span> 👍（1） 💬（0）<div>老师，课后习题中的第一个异步foo函数中会异步执行返回一个Promise对象，那么这个Promise对象在创建返回的过程中，是否会往微任务队列中添加微任务？既然foo()执行返回的结果已经是一个Promise了，那么V8引擎还会将await后的foo()
返回的Promise再进行一次Promise封装吗？</div>2019-09-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡</div>2024-05-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/90/43/e9345631.jpg" width="30px"><span>学无止境</span> 👍（0） 💬（0）<div>script start

bar start

foo

promise executor

script end

bar end

promise then

setTimeout

清晰起来了</div>2023-11-03</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTL7mqNgcWSzn3rG3XmDxNx59Tofsr4YZY53waCicMsVy74pQpZLib4D4iaftoOtibLIEx0e2CNwOkvAxA/132" width="30px"><span>知朋</span> 👍（0） 💬（0）<div>如果微任务执行时间过长，是不是会影响后续宏任务的执行，进而影响整个js线程？</div>2023-10-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/2d/16/b525a71d.jpg" width="30px"><span>zgy</span> 👍（0） 💬（0）<div>const foo = function*() {
  yield &#39;a&#39;;
  console.log(&#39;1&#39;);
  yield &#39;b&#39;;
  console.log(&#39;2&#39;);
  yield &#39;c&#39;;
  console.log(&#39;3&#39;);
};

let str = &#39;&#39;;
for (const val of foo()) {
  str = str + val;
}

console.log(str);&#47;&#47; abc
生成器也可以不使用 next 执行吗？</div>2023-05-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/08/f4/492bb269.jpg" width="30px"><span>小明</span> 👍（0） 💬（1）<div>老师, 有个问题很困惑, 下面代码为什么有主线程while true死循环了, 还能执行setTimeout的宏任务, 还能响应点击事件呢?
  
  &#47;&#47; 两个按钮
  let btn1 = document.getElementById(&#39;btn1&#39;)
  let btn2 = document.getElementById(&#39;btn2&#39;)

  &#47;&#47; 一定时间后resolve Promise
  const sleep = time =&gt; new Promise((resolve, reject) =&gt; {
    setTimeout(resolve, time)
  })

  &#47;&#47; 开始无限循环
  const go = async () =&gt; {
    let i = 0
    while(true) {
      console.log(i++)
      await sleep(1000)
      console.log(i++)
      await sleep(1000)
      console.log(i++)
      await sleep(1000)
    }
  }

  &#47;&#47; 点击开始无限循环
  btn1.addEventListener(&#39;click&#39;, go)
  &#47;&#47; 点击打印
  btn2.addEventListener(&#39;click&#39;, () =&gt; {
    console.log(&#39;btn2 clicked&#39;)
  })</div>2023-03-24</li><br/><li><img src="" width="30px"><span>Geek_ajing</span> 👍（0） 💬（0）<div>script start
bar start
foo
promise executor
script end
bar end
promise then
setTimeout</div>2022-11-25</li><br/><li><img src="" width="30px"><span>Geek_2500a0</span> 👍（0） 💬（0）<div>输出结果如下：
script start
bar start
foo
promise executor
script end
bar end
promise then
setTimeout

分析如下：
1、首先执行 console.log(&#39;script start&#39;)，输出 script start。
2、执行 setTimeout，产生一个宏任务，放到消息队列里。
3、再执行 bar() ，产生一个协程bar，并输出 bar start。
4、然后执行 await foo() ，此时输出 foo，并隐式执行 resolve(undefined)，产生第一个微任务，并暂停协程bar。
5、返回父协程继续执行，输出 promise executor， 并产生第二个微任务。
6、最后再执行 console.log(&#39;script end&#39;)， 输出 script end。此时该宏任务执行完毕，到了检查点，开始执行微任务队列的内容。
7、第一个微任务执行，返回 undefined，然后输出 bar end。
8、第二个微任务执行， 输出 promise then。
9、最后当前宏任务下的微任务都执行完成，开始下一个宏任务（setTimeout）执行，输出 setTimeout。</div>2022-10-20</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLzSRrK59sydknSSYZdeTww3Cgib9Gy9N4BJGgSXMYdmVIxJYwDXPsLCIE68AbwTkgUct8J4iboAqicA/132" width="30px"><span>罗武钢</span> 👍（0） 💬（0）<div>感谢老师的分享，懂了，生成器+Promise+自动迭代器=async&#47;await。</div>2022-09-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/62/02/fd00a1de.jpg" width="30px"><span>七月拾思</span> 👍（0） 💬（0）<div>async function foo() {
    console.log(1)
    let a = await 100
    console.log(a)
    console.log(2)
    return &#39;hello&#39;
}
console.log(0)
let res = await foo()
console.log(3)
console.log(res);

如果在 foo() 前面加上 await，这样只有当 foo 函数执行完有返回值了，才继续往下面执行

输出： 

0
1
100
2
3
hello</div>2022-04-11</li><br/>
</ul>