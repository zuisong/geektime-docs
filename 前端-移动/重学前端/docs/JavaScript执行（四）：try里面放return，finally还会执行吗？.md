你好，我是winter。

在前面几篇文章中，我们已经了解了关于执行上下文、作用域、闭包之间的关系。

今天，我们则要说一说更为细节的部分：语句。

语句是任何编程语言的基础结构，与JavaScript对象一样，JavaScript语句同样具有“看起来很像其它语言，但是其实一点都不一样”的特点。

我们比较常见的语句包括变量声明、表达式、条件、循环等，这些都是大家非常熟悉的东西，对于它们的行为，我在这里就不赘述了。

为了了解JavaScript语句有哪些特别之处，首先我们要看一个不太常见的例子，我会通过这个例子，来向你介绍JavaScript语句执行机制涉及的一种基础类型：Completion类型。

## Completion类型

我们来看一个例子。在函数foo中，使用了一组try语句。我们可以先来做一个小实验，在try中有return语句，finally中的内容还会执行吗？我们来看一段代码。

```
function foo(){
  try{
    return 0;
  } catch(err) {

  } finally {
    console.log("a")
  }
}

console.log(foo());
```

通过实际试验，我们可以看到，finally确实执行了，而且return语句也生效了，foo()返回了结果0。

虽然return执行了，但是函数并没有立即返回，又执行了finally里面的内容，这样的行为违背了很多人的直觉。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/19/b3/b8/62214c79.jpg" width="30px"><span>csᵏᵒᵖ</span> 👍（7） 💬（2）<div>winter老师，特殊处理就是指后面的 “因为 finally 中的内容必须保证执行，所以 try&#47;catch 执行完毕，即使得到的结果是非 normal 型的完成记录，也必须要执行 finally“ 吗</div>2019-10-26</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/WADWW2CpTUau6VakOsNXVtdoVaASQR7l1uKIDakINy8iaSibglv5Gjh67PdEAgXNVqzQrmRSrouaKZkJ8MQVVQsA/132" width="30px"><span>小say</span> 👍（6） 💬（1）<div>老师你好，前面说[[value]]如果没有返回值就是empty但是为什么在Chrome调试器下显示的是undefined？
后文中语句块中
{
  var i = 1; &#47;&#47; normal, empty, empty
  i ++; &#47;&#47; normal, 1, empty
  console.log(i) &#47;&#47;normal, undefined, empty
} &#47;&#47; normal, undefined, empty
其中 var i = 1; 为什么[[value]]会是empty？console.log(i)的[[value]]为什么是undefined？所以到底什么时候是empty什么时候是undefined？</div>2019-09-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/78/51/4790e13e.jpg" width="30px"><span>Smallfly</span> 👍（2） 💬（1）<div>winter 老师，有什么工具能查看 JS 引擎的运行时的特殊类型么？</div>2019-10-17</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqicfns3FdbrFmETHickC5xibHXhYmFOkNzK3AiaJRpwJLQMAszmpf7BQOvicwnMD0qdAYWG1K78pbxPAw/132" width="30px"><span>Puru</span> 👍（1） 💬（2）<div>Python 也是先执行finally后执行return</div>2019-06-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/1a/c3/02bb2ebe.jpg" width="30px"><span>尤璐洁</span> 👍（0） 💬（1）<div>winter老师，这些个私有属性的值执行时的值是如何得出的，是靠分析，还是说有某种方式可以看到验证呢？</div>2019-10-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/77/33/121176bb.jpg" width="30px"><span>东</span> 👍（0） 💬（3）<div>void function() {
	if(true){
		console.log(1)
		break
		console.log(2)
	}
}()
在if中用break、continue会报错VM506:4 Uncaught SyntaxError: Illegal break statement，而不是穿透，为什么和表格举出的不一致呢</div>2019-07-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/80/71/df2415a6.jpg" width="30px"><span>热爱减肥的胖子</span> 👍（0） 💬（1）<div>请问，上图上那个“特殊处理”怎么理解？</div>2019-06-26</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/3XbCueYYVWTiclv8T5tFpwiblOxLphvSZxL4ujMdqVMibZnOiaFK2C5nKRGv407iaAsrI0CDICYVQJtiaITzkjfjbvrQ/132" width="30px"><span>有铭</span> 👍（98） 💬（8）<div>很感兴趣这些高级特性的知识老师是从哪里学到的，我翻过js高级编程那本书都没讲到过这些</div>2019-03-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/c1/cc/6b6bbd41.jpg" width="30px"><span>周小成</span> 👍（88） 💬（3）<div>穿透和消费，报错应该是连贯的，“穿透”就是指不在当前这一层处理，向外逐层寻找可以“消费”的那一层，直到最后都没找到就报错，比如：function里面有while, while里面有switch, switch里面又有continue，按图表来看，switch-continue应该是穿透，向上层寻找消费，碰到while-contine,那就是消费，再如switch里面是return, switch-return穿透，向上层whlie-return穿透，最后function-return是消费。</div>2019-03-12</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/XSnxM4uP67kdzzCRW8KxhS5jkHiaaSrgkuLh1Z5BxawvQase46pbGAL4Bngmd3eFHckQml6zexyukFoWpeNENTg/132" width="30px"><span>Rushan-Chen</span> 👍（59） 💬（13）<div>请问老师，表格中的“穿透”和“消费”是什么意思？</div>2019-03-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/93/4a/de82f373.jpg" width="30px"><span>AICC</span> 👍（46） 💬（0）<div>3楼你好，我的理解是，消费指对应的代码被有效的执行了，穿透指对应代码被跳过了，也就是对应控制的语句体被有效执行比如try catch,当try中出现了throw,能被有效捕获进而执行catch，这在我理解就是try被消费执行了，而当catch中还有throw时，由于catch不具备处理throw的能力，于是catch被中断跳出，也就是作者所说的穿透，希望能帮到你</div>2019-03-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/59/86/0f9f81d5.jpg" width="30px"><span>加利率的钟摆</span> 👍（33） 💬（4）<div>```javascript
function test(){
  if(true){
    console.log(&quot;111&quot;);
    break;
  }
  if(true){
    console.log(&quot;222&quot;);
  }
}

test(); &#47;&#47; SyntaxError: Illegal break statement
```

