你好，我是宫文学。

Julia这门语言，其实是最近几年才逐渐获得人们越来越多的关注的。有些人会拿它跟Python进行比较，认为Julia已经成为了Python的劲敌，甚至还有人觉得它在未来可能会取代Python的地位。虽然这样的说法可能是有点夸张了，不过Julia确实是有它的可取之处的。

为什么这么说呢？前面我们已经研究了Java、Python和JavaScript这几门主流语言的编译器，这几门语言都是很有代表性的：Java语言是静态类型的、编译型的语言；Python语言是动态类型的、解释型的语言；JavaScript是动态类型的语言，但可以即时编译成本地代码来执行。

而Julia语言却声称同时兼具了静态编译型和动态解释型语言的优点：**一方面它的性能很高，可以跟Java和C语言媲美；而另一方面，它又是动态类型的，编写程序时不需要指定类型。**一般来说，我们很难能期望一门语言同时具有动态类型和静态类型语言的优点的，那么Julia又是如何实现这一切的呢？

原来它是充分利用了LLVM来实现即时编译的功能。因为LLVM是Clang、Rust、Swift等很多语言所采用的后端工具，所以我们可以借助Julia语言的编译器，来研究如何恰当地利用LLVM。不过，Julia使用LLVM的方法很有创造性，使得它可以同时具备这两类语言的优点。我将在这一讲中给你揭秘。
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="" width="30px"><span>myrfy</span> 👍（5） 💬（1）<div>从速度角度考虑，julia的编译应该是AOT的，可以在编译期多花时间，来换取执行期的速度，而v8是jit，要保证运行流畅，不能花太多时间。
从jit的角度分析，如果依赖统计数据确定了某一变量的类型，则该变量类型变动的概率很低，为小概率的事件再生成一套机器码不划算
从内存占用角度，生成更多的版本意味着占用更多内存，而v8的主要使用场景，浏览器，对资源的限制是比较严格的。</div>2020-07-22</li><br/><li><img src="" width="30px"><span>minghu6</span> 👍（1） 💬（1）<div>julia设计得不错, 一个它一个Rust基本上是我比较欣赏的21世纪10年代以后的新生语言, 文中提到的函数分发作为面向对象里重载的实现,好像最初的面向对象smalltalk就是这种风格,只不过后来一系列像C++这种所谓静态类型的指令型的面向对象把路给带偏了.

另外一个scheme风格的宏我以前很喜欢,极客风很酷, 但现在我认为还是基于Pattern match的用ALGOL风格的宏更好一点,原因就是编写得效率高,易读易维护.(就比如在那个我的demo项目里面用几十分钟(包括查资料)写的解析生成式的宏我之前用Hy(sheme风格)来试着写过,那简直是time-consumer,一晃几天过去了还在写底层的机制呢)</div>2021-06-16</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJOBwR7MCVqwZbPA5RQ2mjUjd571jUXUcBCE7lY5vSMibWn8D5S4PzDZMaAhRPdnRBqYbVOBTJibhJg/132" width="30px"><span>ヾ(◍°∇°◍)ﾉﾞ</span> 👍（1） 💬（1）<div>老师，很多语言都声称使用llvm提升性能，但是在lua领域好像一直是luajit无法超越</div>2020-07-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2e/28/fc/cf7b476f.jpg" width="30px"><span>常新CXIN</span> 👍（1） 💬（0）<div>老师，Julia的动态分派性能和Rust以及C++的运行时多态对比怎么样呢？</div>2022-06-12</li><br/><li><img src="" width="30px"><span>Geek_5c11cd</span> 👍（0） 💬（0）<div>&quot;flisp 解析器并不是一个经典的递归下降解析器，因为它经常回顾并修改它已经生成的输出树&quot;</div>2022-12-04</li><br/>
</ul>