你好，我是王沛。这节课我们来继续学习内置 Hooks 的用法。

在上节课你已经看到了 useState 和 useEffect 这两个最为核心的 Hooks 的用法。理解了它们，你基本上就掌握了 React 函数组件的开发思路。

但是还有一些细节问题，例如事件处理函数会被重复定义、数据计算过程没有缓存等，还都需要一些机制来处理。所以在这节课，你会看到其它四个最为常用的内置 Hooks （包括useCallback、useMemo、useRef和useContext）的作用和用法，以及如何利用这些 Hooks 进行功能开发。

# useCallback：缓存回调函数

在 React 函数组件中，每一次 UI 的变化，都是通过重新执行整个函数来完成的，这和传统的 Class 组件有很大区别：函数组件中并没有一个直接的方式在多次渲染之间维持一个状态。

比如下面的代码中，我们在加号按钮上定义了一个事件处理函数，用来让计数器加1。但是因为定义是在函数组件内部，因此在多次渲染之间，是无法重用 handleIncrement 这个函数的，而是每次都需要创建一个新的：

```
function Counter() {
  const [count, setCount] = useState(0);
  const handleIncrement = () => setCount(count + 1);
  // ...
  return <button onClick={handleIncrement}>+</button>
}
```

你不妨思考下这个过程。每次组件状态发生变化的时候，函数组件实际上都会重新执行一遍。在每次执行的时候，实际上都会创建一个新的事件处理函数 handleIncrement。这个事件处理函数中呢，包含了 count 这个变量的闭包，以确保每次能够得到正确的结果。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1d/3a/8d/f5e7a20d.jpg" width="30px"><span>何以解忧</span> 👍（19） 💬（9）<div>关于子组件props 不变，可以减少不必要的渲染问题，不是特别理解。似乎只要父组件重新渲染子组件必然重新渲染，是内部有什么别的地方优化么？</div>2021-06-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/0f/a2/2bb7df25.jpg" width="30px"><span>满月</span> 👍（69） 💬（3）<div>我们能否用 state 去保存 window.setInterval() 返回的 timer 呢？
我理解的是可以，只是没有 useRef 更优，因为在更新 state 值后会导致重新渲染，而 ref 值发生变化时，是不会触发组件的重新渲染的，这也是 useRef 区别于 useState 的地方。</div>2021-06-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ee/44/26ac883e.jpg" width="30px"><span>桃翁</span> 👍（29） 💬（6）<div>useRef 如果只是用来 在多次渲染之间共享数据，是不是直接可以把变量定义到组件外面，这样也可以达到目的，感觉还更方便一点呢。</div>2021-06-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/2c/64/2a185538.jpg" width="30px"><span>cyh41</span> 👍（15） 💬（6）<div>是任何场景 函数都用useCallback 包裹吗？那种轻量的函数是不是不需要？</div>2021-06-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/f8/f6/3e2db176.jpg" width="30px"><span>七月有风</span> 👍（7） 💬（2）<div>问下老师，useCallback、useMemo 和 useEffect的依赖机制一样吗？都是浅比较吗？</div>2021-06-03</li><br/><li><img src="" width="30px"><span>Geek_71adef</span> 👍（6） 💬（1）<div>1 useState 实现组件共享，考虑到组件之间的通信
2 state 去保存的话 会造成异步渲染 造成无限循环</div>2021-06-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/fc/c3/0991edfc.jpg" width="30px"><span>闲闲</span> 👍（5） 💬（7）<div>useCallBack依赖是空数组表示什么？</div>2021-06-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/9a/0a/da55228e.jpg" width="30px"><span>院长。</span> 👍（4） 💬（1）<div>有个问题想问下，关于useMemo，文档说的是性能优化的保证，也就是涉及到大量计算的时候可以使用，因为依赖项的比较本身也是有开销的。

那如果我就只是很简单的计算，或者就只是返回一个固定的对象，有必要使用吗</div>2021-06-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/94/45/7ea3dd47.jpg" width="30px"><span>开开之之</span> 👍（2） 💬（5）<div>老师，我也有同样的疑问，定时器的例子，不能用一个常量去保存吗？
import React, { useState, useCallback, useRef } from &#39;react&#39;

