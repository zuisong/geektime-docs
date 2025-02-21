你好，我是大圣。

上一讲我们学习了下一代Vuex框架Pinia的原理，今天我来带你分析Vue生态中另外一个重要的框架vue-router的源码。

课程中我们也实现过一个迷你的router，我们通过监听路由的变化，把路由数据包裹成响应式对象后，一旦路由发生变化，我们就去定义好的路由数据中查询当前路由对应的组件，在router-view中渲染即可。今天我们就进入到vue-router源码的内部，看一下实际的vue-router和我们实现的迷你版本有什么区别。

## vue-router入口分析

vue-router提供了createRouter方法来创建路由配置，我们传入每个路由地址对应的组件后，使用app.use在Vue中加载vue-router插件，并且给Vue注册了两个内置组件，router-view负责渲染当前路由匹配的组件，router-link负责页面的跳转。

**我们先来看下createRouter如何实现**，完整的代码你可以在[GitHub](https://github.com/vuejs/vue-router-next/blob/master/src/router.ts#L355)上看到。这个函数比较长，还好我们有TypeScript，我们先看下createRouter的参数。

在下面的代码中，参数RouterOptions是规范我们配置的路由对象，主要包含history、routes等数据。routes就是我们需要配置的路由对象，类型是RouteRecordRaw组成的数组，并且RouteRecordRaw的类型是三个类型的合并。然后返回值的类型Router就是包含了addRoute、push、beforeEnter、install方法的一个对象，**并且维护了currentRoute和options两个属性**。
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIkBhCDbibPDmDTEW6Uia1LAEOcFf75QxA897gcL4oXFMOwgsqFwf7rhPoUoJWgICl0xFT8Iz2cuWRg/132" width="30px"><span>InfoQ_e521a4ce8a54</span> 👍（2） 💬（0）<div>navigate 函数主要是执行一个异步队列；核心代码
function runGuardQueue(guards: Lazy&lt;any&gt;[]): Promise&lt;void&gt; {
  return guards.reduce(
    (promise, guard) =&gt; promise.then(() =&gt; guard()),
    Promise.resolve()
  )
}</div>2022-01-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/d3/a3/52702576.jpg" width="30px"><span>becky</span> 👍（0） 💬（0）<div>navigate应该是按官方文章https:&#47;&#47;router.vuejs.org&#47;guide&#47;advanced&#47;navigation-guards.html#the-full-navigation-resolution-flow 所写的顺序执行路由守卫</div>2023-07-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/f4/d4/b3edd36b.jpg" width="30px"><span>Merlin_nil</span> 👍（0） 💬（0）<div>大圣老师好，install逻辑中似乎有个小错误，文中「通过 app.provide 给全局注册了 route 和 reactive 包裹后的 reactiveRoute 对象」，应该把route改为router吧？</div>2022-04-11</li><br/>
</ul>