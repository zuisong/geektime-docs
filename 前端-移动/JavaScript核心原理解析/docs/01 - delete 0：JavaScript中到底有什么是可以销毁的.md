你好，我是周爱民，感谢你来听我的专栏。

今天是这个系列的第一讲，我将从JavaScript中最不起眼的、使用率最低的一个运算——delete讲起。

你知道，JavaScript是一门面向对象的语言。它很早就支持了delete运算，这是一个元老级的语言特性。但细追究起来，delete其实是从JavaScript 1.2中才开始有的，与它一同出现的，是对象和数组的字面量语法。

有趣的是，JavaScript中最具恶名的typeof运算其实是在1.1版本中提供的，比delete运算其实还要早。这里提及typeof这个声名狼藉的运算符，主要是因为delete的操作与类型的识别其实是相关的。

## 习惯中的“引用”

早期的JavaScript在推广时，仍然采用传统的数据类型的分类方法，也就是说，它宣称自己同时支持值类型和引用类型的数据，并且，所谓值类型中的字符串是按照引用来赋值和传递引用（而不是传递值）的。这些都是当时“开发人员的概念集”中已经有的、容易理解的知识，不需要特别解释。

但是什么是引用类型呢？

在这件事上，JavaScript偷了个懒，它强行定义了“Object和Function就是引用类型”。这样一来，引用类型和值类型就给开发人员讲清楚了，对象和函数呢，也就可以理解了：它们按引用来传递和使用。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/18/6f/10/bfbf81dc.jpg" width="30px"><span>海绵薇薇</span> 👍（108） 💬（12）<div>老师好，我又来了:-)

1.

delete 0

这里的0是一个值（就当前情况），而不是引用是吗？

2.

delete x (x不存在)

返回true

x 表达式返回的应该是一个引用，并且环境中并没有表示这个引用不能被删除，这个理解对吗？

但是文章中有提到delete只能删除属性这一种引用，糊涂了，估计这里的理解还是有问题。

3.

delete null 返回true

delete undefined 返回false 为啥啊？不都是值吗？

