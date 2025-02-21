你好，我是大圣。

上一讲我们主要介绍了Vue项目的首次渲染流程，在mountComponent中注册了effect函数，这样，在组件数据有更新的时候，就会通知到组件的update方法进行更新。

Vue中组件更新的方式也是使用了响应式+虚拟DOM的方式，这个我们在第一讲中有介绍过Vue 1、Vue 2和Vue 3中更新方式的变化，今天我们就来详细剖析一下Vue组件内部如何通过虚拟DOM更新页面的代码细节。

## Vue虚拟DOM执行流程

我们从虚拟DOM在Vue的执行流程开始讲起。在Vue中，我们使用虚拟DOM来描述页面的组件，比如下面的template虽然格式和HTML很像，但是在Vue的内部会解析成JavaScript函数，这个函数就是用来返回虚拟DOM：

```javascript
<div id="app">
  <p>hello world</p>
  <Rate :value="4"></Rate>
</div>
```

上面的template会解析成下面的函数，最终返回一个JavaScript的对象能够描述这段HTML：

```javascript
function render(){
  return h('div',{id:"app"},children:[
    h('p',{},'hello world'),
    h(Rate,{value:4}),
  ])
}
```
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/cd/ed/825d84ee.jpg" width="30px"><span>费城的二鹏</span> 👍（5） 💬（0）<div>key属性有利于判断新旧列表的复用判断，提升列表乱序后的复用率。</div>2021-12-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/39/25/c8cb5b52.jpg" width="30px"><span>chensd</span> 👍（1） 💬（0）<div>什么场景会触发 invalidateJob, 具体的demo可否展示一下</div>2022-04-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/b7/f5/4d9e2727.jpg" width="30px"><span>Meiki</span> 👍（1） 💬（0）<div>vue在进行页面更新时，会通过Diff算法对虚拟DOM进行更新，因为真实的DOM消耗比较大。 假设我们需要对数组进行增删改查，我们需要快速定位到某一项，所以我们需要给每项绑一个具体的唯一的id值</div>2021-12-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/f7/4c/9efa9ece.jpg" width="30px"><span>李凯</span> 👍（0） 💬（0）<div>这一节值得花时间认真阅读，写的很清楚，收获满满！</div>2023-09-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/33/09/d97b0ef2.jpg" width="30px"><span>evan</span> 👍（0） 💬（1）<div>&quot;然后进行队尾元素的预判，可以判断出 g 和元素也是一样的：&quot;  此处文案描述有错误，应该是“然后进行队尾元素的预判，可以判断出 g 和 h 元素也是一样的：”</div>2022-03-28</li><br/>
</ul>