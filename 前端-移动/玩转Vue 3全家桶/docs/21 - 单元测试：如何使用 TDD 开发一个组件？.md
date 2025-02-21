你好，我是大圣。

上一讲我们学习了不少组件库里的经典组件，用TypeScript搭建起了TypeScript + Vite + Sass的组件库开发基础环境，并且实现了Container布局组件。

今天我们来聊另外一个大幅提升组件库代码可维护性的手段：单元测试。在理解单元测试来龙去脉的基础上，我还会给你演示，如何使用测试驱动开发的方式实现一个组件，也就是社区里很火的TDD开发模式。

## 单元测试

单元测试（Unit Testing），是指对软件中的最小可测试单元进行检查和验证，这是百度百科对单元测试的定义。而我的理解是，在我们日常代码开发中，会经常写Console来确认代码执行效果是否符合预期，这其实就算是测试的雏形了，我们把代码中的某个函数或者功能，传入参数后，校验输出是否符合预期。

下面的代码中我们实现了一个简单的add函数, 并且使用打印3和add(1,2)的结果来判断函数输出。

add函数虽然看起来很简单，但实际使用时可能会遇到很多情况。比如说x如果是字符串，或者对象等数据类型的时候，add结果是否还可以符合预期？而且add函数还有可能被你的同事不小心加了其他逻辑，这都会干扰add函数的行为。

```javascript
function add(x,y){
  return x+y
}

console.log(3 == add(1,2))
```
<div><strong>精选留言（20）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/25/91/09/6f0b987a.jpg" width="30px"><span>陈坚泓</span> 👍（22） 💬（1）<div>工作三年 至今还没有机会用上单元测试</div>2022-05-06</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/kDyoSquJMmpZ8MDZRPh6U1n8ry7zW4fRUJ78yxOag61qSUtZQ953y2maNBpjkiaFd21UpIh95sxP6OegcNloFCA/132" width="30px"><span>小海</span> 👍（4） 💬（5）<div>赞, 发现两个小瑕疵
1.在 Button.spec.ts文件中 引入 button.vue组件时.会提示找不到该模块,后来看了github链接的源码才发现是需要在src目录下增加 env.d.ts文件,才能使TS文件顺利引入vue文件的组件,
2. babel.config.js 在课程资料里是创建  .babel.config.js文件  但是源码里并没有&quot;.&quot; 不晓得哪个才是正确写法</div>2021-12-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/fe/8a/8b5f5a66.jpg" width="30px"><span>下一个起跑点</span> 👍（2） 💬（1）<div>还是那句话，等你写完单元测试，项目都上线了，测试还是留着空闲时再写吧</div>2021-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c3/58/ba171e09.jpg" width="30px"><span>小胖</span> 👍（1） 💬（3）<div>接上一篇提问：上篇文章的几个布局组件，定义Props类型的时候。老师有时是使用type、有时用interface，有什么说法么？</div>2021-12-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/fa/7d/6a5065e6.jpg" width="30px"><span>小甜酒</span> 👍（0） 💬（1）<div>
➜  ailemente git:(main) ✗ node add.js
测试数字相加 测试通过
这个运行报错是需要安装什么嘛</div>2022-01-14</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/7icj7X67vvABNjC284ichONicn6PFeZSUAdclWKr8FJIHfWUzx6azxPuDcCNODV8ZmqXMAUibvJZiaXsYxKCmtJfxkg/132" width="30px"><span>于三妮</span> 👍（0） 💬（1）<div>直到现在还没用过自动化测试呢~~</div>2021-12-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e9/42/1de79e71.jpg" width="30px"><span>南山</span> 👍（0） 💬（1）<div>传入的circle属性，生成.btn--circle的classname，实现圆角样式</div>2021-12-08</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83errHypG6kuO0YibnBulyljZ8P5Mtb9iaicVx2VoibKNjYKJfTw16QvmDMmKM5gLsEtno0xU2VnM2FUTzQ/132" width="30px"><span>Geek_623ed8</span> 👍（7） 💬（0）<div>记录一下报错：
ReferenceError: module is not defined in ES module scope
找到package.json里的&quot;type&quot;: &quot;module&quot; 去掉</div>2022-09-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/3f/a8/8da58e53.jpg" width="30px"><span>海阔天空</span> 👍（2） 💬（0）<div>感觉单元测试这块用得比较少，还是用console检查用得比较多，这可能和项目的迭代周期有关。单元测试确实比较更全面。</div>2021-12-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/ed/48/4a40816a.jpg" width="30px"><span>刷子iNG</span> 👍（1） 💬（0）<div>这讲，对自己写个ui库提升kpi很有帮助啊</div>2022-02-15</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/LWicoUend7QOH6pyXGJyJicFn2ITHZ7iaVorxj3cNlX0EOfknIvgC0mPrVPS0CavPGbwMbRM3Jb0V7HIRicq5bEc8g/132" width="30px"><span>Geek_116864</span> 👍（0） 💬（0）<div>还是没明白函数测试怎么用，项目中函数一般都在.vue文件中，要把.vue中的函数copy到.spec.js这里去执行吗</div>2024-07-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/54/d0/6a04d601.jpg" width="30px"><span>但江</span> 👍（0） 💬（0）<div> FAIL  src&#47;components&#47;button&#47;Button.spec.ts
  ● Test suite failed to run

    src&#47;components&#47;button&#47;Button.spec.ts:1:20 - error TS2307: Cannot find module &#39;.&#47;Button.vue&#39; or its corresponding type declarations.

    1 import Button from &#39;.&#47;Button.vue&#39;

