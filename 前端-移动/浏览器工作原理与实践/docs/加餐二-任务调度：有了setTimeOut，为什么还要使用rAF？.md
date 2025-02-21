你好，我是李兵。

我们都知道，要想利用JavaScript实现高性能的动画，那就得使用requestAnimationFrame这个API，我们简称rAF，那么为什么都推荐使用rAF而不是setTimeOut呢？

要解释清楚这个问题，就要从渲染进程的任务调度系统讲起，理解了渲染进程任务调度系统，你自然就明白了rAF和setTimeOut的区别。其次，如果你理解任务调度系统，那么你就能将渲染流水线和浏览器系统架构等知识串起来，理解了这些概念也有助于你理解Performance标签是如何工作的。

要想了解最新Chrome的任务调度系统是怎么工作的，我们得先来回顾下之前介绍的消息循环系统，我们知道了渲染进程内部的大多数任务都是在主线程上执行的，诸如JavaScript执行、DOM、CSS、计算布局、V8的垃圾回收等任务。要让这些任务能够在主线程上有条不紊地运行，就需要引入消息队列。

在前面的《[16 | WebAPI：setTimeout是如何实现的？](https://time.geekbang.org/column/article/134456)》这篇文章中，我们还介绍了，主线程维护了一个普通的消息队列和一个延迟消息队列，调度模块会按照规则依次取出这两个消息队列中的任务，并在主线程上执行。为了下文讲述方便，在这里我把普通的消息队列和延迟队列都当成一个消息队列。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/aFAYPyw7ywC1xE9h1qibnTBwtWn2ClJqlicy5cMomhZVaruMyqSq76wMkS279mUaGhrLGwWo9ZnW0WCWfmMovlXw/132" width="30px"><span>木瓜777</span> 👍（35） 💬（2）<div>window.requestAnimationFrame 应该是在每一帧的开始就执行吧？</div>2019-11-29</li><br/><li><img src="" width="30px"><span>Geek_0d3179</span> 👍（16） 💬（1）<div>如果raf的回调任务会在每一帧的开始执行，如果它执行时间很长（超过一帧），那就会阻碍后面所有任务的执行么？比如说用户的交互事件等高优先级任务也会受到影响导致卡顿么？
我在网上看到的资料：为啥是先执行用户的交互任务，在执行raf的回调？？？</div>2019-12-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/af/b3/3486dea2.jpg" width="30px"><span>gigot</span> 👍（6） 💬（3）<div>老师，我想问下在 primose.then 中执行宏任务（setTimeout或 ajax），其中该宏任务应该加入哪个事件队列。
是说微任务队列都是按顺序执行，其中每个微任务又有新的事件循环（包括宏任务和微任务），类似于新得全局环境，这样理解对吗</div>2019-11-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/f8/0d/0afa80d4.jpg" width="30px"><span>王博</span> 👍（0） 💬（3）<div>觉得老师的绘图工具挺好的，老师可以推荐一下吗？谢谢</div>2019-11-26</li><br/><li><img src="" width="30px"><span>wens</span> 👍（12） 💬（1）<div>react fiber的实现应该是借鉴了chromium的消息队列机制</div>2020-05-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/95/2e/332fee49.jpg" width="30px"><span>刘弥</span> 👍（8） 💬（0）<div>老师的图其实已经给出了答案，VSync 的开始就会执行 RAF 的回调。</div>2020-02-18</li><br/><li><img src="" width="30px"><span>Geek_0d3179</span> 👍（8） 💬（3）<div>老师您好~ 在网上搜了一大圈之后还是存在疑惑，非常希望您的解惑~十分感谢！
1、我了解到event loop的流程是：一个macrotask &gt;&gt; UI 渲染 &gt;&gt; 任务队列取下一个macrotask
疑问：每执行一个macrotask后面一定会UI 渲染吗？如果此时DOM和样式并没有改变，根本不需要重新渲染呢？也就是根本不需要回流、重绘和合成。
2、听了老师的讲解后，得知渲染进程在每一帧时间里都会重新绘制，合成一帧图片推到后缓冲区，就算UI没有变化也会执行吗？那这个执行的时机是？是得到VSync信号的时候吗？那这是作为一个宏任务执行的吗？
3、我并没有搞清楚上面1和2的关系。也就是event loop 和 一帧时间的关系。我的理解：在一帧的时间里会不断的从任务队列中取出任务执行，那如果任务队列有太多任务，“重新绘制一帧推到后缓冲区”这个操作会被延迟吗？
</div>2019-12-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/b5/6c/18c5b2ed.jpg" width="30px"><span>一七</span> 👍（6） 💬（0）<div>https:&#47;&#47;www.bilibili.com&#47;video&#47;BV1K4411D7Jb?spm_id_from=333.1007.top_right_bar_window_default_collection.content.click
强烈推荐大家看一下这个视频，讲事件循环的</div>2022-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/be/3d/2d2cc4fa.jpg" width="30px"><span>Trust_</span> 👍（3） 💬（0）<div>&lt;html&gt;
&lt;head&gt;
  &lt;title&gt;Main&lt;&#47;title&gt;
  &lt;style&gt;
    .test {
      width: 100px;
      height: 100px;
      background-color: royalblue;
    }
  &lt;&#47;style&gt;
&lt;&#47;head&gt;
&lt;body&gt;
  &lt;button&gt;点击&lt;&#47;button&gt;
  &lt;div class=&quot;test&quot;&gt;&lt;&#47;div&gt;
  &lt;script&gt;

    document.querySelector(&#39;button&#39;).addEventListener(&#39;click&#39;, () =&gt; {
      const test = document.querySelector(&#39;.test&#39;);
      test.style.transform = &#39;translate(400px, 0)&#39;;

      requestAnimationFrame(() =&gt; {
        test.style.transition = &#39;transform 3s linear&#39;;
        test.style.transform = &#39;translate(200px, 0)&#39;;
      });
    });

  &lt;&#47;script&gt;
&lt;&#47;body&gt;
&lt;&#47;html&gt;


这段代码在Chrome执行之后，元素是从右往左移动的，说明是先绘制然后才执行的rAf
在火狐执行之后相反，是从右往左移动的

老师能解答一下吗</div>2021-07-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/72/35/e21d4fe8.jpg" width="30px"><span>暖桔灯笼</span> 👍（3） 💬（1）<div>老师，在 宏任务与微任务 那一章的讲解中，下面有一个您的回答说在浏览器的实现中目前只实现了一个消息队列和一个延迟队列？这和这里第二次迭代--根据消息类型来实现消息队列 说法是不是冲突？如果确实实现了多个消息队列，会不会跟之前说的&quot;循环系统的一个循环中，先从消息队列头部取出一个任务执行，该任务执行完后，再去延迟队列中找到所有的过期任务依次执行完&quot;有冲突？我现在有点迷惑浏览器到底实现了几个几个消息队列？囧。。。</div>2020-05-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/57/a9/9abbe7a4.jpg" width="30px"><span>神三元</span> 👍（2） 💬（13）<div>讲的有问题，rAF的回调在微任务执行完成之后才会进行</div>2020-03-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/c2/63/e91ba1c4.jpg" width="30px"><span>猫叔</span> 👍（2） 💬（3）<div>老师，通过window.postMessage 发送的消息执行回调也是在空闲时间内执行的吗。因为我看到react框架为了模拟兼容requestIdleCallback。使用了postMessage</div>2019-12-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/91/09/6f0b987a.jpg" width="30px"><span>陈坚泓</span> 👍（1） 💬（0）<div>标题的 setTimeOut 是固定把小写的o改为大写的 O 嘛   setTimeout</div>2022-11-14</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/MYShyjtRtib2GIQiaK4hV3ZP9pQ1qiaS74DA4K4YHY4SIiaFDfsCKgiaMWwm9zFsSn3bt5pawp5Kdn5MWgiaw5909nug/132" width="30px"><span>Geek_aa1c31</span> 👍（1） 💬（1）<div>这里有一篇将eventloop，rAF, rIC的文章， 强烈建议可以去看一下。
https:&#47;&#47;developpaper.com&#47;in-depth-analysis-of-event-loop-and-browser-rendering-frame-animation-idle-callback-animation-demonstration&#47;</div>2022-07-03</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqKk79X0JKQ5kyPQCnGN5BibI0wsOSAIp7gAhY0FlIukt7K1BJ2nibEpiciba1Rb6bk5Tl7AlhRjdBrsw/132" width="30px"><span>Geek_88dd24</span> 👍（1） 💬（1）<div>老师有个问题，如果浏览器在下一次收到vsyncA信号时，上次绘制还没完成，那么浏览器会怎么处理这个vsyncA</div>2022-01-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/de/ff/8b3b2e87.jpg" width="30px"><span>Clfeng</span> 👍（0） 💬（0）<div>不过大多数任务需要保持其相对执行顺序，如果将用户输入的消息或者合成消息添加进多个不同优先级的队列中，那么这种任务的相对执行顺序就会被打乱，甚至有可能出现还未处理输入事件，就合成了该事件要显示的图片。因此我们需要让一些相同类型的任务保持其相对执行顺序。

老师请问下这里所提出的问题在下个模型中怎么被解决的？感觉不是很理解；在这种优先级消息队列模型下，用户的输入事件和合成事件因被放入了不通的消息队列而无法保障相对的执行顺序。但是在下面根据消息类型类实现消息队列的模型中，用户的输入事件是放到交互事件这一消息队列中去的，合成事件是放在合成事件队列中去的，这两个消息队列依旧有不同的优先级，这样的话跟前面的模型也差不多，提到的两个事件都是放到不同的消息队列中，并且这两类消息队列也都有相对的优先级，实在没看出来问题怎么得到解决的</div>2024-07-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡</div>2024-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/63/14/06eff9a4.jpg" width="30px"><span>Jerry银银</span> 👍（0） 💬（0）<div>让我想起了操作系统的进程调度问题</div>2022-07-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e4/39/a06ade33.jpg" width="30px"><span>极客雷</span> 👍（0） 💬（0）<div>headless chrome</div>2022-06-26</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLfhZXC5a4ibMpVy0x7IEOicYrqEribFUDHdBc3DENR3pQicD3Bmobh7wmwcXY4xkVzjOUl5jVEiaala6w/132" width="30px"><span>Geek_850f66</span> 👍（0） 💬（0）<div>对我前端技术影响最深远的一门课程，没有之一，非常感谢。希望老师可以出本书，一定会购买，反复阅读体会</div>2022-03-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/93/36/abb7bfe3.jpg" width="30px"><span>Hhpon</span> 👍（0） 💬（0）<div>所以当我们代码中包含触发重排操作的时候，是不是也会等到收到sync信号的时候再去重新绘制呢。</div>2022-03-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/6a/22/527904b2.jpg" width="30px"><span>hao-kuai</span> 👍（0） 💬（0）<div>从关键渲染路径的角度来看，rAF 回调的执行时机用来做合适修改，有助于减少回流的次数</div>2021-12-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/48/65/3277386b.jpg" width="30px"><span>刘至</span> 👍（0） 💬（0）<div>浏览器渲染进程主线程任务调度

在单消息队列架构下，存在着低优先级任务会阻塞高优先级任务的情况，也就是队首阻塞问题。

为了解决此问题：
1. 引入优先级队列，高优先级任务队列中的任务先执行，并且为不同类型的任务创建不同优先级的消息队列。目的是为了方便调整一类任务的优先级。

2.动态调整消息队列优先级，以满足页面加载阶段、用户交互阶段、空闲阶段不同场景下的不同需求。

3. 为解决饥饿问题，给每个队列设置权重，在某个优先执行的高优先级消息队列的任务执行到一定个数，间或执行低优先级任务。

中间穿插了Vsync的知识
1. 显示器按照一定频率，通常是60HZ，从显卡的缓冲区读取浏览器生成的图像来呈现画面，这里使用双缓存技术解决图像闪烁问题。
2. 当浏览器生成图像频率和显示器读取图像不一致，会造成不连贯的问题，具体表现在浏览器生成图像频率慢则卡顿、快则丢帧。
3.为同步浏览器与显示器的频率，显示器会在读取下一帧图像前，发送垂直同步信号 VSync 给到 Gpu，Gpu给到 浏览器进程，浏览器进程给到渲染进程，渲染进程收到信号后着手准备新一帧图像的生成，收到信号前的空闲阶段则可以处理低优先级任务（垃圾回收，rI）。
4. rAF回调函数 发生在渲染进程接受到 VSync 信号之后，绘制下一帧图像（style计算，layout）之前。</div>2021-10-15</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJS0jwYKhjm1hq96go05J4R7XDd5FFXXaoyIfX9TgoI3mLURAu2ET72SvYGM2iaET7IV3WDvMibAVfw/132" width="30px"><span>tokey</span> 👍（0） 💬（2）<div>老师您好！想请教下：
1、requestAnimationFrame 是宏任务么？如果不是，那它属于什么呢？
2、
setTimeout(() =&gt; {console.log(&#39;setTimeout&#39;)})
requestAnimationFrame(() =&gt; {console.log(&#39;requestAnimationFrame&#39;)})
requestIdleCallback(() =&gt; {console.log(&#39;requestIdleCallback&#39;)})
多次执行，他们的顺序都是不确定的，如何用“宏任务的执行”和“浏览器的渲染”结合着去解释他们的执行顺序呢？
</div>2021-05-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/c9/d5/b08a27ed.jpg" width="30px"><span>灵感_idea</span> 👍（0） 💬（0）<div>一直看课程的到现在，明显感觉到这就像是平时我们开发项目一样，初始版本总是个最小产出的东西，当遇到某种问题（或者用户，或者测试）再去在先前的版本上去做适当优化，挺好~</div>2021-01-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/27/72/1be6dbb0.jpg" width="30px"><span>老人与海</span> 👍（0） 💬（0）<div>李老师好，请教一个问题，为什么打开一个标签页时，有4个RenderFrameHostIMPL对象被创建。但是打开的同源标签页，却只创建3个。
创建的这3，4个对象，分别有什么功能呢？
有什么资料可以去学习吗？</div>2020-11-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/08/6c/789b8583.jpg" width="30px"><span>水鱼兄</span> 👍（0） 💬（0）<div>老师你之前说虽然标准里面定义了很多类型的消息队列，但是实现的时候只有两种，但是这里又突然多了很多的消息队列，所以哪一个才是对的？</div>2020-08-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/c0/fa/61f78abd.jpg" width="30px"><span>Geek_012295</span> 👍（0） 💬（0）<div>raf保证在接收到vsync信号时开始执行，而setTimeout异步回调的执行时机却是不确定的，如果采用setTimeout则会造成fps的不稳定出现掉帧或者丢帧</div>2020-08-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ec/13/49e98289.jpg" width="30px"><span>neohope</span> 👍（0） 💬（0）<div>0. 消息循环和消息队列（没有优先级）
1. 引入带优先级的队列，并引入任务调度器（采用不同队列区分优先级，优先处理高优先级队列任务）
2. 不同消息类型，优先级不同（不同消息类型，不同静态优先级，优先处理高优先级任务）
3. 不同阶段，不同消息类型，不同优先级（根据阶段，不同消息类型，动态调整优先级，优先处理该阶段高优先级任务）
4. 防止饥饿（动态升高饥饿任务优先级）</div>2020-07-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/de/20/03130a39.jpg" width="30px"><span>沧海一声笑</span> 👍（0） 💬（0）<div>L老师，我想请教下：

浏览器页面没有任何变化也会以每隔16ms左右进行 UI render吗
执行一个宏任务就会触发一次UI render吗 （UI render里面不是也会产生很多宏任务 嗯嗯...这样一想不是一个死循环吗）
16ms的相对时间怎么计算的，我怎么知道我这个交互触发是更好在一个16ms周期进行时，还是结束时

上述问题困扰我很久了，请老师解答</div>2020-07-18</li><br/>
</ul>