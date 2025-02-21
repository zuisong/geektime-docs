你好，我是周爱民。

如果你听过上一讲的内容，心里应该会有一个问题，那就是——在规范中存在的“引用”到底有什么用？它对我们的编程有什么实际的影响呢？

当然，除了已经提及过的`delete 0`和`obj.x`之外，在今后的课程中，我还会与你讨论这个“引用”的其它应用场景。而今天的内容，就从标题来看，若是我要说与这个“引用”有关，你说不定得跳起来说我无知；但若说是跟“引用”无关的话呢，我觉得又不能把标题中的这一行代码解释清楚。

为什么这行代码看起来与规范类型中的“引用”无关呢？因为这行代码出现的时候，连ECMAScript这个规范都不存在。

我大概是在JavaScript 1.2左右的时代就接触到这门语言，在我写的最早的一些代码中就使用过它，并且——没错，你一定知道的：它能执行！

有很多的原因会促使你在JavaScript写出表达式连等这样的代码。从C/C++走过来的程序员对这样的一行代码是不会陌生的。它能用，而且结果也与你的预期会一致，例如：

```
var x = y = 100;
console.log(x); // 100
console.log(y); // 100
```

它既没错、又好用，还很酷，你说我们为什么不用它呢？然而很不幸，这行代码可能是JavaScript中最复杂和最容易错用的表达式了。

所以今天我要和你一起好好地盘盘它。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/c8/d3/3020ae46.jpg" width="30px"><span>fatme</span> 👍（100） 💬（1）<div>声明和语句的区别在于发生的时间点不同，声明发生在编译期，语句发生在运行期。声明发生在编译期，由编译器为所声明的变量在相应的变量表，增加一个名字。语句是要在运行时执行的程序代码。因此，如果声明不带初始化，那么可以完全由编译器完成，不会产生运行时执行的代码。</div>2019-11-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/6f/10/bfbf81dc.jpg" width="30px"><span>海绵薇薇</span> 👍（22） 💬（3）<div>hello，老师好啊，研读完文章和评论后还存在如下疑问：

1.

var y = &quot;outer&quot;;

function f() { 

	console.log(y); &#47;&#47; undefined 

	console.log(x); &#47;&#47; throw a Exception 

	let x = 100; 

	var y = 100; 

	...

}

老师解释函数内部读取不到外部变量的原因是“函数创建的时候标识符x和y就被创建了”。因为这是一个函数声明，也就是在编译的时候就创建了。

高程上的意思是函数执行的时候会生成一个活动对象当做变量对象，这时候标识符才会生成，包括arguments，形参实参，声明的变量，挂在活动对象上。

两个解释好像都能说明上面的现象。

有点糊涂了。

2.

function a() {

	function b() {}

}

在代码执行前连函数b都被创建了吗？

3. 老师对一定了解闭包的本质，后面有机会说到吗？
</div>2019-11-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/b9/5e/a8f6f7db.jpg" width="30px"><span>Ming</span> 👍（20） 💬（2）<div>〈以下是小生愚见〉
概念纷繁，建议老师将讲解重心放到这门语言的现有特性，贯之历史脉络，是否（怎样）解决了某种设计缺陷。这样，知识纵深感更强，并可指导实际工作以避免踩坑。适当穿插示例代码和图文更佳。</div>2019-11-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/e5/aa/57926594.jpg" width="30px"><span>Ppei</span> 👍（18） 💬（2）<div>老师你好，词法声明会有提升吗？
一些书里面会说不存在变量提升，但是文中说，是拒绝访问。
我是不是该从编译期跟运行期去理解？</div>2020-05-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/76/c7/74d54fb5.jpg" width="30px"><span>Mr_Liu</span> 👍（13） 💬（1）<div>思考题: 小白的我，没有太明确的答案，暂时还不能明确自己理解究竟是否正确，希望听老师后续的课程能够明白

