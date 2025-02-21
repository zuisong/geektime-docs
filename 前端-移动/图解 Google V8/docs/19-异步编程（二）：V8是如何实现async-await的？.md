你好，我是李兵。

上一节我们介绍了JavaScript是基于单线程设计的，最终造成了JavaScript中出现大量回调的场景。当JavaScript中有大量的异步操作时，会降低代码的可读性, 其中最容易造成的就是回调地狱的问题。

JavaScript社区探索并推出了一系列的方案，从“Promise加then”到“generator加co”方案，再到最近推出“终极”的async/await方案，完美地解决了回调地狱所造成的问题。

今天我们就来分析下回调地狱问题是如何被一步步解决的，在这个过程中，你也就理解了V8 实现async/await的机制。

## 什么是回调地狱？

我们先来看什么是回调地狱。

假设你们老板给了你一个小需求，要求你从网络获取某个用户的用户名，获取用户名称的步骤是先通过一个id\_url来获取用户ID，然后再使用获取到的用户ID作为另外一个name\_url的参数，以获取用户名。

我做了两个DEMO URL，如下所示：

```
const id_url = 'https://raw.githubusercontent.com/binaryacademy/geektime-v8/master/id'
```

```
const name_url = 'https://raw.githubusercontent.com/binaryacademy/geektime-v8/master/name'
```

那么你会怎么实现这个小小的需求呢？

其中最容易想到的方案是使用XMLHttpRequest，并按照前后顺序异步请求这两个URL。具体地讲，你可以先定义一个GetUrlContent函数，这个函数负责封装XMLHttpRequest来下载URL文件内容，由于下载过程是异步执行的，所以需要通过回调函数来触发返回结果。那么我们需要给GetUrlContent传递一个回调函数result\_callback，来触发异步下载的结果。
<div><strong>精选留言（26）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/c8/04/fed4c1ad.jpg" width="30px"><span>若川</span> 👍（46） 💬（6）<div>co源码实现原理：其实就是通过不断的调用generator函数的next()函数，来达到自动执行generator函数的效果（类似async、await函数的自动自行）。

