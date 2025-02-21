你好，我是大圣。

上一讲我们分析了Vite原理，今天我们来剖析Vuex的原理。其实在之前的课程中，我们已经实现过一个迷你的Vuex，整体代码逻辑比较简单，基于Vue提供的响应式函数reactive和computed的能力，我们封装了一个独立的共享数据的store，并且对外暴露了commit和dispatch方法修改和更新数据，这些原理就不赘述了。

今天我们探讨一下下一代Vuex5的提案，并且看一下实际的代码是如何实现的，你学完之后可以对比之前gvuex mini版本，感受一下两者的区别。

## Vuex5提案

由于Vuex有模块化namespace的功能，所以模块user中的mutation add方法，我们需要使用 `commit('user/add')` 来触发。这样虽然可以让Vuex支持更复杂的项目，但是**这种字符串类型的拼接功能，在TypeScript4之前的类型推导中就很难实现**。然后就有了Vuex5相关提案的讨论，整个讨论过程都是在GitHub的issue里推进的，你可以访问[GitHub链接](https://github.com/vuejs/rfcs/pull/271)去围观。

Vuex5的提案相比Vuex4有很大的改进，解决了一些Vuex4中的缺点。Vuex5能够同时支持Composition API和Option API，并且去掉了namespace模式，使用组合store的方式更好地支持了TypeScript的类型推导，还去掉了容易混淆的Mutation和Action概念，只保留了Action，并且**支持自动的代码分割**。
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/yyibGRYCArsUNBfCAEAibua09Yb9D5AdO8TkCmXymhAepibqmlz0hzg06ggBLxyvXicnjqFVGr7zYF0rQoZ0aXCBAg/132" width="30px"><span>james</span> 👍（3） 💬（0）<div>没有关联的组件之间可以使用 pinia</div>2022-01-13</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/vicCM2yGWiadP0sgKezKqp0SStcDIre2ibl04qxQSdqwl68XcaoiaafdzoXLz5lVjDZ31XJa7w6f8tKgxlTt2nlDLQ/132" width="30px"><span>李增</span> 👍（2） 💬（3）<div>createSetupStore 函数的实现分析部分，有点收尾匆忙了，只说了重点，没有完整捋清楚createSetupStore 的完整实现细节。对于能自己去阅读源码的人来说，倒是没啥，但是对于底子差点的人来说，就很难懂createSetupStore 函数的整个内部实现运作原理了。大圣老师是否可以再补充下这一块的细节哈～</div>2022-03-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/30/e3/f6/823e346a.jpg" width="30px"><span>浣花公子</span> 👍（0） 💬（0）<div>嗯 这个写法就很像 React + Redux + immer</div>2022-10-28</li><br/>
</ul>