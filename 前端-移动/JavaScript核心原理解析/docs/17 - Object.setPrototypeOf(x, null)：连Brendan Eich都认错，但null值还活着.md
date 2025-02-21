你好，我是周爱民。欢迎回来继续学习JavaScript。

今天是关于面向对象的最后一讲，上次已经说过，今天这一讲要讨论的是原子对象。关于原子对象的讨论，我们应该从`null`值讲起。

`null`值是一个对象。

## null值

很多人说JavaScript中的`null`值是一个BUG设计，连JavaScript之父Eich都跳出来对Undefined+Null的双设计痛心疾首，说`null`值的特殊设计是一个“抽象漏洞（abstraction leak）”。这个东西什么意思呢？很难描述，基本上你可以理解为在概念设计层面（也就是抽象层）脑袋突然抽抽了，一不小心就写出这么个怪胎。

> NOTE：[“typeof null”的历史](https://2ality.com/2013/10/typeof-null.html) , [JavaScript 的设计失误](https://juejin.im/entry/5b5ad2fb6fb9a04fb900de7c) 。

然而我却总是觉得不尽如此，因为如果你仔细思考过JavaScript的类型系统，你就会发现`null`值的出现是有一定的道理的（当然Eich当年脑子是不是这样犯的抽抽也未为可知）。怎么讲呢？

早期的JavaScript一共有6种类型，其中number、string、boolean、object和function都是有一个确切的“值”的，而第6种类型`Undefined`定义了它们的反面，也就是“非值”。一般讲JavaScript的书大抵上都会这么说：
<div><strong>精选留言（10）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/dc/90/c980113a.jpg" width="30px"><span>行问</span> 👍（12） 💬（1）<div>多看看技术在历史上是怎么出现的，怎么解决问题的，溯源这种“原型链”让我大呼过瘾。一路学习下来，有完全不懂，有闻所未闻，有懵逼，有茅塞顿开等。今天的这一讲，让我理解了 &quot;null&quot; 在实际开发中的合理运用。</div>2019-12-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/4d/d8/30355c61.jpg" width="30px"><span>程序员劝退师</span> 👍（3） 💬（1）<div>这是除了加餐课外，我能最快理解的一节课，嗯一定是我进步了😁</div>2019-12-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ee/28/c04a0c83.jpg" width="30px"><span>小炭</span> 👍（2） 💬（1）<div>“原子对象” 这一概念只有Javascript才会有吗，在C和C ++的标准术语也有这个“原子对象” 的定义。不知道他们之间有什么区别，或者这个定义的源头来自哪里？</div>2020-11-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/06/54/16bb64d0.jpg" width="30px"><span>蛋黄酱</span> 👍（2） 💬（2）<div>&gt; 如果 MyClass.prototype 指向 null，而 super 指向一个有效的父类，其结果如何呢

这配上示例代码，意思是说setPrototypeOf虽然字面上的意思是改变prototype但本质上只改变了super执行的对象? 我觉得不对吧？</div>2020-03-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/10/30/c07d419c.jpg" width="30px"><span>卡尔</span> 👍（0） 💬（1）<div>老师，我记得有一本书里说，undefined派生于null。老师这句话怎么去理解，他俩到底是什么关系？有什么区别？</div>2021-01-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a3/ea/53333dd5.jpg" width="30px"><span>HoSalt</span> 👍（0） 💬（1）<div>class A {}
class B extends A {}
B.__proto__ === A &#47;&#47; true

B.__proto__.__proto__ === Function.prototype &#47;&#47; true

class MyClass extends null {}

MyClass.__proto__ === Function.prototype &#47;&#47; true
老师继承自null的类的原型链直接指向了Function.prototype，而其它的是在中间加了一层，这是一种特殊处理？</div>2020-05-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/05/6e0193b5.jpg" width="30px"><span>新哥</span> 👍（0） 💬（0）<div>是时候讲一下 prototype和__proto__了😄</div>2020-06-21</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIo6P1BKTjzM5QagaoM99aFmiaTIzpJ7hMG81Hhx9PwCsNjkrpmDPxVHAbQ2MWIKJEYSf5cES9dA7Q/132" width="30px"><span>t86</span> 👍（0） 💬（0）<div>老师的功力真的是深，佩服</div>2020-01-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/11/3d/58ac17a0.jpg" width="30px"><span>水木年华</span> 👍（0） 💬（0）<div>老师讲的真好，有体会有收获😄</div>2020-01-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（0） 💬（0）<div>老师讲得太好了。</div>2019-12-24</li><br/>
</ul>