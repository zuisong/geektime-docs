你好，我是大圣。

在上一讲中，我给你介绍了如何使用Chrome和Vue Devtools来调试项目，相信你已经拥有了调试复杂项目的能力。今天，我们来聊一个相对独立的话题，就是Vue中的JSX。你肯定会有这样的疑惑，JSX不是React的知识点吗？怎么Vue里也有？

实际上，Vue中不仅有JSX，而且Vue还借助JSX发挥了Javascript动态化的优势。此外，Vue中的JSX在组件库、路由库这类开发场景中，也发挥着重要的作用。对你来说，学习JSX，可以让你实现更灵活的开发需求，这一讲我们重点关注一下Vue中的JSX。

## h函数

在聊JSX之前，我需要先给你简单介绍一下h函数，因为理解了h函数之后，你才能更好地理解JSX是什么。下面，我会通过一个小圣要实现的需求作为引入，来给你讲一下h函数。

在Vue 3的项目开发中，template是Vue 3默认的写法。虽然template长得很像HTML，但Vue其实会把template解析为render函数，之后，组件运行的时候通过render函数去返回虚拟DOM，你可以在Vue Devtools中看到组件编译之后的结果。

![图片](https://static001.geekbang.org/resource/image/75/af/75e3242df6e45538a6d43c5f0d39a1af.png?wh=1920x1140)

在上面的示意图中，调试窗口右侧代码中的\_sfc\_render\_函数就是清单应用的template解析成JavaScript之后的结果。所以除了template之外，在某些场景下，我们可以直接写render函数来实现组件。
<div><strong>精选留言（27）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/13/c8/4a/3a322856.jpg" width="30px"><span>ll</span> 👍（28） 💬（1）<div>厉害，看大圣的课，脑中就会涌现出以前学过用过的知识，然后随着文章的推进，这些知识就分条屡清了；然后查漏补缺，最后汇聚到一起，为自己所用。
一点回顾：
      1. template vs Jsx
         直观感觉是“殊途同归”。

         先说同归，这两终都会产出“虚拟DOM”；
         然后 “殊途”，React 的 Jsx 在这方面很“单纯”就提供“虚拟DOM”，也正因为单纯，“性能”方
         面的问题，很大一部分由使用者决定。

         Vue 的 template 像是先定个框架，有些“规则”，就是 v-if 之类的语法，然后使用者
         “照猫画虎”，做出来的东西不至于有太大的“坑”。“性能”方面的优化，大部分框架内就
         主要负责了。

      2. 有什么区别
         React 这种灵活，使得它使用 &quot;门槛&quot; 高一点；而 Vue 在使用门槛稍低，但在有些业务
         场景下 template 的 &quot;灵活度&quot; 就较低。

         但是 Vue 较 React 有个优势，就是 Vue 也提供 JSX，你可以根据使用场景选择，这方
         面是“灵活的”

      3. 一点感想
         要说殊途同归，框架最终还是一样，用JS在浏览器上操纵DOM；这里有几个点，JS，浏览
         器，DOM；你看这几个怎么联系起来？很神奇，vue-devtools，上节课的 devtools，这
         是不是 callback 呢。</div>2021-11-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/d8/96/dcf52430.jpg" width="30px"><span>关关君</span> 👍（3） 💬（1）<div>今天跟着老师的代码做练习的时候控制台报错说没有 defineConfig 一看版本vite才是1.0的，如果遇到和我一样的问题的同学先卸载 &quot;npm un vite&quot; 然后重新安装新版本的vite  &quot;npm install vite@latest -D&quot;</div>2021-11-19</li><br/><li><img src="" width="30px"><span>gongshun</span> 👍（2） 💬（1）<div>&lt;component :is=&quot;&#39;h&#39;+ level&quot;&gt;&lt;&#47;component&gt; 这样就可以实现了，jsx是多余</div>2021-11-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/23/a6/88858c72.jpg" width="30px"><span>mixiuu</span> 👍（1） 💬（1）<div>老师，我想问下，在cli创建的vue3中，使用setup+jsx的方式会报错（TypeError: Cannot read properties of undefined (reading &#39;$createElement&#39;)），我在babel.config.js中已添加： &quot;plugins&quot;: [&quot;@vue&#47;babel-plugin-jsx&quot;]，这是为什么呢</div>2021-11-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/2f/5b/74ba6ffa.jpg" width="30px"><span>酱汁</span> 👍（1） 💬（3）<div>想问下老师开源组件库种中 这种组合方式  jsx怎么实现的
 &lt;tabs&gt;
   &lt;tab-pane&gt; 内容1  &lt;&#47;tab-pane&gt;
   &lt;tab-pane&gt; 内容2 &lt;&#47;tab-pane&gt;
   &lt;tab-pane&gt; 内容3 &lt;&#47;tab-pane&gt;
 &lt;&#47;tabs&gt;</div>2021-11-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/e8/27/0472c557.jpg" width="30px"><span>张飞蓬</span> 👍（0） 💬（2）<div>然后是 @click 函数增加了一个 cache 缓存层，这样实现出来的效果也是和静态提升类似，尽可能高效地利用缓存。最后是，由于在下面代码中的属性里，那些带冒号的属性是动态属性，因而存在使用一个数字去标记标签的动态情况。比如在 p 标签上，使用 8 这个数字标记当前标签时，只有 props 是动态的。而在虚拟 DOM 计算 Diff 的过程中，可以忽略掉 class 和文本的计算，这也是 Vue 3 的虚拟 DOM 能够比 Vue 2 快的一个重要原因。

没看懂这个啥缓存层呢</div>2022-01-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/f7/0b/b01f1d68.jpg" width="30px"><span>百事可乐</span> 👍（0） 💬（3）<div>大圣老师。 我怎么从vue 文件向  jsx文件中传递参数呢？
&lt;Todolist :valueData=&#39;123&#39;&#47;&gt; 
setup(props) {
        console.log(props);
}    这个 props  是这个空对象 </div>2021-11-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/7f/14/ebe97682.jpg" width="30px"><span>小余GUNDAM</span> 👍（0） 💬（1）<div>老师 vue3的 jsx能享受 编译优化 例如静态节点跳过diff吗 </div>2021-11-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/78/7f/ef0e0ec8.jpg" width="30px"><span>uncle 邦</span> 👍（0） 💬（1）<div>vue2 可以使用jsx么？</div>2021-11-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/8a/d7/daabec34.jpg" width="30px"><span>tequ1lAneio</span> 👍（0） 💬（2）<div>为什么我的input用jsx的话无论是keyup还是keydown都绑定不上事件？</div>2021-11-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/89/2f/6211e738.jpg" width="30px"><span>台灯下的我</span> 👍（12） 💬（0）<div>我的理解是优先使用template，如果当用template的时候感觉很麻烦很繁琐的时候，这个时候可以考虑下jsx能不能更方便一点</div>2021-11-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/5b/9e/a8dec12d.jpg" width="30px"><span>cwang</span> 👍（4） 💬（0）<div>补充了解：https:&#47;&#47;v3.cn.vuejs.org&#47;guide&#47;render-function.html</div>2021-12-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/3f/a8/8da58e53.jpg" width="30px"><span>海阔天空</span> 👍（2） 💬（0）<div>template 和 JSX 都有各自的优点，template 算是vue的标配吧，因为其中规中矩（标签化），所以在vue页面或是主要架构，动态性比较低的场景下使用。而JSX则更适合来做小组件和公共组件这些动态性比较高的组件。
</div>2021-11-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2e/64/77/755c94fa.jpg" width="30px"><span>猹子哥一个月要瘦十斤</span> 👍（1） 💬（1）<div>我觉得做动态表单的时候用jsx更舒服一点</div>2022-08-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/d8/e3/987c9195.jpg" width="30px"><span>Spike Jim.Fun</span> 👍（1） 💬（1）<div>export default defineComponent({ 这里可以不需要使用defineComponent</div>2022-05-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/4b/71/591ae170.jpg" width="30px"><span>大恒</span> 👍（1） 💬（1）<div>按照文稿中的代码，直接导出函数的方式导出的组件，和导出defineComponent实例化的组件区别是：defineComponent实例化的组件有实时更新vNode的能力对吗？
下面是我的示例代码，它并不能更新显示button的文本内容
export const Button = (props) =&gt; {
  let text = ref(&quot;click me!&quot;);
  function btnClick() {
    text.value += &quot;!&quot;;
  }
  return &lt;button onClick={btnClick}&gt;{text.value}&lt;&#47;button&gt;;
};
</div>2022-04-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e9/42/1de79e71.jpg" width="30px"><span>南山</span> 👍（1） 💬（0）<div>打卡， 项目比较简单，没用到jsx</div>2021-11-24</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eo3deJAzNI4Pn6xo8zoJPDIgxfv6NrV5iaYCBKSNL5RnkT1m0o7IryOZZSTuFeAkyHpicsTpUWZYDIA/132" width="30px"><span>Geek_d6ee59</span> 👍（1） 💬（0）<div>小白被打开新世界，之前用react多，热衷jsx的灵活，原来也可以这样写vue</div>2021-11-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/65/25/c6de04bc.jpg" width="30px"><span>斜月浮云</span> 👍（1） 💬（2）<div>个人认为，目前大部分页面的量级，性能影响都差别不太大，相比还是灵活性更重要，如果要二选一，还是jsx这种设计更符合开发需求。 当然都用用更好哈哈😄</div>2021-11-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1d/3a/cdf9c55f.jpg" width="30px"><span>未来已来</span> 👍（0） 💬（0）<div>安装 JSX 之后，需要重启 Vue：npm run dev</div>2023-09-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/78/6d/b4a595b1.jpg" width="30px"><span>蒋腾飞</span> 👍（0） 💬（0）<div>这篇文章真是太棒啦～</div>2023-02-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/c9/f9/39492855.jpg" width="30px"><span>阿阳</span> 👍（0） 💬（0）<div>
正在做动态表单，用temple语法感觉不够灵活，现在考虑用jsx实现。</div>2022-08-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/54/9c/b83c52be.jpg" width="30px"><span>刘佳旭</span> 👍（0） 💬（0）<div>XRender,动态表格 都是用JSX</div>2022-06-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/b0/2f/e2096905.jpg" width="30px"><span>马成</span> 👍（0） 💬（4）<div>h函数感觉是比template要更加的灵活，那么template能够实现的功能h函数是否全部可以模拟实现呢？举个例子，template中的v-for指令使用h函数如何模拟类似的效果</div>2022-06-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/18/4e/9beaf580.jpg" width="30px"><span>yanhu</span> 👍（0） 💬（0）<div>动态组件
  &lt;template&gt;
    &lt;Component :is=&quot;comp.name&quot; v-bind=&quot;comp&quot;&gt;
  &lt;&#47;template&gt;
  
  如何将 jsx 作为 slot 传入？</div>2022-02-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/56/ea/32608c44.jpg" width="30px"><span>giteebravo</span> 👍（0） 💬（0）<div>
对 jsx 有了感性的认识</div>2021-11-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/e3/62/141946fb.jpg" width="30px"><span>绿亦歌º</span> 👍（0） 💬（0）<div>第一</div>2021-11-15</li><br/>
</ul>