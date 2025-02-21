在前一篇文章中，我们大致了解了执行上下文是什么，也知道了任何语句的执行都会依赖特定的上下文。

一旦上下文被切换，整个语句的效果可能都会发生改变。那么，切换上下文的时机就显得非常重要了。

在JavaScript，切换上下文最主要的场景是函数调用。在这一课，我们就来讲讲函数调用切换上下文的事情。我们在讲函数调用之前，首先来认识一下函数家族。

## 函数

在ES2018中，函数已经是一个很复杂的体系了，我在这里整理了一下。

**第一种，普通函数：用function关键字定义的函数。**

示例：

```
function foo(){
    // code
}
```

**第二种，箭头函数：用 =&gt; 运算符定义的函数。**

示例:

```
const foo = () => {
    // code
}
```

**第三种，方法：在class中定义的函数。**

示例：

```
class C {
    foo(){
        //code
    }
}
```

**第四种，生成器函数：用function * 定义的函数。**

示例：

```
function* foo(){
    // code
}
```

**第五种，类：用class定义的类，实际上也是函数。**

示例：

```
class Foo {
    constructor(){
        //code
    }
}
```

**第六/七/八种，异步函数：普通函数、箭头函数和生成器函数加上async关键字。**

示例：

```
async function foo(){
    // code
}
const foo = async () => {
    // code
}
async function foo*(){
    // code
}
```

ES6以来，大量加入的新语法极大地方便了我们编程的同时，也增加了很多我们理解的心智负担。要想认识这些函数的执行上下文切换，我们必须要对它们行为上的区别有所了解。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/15/3c/b0/37a7c84d.jpg" width="30px"><span>飞</span> 👍（33） 💬（3）<div>老师，这个例子中的最后一行代码o.showThis(); &#47;&#47; global
好像写错了，应该是C的实例o吧。

class C {
    showThis() {
        console.log(this);
    }
}
var o = new C();
var showThis = o.showThis;

showThis(); &#47;&#47; undefined
o.showThis(); &#47;&#47; global
</div>2019-02-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/76/e9/73ed6cc1.jpg" width="30px"><span>x</span> 👍（5） 💬（1）<div>es6中箭头函数是没有this的吧，所以他不能用作构造函数，他的this取决于外部环境</div>2019-06-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/0b/61/882eb821.jpg" width="30px"><span>奋奋</span> 👍（2） 💬（1）<div>老师我这样对Reference的理解对吗？？？
showThis();               &#47;&#47; Reference中的对象是global
(false || showThis)()   &#47;&#47;  Reference由于运算而被解引用，
                                    然后触发this机制[[thisMode]]私有属性的global取值
</div>2019-10-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/6e/98/44e278ff.jpg" width="30px"><span>dennisleung</span> 👍（0） 💬（1）<div>&gt; 我们可以看到，仅普通函数和类能够跟 new 搭配使用，这倒是给我们省去了不少麻烦。

老师请问这里是省去了什么麻烦呢？</div>2019-08-06</li><br/><li><img src="" width="30px"><span>lsy</span> 👍（0） 💬（1）<div>[[ThisMode]] 是 global （普通函数）的时候，是从哪里取的 this 值呢</div>2019-07-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/77/33/121176bb.jpg" width="30px"><span>东</span> 👍（0） 💬（1）<div>var o = {
     foo: function() {console.log(11111)}
}
new o.foo() &#47;&#47;11111
对象方法用new 调用不会报错呢？</div>2019-07-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/9c/d0/f0dc43c2.jpg" width="30px"><span>咲夜</span> 👍（0） 💬（2）<div>不太能理解为何下面这段代码中 showThis 为 undefined

class C {
    showThis() {
        console.log(this);
    }
}
var o = new C();
var showThis = o.showThis;

showThis(); &#47;&#47; undefined
o.showThis(); &#47;&#47; o</div>2019-06-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/a4/cf/a082eae7.jpg" width="30px"><span>令狐洋葱</span> 👍（0） 💬（1）<div>老师，我想问下 ThisMode 和 ThisBindingStatus 这些只是的获取来源是哪里？是从es标准中查阅的么。</div>2019-06-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/0e/04/d710d928.jpg" width="30px"><span>奥斯特洛夫斯基</span> 👍（110） 💬（23）<div>var a = 1;
foo();

在别处定义了 foo：

