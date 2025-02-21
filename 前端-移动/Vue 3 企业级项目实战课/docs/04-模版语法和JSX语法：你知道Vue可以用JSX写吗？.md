你好，我是杨文坚。

前面几节课，我们讲解了很多Vue.js 3编译相关的内容，了解完Vue.js两个编译打包工具后，我们是时候要开始学习如何使用Vue.js 3进行实际的代码开发了。

这节课，我主要会从Vue.js的两种主要开发语法进行讲解，它们分别是模板语法和JSX语法。从中你不仅能了解到两种开发语法的差异，还可以知道怎么因地制宜地根据需求场景选择合适的语法，从而扩大个人的技术知识储备，更从容地应对用Vue.js 3开发项目过程中遇到的各种问题。

Vue.js从版本1.x到版本3.x，官方代码案例和推荐使用都是模板语法，那么这里我们也根据官方的推荐，优先来了解一下模板语法是怎么一回事。

## 什么是模板语法？

我们可以把Vue.js的模板语法，直接理解为**HTML语法的一种扩展**，它所有的模板节点声明、属性设置和事件注册等都是按照HTML的语法来进行扩展设计的。按照官方的说法就是“所有的 Vue 模板都是语法层面合法的 HTML，可以被符合规范的浏览器和 HTML 解析器解析”。

现在我举个例子，带你了解下模板语法的概念及其不同内容的作用。代码如下所示：

```xml
<template>
  <div class="counter">
    <div class="text">Count: {{state.count}}</div>
    <button class="btn" v-on:click="onClick">Add</button>
  </div>
</template>

<script setup>
  import { reactive } from 'vue';
  const state = reactive({
    count: 0
  });
  const onClick = () => {
    state.count ++;
  }
</script>

<style>
.counter {
  padding: 10px;
  margin: 10px auto;
  text-align: center;
}

.counter .text {
  font-size: 28px;
  font-weight: bolder;
  color: #666666;
}

.counter .btn {
  font-size: 20px;
  padding: 0 10px;
  height: 32px;
  min-width: 80px;
  cursor: pointer;
} 
</style>

```
<div><strong>精选留言（12）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/e0/bb/14ab8d70.jpg" width="30px"><span>深山大泽平原</span> 👍（7） 💬（3）<div>用模板语法的数组实现组件的reverse：

&lt;template&gt;
    &lt;div class=&quot;template-reverse-box&quot;&gt;
        &lt;template v-for=&quot;item in comArr&quot;&gt;
            &lt;component :is=&quot;item.name&quot;&gt;&lt;&#47;component&gt;
        &lt;&#47;template&gt;
        &lt;button @click=&quot;changeModule&quot;&gt;reverse&lt;&#47;button&gt;
    &lt;&#47;div&gt;
&lt;&#47;template&gt;
&lt;script setup lang=&quot;ts&quot;&gt;
import { reactive, markRaw} from &#39;vue&#39;;
import Module01 from &#39;.&#47;Module01.vue&#39;
import Module02 from &#39;.&#47;Module02.vue&#39;
import Module03 from &#39;.&#47;Module03.vue&#39;
import Module04 from &#39;.&#47;Module04.vue&#39;

type Item = {
    name: any
}
let comArr = reactive&lt;Item[]&gt;([
    {
        name: markRaw(Module01)
    },
    {
        name: markRaw(Module02)
    },
    {
        name: markRaw(Module03)
    },
    {
        name: markRaw(Module04)
    },
])
const changeModule = () =&gt; {
    comArr.reverse()
}
&lt;&#47;script&gt;</div>2022-12-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/e1/95/5339b68d.jpg" width="30px"><span>直须</span> 👍（2） 💬（4）<div>怎么在.vue文件中引入jsx组件呢</div>2023-02-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/ae/27/74828c37.jpg" width="30px"><span>ZR-rd</span> 👍（2） 💬（4）<div>JSX 不能配置 scoped 避免 CSS 样式干扰，那么 JSX 应该如何做才能避免样式干扰呢</div>2022-12-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2e/f8/b9/36a74bc2.jpg" width="30px"><span>飞雪👻</span> 👍（0） 💬（2）<div>想请教一下, 我不太明白在用JSX写转换顺序, render函数中-------转换顺序: {`${isReverse}`}------ 为什么不直接写作{ isReverse } , 而是用模板字符串包裹呢 ?</div>2022-12-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5b/25/d78cc1fe.jpg" width="30px"><span>都市夜归人</span> 👍（2） 💬（1）<div>用模板方法一样能通过调整数组的顺序去实现，而不是用v-if。这是为了使用JSX而这样做的吧，个人觉得例子举的不是很恰当。</div>2022-11-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/10/fc/213c381f.jpg" width="30px"><span>请叫我潜水员</span> 👍（1） 💬（3）<div>dialog那个例子用模板是一样的效果，Dialog组件从dialog.vue中引入，然后创建一个相同的createDialog，使用效果一模一样。因为我就是这么用的</div>2022-11-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/6a/22/527904b2.jpg" width="30px"><span>hao-kuai</span> 👍（0） 💬（0）<div>jsx的自由度+vue3度性能那不是要起飞了</div>2025-01-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>组件内递归调用，没有结束条件的话会卡死吧?</div>2024-08-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡</div>2024-08-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/3a/08/27/0bd80208.jpg" width="30px"><span>xhsndl</span> 👍（0） 💬（0）<div>1. 模板语法实现组件递归（借鉴了前辈的想法）
&lt;template v-for=&quot;item in array&quot; :key=&quot;item&quot;&gt;
    &lt;component :is=&quot;item&quot;&#47;&gt;
&lt;&#47;template&gt;
&lt;script&gt;
import A1 from &quot;.&#47;A1.vue&quot;
import A2 from &quot;.&#47;A2.vue&quot;
import A3 from &quot;.&#47;A3.vue&quot;
import {reactive,markRaw} from &quot;vue&quot;

let array = reactive([
    markRaw(A1),
    markRaw(A2),
    markRaw(A3),
])
&lt;&#47;script&gt;

2. JSX实现模板组件递归
想法是将组件构造函数引入，结合数组对象来进行实现
&#47;&#47; 预先用jsx语法实现了A组件,假设用text接收参数、onOk接收点击事件的回调函数
&#47;&#47; 创建组件后返回onClose方法
&lt;script&gt;
import {createA} from &quot;.&#47;A.jsx&quot;

let A1 = createA({
  text:&#39;123456&#39;,
  onOk:() =&gt; {
      A1.onClose()  
  }  
})
&lt;&#47;script&gt;

&#47;&#47; ---------------
&#47;&#47; 实现JSX的循环调用
&lt;script&gt;
import {createA} from &quot;.&#47;A.jsx&quot;
import {reactive} from &quot;vue&quot;

let array = reactive([&#39;123&#39;,&#39;456&#39;,&#39;789&#39;])
array.forEach(item =&gt; 
    let temp = createA(
        text:item,
        onOk:() =&gt; temp.onClose()
    )
)
&lt;&#47;script&gt;</div>2024-01-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/d8/e3/987c9195.jpg" width="30px"><span>Spike Jim.Fun</span> 👍（0） 💬（0）<div>jsx的css模块化可以使用postcss-modules实现</div>2023-12-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/31/4b/77/791d0f5e.jpg" width="30px"><span>中欧校友</span> 👍（0） 💬（0）<div>模板语法递归在组件内用name名再次引用，JSX在组件函数内直接使用函数名调用实现梯柜</div>2023-07-30</li><br/>
</ul>