export default function Timer() {
  const [time, setTime] = useState(0)
  const timer = useRef(null)

  let timer2 = null

  const handleStart = useCallback(() =&gt; {
    timer2 = window.setInterval(() =&gt; {
      &#47;&#47; 这里是个闭包，每次拿到的time值是0，所以要这样写手动去更新time的值
      setTime((time) =&gt; time + 1)
    }, 1000)
  }, [time])

  const handleStop = useCallback(() =&gt; {
    window.clearInterval(timer2)
    timer2 = null
  }, [])

  return (
    &lt;div&gt;
      {time &#47; 10} seconds.
      &lt;br&#47;&gt;
      &lt;button onClick={handleStart}&gt;start&lt;&#47;button&gt;
      &lt;button onClick={handleStop}&gt;stop&lt;&#47;button&gt;
    &lt;&#47;div&gt;
  )
}</div>2021-06-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/44/ea/8a9b868d.jpg" width="30px"><span>琼斯基亚</span> 👍（1） 💬（4）<div>老师，请问：
const handleIncrement = useCallback(() =&gt; setCount(count + 1), [count]);
const handleIncrement = useCallback(() =&gt; setCount(q =&gt; q + 1), []);
在性能方面是否后者优于前者？我的理解：
后者只创建了一次函数，但是又调用了多次在setCount的回调函数
前者只会在count变化的时候创建新的回调函数
这样分析下来我又觉得两者没什么差异
我不是太清楚这两者的优缺点，希望得到老师的解答。</div>2021-06-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f2/4f/59bd4141.jpg" width="30px"><span>Isaac</span> 👍（1） 💬（4）<div>&lt;button onClick={() =&gt; handleClick(&#39;hi&#39;)}&gt;&lt;&#47;button&gt;

老师，上面这种写法，直接将箭头函数作为 props 传递给 button，是不是每次 render 的时候，也会生成一个新的箭头函数？

如果是的话，怎么避免呢？</div>2021-06-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/20/04/72cc2057.jpg" width="30px"><span>Sunny</span> 👍（1） 💬（4）<div>import React, {
  useCallback,
  useRef,
  useReducer,
} from &#39;react&#39;;

const initialState = {time: 0};
function reducer(state, action) {
  switch (action.type) {
    case &#39;increment&#39;:
      return {time: state.time + 1};
    default:
      throw new Error();
  }
}

