你好，我是winter。

不知道你有没有注意到，我们在语句部分，讲到了很多种语句类型，但是，其实最终产生执行效果的语句不多。

事实上，真正能干活的就只有表达式语句，其它语句的作用都是产生各种结构，来控制表达式语句执行，或者改变表达式语句的意义。

今天的课程，我们就深入到表达式语句中来学习一下。

## 什么是表达式语句

表达式语句实际上就是一个表达式，它是由运算符连接变量或者直接量构成的（关于直接量我们在下一节详细讲解）。

一般来说，我们的表达式语句要么是函数调用，要么是赋值，要么是自增、自减，否则表达式计算的结果没有任何意义。

但是从语法上，并没有这样的限制，任何合法的表达式都可以当做表达式语句使用。比如我们看下面的例子。

```JavaScript
a + b;
```

这句代码计算了a和b相加的值，但是不会显示出来，也不会产生任何执行效果（除非a和b是getter），但是不妨碍它符合语法也能够被执行。

下面我们就一起来了解下都有哪些表达式，我们从粒度最小到粒度最大了解一下。

## PrimaryExpression 主要表达式

首先我们来给你讲解一下表达式的原子项：Primary Expression。它是表达式的最小单位，它所涉及的语法结构也是优先级最高的。
<div><strong>精选留言（16）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/18/26/4b/d1fc46d6.jpg" width="30px"><span>奋逗的码农哥</span> 👍（13） 💬（6）<div>js中的运算符有很多，推荐这篇教程 http:&#47;&#47;www.w3school.com.cn&#47;js&#47;js_operators.asp</div>2019-07-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/13/ab/84afa0b5.jpg" width="30px"><span>木木</span> 👍（9） 💬（3）<div>f`a${b}c`;
没有明白这个是什么意思</div>2019-04-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/f3/63/63d30619.jpg" width="30px"><span>mingingคิดถึง</span> 👍（1） 💬（4）<div>winter老师，模板字符串当做参数传入时不带括号的写法不是很懂：
function f(a){console.log(a)}
const b = 1
f`a${b}c`
打印出来是：[&quot;a&quot;, &quot;c&quot;, raw: Array(2)]</div>2019-10-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/fd/df/aff2c193.jpg" width="30px"><span>炒饭</span> 👍（16） 💬（0）<div>@嗨海海 winter老师讲得是语言细节，这些应该都是基础知识，但实际上很多一线前端都忽略了这些。比起常见那些框架工具应用，这课在国内还是很难得的，特别还是winter老师开的，讲的透彻，感谢winter老师，让我受益匪浅</div>2019-04-15</li><br/><li><img src="" width="30px"><span>vspt</span> 👍（14） 💬（1）<div>winter老师，问个问题，在react源码中经常看到如下写法，一直没太理解，请问这种写法有什么好处吗？

```
var validateFormat = function () {};

{
  validateFormat = function (format) {
    if (format === undefined) {
      throw new Error(&#39;invariant requires an error message argument&#39;);
    }
  };
}
```</div>2019-04-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/22/c1/a662fadf.jpg" width="30px"><span>桂马</span> 👍（5） 💬（0）<div>平时不确定优先级的一般都加括号</div>2019-04-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/41/a5/16c615cc.jpg" width="30px"><span>乃乎</span> 👍（3） 💬（0）<div>literal 翻译成字面量会不会更好，好像大多数翻译都是用的那个</div>2019-04-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/13/ab/84afa0b5.jpg" width="30px"><span>木木</span> 👍（1） 💬（0）<div>f`a${b}c`;</div>2019-04-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/9a/ab/fd201314.jpg" width="30px"><span>小耿</span> 👍（0） 💬（0）<div>&quot;不加 new 也可以构成 New Expression&quot;，请问这句咋理解？New Expression 不都需要加 new 吗？
</div>2023-03-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/bb/47/b60ae3eb.jpg" width="30px"><span>你好，阳光</span> 👍（0） 💬（3）<div>winter老师，有个疑问，new expression属于左值表达式，为何new Object()={}会报错invalid assignment left-hand side？</div>2021-09-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/da/3e/e0d073ca.jpg" width="30px"><span>「前端天地」公众号</span> 👍（0） 💬（0）<div>LeftHandSideExpression a() = b那里有点没看明白.
比如:
function a () {
 return {};
}
var b = 1;
a() = b;
这个时候会报错</div>2021-03-04</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/BWDhMILusuficY2zo10KiaetDPjW08aBJ5sn7cLy2VV91hicacriaibDoqDAexLc0Mr4fnwpbllOLZ0BEFib3tic5WtHA/132" width="30px"><span>Geek_e6f5a9</span> 👍（0） 💬（0）<div>运算符优先级：一元(delete,~,!等)&gt;算术&gt;关系&gt;位移&gt;二进制位运算&gt;逻辑&gt;条件&gt;赋值&gt;逗号，mdn链接https:&#47;&#47;developer.mozilla.org&#47;zh-CN&#47;docs&#47;Web&#47;JavaScript&#47;Reference&#47;Operators</div>2020-12-14</li><br/><li><img src="" width="30px"><span>难上加难</span> 👍（0） 💬（1）<div>老师您好，想问一下，
function f(a){console.log(a)}
const b = 1
f`a${b}c`，
这里面的f`a${b}c`是不是跟console,log(&#39;a&#39;+b+&#39;c&#39;)差不多</div>2020-06-08</li><br/><li><img src="" width="30px"><span>难上加难</span> 👍（0） 💬（0）<div>老师您好，想问一下function f(a){console.log(a)}
const b = 1
f`a${b}c`</div>2020-06-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/f3/63/63d30619.jpg" width="30px"><span>mingingคิดถึง</span> 👍（0） 💬（1）<div>winter老师，函数传入模板标签，不带括号的写法不是很了解，我在浏览器运行了一下得到结果也看不懂：</div>2019-10-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/b1/58/7d4f968f.jpg" width="30px"><span>plasmatium</span> 👍（0） 💬（0）<div>
默认的模板字符串就是拼接，但是可以写个函数来改变这种默认行为。之前的课有讲过的。感觉这个有点类似julia语言的@f_str宏</div>2019-04-04</li><br/>
</ul>