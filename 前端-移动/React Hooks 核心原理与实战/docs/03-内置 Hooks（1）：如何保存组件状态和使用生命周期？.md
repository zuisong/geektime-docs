你好，我是王沛。这节课我们一起来学习基本 Hooks 的用法。

如果你用过基于类的组件，那么对组件的生命周期函数一定不会陌生，例如 componentDidMount, componentDidUpdate，等等。如果没有使用过，那也没关系，因为在今天这节课里，你会看到基于 Hooks 去考虑组件的实现，这会是一个非常不同的思路，你完全不用去关心一个组件的生命周期是怎样的。

特别是如果你已经习惯了类组件的开发，那么要做的，甚至是彻底忘掉那些生命周期方法。不要遇到一个需求，就映射到这个功能该在哪个生命周期中去做，然后又要去想原来的声明周期方法在函数组件中应该怎么用 Hooks 去实现。

正确的思路应该是**遇到需求时，直接考虑在 Hooks 中去如何实现**。

React 提供的 Hooks 其实非常少，一共只有10个，比如 useState、useEffect、useCallback、useMemo、useRef、useContext等等。这一讲我们会先学习 useState 和 useEffect 这两个最为核心的 Hooks。下一讲则会介绍另外四个常用的 Hooks。掌握了这些Hooks，你就能进行90%的React 开发了。

不过在讲之前我想强调一点，这些 Hooks 的功能其实非常简单，多看看官方文档就可以了。因为这节课的目的，其实是让你学会如何用 Hooks 的思路去进行功能的实现。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/19/f1/73/6f7e3b35.jpg" width="30px"><span>独白</span> 👍（19） 💬（2）<div>1. 1）依赖那里没有传任何参数的话，会每次render都执行。2）依赖项有传值但是，有部分依赖没有传，那么没有传的那部分，数据即使变化也不会执行副作用。
2.函数应该是不会变化的，所以不需要监听。</div>2021-06-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/52/0e/c5ff46d2.jpg" width="30px"><span>CondorHero</span> 👍（16） 💬（2）<div>老师你好，我看到 redux 官网实现 useActions 函数，让我很困惑：

地址：https:&#47;&#47;react-redux.js.org&#47;api&#47;hooks#recipe-useactions

摘录源码，它的依赖数组是动态的，这肯定是不对的，但是如何在 eslint-plugin-react-hooks 规则下写这个函数的呢？：

```react
import { bindActionCreators } from &#39;redux&#39;
import { useDispatch } from &#39;react-redux&#39;
import { useMemo } from &#39;react&#39;

export function useActions(actions, deps) {
    const dispatch = useDispatch()
    return useMemo(
        () =&gt; {
            if (Array.isArray(actions)) {
                return actions.map(a =&gt; bindActionCreators(a, dispatch))
            }
            return bindActionCreators(actions, dispatch)
        },
        &#47;&#47; 这个依赖数组不是常量的
        deps ? [dispatch, ...deps] : [dispatch]
    )
}
```

</div>2021-05-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f1/15/8fcf8038.jpg" width="30px"><span>William</span> 👍（7） 💬（6）<div>思考题：
1. 未在依赖项中指定变量X，当X发生变化时，不会触发 useEffect 指定的回调函数。
2. setBlogContent可以作为依赖项，但是没必要。因为他只是用来 setState。
3. blogContent不可以作为依赖项，会引起死循环。因为在useEffect中修改了blogContent，会引起新一轮“副作用”回调。

https:&#47;&#47;github.com&#47;Si3ver&#47;react-hooks-demos&#47;blob&#47;main&#47;src&#47;03&#47;BlogView.js</div>2021-05-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/63/4c/09fe3f7a.jpg" width="30px"><span>逍遥一生</span> 👍（7） 💬（2）<div>1. 分两种情况，1）如果依赖为空，则每次都会执行，性能有损耗  2）依赖为数组，且漏掉了部分的依赖，会导致该依赖发生变化的时候useEffect内部的逻辑不执行

