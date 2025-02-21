你好，我是周爱民。

今天这一讲的标题是一个**模板**。模板这个语法元素在JavaScript中出现得很晚，以至于总是有人感到奇怪：为什么JavaScript这么晚才弄出个模板这样的东西？

模板看起来很简单，就是把一个字符串里的东西替换一下就行了，C语言里的printf()就有类似的功能，Bash脚本里也可以直接在字符串里替换变量。这个功能非常好用，但在实现上其实很简单，无非就是字符串替换而已。

## 模板是什么？

但是，模板就是一个字符串吗？或者我们需要更准确地问一个概念上的问题：

模板是什么？

回顾之前的内容，我们说JavaScript中，有**语句**和**表达式**两种基本的可执行元素。这在语言设计的层面来讲，是很普通的，大多数语言都这么设计。少数的语言会省略掉**语句**这个语法元素，或者添加其它一些奇怪的东西，不过通常情况下它的结果就是让语言变得不那么人性。那么，是不是说，JavaScript中只有语句和表达式是可以执行的呢？

答案是“No”，譬如这里讲到的模板，其实就是**一种特殊的可执行结构**。

所有特殊可执行结构其实都是来自于某种固定的、确定的逻辑。这些逻辑语义是非常明确的，输入输出都很确定，这样才能被设计成一个标准的、易于理解的可执行结构。并且，如果在一门语言中添加太多的、有特殊含义的执行结构，那么这门语言就像上面说的，会显得“渐渐地有些奇怪了”。
<div><strong>精选留言（7）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/50/94/d89eeea4.jpg" width="30px"><span>阡陌</span> 👍（6） 💬（1）<div>虽然不知道&quot;模版调用&quot;在实际中有什么用处, 但根据结果来看, 似乎只有在&quot;模版调用&quot;时才能访问到模版字面量这个执行结构的类参数表结构, 作为函数调用的第一个参数.
var c = &#39;ccc&#39;, x = 1;
bar = (a1, a2, ...otherArgs) =&gt; console.log(a1, &#39;-------&#39;, a2, &#39;-----&#39;, otherArgs);
bar`ass${c}edd${x}illll`;
&#47;&#47; [&quot;ass&quot;, &quot;edd&quot;, &quot;illll&quot;, raw: Array(3)] &quot;-------&quot; &quot;ccc&quot; &quot;-----&quot; [1]
</div>2019-11-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/13/7b/74e90531.jpg" width="30px"><span>Astrogladiator-埃蒂纳度斯</span> 👍（6） 💬（3）<div>所以“1=1”是一个运行期错（ReferenceError），而不是语法错误（SyntaxError）。
请问为什么我尝试运行1=1在chrome控制台和node环境都报的语法错？
Uncaught SyntaxError: Invalid left-hand side in assignment</div>2019-11-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/18/65/35361f02.jpg" width="30px"><span>潇潇雨歇</span> 👍（4） 💬（5）<div>看过专栏后，我是这么理解的：模版也是可执行结构，有一个发现-引用的过程，有点类似参数表，但是最后具体表现为值。自然就可以调用，而不是特意去制造这么个语法。</div>2019-11-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/87/62/f99b5b05.jpg" width="30px"><span>曙光</span> 👍（2） 💬（1）<div>老师
1. handler.apply = function(target, thisArgument, argArray) {...} 其中“target”是指什么。
我找到的例子，和老师这个三个参数不能一一对应上；
var person = {
  fullName: function(city, country) {
    return this.firstName + &quot; &quot; + this.lastName + &quot;,&quot; + city + &quot;,&quot; + country;
  }
}
var person1 = {
  firstName:&quot;John&quot;,
  lastName: &quot;Doe&quot;
}
person.fullName.apply(person1, [&quot;Oslo&quot;, &quot;Norway&quot;]);

2. for (var {x, y} in obj) {...} 这个&#39;in&#39; 是否应该为&#39;of&#39;？ in是获取对象索引

function foo({a,b}){console.log({a,b});}
foo({a:1,c:2,b:3}); &#47;&#47; { a: 1, b: 3 }

function f1(){
	var obj =[{a:1,b:2},{a:3,b:4}];
	for(var {a,b} of obj){
		console.log({a,b});
	}
}
f1();  &#47;&#47;{ a: 1, b: 2 }   { a: 3, b: 4 }

3. “为什么 ECMAScript 要创建一个“模板调用”这样古怪的语法呢？”
 1) 猜想ECMAScript 要处理部分内容发生变动的字符串。
 2) 如果像C语言的print格式化字符串也行，但ECMAScript想要更抽象的处理字符串，选用函数处理
 3) foo`aaa${c}bbb${x}ccc`; 对于foo的参数是[aaa,bbb,ccc],c,x,像是通用的数据格式规范，js将参数分隔，其余交给函数处理；
 
4. 全篇看完几遍，只记住“名字和值的绑定”，是似懂非懂。</div>2020-11-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d4/37/528a43e7.jpg" width="30px"><span>Elmer</span> 👍（1） 💬（3）<div>所以我们之前所说的引用都有可能是可执行结构。
会按照场景求值，或者返回引用本身。
可以这么理解么。</div>2019-12-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c3/58/ba171e09.jpg" width="30px"><span>小胖</span> 👍（0） 💬（2）<div>js的函数调用的参数是传名调用，而标签模板会先计算出结果再传递给函数。
所以，模板调用是为了实现函数参数的传值调用?</div>2019-12-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/04/8d/005c2ff3.jpg" width="30px"><span>weineel</span> 👍（0） 💬（0）<div>原来对 js 的理解真是太肤浅了，特殊可执行结构 的概念刷新了我对js 的认识。</div>2019-11-25</li><br/>
</ul>