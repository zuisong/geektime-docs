你好，我是石川。

上节课里，我们在学习组合和管道的工作机制的时候，第一次认识了reducer，同时在讲到transduce的时候，也接触到了map、filter和reduce这些概念。那么今天这节课，我们就通过JS中数组自带的功能方法，来进一步了解下transduce的原理，做到既知其然，又知其所以然。

另外，我们也看看由map作为functor可以引申出的monad的概念，看看它是如何让函数间更好地进行交互的。

## 数据的核心操作

那在正式开始之前，我先来说明下这节课你要关注的重点。课程中，我会先带你通过JavaScript本身自带的映射（map）、过滤（filter）和reduce方法，来了解下这几种方法对值的核心操作。同时呢，我也给你解答下上节课提出的问题，即如何通过映射和过滤来做到reduce。**作为我们后面讲到functor和monad的基础。**

好，下面我们就从map开始讲起。

### map映射和函子

我们经常听说，array.map就是一个函子（functor），那什么是一个函子呢？

实际上，**函子是一个带运算工具的数据类型或数据结构值**。举个常用的例子，在JavaScript中，字符串（string）就是一个数据类型，而数组（array）既是一个数据类型也是一个数据结构，我们可以用字符串来表达一个单词或句子。而如果我们想让下图中的每个字母都变成大写，那么就是一个转换和映射的过程。
<div><strong>精选留言（8）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/13/e8/24/a75dae31.jpg" width="30px"><span>思文</span> 👍（4） 💬（4）<div>单子、函子这些感念看完还是有些陌生，有什么办法深入理解下吗，比如需要看那些文章等等</div>2022-10-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/b4/16/f3c36fd8.jpg" width="30px"><span>Yum.X</span> 👍（1） 💬（3）<div>
function Just(val) {
    return { map };

    function map(fn) { return Just( fn( val ) ); }

}
var A = Just( 10 );
var B = A.map( v =&gt; v * 2 ); &#47;&#47; 20

运行了这段代码，这里回的不是20</div>2022-10-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/0a/40/cf70b198.jpg" width="30px"><span>lin</span> 👍（0） 💬（1）<div>ap 这里我还是不太理解。根据 exp：
、、、
const a = Just(1); &#47;&#47; Just(1)
const b = Just(2); &#47;&#47; Just(2)
const c = a.map(addFive); &#47;&#47; Just(6)

c.ap(b); &#47;&#47; Error: Just(6(2)) -&gt; 6 is not a function
、、、

这里的调用应该会出现问题。</div>2022-12-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/30/cd/d2/f9528a87.jpg" width="30px"><span>朱基</span> 👍（0） 💬（1）<div>在“reduce 和缩减器”这一节的课程里，突然显示了一代码示例，var getSessionId = partial( prop, &quot;sessId&quot; );…if (orders != null) processOrders( orders ); 它是用来说明上面所说的：“我们没有必要为了几乎没有负面影响的副作用—改变了原数据，而牺牲性能”的吗？</div>2022-11-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/33/23/1b8acb62.jpg" width="30px"><span>李滨</span> 👍（0） 💬（2）<div>array 作为 functor 小节下面的那个例子 : Just return 的map函数的定义不对吧 ，map应该直接返回 fn(val)吧？ </div>2022-10-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/0c/4d/90ab20d8.jpg" width="30px"><span>Nuvole Bianche</span> 👍（1） 💬（0）<div>function Just(val) {
  return { map, log };

  function map(fn) {
    return Just(fn(val));
  }

  function log() {
    return `Just(${val})`;
  }
}

var A = Just(10);

var B = A.map((v) =&gt; v * 2); &#47;&#47; 20
console.log(B.log());   &#47;&#47; Just(20)
console.log(A.log());   &#47;&#47; Just(10)


反复看后，注意到这里其实生成了两个闭包，一个是针对A的闭包这时val是10，二针对B的闭包中val存放的是20。作为小白的知道这种写法非常nobility，但现阶段的我完全不知道这种写法的具体使用场景。</div>2023-01-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/6f/10/bfbf81dc.jpg" width="30px"><span>海绵薇薇</span> 👍（1） 💬（0）<div>“而缩减 reduce 除了能独立来实现以外，也可以用映射 map 和过滤 filter 的方法来实现。&quot;

这句话是不是反了🤣，”map和filter除了能独立实现以外，也可以用reduce的方法来实现。“还是我理解的有点问题🤣。</div>2023-01-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/83/52/d67f276d.jpg" width="30px"><span>轩爷</span> 👍（0） 💬（0）<div>function Just(val) {
    return { map };
    function map(fn) { return fn( val ) ; }
}
var A = Just( 10 );
var B = A.map( v =&gt; v * 2 );  &#47;&#47; 20

function Just(val) { 
  return { map }; 
  function map(fn) { return Just( fn( val ) ); }
}

var A = Just( 10 );
var B = A.map( v =&gt; v * 2 );  &#47;&#47; { map: f} </div>2023-02-10</li><br/>
</ul>