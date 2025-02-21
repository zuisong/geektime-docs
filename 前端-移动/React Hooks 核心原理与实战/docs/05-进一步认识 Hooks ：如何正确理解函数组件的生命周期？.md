你好，我是王沛。今天我们来聊聊React组件的生命周期。

这一讲我会带你从 Hooks 的角度进一步理解 React 函数组件的生命周期。你可能会有疑问，前面几节课我们已经学习了 Hooks 的概念和内置 Hooks 的用法，那为什么还会有专门一讲来进一步介绍 Hooks 呢？

原因主要有两个。一方面，如果你已经熟悉了 Class 组件的生命周期，那么还需要一个转换编程思想到 Hooks 的过程，这样才能避免表面上用了 Hooks，却仍然用 Class 组件的方式思考问题。

另一方面，如果你是新接触 React，那么这一讲也能帮你了解原来 Class 组件的工作方式，从而如果看到或接手已有的 React 项目，也能从容应对。

# 忘掉 Class组件的生命周期

基于 Class 的组件作为 React 诞生之处就存在的机制，它的用法早已深入人心，甚至至今为止 React 的官方文档中仍然是以 Class 组件为基础的，而函数组件和 Hooks 则是作为新特性做了补充说明和解释。

这其实有两个原因：

- 一是 React 团队尽最大努力保持 API 的稳定，不希望给你造成一种 Class 组件将被废弃的感觉；
- 二是大量的存量应用其实还都是用 Class 组件实现的，无论是对于维护者还是加入者来说，了解 Class 组件都是很有必要的。
<div><strong>精选留言（18）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/17/e4/75/57809f30.jpg" width="30px"><span>Ada</span> 👍（58） 💬（4）<div>如果想要实现只执行一次的功能，用useEffect，依赖项传空数组，不是可以实现吗？
为什么要写一个自定义钩子？</div>2021-06-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/30/71/ba69f480.jpg" width="30px"><span>毛毛开飞机</span> 👍（33） 💬（1）<div>useEffect(() =&gt; {
  return () =&gt; {
    &#47;&#47; 这里只会在组件销毁前（componentWillUnmount）执行一次
  }
}, [])</div>2021-06-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/04/a7/ea22485a.jpg" width="30px"><span>海洋</span> 👍（7） 💬（2）<div>useEffect 第二个参数传入空，就只在组件初始化时和销毁前分别执行一次</div>2021-06-03</li><br/><li><img src="" width="30px"><span>Geek_12f953</span> 👍（4） 💬（1）<div>老师，useSingleton这个Hook里面使用useRef来定义called标记而不是用useState，是因为called并不会影响UI渲染吗？我尝试了用useState好像也可以实现只执行一次的效果</div>2021-08-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f7/20/e2dfa9c2.jpg" width="30px"><span>花儿与少年</span> 👍（4） 💬（1）<div>请教： 以下代码不是每次render后都会执行吗，return的函数在每次effect执行前执行？

useEffect(() =&gt; {
  return () =&gt; {
    &#47;&#47; 这里只会在组件销毁前（componentWillUnmount）执行一次
  }
}, [])
</div>2021-08-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f2/4f/59bd4141.jpg" width="30px"><span>Isaac</span> 👍（4） 💬（1）<div>老师，useEffect 的执行时机是 DOM 渲染完毕后执行，还是依赖发生变化，不管 DOM 有没有更新完毕就立即执行？</div>2021-06-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/3c/55/74844d08.jpg" width="30px"><span>大大小小</span> 👍（4） 💬（3）<div>BlogView那个例子，为什么要把useCallback返回的函数作为useEffect的依赖呢？是要达到什么目的吗？</div>2021-06-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/72/a8/c24a66a1.jpg" width="30px"><span>Geek_sky</span> 👍（3） 💬（1）<div>老师，我看到useRef的用法有一个疑问：例子中useSingleton包含了一个useRef的定义为false，如果我在MyComp中定义多个useSingleton，程序在启动的时候第二次及之后的调用useRef是怎么确认需要创建新的还是使用之前的？那么界面在刷新之后，useSingleton会再次被调用，那时会有多个useRef的检查，那么程序又是如何判定的？</div>2021-06-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/07/99/2c12c56c.jpg" width="30px"><span>浩然</span> 👍（2） 💬（1）<div>useEffect(() =&gt; {
    return () =&gt; {
        &#47;&#47; 组件销毁时执行
    }
}, [])</div>2021-06-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/22/27/134d9a49.jpg" width="30px"><span>Joseph😈</span> 👍（1） 💬（3）<div>请问下老师，如果只是为了做初始化工作，即只在首次render前执行一次。useSingleton这个自定义hook似乎换成useState或useEffect似乎都能做呀，跟useRef相比有没有什么优劣呢？</div>2021-06-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/ea/74/7dd9c65e.jpg" width="30px"><span>亦枫丶</span> 👍（0） 💬（1）<div>useSingleton 是不是可以直接 `useRef(callback())`</div>2021-06-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/c9/79/68a73484.jpg" width="30px"><span>MarkTang</span> 👍（2） 💬（0）<div>之前买过老师的React视频课，干货非常多，看了很多遍，这次果断买了。还是期待老师以后的视频课</div>2022-01-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/b7/72/54581d7e.jpg" width="30px"><span>1973</span> 👍（0） 💬（0）<div>老师，如果有依赖项的 useEffect 是在每次依赖项变化时，重新 render =&gt; commit，commit 之后执行 callback 吗</div>2023-09-19</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83epibNpKIwo4zFXMLIaucTicJBQ4iasrPXYNwLKiaBaOCic09mrWHPtSAA7zTVFDhXJoWBz2MWQclhlzkRg/132" width="30px"><span>奔跑的小蚂蚁</span> 👍（0） 💬（0）<div>这个和class组件得那个还有点不同得是，useEffect是在数据跟新后才执行得，不会阻塞ui，这里每次执行都会先去掉上一次的副作用，或者销毁的时候去掉副作用依赖项不为[]；依赖赖项为[]只执行一次effect函数；没有依赖项更新的时候每次都会执行 effect函数</div>2022-07-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/2d/32/43595745.jpg" width="30px"><span>鲁滨逊</span> 👍（0） 💬（1）<div>useSingleton(() =&gt; {}) 和 useEffect(() =&gt; {}, [])  是等价的 ？都是函数组件初始化的时候执行一次 ？</div>2022-06-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/48/9e/9bbaa97d.jpg" width="30px"><span>Geek_fcdf7b</span> 👍（0） 💬（0）<div>老师，什么时候出新课？</div>2022-05-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/01/64/5f5e3886.jpg" width="30px"><span>河马非马</span> 👍（0） 💬（0）<div>useEffect 接收的 callback 参数，可以返回一个用于清理资源的函数，从而在下一次同样的 Effect 被执行之前被调用，老师，请问这里的callback中return的函数是会在下次执行前和本次组件销毁时自动执行吗？看文档时一直没清楚他是react自动实现的规则，还是开发者自己定义的规则。</div>2021-06-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/db/ba/304a9a4a.jpg" width="30px"><span>Juntíng</span> 👍（0） 💬（0）<div>依据 useEffect 执行机制，deps 传递空数组，就能保证只在组件销毁时执行消除副作用</div>2021-06-18</li><br/>
</ul>