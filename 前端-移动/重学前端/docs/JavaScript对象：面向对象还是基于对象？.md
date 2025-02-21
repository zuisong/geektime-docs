你好，我是winter。

与其它的语言相比，JavaScript中的“对象”总是显得不那么合群。

一些新人在学习JavaScript面向对象时，往往也会有疑惑：

- 为什么JavaScript（直到ES6）有对象的概念，但是却没有像其他的语言那样，有类的概念呢；
- 为什么在JavaScript对象里可以自由添加属性，而其他的语言却不能呢？

甚至，在一些争论中，有人强调：JavaScript并非“面向对象的语言”，而是“基于对象的语言”。这个说法一度流传甚广，而事实上，我至今遇到的持有这一说法的人中，无一能够回答“如何定义面向对象和基于对象”这个问题。

实际上，基于对象和面向对象两个形容词都出现在了JavaScript标准的各个版本当中。

我们可以先看看JavaScript标准对基于对象的定义，这个定义的具体内容是：“语言和宿主的基础设施由对象来提供，并且JavaScript程序即是一系列互相通讯的对象集合”。

这里的意思根本不是表达弱化的面向对象的意思，反而是表达对象对于语言的重要性。

那么，在本篇文章中，我会尝试让你去理解面向对象和JavaScript中的面向对象究竟是什么。

## 什么是面向对象？

我们先来说说什么是对象，因为翻译的原因，中文语境下我们很难理解“对象”的真正含义。事实上，Object（对象）在英文中，是一切事物的总称，这和面向对象编程的抽象思维有互通之处。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/15/41/bf/3afa1344.jpg" width="30px"><span>如斯</span> 👍（27） 💬（5）<div>有个疑惑哈，讲道理symbolObj对象也是对象。也可以调用symbolObj.toString方法（ symbolObj.toString()  &#47;&#47; &quot;Symbol(a)&quot; ）。
但为什么会 symbolObj+&#39;&#39; 会报错呢。
Uncaught TypeError: Cannot convert a Symbol value to a string at &lt;anonymous&gt;:1:10</div>2019-02-13</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLCbzuoGvE6TMW7MIvL2RcKDN3omNrpss65wS6kabdYnhk33xtXUUeCTyjYRM6TUaQCibURWxaLGFA/132" width="30px"><span>朋友</span> 👍（7） 💬（3）<div>getter setter实际应用的例子有哪些？ vue的数据，视图双向绑定算吗？</div>2019-02-22</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTI7iakTvMwXWBHCK6WicIV2M3yQMZ8BtBgYgzARcEjbEtcWfKsQ2JqpZianKibZ2D7l1D3rwyTOL56Pzw/132" width="30px"><span>Jackchoumine</span> 👍（3） 💬（1）<div>let obj = {};
&#47;&#47; let _a=&quot;&quot;
Object.defineProperty(obj, &quot;a&quot;, {
  &#47;&#47; value: 123,
  &#47;&#47; writable:true,
  configurable: true,
  &#47;&#47; get: function() {
  &#47;&#47;   return &quot;这是访问器属性&quot;;
  &#47;&#47; }
  set: function(newValue) {
    console.log(newValue);
    this.a = newValue;
  }
});
Object.defineProperty(obj, &quot;hi&quot;, {
  value: function() {
    console.log(&quot;Hello&quot;);
  },
  configurable: false
});
console.log(obj);
console.log(&quot;before&quot;, obj.a);
obj.a = &quot;aaaa&quot;;

为甚么这样报错了：xJAjOnELvGnk:55 Uncaught RangeError: Maximum call stack size exceeded.</div>2019-09-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/0f/88/6a262dc8.jpg" width="30px"><span>cnzhujie</span> 👍（2） 💬（6）<div>个人理解：面向对象就是万物皆为类，离开了类就活不了；比如Java里面，就算只写个main函数也要用class包裹起来。而基于对象说的是这门语言可以使用类和对象，但不使用类和对象也照样玩的转，比如c++、php、js。</div>2019-04-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/79/b8/92708e0e.jpg" width="30px"><span>艺术就是派大星</span> 👍（0） 💬（1）<div>OC的面向对象思想简直就是反人类。。。一种基于消息发送的smalltalk风格。。。然鹅OC是比C++还早的面向对象语言。。。</div>2019-09-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/af/9a/23603936.jpg" width="30px"><span>胡琦</span> 👍（0） 💬（1）<div>配图是照猫画虎？
Object. defineProperty是不是有兼容性呢？</div>2019-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/46/58/31205087.jpg" width="30px"><span>恋着歌</span> 👍（0） 💬（1）<div>数据属性、访问器属性，也叫数据描述符、存取描述符，只能选择一种描述符，https:&#47;&#47;developer.mozilla.org&#47;zh-CN&#47;docs&#47;Web&#47;JavaScript&#47;Reference&#47;Global_Objects&#47;Object&#47;defineProperty</div>2019-02-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/69/b4/8d9630ca.jpg" width="30px"><span>风清不扬</span> 👍（146） 💬（10）<div>php 是世界上最好的編程語言</div>2019-01-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/04/42/c0be8d43.jpg" width="30px"><span>37°C^boy</span> 👍（105） 💬（1）<div>这篇讲的思路太好了，追本溯源，娓娓道来。在这里不光能学到知识活着重温知识，还有关于学习和讲授的方法lun</div>2019-01-29</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/gvfibNc3Bol6DzLMG5ia9wSLVYseoq326iae7TczmgmBj9u3Jwt8c0hl9KSzY4GNTFn0ic9m1ibzicqJ3aGzeQemec2Q/132" width="30px"><span>hhk</span> 👍（58） 💬（3）<div>关键点在于是否可以在运行时动态改变对象

