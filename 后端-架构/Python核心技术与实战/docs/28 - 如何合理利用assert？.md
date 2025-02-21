你好，我是景霄。

相信你平时在写代码时，肯定或多或少看到过assert的存在。我也曾在日常的code review中，被一些同事要求增加assert语句，让代码更加健壮。

不过，尽管如此，我发现在很多情况下，assert还是很容易被忽略，人们似乎对这么一个“不起眼”的东西并不关心。但事实上，这个看似“不起眼”的东西，如果能用好，对我们的程序大有裨益。

说了这么多，那么究竟什么是assert，我们又该如何合理地使用assert呢？今天这节课，我就带你一起来学习它的用法。

## 什么是assert？

Python的assert语句，可以说是一个debug的好工具，主要用于测试一个条件是否满足。如果测试的条件满足，则什么也不做，相当于执行了pass语句；如果测试条件不满足，便会抛出异常AssertionError，并返回具体的错误信息（optional）。

它的具体语法是下面这样的：

```
assert_stmt ::=  "assert" expression ["," expression]
```

我们先来看一个简单形式的`assert expression`，比如下面这个例子：

```
assert 1 == 2
```

它就相当于下面这两行代码：

```
if __debug__:
    if not expression: raise AssertionError
```

再来看`assert expression1, expression2`的形式，比如下面这个例子：
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/6f/9e/951afb1f.jpg" width="30px"><span>更好的做自己</span> 👍（79） 💬（3）<div>个人认为assert的使用应该是，有没有assert程序都能够正常运行，但有了assert可以使我们的代码后期维护更加方便</div>2019-07-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/30/29/d6816ebf.jpg" width="30px"><span>小侠龙旋风</span> 👍（13） 💬（1）<div>印象中好像就这个用法比较常用一点：
assert isinstance(input, list), &#39;input must be type of list&#39;</div>2019-07-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/99/27/47aa9dea.jpg" width="30px"><span>阿卡牛</span> 👍（9） 💬（3）<div>正式上线时也建议用assert??</div>2019-07-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/9a/12/06863960.jpg" width="30px"><span>稳</span> 👍（3） 💬（1）<div>我记得以前看过assert会严重影响运行性能，所以一直不在代码里用。工作中，主要是单元测试用，想跟老师了解fb的规定</div>2019-07-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/e8/cf/554f08f9.jpg" width="30px"><span>梁大瓜</span> 👍（12） 💬（0）<div>我记得最早写机器学习代码的时候，assert用来检查输入。</div>2019-08-07</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/DYAIOgq83eppQqDE6TNibvr3DNdxG323AruicIgWo5DpVr6U7yZVNkbF2rKluyDfhdpgAEcYEOZTAnbrMdTzFkUw/0" width="30px"><span>图·美克尔</span> 👍（9） 💬（0）<div>写测试代码时用</div>2019-07-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/0e/d9/e61ce097.jpg" width="30px"><span>郭纯</span> 👍（9） 💬（0）<div>怎么确定使用还是不使用 assert 首先确定这段代码是否有出现错误的可能 然后再确定删除 assert 代码会不会影响到原有的逻辑. assert 不应该用到业务的逻辑代码中 更多的是参数的检查，一段算法结果的验证. </div>2020-10-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/9a/6b/e8ef2989.jpg" width="30px"><span>云蝈蝈</span> 👍（5） 💬（4）<div>学习assert的时候用过</div>2020-08-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/7c/8a/bdeb76ac.jpg" width="30px"><span>Fergus</span> 👍（4） 💬（0）<div>assert 测试一个条件是否满足

检查值在某一确定的范围：
assert a&gt;0, “a must &gt; 0”

检查值的数据类型：
assert isinstance(a, list), “a should be list”

