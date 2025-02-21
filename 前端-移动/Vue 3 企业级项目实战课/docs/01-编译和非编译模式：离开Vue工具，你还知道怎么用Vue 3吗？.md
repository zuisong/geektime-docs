你好，我是杨文坚。

在开始讲解今天课程之前，我们来想象一下这么一个场景：当Vue.js代码在生产环境中报错了，你该如何快速根据生产环境编译后的代码，进行问题定位和排错呢？

代入到这个场景中，你是否会感到无解？虽然说，得益于Vue.js丰富的“全家桶”式开发工具，我们能够低成本地直接使用开发项目，无需关心繁琐的项目构建配置，但这也很容易让新同学产生依赖，甚至误解。

比如误解Vue.js这类语法是浏览器默认就支持的，不清楚Vue.js代码在浏览器中实际的运行方式等等。这种浅尝辄止式的学习，会给我们实际的开发工作带来一些小麻烦。

所以，我们一定得清楚 Vue.js 在非编译的情况下是如何使用的，这样即便我们脱离了Vite、Webpack和Rollup等构建工具，也能让Vue.js 3在浏览器中正常运行。同时，你也可以通过这节课理解Vue.js的代码是如何进行编译，让浏览器识别运行的。

## Vue.js‌ 3 代码编译结果是什么样子的？

在开始讲解Vue.js非编译模式的运行原理之前，我想先带你了解下Vue.js代码编译结果是怎样的。我们都知道，Vue.js代码经过编译后才能在浏览器运行，而且，Vue.js代码编译后的结果就是基于非编译语法来运行的。这能让你更好地理解Vue.js非编译模式的运行原理。
<div><strong>精选留言（15）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/a7/d5/e1221995.jpg" width="30px"><span>Turalyon</span> 👍（10） 💬（2）<div>这个念经试的朗读听着脑瓜子疼</div>2023-05-13</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/dCfVz7wIUT4fM7zQO3gIwXo3BGodP5FJuCdMxobZ5dXpzBeTXiaB3icoFqj22EbIGCu1xxd1FLo9xic0a2pGnunibg/132" width="30px"><span>风太大太大</span> 👍（14） 💬（2）<div>Vue.js 3 非编译场景与 Vue.js 的 JSX 写法有什么联系吗？
jsx写法是一个语法糖，最后会通过编译工具（babel）转化成 “非编译模式”的代码</div>2022-11-21</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/XPWXccJiaGnF4AZuuWnH4SQpKibwAhnRDAlnpcCwKW6JjJHFCz6ldicfC6QMiaJefyGVl8jZpYWvEJicZ2eK5qibCldA/132" width="30px"><span>周大大</span> 👍（13） 💬（1）<div>不论是createElementVNode、h、template、jsx都是为了生成vnode。h和createElementVNode用js写dom方式不友好，但是灵活。template和jsx用html写dom方式友好，但是templated不够灵活。jsx不仅拥有友好的书写方式，而且还可以通过{}实现动态值。</div>2022-11-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/dc/bd/ea9c16b8.jpg" width="30px"><span>莫比斯</span> 👍（3） 💬（1）<div>Vue.js 3 非编译场景与 Vue.js 的 JSX 写法有什么联系吗？
jsx的写法是来源自react，我想 Vue.js 的 JSX ，是可以帮助react开发者用熟悉的方式快速使用vue； Vue.js 的 JSX 写法 会编译转化成 Vue.js 3 非编译场景的代码；</div>2022-11-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/bd/ec/cc7abf0b.jpg" width="30px"><span>L</span> 👍（1） 💬（1）<div>Vue.js 3 非编译场景与 Vue.js 的 JSX 写法有什么联系吗？
jsx本质上还是需要走一段babel的编译过程，编译成vue可以识别的内容后再走vue的编译，好处是有的时候在编写代码的时候会更加的方便一点
对与运行时编译我有一个疑问，现在很多时候一些低代码的实现并不在浏览器端产出新的代码，而是通过一些渲染器之类的设计将json数据渲染成组件，对比将json数据转成实际的代码再进行vue运行时编译的方案的优劣是什么呢？
这样做性能会更加快并且后续的代码好维护吗？</div>2023-03-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/4b/07/791d0f5e.jpg" width="30px"><span>power</span> 👍（1） 💬（1）<div>Vue.js 3 非编译场景与 Vue.js 的 JSX 写法有什么联系吗？
jsx和vue.js3非编译场景都是为了表现vNode，jsx更方便开发者理解和书写，jsx最终会被编译成非编译模式</div>2023-03-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/78/e1/c6a3f7d0.jpg" width="30px"><span>前端WLOP</span> 👍（1） 💬（1）<div>示例图好好看 是用什么软件画的呀</div>2022-11-29</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Pk7HVX99cBlSOicLoa8KN81xqHa4YzRQsu5PAGTlOJgvChtl7T6BE6gTOhiaVJIcNVxIsRO1libPjdkZ6Sq8Qlp1g/132" width="30px"><span>Geek_b640fe</span> 👍（0） 💬（2）<div>浏览器直接运行，是指谷歌浏览器调试控制台直接运行吗</div>2022-11-23</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Pk7HVX99cBlSOicLoa8KN81xqHa4YzRQsu5PAGTlOJgvChtl7T6BE6gTOhiaVJIcNVxIsRO1libPjdkZ6Sq8Qlp1g/132" width="30px"><span>Geek_b640fe</span> 👍（0） 💬（2）<div>浏览器直接运行，是指比如 google浏览器的调试控制台，直接复制运行下面的?