读完今天的这篇理解了昨天的提问，为什么var x = &#39;123&#39;   delete x  是false, 
即使是
var obj ={
 a: &#39;123&#39;,
 b: {
   name: &#39;123&#39;
  }
} 
var z = obj.b
delete z 返回也是false
所以问了那么delete x 存在有什么意义。
今天老师的科解答了
x = &#39;123&#39;
delete x 返回true 
是因为你可以删除掉这个动态添加的“变量”，因为本质上就是在删除全局对象的属性。同时也理解了上一讲的“只有在delete x等值于delete obj.x时 delete 才会有执行意义。例如with (obj) ...语句中的 delete x，以及全局属性 global.x。”这句
但上一节关于“delete x”归根到底，是在删除一个表达式的、引用类型的结果（Result），而不是在删除 x 表达式，或者这个删除表达式的值（Value）。后一句理解了，但前一句是否可以理解为实际上是删除引用呢，希望老师解答一下
立一个flag ，每个争取评论下面都有我的，不为别的，就为增加自己的思考</div>2019-11-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/89/5b/d8f78c1e.jpg" width="30px"><span>孜孜</span> 👍（10） 💬（2）<div>今天写IIFE,突然有点问题想问下老师，
1. 为什么(function f(){ return this}) 可以，(var test=1) 不可以。
2. 两种IIFE的写法，(function f(){ return this})() 和 (function f(){ return this}()) 有何区别。
3. 函数调用（）和表达式取值（）如何在ECMAScript找到说明？</div>2020-07-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f2/4f/59bd4141.jpg" width="30px"><span>Isaac</span> 👍（10） 💬（1）<div>「一个赋值表达式操作本身也是有“结果（Result）”，它是右操作数的值。注意，这里是“值”而非“引用”」
老师，你好，这句话从“值类型”的角度可以理解，但是对于引用类型怎么理解？
比如：var x = y = { name: &#39;jack ma&#39; }。

我的理解：
由于 { name: &#39;jack ma&#39; } 本身是引用类型，所以 y = { name: &#39;jack ma&#39; } 的赋值操作的结果也是“一个引用”，所以这里的“值”其实和类型无关，仅仅是一个运算结果。

在回到这句话：「它是右操作数的值」 ，用更通俗易懂话来讲，这里的“值”仅仅是一个运算结果，和类型无关。

请问老师我这样理解正确吗？如果错误的话，该怎么解释 var x = y = { name: &#39;jack ma&#39; }？</div>2020-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d4/37/528a43e7.jpg" width="30px"><span>Elmer</span> 👍（10） 💬（1）<div>文中提到：ECMAScript 规定在这个全局对象之外再维护一个变量名列表（varNames）
那么window是怎么取到这些变量的值的，如window.a
不是平级么。在global scope中, window var let const 的关系是什么。
求讲解</div>2019-12-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/9e/bf/439c9afb.jpg" width="30px"><span>Zheng</span> 👍（9） 💬（1）<div>老师，我用node执行这段代码，结果是undefined，但是换成浏览器打印就可以打印出来a的配置信息，这是因为node环境和浏览器的差异还是什么，我试过好多次了，应该不是偶然:

var a = 100;
x = 200;
console.log(Object.getOwnPropertyDescriptor(global,&quot;a&quot;)); &#47;&#47;浏览器执行的时候global改为globalThis</div>2020-01-14</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/yicicolgdxU2vTP6ExtAf6NicvFicuAfM0tL7bOoPDMZa0bYVa8wkV10DgnpobHX9blmIicdL6zFS76Dq40Rm8xt21g/132" width="30px"><span>Geek_baa4ad</span> 👍（8） 💬（1）<div>var x = y = 100;
Object.getOwnPropertyDescriptor(global, &#39;x&#39;);
Object.getOwnPropertyDescriptor(global, &#39;y&#39;);
{value: 100, writable: true, enumerable: true, configurable: false}configurable: falseenumerable: truevalue: 100writable: true__proto__: Object
Object.getOwnPropertyDescriptor(global, &#39;x&#39;);
{value: 100, writable: true, enumerable: true, configurable: false}
Object.getOwnPropertyDescriptor(global, &#39;y&#39;);
{value: 100, writable: true, enumerable: true, configurable: false}

得到结果一样吖，x y 是一个相同的东西吧 最新的v8 实现不一样啦？</div>2020-05-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/32/3a/ead5611e.jpg" width="30px"><span>陆昱嘉</span> 👍（8） 💬（1）<div>老师，一个赋值表达式的左边和右边其实“都是”表达式，那么var x=(var y=100);这样就报错，原因是什么？varNames里面的冲突？</div>2019-11-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/43/f1/3c69eb09.jpg" width="30px"><span>佳民</span> 👍（7） 💬（2）<div>思考题：var声明会声明提升，在语法解析（静态分析）阶段进行，不是在运行阶段执行，这样理解对吗？</div>2019-11-13</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/3lp20weUpmEjiaLAS6umkKRGB7WicIPGWQ7sjRsxbw0EAiapnslID17FfmrMFppSDw7vn0A8bu1icBBmPXGGweGhjQ/132" width="30px"><span>G</span> 👍（6） 💬（3）<div>老师您好，在回过头来重新读这个课程的时候，我产生了一些新的疑惑。
在静态语法解析阶段，会在词法环境中添加所声明的标识符，那么像下面这样的代码：
var arr = new Array;
for (var i=0; i&lt;5; i++) arr.push(function f() {
  &#47;&#47; ...
});
这段代码是在第八讲中粘贴过来的，第八讲中有说，静态函数f（）有且仅有一个。那么这个函数f是什么时候被定义的，又被定义在了什么样的词法环境下呢？
我上面的表述可能不明确，我大概就是想问这么一个问题：
let obj = {
      test:function(cb){
        cb();
        (()=&gt;{console.log(this);})()
      }
    }
    obj.test(() =&gt; {console.log(this);})


() =&gt; {console.log(this) 这个箭头函数，是在什么时候被定义的，定义在了哪里。
从 cb执行 this打印来看，应该是定义在了全局环境下。
但是由于它是一个匿名函数，所以我在全局无法打印出它来验证。但是我把
() =&gt; {console.log(this)换成function f() {console.log(this)},全局下也没有办法访问到 f 。

我描述的可能不太清楚，我大概是想知道，被当做实参传入的函数，是在什么时候被声明的，声明在了哪里。  


</div>2020-10-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ba/bd/6f2f078c.jpg" width="30px"><span>Marvin</span> 👍（6） 💬（1）<div>相当于
var&#47;let&#47;const x = (y =100)
再拆就是
y=100 &#47;&#47; 变量泄漏
var x=y &#47;&#47; 模拟表达式返回值赋值
</div>2019-11-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/94/82/d0a417ba.jpg" width="30px"><span>蓝配鸡</span> 👍（6） 💬（2）<div>醍醐灌顶，但是有一些疑问：
文中说，
&quot;如果是在一门其它的（例如编译型的）语言中，“为变量 x 绑定一个初值”就可能实现为“在创建环境时将变量 x 指向一个特定的初始值”。这通常是静态语言的处理方法，然而，如前面说过的，JavaScript 是门动态的语言，所以它的“绑定初值”的行为是通过动态的执行过程来实现的，也就是赋值操作。&quot;

为什么动态语言就不可以给变量初始化， 一定要使用动态赋值呢？
我对动态语言的理解是，变量的类型可以在运行时改变，静态语言变量的类型不可以改变。 但是这性质好像并不影响初始化？</div>2019-11-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/10/30/c07d419c.jpg" width="30px"><span>卡尔</span> 👍（5） 💬（2）<div>老师，你说let声明的变量不能在赋值之前使用。
这里说的赋值是不是说赋值操作呢？
let a;
console.log(a)
上面代码对a是没有赋值操作吧？</div>2020-06-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/78/51/4790e13e.jpg" width="30px"><span>Smallfly</span> 👍（5） 💬（1）<div>y = 100 有的地方叫赋值语句，有的地方叫赋值表达式。因为它的执行结构能在代码层面获得 x = (y = 10)，所以我更倾向于认为它是表达式。

想请问下老师叫赋值语句是错误的么，还是有其它的原因？</div>2020-02-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/96/78/114b03c7.jpg" width="30px"><span>家家家家</span> 👍（5） 💬（2）<div>忘了在哪本书中还是哪篇文章中讲过，变量的生命周期：声明阶段、初始化阶段、赋值阶段。
老师这里讲的静态分析阶段就是指的变量生命周期中的声明阶段对吗？
对于var，它的声明阶段和初始化阶段是一起发生的，都在静态分析中；对于let，它的声明阶段和初始化阶段是分开的，只有声明阶段在静态分析中，是这样理解的嘛？</div>2019-12-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/2c/b0793828.jpg" width="30px"><span>ssala</span> 👍（5） 💬（1）<div>老师，像变量提升这种不符合直觉的设计，难道规范不能将其移除吗？不移除是为了兼容老代码吗？我想应该没有代码会依赖这个特性吧？</div>2019-11-13</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqW6sdNZ1OF8n5Wsfr7Vr8sBY4vOD8iaj31icqPgyk8NdALibhzKXwdIDmoMJfJznWf8b0NGjcGWKRNg/132" width="30px"><span>Geek__kkkkkkkk</span> 👍（5） 💬（2）<div>老师，您文章中讲到“ECMAScript 规定在这个全局对象之外再维护一个变量名列表（varNames），所有在静态语法分析期或在 eval() 中使用var声明的变量名就被放在这个列表中。然后约定，这个变量名列表中的变量是“直接声明的变量”，不能使用delete删除。”，这里面的意思我理解了 eval() 中使用var声明的变量名，不可用delete删除，但是下面的代码中eval()声明了b,configurable是true,可删除，是否矛盾了？还是我理解的不够全面？</div>2019-11-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/82/a4/a92c6eca.jpg" width="30px"><span>墨灵</span> 👍（4） 💬（1）<div>以前我把
```
console.log(x);
var x = 100;
```
理解成
```
var x;
console.log(x);
x = 100;
```
看来以前的理解是有误的，是更为底层的东西在起作用。</div>2020-03-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/37/e1/0953c506.jpg" width="30px"><span>授人以摸鱼</span> 👍（4） 💬（2）<div>发现我好像对全局作用域的理解有一些偏差：
var，或者没有声明直接赋值，这样的创建标识符（引用）是作为global对象的字段存在的，可以用Object.getOwnPropertyDescriptor从global上读到。
全局作用域里用let，const创建的变量，虽然也是全局可见，但它并没有创建在global上，而是创建在了另一个地方。从作用域链的视角来看的话，这个作用域要比global低一级这样子。</div>2019-11-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/78/51/4790e13e.jpg" width="30px"><span>Smallfly</span> 👍（4） 💬（1）<div>老师文中说变量声明分为两步，静态分析和动态绑定，JS 是在进入每个作用域后，执行前进行词法分析的么？</div>2019-11-13</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/3fB603VY46iaYS2h2MibvV4H5iamibPMr6AT4Fiac5snKOiaMI180pb2DVCe5Bd2sNSJibZSwQg8Qo1PD7bVw1uVBx7YA/132" width="30px"><span>埋坑专家</span> 👍（3） 💬（1）<div>想请问一下老师：

var 声明的变量，configurable为false，这个值是因为varNames不给删除，所以才这样设置的吗？

但我从老师回答其他同学的答案里，得知varNames不限制删除，只是var 声明的变量，configurable为false，导致出现varNames里的变量不给删除这种现象。

那么这两者是否有因果关系呢？

谁是因，谁是果？

或者是否有第三方的原因导致其一是这样，从而影响到另一方了呢？

谢谢老师！</div>2020-07-01</li><br/><li><img src="" width="30px"><span>阳少宇</span> 👍（3） 💬（2）<div>老师你好,对于let声明一个变量说是有个编译期且不会初始化.
那么 let a; console.log(a) 得到的结果是undefined, 那这个undefined是从哪里来的呢?</div>2020-05-11</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLTYpERVj4wtwAwqz4SUiaoQXDIyhYaKjABMvkJbVXaI3kcJterXovCTqZZSQ1TnueIWX7VGvC3koA/132" width="30px"><span>麦田里的守望者</span> 👍（3） 💬（1）<div>为了兼容旧的 JavaScript 语言设计，现在的 JavaScript 环境仍然是通过将全局对象初始化为这样的一个全局闭包来实现的。但是为了得到一个“尽可能”与其它变量环境相似的声明效果（varDecls），ECMAScript 规定在这个全局对象之外再维护一个变量名列表（varNames），所有在静态语法分析期或在 eval() 中使用var声明的变量名就被放在这个列表中。然后约定，这个变量名列表中的变量是“直接声明的变量”，不能使用delete删除。
这段话的最后几句，是不是写错了</div>2019-12-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/a3/45/8e9c6a69.jpg" width="30px"><span>因为有你心存感激</span> 👍（3） 💬（1）<div>var x = y =100  中的y 是可以通过delete y 删除，老师又说 delete 只删除引用不删除值，在这里y是引用吗？还有对于 js 为什不能  变量名 = 值  这样赋值呢？</div>2019-11-27</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLZXUUB3zpdQOENbBmqgPgjPdXmAomUwLISaKfQ9eFkwv0rsCdaibHapVd7dmBnvplxKbBPaz0IRTQ/132" width="30px"><span>Geek_8cn3qp</span> 👍（3） 💬（1）<div>为什么eval里var的变量可以删除？还是没明白</div>2019-11-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ee/00/3cca3642.jpg" width="30px"><span>Makus</span> 👍（3） 💬（1）<div>附「语句和声明」的链接：https:&#47;&#47;developer.mozilla.org&#47;zh-CN&#47;docs&#47;Web&#47;JavaScript&#47;Reference&#47;Statements
严格意义上来说，除了本篇中出现的六种和链接中的五大类都不能算作语句吧。
例如 ：标题中的 y = 100
麻烦老师指正一下，不太懂</div>2019-11-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e6/a9/b459efb7.jpg" width="30px"><span>如故</span> 👍（2） 💬（1）<div>老师您好
var a = 1;
b = 2;
a和b都是全局对象上的一个属性，但a存在于一个varNames列表中，并且是不可配置的。
那么为啥要设置这样一个varNames列表呢？文中说：是为了得到一个“尽可能”与其它变量环境相似的声明效果（varDecls）。这句话不太理解</div>2021-02-24</li><br/>
</ul>