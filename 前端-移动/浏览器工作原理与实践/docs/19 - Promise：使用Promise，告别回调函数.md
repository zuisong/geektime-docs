在[上一篇文章](https://time.geekbang.org/column/article/135624)中我们聊到了微任务是如何工作的，并介绍了MutationObserver是如何利用微任务来权衡性能和效率的。今天我们就接着来聊聊微任务的另外一个应用**Promise**，DOM/BOM API中新加入的API大多数都是建立在Promise上的，而且新的前端框架也使用了大量的Promise。可以这么说，Promise已经成为现代前端的“水”和“电”，很是关键，所以深入学习Promise势在必行。

不过，Promise的知识点有那么多，而我们只有一篇文章来介绍，那应该怎么讲解呢？具体讲解思路是怎样的呢？

如果你想要学习一门新技术，最好的方式是先了解这门技术是如何诞生的，以及它所解决的问题是什么。了解了这些后，你才能抓住这门技术的本质。所以本文我们就来重点聊聊JavaScript引入Promise的动机，以及解决问题的几个核心关键点。

要谈动机，我们一般都是先从问题切入，那么Promise到底解决了什么问题呢？在正式开始介绍之前，我想有必要明确下，Promise解决的是异步编码风格的问题，而不是一些其他的问题，所以接下来我们聊的话题都是围绕编码风格展开的。

## 异步编程的问题：代码逻辑不连续

首先我们来回顾下JavaScript的异步编程模型，你应该已经非常熟悉页面的事件循环系统了，也知道页面中任务都是执行在主线程之上的，相对于页面来说，主线程就是它整个的世界，所以在执行一项耗时的任务时，比如下载网络文件任务、获取摄像头等设备信息任务，这些任务都会放到页面主线程之外的进程或者线程中去执行，这样就避免了耗时任务“霸占”页面主线程的情况。你可以结合下图来看看这个处理过程：
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/13/c1/05/fd1d47b6.jpg" width="30px"><span>空间</span> 👍（70） 💬（2）<div>异步AJAX请求是宏任务吧？Promise是微任务，那么用Promise进行的异步Ajax调用时宏任务还是微任务？</div>2019-09-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/49/57/978fb576.jpg" width="30px"><span>皮皮大神</span> 👍（29） 💬（11）<div>老师，我觉得这章没有前面的讲得透彻，手写的bromise非常不完整，希望老师答疑的时候可以带我们写一遍完整promise源码，三种状态的切换，还有.then为什么可以连续调用，内部如何解决多层异步嵌套，我觉得都很值得讲解，老师带我们飞。</div>2019-09-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f8/99/8e760987.jpg" width="30px"><span>許敲敲</span> 👍（4） 💬（10）<div>面试手写promise也不怕了</div>2019-09-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/eb/09/ba5f0135.jpg" width="30px"><span>Chao</span> 👍（3） 💬（2）<div>老师 你有答疑环节吗</div>2019-09-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/23/71/57c16ecb.jpg" width="30px"><span>任振鹏</span> 👍（1） 💬（1）<div>老师 渲染流水线 在 微任务 之前 还是 之后 执行啊？</div>2019-12-07</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTL7KMU6r5CquSI5kQlcaLuwph9HCSWcClT0YSmbon1Vov5ZcJpOCrc8WHEbfLrxbFedTjsEWuhgiaw/132" width="30px"><span>Geek_6b0898</span> 👍（1） 💬（1）<div>想问下老师什么时候给加餐课？支持老师尽快出啊</div>2019-11-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/ad/ec/776c9f72.jpg" width="30px"><span>袋袋</span> 👍（1） 💬（1）<div>老师，最后说定时器的效率不高，promise又把定时器改造成了微任务，可以说下具体是怎么改造的吗</div>2019-09-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/94/82/d0a417ba.jpg" width="30px"><span>蓝配鸡</span> 👍（0） 💬（1）<div>请问老师你用的什么工具画图？ </div>2019-11-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f7/20/e2dfa9c2.jpg" width="30px"><span>花儿与少年</span> 👍（0） 💬（1）<div>老师会在加班课里给大家讲解典型课后思考题吗</div>2019-09-19</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJ0F94uoYZQicRd7YEFjEJWm0EaUJXzkhiaqa5GQQ8a1FkicQIoHC4sp2ZG9m1JAFABuGsj34ucztjibA/132" width="30px"><span>Geek_Jamorx</span> 👍（88） 💬（9）<div>这三个题目非常重要，就跟做笔记一样回答了
1、Promise 中为什么要引入微任务？

由于promise采用.then延时绑定回调机制，而new Promise时又需要直接执行promise中的方法，即发生了先执行方法后添加回调的过程，此时需等待then方法绑定两个回调后才能继续执行方法回调，便可将回调添加到当前js调用栈中执行结束后的任务队列中，由于宏任务较多容易堵塞，则采用了微任务

2、Promise 中是如何实现回调函数返回值穿透的？
首先Promise的执行结果保存在promise的data变量中，然后是.then方法返回值为使用resolved或rejected回调方法新建的一个promise对象，即例如成功则返回new Promise（resolved），将前一个promise的data值赋给新建的promise

3、Promise 出错后，是怎么通过“冒泡”传递给最后那个捕获
promise内部有resolved_和rejected_变量保存成功和失败的回调，进入.then（resolved，rejected）时会判断rejected参数是否为函数，若是函数，错误时使用rejected处理错误；若不是，则错误时直接throw错误，一直传递到最后的捕获，若最后没有被捕获，则会报错。可通过监听unhandledrejection事件捕获未处理的promise错误



</div>2019-09-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/ae/a0/707350ef.jpg" width="30px"><span>穿秋裤的男孩</span> 👍（13） 💬（2）<div>promise.then是订阅者，订阅promise状态的改变，并且负责回掉；promise.resolve和promise.reject为发布者，发布promise的状态改变的信息。</div>2020-04-17</li><br/><li><img src="" width="30px"><span>Rapheal</span> 👍（9） 💬（1）<div>Promise的改进版，测试过也无问题。之前使用闭包存放所有回调函数有些问题，所有的Promise对象都是共享，这样会造成全局数据结构有问题。当前是基于回调函数数组传递在Promise对象之间传递实现。


    function _Promise(executor) {
        this._resolve = [];
        this._reject = [];
        this._catch;

        &#47;*临时保存引用*&#47;
        let self = this;
        
        this.then = function (resolve, reject) {
            resolve &amp;&amp; this._resolve.push(resolve);
            reject &amp;&amp; this._reject.push(reject);
            return this;
        }

        
        this.resolve = function (data) {
            setTimeout(() =&gt; {
                let callback = self._resolve.shift();
                self._reject &amp;&amp; self._reject.shift();
                let pro;
                callback &amp;&amp; (pro = callback(data));
                self._resolve &amp;&amp; (pro._resolve = self._resolve);
                self._reject &amp;&amp; (pro._reject = self._reject);
                self._catch &amp;&amp; (pro._catch = self._catch);

            }, 0)
        }

        this.reject = function (error) {        
            setTimeout(() =&gt; {
                let callback;
                self._reject &amp;&amp; (callback = self._reject.shift());
                callback &amp;&amp; callback(error);
                callback || self._catch(error);

            }, 0);
        }

        this.catch = function (callback) {
            this._catch = callback;
            return this;
        }
        executor(this.resolve, this.reject);
    }


function executor(resolve, reject) {
    let rand = Math.random();
    console.log(1)
    console.log(rand)
    if (rand &gt; 0.5)
        resolve(rand)
    else
        reject(rand)
}
var p0 = new _Promise(executor);

var p1 = p0.then((value) =&gt; {
    console.log(&quot;succeed-1&quot;)
    return new _Promise(executor)
})

var p3 = p1.then((value) =&gt; {
    console.log(&quot;succeed-2&quot;)
    return new _Promise(executor)
})

var p4 = p3.then((value) =&gt; {
    console.log(&quot;succeed-3&quot;)
    return new _Promise(executor)
})

p4.catch((error) =&gt; {
    console.log(&quot;error&quot;)
})


console.log(2)
</div>2019-10-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/04/bb/5e5c37c1.jpg" width="30px"><span>Angus</span> 👍（8） 💬（3）<div>看完这节之后我自己去实现了手写Promise，回顾了一下Promise，关于这方面的文章很多，我觉得老师大可不必在这里花大量篇幅去讲。专栏的名字是浏览器工作原理与实践，所以我希望老师能够更加着重这一方面的讲解。</div>2019-09-20</li><br/><li><img src="" width="30px"><span>乔小爷</span> 👍（6） 💬（2）<div>不是说要手写promise吗，，怎么在教程里面没有看到</div>2020-04-15</li><br/><li><img src="" width="30px"><span>Geek_be6d3f</span> 👍（5） 💬（1）<div>请问以下，在“异步编程的问题：代码逻辑不连续”这段中，代码下方的第一行，老师说“这短短的一段代码里面竟然出现了五次回调”，可是我怎么数，都只有三次回调啊，还有两次在哪里？</div>2020-03-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/52/0e/c5ff46d2.jpg" width="30px"><span>CondorHero</span> 👍（3） 💬（1）<div>```js
new Promise((r, rj) =&gt; {
    r();
}).then(() =&gt; {
    new Promise((r, rj) =&gt; {
        r();
    }).then(() =&gt; {
        console.log(&quot;inner then1&quot;)
        return new Promise((r, rj) =&gt; {
            r();
        })
    }).then(() =&gt; {
        console.log(&quot;inner then2&quot;)
    })
})
.then(() =&gt; {
    console.log(&quot;outer then2&quot;);
})
.then(() =&gt; {
    console.log(&quot;outer then3&quot;);
})
.then(() =&gt; {
    console.log(&quot;outer then4&quot;);
})
.then(() =&gt; {
    console.log(&quot;outer then5&quot;);
})
.then(() =&gt; {
    console.log(&quot;outer then6&quot;);
})
```
输出结果：

```
inner then1
outer then2
outer then3
outer then4
inner then2
outer then5
outer then6
```
老师能帮忙解释下这段代码的输出逻辑吗？

搞不懂输出 `outer then2` 之后紧接着输出了 `outer then3` 和  `outer then4` ，然后才输出 `inner then2`。

而我理解的是 `outer then2` 之后直接输出 `inner then2` 才对，我理解的顺序：

```
inner then1
outer then2
inner then2
outer then3
outer then4
outer then5
outer then6
```
</div>2021-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/5f/80/51269d88.jpg" width="30px"><span>Hurry</span> 👍（3） 💬（1）<div>这个太赞了 “ Promise 通过回调函数延迟绑定、回调函数返回值穿透和和错误“冒泡”技术 “， 之前看到别人手写实现 Promise，代码虽然可以看懂，但是理解不深，所以关键还是看如何实现这个三个点 回调函数延迟绑定、回调函数返回值穿透和和错误“冒泡”，结合这三个点和 promise API，手写一个 Promise, So easy

```js
class PromiseSimple {
  constructor(executionFunction) {
    this.promiseChain = []; &#47;&#47; 1.通过数组存储 callback，实现callback 延迟执行
    this.handleError = () =&gt; {};

    this.onResolve = this.onResolve.bind(this);
    this.onReject = this.onReject.bind(this);

    executionFunction(this.onResolve, this.onReject);
  }

  then(onResolve) {
    this.promiseChain.push(onResolve);

    return this;
  }

  catch(handleError) {
    this.handleError = handleError;

    return this;
  }

  onResolve(value) {
    let storedValue = value;

    try {
      this.promiseChain.forEach((nextFunction) =&gt; {
         storedValue = nextFunction(storedValue); &#47;&#47; 2.循环，实现 callback 值传递
      });
    } catch (error) {   &#47;&#47; 3. try catch, 实现错误值冒泡
      this.promiseChain = [];

      this.onReject(error);
    }
  }

  onReject(error) {
    this.handleError(error);
  }
}
```
</div>2019-09-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/63/5a/4ec96cfe.jpg" width="30px"><span>林高鸿</span> 👍（2） 💬（2）<div>老师，我理解是这样，这里感觉大部分人（可能也包括老师）都弄错了，我理解的是：

对我们（普通使用者）来说，用 Promise 是因为有宏任务问题（AJAX，SetTimeout）需要解决，而专注问题解决时是不需要考虑工具（Promise）自身实现原理（微任务）的

简言之，对普通使用者来说，把 Promise 和微任务联系起来是本末倒置


PS：其实，如果能保证用 Promise 解决的是异步问题（宏任务&#47;微任务），那 Promise 自身实现原理也不需要微任务来“延迟绑定”（因为异步回来要 resolve 时，then 一定已经执行绑定...）</div>2021-08-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/04/13/84d35588.jpg" width="30px"><span>张萌</span> 👍（2） 💬（2）<div>一个简易版的 Promise
class Promise {
  constructor(fn) {
    this.state = Promise.PENDING;
    this.value = undefined;
    this.reason = null;
    this.onFulfilledCallbacks = [];
    this.onRejectedCallbacks = [];
    fn(this.resolve.bind(this), this.reject.bind(this));
  }

  then(onFulfilled, onRejected) {
    if (this.state === Promise.FULFILLED) {
      onFulfilled(this.value);
    } else if (this.state === Promise.REJECTED) {
      onRejected(this.reason);
    } else {
      this.onFulfilledCallbacks.push(onFulfilled);
      this.onRejectedCallbacks.push(onRejected);
    }
    return this;
  }

  resolve(value) {
    this.state = Promise.FULFILLED;
    this.value = value;
    if (value.constructor === this.constructor) {
      value.onFulfilledCallbacks = [...this.onFulfilledCallbacks];
      value.onRejectedCallbacks = [...this.onRejectedCallbacks];
    } else {
      this.onFulfilledCallbacks.forEach((item) =&gt; {
        if (typeof item === &#39;function&#39;) {
          item(value);
        }
      });
    }
  }

  reject(reason) {
    this.state = Promise.REJECTED;
    this.reason = reason;
    this.onRejectedCallbacks.forEach((item) =&gt; {
      if (typeof item === &#39;function&#39;) {
        item(reason);
      }
    });
  }
}

Promise.PENDING = &#39;pending&#39;;
Promise.FULFILLED = &#39;fulfilled&#39;;
Promise.REJECTED = &#39;rejected&#39;;


module.exports = Promise;</div>2020-05-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/71/45/126cd913.jpg" width="30px"><span>袭</span> 👍（1） 💬（1）<div>延迟绑定和返回值穿透，可以理解成是提供了新的思路：原思路是嵌套处理任务结果。这种写法是先声明任务，再声明任务的返回处理流程，实际上是创造了独立性，把原来的嵌套变成了分割的两步，再用微任务把两部分连起来</div>2021-05-27</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/mX9k3VNGc2mZkfTmI9zia209EugGkpFyLXl8ia1HcnhJCrAsoJ2UliaHQaeDjKOkoCaQOia6iaoj1Dkv3gZqsONlaMg/132" width="30px"><span>悠米</span> 👍（1） 💬（0）<div>老师，手写 Promise 什么时候会有？非常期待~</div>2020-08-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/54/c6/c2481790.jpg" width="30px"><span>lisiur</span> 👍（1） 💬（1）<div>then函数为什么延时绑定就需要在微任务里执行resolve？先将结果保存下来，什么时候调用then函数时就把结果抛出去不行吗？</div>2019-11-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/67/8e/14f06610.jpg" width="30px"><span>胖虎</span> 👍（1） 💬（1）<div>&quot;回调函数返回值穿透到最外层&quot; 这句话配合老师您讲的例子是错误的  return x2  这个x2按照您那种方式没办法返回到最外层  最外层的x2和里面函数return 出来的x2根本就是两个东西</div>2019-11-22</li><br/><li><img src="" width="30px"><span>Rapheal</span> 👍（1） 💬（0）<div>自己手写了一个_Promise,运行老师上面的程序，没啥毛病。除了使用宏任务，可以解决嵌套和参数穿透问题。


var _Promise = (function () {
    
    &#47;*使用闭包 保存所有的回调函数 *&#47; 
    var _resolve = [];
    var _reject = [];
    var _catch;

    return function (executor) {

        this.print = function () {
            console.log(_resolve)
            console.log(_catch)

        }
        this.then = function (resolve, reject) {
            resolve &amp;&amp; _resolve.push(resolve);
            reject &amp;&amp; _reject.push(reject);
            return this;
        }

        this.resolve = function (data) {
            setTimeout(function () {
                let callback = _resolve.shift();
                let pro;
                callback &amp;&amp; (pro = callback(data));
                _reject.shift();

            }, 0)
        }

        this.reject = function (error) {
            setTimeout(function () {
                let callback = _reject.shift();
                callback &amp;&amp; callback(error);
                callback || _catch(error);

            }, 0);
        }

        this.catch = function (callback) {
            _catch = callback;
            return this;
        }
        executor(this.resolve, this.reject);
    }
})()

function executor(resolve, reject) {
    let rand = Math.random();
    console.log(1)
    console.log(rand)
    if (rand &gt; 0.5)
        resolve(rand)
    else
        reject(rand)
}
var p0 = new _Promise(executor);

var p1 = p0.then((value) =&gt; {
    console.log(&quot;succeed-1&quot;)
    return new _Promise(executor)
})

var p3 = p1.then((value) =&gt; {
    console.log(&quot;succeed-2&quot;)
    return new _Promise(executor)
})

var p4 = p3.then((value) =&gt; {
    console.log(&quot;succeed-3&quot;)
    return new _Promise(executor)
})

p4.catch((error) =&gt; {
    console.log(&quot;error&quot;)
})


console.log(2)
</div>2019-10-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/97/7d/803956d5.jpg" width="30px"><span>Mick</span> 👍（0） 💬（1）<div>老师，这里promise 中then中的回调，是执行then的时候 加入到微队列的吗</div>2024-06-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡</div>2024-05-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/53/a7/a3f98d9c.jpg" width="30px"><span>黄秋生</span> 👍（0） 💬（0）<div>突然发现之前看的内容都漏球很严重，有的东西就是略过了，或者根本没讲</div>2022-12-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/8a/d6/00cf9218.jpg" width="30px"><span>撒哈拉</span> 👍（0） 💬（0）<div>promise 为了解决嵌套调用，我理解。 为了解决成功和错误多次处理我是没想到的 </div>2021-10-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/71/45/126cd913.jpg" width="30px"><span>袭</span> 👍（0） 💬（0）<div>1.因为需要提供resolve函数给executor,而resolve并未指名，所以需要通过微任务机制等then中绑定后再执行。
2.executor生成了业务相关数据，而resolve进行了返回值的返回，因此在then绑定时才明确了返回值是什么，从而实现从resolve函数穿透executor</div>2021-05-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/51/c7/15cb1d28.jpg" width="30px"><span>tobemaster</span> 👍（0） 💬（0）<div>有个问题非常困惑。

const p1 = new Promise(resolve =&gt; {
      console.log(&#39;begin&#39;);
      resolve(&#39;then1&#39;);
    }).then(v =&gt; {
      console.log(v);
      return &#39;then2&#39;;
    })
  
    &#47;&#47; then 链式调用，和微任务的产生关系
    new Promise(resolve =&gt; {
      console.log(1);
      resolve();
    })
      .then(() =&gt; {
        console.log(2);
      })
      .then(() =&gt; {
        console.log(3);
      })
      .then(() =&gt; {
        console.log(4);
        syncSleep(1000)
      })
      .then(() =&gt; {
        console.log(5);
      })
  
    const p2 = new Promise(resolve =&gt; {
     
      resolve(p1);
    })
  
    p2.then(v =&gt; console.log(v));

这段代码的实际结果和我预期的不一致。
我的预期是
begin
 1
then1
2
then2
3
4
5
但是实际结果是
begin
1
then1
2
3
4
then2
5
主要是 P1 变成接受状态（fullfill）后，P2 究竟何时 变成接受状态，这个时机没太懂</div>2021-05-10</li><br/>
</ul>