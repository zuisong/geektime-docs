你好，我是大圣，欢迎进入课程的第六讲。

在上一讲中，我带你搭建了项目的雏形，这是后面项目开发的起点。从今天开始，我就带你在这个骨架结构的基础之上，开始项目的实战开发。首先我们要掌握的，就是 Vue 3 的Composition API + &lt;script setup&gt;这种最新的代码组织方式。

![](https://static001.geekbang.org/resource/image/6f/0a/6fd86f3d33a0200d64c7423bc88e890a.png?wh=1222x432)

我们在前面的第三讲中，有详细地讲到过 Composition API ，相信你对这个API 的语法细节已经有所掌握了。那你肯定会很好奇，这个&lt;script setup&gt;又是什么？为什么尤雨溪要在微博上强推&lt;script setup&gt;呢？

别急，今天我就带你使用Composition API 和 &lt;script setup&gt; 去重构第二讲的清单应用。在重构的过程中，你能逐渐明白，**Composition API 可以让我们更好地组织代码结构**，而让你感到好奇的 &lt;script setup&gt;本质上是以一种更精简的方式来书写Composition API 。

## Composition API 和 &lt;script setup&gt; 上手

首先我想提醒你，我们在这一讲中写代码的方式，就和前面的第二讲有很大的区别。

在第二讲中，我们开发清单应用时，是直接在浏览器里使用 Options API 的方式写代码；但在接下来的开发中，我们会直接用单文件组件——也就是 `.vue` 文件，的开发方式。这种文件格式允许我们把 Vue 组件的HTML、CSS和JavaScript写在单个文件内容中。下面我带你用单文件组件的方式，去重构第二讲做的清单应用。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/be/e2/57d62270.jpg" width="30px"><span>奇奇</span> 👍（15） 💬（3）<div>大圣，能不能搞一个 git 仓库来放每一讲的课程代码内容呢</div>2021-10-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/c8/4a/3a322856.jpg" width="30px"><span>ll</span> 👍（137） 💬（5）<div> 每节课都有很多收获！
  ✿ Options API vs Composition API
        字面上, 选项 API 与 组合 API，细品, 这反映了设计面向的改变：
        1. 选项，谁的选项，关键在“谁”。谁？组件。也是 Vue2.x 的设计基础。组件有什么，
           有状态，有改变状态的方法，有生命周期，还有组件和组件之间的关系。这种情况
           下，“数据”要接受一定的“规矩”，“什么时候能做什么事”，“什么时候有什么表现”；
           这个状态下，开发模式像是“被动接受”。

        2. 组合，什么组合，关键在“什么”。什么？数据。数据的组合。Vue3.x 设计重点变了，数
           据变绝对的C了，现在去组件里串门，不用“守规矩”了，只需要说“我在 onMounted 的时
           候要这样这样，你看着办”，真只能的以“数据”为中心，没人能管得了了，想去哪就去哪，
           自然就灵活了

        至于这些是怎么做到由“被动接受”到“主动告知”的，实现这部分内容，我很期待。

  ✿ 模板语法更好用
        &lt;script setup&gt; 像是“语法糖”，很甜；&lt;style&gt;里能用 v-bind，以后开发可以
        少用“黑科技”了，双手点赞。

  ✿ 至于思考题
        Vue 本来就属于 DSL，语法方面各有偏好，见仁见智；响应式和生命周期需要 import，个
        人认为就代表了从之前的“被动主动”转向“主动告知”，这样设计更加灵活。从此一条主线在
        ”数据&quot;，以后查 bug 顺着这条 &quot;线&quot; 应该更加容易了。</div>2021-10-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/44/ea/8a9b868d.jpg" width="30px"><span>琼斯基亚</span> 👍（39） 💬（2）<div>对于value，官方是这样解释的：
将值封装在一个对象中，看似没有必要，但为了保持 JavaScript 中不同数据类型的行为统一，这是必须的。这是因为在 JavaScript 中，Number 或 String 等基本类型是通过值而非引用传递的：在任何值周围都有一个封装对象，这样我们就可以在整个应用中安全地传递它，而不必担心在某个地方失去它的响应性</div>2021-11-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/f5/7a/7351b235.jpg" width="30px"><span>ch3cknull</span> 👍（15） 💬（2）<div>关于导入问题，antfu大神有一个插件unplugin-auto-import，可以自动注入依赖项，不用import

https:&#47;&#47;github.com&#47;antfu&#47;unplugin-auto-import

.value问题貌似最新的ref语法糖可以算是一个解决方案，但是目前褒贬不一，我不推荐现在就用</div>2021-10-29</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJrIyCrRXMPXUQTR5IHNOh6niaY3MRr2mtv6W6WXcT1FHK1aic3NOhfzdaqfx3u8mmFAmibgX8xDdB2g/132" width="30px"><span>王俊</span> 👍（15） 💬（6）<div>建议增加代码库，实时拉取更新，现在的代码片段看着比较麻烦</div>2021-10-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/5b/9e/a8dec12d.jpg" width="30px"><span>cwang</span> 👍（12） 💬（9）<div>谢谢大圣老师的讲解。其中清单应用中，独立出来的useTodos函数，放在了哪里进行维护？并且，在使用这个函数时：let { title, ……} = useTodos() ，是不是还要对它进行一个引用？谢谢。</div>2021-10-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/48/9e/9bbaa97d.jpg" width="30px"><span>Geek_fcdf7b</span> 👍（9） 💬（1）<div>大圣老师，请教一下，3.2版本之后，是不是定义响应式数据都可以用ref一把梭？我看有的文章是这样说的，ref在3.2之后性能进行了大幅度提升，所以建议使用ref，不管简单数据还是复杂数据都可以用ref，没必要用reactive</div>2021-12-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/95/7a/2b48a36e.jpg" width="30px"><span>凌旭</span> 👍（9） 💬（2）<div>1，Composition API +setup的写法，看起来是把vue2中属于单个组件的js代码和组件解耦了，这样可以高效复用到其他组件中，但随着业务代码的增对，这样抽离出来的js也会越来越多，到时的维护管理难度又会加大，虽然这样做杜绝了在template,script间的反复横跳，但是无法避免地需要在各个js文件中跳转呀。</div>2021-10-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/3e/49/ff5c8f69.jpg" width="30px"><span>超</span> 👍（7） 💬（6）<div>请问大圣，如果把useTodos单独抽成一个js文件，改js里的文件，浏览器界面不会自动热重载，有啥解决方法没？是改webpack的配置吗？</div>2021-10-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/fd/da/7e0f0a02.jpg" width="30px"><span>1⃣️</span> 👍（6） 💬（1）<div>ref的副作用也可以用$ref解决是什么意思？哪里能找到这个语法介绍吗？</div>2022-01-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/5f/eb/ef7aa4c1.jpg" width="30px"><span>特供版</span> 👍（5） 💬（2）<div>强烈建议听课前
过一遍vue3的文档先！
过一遍vue3的文档先！
过一遍vue3的文档先！
https:&#47;&#47;v3.cn.vuejs.org&#47;api&#47;
对老师的建议：稍微提一下setup(),再提&lt;script setup&gt;。要不然直接跳到语法糖，简直是一头雾水。
还有类似style的v-bind，如果是vue2没有的特性的话，希望也顺带提一嘴。

另外mac也有热更新的问题，最后把文件引用全部补全了（例如文件路径没有.js后缀等），莫名的就好使了。</div>2021-12-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/9a/ce/89430cc1.jpg" width="30px"><span>月落梅影</span> 👍（4） 💬（1）<div>以前在极客时间上买了李兵老师浏览器相关的课程，现在再来看大圣老师的课，觉得差别还是挺大的，大圣老师的课程中，经常出现相信你一定怎样怎样，觉得缺乏一根主线。</div>2022-01-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4c/79/390fa870.jpg" width="30px"><span>流星的泪痕</span> 👍（3） 💬（1）<div>useTodos() 放到哪里去？上面的代码也没看到引用useTodos js相关文件。去查看了 https:&#47;&#47;github.com&#47;shengxinjing&#47;geektime-vue-course 代码里面好像也没有看到useTodos()这个函数</div>2021-12-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/59/0a/2a087c97.jpg" width="30px"><span>嘻哈</span> 👍（3） 💬（2）<div>感觉会 react学本节内容成本不高的</div>2021-10-29</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/ruxj2Ko6lpWdmf4ePtUCjZU0LpicbVUuTicWaSDRkGHGMB78b3vQNNbfhlqMWlibxCLX6V0IfueFxUyxs5BlryzVQ/132" width="30px"><span>SjmBreadrain</span> 👍（2） 💬（1）<div>现在是setup 被 script setup 替代了？</div>2022-01-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/2b/c7/9c8647c8.jpg" width="30px"><span>鐘</span> 👍（2） 💬（1）<div>關於 useMouse 這個使用案例
如果畫面上同時有 N 個組件都引入這個功能
每次畫面更新會被呼叫 N 次 onMounted
移動一次滑鼠會被觸發 N 次 update
但已經有使用 reactive , 不需要重複更新這麼多次</div>2022-01-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a1/0e/b98542f6.jpg" width="30px"><span>黄智勇</span> 👍（2） 💬（3）<div>用了$ref代替ref，就可以不用到处都是.value了</div>2021-10-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/7b/f0/ccc11dec.jpg" width="30px"><span>Cris</span> 👍（1） 💬（2）<div>Composition API script setup 这种写法怎么访问this的呢，比如父组件想访问子组件里的某个方法，options api是通过this.$refs.xxx.show()</div>2022-01-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/2b/c7/9c8647c8.jpg" width="30px"><span>鐘</span> 👍（1） 💬（2）<div>請問遇到這種情形怎樣處理比較好?
當一堆相關的邏輯會用到一些共用的變數, 目前想到兩種方式去表達, 但都覺得有問題:

1. 寫成一個函數
1-1 整個函數會太長, 有的人認為函數 20 行就算長了
1-2 裡面的函數如果要寫單元測試的話也測不到, 又或者要全部都 export 出來? 但是這樣又有測試私密函數的問題
```
function longFunction(){
  &#47;&#47; 1000 行代碼
}
```

2. 拆開成不同函數
會需要將共用變數傳來傳去, 
單元測試也不見得比較好寫, 函式之間某些狀態會互相依賴
```
const value1 = ref()
const {value2, value3} = useFuncA(value1)
const {value4} = useFuncB(value1, value2)
```

我想是我在邏輯拆分上有問題, 我想將相關的邏輯寫在同一個函數中
這樣其他人感覺比較知道這個流程在做甚麼
但會用到一些共用的狀態, 然後就寫出互相糾葛的義大利麵代碼</div>2022-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/20/6d/c16a5f67.jpg" width="30px"><span>黎川</span> 👍（1） 💬（2）<div>上节课提到的outer文件里面的引入的页面名字是大写，而页面文件名是小写，这样会导致页面引入的组件不热更新，我引入到home页面的todolist组件修改后，就没有出发更新，把home的名字改成小写就行了
import Home from &#39;..&#47;pages&#47;home.vue&#39;
{
      path: &#39;&#47;&#39;,
      name: &#39;Home&#39;,
      component: Home
    },</div>2021-12-21</li><br/><li><img src="" width="30px"><span>Geek_5db5e3</span> 👍（1） 💬（2）<div>大圣老师，到时候每个页面都要引入一遍ref和生命周期之类的，感觉有点繁琐的样子，有啥办法么</div>2021-12-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/85/f6/0edde5c2.jpg" width="30px"><span>鱿鱼</span> 👍（1） 💬（4）<div>大圣老师，我有一个问题，当我在style中使用v-bind的时候，我是这样用的：
import { ref } from &#39;vue&#39;;
let styleBind = ref(&#39;23123213&#39;)
let color = ref(&#39;pink&#39;)
&lt;&#47;script&gt;
&lt;style scoped&gt;
.test_p {
    color: v-bind(color);
}
.test_p::after {
    content: v-bind(styleBind);
}
&lt;&#47;style&gt;
，我在这样使用的过程中，绑定的color就有效，但是伪元素中的就无效了，这是为什么呢</div>2021-12-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/aa/b6/81a6595f.jpg" width="30px"><span>superZchen</span> 👍（1） 💬（1）<div>let todos = ref([
    {
      title: &#39;学习Vue3&#39;,
      done: false,
    },
  ]); 
ref不是只适用于简单数据结构吗？为什么能监听数组的响应？</div>2021-11-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/59/a7/9a086b7e.jpg" width="30px"><span>我的世界很小</span> 👍（1） 💬（1）<div>将TodoList模块中变量、函数提取到useTodos() 中，但是template、style的内容没有提取，是为了方便自定义样式和排版么？</div>2021-11-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/36/c3/a56ff6a6.jpg" width="30px"><span>pingxiu</span> 👍（1） 💬（1）<div>大圣老师，composition api + option api搭配使用，怎么用方便呢</div>2021-11-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/21/75/21222fa9.jpg" width="30px"><span>DXL</span> 👍（1） 💬（1）<div>大圣，你好，我想问一下，在Composition API拆分useMouse方法时，在里面引入了mounted钩子函数，如果我在引入useMouse的.vue组件里面又引入了mounted钩子函数，两个方法会分先后执行或者冲突吗？</div>2021-11-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ea/b7/1a18a39d.jpg" width="30px"><span>5-刘新波(Arvin)</span> 👍（1） 💬（1）<div>这种简化代码组织方式是怎么实现的？感觉是把原来组件里的东西抽到vue包全局层面了。vue是如何识别的，并完成一个组件生命周期，状态数据的维护组装的？</div>2021-11-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/52/16/ba6fe9a5.jpg" width="30px"><span>Temp</span> 👍（1） 💬（1）<div>大圣老师, 如果存在多个useXXX.js 函数的话, 每个函数可能都需要导入 import { ref } from &#39;vue&#39; , 这样不会冗余吗? 还是说 vue 在某些步骤做了优化?</div>2021-11-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/c4/77/c8783e83.jpg" width="30px"><span>wjxfhxy</span> 👍（1） 💬（1）<div>useTodos为什么要封装成函数？
在ts中，能封装成类: class UseTodos(){}，然后在setup中 new UseTodos()吗？</div>2021-11-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/3a/e2/c48bd3b7.jpg" width="30px"><span>Kevin</span> 👍（1） 💬（2）<div>移动端转前端，有一下代码感觉比较怪异：
`let all = computed(() =&gt; todos.value.length)`
这里面是说明`all`是一个动态计算的变量，为啥就不能直接使用 ` todos.value.length`? 我在Android 开发的时候，很自然的就会给`all` 映射未对应的Getter方法`getAll`，就很简洁，而上述的代码就显得很啰嗦。
更优雅的语法是不是应该类似这样的：
`let all.getter = ()=&gt;  todos.value.length` 这样语义也更加的清晰，当前这个语法可能是有问题的。

多年Java经验，现在学前端，有此疑惑，盼望解答。</div>2021-11-03</li><br/>
</ul>