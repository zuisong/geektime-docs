在前面[《07 | 变量提升：JavaScript代码是按顺序执行的吗？》](https://time.geekbang.org/column/article/119046)这篇文章中，我们已经讲解了JavaScript中变量提升的相关内容，**正是由于JavaScript存在变量提升这种特性，从而导致了很多与直觉不符的代码，这也是JavaScript的一个重要设计缺陷**。

虽然ECMAScript6（以下简称ES6）已经通过引入块级作用域并配合let、const关键字，来避开了这种设计缺陷，但是由于JavaScript需要保持向下兼容，所以变量提升在相当长一段时间内还会继续存在。这也加大了你理解概念的难度，因为既要理解新的机制，又要理解变量提升这套机制，关键这两套机制还是同时运行在“一套”系统中的。

但如果抛开JavaScript的底层去理解这些，那么你大概率会很难深入理解其概念。俗话说，“断病要断因，治病要治根”，所以为了便于你更好地理解和学习，今天我们这篇文章会先“**探病因**”——分析为什么在JavaScript中会存在变量提升，以及变量提升所带来的问题；然后再来“**开药方**”——介绍如何通过**块级作用域并配合let和const关键字**来修复这种缺陷。

## 作用域（scope）

为什么JavaScript中会存在变量提升这个特性，而其他语言似乎都没有这个特性呢？要讲清楚这个问题，我们就得先从作用域讲起。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/82/dc/5dbbe598.jpg" width="30px"><span>coolseaman</span> 👍（555） 💬（37）<div>【最终打印结果】：VM6277:3 Uncaught ReferenceError: Cannot access &#39;myname&#39; before initialization
【分析原因】：在块作用域内，let声明的变量被提升，但变量只是创建被提升，初始化并没有被提升，在初始化之前使用变量，就会形成一个暂时性死区。
【拓展】
var的创建和初始化被提升，赋值不会被提升。
let的创建被提升，初始化和赋值不会被提升。
function的创建、初始化和赋值均会被提升。</div>2019-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/c5/0c/03bd4b4e.jpg" width="30px"><span>朙</span> 👍（73） 💬（11）<div>这篇真的是神作啊。 有一个疑问，在abcd那个例子里，第一步&lt;编译并创建执行上下文&gt;的图里并没有块级作用域的b=undefined; d=undefined。而在第二步里&lt;继续执行代码&gt;的图中才出现b=undefined; d=undefined。想问下这个块级作用域的b=undefined; d=undefined是不是应该在第一步的编译阶段里就有。还是说在执行阶段像函数那样，块级作用域会有一个自己的编译阶段

</div>2019-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/33/2f/84f7d587.jpg" width="30px"><span>YBB</span> 👍（65） 💬（4）<div>有个问题，在一个块级作用域中，let和const声明的变量是在编译阶段被压入栈中还是执行阶段被压入栈中？在文中的表述来看，第一个let声明的变量是在编译阶段就压入栈中的，但是后面的变量又感觉是在执行是压入栈中，有点混乱。</div>2019-08-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/98/7c/07e6e7b7.jpg" width="30px"><span>Tim</span> 👍（55） 💬（11）<div>看得很生气，全篇文章不提变量的「创建」「初始化」「赋值」这三种区别，把创建和初始化揉在一起了，也是看了精选留言里第一条评论之后Google才查找到，否则刚开始我真的不理解为啥都已经在词法环境找到了变量却报错了！按照这种理论的话，是否说明词法环境只有变量，并没有等于undefined？
真的不需要更新一下吗？？？？？</div>2020-01-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/3a/93/d7be8a1a.jpg" width="30px"><span>晓小东</span> 👍（27） 💬（3）<div>在ES3开始，try &#47;catch 分句结构中也具有块作用域。补充……</div>2019-08-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/4d/04/5e0d3713.jpg" width="30px"><span>李懂</span> 👍（18） 💬（7）<div>执行上下文是在编译时创建的，在执行代码的时候已经有词法环境了，而且变量已经默认初始化了undefiend，为什么还会存在暂时性死区，老师解答一下！</div>2019-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f1/15/8fcf8038.jpg" width="30px"><span>William</span> 👍（10） 💬（8）<div>第二步，继续执行代码。 这张图我觉得有错误，当进入foo函数内部的代码块之后，并没有了编译阶段，此时，新创建的栈顶块级作用域的内容为空，而并没有 b = undefined 和 d = undefined 两项内容。 执行完 let b = 3 之后，分配内存，块级作用域出现 b = 3 一项。 执行 let d = 5 之后，为d分配内存，栈顶块级作用域增加一项 d = 5。</div>2019-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/c5/0c/03bd4b4e.jpg" width="30px"><span>朙</span> 👍（9） 💬（2）<div>if(0){ var myname = &quot; 极客邦 &quot;} 这段代码里的if条件是false很有意思。是说编译阶段不管if会不会执行。里面的代码都会编译，因此这里的myname变量提升，从而导致上面的console.log(myname)输出undefined吗？ 
另外let 声明的变量会提升吗？</div>2019-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/c4/4f/fdd51040.jpg" width="30px"><span>小锅锅</span> 👍（8） 💬（1）<div>老师，听你对比了c语言，既然let const存在暂时性死区，那么c语言的变量也存在同样的暂时性死区报错吗？</div>2019-08-25</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqXKSvfaeicog2Ficx4W3pNeA1KRLOS7iaFy2uoxCDoYpGkGnP6KPGecKia6Dr3MtCkNGpHxAzmTMd0LA/132" width="30px"><span>Geek_East</span> 👍（1） 💬（1）<div>我想，理解execution context和scope的区别是理解这个问题的一个关键；很多时候执行上下文和作用域都混着说</div>2019-12-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/94/82/d0a417ba.jpg" width="30px"><span>蓝配鸡</span> 👍（1） 💬（3）<div>let myname= &#39;极客时间&#39;
{
  console.log(myname) 
  let myname= &#39;极客邦&#39;
}

编译过程：
生成执行上下文压入栈
变量环境为空
词法环境中myname=undefined压入栈

执行过程：
词法环境中myname=极客时间
新开一个 myname =undefined 压入词法环境栈
查找myname并输出undefined 
赋值当前栈头上myname=极客邦
pop栈头

结束

</div>2019-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/fd/90/ae39017f.jpg" width="30px"><span>爱吃锅巴的沐泡</span> 👍（1） 💬（1）<div>有个疑问：
在思考题中，
1、执行到console.log(myname)这句话时，编译阶段已经完成，那么词法环境中的栈顶 是不是已经有了该作用域块了，let myname =‘极客邦’  是不是也已经在栈顶的作用域快中了？
2、执行到console.log(myname)这句话时，是按着从词法环境栈顶到栈底到变量环境的顺序查找，栈底已经存在了函数级的 let myname了，那为什么还是会报错呢？</div>2019-08-24</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/ibZVAmmdAibBeVpUjzwId8ibgRzNk7fkuR5pgVicB5mFSjjmt2eNadlykVLKCyGA0GxGffbhqLsHnhDRgyzxcKUhjg/132" width="30px"><span>pyhhou</span> 👍（1） 💬（5）<div>思考题中，在 node 环境中 run 的话，console.log(myname) 这一行会报错，但是在网上的一些 JavaScript 的 editor 中 run，输出就是 undefined。一开始没有 run 代码，把词法环境当作变量环境来分析的话，我认为会输出 undefined，可能在 node 环境下，词法环境中可能还是会有逻辑去判断一个声明是在运行代码前还是后，比如
let a;
console.log(a);    &#47;&#47; undefined

如果声明在运行之后就会报错：
console.log(a);  &#47;&#47; 报错
let a;

想请教老师的一点细节方面的问题，就是平时写 JavaScript 代码每行结束后需要带上分号吗？看老师您这里写的代码有很多结束都没有带分号，但是之前看到过一篇文章说 JavaScript 里面是通过分号去判断一个语句的结束，不知道这一点在实际的开发中是否有影响？
</div>2019-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/6f/84/5b56dba2.jpg" width="30px"><span>mmma</span> 👍（0） 💬（1）<div>为什么不创建一个块级执行上下文，而是放入词法环境？</div>2019-09-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/9e/0c/2008b3ed.jpg" width="30px"><span>假面猫</span> 👍（0） 💬（1）<div>let myname= &#39;极客时间&#39;
{
  console.log(myname) 
  let myname= &#39;极客邦&#39;
}
VM20209:3 Uncaught ReferenceError: myname is not defined
    at &lt;anonymous&gt;:3:15

奇怪，我在控制台输入竟然是 myname 未定义。</div>2019-09-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/9f/90/4656119a.jpg" width="30px"><span>拖鞋</span> 👍（0） 💬（1）<div>  console.log(a)
      var a= 1

      console.log(a)
      let a = 1
老师按照您词法环境的解释  这俩中写法应该执行结果是一样的啊</div>2019-09-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/bc/29/c248bfd1.jpg" width="30px"><span>肥嘟嘟左卫门</span> 👍（0） 💬（3）<div>老师，您好，想问一个问题，为什么下面这段代码可以分别打印出 0，1，2，3，4，这里明明是只声明了一个 i 啊
var liList = document.querySelectorAll(&#39;li&#39;) &#47;&#47; 共5个li
for( let i=0; i&lt;liList.length; i++){
  liList[i].onclick = function(){
    console.log(i)
  }
}</div>2019-08-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/eb/09/ba5f0135.jpg" width="30px"><span>Chao</span> 👍（0） 💬（1）<div>思考题带来一个 临时死区的概念 </div>2019-08-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/8c/d5/398b31fe.jpg" width="30px"><span>木棉</span> 👍（0） 💬（1）<div>ES6 明确规定，如果区块中存在let和const命令，这个区块对这些命令声明的变量，从一开始就形成了封闭作用域。凡是在声明之前就使用这些变量，就会报错。</div>2019-08-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/17/36/19ac6798.jpg" width="30px"><span>Y ｓ.</span> 👍（0） 💬（3）<div>老师您好，ES5标准文档中规定，执行环境包括：词法环境、变量环境、this绑定。并且解释道：其中执行环境的词法环境和变量环境组件始终为词法环境对象。当创建一个执行环境时，其词法环境组件和变量环境组件最初是同一个值。在该执行环境相关联的代码的执行过程中，变量环境组件永远不变，而词法环境组件有可能改变。

我想知道为何说：变量环境组件永远不变，而词法环境组件有可能改变。为什么需要两个词法环境对象？一个不行吗？什么时候使用词法组件，什么时候使用变量组件呢？</div>2019-08-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1b/d5/0cae2c5b.jpg" width="30px"><span>😁陈哲奇</span> 👍（0） 💬（1）<div>我想问问老师，这类知识大部分书籍都不会提及，ECMA Script的规范文档应该有描述这些内容，建不建议通过阅读这个文档来学习呢？</div>2019-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/5f/80/51269d88.jpg" width="30px"><span>Hurry</span> 👍（0） 💬（1）<div>简单画个图

-------- 代码执行上下文 ----------

---- 变量环境 ---  ---- 词法环境 ----

                             --------------
                             name = undefined
                             --------------

                             --------------
                              name = ’极客帮‘
                             --------------</div>2019-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（0） 💬（2）<div>思考题：
当运行到块级作用域时，先预编译，词法环境中会生成 myname = undefined，然后console.log会先在词法环境中找，当遇到undefined时，报错：不能使用未初始化前使用‘myname’。</div>2019-08-24</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJOBwR7MCVqwZbPA5RQ2mjUjd571jUXUcBCE7lY5vSMibWn8D5S4PzDZMaAhRPdnRBqYbVOBTJibhJg/132" width="30px"><span>ヾ(◍°∇°◍)ﾉﾞ</span> 👍（0） 💬（3）<div>js的新标准哪些是浏览器原生支持，哪些需要编译后支持的呢？</div>2019-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/d9/c6/8be8664d.jpg" width="30px"><span>ytd</span> 👍（0） 💬（3）<div>```js
let myname= &#39;极客时间&#39;
{
  console.log(myname)  &#47;&#47; 报错，在chrome下会报Uncaught ReferenceError: Cannot access &#39;myname&#39; before initialization
  let myname= &#39;极客邦&#39;
}
```
let声明的变量在编译阶段会被加入执行上下文的词法环境，而且不会被提升到作用域的顶部（这也就是块级作用域原理）
或者可以这么说：myname直到`let myname= &#39;极客邦&#39;`声明语句被执行时才被初始化
所以，在声明之前访问let声明的变量会报错。不知道这么理解合不合理？
但是浏览器的报错感觉有些让人疑惑，`Cannot access &#39;myname&#39; before initialization
`，变量在初始化之前不能访问，那么既然let声明的变量未被提升，为什么不报变量未定义错误呢？期待老师的解惑。</div>2019-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/f5/b8/9f165f4b.jpg" width="30px"><span>mfist</span> 👍（0） 💬（1）<div>1. 在块级作用域中，从｛开始到let myname= &#39;极客邦&#39; 代码之间会形成一个暂时性死区，如果中间去访问变量myname，会报初始化之前不能访问myname的错误。Uncaught ReferenceError

2. 另外上面的一个foo函数也会报d没有定义吧，d在块级作用域中声明，在外面是访问不到的
function foo(){
    var a = 1
    let b = 2
    {
      let b = 3
      var c = 4
      let d = 5
      console.log(a)
      console.log(b)
    }
    console.log(b) 
    console.log(c)
    console.log(d)
}   
foo()
</div>2019-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/b7/b6/d01f8727.jpg" width="30px"><span>…Lucky</span> 👍（9） 💬（5）<div>老师，按照最后的思考题。let，const会在编译阶段创建，但不赋值。但是上面几个图中都是直接赋值的undefined。这是否矛盾
？</div>2019-09-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/fd/90/ae39017f.jpg" width="30px"><span>爱吃锅巴的沐泡</span> 👍（7） 💬（1）<div>对文中foo()函数的分析和一些问题：
           我调试了一下，①断点打在 let b = 2，此时的scope中只有local：a = 1，b = undefined，c = undefined；并没有block，这应该说明js是解释性语言，一句一执行的。
           ②当断点走到 let b = 3时，这时进入了作用域，scope中有了block：b = undefined，d = undefined，这应该说明在进入作用域之前AST已经生成，并确定了作用域的范围。
           问题：1、老师提到在进入作用域时let声明的变量被创建，结合断点可以证明，那么是不是说 let声明的变量在该作用域内提升了，但没有提升赋值语句？因为在②处已经有了d = undefined。
           问题：2、把foo()中的作用域变形如下：
                           {
                                  let b = 3
                                  console.log(d)
                                  var c = 4
                                  let d = 5
                                  console.log(a)
                                  console.log(b)
                             }
                   当断点走到 let b = 3处，scope的block中只有b = undefined，并没有d = undefined，是因为“暂时性死区”是js在语法上的设置，防止访问声明前的变量，而在进入作用域之前就会有语法树的生成，所以在编译到console.log(d)时，遇到错误，所以没有在词法环境中创建变量d。这样分析是否正确？</div>2019-09-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/25/2c/8f61089f.jpg" width="30px"><span>宗麒麟</span> 👍（5） 💬（1）<div>精选留言也好多精品啊，老师看到应该也很欣慰吧</div>2020-04-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/d0/73/06ed7823.jpg" width="30px"><span>阿郑</span> 👍（5） 💬（0）<div>ES6明确规定，如果区块中存在let和const命令，这个区块对这些命令声明的变量，从一开始就形成了封闭作用域。凡是在声明之前就使用这些变量，就会报错。
总之，在代码块内，使用let命令声明变量之前，该变量都是不可用的。这在语法上，称为“暂时性死区”（temporal dead zone，简称TDZ）
因此，思考题中的那段代码，执行会报错：
Uncaught SyntaxError: Identifier &#39;myname&#39; has already been declared
    at &lt;anonymous&gt;:1:1</div>2020-03-28</li><br/>
</ul>