结合文章通篇看下来，觉得 JS 的 OO 和他基于类的 OO 不同之处，在于 JS 可以在运行时修改对象，而 class based 的类只能预先全部定义好，我们并不能在运行时动态修改类。在我理解来说，条条大路通罗马，面向对象是罗马，class based 是一条路，prototype based 是另一条路。而且 Symbol 的出现，暴露出了许多内置接口，让 JS 又在这条路上走了更远一些。（以前上学背面向对象的三个特征，封装，继承，多态，现在看一下突然觉得很对。。。

像我这种年轻一点的前端，很可能就只是相对熟悉 JS 而已，对于其他语言更多都是道听途说，计算机基础也比较薄弱，所以用来比较其实比较难。
只知道 class based 的大概有 Java，C++, C#, Python

另外，好奇 Symbol 是怎么实现的，希望老师以后能大概讲讲啦。暂时只想到这些，其他的还在消化</div>2019-01-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/39/30/f7df6ba7.jpg" width="30px"><span>米斯特菠萝</span> 👍（39） 💬（4）<div>好像winter老师没有回答过同学的提问，是我没看见吗？</div>2019-01-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/08/75/512b9f26.jpg" width="30px"><span>张汉桂-东莞</span> 👍（37） 💬（3）<div>    var o = { get a() { return 1 } };
    console.log(o.a); &#47;&#47; 1

看到这段我就感到值了。我目前在用layui框架，根据layui文档的描述，只有执行var form = layui.form;这一句时才会下载form.js这个文件，我一直没能理解。这篇文章解除了我的疑惑，原来调用getter时可以不写括号()。谢谢老师！</div>2019-01-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/07/97/68388d28.jpg" width="30px"><span>王小宏music</span> 👍（25） 💬（1）<div>var o = { get a() { return 1 } }
console.log(o.a); &#47;&#47; 1
肯定有同学对这里有疑问，解释一下吧， 这里边应用到了ES6的getter,setter属性， 为啥o.a，没写小括号呢？ 因为每次访问get，函数返回为1，作为一个value返回的，而非Obj中，调用某个方法，所以才没写成Obj.fun()的方式， 另外 老师下边有一句总结，很容易遗漏 ，每次访问，访问器属性，都会执行get,set方法</div>2019-03-19</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/3Uk6JicOE0D8BC5SQbPHlIZ33llRPTmkDquCOLW1d5gibicrEb5P1UncZnBRAv9KPdjYyuAzs263KdXWQwp0Hp76A/132" width="30px"><span>bitmxy</span> 👍（24） 💬（2）<div>JS的設計者原本是個Lisp程序員而且不怎麼喜歡Java面向對象，所以採用了原型。在當時基於原型比基於類的做法要靈活很多。
</div>2019-01-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/1d/17/94e4c63a.jpg" width="30px"><span>咩啊</span> 👍（16） 💬（4）<div>请问“运行时”是指什么？一开始我以为是指“程序执行的时候”这一时间状态，但是在正文倒数第三段又有“但是 JavaScript 提供了完全运行时的对象系统，这使得它可以模仿多数面向对象编程范式”这一句，这里的“完全运行时”是什么意思？我上网查了一下，好像没有比较符合的解析。</div>2019-02-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/2b/d6/945f0d82.jpg" width="30px"><span>_(:з」∠)_</span> 👍（16） 💬（2）<div>太难了(눈_눈)
完全没看懂面向对象，有没有更加数学一点更加精确一点的定义啊。
( •̥́ ˍ •̀ू )</div>2019-02-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/94/56/4b8395f6.jpg" width="30px"><span>CC</span> 👍（12） 💬（0）<div>我暂时接触的编程有限，JavaScript 是我接触的第一个面向对象语言。

