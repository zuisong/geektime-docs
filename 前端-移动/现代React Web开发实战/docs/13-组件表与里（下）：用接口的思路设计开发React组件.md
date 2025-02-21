你好，我是宋一玮，欢迎回到React应用开发的学习。

上节课一开始就提到了，我们会用两节课的时间学习组件的“面子”和“里子”。那你可能会问了，上节课讲到的React单向数据流算是“面子”还是“里子”呢？我先卖个关子，学完这节课你就有答案了。

在面向对象编程实践中，接口就是天然的“面子”，接口实现就是“面子”后面的“里子”。那么这节课，我们就要借鉴面向接口编程的思路，一边探讨在React应用开发中接口会以什么形式存在，一边继续上节课的 `oh-my-kanban` 大重构。在这节课的后半段，我们还会为 `oh-my-kanban` 加入基础的管理员功能。

当学习完这节课，你会对React组件的分工和交互有更深入的理解，同时也会收获一个好用的看板应用。

下面我们开始这节课的内容。

## 面向接口编程

现代软件编程的一大最佳实践是面向接口编程。**所谓软件接口**（Software Interface）**，就是两个或多个模块间用来交换信息的一个共享的边界**。

前端组件也有接口的概念，不同框架对接口的定义和使用都有所不同。这里举三个例子。

第一个例子，Angular里的Form，是一个命令式接口，开发者一般不需要自己实现它，因为Angular框架里已经内置了实现：
<div><strong>精选留言（15）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/30/61/98/0d6b499d.jpg" width="30px"><span>船长</span> 👍（1） 💬（3）<div>反馈个 Bug：文章里的 KanbanCard 判断是否展示删除按钮时，isAdmin 会始终为 True，因为从 useContext 引出来后，其值是：{isAdmin:false}，是个 obj，始终为 true，删除按钮会一直显示</div>2022-09-26</li><br/><li><img src="" width="30px"><span>Geek_a19712</span> 👍（0） 💬（2）<div>代码是不是写错了，上边 KanbanCard 删除的方法传的是 title ，但是在 App.js 中的 handleRemove 方法中过滤的条件是 item.title !== cardToRemove.title ，所以是不是应该把 KanbanCard  删除方法改成传 props 或者 App.js 中过滤条件 item.title !== cardToRemove.title 改成 item.title !== cardToRemove</div>2023-08-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/6a/42/51c5db2b.jpg" width="30px"><span>网瘾少年</span> 👍（0） 💬（1）<div>M
https:&#47;&#47;github.com&#47;xzxldl55&#47;FE-collection&#47;tree&#47;main&#47;task-board</div>2023-07-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/dc/bd/ea9c16b8.jpg" width="30px"><span>莫比斯</span> 👍（0） 💬（1）<div>M_M</div>2023-07-16</li><br/><li><img src="" width="30px"><span>Geek_b8f92f</span> 👍（0） 💬（1）<div>请问老师： 代码中有大量的onDragStart &amp;&amp; onDragStart(evt)这种写法
为什么不是直接写成onDragStart(evt)，
这么写的好处是什么，谢谢</div>2023-06-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/1d/59/8abc559e.jpg" width="30px"><span>进击的莫莫哒</span> 👍（0） 💬（1）<div>M</div>2022-10-16</li><br/><li><img src="" width="30px"><span>Geek_8e9c8d</span> 👍（0） 💬（1）<div>M</div>2022-10-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/a5/f4/9bf287ea.jpg" width="30px"><span>WL</span> 👍（0） 💬（1）<div>老师讲得很好，组件也可以看作是接口，我们通过props传入一些内容，组件帮我们实现一些功能，组件不负责保存上级组件的状态</div>2022-09-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/30/61/98/0d6b499d.jpg" width="30px"><span>船长</span> 👍（0） 💬（2）<div>思考题 2：
父-子通信：props，context
子-父通信：props.callback()   --（查课外资料）
兄弟通信：context</div>2022-09-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/30/61/98/0d6b499d.jpg" width="30px"><span>船长</span> 👍（0） 💬（1）<div>思考题 1：有父子、祖孙之间的 props 传递流，也有组件内部的 state 数据流，也有 context 共享数据流（可以忽略 props 的层层传递，直接一步到位）</div>2022-09-26</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/rE4T58OUZcO6DcnaR4QFLV3FItDQKicHqOyBGvAj9oYDsVuH4y8RbBJ2fgWQAEoic7nW6UjibKOSFehPnQBzDiaB0hJKviafb7LlWRwY4UbkgFM4/132" width="30px"><span>Geek_0af63d</span> 👍（0） 💬（0）<div>M</div>2024-07-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/54/2c/2739427d.jpg" width="30px"><span>Tanya</span> 👍（0） 💬（0）<div>M</div>2023-08-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2d/ca/7c/98193e9e.jpg" width="30px"><span>奕晨</span> 👍（0） 💬（0）<div>M</div>2023-06-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/83/16/59e5ba00.jpg" width="30px"><span>secondmax</span> 👍（0） 💬（1）<div>不知道是不是我code的有问题 按照流程走的 但是项目报错 然后自己查漏补缺 将KanbanBoard.js文件中 ’done&#39;的KanbanColumn的onRemove事件有原来透传的onRemove改成了onDrop，并且在app.js中改写了筛选 从而解决了报错并删不掉已完成card的事件
 `
&lt;KanbanColumn
        bgColor={COLUMN_BG_COLOR.done}
        title={&#39;已完成&#39;}
        setDraggedItem={setDraggedItem}
        setIsDragSource={(isSrc) =&gt; setDragSource(isSrc ? COLUMN_KEY_DONE : null )}
        setIsDragTarget={(isTgt) =&gt; setDragTarget(isTgt ? COLUMN_KEY_DONE : null )}
        onDrop={handleDrop}
        cardList={doneList}
        onRemove={onDrop.bind(null, COLUMN_KEY_DONE)}
      &gt;
      &lt;&#47;KanbanColumn&gt;`
`const handleRemove = (column, cardToRemove) =&gt; {
    updaters[column]((currentStat) =&gt; {
      console.log(currentStat, &#39;展示的东西&#39;, cardToRemove);
      return currentStat.filter((item) =&gt; item.title !== cardToRemove.title)
    });
  };
`还望能够指正一下</div>2023-04-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/96/87/bbdeb4ee.jpg" width="30px"><span>杨永安</span> 👍（0） 💬（1）<div>初学者请问一下老师，handleRemove这个方法相当于是在爷爷组件中，想在孙子组件中调用，只能通过props一级一级的传递到孙子组件去吗？还有没有其他优雅的做法？
直接 export 可行否</div>2023-03-13</li><br/>
</ul>