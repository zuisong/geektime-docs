你好，我是周爱民，欢迎回到我的专栏。

今天我要讲述的内容是从ECMAScript 6开始在JavaScript中出现的**模块技术**，这对许多JavaScript开发者来说都是比较陌生的。

一方面在于它出现得较晚，另一方面，则是因为在普遍使用的Node.js环境带有自己内置的模块加载技术。因此，ECMAScript 6模块需要通过特定的命令行参数才能开启，它的应用一直以来也就不够广泛。

导致这种现象的根本原因在于**ECMAScript 6模块是静态装配的**，而传统的Node.js模块却是动态加载的。因而两种模块的实现效果与处理逻辑都大相径庭，Node.js无法在短期内提供有效的手段帮助开发者将既有代码迁移到新的模块规范下。

总结起来，确实是这些更为现实的原因阻碍了ECMAScript 6模块技术的推广，而非是ECMAScript 6模块是否成熟，或者设计得好与不好。

不过即使如此，ECMAScript 6模块仍然在JavaScript的一些大型应用库、包，或者对新规范更友好的项目中得到了不错的运用和不俗的反响，尤其是在使用转译器（例如Babel）的项目中，开发者通常是首选ECMAScript 6模块语法的。

因此ECMAScript 6模块也有着非常好的应用环境与前景。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/04/8d/005c2ff3.jpg" width="30px"><span>weineel</span> 👍（51） 💬（1）<div>ESModule 根据 import 构建依赖树，所以在代码运行前名字就是已经存在于上下文，然后在运行模块最顶层代码，给名字绑定值，就出现了‘变量提升’的效果。</div>2019-11-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/6f/10/bfbf81dc.jpg" width="30px"><span>海绵薇薇</span> 👍（15） 💬（2）<div>hello 老师好，感谢老师之前的回答，有醍醐灌顶之效。

下面是读完这篇文章和下面评论之后的观点，不知是否有误，望指正，一如既往的感谢：）

1.

function a() {} &#47;&#47; 函数声明，在六种声明内

function () {} &#47;&#47; 报错，以function 开头应该是声明，但是又没有名字

(function() {}) &#47;&#47; 函数表达式（这是一个正真的匿名函数(function() {}).name 为 “”），即使是具名函数（function a() {}），当前作用域也找不到a，因为这不是声明

var a = function() {} &#47;&#47; 函数定义，这里的function() {} 也是表达式，只是赋给了变量a，所以有了区别，也有了名字a.name为a，称作函数定义

var b = function c() {} &#47;&#47; 函数定义，函数function c() {} 也是表达式，只是赋值给了变量b，但是b.name却为c，和上面存在的区别，但也是函数定义

2.

导出的是&quot;名字&quot;，我理解为名字就像一个绳子，后面拴的牛是会变的。这就是为什么import {a} from &#39;..&#47;a.js&#39; 这个a会变，虽然当前模块不能赋值给a。</div>2019-11-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/bd/ff/f4f2ae6a.jpg" width="30px"><span>Y</span> 👍（15） 💬（1）<div>老师，关于这边文章的中心，我能总结成这个意思吗。
export default function(){}。这个语法本身没有任何的问题。但是他看似导出一个匿名函数表达式。其实他真正导出的是一个具有名字的函数，名字的default。</div>2019-11-18</li><br/><li><img src="" width="30px"><span>万籁无声</span> 👍（12） 💬（1）<div>感觉没有抓住主题思想在表达什么，可能是我层次太低了</div>2019-11-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/c6/51/44791c01.jpg" width="30px"><span>🇧🇪 Hazard🇦🇷</span> 👍（10） 💬（1）<div>老师，有一句话不太明白。
&quot; import 的名字与 export 的名字只是一个映射关系 &quot;。

export 一个变量，比如 count，如果设一个定时器执行，每次count都加 1；
import { count }， 这个count也会每次都改变。这就是所说的映射关系吗？

