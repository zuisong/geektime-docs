你好，我是周爱民。欢迎回到我的专栏，我将为你揭示JavaScript最为核心的那些实现细节。

语句，是JavaScript中组织代码的基础语法组件，包括函数声明等等在内的六种声明，其实都被归为“语句”的范畴。因此，如果将一份JavaScript代码中的所有语句抽离掉，那么大概就只会剩下为数不多的、在全局范围内执行的表达式了。

所以，理解“语句”在JavaScript中的语义是重中之重。

尽管如此，你实际上要了解的也无非是**顺序**、**分支**、**循环**这三种执行逻辑而已，相比于它们，其它语句在语义上的复杂性通常不值一提。而这三种逻辑中尤其复杂的就是循环，今天的这一讲，我就来给你讲讲它。

## 块

在ECMAScript 6之后，JavaScript实现了**块级作用域**。因此，现在绝大多数语句都基于这一作用域的概念来实现。近乎想当然的，几乎所有开发者都认为一个JavaScript语句就有一个自己的块级作用域。这看起来很好理解，因为这样处理是典型的、显而易见的**代码分块的结果**。

然而，事实上正好相反。

真正的状况是，**绝大多数JavaScript语句都并没有自己的块级作用域**。从语言设计的原则上来看，越少作用域的执行环境调度效率也就越高，执行时的性能也就越好。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/17/bd/ff/f4f2ae6a.jpg" width="30px"><span>Y</span> 👍（43） 💬（14）<div>老师，在es6中，其实for只要写大括号就代表着块级作用域。所以只要写大括号，不管用let 还是 var，一定是会创建相应循环数量的块级作用域的。
如果不用大括号，在for中使用了let，也会创建相应循环数量的块级作用域。
也就是说，可以提高性能的唯一情况只有（符合业务逻辑的情况下），循环体是单行语句就不使用大括号且for中使用var。</div>2019-11-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/ea/05/9976b871.jpg" width="30px"><span>westfall</span> 👍（22） 💬（2）<div>因为单语句没有块级作用域，而词法声明是不可覆盖的，单语句后面的词法声明会存在潜在的冲突。</div>2019-11-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9a/af/ac09799f.jpg" width="30px"><span>小毛</span> 👍（14） 💬（1）<div>老师，最后的思考题感觉有点懵，按你文章里说的，for(let&#47;const...)这中语法，不管怎样在执行阶段，都会为每次循环创建一个iterationEnv块级作用域，那又为什么在单语句语法中不能有let词法声明呢，像if不能有是可以理解的，但是对于for(let&#47;const...)就不能理解了。
另外如果要提高for的性能，是不是不for(let&#47;const...)这样写，把let x放在for语句体外，在其之前声明，是不是就可以在执行阶段只有一个loopEnv，而不创建iterationEnv，从而提高性能。</div>2020-03-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d4/37/528a43e7.jpg" width="30px"><span>Elmer</span> 👍（12） 💬（1）<div>从语言设计的原则上来看，越少作用域的执行环境调度效率也就越高，执行时的性能也就越好。
单语句如果支持变量声明，相当于需要支持为iteration env新增子作用域，降低了效率？ 
如果需要完全可以自己写{} 来强制生成一个子作用域
不知道这样说对不对</div>2019-12-08</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eoJ8fUFEicTEPIvIdsicBywsBoIlBrPAPSbiasul9LNSO5juOxXJub1icIoWRdyk33MByyFxzHhdVKkUw/132" width="30px"><span>wDaLian</span> 👍（11） 💬（1）<div>const array = Array.from({length:100000},(item,i)=&gt;i)

    &#47;&#47; 案例一
    console.time(&#39;a&#39;)
    const cc = []
    for(let i in array){
        cc.push(i)
    }
    console.log(cc)
    console.timeEnd(&#39;a&#39;)

    &#47;&#47; 案例二
    console.time(&#39;b&#39;)
    const ccc = []
    for(var i in array){
        ccc.push(i)
    }
    console.log(ccc)
    console.timeEnd(&#39;b&#39;)
    
    &#47;&#47; 案例三
    console.time(&#39;c&#39;)
    const cccv = []
    for(let i in array)
        cccv.push(i);
    console.log(cccv)
    console.timeEnd(&#39;c&#39;)

1.老师你上次的评论我没看懂，第一我案例一和案例三是为了做区分所以案例一有大括号的
2.编译引擎的debug版本然后track内核，或者你可以尝试一个prepack-core这个项目，这两个东西是啥 我百度也没查到
3.老师你讲的都是概念的，我就想看到一个肉眼的案例然后根据概念消化，要不现在根本就是这个for循环到底应该咋写我都懵了</div>2020-01-12</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83epneC3LXv0Ve2tCXPfvsXtRb5StVicNCEHUSfzneLYUDJ03B6ocINHzeLf94aw0dEkjLShSdK9NUoA/132" width="30px"><span>Geek_8d73e3</span> 👍（9） 💬（5）<div>老师我发现运行以下代码会报错
for(let x = 0;x&lt;1;x++){
      var x = 100;
    }
    &#47;&#47;Uncaught SyntaxError: Identifier &#39;x&#39; has already been declared
在我理解中，let声明的x是在forEnv中，而我使用var声明的x因为javaScript早期设计，会在全局中声明一个x。这两个作用域是不会冲突的呀，为什么报错了？</div>2020-06-08</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83epneC3LXv0Ve2tCXPfvsXtRb5StVicNCEHUSfzneLYUDJ03B6ocINHzeLf94aw0dEkjLShSdK9NUoA/132" width="30px"><span>Geek_8d73e3</span> 👍（7） 💬（1）<div>老师，我发现，我运行这段代码的时候，并没有报错。
for(let i = 0;i&lt;10;i++){

        let i = 1000;

        console.log(i);
      }</div>2020-05-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/cf/14/384258ba.jpg" width="30px"><span>Wiggle Wiggle</span> 👍（7） 💬（2）<div>词法、词法作用域、语法元素……等等，这些概念特别模糊，老师有什么推荐的书吗？</div>2019-11-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/52/36/18f5d218.jpg" width="30px"><span>zcdll</span> 👍（7） 💬（5）<div>看不懂。。。第一个 switch 那个例子都看不懂。。</div>2019-11-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/bd/ff/f4f2ae6a.jpg" width="30px"><span>Y</span> 👍（6） 💬（1）<div>既然是单语句就说明只有一句话，如果就一句话，还是词法声明，那就会创建一个块级作用域，但是因为是单语句，那一定就没有地方会用到这个声明了。那这个声明就是没有意义的。所以js为了避免这种没有意义的声明，就会直接报错。是这样嘛</div>2019-11-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/60/12/268826e6.jpg" width="30px"><span>Marvin</span> 👍（5） 💬（3）<div>如果使用let &#47;const 声明for循环语句，会迭代创建作用域副本。那么不是和文中的：
对于支持“let&#47;const”的 for 语句来说）“通常情况下”只支持一个块级作用域这句话相矛盾么？</div>2019-11-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/6f/10/bfbf81dc.jpg" width="30px"><span>海绵薇薇</span> 👍（4） 💬（1）<div>hello，老师好，一如既往有许多问题等待解答：）

for(let&#47;const ...) ... 这个语句有两个词法作用域，分别是 forEnv 和 loopEnv。还有一个概念是iterationEnv，这个是迭代时生成的loopEnv的副本。

对于forEnv和loopEnv的范围我不是很清楚，请老师指点。

for(let i = 0; i &lt; 10; i++) 

​	setTimeout(() =&gt; console.log(i))

1 如上代码，let i 声明的 i 在forEnv还是在loopEnv &#47; iterationEnv里？

	1.1 如果在loopEnv &#47; iterationEnv里那么forEnv看起来就没啥用了
	
	1.2 如果在forEnv（文章中说let只会执行一次，并且forEnv是lopEnv的上级），那么按理说console.log打印出来的都是11（参考于：晓小东）

2 关于单语 let a = 1 报错问题

	2.1 如果是单语句中词法声明被重复有问题，那么with({}) let b = 1 这个报错就解释不通了。上面是说with有自己的块作用域，这个词法声明是在自己块语句中做的，并不会和别人冲突 

	2.2 同样的情况存在于for(let a...) ... 中，for也有自己的作用域，并且每次循环都会生成新的副本，也不应该存在重复问题

3 关于上面提到的eval
	eval(&#39;let a = 1&#39;); console.log(a) &#47;&#47; 报错
	eval是不是自己也有一个作用域？

期待：）</div>2019-11-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/3a/93/d7be8a1a.jpg" width="30px"><span>晓小东</span> 👍（4） 💬（1）<div>
老师您看下这段代码， 我在Chrome 打印有点不符合直觉， Second 最终打印的应该是2， 为什么还是1，2， 3；

for (let i = 0; i &lt; 3; i ++, setTimeout(() =&gt; console.log(&quot;Second&quot; + i), 20))
    console.log(i), setTimeout(() =&gt; console.log(&#39;Last:&#39; + i), 30);

0, 1, 2 
Second: 0, 1,  2
Last: 0, 1, 2</div>2019-11-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/2d/44/0a209c31.jpg" width="30px"><span>桔右</span> 👍（4） 💬（2）<div>假设允许的话，没有块语句创建的iterationEnv的子作用域，let声明就直接在iterationEnv作用域中，会每次循环重复声明。</div>2019-11-21</li><br/><li><img src="" width="30px"><span>二二</span> 👍（2） 💬（1）<div>你好老师，按照文章的解释，因为for循环中let会导致块级作用域，开销会变大，此处的开销可以粗略理解成时间。
var a = new Array(10000).fill(0)
console.time(&#39;var&#39;)
for(var i=0, len=a.length; i&lt;len; i++){}
console.timeEnd(&#39;var&#39;)
console.time(&#39;let&#39;)
for(let i=0, len=a.length; i&lt;len; i++){}
console.timeEnd(&#39;let&#39;)
在chrome devtool执行的结果，var会比let要慢许多，请问中间还发生了什么，导致var会比let慢呢？</div>2020-10-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/7f/a4/34955365.jpg" width="30px"><span>青山入我怀</span> 👍（2） 💬（1）<div>老师，请问既然forEnv是loopEnv的上级，而iterationEnv又是loopEnv的副本，那么按道理在iterationEnv中对i的改动，在查找i时不都是会通过环境链回溯，找到forEnv这个运用域下的i吗，那么闭包现象发生时，找到的i应该是同一个i啊，感觉增加了副本无法避免这个问题啊？</div>2020-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/61/02/6ccf315c.jpg" width="30px"><span>A.     成事在天</span> 👍（2） 💬（2）<div>老师我认为的是函数递归比for循坏开支大，首先函数递归会不断重复的在作用域链中生成global scope，如果递归10次就会有十个重复的global scope，for循环是块级作用域它确实也会重复的生成内部的上下文但是不会生成作用域链也就不会重复的去生成global scope，老师我理解的对吗</div>2020-08-02</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83epneC3LXv0Ve2tCXPfvsXtRb5StVicNCEHUSfzneLYUDJ03B6ocINHzeLf94aw0dEkjLShSdK9NUoA/132" width="30px"><span>Geek_8d73e3</span> 👍（2） 💬（1）<div>所以，语句for ( x ...) ...语法中的标识符x是一个词法名字，应该由for语句为它创建一个（块级的）词法作用域来管理之。
老师，对于这句话，如果我运行以下代码
var x = 1;
let  y = 2;
那么javaScript也会创建两个作用域？一个变量作用域管理x，一个词法作用域管理y？
那么如果全局中已经存在了变量作用域和词法作用域
为什么for(let i =0....)中， 这个i不在刚才的词法作用域中声明，而要重新再创讲一个词法作用域？</div>2020-06-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/6f/10/bfbf81dc.jpg" width="30px"><span>海绵薇薇</span> 👍（2） 💬（2）<div>老师好，关于forEnv和loopEnv和loopEnv的抄写是否可以简单模拟如下？

function forEnv() {
    for (var i = 0, len = 10; i &lt; len; i++) 
	(function loopEnv(i) {
	    console.log(i)
	}(i))
}

其中forEnv就可以被看做for(let i ...) ... 生成的forEnv。
循环体每次迭代进行的loopEnv抄写，被每次迭代生成的函数闭包所模拟。
</div>2020-04-07</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTI5jr1KfpLoXdoiaLzLswPiazCgCnyPkKhIqrEujPtGA1kryZYaruF8GmUTRRWn1YK71QVSTSVpwkzQ/132" width="30px"><span>从未止步</span> 👍（2） 💬（1）<div>老师，因为在循环后边的单语句中如果出现了词法声明，但是这时候其实单语句并没有块级作用域，需要重复声明创建作用域副本，来支持这个语句的执行，所以javaScript限制了这种情况的发生，可以这样理解嘛？ 谢谢老师～</div>2020-03-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（2） 💬（1）<div>为什么单语句（single-statement）中不能出现词法声明（ lexical declaration ）？
我觉得应该是语法规定 单语句后面需要一个表达式，而一个声明语句是不行的。</div>2019-11-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5c/c2/8ffd2ad0.jpg" width="30px"><span>qqq</span> 👍（2） 💬（1）<div>单语句对应的是变量作用域，不能出现词法声明吗</div>2019-11-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1b/d5/0cae2c5b.jpg" width="30px"><span>😁陈哲奇</span> 👍（1） 💬（1）<div>ECMA规范中并没有看到 forEnv 的描述，只有 loopEnv 和 (this)InterrationEnv，循环变量 i 是在 loopEnv 中创建的，每次循环，InterrationEnv 都会从上一个 InterrationEnv 中拷贝新的变量值（一般是经过了 increment 后的变量值）。

这个和文章中的描述并不一致。

https:&#47;&#47;262.ecma-international.org&#47;13.0&#47;#sec-forbodyevaluation</div>2022-09-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/81/fa/542577c8.jpg" width="30px"><span>👣</span> 👍（1） 💬（1）<div>老师。 我是这样理解的。 
1. 如果使用了 for（let &#47; const....) {} 在使用了let &#47; const 和 {} 会创建n个此法作用域 和 创建n个块级作用域。
    如果不是的话： 那么看一下代码
   for（let x in {name: 1, gae: 2}）{
     &#47;&#47; 在这里的话 会创建2个父级作用域 两个父级作用域下会有不同的块级作用于
      如果不是的话， 那么这里的x 不是重复声明 而是 重新赋值？ 但是如果是重新赋值 那么使用const的话 会报一个 重复创建的错误
    }
2。 如果使用了 for（var x ...)   这里的var 是创建在 上级作用域的 varNames里的 如果写在函数中则是创建在函数作用于中。。。。。
      for（var x  in {name: 1, age:2})  {
           setTimeout(_ =&gt; console.log(x), 1000)
           &#47;&#47; 这里的虽然创建块级作用域， 但是没有声明 自己的词法作用域。 在要执行宏任务的时候， 可能 循环已经完成 而x 已经是最新的值， 所以输出是 age 但是如果使用的是 let &#47; const。则x 是不同的key 应为， 他们创建了自己的词法作用域名， 所有哪怕10秒之后在执行的宏任务。依旧可以访问到。 forEvn中变量。 其实这里也算是一种闭包的使用是吗？
      }</div>2021-11-25</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83epneC3LXv0Ve2tCXPfvsXtRb5StVicNCEHUSfzneLYUDJ03B6ocINHzeLf94aw0dEkjLShSdK9NUoA/132" width="30px"><span>Geek_8d73e3</span> 👍（1） 💬（1）<div>老师，我发现这行代码会输出1000。这是为什么呀
      let x = 1000;
      try{
        console.log(x);

        if(true){
          let x = 100;
        }

      }catch(e){
        console.log(e)
      }</div>2020-05-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/a9/64/819fccec.jpg" width="30px"><span>蔡孟泳</span> 👍（1） 💬（1）<div>老师 请问下 有时候会采用数组倒序来有话，原理是？因为数组是顺序存储结构？</div>2020-04-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a3/ea/53333dd5.jpg" width="30px"><span>HoSalt</span> 👍（1） 💬（1）<div>&#47;&#47;（注：没有使用大括号）
with (x) &#47;* 作用域1 *&#47;; &#47;&#47; &lt;- 这里存在一个块级作用域

with 没有大括号却有作用域能怎么体现（证明）吗？</div>2020-04-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/01/73/a3bbaab9.jpg" width="30px"><span>Aiden</span> 👍（1） 💬（1）<div>&gt; 一些简单的、显而易见的块级作用域包括：

这里没看懂第三点
1；try catch finally 会形成块作用域
2：with会形成块作用域
3：快语句是个啥？

我的理解是块语句要和let const配置使用才会形成块作用域。</div>2020-03-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/53/fd/db2cac71.jpg" width="30px"><span>红白十万一只</span> 👍（1） 💬（2）<div>根据ECMAScript 规范第 13.7.4.7 节
for循环的var和let、const处理是不同的
var的就不说了，老师已经说得很明白了。会变量提升至当前作用域
而let和const：
for (let i = 0; i &lt; 3; i++) {
  let i = &#39;a&#39;;
  console.log(i);
}
输出 a a a
其实底层处理时在for (let i = 0; i &lt; 3; i++)这个括号内有一个隐藏作用域
每次迭代循环时都创建一个新变量i，并以之前迭代中同名变量(i)的值将其初始化
所以这三次循环相当于(伪)
(let i=0){
  let i = &#39;a&#39;;
  console.log(i);
}
(let i=1){
  let i = &#39;a&#39;;
  console.log(i);
}
(let i=2){
  let i = &#39;a&#39;;
  console.log(i);
}
这就是let、const在for(有{}的情况下)是有两个作用域的。另外for (const i = 0; i &lt; 3; i++) 会报错，因为虽然const i是重新生成的，但是i++修改了i这个值，const又是常量无法修改导致报错
最后
单语句中不能出现词法声明，是因为没有使用{}强制创建作用域，无法词法声明么？</div>2020-02-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/06/54/16bb64d0.jpg" width="30px"><span>蛋黄酱</span> 👍（1） 💬（1）<div>老师，switch case 如果加了{} 就会转成块级作用域了吧。
正在用AST写工具，测switch的时候并没有意识到case的作用域问题，现在感觉最好把ecma读一遍。</div>2019-12-13</li><br/>
</ul>