具体代码分析，我之前写过一篇文章：
《学习 koa 源码的整体架构，浅析koa洋葱模型原理和co原理》
https:&#47;&#47;juejin.im&#47;entry&#47;5e6a080af265da575b1bd160</div>2020-05-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a3/ea/53333dd5.jpg" width="30px"><span>HoSalt</span> 👍（13） 💬（1）<div>老师 async、await 是 generator promise 的语法糖吗，v8里面前者是借助后者实现的吗？async await 为什么能用try catch 捕获错误？</div>2020-04-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/20/97/919f5e6b.jpg" width="30px"><span>Geek_gaoqin</span> 👍（10） 💬（1）<div>哦，我知道了，async 修饰的函数会有自己的协程，那么它代码内部创建的宏任务，主线程有空了还是会拿消息队列中的宏任务来执行，如果await等待了一个never resolve，那么它后面的代码就再也不会执行！但是却不会影响消息队列中键盘鼠标事件等其它任务的执行！</div>2020-06-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/18/65/35361f02.jpg" width="30px"><span>潇潇雨歇</span> 👍（8） 💬（1）<div>co的原理是自动识别生成器代码的yield，做暂停执行和恢复执行的操作</div>2020-04-28</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83epcs6PibsP9vEXv4EibUw3bhQPUK04zRTOvfrvF08TwM67xPb1LBh2uRENHQwo2VqYfC5GhJmM7icxHA/132" width="30px"><span>蹦哒</span> 👍（5） 💬（5）<div>请教老师：为什么Generator方案不实现自动执行next的功能呢？我理解async&#47;await相对于Generator方案主要是能够自动执行next吧，co方案也是这么做的</div>2020-05-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/20/97/919f5e6b.jpg" width="30px"><span>Geek_gaoqin</span> 👍（1） 💬（1）<div>老师，很长很长一段代码中，业务逻辑很复杂，既有产生微任务，又有setTimeout产生宏任务，更有很多await的语句，那么这些结合上一章节讲的内容，它的执行顺序是怎样的呢？可以帮我分析下吗？</div>2020-06-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/d4/57/b0a11ae5.jpg" width="30px"><span>华仔</span> 👍（1） 💬（4）<div>setTimeout(() =&gt; {
console.log(&#39;in timeout&#39;);
})
new Promise((resolve, reject) =&gt; {
setTimeout(() =&gt; {
resolve(3);
console.log(&#39;in promise-timeout&#39;)
})
console.log(&#39;in promise&#39;)
}).then((res) =&gt; {
console.log(&#39;in then&#39;)
})
老师，想问下promise创建的then是微任务，是宏任务中创建的队列保存的消息队列中维护的。那么我这里这样一个场景，在promise中通过setTimeout(模拟宏任务http request)异步resolve的场景下，then也就会在下一个宏任务执行之后再执行了。这种当前宏任务中注册的微任务被拖到下一个宏任务执行，是怎么实现的呢？</div>2020-05-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/3f/4c/0f186696.jpg" width="30px"><span>断线人偶</span> 👍（0） 💬（2）<div>老师可以讲一下为什么在使用async...await...可以通过try...catch...来捕获到异步函数中的异常吗，v8是怎么实现的</div>2020-05-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/01/44/3a9b2b69.jpg" width="30px"><span>地球外地人</span> 👍（0） 💬（1）<div>老师能讲讲 generate 和 await async中的闭包吗？</div>2020-05-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/06/2a/3964c2a2.jpg" width="30px"><span>天然呆</span> 👍（0） 💬（1）<div>
function HaveResolvePromise(){
    return new Promise((resolve, reject) =&gt; {
        setTimeout(() =&gt; {
            resolve(100)
          }, 0);
      })
}
async function getResult() {
    console.log(1)
    let a = await NoResolvePromise()
    console.log(a)
    console.log(2)
}
console.log(0)
getResult()
console.log(3)

是不是要改动？NoResolvePromise ==&gt;&gt; HaveResolvePromise</div>2020-04-28</li><br/><li><img src="" width="30px"><span>Geek_f74777</span> 👍（0） 💬（1）<div>看来一下co源码, 我的理解是: co的执行原理就是通过promise将generator函数中yield的异步操作的暂停和恢复执行自动化</div>2020-04-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/41/38/4f89095b.jpg" width="30px"><span>写点啥呢</span> 👍（0） 💬（1）<div>async&#47;await章节的示例代码看着迷糊了，想和老师请教下，
1. 这部分代码，foo是不是应该调用getResult

function NeverResolvePromise(){
    return new Promise((resolve, reject) =&gt; {})
}
async function getResult() {
    let a = await NeverResolvePromise()
    console.log(a)
}
foo()
console.log(0)

2. 在这个代码片段里，foo函数内await的应该是HasResolvePromise

function HaveResolvePromise(){
    return new Promise((resolve, reject) =&gt; {
        setTimeout(() =&gt; {
            resolve(100)
          }, 0);
      })
}
async function foo() {
    console.log(1)
    let a = await NoResolvePromise()
    console.log(a)
    console.log(2)
}
console.log(0)
foo()
console.log(3)

另外#2问题里的代码对应的图例中的函数名字和代码对应不上。</div>2020-04-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/61/c1/93031a2a.jpg" width="30px"><span>Aaaaaaaaaaayou</span> 👍（4） 💬（0）<div>co 里面一般会定义一个方法,比如nextStep，执行改方法时会调用迭代器的next，根据结果中的done的取值来决定是继续递归调用nextStep还是结束。</div>2020-04-28</li><br/><li><img src="" width="30px"><span>kuaishou88880043</span> 👍（1） 💬（0）<div>讲的好好 ，“async修饰的函数会开启一个协程”，看到就通了</div>2024-09-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡</div>2024-06-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/4c/fd/2e4cd48f.jpg" width="30px"><span>见字如晤</span> 👍（0） 💬（0）<div>function NeverResolvePromise() {
  return new Promise((resolve, reject) =&gt; {});
}

async function getResult() {
  await NeverResolvePromise();
  console.log(1);
}

function NeverResolvePromise2() {
  return new Promise((resolve, reject) =&gt; resolve(2));
}


async function getResult2() {
  console.log(await NeverResolvePromise2());
}

getResult();
console.log(0);
getResult2();

以上代码输出 &#47;&#47; 0 2，想问一下既然NeverResolvePromise的协程没有恢复，为什么NeverResolvePromise2的协程还能进行，不是只能同时执行一个协程吗？</div>2023-10-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/fd/06/752d7465.jpg" width="30px"><span>kakong大雄</span> 👍（0） 💬（0）<div>老师 请问一下协程执行流程图中的 result.next() 的触发时机是什么时候？ 对比图中前后的 result.next() 的位置都不同</div>2022-09-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/b3/a2/4d372148.jpg" width="30px"><span>ruoyiran</span> 👍（0） 💬（0）<div>老师您好，想请教一个问题，在V8中是否有办法实现类似下面这样的代码，或者有什么思路可以提供吗？

var signal = createSignal();

async function asyncFunction() {
    Promise.resolve().then(() =&gt; {
        console.info(&quot;resolved!!!&quot;);
        signal.notify();
      });
}

function run() {
  asyncFunction();
  console.info(&quot;waiting for Promise.resolve&quot;);
  signal.wait();
  console.info(&quot;continue to do sth.&quot;);
}

function main() {
    &#47;&#47; code1....
    run();
    &#47;&#47; code2...
    &#47;&#47; 期望输出结果：
    &#47;&#47; waiting for Promise.resolve
    &#47;&#47; resolved!!!
    &#47;&#47; continue to do sth.
}

学习了老师这节的异步编程，收获挺多的。最近在工作中因项目需要，想实现一个在非async函数（如上面的run函数）中，等待一个async函数执行完成。因为在某个地方看到别人的代码实现逻辑差不多就这样的，在项目中也希望能实现这样的逻辑，只是createSignal内部实现不知道是怎样的。想请教下。</div>2021-11-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/35/35/9c5eb2c2.jpg" width="30px"><span>Prof.Bramble</span> 👍（0） 💬（0）<div>我觉得有部分描述有点小问题，比如 generator 运行，其运行后返回就不是函数了，而且也不会直接执行函数体的内容</div>2021-08-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/e7/d4/115cef63.jpg" width="30px"><span> 小云子</span> 👍（0） 💬（0）<div>还是想不通协程和消息队列、调用栈之间的执行流程是怎样的，有点难理解。</div>2021-03-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/2c/07/636a47cd.jpg" width="30px"><span>慢慢来的比较快</span> 👍（0） 💬（1）<div>协程在运行的时候，主线程可以从消息队列中获取事件执行吗？</div>2021-03-17</li><br/><li><img src="" width="30px"><span>Geek_mbq1n0</span> 👍（0） 💬（0）<div>
const id_url = &#39;https:&#47;&#47;raw.githubusercontent.com&#47;binaryacademy&#47;geektime-v8&#47;master&#47;id&#39;

这两个链接如果不翻墙，访问不到啊，国内这网络环境……</div>2021-01-04</li><br/><li><img src="" width="30px"><span>Geek_mbq1n0</span> 👍（0） 💬（0）<div>v8里面竟然也有协程，我以为只有go才有</div>2021-01-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/20/97/919f5e6b.jpg" width="30px"><span>Geek_gaoqin</span> 👍（0） 💬（1）<div>老师，请问一下，const a = await funA()时，此时 async funA中，比如又有 const b = await funB(), return的数据如果不依赖于funA中await的结果时 它就会不等funB执行就return数据了，如果是return b(或者是返回结果对b有依赖)它就会等funB执行结束再返回。我感觉项目中这也是一个容易出bug的地方，为什么不是统一都按照funB执行结束后再return数据呢？直觉和主观意图应该是要等结果后再返回呀。</div>2020-09-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/48/4e/51896855.jpg" width="30px"><span>落风</span> 👍（0） 💬（0）<div>co 迭代了好多个版本，目前把支持的数据类型，都转换成 Promise 在流转；核心就是一个 generator runner，通过 next(val) 来不断执行 generator，理解 next(val) 用来获取和传参对于流程分析至关重要</div>2020-09-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/fe/93/31869247.jpg" width="30px"><span>Presbyter🎱</span> 👍（0） 💬（0）<div>老师，我如果想在一个async内同时执行多个await操作，这个应该怎么处理呢</div>2020-06-11</li><br/>
</ul>