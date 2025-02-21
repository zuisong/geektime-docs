你好，我是王沛。今天我们来聊聊React还有哪些值得期待的新特性。

React 自诞生到现在，已经有七八年的时间了，不知道你是不是和我有一样的疑惑。React 好像这么多年来就发布了一个 React Hooks，除此之外就没有什么其他新功能了。那么，React 团队到底在做哪些事情呢？其实我们只要仔细想一想，这个疑惑也挺容易解开。

一方面，React 的 API 足够稳定，这就让我们开发人员不太能感知到一些内部的优化。比如在2017年，React 就基于 Fiber 的架构重写了整个 React，优化了渲染的机制，为之后的 Suspense 等特性提供了基础。

另一方面，React 团队其实一直在探索一些新的前端开发方式，只是不到足够成熟就不会正式发布。比如 Suspense，作为一个试验特性，它已经推出有三年多了，但官方一直没有宣布正式可用。而最近提出的一个新的服务器端组件的概念，虽然让人眼前一亮，但同样也还处于探索和开发阶段。

不过，了解React 17.0版本，还是十分有必要的，能让我们对 React 的未来会有哪些新特性，做到心中有数。

所以今天这节课，我们就来看下 React 17.0 这个没有新特性的版本带来了什么新变化。然后再通过例子，去学习 Suspense 和服务器端组件，看看它们究竟是什么，试图去解决哪些问题。
<div><strong>精选留言（11）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/cf/7a/3c37260a.jpg" width="30px"><span>竹杖</span> 👍（21） 💬（3）<div>看完专栏感觉稍微有点失落，这就结束了？本想着有些Hook的内部深入解析之类的，感觉还是停留在api使用的层面上，入门吧</div>2021-07-14</li><br/><li><img src="" width="30px"><span>Geek_413aa8</span> 👍（3） 💬（1）<div>react 18 Alpha 版本不是已经发布了；希望老师给讲解一下</div>2021-07-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/43/cf/118c4ef5.jpg" width="30px"><span>lunar</span> 👍（1） 💬（2）<div>从视频追到专栏， 这又双双双结束了？</div>2021-07-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/57/f4/63c3c5ae.jpg" width="30px"><span>Dark I</span> 👍（0） 💬（1）<div>这就结束了 好快啊</div>2021-07-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/43/cf/118c4ef5.jpg" width="30px"><span>lunar</span> 👍（4） 💬（0）<div>从视频追到专栏，这又双叒叕要结束了？我一个做后端的也不知道为啥对这门课这么感兴趣， 莫非是老师讲得太好了！😂</div>2021-07-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/fc/c3/0991edfc.jpg" width="30px"><span>闲闲</span> 👍（2） 💬（2）<div>老师我有几个问题咨询下
1、对于事件冲突，其实我没有太理解，我记得用addeventLicense监听的事件，即便是同一个dom绑定也是不会冲突的，那怎么来说，事件应该不会冲突吧，是有其他场景或者应该是我对事件理解不深，还请老师解答
2、对于服务器端渲染的问题，react是状态驱动的，服务器端渲染的话，这个状态驱动是怎么实现的呢？另外对于一些复杂界面，状态可能很复杂也很容易变化，那服务器端渲染会不会给服务器造成压力呢？</div>2021-07-11</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eotuhVFN9phZsthxdS2bBAV9Cjb1NqIFbSQhiclmtsUDCn1cOKrzU8Ie1ickxlWC4kIlI3S69XrST7w/132" width="30px"><span>Geek_4e92cc</span> 👍（1） 💬（0）<div>问个问题：class组件中 this.foreUpdate(), 是当前组件重新render 还是 整个组件树重新render？</div>2022-05-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/04/8e/e75ecc5e.jpg" width="30px"><span>浩明啦</span> 👍（1） 💬（0）<div>在微前端里，多个 react 16 的微应用可能会出现问题</div>2021-07-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/3c/88/6bef27d6.jpg" width="30px"><span>大神博士</span> 👍（0） 💬（0）<div> Suspense 很奇怪哎，是不是会造成 ui 页面的闪烁，突然一个 fallback 的 loading</div>2022-02-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/e1/8a/df410c85.jpg" width="30px"><span>七秒</span> 👍（0） 💬（0）<div>这就结束了 意犹未尽，老师讲得很好！</div>2021-10-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/fc/c3/0991edfc.jpg" width="30px"><span>闲闲</span> 👍（0） 💬（0）<div>我还有个疑问麻烦老师解答：
1、suspense 怎么区分那个异步逻辑对于那个组件呢？按照例子觉得 ，将TopicDetail这个组件包裹在了suspent里面，那如果有多个请求呢，每个组件都包裹在suspense里面吗？还是怎么操作的？</div>2021-07-11</li><br/>
</ul>