Button.vue 确实存在</div>2023-10-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/05/81/da39f079.jpg" width="30px"><span>Le Soleil</span> 👍（0） 💬（0）<div>按老师的代码敲了，报这个错，有谁知道怎么解决吗？

TypeError: Cannot read properties of null (reading &#39;compilerOptions&#39;)

    &gt; 1 | import Button from &#39;..&#47;..&#47;packages&#47;button&#47;index.vue&#39;
        | ^
      2 | import { mount } from &#39;@vue&#47;test-utils&#39;
      3 | describe(&#39;按钮测试&#39;, () =&gt; {
      4 |   it(&#39;按钮能够显示文本&#39;, () =&gt; {

      at Object.process (node_modules&#47;vue-jest&#47;lib&#47;transformers&#47;typescript.js:33:16)
      at processScript (node_modules&#47;vue-jest&#47;lib&#47;process.js:44:30)
      at Object.module.exports [as process] (node_modules&#47;vue-jest&#47;lib&#47;process.js:138:24)
      at ScriptTransformer.transformSource (node_modules&#47;@jest&#47;transform&#47;build&#47;ScriptTransformer.js:464:35)
      at ScriptTransformer._transformAndBuildScript (node_modules&#47;@jest&#47;transform&#47;build&#47;ScriptTransformer.js:569:40)
      at ScriptTransformer.transform (node_modules&#47;@jest&#47;transform&#47;build&#47;ScriptTransformer.js:607:25)
      at Object.&lt;anonymous&gt; (test&#47;packages&#47;button.spec.ts:1:1)</div>2022-12-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/0c/8b/e967775c.jpg" width="30px"><span>金针菇饲养员</span> 👍（0） 💬（0）<div>ReferenceError: module is not defined in ES module scope
</div>2022-08-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/0c/8b/e967775c.jpg" width="30px"><span>金针菇饲养员</span> 👍（0） 💬（0）<div>你们都按照老师代码敲了么，有发现这些报错么？
babel.config.js: Error while loading config - You appear to be using a native ECMAScript module configuration file, which is only supported when running Babel asynchronously.</div>2022-08-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/c2/67/93b7c47e.jpg" width="30px"><span>宋玉</span> 👍（0） 💬（0）<div>Also note that the APIs Jest uses to implement ESM support is still considered experimental by Node (as of version 14.13.1). node 版本需要 14.13.1 以上否则会报错</div>2022-05-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/90/6e/d729672d.jpg" width="30px"><span>云中歌</span> 👍（0） 💬（0）<div>能讲讲ui测试吗</div>2022-04-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/97/44/52b5e2e2.jpg" width="30px"><span>cweioo</span> 👍（0） 💬（1）<div>toBe not defined</div>2022-01-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/fa/7d/6a5065e6.jpg" width="30px"><span>小甜酒</span> 👍（0） 💬（0）<div>
➜  ailemente git:(main) ✗ node add.js
测试数字相加 测试通过</div>2022-01-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/b7/59/9a0cad96.jpg" width="30px"><span>爱我所爱</span> 👍（0） 💬（0）<div>几乎不用单元测试，工作中不用</div>2022-01-05</li><br/>
</ul>