注：
1. assert 是可以使用-O关闭的；
2. run-time error需要使用try-except异常处理；</div>2019-07-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/5b/08/b0b0db05.jpg" width="30px"><span>丁丁历险记</span> 👍（3） 💬（0）<div>个人理解，assert 主要是做健壮性处理。</div>2019-10-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/41/83/a6263932.jpg" width="30px"><span>倾</span> 👍（3） 💬（0）<div>一般不怎么用，全部使用异常处理的。</div>2019-07-15</li><br/><li><img src="" width="30px"><span>Ray</span> 👍（2） 💬（0）<div>之前在一个C++程序中用过assert语句，记得好像是在一个FTP下载模块中。后来很长时间没啥问题后也忘了，然后有一阵程序偶尔异常退出，查了半天发现是assert条件原因，最后发现原来是交换机出问题了时好时坏。</div>2020-03-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/8a/bc/cb39ed38.jpg" width="30px"><span>自由民</span> 👍（2） 💬（2）<div>在c++里用过，用得不多。Python里没用过。</div>2019-10-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/47/71/4fdb52bc.jpg" width="30px"><span>Eski</span> 👍（2） 💬（0）<div>经常在 try except 当中用 assert，比较方便在一些不需要程序继续执行下去的地方跳出来，比if else好用</div>2019-07-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/3c/1b/c0/e59d530a.jpg" width="30px"><span>D.mc</span> 👍（0） 💬（0）<div>读下来认为是这样：
1.try-except, 用于处理可能有多种异常的情况
2.if-else, 用于处理多种情况，但不同情况都可能合理的情况
3.assert, 则只能用于处理一种特定的情况，当要特定地确认某个情况是否发生时；或者说，一般只用于增强健壮性</div>2025-01-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0a/a4/828a431f.jpg" width="30px"><span>张申傲</span> 👍（0） 💬（0）<div>第28讲打卡~</div>2024-06-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2d/48/18/e524f344.jpg" width="30px"><span>Soyoger</span> 👍（1） 💬（0）<div>业务代码确实很少用，但在测试的时候用的比较多。</div>2022-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/7d/41/3c5b770b.jpg" width="30px"><span>喵喵喵</span> 👍（0） 💬（0）<div>打卡～</div>2020-02-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/49/71/fc2b5cf2.jpg" width="30px"><span>隔壁家老鲍</span> 👍（0） 💬（0）<div>一般都在测试里面使用
没有在正式环境里面使用过</div>2019-12-16</li><br/><li><img src="" width="30px"><span>Paul Shan</span> 👍（0） 💬（0）<div>Assert 是正常逻辑之外的自检，只是写在代码里面多少有些让代码主体不清。</div>2019-11-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/a5/98/a65ff31a.jpg" width="30px"><span>djfhchdh</span> 👍（0） 💬（0）<div>一般来说，测试代码最后一步都是assert</div>2019-09-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/1c/01/5aaaf5b6.jpg" width="30px"><span>Ben</span> 👍（0） 💬（0）<div>python -V: Python 3.7.0
Python test.py -O时__debug__仍为True, Python -O test.py时为False</div>2019-07-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/d7/39/6698b6a9.jpg" width="30px"><span>Hector</span> 👍（0） 💬（0）<div>项目中封装自己公司封装定义的expection，接口给出展示不同错误不会混用</div>2019-07-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fe/44/3e3040ac.jpg" width="30px"><span>程序员人生</span> 👍（0） 💬（0）<div>老师，没有用过assert唉。看你介绍，好像用来调试程序用</div>2019-07-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/91/6c/054a0745.jpg" width="30px"><span>carpe_diem</span> 👍（0） 💬（0）<div>assert主要用于开发和测试阶段，使用assert时，应该是思考一下，当去掉assert语句之后，代码逻辑是否仍然正确。</div>2019-07-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/56/11/5d113d5c.jpg" width="30px"><span>天凉好个秋</span> 👍（0） 💬（0）<div>感觉只要可以disable，那还是需要对相同问题加入if判断啊。是否是像其他同学说的自测阶段才能用assert呢？并且对于可能出现的相同问题需要用assert写一遍，再用if写一遍？</div>2019-07-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/43/2d/af86d73f.jpg" width="30px"><span>enjoylearning</span> 👍（0） 💬（2）<div>assert想用但不确信什么情况下用，一直以为python没法做debug判断，原来也有个类似，我们线上经常出现一些诡异的bug，不知道可不可以开启这个</div>2019-07-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/39/fa/a7edbc72.jpg" width="30px"><span>安排</span> 👍（0） 💬（0）<div>自测阶段才能用assert吧？上线长时间运行的程序都会disable掉assert吧？</div>2019-07-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a5/67/bf286335.jpg" width="30px"><span>AllenGFLiu</span> 👍（0） 💬（0）<div>以前看其他课程，倒是都没讲过 assert这一点，看下来觉得assert还是大有用武之地的，一定找机会用一下。</div>2019-07-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/09/42/1f762b72.jpg" width="30px"><span>Hurt</span> 👍（0） 💬（0）<div>可以这么理解吗 只是用来作为自我检查 而不是用来做你代码的判断条件的</div>2019-07-12</li><br/>
</ul>