由于缺少对其他语言的了解，winter 老师在文中的横向对比，感觉能让我更容易理解 JavaScript 的设计思路，以及 Object 这么设计的原因。

关于ECMAScript 2015 加入的 “类”，其实它并不是 JavaScript 新增的面向对象模式，它主要是语法糖的作用，只是一种特殊的函数，背后仍然是基于原型的设计思路。
</div>2019-01-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/35/e6/5a05a2fb.jpg" width="30px"><span>庖丁</span> 👍（12） 💬（0）<div>我们应该在理解其设计思想的基础上充分挖掘它的能力，而不是机械地模仿其它语言。</div>2019-01-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/b5/73/7ed0cfb7.jpg" width="30px"><span>next_one</span> 👍（11） 💬（0）<div>我理解的，重学前端专栏的意义是，从语言使用者的角度，转到语言实现者的角度，来看待语言的发展，通过对比其他语言，来阐述js语言本身的特性。重学的意义在于，多数开发者是语言使用者，而没有从语言实现者的角度，对语言本身有思考。有一种“不识庐山真面目，只缘身在此山中”的感觉。简单说，就是大多数人就是用用，没有想过（或者没有能力）去了解语言本身的来龙去脉。</div>2019-10-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/29/39/0aec7827.jpg" width="30px"><span>费马</span> 👍（9） 💬（0）<div>这才理解数值属性和访问器属性！赞</div>2019-02-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/f9/bc/cbc0207b.jpg" width="30px"><span>Scorpio</span> 👍（7） 💬（1）<div>感觉js出es6后，和java更像了。。</div>2019-01-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/65/3a/48f3f4e8.jpg" width="30px"><span>白嗣</span> 👍（6） 💬（0）<div>老师是否按照犀牛书的顺序讲解😁</div>2019-01-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/78/51/4790e13e.jpg" width="30px"><span>Smallfly</span> 👍（6） 💬（0）<div>基于类的面向对象使用的是继承，而 Javascript 更像是组合。</div>2019-01-29</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/SqTNLaU4hVdkqbXzFtwjZFYmdZ2BvSiaOy8hOkLxGDWatO2eWZ5hDR5kplq5j184T9KAlnMHWico0VkgXt8pq6og/132" width="30px"><span>Geek_szk4iq</span> 👍（4） 💬（1）<div>做了几年的前端开发，算是老学生不算优等生。越来越讨厌JS目前的状态，被赋予了太多的责任和设计思想，借鉴了太多其他语言，新特性、新玩法层出不穷。     前端开发者太累了，真的太累了 。 一门被拿来玩玩的脚本语言承受了太多它不该承受的... </div>2020-06-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/db/26/54f2c164.jpg" width="30px"><span>靠人品去赢</span> 👍（3） 💬（0）<div>关于JS可以动态添加属性，反之Java就不行，分分钟给你一个报错。这个平时没注意，一对比确实觉得挺有意思。</div>2019-02-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/57/0e/36847d8c.jpg" width="30px"><span>宋捷</span> 👍（2） 💬（3）<div>什么时候Symbol作为属性的键去使用呢？实际的应用场景还比较模糊想不到，有同学和老师简单提示下吗？</div>2020-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/22/c1/a662fadf.jpg" width="30px"><span>桂马</span> 👍（2） 💬（3）<div>js是一个具有动态性的面向对象的语言，ES2015前主要以“prototype”面向对象编程，ES2015问世后主要以“class”实现面向对象编程，我想super也是借鉴Java的，以后js可能还会有interface，那就更灵活了</div>2019-03-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/b1/92/f3dabcb1.jpg" width="30px"><span>小小代码</span> 👍（2） 💬（0）<div>个人感觉JavaScript基于原型的面向对象设计比Java基于类的面向对象设计灵活</div>2019-02-14</li><br/><li><img src="" width="30px"><span>Geek_f2de52</span> 👍（1） 💬（0）<div>这篇看了之后真的颇有感触，学到了。javascript是一种面向对象的语言，但是又不是和我们熟知的java和C++语言采用完全相同的构建思路。java和C++的面向对象定义不同的静态类型，实例化产生对象。而javascript的对象是一个高度动态灵活的对象，可以在运行时动态增删属性。</div>2022-04-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/7b/ee/53124b75.jpg" width="30px"><span>东坡芝士</span> 👍（1） 💬（0）<div>JS是面向对象，只是不同于其他主流面向对象的设计，在继承和多态特性上的编程范式不一致。他符合的是面向对象的思想，语言标准。</div>2020-10-27</li><br/>
</ul>