2. 不需要，因为我们希望的仅仅是在id变化的时候触发更新</div>2021-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/fc/c3/0991edfc.jpg" width="30px"><span>闲闲</span> 👍（4） 💬（2）<div>老师我有个疑问，
我们项目里面用到hook，但是有个问题，一般情况下，state会很多，不可能一两个，所以会把sate组合成对象，但是有时候对象发生了改变，例如{aa:1}--&gt;{aa:2},useEffect 监听函数没有进，需要手动的将两次对象Obeject.assgin一下才能触发监听，不知道老师有没有遇到过？</div>2021-05-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/e6/1e/ab237ae4.jpg" width="30px"><span>Hottou</span> 👍（2） 💬（1）<div>王老师，对于第二个问题，因为无论调用多少次setBlogContent函数，它的指向地址是不变的，所以即使把它作为依赖项，那么它永远也不会发生改变，是这样子吗？</div>2021-08-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/57/f4/63c3c5ae.jpg" width="30px"><span>Dark I</span> 👍（2） 💬（1）<div>函数体也是每次render都会执行 那么需要每次都会render执行的语句是放在 无依赖的useEffect中还是直接放在函数体中比较好呢</div>2021-06-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a8/5e/e5307db8.jpg" width="30px"><span>陈威严</span> 👍（2） 💬（1）<div>将函数定义在 useEffect 的 callback 中，每次执行 useEffect 时都会重新创建函数，这样对性能会有影响吗？</div>2021-06-01</li><br/><li><img src="" width="30px"><span>Geek_6b7a3b</span> 👍（1） 💬（1）<div>老师，第二个问题为什么说setBlogContent是一个局部变量，这个难道不是全局的吗？</div>2021-08-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/52/67/f4e1d20a.jpg" width="30px"><span>雅丽丽</span> 👍（1） 💬（1）<div>state 中永远不要保存可以通过计算得到的值。这是为什么呢？</div>2021-06-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/2c/64/2a185538.jpg" width="30px"><span>cyh41</span> 👍（1） 💬（1）<div>建议分开用多个值多个useState，还是多个值合成一个useState呢？</div>2021-06-01</li><br/><li><img src="" width="30px"><span>Geek_d9bc76</span> 👍（0） 💬（1）<div>“state中永远不要保存可以通过计算得到的值”，不太明白，我视图需要根据clineWidth计算出的值决定渲染item的个数，如果不通过useState，我要怎么触发界面更新呢？？</div>2021-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/47/74/5e292ded.jpg" width="30px"><span>寇云</span> 👍（0） 💬（1）<div>思考题1:大部分同学回答的挺好了 
问题2： 可以把 content  和 loading  封装成一个hooks,  const [loading, content] =  useBolgContent(id)</div>2021-06-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/5f/a8/4a6c6d9b.jpg" width="30px"><span>Afan</span> 👍（0） 💬（2）<div>import React, { useState, useEffect } from &quot;react&quot;;