var b = 2;
function foo(){
    console.log(b); &#47;&#47; 2
    console.log(a); &#47;&#47; error
}
为什么我执行出来是undefined ，1</div>2019-02-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/b0/1a/7e8ab46e.jpg" width="30px"><span>Geek_gfnho0</span> 👍（89） 💬（2）<div>关于this，Kyle Simpson有四条总结：
1. 由new调用? 绑定到新创建的对象。
2. 由call或者apply(或者bind)调用? 绑定到指定的对象。
3. 由上下文对象调用? 绑定到那个上下文对象。
4. 默认:在严格模式下绑定到undefined，否则绑定到全局对象。
例外：箭头函数不适用以上四条规则，它会继承外层函数调用的 this 绑定(无论 this 绑定到什么)。</div>2019-02-28</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/XSnxM4uP67kdzzCRW8KxhS5jkHiaaSrgkuLh1Z5BxawvQase46pbGAL4Bngmd3eFHckQml6zexyukFoWpeNENTg/132" width="30px"><span>Rushan-Chen</span> 👍（30） 💬（4）<div>老师写的 &quot;在别处定义了foo&quot; 的意思是，这句话上下两部分的代码，不在同一个文件哒~
已经有同学贴了代码，是这样的：
```js
&#47;&#47; 这是 foo.js 文件里的代码
var b = 2;
module.exports = function() { &#47;&#47; 导出function
  console.log(b);
  console.log(a);
};
```
```js
&#47;&#47; 这是test.js 文件里的代码
var foo = require(&quot;.&#47;foo.js&quot;); &#47;&#47; 引入function 为foo
var a = 1;
foo();
&#47;&#47; node 执行 test.js 输出：
&#47;&#47; -&gt; 2
&#47;&#47; -&gt; ReferenceError: a is not defined
```</div>2019-03-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/35/d0/f2ac6d91.jpg" width="30px"><span>阿成</span> 👍（25） 💬（0）<div>这里先说声抱歉，之前可能误导了大家...
这里更新一下答案😅
@Rushan-Chen（虽然你并不能收到，希望极客时间赶紧增加@或者评论的功能，至少也展示个邮箱啊...不然找人都找不到，影响大家交流）
--------------分割线-------------------
文中，winter老师所说的“在别处定义”的意思，应该就是指在另一个模块中定义，即：

在另一个模块中定义...这样引入这个模块时，b就定义且初始化了，而且在这个模块中访问不到变量a...
&#47;&#47; module a.js
import {foo} from &#39;b.js&#39;
var a = 1
foo()

&#47;&#47; module b.js
var b = 2;
export function foo () {
  console.log(b); &#47;&#47; 2
  console.log(a); &#47;&#47; error
}

其实，只要foo访问不到变量a就可以了嘛:
var b = 2;
function foo () {
  console.log(b); &#47;&#47; 2
  console.log(a); &#47;&#47; error
}

void function () {
	var a = 1
	foo()
}()</div>2019-03-16</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/nD10dsXDZ07WyBbqheDtflyxqaR7QsuznhEgtTia0Pticf5fSjQhgSKUUTbibBozY5h2QAD0oYoBCNbvLGpHVeTow/132" width="30px"><span>TY</span> 👍（17） 💬（3）<div>晕得一塌糊涂... 结合上一章的 let var 来看, js 这门语言居然还能火成这样, 世界实在是太奇妙了😥</div>2019-03-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/06/a8/5223644a.jpg" width="30px"><span>Thomas Cho</span> 👍（14） 💬（1）<div>我发现啊，不能只看文中代码结果，还是得自己跑一下，我看了文章后很是疑惑，跑了一下[[Environment]]下方那段代码后，打印出来的是 undefined和1。而不是2和error，不知为何</div>2019-02-28</li><br/><li><img src="" width="30px"><span>DXYF2E</span> 👍（11） 💬（8）<div>觉得没看懂的同学，我觉得可以结合李兵老师的「浏览器工作原理与实践」中的第10、11节课一起阅读，可能理解程度会好一些</div>2019-12-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/e5/2b/47a48b9b.jpg" width="30px"><span>柳林博弈</span> 👍（8） 💬（1）<div>切换上下文
let b = 2;
function foo () {
  console.log(b); &#47;&#47; 2
  console.log(a); &#47;&#47; error
}

{
  let a = 1
  foo()
}</div>2020-04-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7a/fa/abb7bfe3.jpg" width="30px"><span>dingtingli</span> 👍（5） 💬（1）<div>能把复杂的事情讲得清晰明了也是需要天赋的。这门课只感受到了老师的知识面很广，完全无法清晰地理解讲的内容。</div>2020-12-14</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIEODRricvc32UpO3PxoPrFBDgmoGXdiagcibNh0outmZicXFg1icV4c5ibSknc4be3PWUPsIa3OjdMmlwA/132" width="30px"><span>study</span> 👍（5） 💬（0）<div>@奥斯特洛夫斯基
var和function，只是提升声明，代码提升完成是下面的代码：
var a,b;
function foo(){};
a = 1;
foo();
b = 2;
所以a的值为1，b为undefined</div>2019-05-09</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJ26xdibLibk37rdrIA3zStsayOo9b0SGiasibNGfic6n2EIJiba1ptZOtWqV797wkszdjDM8aQkz1A2vibw/132" width="30px"><span>jacklovepdf</span> 👍（4） 💬（0）<div>按照老师的理解，应该少了一种，类的方法也是可以加async的，亲测有效。</div>2019-06-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d7/72/deec1d6b.jpg" width="30px"><span>我五岁了呀</span> 👍（3） 💬（2）<div>没太理解，外层词法环境（outer lexical environment）是指的什么？</div>2020-07-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/06/67/a78a98fe.jpg" width="30px"><span>肉卷</span> 👍（3） 💬（1）<div>var a = 1;
foo();

