你好，我是王沛。

我在开篇词就说过，要用好 React Hooks，很重要的一点，就是要能够从 Hooks 的角度去思考问题。要做到这一点其实也不难，就是在遇到一个功能开发的需求时，首先问自己一个问题：**这个功能中的哪些逻辑可以抽出来成为独立的 Hooks？**

这么问的目的，是为了让我们尽可能地把业务逻辑拆成独立的 Hooks ，这样有助于实现代码的模块化和解耦，同时也方便后面的维护。如果你基础篇的知识掌握得牢固的话，就会发现，这是因为 Hooks 有两个非常核心的优点：

- 一是方便进行逻辑复用；
- 二是帮助关注分离。

接下来我就通过一个案例，来带你认识什么是自定义Hooks，以及如何创建。然后，我们再通过其它3个典型案例，来看看自定义Hooks 具体有什么用，从而帮你掌握从 Hooks 角度去解决问题的思考方式。

# 如何创建自定义 Hooks？

自定义 Hooks 在形式上其实非常简单，就是**声明一个名字以 use 开头的函数**，比如 useCounter。这个函数在形式上和普通的 JavaScript 函数没有任何区别，你可以传递任意参数给这个 Hook，也可以返回任何值。

但是要注意，Hooks 和普通函数在语义上是有区别的，就在于**函数中有没有用到其它 Hooks。**
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/18/03/86/c9051c6a.jpg" width="30px"><span>Bug般的存在</span> 👍（32） 💬（1）<div>《拆分复杂组件》 这个例子，有种醍醐灌顶的感觉，豁然开朗，感谢-</div>2021-06-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/f8/3a/dbf7bdee.jpg" width="30px"><span>凡凡</span> 👍（17） 💬（1）<div>import { useState, useCallback } from &#39;react&#39;;

const useCounter = (step) =&gt; {
  const [counter, setCounter] = useState(0);
  const increment = useCallback(() =&gt; setCounter(counter + step), [counter, step]);
  const decrement = useCallback(() =&gt; setCounter(counter - step), [counter, step]);
  const reset = useCallback(() =&gt; setCounter(0), []);
  
  return {counter, increment, decrement, reset};
}

export default useCounter;</div>2021-06-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/be/74/0d900ed9.jpg" width="30px"><span>Tristan</span> 👍（2） 💬（1）<div>醍醐灌顶啊，敢问如何保养头发？</div>2021-07-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/db/0b/f0ded153.jpg" width="30px"><span>江谢木</span> 👍（1） 💬（2）<div>老师，useMemo、useCallback对数据进行缓存时，依赖项是进行浅比较？ 如果存在依赖项是深层对象的数据发生变化会影响缓存计算结果？</div>2021-08-17</li><br/><li><img src="" width="30px"><span>Free fall</span> 👍（1） 💬（1）<div>const useCounter = (initCount = 0) =&gt; {
  const [count, setCount] = useState(initCount)

  const increase = useCallback((body) =&gt; {
    setCount((count) =&gt; (count += body))
  }, [])

  return [count, increase]
}</div>2021-06-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/e6/39/16208644.jpg" width="30px"><span>重生</span> 👍（0） 💬（1）<div>自定义hooks一般放在哪个文件夹下</div>2021-06-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f2/4f/59bd4141.jpg" width="30px"><span>Isaac</span> 👍（0） 💬（2）<div>老师，自定义 hooks 必须要以 usexxx开头吗？</div>2021-06-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/53/9a/2eddfce2.jpg" width="30px"><span>小个子外星人：）</span> 👍（0） 💬（1）<div>这节课超级棒！谢谢老师。努力在实践中，使用这节课的内容</div>2021-06-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/0f/a2/2bb7df25.jpg" width="30px"><span>满月</span> 👍（0） 💬（1）<div>import React, { useState, useCallback } from &#39;react&#39;;

function useCounter() {
  const [count, setCount] = useState(0);
  const increment = useCallback(
    (delta = 1) =&gt; setCount(count + delta),
    [count],
  );
  const decrement = useCallback(
    (delta = 1) =&gt; setCount(count - delta),
    [count],
  );
  const reset = useCallback(() =&gt; setCount(0), []);
  return {
    count,
    increment,
    decrement,
    reset,
  };
}