我们可以这么分析：

1. if 和 break 相遇，break 穿透至 function
2. function 和 break 相遇，报错

```javascript
function test() {
  var a = 0;
  switch (a) {
    case 0:
      if (true) {
        console.log(&quot;111&quot;);
        break;
      }
  }

  if (true) {
    console.log(&quot;222&quot;);
  }
}

test();
&#47;&#47; 111
&#47;&#47; 222
```

我们可以这么分析：

1. if 和 break 相遇，break 穿透至 switch
2. swicth 和 break 相遇，消费掉 break
3. 接着执行之后的代码</div>2019-04-17</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83er9YqiaybDPpZMr3ecHDv8P3chyr3dETz5Ljft8s3F47JDN93yOKeOyysxxhaN7MJmXt7ib5X6EgMGQ/132" width="30px"><span>火云邪神0007</span> 👍（16） 💬（0）<div>老师在前面讲过，穿透就是去上一层的作用域或者控制语句找可以消费break，continue的执行环境，消费就是在这一层就执行了这个break或者continue</div>2019-03-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1d/d6/76fe5259.jpg" width="30px"><span>Dream.</span> 👍（15） 💬（1）<div>第一次看见『消费』与『穿透』这样的描述。

这两个词的来源自哪里呢？

结合表格中的控制语句组合使用得到的结果来看，我的理解是

