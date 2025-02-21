你好，我是蒋宏伟。

今天这一讲，我要和你聊的是，如何使用 Redux 来管理复杂的、大型的应用状态。

有人认为，在 React 出了 hooks 之后，官方提供的 useReducer 和 useContext 的组合，已近似能够代替 Redux 了，所以，现在是时候抛弃 Redux，直接用 useReducer 和 useContext 对大型应用进行状态管理了。

也有人认为，虽然 Redux 解决了状态管理的问题，但是 Redux 模板代码太多，应该抛弃 Redux，改用 Mobx 或 Zustand 这类写起来更简单的工具。

但我认为，从目前来看，Redux 依旧是我们开发大型项目时，应该最优先考虑的状态管理工具。为什么呢？

一方面，大型项目的状态管理复杂度很高，useContext 并不是状态管理工具，它只是一个提供了跨层级传递状态的工具而已。真要拿 useReducer 和 useContext 来写大型项目，你需要写更多的模板代码，而且更难维护。

另一方面，开发大型项目需要考虑团队成员的协作成本，目前来看，无论是 [npm trends 上的下载量](https://www.npmtrends.com/mobx-vs-redux-vs-zustand)，还是我对 React Native 开发者的[调研报告](https://segmentfault.com/a/1190000041324009)都显示，Redux 的流行程度远超于其他状态管理工具。团队招一个新人，新人熟悉 Redux 概率远比熟悉 Mobx、Zustand 的概率更高，学习成本、协作成本也是最低的。
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="" width="30px"><span>Geek_4e11e2</span> 👍（0） 💬（0）<div>现在最新的react native版本是0.71. 我的app是0.63.4版本，请问老师，建议升级到那个版本比较好。在升级时候，需要注意哪些事项。</div>2023-06-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/96/87/bbdeb4ee.jpg" width="30px"><span>杨永安</span> 👍（0） 💬（0）<div>想知道在react native中，所有的js代码都是在同一个上下文的js运行时中吗？

否则Redux这种对象数据是如何跨页面共享的。

因为我之前接触到的是多个WebView这样的，他们的数据不能共享</div>2023-04-14</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83epfMaQHtCXaQkepugPQb4P9GYdPQzo6LiahxosVPtjjg8hKhcq1d9PTnODZQ6STa1XqxFvVHjJvhfw/132" width="30px"><span>海绵豹豹</span> 👍（0） 💬（1）<div>用FB的Recoil吧, Redux太啰嗦了而且心智负担较高</div>2022-10-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/cc/1d/3c0272a1.jpg" width="30px"><span>abc🙂</span> 👍（0） 💬（1）<div>能不能讲讲全局状态的场景，感觉很多情况不需要redux</div>2022-06-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/9d/5f/06671a0d.jpg" width="30px"><span>python4</span> 👍（0） 💬（0）<div>函数命名上加一点redux概念是否更好, 方便新手牢记概念, 比如: filter -&gt; filterReducer</div>2022-05-14</li><br/>
</ul>