export default function Counter() {
  &#47;&#47; 调用自定义 Hook
  const { count, increment, decrement, reset } = useCounter();

  &#47;&#47; 渲染 UI
  return (
    &lt;div&gt;
      &lt;button onClick={() =&gt; decrement()}&gt; - &lt;&#47;button&gt;
      &lt;p&gt;{count}&lt;&#47;p&gt;
      &lt;button onClick={() =&gt; increment(2)}&gt; + &lt;&#47;button&gt;
      &lt;button onClick={reset}&gt; reset &lt;&#47;button&gt;
    &lt;&#47;div&gt;
  );
}</div>2021-06-06</li><br/><li><img src="" width="30px"><span>Geek_71adef</span> 👍（0） 💬（1）<div>请问如何区别 自定义hook是在usehook传参，还是在usehook里面的方法传参？</div>2021-06-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/ec/cf/8c1f8d38.jpg" width="30px"><span>xgqfrms</span> 👍（0） 💬（7）<div>完全没有必要使用 await 处理 res 呀

```js
&#47;&#47; return await res.json();

 return res.json();

```</div>2021-06-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ee/e2/23e44221.jpg" width="30px"><span>余熙</span> 👍（9） 💬（0）<div>这一节总结得非常好，官方文档和网上文章没写出来的干货👍</div>2021-06-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/92/d9/84c1de45.jpg" width="30px"><span>傻子来了快跑丶</span> 👍（3） 💬（0）<div>老师，后面的课程能不能出门更深入的，比如fibier，hooks的底层实现啊，这种，以及fiber的各种调度，啥的</div>2021-12-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/e0/4c/e6042c6c.jpg" width="30px"><span>别拦我让我学</span> 👍（3） 💬（0）<div>useScroll中getPosition中应该将document.body.scrollTop改为document.documentElement.scrollTop。</div>2021-07-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/51/c2/90a959d2.jpg" width="30px"><span>山城旧客</span> 👍（3） 💬（5）<div>
import React from &quot;react&quot;;
import useAsync from &#39;.&#47;useAsync&#39;;

