你好，我是大圣。

上一讲我带你手写了一个迷你的Vue compiler，还学习了编译原理的基础知识。通过实现这个迷你Vue compiler，我们知道了tokenizer可以用来做语句分析，而parse负责生成抽象语法树AST。然后我们一起分析AST中的Vue语法，最后通过generate函数生成最终的代码。

今天我就带你深入Vue的compiler源码之中，看看Vue内部到底是怎么实现的。有了上一讲编译原理的入门基础，你会对Compiler执行全流程有更深的理解。

## Vue compiler入口分析

Vue 3内部有4个和compiler相关的包。compiler-dom和compiler-core负责实现浏览器端的编译，这两个包是我们需要深入研究的，compiler-ssr负责服务器端渲染，我们后面讲ssr的时候再研究，compiler-sfc是编译.vue单文件组件的，有兴趣的同学可以自行探索。

首先我们进入到vue-next/packages/compiler-dom/index.ts文件下，在[GitHub](https://github.com/vuejs/vue-next/blob/master/packages/compiler-dom/src/index.ts#L40)上你可以找到下面这段代码。

compiler函数有两个参数，第一个参数template，它是我们项目中的模板字符串；第二个参数options是编译的配置，内部调用了baseCompile函数。我们可以看到，这里的调用关系和runtime-dom、runtime-core的关系类似，compiler-dom负责传入浏览器Dom相关的API，实际编译的baseCompile是由compiler-core提供的。
<div><strong>精选留言（8）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/78/02/eeb3ce7f.jpg" width="30px"><span>Little何</span> 👍（3） 💬（3）<div>评论越来越少，表示看不懂</div>2022-02-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/00/fb/85b07045.jpg" width="30px"><span>肥柴</span> 👍（2） 💬（0）<div>大圣老师绘制的 Vue 全流程的架构图 超级赞!!!!</div>2022-07-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/39/d0/82/791d0f5e.jpg" width="30px"><span>大将</span> 👍（1） 💬（0）<div>新版本parse函数向较于之前有了很大的变动，建议后续学习的人，可以直接参考源码去看</div>2024-03-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/65/25/c6de04bc.jpg" width="30px"><span>斜月浮云</span> 👍（1） 💬（0）<div>全流程汇总图好评哦👍</div>2022-01-06</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKwICrbHZaPZV5LC0UkR9xwUSKHuEIETCYIhoRjKCyxgmia2iaiah2UEm09FxfBBJGgP9ld38ibQH8bOA/132" width="30px"><span>All Fiction</span> 👍（0） 💬（0）<div>跟不上了，先听个响，回头慢慢悟</div>2023-04-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/70/75/421516b6.jpg" width="30px"><span>文春伟</span> 👍（0） 💬（0）<div>全景图的一步一步更新很赞！</div>2022-06-12</li><br/><li><img src="" width="30px"><span>Hermanyin</span> 👍（0） 💬（0）<div>文章说  isVoidTag 判断标签是否是自闭合标签，isVoidTag是判断是否是合法标签把</div>2022-04-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/d8/96/dcf52430.jpg" width="30px"><span>关关君</span> 👍（0） 💬（0）<div>advance() advancePositionWithMutation() 这两个函数没怎么理解是干什么的？大圣老师有demo讲解吗？</div>2022-02-09</li><br/>
</ul>