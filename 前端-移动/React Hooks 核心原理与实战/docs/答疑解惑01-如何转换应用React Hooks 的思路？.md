你好，我是王沛。今天我们来对第一章的内容进行集中答疑。

不知不觉我们的基础篇已经讲完了，也很高兴看到你在交流区积极留言，提出了很多有意义的问题。所以这节课呢，我会针对一些具有代表性的问题，进行集中答疑。一方面算是对课程内容作一个有针对性的补充，另外一方面也希望能对更多的同学有所帮助。

我会先对评论区的提出的几个具有代表性的问题进行讲解，然后再对课程中的几个思考题，做一个回答参考，并给出代码示例。

# 留言区的问题

## [02讲](http://https://time.geekbang.org/column/article/378311)

问题：文中的例子里说，窗口大小发生变化，组件就会更新。对于这一点我不太理解，Class封装的还可以理解为，state发生改变了，导致重新render了，但Hooks感觉这么理解并不通顺，Hook哪里写得就类似一个纯函数调用，是怎么驱动组件重新更新的呢？

讲解：一个很好的问题，这是很多初学 Hooks 的同学都会有的困惑：一个普通函数怎么就让组件刷新了呢？其实答案也特别简单，那就是**自定义 Hooks 中也是通过 useState 这样的内置 Hook 来完成组件的更新的**。

可能你会觉得，自定义 Hooks 中一定会用到 state 吗？如果你写多了就会发现，自定义 Hooks 要实现的逻辑，要么用到 state，要么用到副作用，是一定会用到内置 Hooks 或者其它自定义 Hooks 的。
<div><strong>精选留言（9）</strong></div><ul>
<li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83epxnsPibclOEASgqLeRnJtwGwjeSygjD6RgPr60TibL03KVVAJAKf5u9g4LLg337uC9Cc2dDM4SnDcw/132" width="30px"><span>TMiRobot</span> 👍（1） 💬（1）<div>老师，React 文档提到“React 保证了 setState 函数标识是稳定的，并且不会在重渲染时改变，因此在 useEffect 和 useCallback 的依赖列表中忽略它是安全的。” 
useCallback(() =&gt; setCount(count - n), [count])
那像这种优化是不是没有必要，根本不需要再去包裹一层 useCallback</div>2021-06-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c0/99/259a412f.jpg" width="30px"><span>Geeker</span> 👍（9） 💬（0）<div>我是假期学习第一人</div>2021-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/46/3e/f9ae9462.jpg" width="30px"><span>盖世英雄</span> 👍（4） 💬（1）<div>hooks也用的两年了，一直都停留在使用，完成功能上！
没有深入了解过，感谢老师！</div>2021-06-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/07/d2/d7a200d5.jpg" width="30px"><span>小鸟淫太</span> 👍（2） 💬（2）<div>老师您好，我在网上看到说过度使用 useCallback 会对性能有影响。

https:&#47;&#47;blog.csdn.net&#47;weixin_47143210&#47;article&#47;details&#47;106193323</div>2021-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b1/84/d7034d7c.jpg" width="30px"><span>吴颜</span> 👍（0） 💬（0）<div>文中奖“但是始终使用 useCallback 是个比较好的习惯。”，这个感觉很难认同，而使用react过程中也确实极少使用useCallback，useCallback在函数组件中的作用我感觉与函数组件本身是有点格格不入的，我体验useCallback更多是为了保证react功能的完备性而推出的，是为了“解决问题”而非用来日常开发使用</div>2023-09-07</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTI7iakTvMwXWBHCK6WicIV2M3yQMZ8BtBgYgzARcEjbEtcWfKsQ2JqpZianKibZ2D7l1D3rwyTOL56Pzw/132" width="30px"><span>Jackchoumine</span> 👍（0） 💬（1）<div>副作用一定是和当前 render 的结果没关系的，而只是 render 完之后做的一些额外的事情？很不理解这里。为何说副作用和当前render 结果无关呢？ 比如接口发返回了，要重新设置 state 就是会触发重新渲染，就是和渲染结果相关的。 我时哪儿没有理解到位吗？</div>2023-06-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/f4/14/4599c47e.jpg" width="30px"><span>Jia添！</span> 👍（0） 💬（0）<div>补充 ：
useAction实际上不仅用起来麻烦且无法通过eslint-hooks检测，而且根据官方文档Dan的说法，不仅不符合hooks思想，也没有必要（因为函数式编程，hooks api是直接使用调用结果，甚至没有原先oop式独立的component中间层）。
所以useAction在最新的alpha版本中已经凉了。</div>2022-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/32/7a/1e95206c.jpg" width="30px"><span>micstone</span> 👍（0） 💬（0）<div>hooks</div>2021-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/13/ea/e95bc408.jpg" width="30px"><span>与你.</span> 👍（0） 💬（2）<div>逃不过万年老二</div>2021-06-14</li><br/>
</ul>