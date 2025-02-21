你好，我是宋一玮，欢迎回到React应用开发的学习。

上节课我们讲了什么是Hooks，React 18里都有哪些Hooks，然后深入学习了基础Hooks之一的 `useState` ，在结束前也介绍了 `useRef` 。

这节课我们紧接着来学习另一个基础Hook：`useEffect` ，以及用于组件性能优化的Hooks：`useMemo` 和 `useCallback` 。讲完这些Hooks，我们回过头了解一下所有React Hooks共通的使用规则。最后回答上节课一开始提到的疑问：

- 函数组件加Hooks可以完全替代类组件吗？
- 还有必要学习类组件吗？

好的，我们先从 `useEffect` 开始。

## 什么是副作用？

副作用（Side-effect，或简称Effect）这个概念在上节课已经多次出现了，你可能还是觉得迷惑，到底什么是副作用？

计算机领域的副作用是指：

> 当调用函数时，除了返回可能的函数值之外，还对主调用函数产生附加的影响。例如修改全局变量，修改参数，向主调方的终端、管道输出字符或改变外部存储信息等。  
> ——[《副作用（计算机科学）- 维基百科》](https://zh.wikipedia.org/zh-hans/%E5%89%AF%E4%BD%9C%E7%94%A8_%28%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%A7%91%E5%AD%A6%29)

总之，**副作用就是让一个函数不再是纯函数的各类操作**。注意，这个概念并不是贬义的，在React中，大量行为都可以被称作副作用，比如挂载、更新、卸载组件，事件处理，添加定时器，修改真实DOM，请求远程数据，在console中打印调试信息，等等。
<div><strong>精选留言（9）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/21/69/79/b4132042.jpg" width="30px"><span>🐑</span> 👍（0） 💬（1）<div>你好，我是《现代React Web开发实战》的编辑辰洋，这是👇项目的源代码链接，供你学习与参考：https:&#47;&#47;gitee.com&#47;evisong&#47;geektime-column-oh-my-kanban&#47;releases&#47;tag&#47;v0.10.0</div>2022-09-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/30/61/98/0d6b499d.jpg" width="30px"><span>船长</span> 👍（2） 💬（2）<div>不是很理解 useMemo 那个例子，比如用 下面这个useEffect  写法不是也可以持久化记忆数据吗？好像只是比 useMemo 那种写法多了个 setXXX 所造成的一次渲染？
const [num, setNum] = useState(&quot;0&quot;);
  const [num2, setNum2] = useState(&quot;0&quot;);
  useEffect(() =&gt; {
    const n = parseInt(num, 10);
    setNum2(fibonacci(n));
  }, [num]);</div>2022-09-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/4f/39/791d0f5e.jpg" width="30px"><span>学习前端-react</span> 👍（2） 💬（3）<div>请问：use Effect 的执行是可以拿到真实dom的，那为啥在图中提交阶段却是在真实dom之前？</div>2022-09-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5b/25/d78cc1fe.jpg" width="30px"><span>都市夜归人</span> 👍（1） 💬（4）<div>
const KanbanCard = ({ title, status }) =&gt; {
  const [displayTime, setDisplayTime] = useState(status);
  useEffect(() =&gt; {
    const updateDisplayTime = () =&gt; {
      const timePassed = new Date() - new Date(status);
      let relativeTime = &#39;刚刚&#39;;
      &#47;&#47; ...省略
      setDisplayTime(relativeTime);
    };
    const intervalId = setInterval(updateDisplayTime, UPDATE_INTERVAL);
    updateDisplayTime();

    return function cleanup() {
      clearInterval(intervalId);
    };
  }, [status]);
可以看到，useEffect 接收了副作用回调函数和依赖值数组两个参数，其中副作用回调函数的返回值也是一个函数，这个返回的函数叫做清除函数。组件在下一次提交阶段执行同一个副作用回调函数之前，或者是组件即将被卸载之前，会调用这个清除函数。

没有看懂，上面的哪有两个参数啊？
</div>2022-09-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/1b/0c/e236e8c2.jpg" width="30px"><span>满眼星🌟 辰🍊</span> 👍（0） 💬（1）<div>图例中，useLayoutEffect是同步更新dom，应该在useEffect之前执行，不是吗</div>2022-09-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5b/25/d78cc1fe.jpg" width="30px"><span>都市夜归人</span> 👍（0） 💬（2）<div>其实这两个 Hooks 与 useEffect 并不沾亲带故。且不说它们的用途完全不同，单从回调函数的执行阶段来看，前者是在渲染阶段执行，而后者是在提交阶段。

这句话与上面的生命周期图不太一致，求解惑</div>2022-09-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/e2/8e/b4ccfa02.jpg" width="30px"><span>Imart</span> 👍（2） 💬（0）<div>useEffect 是在浏览器渲染&#47;呈现dom内容后执行的；
useLayoutEffect 是在真实dom更新后，浏览器渲染dom内容前执行的，即在render函数执行后，接着同步马上执行回调函数内容；</div>2022-11-15</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eor68N3pg8Joqw3XH1EkFjmLVK5fkKokj1025XjR4va1CW8CdsKSytbw3f4WPjIbiazEbACOibNDnnA/132" width="30px"><span>Geek_9y01z7</span> 👍（0） 💬（0）<div>我试图在 handleSubmit 里调用 handleSaveAll()，希望每次新增“待处理” 后自动保存，但失败了。调用 handleSaveAll 的时候 todoList 还没有被更新，第二次新增后才会把第一次新增的保存进去，这是为什么呢 ？

const handleSubmit = (title) =&gt; {
    const d = new Date()
    const n = d.toLocaleDateString().replace(&#39;&#47;&#39;, &#39;-&#39;) + &#39; &#39; + d.toLocaleTimeString();
    setTodoList(currentTodoList =&gt; [
      { title, dt: n},
      ...currentTodoList
    ]);
    
    handleSaveAll()
  };</div>2023-07-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c0/99/259a412f.jpg" width="30px"><span>Geeker</span> 👍（0） 💬（1）<div>个人觉得框架不应该把“负担” 甩给用户</div>2022-11-04</li><br/>
</ul>