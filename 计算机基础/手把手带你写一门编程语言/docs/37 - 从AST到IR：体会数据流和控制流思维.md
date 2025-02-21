你好，我是宫文学。

在上一节课，我们已经初步认识了基于图的IR。那接下来，我们就直接动手来实现它，这需要我们修改之前的编译程序，基于AST来生成IR，然后再基于IR生成汇编代码。

过去，我们语言的编译器只有前端和后端。加上这种中间的IR来过渡以后，我们就可以基于这个IR添加很多优化算法，形成编译器的中端。这样，我们编译器的结构也就更加完整了。

今天这节课，我先带你熟悉这个IR，让你能够以数据流和控制流的思维模式来理解程序的运行逻辑。之后，我还会带你设计IR的数据结构，并介绍HIR、MIR和LIR的概念。最后，我们再来讨论如何基于AST生成IR，从而为基于IR做优化、生成汇编代码做好铺垫。

首先，我还是以上一节课的示例程序为础，介绍一下程序是如何基于这个IR来运行的，加深你对控制流和数据流的理解。

## 理解基于图的运行逻辑

下面是上节课用到的示例程序，一个带有if语句的函数，它能够比较充分地展示数据流和控制流的特点：

```plain
  function foo(a:number, b:number):number{
    let x:number;
    if (a>10){
      x = a + b;
    }
    else{
      x = a - b;
    }
    return x;
  }
```

我们把这个程序转化成图，是这样的：
<div><strong>精选留言（6）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡</div>2022-10-01</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIicr82CnrdEjibibAvyeKRQHszSzIAqoCWxN0kqC442XcjEae6S9j6NDtKLpg4Da4CUQQeUFUicWqiaDw/132" width="30px"><span>有学识的兔子</span> 👍（0） 💬（0）<div>HIR 贴近源码，会基于SSA进行格式化； LIR 接近汇编的一种表达；MIR介于两者之间，与硬件尽量无关； 因此问题对应的顺序是HIR，MIR，LIR。</div>2021-11-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/7f/24/ceab0e7b.jpg" width="30px"><span>奋斗的蜗牛</span> 👍（0） 💬（1）<div>老师，节点之海和DAG是指同一种IR吗</div>2021-11-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/7f/24/ceab0e7b.jpg" width="30px"><span>奋斗的蜗牛</span> 👍（0） 💬（0）<div>场景1是HIR，场景2是MIR，场景3是LIR</div>2021-11-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/7f/24/ceab0e7b.jpg" width="30px"><span>奋斗的蜗牛</span> 👍（0） 💬（0）<div>厉害，老师的水平真高，编译原理到老师的手里，信手拈来</div>2021-11-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/7f/24/ceab0e7b.jpg" width="30px"><span>奋斗的蜗牛</span> 👍（0） 💬（0）<div>太赞了，感觉一下子茅塞顿开</div>2021-11-08</li><br/>
</ul>