export default function Timer() {
  console.log(&#39;--render--&#39;)

  const [state, dispatch] = useReducer(reducer, initialState);
  
  const timer = useRef(null);

  const setIntervalCallback = useCallback( () =&gt; {
    dispatch({type: &#39;increment&#39;});
    console.log(&#39;setinterval time:&#39;, state.time)  &#47;&#47;为什么这里的state.time不变？
  }, [state.time]);&#47;&#47;这里的state.time变化被监听到了

  const handleStart = useCallback(() =&gt; {
    console.log(&#39;handlestart&#39;)
    timer.current = window.setInterval(setIntervalCallback, 1000);
  }, [timer, setIntervalCallback]);
  
  const handlePause = useCallback(() =&gt; {
    console.log(&#39;handlePause&#39;)
    window.clearInterval(timer.current);
    timer.current = null;    
  }, [timer]);
  
  return(
    &lt;div&gt;
      {state.time} seconds.
      &lt;MyStartBtn handleStart={handleStart}&#47;&gt;
      &lt;MyPauseBtn handlePause={handlePause}&#47;&gt;
    &lt;&#47;div&gt;
  );
}

function StartButton({handleStart}){
  console.log(&#39;startButton render --&#39;)
  return &lt;button onClick={handleStart}&gt;Start&lt;&#47;button&gt;;
}
const MyStartBtn = React.memo(StartButton, (prevProps, nextProps) =&gt; {
  return prevProps.handleStart === nextProps.handleStart;
});

function PauseButton({handlePause}){
  console.log(&#39;pauseButton render --&#39;)
  return &lt;button onClick={handlePause}&gt;Pause&lt;&#47;button&gt;;
}
const MyPauseBtn = React.memo( PauseButton, (prev, next) =&gt; {
  return prev.handlePause === next.handlePause;
})

&#47;*
console.log打印结果：
--render--
startButton render --
setinterval time: 0
每秒循环打印上面3行...


疑问：
const setIntervalCallback = useCallback( () =&gt; {
    dispatch({type: &#39;increment&#39;});
    console.log(&#39;setinterval time:&#39;, state.time)  &#47;&#47;为什么这里的state.time不变？
  }, [state.time]);&#47;&#47;这里的state.time变化被监听到了
*&#47;</div>2021-06-01</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eoBfn5GA1iclA3lS5wbRk0picaD3A5GeP9kfxk72AmwPrrsibOhqPAiawPu11dUlgY3LYXniaEwNAvVuDw/132" width="30px"><span>快扶我起来学习</span> 👍（0） 💬（1）<div>const ThemeContext = React.createContext(themes.light);  这里的themes. Light参数有什么作用呢？我传null也正常work了
</div>2021-08-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f7/20/e2dfa9c2.jpg" width="30px"><span>花儿与少年</span> 👍（0） 💬（2）<div>useContext的官方例子中，子组件中 const theme = useContext(ThemeContext);  那是需要子组件 引用ThemeContext 这个变量吗， 实际开发中这个子组件可能是单独的一个jsx文件，需要每个用到的子组件 import 这个变量？</div>2021-08-01</li><br/><li><img src="" width="30px"><span>rookielink</span> 👍（0） 💬（1）<div>useRef示例中替换这个有什么区别呢？ 
const timer = useRef(null);  =&gt;  const timer = {}; </div>2021-07-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/0d/cf/22b9c975.jpg" width="30px"><span>不瘦到160不改头像</span> 👍（0） 💬（1）<div>Start点了两次以后Pause的功能就用不了了。代码里这边的逻辑有点没有读明白。。。。
</div>2021-06-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/94/a7/43c1efaa.jpg" width="30px"><span>笨重的企鹅</span> 👍（0） 💬（3）<div>useRef那个计时器的例子，不用useRef，直接声明一个普调变量：let timer = null（注意不能是const）也是OK的，所以多次渲染之间共享数据这个貌似不怎么实用</div>2021-06-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/92/d9/84c1de45.jpg" width="30px"><span>傻子来了快跑丶</span> 👍（0） 💬（1）<div>老师讲的很棒，希望后面的课程质量更棒</div>2021-06-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/06/d2/e6efc3db.jpg" width="30px"><span>D.W</span> 👍（0） 💬（1）<div>老师，你好。
1，如果用state保存timer，在清空times贵引起不必要的渲染吧

2，请问像一些事件监听的函数，比如监听下拉框的变化，按钮的点击回调，应该没有必要用useCallback包裹吧？就像文中说的，使用useCallback主要是为了避免函数重新生成，接受函数作为参数的组件也重新渲染</div>2021-06-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/6d/7c/e91866cf.jpg" width="30px"><span>aloha66</span> 👍（0） 💬（2）<div>如果通过useMemo，依赖数组是容器组件的state,来优化展示组件的渲染，这个方案可行吗？
 const ItemRender = useMemo(() =&gt;&lt;ComA {...props}&#47;&gt;},[state])
...
{ItemRender}</div>2021-06-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/66/7b/535144e8.jpg" width="30px"><span>陈东</span> 👍（7） 💬（0）<div>感觉useMemo和useCallback的demo，子组件还是需要重新渲染。除非父组件使用useMemo&#47;useCallback，同时子组件使用React.memo&#47;shouldComponentUpdate，才能避免子组件重新渲染。</div>2021-07-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/d4/85/f35e0422.jpg" width="30px"><span>litchi2333333</span> 👍（5） 💬（2）<div>计时器的例子, 使用useCallback缓存了函数定义, 但是依旧会导致重新渲染整个render里面的子组件, 即使子组件的props等没有变化, 如果不使之渲染的话只能采用React.memo来定义缓存子组件吧? </div>2021-07-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/53/9a/2eddfce2.jpg" width="30px"><span>小个子外星人：）</span> 👍（5） 💬（1）<div>请问有什么react优秀项目&#47;案例，推荐学习吗？在工作中遇到关于一些业务逻辑的问题，不知道怎么实现会比较好。想看看react优秀项目学习学习，求推荐。谢谢</div>2021-06-07</li><br/><li><img src="" width="30px"><span>豆浆油条</span> 👍（3） 💬（2）<div>我在网上看到说useCallBack最好不要频繁使用，因为每次要执行对比，比重新创建一个函数消耗要高，老师这是不是和你说的函数都用useCallBack缓存冲突了。</div>2021-11-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/d5/34/10df391a.jpg" width="30px"><span>Zeal</span> 👍（1） 💬（0）<div>useCallback的用处应该在于利用memoize减少不必要的子组件的重新渲染问题，而不是函数组件过多内部函数的问题。</div>2022-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/85/7e/dc5ee66c.jpg" width="30px"><span>天天</span> 👍（1） 💬（0）<div>“比如 Redux，正是利用了 Context 的机制来提供一种更加可控的组件之间的状态管理机制。因此，理解 Context 的机制，也可以让我们更好地去理解 Redux 这样的框架实现的原理。”

老师上面这段话，我觉得不太对，redux 是通过connect来做的，connect 是一个高级函数，内部有一个 setState的来改变被包装组件的props来刷新子组件的，不是context的做法。

只是他们的思想比较像</div>2021-10-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/cd/45/15d2f59e.jpg" width="30px"><span>半夏</span> 👍（1） 💬（0）<div>想问一下老师，对于作为html节点属性的函数或者对象是否应该去缓存
```
function Test(props) {
	const [count, setCount] = useState(0);

	&#47;&#47; 第一种方式，直接创建handleClick1
	const handleClick1 = () =&gt;{
		console.log(&quot;方式一&quot;);
	}

	&#47;&#47; 第二种方式，创建用useCallback包裹的handleClick1
	&#47;&#47; const handleClick1 = useCallback(()=&gt;{
	&#47;&#47;	console.log(&quot;方式二&quot;)
	&#47;&#47; },[]);

return &lt;div&gt;
					&lt;div onClick={handleClick1}&gt;1111&lt;&#47;div&gt;
					&lt;span&gt;{count}&lt;&#47;span&gt;
					&lt;button onClick={()=&gt;setCount(count + 1)}&gt;add count&lt;&#47;button&gt;
			 &lt;&#47;div&gt;
}
```
个人认为在setCount的时候，组件触发重绘，handleClick1也会重新被创建；
1. 如果直接创建handleClick1的话，react在对比的时候就会认为它和之前绑定的函数不一致了，需要更新，这里会有性能损耗；
2. 如果用useCallback去缓存的话，虽然useCallback缓存时也会有性能损失，但是在后面渲染阶段react对比的时候每次用的handleClick1就都是旧的，这里就可以省掉后面的更新处理，节省性能；
不知道在这种情况下是应该直接定义，还是去创建一个依赖项为空的缓存值更好</div>2021-08-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/24/d8/aa41d743.jpg" width="30px"><span>🐒🐱🐭🐮🐯🐰🐶</span> 👍（0） 💬（0）<div>使用useState 可以去保存计时器的返回id  但是会导致不必要的组件重新渲染</div>2024-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/55/28/66bf4bc4.jpg" width="30px"><span>荷兰小猪8813</span> 👍（0） 💬（0）<div>比起 Class 组件，还缺少了一个很重要的能力：在多次渲染之间共享数据。

想问下，useState 和 useRef 不都是共享数据么？为啥说依然缺少呢？</div>2024-01-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/55/28/66bf4bc4.jpg" width="30px"><span>荷兰小猪8813</span> 👍（0） 💬（0）<div>每次组件状态发生变化的时候，函数组件实际上都会重新执行一遍。在每次执行的时候，实际上都会创建一个新的事件处理函数 handleIncrement。

问一下，那 useState 也会执行一边么？</div>2024-01-07</li><br/>
</ul>