export default  function BlogView() {
    &#47;&#47; 设置一个本地 state 用于保存 blog 内容
    const [blogContent, setBlogContent] = useState(&#39;&#39;);
    const id = 100;

    &#47;&#47; useEffect 的 callback 要避免直接的 async 函数，需要封装一下
    const doAsync =  () =&gt; {
        setBlogContent(&#39;demo&#39;);
    };

    useEffect(() =&gt; {
        console.log(1);
        doAsync();
    }, [id]); &#47;&#47; 使用 id 作为依赖项，变化时则执行副作用

    &#47;&#47; 如果没有 blogContent 则认为是在 loading 状态
    const isLoading = !blogContent;
    return &lt;div&gt;{isLoading ? &quot;Loading...&quot; : blogContent}&lt;&#47;div&gt;;
}
打印一次1


import React, { useState, useEffect } from &quot;react&quot;;

export default  function BlogView() {
    &#47;&#47; 设置一个本地 state 用于保存 blog 内容
    const [blogContent, setBlogContent] = useState(&#39;&#39;);
    const id = 100;

    &#47;&#47; useEffect 的 callback 要避免直接的 async 函数，需要封装一下
    const doAsync =  () =&gt; {
        setBlogContent(&#39;demo&#39;);
    };

    useEffect(() =&gt; {
        console.log(1);
        doAsync();
    }, [id, blogContent]); &#47;&#47; 使用 id 作为依赖项，变化时则执行副作用

    &#47;&#47; 如果没有 blogContent 则认为是在 loading 状态
    const isLoading = !blogContent;
    return &lt;div&gt;{isLoading ? &quot;Loading...&quot; : blogContent}&lt;&#47;div&gt;;
}
打印2次1</div>2021-06-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f1/15/8fcf8038.jpg" width="30px"><span>William</span> 👍（0） 💬（1）<div>思考题：
1. 不放在依赖数组中，则无法触发 useEffect 回调；
2. 不需要，setBlogContent 仅仅是用来更新博客内容的函数；

写了个demo: https:&#47;&#47;github.com&#47;Si3ver&#47;react-hooks-demos&#47;blob&#47;main&#47;src&#47;03&#47;BlogView.js</div>2021-05-30</li><br/><li><img src="" width="30px"><span>阳少宇</span> 👍（0） 💬（1）<div>1.当变量发生改变时，useEffect不会去执行
2. 不能，如果被作为依赖项会发生死循环。因为useEffect使用setBlogContent会触发状态的更新，状态更新会导致函数组件重新render，这样setBlogContent也会被更新</div>2021-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/6d/7c/e91866cf.jpg" width="30px"><span>aloha66</span> 👍（0） 💬（6）<div>代码的原意可能是在 todos 变化的时候去产生一些副作用
const todos = [{ text: &#39;Learn hooks.&#39;}];  useEffect(() =&gt; {    console.log(&#39;Todos changed.&#39;);  }, [todos]);
如果真的是需要监听todos变化做一些操作应该怎么实践了？</div>2021-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/f7/b4/d7a89271.jpg" width="30px"><span>健牌哥.</span> 👍（2） 💬（2）<div>老师能详细讲一下hooks为什么只能在函数顶层调用吗？</div>2021-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/55/51/c7bffc64.jpg" width="30px"><span>Andrew</span> 👍（1） 💬（0）<div>老师，不是很理解hooks必须按顺序执行这句话。本来不就是按顺序逐条执行的吗？是不是指带有callback的hook，他们的callback是按顺序执行的？</div>2022-07-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/3a/8d/f5e7a20d.jpg" width="30px"><span>何以解忧</span> 👍（1） 💬（1）<div>useEffect 依赖项是空数组的时候，动态挂载的时候为什么会执行两次</div>2022-04-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/51/3f/d11288e4.jpg" width="30px"><span>我是测试小达人</span> 👍（1） 💬（3）<div>老师好，想问一个问题～
在用useEffect处理副作用的时候，如果只想在依赖项变化的时候执行，但是第一次不执行，
类似于只需要class组件中的componentDidUpdate应该怎么写呢</div>2021-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/ad/7d/23379cd7.jpg" width="30px"><span>慕森</span> 👍（0） 💬（0）<div>想要把函数组件根据props参数中的值来判断，如果props参数等于某个值时整个函数组件不渲染也就是返回return null，但是其他情况继续执行，那这种情况下是否可以把 hooks 写到return后面呢？</div>2024-12-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/55/28/66bf4bc4.jpg" width="30px"><span>荷兰小猪8813</span> 👍（0） 💬（0）<div>在函数组件的当次执行过程中，useEffect 中代码的执行是不影响渲染出来的 UI 的。

如果影响了，会导致 cycle 渲染报错？？</div>2024-01-14</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTI7iakTvMwXWBHCK6WicIV2M3yQMZ8BtBgYgzARcEjbEtcWfKsQ2JqpZianKibZ2D7l1D3rwyTOL56Pzw/132" width="30px"><span>Jackchoumine</span> 👍（0） 💬（0）<div>&quot;useEffect 中代码的执行是不影响渲染出来的 UI 的。&quot; 这里是不是写错了呢，我理解的是影响渲染输出的操作才是副作用。</div>2023-06-05</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/MhhjicsUYicAmWyRxvLUQvEvhkmWfcVpTnHdx1SSROgJ0wqTSjnxZuqTWLQP0sian1C8InD5O5qMAEXLHibmuq4gJA/132" width="30px"><span>再见孙悟空</span> 👍（0） 💬（0）<div>老师你好，useEffect是在渲染后执行，那是在函数组建中return后面执行吗？如果是这样 比如一个列表中的数据初始状态为空，函数执行return出去了一个空数组，此时useEffect执行请求了数据，有了数据后怎样讲之前的空替换掉的</div>2023-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e7/20/70a95f94.jpg" width="30px"><span>潮汐</span> 👍（0） 💬（0）<div>1.多次组件重新渲染后，状态可能会发生错乱，导致很奇怪的报错
2.不用，useState返回的更新函数会保持不变（细想了下好像又需要加到依赖项数组，需要实践确认下）</div>2023-02-07</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eol3PaaOgxxVV7hic4mKiaCKzzpoZEp1QIOlMXGQAYianaxC56LqU1gkVFkTP1uqIq1REbAW082m7LqA/132" width="30px"><span>月无痕</span> 👍（0） 💬（0）<div>useEffect() =&gt; { return () =&gt; {} }, [])
这里少了个(</div>2022-11-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/4e/59/e528a0bb.jpg" width="30px"><span>Swelldg</span> 👍（0） 💬（0）<div>!</div>2022-09-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/87/2d/dc5fe99f.jpg" width="30px"><span>官锭AL</span> 👍（0） 💬（0）<div>useEffect使用async函数直接作为cb，有啥问题嘛</div>2022-03-23</li><br/><li><img src="" width="30px"><span>Geek_202275</span> 👍（0） 💬（0）<div>在 useEffect 中如果使用了某些变量，却没有在依赖项中指定，会发生什么呢？</div>2022-03-08</li><br/>
</ul>