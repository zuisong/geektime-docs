你好，我是石川。

在前面一讲中，我们提到了 React 也有一个 JavaScript 的语法扩展，叫做 JSX。它的全称是 JavaScript XML，顾名思义，它是以 XML 为格式设计的。它最主要的目的是与 React 框架结合，用于应用中 Web UI 相关的开发。在React中，DOM 树是通过 JSX 来定义的，最终会在浏览器中渲染成 HTML。基于 React 的普及率，即使你没有用过 React，估计对 JSX 也有所耳闻。

今天，我们就来看看 JSX 是如何用在 Web UI 开发中的。即使你不使用 React，这样的模版模式也有很大的借鉴意义。

## 类HTML的元素

首先，我们来看下 JSX 的基本使用，它是如何创建元素、相关的属性和子元素的。

你可以把 JSX 元素当成一种新的 JavaScript 语法表达。我们知道在标准的 JavaScript 中，字符串的字面量是通过双引号来分隔的，正则表达式的字面量是通过斜线号来分隔的。类似的，JSX 的字面量则是通过**角括号**来分隔的。比如下面的 &lt;h1 /&gt; 标签就是一个简单的例子，通过这种方式，我们就创建了一个 React 的标题元素。

```javascript
var title = <h1 className="title">页面标题</h1>;
```

但是像上面这样的标签，我们知道JS引擎是没办法理解的，那它如何被运行呢？这时，我们可以通过我们在上一讲提到的 Babel 把 JSX 的表达**先转译成标准的 JavaScript，然后才会给到浏览器做编译和执行**。Babel 会把上面变量声明赋值中的 JSX 表达，转换成一个符合 JavaScript 规范的 createElement() 函数，来进行函数的调用。
<div><strong>精选留言（1）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/15/28/73/44a94124.jpg" width="30px"><span>陈英娜</span> 👍（0） 💬（0）<div>传统的模板引擎经常是要用字符串形式来拼接，可读性及复用性都非常差</div>2023-06-01</li><br/>
</ul>