你好，我是winter。

在前面的课程中，我已经讲解了JavaScript对象的一些基础知识。但是，我们所讲解的对象，只是特定的一部分，并不能涵盖全部的JavaScript对象。

比如说，我们不论怎样编写代码，都没法绕开Array，实现一个跟原生的数组行为一模一样的对象，这是由于原生数组的底层实现了一个自动随着下标变化的length属性。

并且，在浏览器环境中，我们也无法单纯依靠JavaScript代码实现div对象，只能靠document.createElement来创建。这也说明了JavaScript的对象机制并非简单的属性集合+原型。

我们日常工作中，接触到的主要API，几乎都是由今天所讲解的这些对象提供的。理解这些对象的性质，我们才能真正理解我们使用的API的一些特性。

## JavaScript中的对象分类

我们可以把对象分成几类。

- 宿主对象（host Objects）：由JavaScript宿主环境提供的对象，它们的行为完全由宿主环境决定。
- 内置对象（Built-in Objects）：由JavaScript语言提供的对象。
  
  - 固有对象（Intrinsic Objects ）：由标准规定，随着JavaScript运行时创建而自动创建的对象实例。
  - 原生对象（Native Objects）：可以由用户通过Array、RegExp等内置构造器或者特殊语法创建的对象。
  - 普通对象（Ordinary Objects）：由{}语法、Object构造器或者class关键字定义类创建的对象，它能够被原型继承。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/13/84/5aeaea9c.jpg" width="30px"><span>XXX</span> 👍（8） 💬（2）<div>关于原生构造器无法用 class&#47;extend 语法来继承的观点，能否举例说明呢？我写个demo跑了一下，发现还是可以的呐

</div>2019-02-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/d2/78/1f1b45f9.jpg" width="30px"><span>Jaykey</span> 👍（3） 💬（3）<div>打印出来了989个对象，有很多是没有用过的，区分清楚了内置对象的差距，也知道了平时使用的一些方法是“构造器”</div>2019-06-13</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/3XbCueYYVWTiclv8T5tFpwiblOxLphvSZxL4ujMdqVMibZnOiaFK2C5nKRGv407iaAsrI0CDICYVQJtiaITzkjfjbvrQ/132" width="30px"><span>有铭</span> 👍（1） 💬（2）<div>这个“原型继承方法”不能正常工作，是什么意思？我放狗搜了一下，发现，Number对象仍然可以用prototype属性来添加方法和属性啊</div>2019-02-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/ea/d3/42566a75.jpg" width="30px"><span>LaMer</span> 👍（0） 💬（1）<div>这些构造器创建的对象多数使用了私有字段, 例如：Error: [[ErrorData]]。  [[ErrorData]]指的是什么  不明白 可以说的清楚一些吗  望老师回答下</div>2019-10-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/4e/a4/433305bb.jpg" width="30px"><span>卡洛斯(๑Ő௰Ő๑)</span> 👍（0） 💬（1）<div>winter 你好，
对于用户使用 function 语法或者 Function 构造器创建的对象来说，[[call]] 和 [[construct]] 行为总是相似的，它们执行同一段代码。

function f(){
 return 1;
}
&#47;&#47; 把 f 作为函数调用
var v = f(); &#47;&#47; 1
&#47;&#47; 把 f 作为构造器调用
var o = new f(); &#47;&#47; {}