在别处定义了 foo：

var b = 2;
function foo(){
    console.log(b); &#47;&#47; 2
    console.log(a); &#47;&#47; error
}
这个例子，改成如下例子应该更容易让人理解一些：
var a = 1
  function test() {
    var b = 2

    test1()
  }
  function test1() {
    console.log(2, a, b);
  }
  test()</div>2019-12-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/be/4c/8d19d90a.jpg" width="30px"><span>存</span> 👍（3） 💬（0）<div>var a = 1;
foo();

在别处定义了 foo：

var b = 2;
function foo(){
    console.log(b); &#47;&#47; 2
    console.log(a); &#47;&#47; error
}
为什么我执行出来是2，1</div>2019-03-18</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/pTZS48zWWAhI0zGXrib8s124HSenCS2FTDD0r4SKCqw2ub4adicI4x2wTeH7bHdlsl8QwxeVmzTGs1PIImURxxPg/132" width="30px"><span>itgou</span> 👍（3） 💬（0）<div>var a = 1;
foo();

在别处定义了 foo：

var b = 2;
function foo(){
    console.log(b); &#47;&#47; 2
    console.log(a); &#47;&#47; error
}
这段代码我在chrome上执行出来是undefined,1.
我是写在一个js文件中，然后通过HTML的script引入，不知道老师说的在别处定义是什么意思，是写在两个js文件吗？

如果是两个文件，HTML中引入文件的顺序不同，会有不同的结果，一种报错，一种两个值都正常打印，我都试了的，总之怎么也不会有老师说的那种结果。

请老师看看是不是我哪里理解错了，还是老师写错了</div>2019-03-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/48/3f/3ff67fb2.jpg" width="30px"><span>Geek_376ed4</span> 👍（3） 💬（0）<div>&#47;&#47; foo.js
var b=2;
module.exports = function() {
 console.log(b);&#47;&#47;2
 console.log(a);&#47;&#47;error

};

var foo = require(&quot;.&#47;foo.js&quot;);

var a=1;

foo();

</div>2019-03-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/1a/8c/d91b01a6.jpg" width="30px"><span>zhangbao</span> 👍（3） 💬（1）<div>老师，您好，看完文章后，我有几个问题：

1.  代码段

```
class C {
    showThis() {
        console.log(this);
    }
}
var o = new C();

o.showThis(); &#47;&#47; 这里打印的 this 应该是 o 吗？
```

2. 介绍函数时提到了“方法”，定义是“在 class 中定义的函数”。但是举代码例子时，举了对象方法的例子。方法定义成“作为属性值的函数”，是不是更贴切一点呢？

3. 执行代码段

```
var a = 1;
foo();

&#47;&#47; 在别处定义了 foo：

var b = 2;
function foo(){
    console.log(b); &#47;&#47; 2
    console.log(a); &#47;&#47; error
}
```

后，控制台，打印出的 b 是 undefined，a 是 1。跟老师描述的不一样，是我理解错了吗？

麻烦老师您解答一下，谢谢啦！</div>2019-02-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/29/7b/864f593c.jpg" width="30px"><span>答案</span> 👍（1） 💬（0）<div>奥斯特洛夫斯基的懵</div>2020-10-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/c5/dd/5a482cab.jpg" width="30px"><span>杜森垚</span> 👍（1） 💬（0）<div>  function cutThis()
  {
    var b = 2;
    function foo()
    {
      console.log(b); &#47;&#47; 2
      console.log(a); &#47;&#47; error
    }

    void function()
    {
      var a = 1;
      foo();
    }();
  }</div>2020-08-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/f1/a0/bb40ff4f.jpg" width="30px"><span>呜呼千里快哉风</span> 👍（1） 💬（0）<div>哈哈</div>2020-02-19</li><br/><li><img src="" width="30px"><span>Geek_fc1551</span> 👍（1） 💬（1）<div>winter老师普通函数不是方法吗？</div>2019-11-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/04/92/345d2382.jpg" width="30px"><span>孙郅竣</span> 👍（1） 💬（0）<div>class C {
    showThis() {
        console.log(this);
    }
}
var o = new C();
var showThis = o.showThis;

showThis(); &#47;&#47; undefined
o.showThis(); &#47;&#47; o
&#47;*************************提问***********************************************&#47;
showThis(); &#47;&#47; 输出undefined 是因为这里的this指向全局，但是class为严格模式，所以输出undefined吗</div>2019-10-14</li><br/>
</ul>