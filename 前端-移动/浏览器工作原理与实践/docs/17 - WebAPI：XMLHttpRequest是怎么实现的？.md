在[上一篇文章](https://time.geekbang.org/column/article/134456)中我们介绍了setTimeout是如何结合渲染进程的循环系统工作的，那本篇文章我们就继续介绍另外一种类型的WebAPI——XMLHttpRequest。

自从网页中引入了JavaScript，我们就可以操作DOM树中任意一个节点，例如隐藏/显示节点、改变颜色、获得或改变文本内容、为元素添加事件响应函数等等， 几乎可以“为所欲为”了。

不过在XMLHttpRequest出现之前，如果服务器数据有更新，依然需要重新刷新整个页面。而XMLHttpRequest提供了从Web服务器获取数据的能力，如果你想要更新某条数据，只需要通过XMLHttpRequest请求服务器提供的接口，就可以获取到服务器的数据，然后再操作DOM来更新页面内容，整个过程只需要更新网页的一部分就可以了，而不用像之前那样还得刷新整个页面，这样既有效率又不会打扰到用户。

关于XMLHttpRequest，本来我是想一带而过的，后来发现这个WebAPI用于教学非常好。首先前面讲了那么网络内容，现在可以通过它把HTTP协议实践一遍；其次，XMLHttpRequest是一个非常典型的WebAPI，通过它来讲解浏览器是如何实现WebAPI的很合适，这对于你理解其他WebAPI也有非常大的帮助，同时在这个过程中我们还可以把一些安全问题给串起来。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/94/82/d0a417ba.jpg" width="30px"><span>蓝配鸡</span> 👍（68） 💬（10）<div>如何高效学习安全理论

1. why， 知道为什么有这个安全机制， 历史是什么样的

2. how，知道why之后自己先想想怎么解决这个问题， 再去看看别人是怎么解决的， 分析利弊

3. 学完之后自己上手试试

4. 拉个你身边最蠢的小伙伴把这件事给他说明白</div>2019-09-12</li><br/><li><img src="" width="30px"><span>Geek_d972f2</span> 👍（49） 💬（2）<div>建立tcp连接是在xhr open还是send?</div>2019-09-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/72/89/1a83120a.jpg" width="30px"><span>yihang</span> 👍（38） 💬（3）<div>请教老师，我看到 es6中可以通过一个 fetch api来请求，它的实现是用了 xmlHttpRequest么？如果不是，原理上有什么不同？</div>2019-09-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/5b/d6/d6c26ea2.jpg" width="30px"><span>imperial</span> 👍（17） 💬（1）<div>老师，异步函数的调用不应该有三种方式吗，可以放到队列尾，微任务中，也可以放入延迟队列中，为什么不放入延迟队列中呢</div>2019-10-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/5f/80/51269d88.jpg" width="30px"><span>Hurry</span> 👍（10） 💬（2）<div>IPC是什么</div>2019-09-14</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJibVeub5HnlS9HgLdrDSnQma6VINyAyf1bTOhKh4MGQkMydoCVs7ofbicePRomxjDM873A56fqx97w/132" width="30px"><span>oc7</span> 👍（7） 💬（1）<div> 异步回调的第二种方式 把异步函数添加到微任务队列中 具体是哪些WebAPI呢? Promise.then?</div>2019-09-12</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/xRYuVOluJxeuRtmKPjwwkSibKeeHEia1fVyiaK14JQtdM3bLqHShGTSvF3yRY4Mp81gz2hLw6BZoY02AXSFHZiaBxg/132" width="30px"><span>bobi</span> 👍（5） 💬（1）<div>老师，什么时候专门讲微任务？</div>2019-09-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/f5/b8/9f165f4b.jpg" width="30px"><span>mfist</span> 👍（5） 💬（1）<div>作为一名前端开发工程师，要如何高效地学习前端web安全理论呢？
作为web工程师可以稍微把自己领域知识向后端扩展一些，这样理解web问题、网络传输问题会
更加得心应手。比如说前端浏览器因为跨域block，后端到底有没有处理请求；XSS 漏洞 以及CSRF
漏洞如果能前后端一起模拟一下，会更容易理解的。

今日总结
xmlhttprequest是为了解决网页局部数据刷新产生的技术。通过同步回调和异步回调以及系统调用栈来引出了
xmlhttprequest运行机制。一个xhr主要包含下面四个步骤：1. 创建xmlhttprequest对象；2. 为xhr对象
注册回调函数（ontimeout、onerror、onreadystatechange）；3. 打开请求（xhr.open（&#39;GET&#39;, url,true））4. 配置基础的请求信息（timeout&#47;responseType&#47;setRequestHeader）；5. 发送请求。xhr中场景的坑（
跨域和混合内容）</div>2019-09-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/cf/3e/5c684022.jpg" width="30px"><span>朱维娜🍍</span> 👍（4） 💬（1）<div>想知道 延时任务是不是一种微任务啊</div>2019-09-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/9d/5d/3fdead91.jpg" width="30px"><span>レイン小雨</span> 👍（20） 💬（13）<div>老师后面能详细的讲一下浏览器同源策略的具体实现吗？作为前端最基本的常识性知识却总是感觉理解的不够深入，开始我以为是跨域的请求是被浏览器“拦截在了门内”----即请求没有发送出去，但是看了很多文章中说，其实跨域的请求是发送出去了，服务器也接收到了并响应了，而是在返回的时候被浏览器“拦截在门外”，还有人说，不同的浏览器实现也不一样，很是困惑这里，希望老师能给一个确定的答案。</div>2019-09-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/39/08/09055b47.jpg" width="30px"><span>淡</span> 👍（9） 💬（5）<div>老师你好，我有以下几个疑问：
1.渲染进程里的主线程while循环空转，为啥不会造成系统卡死？我们自己code里空while死循环会造成卡死
2.就是网络进程IPC给渲染进程时，渲染进程收到消息。这里的”消息“具体包含哪些内容啊？
谢谢。</div>2019-09-17</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83epcs6PibsP9vEXv4EibUw3bhQPUK04zRTOvfrvF08TwM67xPb1LBh2uRENHQwo2VqYfC5GhJmM7icxHA/132" width="30px"><span>蹦哒</span> 👍（3） 💬（1）<div>老师请问是否可以这样理解：
异步的本质，就是通过把方法（函数）添加到消息队列尾部，通过循环系统在下一次循环中去执行；
同步的本质，就是在当前方法中执行另外一个方法，执行完之后接着执行原来的方法</div>2020-07-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/c8/e9/c7c5cbf5.jpg" width="30px"><span>l1shu</span> 👍（3） 💬（3）<div>为什么有些文章说渲染进程中有一个定时器线程用来计时的 到时间后会把回调函数塞到消息队列  而没有提到延迟队列这个说法  求老师解答</div>2019-10-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/cc/2d/124656fb.jpg" width="30px"><span>Yefei</span> 👍（2） 💬（0）<div>前几章都很赞，这一章看来三篇了，对于前端开发同学来说，整体有点hello world的感觉，难道是另一个人准备的么 :(</div>2023-02-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/93/4a/de82f373.jpg" width="30px"><span>AICC</span> 👍（2） 💬（1）<div>老师什么时候出一个web安全的专栏啊，好想系统性的学学</div>2019-09-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（2） 💬（0）<div>文中说：网络进程接收到数据之后，就会利用 IPC 来通知渲染进程；渲染进程接收到消息之后，会将 xhr 的回调函数封装成任务并添加到消息队列中
---------------------------------------------------------
这里网络进程收到数据之后，会进行资源请求的结果状态判断吗？ 只是把对应的资源请求的结果状态 和 响应数据通知给 渲染进程，然后渲染进程 根据请求结果状态选择对应的回调函数添加人任务队列中的呢？</div>2019-09-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/27/d5/0fd21753.jpg" width="30px"><span>一粟</span> 👍（2） 💬（0）<div>随着互联网金融的发展，web安全越来越重要了</div>2019-09-12</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/yyibGRYCArsUNBfCAEAibua09Yb9D5AdO8TkCmXymhAepibqmlz0hzg06ggBLxyvXicnjqFVGr7zYF0rQoZ0aXCBAg/132" width="30px"><span>james</span> 👍（1） 💬（0）<div>三个点：
what（是什么）、why（为什么）、how（怎么做）</div>2020-06-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/1a/8c/d91b01a6.jpg" width="30px"><span>zhangbao</span> 👍（1） 💬（3）<div>老师好！关于 XMLHttpRequest 的工作机制，有一个疑问，想不太明白：xhr 的 onreadystatechange 回调，在整个请求过程中，会触发好几次，那么封装成任务的 xhr 的回调函数，第一次从消息队列中取出执行一次后，不就没有了吗，怎么能保证后续 state 改变时的还有回调来执行的呢？

 </div>2020-05-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/22/97/5263baeb.jpg" width="30px"><span>健忘症。</span> 👍（1） 💬（2）<div>老师，我有一些疑问想请教您一下。

您说过 MutationObserver、和 Promise 是可以实现微任务的两种方式。
而微任务的执行时机又是主线程执行结束后，当前宏任务结束前的时机。
那么说明微任务是依赖与宏任务存在的，而宏任务是指存放在消息队列中的回调函数。
那是不是可以说，我使用 Promise 包装了一下 XMLHttpRequest 请求，有 .then 的操作，
那么 XMLHttpRequest 请求成功后返回的结果，通过 IPC 包装成了宏任务进入了消息队列中。
当消息队列执行到XMLHttpRequest 回调函数的时候，是执行了一个宏任务，那么为什么.then 中的回调函数就可以被判定为微任务而去执行的呢？？
还有一个问题就是，如果 Promise 并没有进行异步操作，而是直接 new Promise(resolve =&gt; {resolve(1)}).then((res) =&gt; {})
那么.then 中的回调函数还是否是一个微任务了呢？？

望指点一二，再次感谢老师的付出。</div>2020-04-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/98/1c/d7a1439e.jpg" width="30px"><span>KaKaKa</span> 👍（1） 💬（2）<div>执行 JS 代码是一个任务，执行任务时会维护一个系统调用栈。那当执行 JS 代码这个任务时，系统调用栈和 JS 代码内的执行上下文栈有什么关联？</div>2020-04-08</li><br/><li><img src="" width="30px"><span>Geek_177f82</span> 👍（1） 💬（3）<div>有个疑惑，就是使用setTimeout执行任务时会把任务添加到延迟消息队列，但是在函数中使用setTimeout就是异步回调。而异步回调函数有两种方式：1， 放入微任务处理；2，放入消息队列处理。这样以来就有点迷糊了。那使用setTimeout执行的任务到底应该放哪里执行。还是依据执行环境分别处理。希望老师解答疑惑。谢谢🙏！</div>2019-09-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡</div>2024-05-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/3a/f5/1fa34f88.jpg" width="30px"><span>润曦</span> 👍（0） 💬（0）<div>`XMLHttpRequest`的异步回调属于**宏任务**（Macro Task）。

在JavaScript中，任务被分为两大类：宏任务和微任务。它们都是异步任务，但在事件循环中的处理顺序不同。

### 宏任务（Macro Task）

宏任务是由宿主环境（如浏览器或Node.js）发起的任务，每次事件循环只执行一个宏任务。宏任务包括：

- `setTimeout`
- `setInterval`
- `setImmediate`（Node.js特有）
- I&#47;O 操作
- UI 渲染
- `XMLHttpRequest`的回调

### 微任务（Micro Task）

微任务通常是由JavaScript引擎发起的任务，每次事件循环会执行所有队列中的微任务。微任务包括：

- `Promise`回调（`then`、`catch`、`finally`）
- `MutationObserver`
- `process.nextTick`（Node.js特有）

### 执行顺序

在每个事件循环中，首先执行当前宏任务中的代码，然后执行该宏任务产生的所有微任务。如果微任务执行过程中继续产生新的微任务，这些新的微任务也会在当前宏任务之后、下一个宏任务之前执行完成。

### `XMLHttpRequest`回调的处理

当`XMLHttpRequest`操作完成（无论是成功还是失败），它的回调函数会被放入宏任务队列。这意味着回调的执行会等到当前执行栈清空，并且已经在微任务队列中的所有微任务都执行完毕之后。

### 结论

所以，`XMLHttpRequest`的异步回调是宏任务，这也意味着它的执行可能会被当前执行栈中的代码以及微任务队列中的任务所延迟。这种机制确保了异步代码的执行顺序和预期效果，但在编写代码时也需要考虑到它可能带来的影响。</div>2024-02-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/fb/ee/e574554d.jpg" width="30px"><span>王晓聪</span> 👍（0） 💬（0）<div>老师有出书的计划吗？课程还是从比较宏观的角度讲了浏览器的原理。希望老师出本书讲讲更细节的浏览器实现原理</div>2023-10-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2f/99/7c/b85e0be1.jpg" width="30px"><span>Geek_89dbe0</span> 👍（0） 💬（0）<div>留下jio印</div>2022-09-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/2d/16/b525a71d.jpg" width="30px"><span>zgy</span> 👍（0） 💬（0）<div>突然出现的安全篇，是为下文点题吗？感觉上有点突兀。</div>2022-03-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/10/5e/42f4faf7.jpg" width="30px"><span>天择</span> 👍（0） 💬（0）<div>这里面有个问题，网络请求回来之后，浏览器怎么知道把哪个callback任务放入队列呢？是每个callback和tcp请求之间（socket标识？）有映射关系？</div>2021-12-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/91/b1/ae745f2f.jpg" width="30px"><span>nabaonan</span> 👍（0） 💬（0）<div>xmlhttprequest是开启的进程还是线程？我看网上有的文章说是开启的线程</div>2021-11-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/e0/93/c512e343.jpg" width="30px"><span>云销雨霁</span> 👍（0） 💬（0）<div>ontimeout， onerror 这些回调，已经在消息队列里，onreadystatechange = 4消息正确的被接受了，这些ontimeout， onerror任务什么时候会被清理呢</div>2021-08-15</li><br/>
</ul>