『消费』是控制语句里的内容执行完毕。
『穿透』是控制语句里的内容没能执行完，被中止了。
</div>2019-03-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/57/6e/b6795c44.jpg" width="30px"><span>夜空中最亮的星</span> 👍（10） 💬（0）<div>老师，我昨天成功的把您的课推销出去了一份，哈哈😄高兴</div>2019-03-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4e/19/69f6e2ec.jpg" width="30px"><span>王大可</span> 👍（3） 💬（0）<div>配合周爱民老师的专栏食用效果更佳</div>2020-11-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/bb/01/568ac2d6.jpg" width="30px"><span>K4SHIFZ</span> 👍（3） 💬（1）<div>老师，请出一份ES标准解读。带着我们学一次。必买！</div>2019-03-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/db/26/54f2c164.jpg" width="30px"><span>靠人品去赢</span> 👍（3） 💬（0）<div>这个把completion称作一个类型，感觉有点怪，首先这个不是我们自己去定义的，这个是因为我们执行语句都会有这个东西。小白看到这个“类型”会往前找，发现没这个类型，之前掌握的的语言系统也没有相关的类型，结果就是“我擦，这是啥，ES6的新特性吗？”。关于这个，这是我在MDN上找的相关资料，希望大家指点一下（看run-to-completion这部分）https:&#47;&#47;developer.mozilla.org&#47;en-US&#47;docs&#47;Web&#47;JavaScript&#47;EventLoop
</div>2019-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/44/9a/c03bea17.jpg" width="30px"><span>金子菇凉的铁粉小逗</span> 👍（3） 💬（0）<div>Completion 类型是个神马鬼？</div>2019-03-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/f7/a6/0b590c34.jpg" width="30px"><span>心平气和的韩丽媛</span> 👍（2） 💬（0）<div>老师基本不在评论区答疑是不太理解的，因为大家提出了问题，就是对课程内容有疑问，半天得不到解答，搞来搞去疑问更多</div>2020-12-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/05/93/3c3f2a6d.jpg" width="30px"><span>安石</span> 👍（2） 💬（0）<div>结合下面的评论，我的理解是，消费就是:比如说for循环里面，continue或者break起作用，就是上文提到的completion type 非normal的情况，命中了。穿透就是这个语句架子太大了(县官审理亲王？)让外层的语句（总之上报上级吧一层层的报）来处理。</div>2020-11-06</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/s0bx4WXQNkAJ3c3map0g6dlt3sKDgTtN7Ria96YoufjQcVVI8Shv5CN1jnK1ZTImNnlPcibRqvyiaUuhpIvV1TpnQ/132" width="30px"><span>wingsico</span> 👍（2） 💬（0）<div>在导语中就特意去了解了completion record(下文简称cr)的具体含义，但仅了解到cr的组成和各种语句对应的cr，但没有实际了解到cr的作用。在这篇文章后，了解了cr的实际作用: 与js的树形嵌套结构结合，对各种分支循环执行相应的逻辑。不同的非normal cr会穿透不同的语句和被不同的语句消费，穿透的实际表示是将整个语句(块)变为相应的cr，消费则是在当前语句(块)内产生作用，并且阻止其继续穿透(整个语句不会变为相应的cr)。第三个参数target则是指定消费该cr的对象，通过js中的标签语法来指定，一般用于跳出外层循环体。

通过这次学习，从原来现象了解到如今的本质实现和其作用机理，了解到现象背后的原因。

对于题中的finally问题则是cr和finally的作用方式相结合的结果。finally的必执行加上非normal cr的穿透综合得到的结果。以后对于类似的问题则可以举一反三的解释其背后的原因。</div>2020-04-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1d/7d/368df396.jpg" width="30px"><span>somenzz</span> 👍（2） 💬（0）<div>Python的try finally也是这样的，我想知道有语言不是这样的吗？</div>2019-10-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/7e/fc/53ce9019.jpg" width="30px"><span>孤单听雨的猫</span> 👍（2） 💬（0）<div>标准 https:&#47;&#47;tc39.github.io&#47;ecma262&#47;</div>2019-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/40/67/2f477947.jpg" width="30px"><span>宝贝爱学习</span> 👍（2） 💬（1）<div>try finally 那个跟Java不是一样的吗</div>2019-04-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/80/a5/1a9921de.jpg" width="30px"><span>稚鸿同学</span> 👍（1） 💬（0）<div>理解【消费】和【穿透】，从使用经验来说，消费在语句里面直接了当，完全终止；穿透就是悠游寡断，欲断未断的意思；</div>2019-10-17</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJayib1ZcRfOaoLsdsWZokiaO5tLAdC4uNAicQJRIVXrz9fIchib7QwXibnRrsJaoh5TUlia7faUf36g8Bw/132" width="30px"><span>明月</span> 👍（1） 💬（0）<div>我理解的穿透或者消费是break continue return thow对if等的影响范围 如果能影响到if层级之外就是穿透 如果是只影响if语句就是消费 </div>2019-08-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/18/64/00d7e8ab.jpg" width="30px"><span>守候</span> 👍（1） 💬（0）<div>学到了</div>2019-03-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/35/d0/f2ac6d91.jpg" width="30px"><span>阿成</span> 👍（1） 💬（1）<div>涨姿势啦
不过，从来没用过label...
甚至第一次知道js里没有goto...</div>2019-03-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/0a/83/f916f903.jpg" width="30px"><span>风</span> 👍（0） 💬（0）<div>要做过脚本引擎或者编译器，才会知道这节课在讲什么。实现语句控制，ecma这里的completion record 只是一种最佳实践而已</div>2021-12-23</li><br/>
</ul>