import { 
  toDisplayString, createElementVNode, openBlock,
  createElementBlock, ref,
} from &quot;Vue.js&quot;;

const _hoisted_1 = { class: &quot;v-counter&quot; }
const _hoisted_2 = { class: &quot;v-text&quot; }

const __sfc__ = {
  __name: &#39;App&#39;,
  setup(__props) {
    const num = ref(0)
    const click = () =&gt; {
      num.value += 1;
    }
    return (_ctx, _cache) =&gt; {
      return (openBlock(), createElementBlock(&quot;div&quot;, _hoisted_1, [
        createElementVNode(
          &quot;div&quot;, _hoisted_2, toDisplayString(num.value), 1),
        createElementVNode(&quot;button&quot;, {
          class: &quot;v-btn&quot;,
          onClick: click
        }, &quot;点击数字加1&quot;)
      ]))
    }
  }

}
__sfc__.__file = &quot;counter.Vue.js&quot;
export default __sfc__</div>2022-11-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/6a/22/527904b2.jpg" width="30px"><span>hao-kuai</span> 👍（0） 💬（0）<div>JSX作为React的”template“语法，平衡了友好度和灵活度，最终还是会转换成基于Vnode的代码，然后经过渲染之后变成通过js的api生成的dom代码交给浏览器执行</div>2025-01-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡</div>2024-08-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/c1/9d/ecd6e2b3.jpg" width="30px"><span>陈彪</span> 👍（0） 💬（0）<div>Vue.js 3的非编译场景与JSX写法之间的联系在于，JSX作为一种语法糖，它允许开发者使用类似HTML的标记语法来编写Vue组件。这种写法直观且易于理解，特别是对于熟悉HTML的开发者来说。JSX最终会被Babel编译器转换成Vue.js 3的非编译模式代码，这种代码是Vue.js虚拟DOM（vNode）的表现形式，是非编译场景下的标准写法。

在非编译场景下，Vue.js 3使用&lt;template&gt;标签来编写模板代码，这些模板代码会被编译成JavaScript中的vNode对象。而使用JSX时，开发者可以直接编写出这些vNode的结构，从而在源代码中更清晰地看到最终渲染的HTML结构，这样做有以下好处：
● 代码可读性：JSX的标记语法让代码更接近最终渲染的结果，提高了代码的可读性。
● 开发体验：JSX可以提供更好的开发体验，例如在IDE中提供更好的自动完成和错误检查功能。
● 递归组件：在处理递归组件时，JSX可以更容易地表达递归的模板结构。</div>2024-03-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/da/58/87ce3d95.jpg" width="30px"><span>Michaels Geek</span> 👍（0） 💬（1）<div>杨大大，非编译模式demo(demo-counter-with-h.html), Counter的setup为什么要return两次才能正常渲染呢？

```
const Counter = {
                setup() {
                    const num = ref(0)
                    const click = () =&gt; {
                        num.value++
                    }
                    &#47;&#47; return 第一次
                    return (_ctx, cache) =&gt; {
                       &#47;&#47; return 第二次
                        return h(&#39;div&#39;, {
                            class: &#39;v-counter&#39;
                        }, [
                            h(&#39;div&#39;, {
                                class: &#39;v-text&#39;
                            }, toDisplayString(num.value)),
                            h(&#39;button&#39;, {
                                class: &#39;v-btn&#39;,
                                onClick: click
                            }, &#39;点击加1&#39;)
                        ])
                    }
                }
            }
```</div>2023-04-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/31/41/82/18d12e07.jpg" width="30px"><span>🇴</span> 👍（0） 💬（0）<div>git仓库挂了</div>2023-01-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/2b/c7/9c8647c8.jpg" width="30px"><span>鐘</span> 👍（0） 💬（1）<div>請問後續會介紹低代碼嗎? 
猜測低代碼平台是編譯模式(開發低代碼平台本身)和非編譯(資料庫資料轉換成組件)混用</div>2022-12-01</li><br/>
</ul>