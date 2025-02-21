你好，我是大圣。

在上一讲中，我为你介绍了Vue中的JSX，以及template和JSX各自的优缺点。就像在上一讲中我提到的template牺牲灵活性换来了静态标记的收益，你能看到：有些时候，我们需要放弃一些灵活性去换取项目的整体收益。那么在这一讲中，我会给你介绍一个可以在语言层面上，提高代码可维护性和调试效率的强类型语言——TypeScript。

在整体上，我们的课程还是以使用JavaScript为主。对于TypeScript的内容，我会在这一讲中先带着你入门。下面，我会先讲一下TypeScript的入门知识 ；然后作为巩固，我会带你在Vue 3里再实战一下TypeScript；最后，我会对TypeScript和JavaScript这两者做一个对比分析，让你明白如何在这两者之间做一个更好的平衡。

## 什么是TypeScript

TypeScript是微软开发的JavaScript的超集，这里说的超集，意思就是TypeScript在语法上完全包含JavaScript。TypeScript的主要作用是给JavaScript赋予强类型的语言环境。现在大部分的开源项目都是用TypeScript构建的，并且Vue 3本身TS的覆盖率也超过了95%。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/13/c8/4a/3a322856.jpg" width="30px"><span>ll</span> 👍（27） 💬（1）<div>几节课学下来，发现工程就是“灵活与稳定”之间的平衡。
上节是 template 与 JSX 各自的优缺点，实际上也能看出各自设计对“灵活”与“稳定”的取舍。我非专业转行，对于类型系统有点学习体会：
  1. 动态 vs 静态语言
    从运行过程上说，动态比较简单，你写代码，然后丢给解释器运行，如果出错，就会报运行时错误 
  （runtime error）；静态语言比动态语言多个“门卫”，编译器，代码在运行前，它帮你检查一边，出问 
    题报错，报的是编译错误（compile error）。编译出错的代码根本不会走到运行时阶段。

  2. 怎么实现的
    静态语言怎么检查代码，通过“规则”，这个规则就是所谓的&quot;强类型系统&quot;。
    简单的说就是&quot;先定规则，再执行”，“先得有类型，才能执行”。这也是为什么它在“灵活性”上不如动 
    态语言。

 3. 超集
    刚开始看这个定义的时候也没搞太明白，后来就清楚了；各个厂家的浏览器中“实现”JavaScript 是根 
    据 ECMAScript 标准。而浏览器只能看的懂 JavaScript。
    所以 TypeScript 最终都会“编译”成 JavaScript 跑在宿主环境里。哪些在 ts 中看到的 “超级” 语法，关 
    键词 最终都会变成 js。

 4. 也挑个小错
     let todos:Ref(Todo[]) = ref([{title: &quot;学习Vue&quot;, done: false}]) 中，应该是 Ref&lt;Todo[]&gt; 吧
</div>2021-11-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/cd/ed/825d84ee.jpg" width="30px"><span>费城的二鹏</span> 👍（3） 💬（1）<div>了解了 TypeScript 的使用后，你可以回想一下 Vue 2 里有哪些写法是对 TypeScript 不友好的，以及我们应该怎么在 Vue 3 优化呢？

在公司项目使用 ts 开发 vue2，感觉这个写法掩盖了很多 vue2 本身的概念。比如说 data 方法没了，watch 方法没了，都变成了注解，不太容易理解到 vue 本身的设计思路。</div>2021-11-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/cd/ed/825d84ee.jpg" width="30px"><span>费城的二鹏</span> 👍（1） 💬（1）<div>const emit = defineEmits&lt;{

