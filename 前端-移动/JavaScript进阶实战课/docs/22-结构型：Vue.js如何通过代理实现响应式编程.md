你好，我是石川。

上一讲我们介绍了几种不同的创建型模式，今天我们来说说设计模式中的结构型模式。在结构型模式中，最经典、最常用的就非代理模式莫属了。在JavaScript的开发中，代理模式也是出现频率比较高的一种设计模式。

前端的朋友们应该都对Vue.js不会感到陌生。Vue.js的一个很大的特点就是用到了如今流行的响应式编程（Reactive Programming）。那它是怎么做到这一点的呢？这里面离不开代理模式，这一讲我们主要解答的就是这个问题。但是在解开谜底之前，我们先来看看代理模式比较传统直观的一些应用场景和实现方式吧。

## 代理的应用场景

在代理设计模式中，一个代理对象充当另一个主体对象的接口。很多人会把代理模式和门面模式做对比。后面几讲，我们会介绍到门面模式。这里我们需要了解的是代理模式与门面模式不同，门面模式最主要的功能是简化了接口的设计，把复杂的逻辑实现隐藏在背后，把不同的方法调用结合成更便捷的方法提供出来。而代理对象在调用者和主体对象之间，主要起到的作用是保护和控制调用者对主体对象的访问。代理会拦截所有或部分要在主体对象上执行的操作，有时会增强或补充它的行为。

![图片](https://static001.geekbang.org/resource/image/c1/2a/c1955c431c2166d62da6f956576ec32a.png?wh=1920x695)

如上图所示，一般代理和主体具有相同的接口，这对调用者来说是透明的。代理将每个操作转发给主体，通过额外的预处理或后处理增强其行为。这种模式可能看起来像“二道贩子”，但存在即合理，代理特别是在性能优化方面还是起到了很大作用的。下面我们就一一来看看。
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/21/10/5e/42f4faf7.jpg" width="30px"><span>天择</span> 👍（1） 💬（1）<div>响应式编程可以利用“副作用”达到目的（比如更新UI），函数本身可能不是目的。而函数式编程还包括如“纯函数”一类的消除副作用的场景，函数本身即是目的。</div>2022-11-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/f4/73/8079d3fd.jpg" width="30px"><span>郭慧娟</span> 👍（0） 💬（1）<div>对象增强的那个例子，为什么会有副作用呢？</div>2022-11-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/6a/18/d9e067f0.jpg" width="30px"><span>cyw0220</span> 👍（0） 💬（2）<div>运算符重载的例子执行下来返回的是1啊，不太能理解13行的obj.count为啥会设置count</div>2022-11-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/40/d0/4aa34250.jpg" width="30px"><span>peter</span> 👍（0） 💬（1）<div>import { reactive, computed } from &#39;vue&#39;
var A0 = reactive(0);
var A1 = reactive(1);
var A2 = computed(() =&gt; A0.value + A1.value);
A0.value = 2;


这段代码应该是用 ref</div>2022-11-08</li><br/>
</ul>