这个映射关系是怎么做到的？</div>2020-03-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（10） 💬（1）<div>为什么在 import 语句中会出现“变量提升”的效果？
如老师所说，在代码真正被执行前，会先进行模块的装配过程，也就是执行一次顶层代码。所以如果import了一个模块，就会先执行模块内部的顶层代码，看起来的现象就是“变量提升”了。</div>2019-11-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/1f/86/3a7eeac4.jpg" width="30px"><span>leslee</span> 👍（7） 💬（1）<div>第三个结论推导过程的中间语法定义的引用那里(markdown &#39;&gt;&#39; 符号表示的引用)读得不是很通顺, 有点迷....</div>2019-11-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ba/bd/6f2f078c.jpg" width="30px"><span>Marvin</span> 👍（6） 💬（4）<div>export default v=&gt;v 这种，箭头函数是特例吗？</div>2019-11-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/f8/f6/3e2db176.jpg" width="30px"><span>七月有风</span> 👍（5） 💬（1）<div>ECMAScript 6 模块是静态装配的，而传统的 Node.js 模块却是动态加载的。是不是说node是在执行阶段才会执行模块的顶层代码。</div>2020-02-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/78/86/d5019bb0.jpg" width="30px"><span>Gamehu</span> 👍（5） 💬（1）<div>所以当都是export default...，以default为名字，但是import xx from ...，其实xx是import 重命名了default是么？不然就没法使用了</div>2020-02-21</li><br/><li><img src="" width="30px"><span>Geek_885849</span> 👍（4） 💬（2）<div>&quot;use strict&quot;;
      (function a() {
        const a = 2;
        console.log(a);
      })();
老师您好,这个函数名a 不是已经作为函数内部的标识符了吗,为什么还可以重新声明呢?</div>2020-08-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/3a/93/d7be8a1a.jpg" width="30px"><span>晓小东</span> 👍（4） 💬（1）<div>老师，我又来了，怕您看不到我的问题，接上一个问题，函数声明标识符不应该放入词法环境用中，本来我想函数声明标识符放入词法环境，来验证函数声明提升优先级高于var ，因为标识符的查找先从词法环境中查找，再到变量环境，再到上级作用域，从而实现声明的优先级。老师对于函数声明的优先级，你怎么看。</div>2019-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/1f/86/3a7eeac4.jpg" width="30px"><span>leslee</span> 👍（4） 💬（1）<div>是否可以理解为，一个具有了名字的函数表达式就可以称为函数定义</div>2019-12-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/ae/a0/707350ef.jpg" width="30px"><span>穿秋裤的男孩</span> 👍（4） 💬（1）<div>可以这样理解吗？
静态解析期：export只导出名字到某个名字表，import从名字表获取映射关系。
执行期：执行代码，为名字赋值。</div>2019-11-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/ae/a0/707350ef.jpg" width="30px"><span>穿秋裤的男孩</span> 👍（4） 💬（2）<div>所谓模块的装配过程，就是执行一次顶层代码而已。

这边的顶层代码是指什么呢？模块装配不是在静态解析期进行的吗？为什么还会执行代码？还是这边指的执行并不是一般意义上的执行呢？</div>2019-11-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/b9/ba/20714875.jpg" width="30px"><span>何嘉辉</span> 👍（3） 💬（1）<div>老师，我自己搞得有点混淆，帮我看看
node,js 自带的
commonjs 规范  
module.exports 与 require，它的原理是怎样的，与 esmodule 运行过程是否不一样；

然后前端webpack babel来实现的 es6 export import ,又是怎么回事呢，装配过程是否如课上说的一样，在代码真正被执行前，会先进行模块的装配过程，执行一次顶层代码这样吗？
nodejs 与浏览器装配过程的区别是怎样的呢？

以前面试题提到 import 是在编译时，require 是在运行时，这两者又有什么关系呢</div>2021-02-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/7d/67/791d0f5e.jpg" width="30px"><span>清波</span> 👍（2） 💬（1）<div>周老师，我有个疑问，标识符的产生和声明是在词法分析阶段，而值的绑定是在代码运行阶段嘛？还是，两个过程都在词法分析阶段？</div>2022-04-20</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/EK8FZ09JfUIvohJYwkco846n5DeBHyggeWFlO7ZTicjYZgDuibDG7bZkX4wDdz1yzq7IIvXd7g19ibzouT0GfxkVA/132" width="30px"><span>柠柚不加冰</span> 👍（2） 💬（1）<div>老师，问一下
export default ()=&gt;{……XXX};
和
const f = ()=&gt;{……XXX};
export default f;
这两种方式有没有本质区别呢？还有就是在webpack打包后这两种写法的打包后的产物是一样的吗？
我在umi官网的Fast Refresh章节看到是推荐用const存一下的写法，这个只是为了开发阶段的模块热替换有保持组件状态的功能，还是说有其他影响？平常开发中推荐用哪一种方式呢？</div>2021-03-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/1e/1a/e748832f.jpg" width="30px"><span>龙眼</span> 👍（2） 💬（1）<div>我的理解就是，export default function(){}，你导出的不是function() {}，而是名为default的函数。</div>2020-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/89/5b/d8f78c1e.jpg" width="30px"><span>孜孜</span> 👍（2） 💬（1）<div>是不是因为“import语句所在的模块中却是一个常量”，这样才能保证无论多少个import，它们始终都是指向的是export那个变量？</div>2020-06-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/6f/10/bfbf81dc.jpg" width="30px"><span>海绵薇薇</span> 👍（2） 💬（1）<div>Hello 老师好：）