export default function UserList() {
  &#47;&#47; 通过 useAsync 这个函数，只需要提供异步逻辑的实现
  const {
    execute: fetchUsers,
    data: users,
    loading,
    error,
  } = useAsync(async () =&gt; {
    const res = await fetch(&quot;https:&#47;&#47;reqres.in&#47;api&#47;users&#47;&quot;);
    const json = await res.json();
    return json.data;
  });
  
  return (
    &#47;&#47; 根据状态渲染 UI...
  );
}

我验证了这个案例必须执行副作用useEffect(() =&gt; fetchUsers(), []);才能发起异步数据请求，如果在依赖项数组中再传入useEffect(() =&gt; fetchUsers(), [fetchUsers]);会陷入异步数据请求死循环。</div>2021-06-09</li><br/><li><img src="" width="30px"><span>李克勤</span> 👍（2） 💬（0）<div>function useCounter() {

    const [count,setCount] = useState(0);
    const [step ,setStep] =useState(1)  

    const changeStep = useCallback((value) =&gt; {
        setStep(value);
    },[]);
    const increment = useCallback(() =&gt; {
        setCount(count+step);
    },[count,step]);
    const decrement = useCallback(() =&gt; {
        setCount(count-step);
    },[count,step]);
    
    const reset = useCallback(() =&gt; {
        setCount(0);
    },[])

    return {count,increment,decrement,reset,changeStep};

}
export default function Counter () {

   
   const {count,increment,decrement,reset,changeStep} = useCounter();

   return(
       &lt;div&gt;
           &lt;button onClick={decrement}&gt;-&lt;&#47;button&gt;
           &lt;p&gt;count:{count}&lt;&#47;p&gt;
           &lt;button onClick={increment}&gt;+&lt;&#47;button&gt;
           &lt;button onClick={reset}&gt;Reset&lt;&#47;button&gt;
           &lt;div&gt;
               &lt;InputNumber defaultValue={1} onChange={(v) =&gt; changeStep(v)}&#47;&gt;
           &lt;&#47;div&gt;
       &lt;&#47;div&gt;
   )
}</div>2021-09-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/47/74/5e292ded.jpg" width="30px"><span>寇云</span> 👍（2） 💬（0）<div>感谢老师，之前对于hooks 只停留在如何使用的层面。 慢慢的会把单文件中引入很多的useState，通过这节课，知道了应该如何创建自己的 hooks 来优化代码。</div>2021-06-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/f5/95/a362f01b.jpg" width="30px"><span>Geek1560</span> 👍（2） 💬（2）<div>老师您好，uesAsync 这个例子中，execute 使用了 useCallback，但实际传入的函数每次都是重新创建的，浅比较结果是不相同，缓存依然会更新，如果要使用uesCallback，是否是应该在外层缓存传入的asyncFunction</div>2021-06-06</li><br/><li><img src="" width="30px"><span>林芊芊</span> 👍（1） 💬（0）<div>react根本不关心 名字是否是usexxx 。 </div>2022-06-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/d3/bc/51c1029f.jpg" width="30px"><span>Geek_983da8</span> 👍（1） 💬（0）<div>原来这就是花钱的才能感受到的魅力</div>2022-03-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/bb/82/5a32de87.jpg" width="30px"><span>泷沁心</span> 👍（1） 💬（0）<div>写了这么久Hooks，一直以逻辑+UI作为基本区分，看到这里老师的几个例子，更加对Hooks另眼相看了，感谢老师，大赞！！！</div>2021-09-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8b/5f/ecf0e687.jpg" width="30px"><span>Neil 陈荣</span> 👍（1） 💬（0）<div>useAsync 命名成 useFetch 是否贴切些</div>2021-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/94/45/7ea3dd47.jpg" width="30px"><span>开开之之</span> 👍（0） 💬（0）<div>老师，你好，请问这里为何要这样写？
  const { execute, data, loading, error } = useAsync(
    useCallback(async () =&gt; {
      const res = await fetch(`${endpoint}&#47;categories`);
      return await res.json();
    }, []),
  );
  &#47;&#47; 执行异步调用
  useEffect(() =&gt; execute(), [execute]);</div>2024-05-18</li><br/><li><img src="" width="30px"><span>Geek_130786</span> 👍（0） 💬（0）<div>接口好像炸了</div>2024-02-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/55/28/66bf4bc4.jpg" width="30px"><span>荷兰小猪8813</span> 👍（0） 💬（0）<div>答案：

function useCounter(step) {
  &#47;&#47; 定义 count 这个 state 用于保存当前数值
  const [count, setCount] = useState(0);
  &#47;&#47; 实现加 1 的操作
  const increment = useCallback(() =&gt; setCount(count + step), [count, step]);
  &#47;&#47; 实现减 1 的操作
  const decrement = useCallback(() =&gt; setCount(count - step), [count, step]);
  &#47;&#47; 重置计数器
  const reset = useCallback(() =&gt; setCount(0), []);
  &#47;&#47; 将业务逻辑的操作 export 出去供调用者使用
  return { count, increment, decrement, reset };
}

function useStep() {
  const [step, setStep] = useState(5);
  const increments = useCallback(() =&gt; setStep(step + 1), [step]);
  const decrements = useCallback(() =&gt; {
    if (step - 1 == 0) {
      setStep(0);
    } else {
      setStep(step - 1);
    }
  }, [step]);
  return { step, increments, decrements };
}</div>2024-01-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/55/28/66bf4bc4.jpg" width="30px"><span>荷兰小猪8813</span> 👍（0） 💬（0）<div>const useArticles = () =&gt; {
  &#47;&#47; 使用上面创建的 useAsync 获取文章列表
  const { execute, data, loading, error } = useAsync(

const useCategories = () =&gt; {
  &#47;&#47; 使用上面创建的 useAsync 获取分类列表
  const { execute, data, loading, error } = useAsync(

上面多次调用了 useAsync，而 useAsync 里面多次调用了 const [data, setData] = useState(null);

想问下，这个 useState 是会复用，还是每次调用都是一个新的呢？

这里多次调用了 useAsync，</div>2024-01-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b1/84/d7034d7c.jpg" width="30px"><span>吴颜</span> 👍（0） 💬（0）<div>很清晰，有点东西</div>2023-09-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/b1/81/13f23d1e.jpg" width="30px"><span>方勇(gopher)</span> 👍（0） 💬（0）<div>ahooks是这么处理scrollTop的
top: Math.max(
  window.pageYOffset,
  document.documentElement.scrollTop,
  document.body.scrollTop,
),</div>2023-03-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/b1/81/13f23d1e.jpg" width="30px"><span>方勇(gopher)</span> 👍（0） 💬（0）<div>document.body.scrollTop 这个api在chrom里有问题，y: document.documentElement.scrollTop || document.body.scrollTop</div>2023-03-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/62/67/cd17dabe.jpg" width="30px"><span>elune3344</span> 👍（0） 💬（0）<div>useEffect(() =&gt; execute(), [execute]);
为啥不把这个执行的逻辑封在useAsync里面呢</div>2022-08-31</li><br/>
</ul>