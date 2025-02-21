你好，我是周爱民，欢迎回到我的专栏。

今天是专栏最后一讲，我接下来要跟你聊的，仍然是JavaScript的动态语言特性，主要是动态函数的实现原理。

标题中的代码比较简单，是常用、常见的。这里稍微需要强调一下的是“最后一对括号的使用”，由于运算符优先级的设计，它是在new运算之后才被调用的。也就是说，标题中的代码等义于：

```
// （等义于）
(new Function('x = 100'))()

// （或）
f = new Function('x = 100')
f()
```

此外，这里的`new`运算符也可以去掉。也就是说：

```
new Function(x)

// vs.
Function(x)
```

这两种写法没有区别，都是动态地创建一个函数。

## 函数的动态创建

如果在代码中声明一个函数，那么这个函数必然是具名的。具名的、静态的函数声明有两个特性：

1. 是它在所有代码运行之前被创建；
2. 它作为语句的执行结果将是“空（Empty）”。

这是早期JavaScript中的一个硬性的约定，但是到了ECMAScript 6开始支持模块的时候，这个设计就成了问题。因为模块是静态装配的，这意味着它导出的内容“应该是”一个声明的结果或者一个声明的名字，因为只有**声明**才是静态装配阶段的特性。但是，所有声明语句的完成结果都是Empty，是无效的，不能用于导出。

> NOTE：关于6种声明，请参见《[第02讲](https://time.geekbang.org/column/article/165198)》。

而声明的名字呢？不错，这对具名函数来说没问题。但是匿名函数呢？就成了问题了。
<div><strong>精选留言（10）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/18/cd/4b/36396a18.jpg" width="30px"><span>独钓寒江雪</span> 👍（8） 💬（1）<div>今天读完了专栏必学内容的最后一讲，跟着老师的步伐一路走来，很艰辛，同时也收获很多，通过一行极简的代码去洞悉一门语言的核心原理，也是我一直梦想着能做到的事，向老师致敬！

其实，可以说，看这种底层的东西，每一讲都很吃力，要想有更深入的理解，必须再花时间回过头反复研读；其实，阅读专栏，很多时候也是一种思维的提升，比如以前只知道变量提升，却没想过为什么要提升；知道...运算符，却说不出为什么可以用它来展开对象。。。

或许专栏短期内对开发能力不会有多么显著的提升，但我相信，因为对语言本质的洞悉而产生的自信以及思想层面的提升，将会使我在前端走的更远。衷心的感谢🙏</div>2020-01-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/dc/90/c980113a.jpg" width="30px"><span>行问</span> 👍（4） 💬（2）<div>new Function(x)  vs  Function(x) 没什么区别。如果是“类化”的话，也是没什么区别吗？在使用 class 声明一个类时，new class 与 class 直接调用。


函数是对象的概念比较清晰，明了。这让我想起之前的 &quot;null&quot;，请教个问题，在通常的开发中，会把一些变量释放空间，把值置为 null, 那么如果是置为 {} 呢？如下：


var a = null 和 var a = {}，是否有大差异？


我的理解是 {} 会存放在“堆空间”占据内存，但同时它是一个空对象，null 也是一个什么都没有的空对象，但 null 也是其它对象的原型，所以也会有 Object.create(null)


不知道周大能否看懂我的逻辑？

感谢
</div>2020-01-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/3a/93/d7be8a1a.jpg" width="30px"><span>晓小东</span> 👍（2） 💬（1）<div>好快，这个专栏结束了，有点舍不得，一个多月来我一直关注老师更新，反复阅听之前章节。体会深思理解，发现如果没有老师带领层层分析JavaScript 最核心那部分设计和概念，真的无缘了解这门语言了，谢谢老师给我们思维上的提升，同时也发现自己对这门语言的理解上，上了一个大大的台阶。在此由衷的感谢，真的感觉，遇到了恩师。</div>2020-01-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/04/8d/005c2ff3.jpg" width="30px"><span>weineel</span> 👍（1） 💬（1）<div>老师的每一篇都很有深度。我们平时开发中，this 的动态绑定虽然很复杂，但时间长了也能找到规律，仅仅是应用还是没啥问题的。老师要是有时间给我们加个餐，聊聊 this 的深层原理吧。</div>2020-01-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/63/5b/a23a82a4.jpg" width="30px"><span>大雄不爱吃肉</span> 👍（0） 💬（1）<div>专栏虽然是二十多讲，但是自己看了很久，很多地方反复看反复试。可能最终记住的不是很多，但对js以及语言规范有了深刻的理解，感谢老师这门课，这一门独特的课程我收获颇多，期待老师的下一门课！</div>2021-04-01</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqOtThoyf1GUazm9fn7jTFJiaf7yZwh9unGgLSsIJ2Op20wIpJHDw5ZxeCGf3ibZKdZ2K3ibCR1n71Hg/132" width="30px"><span>igetter</span> 👍（0） 💬（1）<div>老师，问一个不太相关的问题: MDN中说，Function()比eval()更高效。这是真的吗？</div>2020-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/18/11/f1f37801.jpg" width="30px"><span>James</span> 👍（0） 💬（2）<div>老师，我从头听了一遍，有几篇文章听了好几遍，但是感觉完全是云里雾里，没弄懂。我应该怎么办。🤣</div>2020-02-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（0） 💬（1）<div>一路跟着老师走过来，自以为对JavaScript这门语言有一定的了解，才发现只是懂点皮毛，更多深入的知识自己都还没有探究到，感谢老师带我领会了更深刻的JavaScript。之后还是会持续学习，保持对JavaScript的敬畏之心，加油。</div>2020-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/cd/4b/36396a18.jpg" width="30px"><span>独钓寒江雪</span> 👍（0） 💬（2）<div>以前有碰到了这样一个疑惑，看了专栏前面的内容，还是不太明白。下面是我的代码，虽然问题比较好解决，但是不太明白：
import { message } from &#39;antd&#39; &#47;&#47; 引入AntD组件库中的message
export const generateRemark = (skus, message) =&gt; {&#47;&#47; 这个方法被导出，接收两个参数，其中一个写成了message
  let remark = &#39;&#39;
  ......
  remark = remark + (message || &#39;&#39;)&#47;&#47;  使用了message参数
  return remark
}
当我调用generateRemark(skus, &#39;&#39;)时（message传入的是空字符串），返回是[object Object],调试发现，原来message被解析成了antd的message组件了。

是代码环境的问题还是JS底层机制的问题呢？希望老师能帮我解惑，谢谢🙏

最后，也感谢老师的专栏，这样关注底层核心原理的专栏，正是我这种自学前端出道的同学的所需要的。</div>2020-01-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/bb/01/568ac2d6.jpg" width="30px"><span>K4SHIFZ</span> 👍（0） 💬（0）<div>动态函数创建在规范19.2.1.1.1
Let proto be ? GetPrototypeFromConstructor(newTarget, fallbackProto).
Let realmF be the current Realm Record.
Let scope be realmF.[[GlobalEnv]].
Let F be ! OrdinaryFunctionCreate(proto, sourceText, parameters, body, non-lexical-this, scope).
Perform SetFunctionName(F, &quot;anonymous&quot;)</div>2020-05-03</li><br/>
</ul>