代码片段貌似不完整</div>2021-11-17</li><br/><li><img src="" width="30px"><span>Geek_0c8aff</span> 👍（0） 💬（1）<div>typescript加餐++++++</div>2021-11-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/9d/70/d575f2ab.jpg" width="30px"><span>以梦为马</span> 👍（0） 💬（1）<div>TS 加个餐吧，如何系统得在 Vue3 项目实战 TS，感觉现在 TS 都快成标准了，都在用</div>2021-11-22</li><br/><li><img src="" width="30px"><span>Geek_073752</span> 👍（0） 💬（1）<div>大圣老师，有计划TypeScript加餐吗？</div>2021-11-18</li><br/><li><img src="" width="30px"><span>Geek_a84b8d</span> 👍（63） 💬（1）<div>希望大圣老师有TS的加餐</div>2021-11-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/d8/96/dcf52430.jpg" width="30px"><span>关关君</span> 👍（10） 💬（0）<div>加餐 想看 TypeScript 和 Vue3 的 项目最佳实践</div>2021-11-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/ba/bd/446a2876.jpg" width="30px"><span>东东</span> 👍（10） 💬（0）<div>老师，后面的项目可以用TS写不？</div>2021-11-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/e8/f5/d851eb46.jpg" width="30px"><span>哎哟迪奥</span> 👍（5） 💬（0）<div>typescript yyds，大圣大佬yyds，加餐yyds。</div>2021-11-17</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83epmBmNzSU9po7PX7NapoPlIPoRWOUUAiaQ1RvOnqmMZkFLnVTKiafHEMzwiamEqWyDCYWcvpYunAJ5Kg/132" width="30px"><span>aehyok</span> 👍（2） 💬（0）<div>TS必须加餐</div>2021-11-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/08/8b/1b7d0463.jpg" width="30px"><span>晴空万里</span> 👍（2） 💬（0）<div>别加了 ts可以单独成课 毕竟前端不需要强类型 影响效率</div>2021-11-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/9b/9a/7c87614b.jpg" width="30px"><span>YK菌</span> 👍（1） 💬（0）<div>直接看文档吧~ https:&#47;&#47;v3.cn.vuejs.org&#47;guide&#47;typescript-support.html
</div>2022-04-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/ff/d1/7a4a6f4f.jpg" width="30px"><span>风一样</span> 👍（1） 💬（2）<div>你好，老师：我在&lt;script setup lang=&#39;ts&#39;&gt;里添加下面的代码：
let num: number = 100
num = &#39;aaa&#39;
怎么没有错误的提示呢？
而在单独的 ts 文件里这样写，就有一个错误信息。</div>2022-02-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/fa/f7/2af81dc7.jpg" width="30px"><span>未央-</span> 👍（1） 💬（0）<div>TS加餐加餐</div>2022-02-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/3f/a8/8da58e53.jpg" width="30px"><span>海阔天空</span> 👍（1） 💬（0）<div>ts是趋势了，我一直不喜欢在项目中使用ts，因为项目迭代太快，现在也考虑项目中引入ts。</div>2021-11-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/94/6a/d40f64ec.jpg" width="30px"><span>尝试者说</span> 👍（0） 💬（0）<div>let todoRef: Ref&lt;Todo[]&gt; = ref([
  {
    title: &#39;学习react&#39;,
    done: false
  }
])

let todo = ref&lt;Todo[]&gt;([
  {
    title: &#39;学习react&#39;,
    done: false
  }
])这两种写法有什么区别</div>2023-05-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/7f/09/1e95ccbf.jpg" width="30px"><span>爱拼才会赢</span> 👍（0） 💬（0）<div>求TS加餐</div>2022-07-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/04/aa/275a47d6.jpg" width="30px"><span>张泽涛</span> 👍（0） 💬（0）<div>ts 加餐加餐</div>2022-05-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/49/f7/a88dfb7c.jpg" width="30px"><span>kevin梁</span> 👍（0） 💬（0）<div>typescript会不会被微软制裁😓😓</div>2022-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/b4/e5/f4e2341c.jpg" width="30px"><span>余生只有你</span> 👍（0） 💬（0）<div>todos不应该是使用reactive来创建响应式吗？</div>2022-01-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/8a/9c/023d6963.jpg" width="30px"><span>div</span> 👍（0） 💬（0）<div>加餐 想看 TypeScript 和 Vue3 的 项目最佳实践</div>2021-12-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/75/4f/e22e91b2.jpg" width="30px"><span>雪狼</span> 👍（0） 💬（0）<div>希望加餐ts结合vue3</div>2021-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/48/4e/51896855.jpg" width="30px"><span>落风</span> 👍（0） 💬（0）<div>类型体操做起来！</div>2021-12-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/f9/e1/12dc66dd.jpg" width="30px"><span>JZ</span> 👍（0） 💬（0）<div>希望加餐</div>2021-11-29</li><br/><li><img src="" width="30px"><span>普通上班族_wt</span> 👍（0） 💬（0）<div>加餐</div>2021-11-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/21/0d/b6a547e0.jpg" width="30px"><span>Eliauk</span> 👍（0） 💬（0）<div>加餐加餐</div>2021-11-25</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/an41WXWK0xmCxYxsT3vxUFIenDSoHbJEeH6YYF6iao9K3j6qs7gfevjicb0M9Y67eRz5PZYnun8iapDrZGcp2sV1w/132" width="30px"><span>Geek_e84263</span> 👍（0） 💬（0）<div>现在新项目的开发用了vue3+ts</div>2021-11-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/76/ba/2373075b.jpg" width="30px"><span>陈豆</span> 👍（0） 💬（0）<div>希望加餐TypeScript！！</div>2021-11-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/aa/b6/81a6595f.jpg" width="30px"><span>superZchen</span> 👍（0） 💬（0）<div>希望大圣老师有ts的加餐 后面代码多用ts来写</div>2021-11-22</li><br/>
</ul>