函数定义

var a = function foo() {

	console.log(foo)

}

当前上下文没有标识符foo，但是foo函数内却可以拿到该标识符，所以foo这个标识符应该是声明了，但是不在当前作用域，那么可以简单理解为

var a = eval(&#39;\
    let foo;\
    foo = function (){\
        console.log(foo)\
    }\
&#39;)

可以这么理解吗？</div>2019-11-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a3/ea/53333dd5.jpg" width="30px"><span>HoSalt</span> 👍（1） 💬（1）<div>「导出“（其它模块的）名字”
export ... from ...;」
老师，导出其它模块的形式，为什么在当前模块无法使用这个变量?</div>2020-05-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/ae/a0/707350ef.jpg" width="30px"><span>穿秋裤的男孩</span> 👍（1） 💬（2）<div>老师，下面这句话我不是很懂，希望给解惑：

------
因此，该匿名函数初始化时才会绑定给它左侧的名字“default”，这会导致import f from ...之后访问f.name值会得到“default”这个名字。
------
根据这句话我实际运行了下代码，如下：
&#47;&#47; a.js
export default function() {};

&#47;&#47; b.js
import a from &#39;.&#47;a.js&#39;;
console.log(a.name); &#47;&#47; 打印为空字符串“”;

&#47;&#47; 疑惑点
按照您的解释，这边不是应该打印default吗？很奇怪</div>2019-11-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/cf/14/384258ba.jpg" width="30px"><span>Wiggle Wiggle</span> 👍（1） 💬（6）<div>文中多次出现“最顶层代码”，那什么是最顶层代码呢？</div>2019-11-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/2a/63/4d06890c.jpg" width="30px"><span>周星星</span> 👍（0） 💬（1）<div>因此，该匿名函数初始化时才会绑定给它左侧的名字“default”，这会导致import f from ...之后访问f.name值会得到“default”这个名字。

在导出匿名函数定义，我没有在导入的js中打印出来 &#39;default&#39;，而是空字符串，老师，这里是为什么啊，有其他同学遇到过吗</div>2021-03-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/c6/b4/e80a4fc8.jpg" width="30px"><span>Wise</span> 👍（0） 💬（1）<div>老师：export {x, y, z, ...}; 为什么归为导出声明的名字， 声明语句不就有那六种情况吗？</div>2021-03-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/fd/32/b905ea74.jpg" width="30px"><span>随波逐狼</span> 👍（0） 💬（1）<div>导出一个匿名函数，或者一个具名的函数的时候，这两种情况下是不同的。但无论它是否具名，它们都是不可能在当前作用域中绑定给default这个名字，作为这个名字对应的值的。
这段处理逻辑被添加在语法：
ExportDeclaration: export  default  AnonymousFunctionDefinition;
NOTE: ECMAScript 是将这里导出的对象称为 _Expression_&#47;AssignmentExpression，这里所谓 _AnonymousFunctionDefinition_ 则是其中 _AssignmentExpression_ 的一个具体实例。
的执行（Evaluation）处理过程中。也就是说当执行这行声明时，如果后面的表达式是匿名函数声明，那么它将强制在当前作用域中登记为“default”这样一个特殊的名字，并且在执行时绑定该匿名函数。所以，尽管语义上我们需要将它登记为类似var default ...所声明的名字“default”，但事实上它被处理成了一个不可访问的中间名字，然后影射给该模块的“某个名字表”。这段话是否矛盾了？上面说不可能在当前作用域绑定，下面说又可以给他绑定，啥情况？</div>2020-10-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/38/a4/46d7405b.jpg" width="30px"><span>Sixty</span> 👍（0） 💬（1）<div>请问老师，何为顶层代码何为非顶层代码啊？它们分别在什么时候被执行呢？一段js代码被v8引擎执行这个过程中到底做了些什么事情呢？</div>2020-07-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/b1/6a/7bd83c94.jpg" width="30px"><span>香瓜</span> 👍（0） 💬（1）<div>老师，是站在语言的角度来讲解的吗？就是老师刚开始说的，学会学习一门语言的通路，而不仅仅是javascript</div>2020-04-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/49/2d/fd085556.jpg" width="30px"><span>会飞小超人</span> 👍（0） 💬（1）<div>&#47;&#47; 导出“（声明的）名字”
export x ...;
export function x() ...
export class x ...
export {x, y, z, ...};

老师，我不太理解为什么最后一句话export{x,y,z,...}也是声明呢？</div>2020-03-10</li><br/>
</ul>