代码执行的结果是不同，函数调用返回的是 1，构造器调用返回的一个对象。
这里的行为是指什么呢，为什么又总是相似的呢。
相似是指 函数调用和构造器调用，都能被调用？还是指都调用的同一个代码？</div>2019-08-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9e/fa/8d206a46.jpg" width="30px"><span>丁丁丁丁丁大树。</span> 👍（0） 💬（1）<div>winter老师你好，我对08节的内容有一个疑问，老师有空的话请为学生解惑
文中你有一句话“构造器对象的定义是：具有私有字段 [[construct]]”
我的理解是带有constructor的对象就是构造器对象，所以我做了下面这个实验
var obj = {constructor:function(){return {say:function(){alert(&#39;hello&#39;)}}}}
var ins = new obj() 
但是会报错obj不是一个construct，
我想问老师是不是我理解错了？
</div>2019-02-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/05/b8/35d8e0e2.jpg" width="30px"><span>Miss</span> 👍（0） 💬（1）<div>在讲到函数对象和构造器对象时[[call]]和[[construct]] 指的是？</div>2019-02-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ac/17/92b5114f.jpg" width="30px"><span>大雄</span> 👍（0） 💬（1）<div>proxy模拟array怎样？</div>2019-02-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/43/da/0702102a.jpg" width="30px"><span>九</span> 👍（0） 💬（2）<div>当然了，用户用 function 关键字创建的函数必定同时是函数和构造器。不过，它们表现出来的行为效果却并不相同。

对于用户使用 function 语法或者 Function 构造器创建的对象来说，[[call]] 和 [[construct]] 行为总是相似的，它们执行同一段代码。

请问这里的意思是，call 和 construct 它们虽然执行同一段代码，但是行为效果是不同的？感觉读起来似乎有歧义……
</div>2019-02-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f1/15/8fcf8038.jpg" width="30px"><span>William</span> 👍（215） 💬（3）<div>&#47;&#47; 1. 利用字面量
var a = [], b = {}, c = &#47;abc&#47;g
&#47;&#47; 2. 利用dom api
var d = document.createElement(&#39;p&#39;)
&#47;&#47; 3. 利用JavaScript内置对象的api
var e = Object.create(null)
var f = Object.assign({k1:3, k2:8}, {k3: 9})
var g = JSON.parse(&#39;{}&#39;)
&#47;&#47; 4.利用装箱转换
var h = Object(undefined), i = Object(null), k = Object(1), l = Object(&#39;abc&#39;), m = Object(true)</div>2019-02-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/ce/f8/40e72791.jpg" width="30px"><span>多啦斯基周</span> 👍（129） 💬（2）<div>这块的内容确实有些复杂，作者讲的很深入。
但是个人觉得思路是否可以再整理一下，总是感觉有一些绕，把知识讲得更易理解一些呢？</div>2019-02-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e4/60/a011a649.jpg" width="30px"><span>Alan</span> 👍（69） 💬（1）<div>一期比一期深入，一期比一期了解的更少了，蓝瘦</div>2019-02-02</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJy3VhrhNLDDzCjbqs0EAN5lp4svORB4ELRwQJbkOaCAUV3ic38OUIu1OoibwuyMicKhQowZGwSImvjA/132" width="30px"><span>kesikesie</span> 👍（30） 💬（5）<div>    console.log(new Date); &#47;&#47; 1
    console.log(Date())
这个在控制台打印的都是日期</div>2019-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/f6/3d/7ec71bc4.jpg" width="30px"><span>吃不饱</span> 👍（29） 💬（2）<div>前端工作一年，好难理解。</div>2019-02-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/39/30/f7df6ba7.jpg" width="30px"><span>米斯特菠萝</span> 👍（23） 💬（7）<div>利用构造器的执行规则来实现私有，真是个意外的发现

之前用class构建一个类，有一些方法暴露给外面总觉得怪怪的。现在好了，在constructor函数里return一个对象，在对象里写方法来对应返回类里写的需要暴露的method就解决了</div>2019-02-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/b1/58/7d4f968f.jpg" width="30px"><span>plasmatium</span> 👍（16） 💬（3）<div>try {
  Image()
) catch (err) {
  &#47;&#47; 获得一个对象err
}</div>2019-02-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/1f/ec/dede5cb2.jpg" width="30px"><span>clannad-</span> 👍（15） 💬（0）<div>1.var o = [];
2.document.createElement(&#39;div&#39;)；
3.Object.create(Object.prototype);
4.var o = Object.assign({});
5.var o = JSON.parse(&#39;{}&#39;);</div>2019-02-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/93/4a/de82f373.jpg" width="30px"><span>AICC</span> 👍（15） 💬（1）<div>不那么规律不那么优雅看得云里雾里</div>2019-02-02</li><br/><li><img src="" width="30px"><span>Geek_1d054d</span> 👍（12） 💬（3）<div>老师提到原生构造器无法继承。
而阮一峰老师在http:&#47;&#47;es6.ruanyifeng.com&#47;#docs&#47;class-extends中表示，es6已经可以继承原生构造函数，并且能定义子类。
以我的理解来看，阮一峰老师的说法没有问题。
不知道老师怎么看？</div>2019-05-19</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/s0bx4WXQNkAJ3c3map0g6dlt3sKDgTtN7Ria96YoufjQcVVI8Shv5CN1jnK1ZTImNnlPcibRqvyiaUuhpIvV1TpnQ/132" width="30px"><span>wingsico</span> 👍（11） 💬（0）<div>JS中对象的分类一般分为宿主对象和内置对象，宿主对象就是由js运行的环境提供的对象，它的行为由环境控制，例如浏览器中的Window，Node中的global等，而内置对象可以再次细分，分为固有对象、原生对象和普通对象，这些对象可以隶属于多种对象，例如Array 即是固有对象，也是原生对象，固有对象是由环境或者宿主提供的，这里的对象并不但只类似{}这样的对象，函数也是对象。固有对象包含了所有的原生对象的创造者，例如 var array = new Array(), 其中 array 是原生对象，而Array是其创造者，属于固有对象。这些固有对象往往包含两个特殊的私有属性 [[call]] 和 [[construct]]，拥有 [[call]] 的对象可以作为函数进行调用，拥有 [[construct]] 的可以作为构造器被new调用。这两个属性是由js引擎写入，通过上层js代码是无法进行赋值或修改的。对于一些对象的特殊行为，一般都是由js引擎完成的，但通过一些上层js代码模拟，也可以模拟出类似操作。</div>2020-04-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/94/56/4b8395f6.jpg" width="30px"><span>CC</span> 👍（10） 💬（1）<div>除了老师提到的：
var o = {}
var o = function(){}

还有：

&#47;&#47; 使用 Object 构造器
var o = new Object();

&#47;&#47; 使用 function
var o = new function f() {};

&#47;&#47; 使用 method
var o = Object.create(null)

&#47;&#47; 使用 ES6 class
class myOwnObject {
  constructor(a) { this.a = a; }
}
var o = new myOwnObject(‘hey yo’);

暂时想到这些。
</div>2019-02-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/2d/5f/f648ec62.jpg" width="30px"><span>覃</span> 👍（9） 💬（0）<div>老师好，看完文章后有两个小疑问
1.Js的30多个构造器是怎么实现的？ 
2.div对象虽然属性很多。那可以用纯js模拟吗？使用document.createElement的时候，浏览器还做了什么别的工作吗？</div>2019-02-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8c/2d/78e39300.jpg" width="30px"><span>Evo</span> 👍（6） 💬（0）<div>&quot;用对象来模拟函数与构造器：函数对象与构造器对象&quot; 最后一段：“如果我们的构造器返回来一个新的对象，那么new创建的新对象就变成了一个构造函数之外完全无法访问的对象”， 明明是“构造器中的某些属性可以被写成构造函数之外完全无法访问的属性”。</div>2019-02-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a4/45/3cb5cdc6.jpg" width="30px"><span>拾迹</span> 👍（5） 💬（0）<div>1、使用 Object 构造函数
var person1 = new Object();
2、使用对象字面量
var person1 = {}
3、工厂模式
function createPerson(name, age, job){
    var o = new Object();
    o.name = name;
    o.age = age;
    o.job = job;
    o.sayName = function(){
        alert(this.name);
    }
    return o;
}
var person1 = createPerson(&#39;zs&#39;, 18, &#39;programmer&#39;);
var person2 = createPerson(&#39;ls&#39;, 28, &#39;teacter&#39;);
4、构造函数
function Person(){...}
var p = new Person()
5、原型模式
function Person(){...}
Person.prototype.x = ...
var p = new Person()
6、Object.create()</div>2019-02-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/43/9b/ce86894a.jpg" width="30px"><span>Nirvana</span> 👍（5） 💬（0）<div>我发现老师很稀罕猫啊，都是猫的配图</div>2019-02-03</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/cviaNUiaiaMq9eicjZTupibehtBk1sY9NKWuIsYjB5514Sj1IV3oKIhjicerlnl2FFicW1BEUUqHU1qn0lRdq8bWOzyag/132" width="30px"><span>Geek_657e73</span> 👍（4） 💬（0）<div>不要为了 去凑 而凑好吧，我看了下面的创造对象的方法，瑟瑟发抖，你们比官方还专业，去项目中那么写试试，第二天就被开除，自以为很高大上，其实就是在给被人制造麻烦，现有的都不会更搞不懂，老师说实话 目前看了前几节，感觉该需要去解释说明的，一掠而过，让人感觉很遥远很模糊</div>2021-06-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/3b/68/a409de4b.jpg" width="30px"><span>Chen</span> 👍（4） 💬（3）<div>老师你说的那个console.log(new Date)和console.log(Date())在控制台全部输出时间字符串，咋回事</div>2019-03-20</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/dGa4C9GU5rcZYK2ibfSFh9J2bQ2IgLibGWdZH1ORESCKDCWdHiaMqicNawibqoWErBDyU8jVB68dUxbN8MM53BVqofA/132" width="30px"><span>Geek_hx</span> 👍（3） 💬（0）<div>读此篇后，觉得我还是先去重学JavaScript吧</div>2019-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/29/41/18d5e211.jpg" width="30px"><span>路人</span> 👍（3） 💬（1）<div>本文 -用对象来模拟函数与构造器：函数对象与构造器对象- 结尾处，这样写道：
「如果 [[call]] 的返回值是对象，那么，返回这个对象，否则返回第一步创建的新对象。」

在《Javascript高级程序设计》——第6章 面对对象的程序设计 p160-p161的寄生构造函数模式有类似讲解：
「构造函数在不返回值的情况下，默认会返回新对象实例。而通过在构造函数的末尾添加一个 return 语句，可以重写调用构造函数时返回的值。 」</div>2019-03-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/01/09/a35710f0.jpg" width="30px"><span>啊咩</span> 👍（3） 💬（0）<div>原生对象语法用extends继承，可以举一个具体的例子嘛？我试了下继承Array是可以的呀</div>2019-02-05</li><br/>
</ul>