你好，我是宋一玮，欢迎回到React应用开发的学习。

前面两节课我们学习了React Hooks，加上前面第8节课学到的组件生命周期方法，这些API都可以用来编写组件逻辑。不过到目前为止，我们讲到的组件逻辑以展示为主，与用户的交互是偏单向的，而在实际项目中，Web应用也包含很多**双向交互**。实现双向交互的一个重要途径，就是**事件处理**。

在浏览器中，事件处理不是一个新鲜的概念。标准的DOM API中，有完整的DOM事件体系。利用DOM事件，尤其是其捕获和冒泡机制，网页可以实现很多复杂交互。

React里内建了一套名为**合成事件**（SyntheticEvent）的事件系统，和DOM事件有所区别。不过第一次接触到合成事件概念的开发者，常会有以下疑问：

- 什么是React合成事件？
- 为什么要用合成事件而不直接用原生DOM事件？
- 合成事件有哪些使用场景？
- 有哪些场景下需要使用原生DOM事件？

经过这节课的学习，你将了解到**合成事件的底层仍然是DOM事件，但隐藏了很多复杂性和跨浏览器时的不一致性**，更易于在React框架中使用。在 `oh-my-kanban` 出现过的受控组件，就是合成事件的重要使用场景之一。此外，我们还会利用其他合成事件为看板卡片加入拖拽功能，顺便了解一下合成事件的冒泡捕获机制。最后，我会介绍一些在React中使用原生DOM事件的场景。
<div><strong>精选留言（11）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/21/69/79/b4132042.jpg" width="30px"><span>🐑</span> 👍（0） 💬（0）<div>你好，我是《现代React Web开发实战》的编辑辰洋，这是👇项目的源代码链接，供你学习与参考：https:&#47;&#47;gitee.com&#47;evisong&#47;geektime-column-oh-my-kanban&#47;releases&#47;tag&#47;v0.11.0</div>2022-09-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/b9/d8/92c2b3ab.jpg" width="30px"><span>海华呀</span> 👍（3） 💬（1）<div>1、执行顺序 是父-子-父，有些洋葱圈模型的感觉 
&lt;div onClickCapture={() =&gt; console.log(1)} onClick={() =&gt;console.log(4)} &gt;
      &lt;p onClickCapture={() =&gt; console.log(2)} onClick={() =&gt; { console.log(3) }}&gt;
        target
      &lt;&#47;p&gt;
    &lt;&#47;div &gt; 
例如这个点击会依次打印出1、2、3、4；
阻止冒泡 一般是父子组件都对事件做了处理，例如 文章列表页 ，点赞按钮，和打开详情页面；
</div>2022-10-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/c9/f9/39492855.jpg" width="30px"><span>阿阳</span> 👍（1） 💬（1）<div>每节课的内容好多，全是干货。需要反复的听，看，动手实践。请问老师，每节课的课后习题有没有专门的章节做解答啊？</div>2022-11-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/a5/f4/9bf287ea.jpg" width="30px"><span>WL</span> 👍（1） 💬（1）<div>感觉老师讲得过于多内容了，看着挺花时间；可以简化些就更好了</div>2022-09-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e7/20/70a95f94.jpg" width="30px"><span>潮汐</span> 👍（0） 💬（3）<div>老师，想问一下，这节课的拖拽的例子，你的拖拽开始的时候，卡片会不会有一闪而过的卡片时间从status的时间变成相对时间的画面。分析了下，感觉像是KanbanCard的setDraggedItem触发了App的更新渲染，KanbanColumn和KanbanCard也会被重新渲染。但是draggedItem也并没有传给KanbanCard，为啥会触发KanbanCard的协调更新呢。</div>2023-01-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/5c/31/d7b92b6b.jpg" width="30px"><span>癡癡的等你歸</span> 👍（0） 💬（1）<div>老师，课程源码不见了，404了</div>2022-11-16</li><br/><li><img src="" width="30px"><span>Geek_8e9c8d</span> 👍（0） 💬（1）<div>已经开始期待以后开的项目课了
希望能得到省份和城市的那个思考题的更多提示~,谢谢</div>2022-10-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/19/64/6f2b7b86.jpg" width="30px"><span>01</span> 👍（0） 💬（2）<div>对目前发展来讲， 合成事件是否是个好的选择。 同时是否增加了开发的心智负担。 许多类react相关库不采用合成事件代替原生事件。</div>2022-09-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/a8/1e/4ec85e24.jpg" width="30px"><span>joel</span> 👍（0） 💬（1）<div>终于追上来了</div>2022-09-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/31/23/90/5dea860f.jpg" width="30px"><span>C0S_02</span> 👍（2） 💬（0）<div>老师您好，我一直没明白 合成事件 的必要性是什么，react 到底在解决什么需求</div>2023-05-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/a8/1e/4ec85e24.jpg" width="30px"><span>joel</span> 👍（0） 💬（0）<div>还没有更吗</div>2022-09-16</li><br/>
</ul>