4. 还想知道昨天提问的1和2两条是不是漏洞百出啊，就想知道个结果😁。</div>2019-11-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/6f/10/bfbf81dc.jpg" width="30px"><span>海绵薇薇</span> 👍（68） 💬（9）<div>hello 老师好，感谢老师之前的回答：）
突然想到，访问不存在的变量x报ReferenceError错误，其实是对x表达式的的Result引用做getValue的时候报的错误，然后为啥typeof x和delete x不报错，因为这两个操作没有求值。</div>2019-11-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/18/65/35361f02.jpg" width="30px"><span>潇潇雨歇</span> 👍（33） 💬（4）<div>1、如果x根本不存在，delete x什么也不做，返回true
2、如果x只读，delete object.x不能删除掉x属性，返回false；如果在严格模式下，会报错：TypeError: Cannot delete property &#39;c&#39;</div>2019-11-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/18/65/35361f02.jpg" width="30px"><span>潇潇雨歇</span> 👍（25） 💬（7）<div>关于delete的知识，大家可以看下MDN的讲解：https:&#47;&#47;developer.mozilla.org&#47;zh-CN&#47;docs&#47;Web&#47;JavaScript&#47;Reference&#47;Operators&#47;delete
以及这篇深入delete博客：http:&#47;&#47;perfectionkills.com&#47;understanding-delete&#47;</div>2019-11-11</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83ep7yaY0ibpBicMhk0gr01lZrn2Sj9SJU0OdFMWWZbicx1JFVEycKkw3xMoFFs5STPoXhTp823nPtkJjw/132" width="30px"><span>SOneDiGo</span> 👍（21） 💬（1）<div>想问下老师如何理解用delete处理array element实际上在底层是如何操作的?
例如：array = [1,2,&#39;1&#39;]
为什么 delete array[2] 后数组就成了[1,2,undefined&#47;empty]?</div>2019-11-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/6f/10/bfbf81dc.jpg" width="30px"><span>海绵薇薇</span> 👍（20） 💬（3）<div>感谢老师指点😁

ref：语法上的引用

我又看了几遍文章并根据提供的连接，得出如下结论：

1.

var x

x = 0
console.log(x)

x 表达式返回的是一个ref（{referencedName: &#39;x&#39;, base: Environment Record}），然后计算值getValue(ref)得到具体的值，具体的值会分为传统意义上的基本类型和引用类型

2. 衍生出下面的猜想

var obj

obj = {a: 1}

console.log(obj.a)

obj.a 也是一个ref（{referencedName: &#39;a&#39;, base: obj}），然后计算值的时候getValue(ref)得到具体的值1

3. 关于表达式的结果Result的疑问。

文中说：表达式的值，在 ECMAScript 的规范中，称为“引用”。（表达式的结果（Result）是引用。）

但是后文说Result可能是引用&#47;值。

这里的值我不能很好的理解。值指的是另一种引用的格式吗？例如链接文档中提到的base其实有很多种值 undefined, Object, a Boolean, a String, a Symbol, a Number。值指的是{base: 0}这种引用吗？如果不是这样的话base的Boolean等基本值类型有啥用啊？

还是说 0 这个表达式的Result就是0这个值？

期待老师的指点😁</div>2019-11-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/18/65/35361f02.jpg" width="30px"><span>潇潇雨歇</span> 👍（19） 💬（2）<div>看的第三遍。还是要去看看规范加深理解。
如果x根本不存在，delete x操作时，x首先是一个表达式，语义上是一个引用，然后去寻找该引用的result，但是x根本不存在，是找不到的。也就做不了什么，返回ture。
如果obj.x是只读的或者不可配置的，表示他是不能删除的，但是他是实实在在的引用，是可以求值得到Result的，所以返回false。表示不能删除。</div>2019-11-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/cf/14/384258ba.jpg" width="30px"><span>Wiggle Wiggle</span> 👍（16） 💬（1）<div>即便 obj.x 是一个 function，当 obj.x 作为右手端时，也会被 GetValue 方法抽取出值来，而这个“值”并不是直觉上的数字或字符串。这里是有恍然大悟的感觉的，“值”和“引用”应当从严格的规范定义层面理解，而不能从直觉上来理解，只要满足定义，那就是“值”&#47;“引用”。</div>2019-11-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/b9/5e/a8f6f7db.jpg" width="30px"><span>Ming</span> 👍（16） 💬（4）<div>乍一读，云里雾里。翻了文档并做测试，总结如下：

delete 操作符用于删除对象的属性，它接收一个表达式，该表达式应返回对象属性的引用。

1. 如果表达式返回的结果是引用：
当该引用是 let 或 const 定义的，delete 执行结果总是 false；
当引用作为对象的属性不存在时，delete 对象的属性，执行结果为 true，表示未处理；
当该引用为 window 对象的属性且是 var 定义的，delete window 对象的属性，执行结果为 false，表示处理失败（获取属性描述符时为不可配置）；
如果在全局环境下显示定义一个属性描述符为可配置的全局属性，执行 delete，结果是 true，表示操作成功；
当该引用为非 window 对象的属性且是 var 定义的，delete 非 window 对象的属性，执行结果为 true，表示处理成功（获取属性描述符时为可配置）。

2. 如果表达式返回的结果是值，如数字、字符串等，delete 执行结果为 true，表示未处理。</div>2019-11-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/22/d6/9378f4d5.jpg" width="30px"><span>隔夜果酱</span> 👍（14） 💬（1）<div>既然delete这么鸡肋,只能删除对象的成员.
那么后来的版本中为什么不进行改进呢?
比如限定其只能用delete obj.x这种语法格式.
或者加入trycatch,对删除value的操作直接报错呢?</div>2019-11-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/ff/1f/4f927519.jpg" width="30px"><span>渭河</span> 👍（13） 💬（3）<div>这句话要怎么理解呀 
所谓值类型中的字符串是按照引用来赋值和传递引用（而不是传递值）的</div>2019-11-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ee/44/26ac883e.jpg" width="30px"><span>桃翁</span> 👍（12） 💬（3）<div>我突然 明白了 (obj.func=obj.func)()这种方式会丢掉obj里面的this，因为等号右边的obj.func是值，所以得到的仅仅是个函数这个值，而不是引用。 老师我理解得是对的吗？</div>2020-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/2f/1f/f95bd8c9.jpg" width="30px"><span>余文郁</span> 👍（12） 💬（5）<div>老师，JS是基于对象的语言，不是面象对象的语言吧，感觉第二段这有点不妥，虽然ES6增加了class语法，但只是原型的语法糖而已
</div>2019-11-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/2c/b0793828.jpg" width="30px"><span>ssala</span> 👍（10） 💬（2）<div>关于delete，搜集了一些资料，结合代码测试，我目前是这样理解的：delete为一元操作符，其操作数为一个表达式，如果表达式的求值结果是一个值，那么`delete 值`直接返回true，表示该操作没有异常。如果表达式求值结果是一个引用，那么`delete 引用`则会有如下表现，如果引用是可删除的，则直接删除该引用，返回true，否则返回false。

关于属性&#47;property的可删除特性，参照这篇文章：http:&#47;&#47;perfectionkills.com&#47;understanding-delete&#47;

关于引用和值的理解，我用段代码说明，如下：
```
var x = {a: 20}
```
代码中，x是引用，它&quot;指向&quot;执行系统中{a: 20}的一个对象，而{2: 20}则是值，它对应执行系统中内存上的一块区域。x.a是引用，它&quot;指向&quot;执行系统中内存20这个值，而20是值，它也对应执行系统中内存上的一块区域。因此：
```
delete x &#47;&#47; `false` ，x为表达式，求值结果为global.x，且该属性是用var来声明的，其特性是不可删除

delete 20 &#47;&#47; `true`，当执行系统遇到20字面量时，认为其为表达式，对其求值以后得到20这个值，delete 值返回true

delete x.a &#47;&#47; `true` x.a 为引用，且可以删除
```

另外关于delete x，若x不存在，我的解释是：x为表达式，由于未定义，表达式求值结果是未定义的，但是虽然未定义，但求值结果仍然是值，而delete 值就返回true。不知这种解释是否正确？
</div>2019-11-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/b8/79/a4dbe9ee.jpg" width="30px"><span>blueBean</span> 👍（8） 💬（1）<div>表达式的值，在 ECMAScript 的规范中称为“引用”。
ECMAScript 约定：任何表达式计算的结果（Result）要么是一个值，要么是一个引用。
上面这两句话矛盾了吧
</div>2020-02-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/0b/9f/788b964e.jpg" width="30px"><span>仰望星空</span> 👍（7） 💬（1）<div>老师的英语发音delete偏差的有点多</div>2019-11-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/60/12/268826e6.jpg" width="30px"><span>Marvin</span> 👍（6） 💬（1）<div>关于文中delete x的解释，我有一点疑问。
文中是这样说的：
于是，我们现在可以解释，当 x 是全局对象 global 的属性时，所谓delete x其实只需要返回global.x这个引用就可以了。而当它不是全局对象 global 的属性时，那么就需要从当前环境中找到一个名为x的引用。找到这两种不同的引用的过程，称为 ResolveBinding；而这两种不同的x，称为不同环境下绑定的标识符 &#47; 名字。
如果把x解释为引用，而且先寻找global.x，当不是全局属性再寻找当前环境的话：
```
window.apple = 10;
let apple = 10;
delete apple; &#47;&#47; false
```
上面的代码应该先去全局寻找apple引用，那么删除就成功了，应该返回true才对，而不是false。</div>2019-11-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/76/c7/74d54fb5.jpg" width="30px"><span>Mr_Liu</span> 👍（6） 💬（2）<div>思考题1：delete x  x不存在返回的是true
2:  删除会返回false,严格模式会报错
第一遍听感觉有些云里雾里的感觉，又听了一遍加实践。但是有一点不理解或者不知道理解的对不对，希望老师解答一下
问题一：
例如var a = &#39;123&#39;  delete a 返回的是false , 
再次输入a 得到结果依然是 ‘123’，
这是说明delete  没有起作用，其没有起作用的原因是因为 var a = &#39;123&#39; 中的a 是基本数据类型，不是引用类型，所以删除a 元素失败，借此印证了所讲的delete 删除的是表达式或者引用类型的结果。印证这句话的另一个例子是:
var obj = {
   a: &#39;123&#39;
},
var b = obj.a
delete b  返回false , 因为b = obj.a  属于一个赋值语句，b 也是个基本数据类型，所以也不起作用
那么修改成
var obj = {
a: &#39;123&#39;,
b: {
	name: &#39;123&#39;
}
}
var val = obj.b
deletet val 返回的依然是false 后来会读了一下，有这样一句话：delete 其实只能删除一种引用，即对象的成员（Property）
那么 delete x 还有什么存在的意义么。

问题二：
接着我使用delete obj.a   返回的是true ,再次输入 obj.a   返回的就是undefined
但如果我使用
var val = obj.b
delete obj.b  返回的是true
然后打印 obj.b  为undefined;   val 为 {name: &#39;123&#39;}
，那老师的那句delete实际上是删除一个表达式的、引用类型的结果（Result），而不是在删除 x 表达式，或者这个删除表达式的值（Value）。是否可以理解为实际是是删除一直引用呢。</div>2019-11-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/18/11/f1f37801.jpg" width="30px"><span>James</span> 👍（5） 💬（1）<div>老师问你一个问题。
var a = 1
delete(a) &#47;&#47; false
这个为什么返回false啊，我查看不是只读的。
Obect.getOwnPropertyDescriptor(window, &#39;a&#39;)
{
value: 1
writable: true
enumerable: true
configurable: false
}</div>2020-02-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/f5/82/af81ab59.jpg" width="30px"><span>老姚</span> 👍（5） 💬（1）<div>下面从5.1语言规范上找到的，希望能辅助大家理解。内容copy于某个版本的翻译。

一、类型分类

类型分为 ECMAScript 语言类型 与 规范类型 。

 ECMAScript 语言类型 是 ECMAScript 程序员使用 ECMAScript 语言直接操作的值对应的类型。ECMAScript 语言类型包括 未定义 （Undefined）、 空值 （Null）、 布尔值（Boolean）、 字符串 （String）、 数值 （Number）、 对象 （Object）。

 规范类型 是描述 ECMAScript 语言构造与 ECMAScript 语言类型语意的算法所用的元值对应的类型。规范类型包括 引用 、 列表 、 完结 、 属性描述式 、 属性标示 、 词法环境（Lexical Environment）、 环境纪录（Environment Record）。规范类型的值是不一定对应 ECMAScript 实现里任何实体的虚拟对象。规范类型可用来描述 ECMAScript 表式运算的中途结果，但是这些值不能存成对象的变量或是 ECMAScript 语言变量的值。

 在本规范中，我们将「x 的类型」简写为 Type(x) ，而类型指的就是上述的 ECMAScript 语言类型 与 规范类型 。

二、规范类型中的引用类型定义
 引用类型用来说明 delete，typeof，赋值运算符这些运算符的行为。例如，在赋值运算中左边的操作数期望产生一个引用。通过赋值运算符左侧运算子的语法案例分析可以但不能完全解释赋值行为，还有个难点：函数调用允许返回引用。承认这种可能性纯粹是为了宿主对象。本规范没有定义返回引用的内置 ECMAScript 函数，并且也不提供返回引用的用户定义函数。（另一个不使用语法案列分析的原因是，那样将会影响规范的很多地方，冗长并且别扭。）

 一个 引用 (Reference) 是个已解决的命名绑定。一个引用由三部分组成， 基 (base) 值， 引用名称（referenced name） 和布尔值 严格引用 (strict reference) 标志。基值是 undefined, 一个 Object, 一个 Boolean, 一个 String, 一个 Number, 一个 environment record 中的任意一个。基值是 undefined 表示此引用可以不解决一个绑定。引用名称是一个字符串。

 本规范中使用以下抽象操作接近引用的组件：

GetBase(V)。 返回引用值 V 的基值组件。
GetReferencedName(V)。 返回引用值 V 的引用名称组件。
IsStrictReference(V)。 返回引用值 V 的严格引用组件。
HasPrimitiveBase(V)。 如果基值是 Boolean, String, Number，那么返回 true。
IsPropertyReference(V)。 如果基值是个对象或 HasPrimitiveBase(V) 是 true，那么返回 true；否则返回 false。
IsUnresolvableReference(V)。 如果基值是 undefined 那么返回 true，否则返回 false。

三、delete运算符
产生式 UnaryExpression : delete UnaryExpression 按照下面的过程执行 :

1.令 ref 为解释执行 UnaryExpression 的结果。
2.如果 Type(ref) 不是 Reference，返回 true。
3.若 IsUnresolvableReference(ref) 则 , 如果 IsStrictReference(ref) 为 true ，抛出一个 SyntaxError 异常。 否则，返回 true。
4.如果 IsPropertyReference(ref) 为 true 则： 返回以 GetReferencedName(ref) 和 IsStrictReference(ref) 做为参数调用 ToObject(GetBase(ref)) 的 [[Delete]] 内置方法的结果。
5.否则 , ref 是到环境记录项绑定的 Reference，所以： 如果 IsStrictReference(ref) 为 true ，抛出一个 SyntaxError 异常 . 令 bindings 为 GetBase(ref). 返回以 GetReferencedName(ref) 为参数调用绑定的 DeleteBinding 具体方法的结果。

</div>2020-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/78/51/4790e13e.jpg" width="30px"><span>Smallfly</span> 👍（5） 💬（1）<div>在 ECMAScript 规范中，引用的构成至少需要 base value、referenced name、strict reference flag，具体引擎实现应该会把它们封装成一种数据结构来，从而来操作引用。

而文中把 x = x 中的 x 叫做一个引用，应该不是很精确，x 只是引用的 referenced name。

因为我们代码层面无法获取引用，也就没有名字，所以这里用 x 指代规范中的引用。

请问老师这样理解对么？</div>2019-11-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/8d/0e/5e97bbef.jpg" width="30px"><span>半橙汁</span> 👍（5） 💬（1）<div>在《你不知道JavaScript-上》中，看到过关于lhs和rhs的相关介绍，涉及到很多编译，语法解析的知识，真的很难肯...
希望通过对老师专栏的学习，能够更加顺畅地去啃另外的中、下两本😂😂😂</div>2019-11-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/1f/86/3a7eeac4.jpg" width="30px"><span>leslee</span> 👍（4） 💬（1）<div>所谓值类型中的字符串是按照引用来赋值和传递引用（而不是传递值）的

看了一些老师的解释还是有点疑惑， 这句话可以拆成两部分，值类型的字符串是按照引用来赋值的， 与值类型的字符串是按照引用来传递引用的，但是又说这里的引用不是规范类型引用， 那这里的引用如何理解， 因为在代码中字符串的赋值表现，也是抄写。</div>2019-12-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/77/76/68d93fe8.jpg" width="30px"><span>鹿由菌</span> 👍（4） 💬（1）<div>提个不成熟的建议，老师不如先明确解释出规范中的Reference Specification Type，然后再讨论delete相关的问题，不然XXX表达式的Result、“引用”，“值”就太懵逼了。</div>2019-11-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a3/ea/53333dd5.jpg" width="30px"><span>HoSalt</span> 👍（3） 💬（1）<div>老师，我有两个问题想问下
1. 为什么全局作用域下函数的声明无法删除，其也是windows的属性值
2. 全局作用域下声明的函数，调用时其base是否指向windows，在严格模式下全局作用域下的函数内的this指向了undefined</div>2020-05-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e8/f0/b7206e15.jpg" width="30px"><span>张木公</span> 👍（3） 💬（1）<div>由于全局变量实际上是通过全局对象的属性来实现的
这个知识点初学者都知道，但是听老师一说才把这个点和js的对象模型联系起来
请问老师，是不是因为这个知识点所以才有很多人说 js一切皆对象 。
函数作用域中定义的变量是哪个对象的属性
js内存模型是不是不分堆栈了，因为基本类型其实是引用类型的属性</div>2020-03-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ea/0a/f82fa85d.jpg" width="30px"><span>h.g.</span> 👍（3） 💬（1）<div>&gt; var a = 1
undefined
&gt; global.a
1
&gt; delete global.a
false
&gt; global.a
1
&gt; 

咨询一下，为什么，这种挂载全局的变量，无法删除，
这个也满足 delete --&gt; a = object.a 的条件</div>2020-01-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/d3/b2/4a4cc464.jpg" width="30px"><span>蜗牛</span> 👍（3） 💬（1）<div>1、delete x 中，如果 x 根本不存在，会发生什么？
直接返回true，不做任何处理。
x是未声明的变量，会被当成全局对象的属性，且是可以被删除的
严格模式下会报错：Delete of an unqualified identifier in strict mode
2、delete object.x 中，如果 x 是只读的，会发生什么？
返回false，不删除属性x
属性的特性是不可删除(只读)，所以不能被删除
严格模式下会报错：Cannot delete property &#39;x&#39; of object....

他俩最根本的差别在于：属性的特性是否有DontDelete</div>2019-11-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e5/33/ff5c52ad.jpg" width="30px"><span>不负</span> 👍（3） 💬（1）<div>1）“表达式的结果是什么”这一段中表述了&#39; 表达式的值，在 ECMAScript 的规范中，称为“引用” &#39;，之后用到引用是传统理解的引用还是ECMAScript规范中定义的（表达式的值）？
2）这一段后对“引用”这个词很懵逼，如：表达式计算的结果再判断是值还是引用，① 如果此处的“引用”指ECMAScript定义的，就变成了“判断表达式的值是值还是引用”，表达式的值不是值？②在&#39; {} 表示一个字面量的对象，当它被作为表达式执行的时候，结果也是一个值。&#39; 这里的{}计算结果就是{}，{}是一个值？不太理解这个</div>2019-11-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/2c/b0793828.jpg" width="30px"><span>ssala</span> 👍（3） 💬（1）<div>我先不求甚解吧，因为好多概念我不理解，或者以往理解有误，表达式和语句跟我之前的理解都不一样，我一直以为语句可能不产生值。

感谢老师如此较真地探讨这些问题，期待后续更新。</div>2019-11-12</li><br/>
</ul>