你好，我是蒋宏伟。

那么这一讲，我们来讲搭建页面的第二步，让页面“动”起来，这里的“动”说的是在不同场景下，让页面展示出不同的内容。

怎么让页面“动”起来呢？这就要用到状态 State 了。

一个页面也好，一个应用也好，只有把状态设计清楚了，程序才能写得好。讲到状态，有些人可能会说，状态不就是页面中那些会“动”的数据吗？这很简单，还有什么好讲的。

这没错，状态确实是页面中会“动”的数据，但是要把状态用好不容易，有时候容易把状态设计复杂了，不仅代码要写得更多，还容易导致程序维护起来更麻烦。

这次，我会以搭建一个会“动”的简易购物车页面为例，和你分享下我在这方面的经验。简易购物车页面是这样的：

![图片](https://static001.geekbang.org/resource/image/dd/9e/dd69765bb8fcb1f9dffyy2df4d2b789e.png?wh=1000x784)

它比上一讲的商品表单页多了一些交互，它的所有数据都是从网络请求过来的，这些数据包括商品名称、商品价格、商品数量，数据从网络请求回来后会展示在页面上。你可以点击页面中的加号或减号，来添加数量或减少商品数量，底部的结算总价会随着商品数量的变化而变化。

要实现这个简易购物车的静态很简单，它只包括两个组件，商品表单组件 ProductTable 和商品组件 ProductRow。完成静态页面的搭建后，接下来就**要让页面“动”起来了**，我把这个过程分成了 4 步来实现，状态初选、状态确定、状态声明、状态更新。
<div><strong>精选留言（19）</strong></div><ul>
<li><img src="" width="30px"><span>beetcb</span> 👍（0） 💬（1）<div>感谢老师推荐！我自己也去学习了 beta 文档，状态管理那章写得真好，除了有本文中提到的方法，还把 useState useReducer Context 都串起来啦，非常清晰。</div>2022-04-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/ca/af/8e93c68c.jpg" width="30px"><span>Le vent se lève</span> 👍（0） 💬（1）<div>终于运行起来了</div>2022-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/ca/af/8e93c68c.jpg" width="30px"><span>Le vent se lève</span> 👍（0） 💬（1）<div>老师我想问下productTable。tsx文件里边的fetch请求第二个then中products: Products，这个Products是什么意思呢？可以帮我分析下吗没太看懂？
</div>2022-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/e9/58/7bb2c561.jpg" width="30px"><span>请务必优秀</span> 👍（0） 💬（1）<div>interface声明方式在jsx文件怎么生效呢
</div>2022-04-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/e9/58/7bb2c561.jpg" width="30px"><span>请务必优秀</span> 👍（0） 💬（2）<div>fetch(&#39;https:&#47;&#47;61c48e65f1af4a0017d9966d.mockapi.io&#47;products&#39;)这个接口没有怎么模拟呢</div>2022-04-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/36/d6/343ab8c7.jpg" width="30px"><span>Asterisk</span> 👍（4） 💬（0）<div>讲的也有点太简单了，能不能把关键的地方，或者容易入坑的地方好好讲讲。至于基础知识这个官网讲的就挺好了。</div>2022-10-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/ea/a9/0a917f2c.jpg" width="30px"><span>Sunny</span> 👍（2） 💬（5）<div>export default function ProductTable() {
    &#47;&#47; ...
}
请教一下，这也是声明组件么 ？为什么不用 class 声明 ？</div>2022-04-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/48/4e/ff28a022.jpg" width="30px"><span>江左小海</span> 👍（1） 💬（3）<div>为什么有jsx，tsx，不都是JS吗，Android开发，对这一块不懂，这个项目也运行不起来，第一个ProductTabled的id找不到，删除后，又说ProductRow没有引入</div>2022-07-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/d7/f5/df6b6b60.jpg" width="30px"><span>angelajing</span> 👍（0） 💬（0）<div>github能否添加一个readme.md文件，详细介绍下怎样执行每个示例的代码。因为是初学者，对Android studio的run配置和npm、npx react-native命令行都不太熟悉。</div>2023-11-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/97/ca/1297b401.jpg" width="30px"><span>左手指月</span> 👍（0） 💬（0）<div>countObject.num === countObject.num &#47;&#47; false

真的没问题么，复制到浏览器是true耶</div>2023-08-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a7/98/1491b4a3.jpg" width="30px"><span>kittyE</span> 👍（0） 💬（0）<div>声明一个3*3的二维数据或者9位的一维数组，循环数组渲染</div>2023-07-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/37/17/ebb55b28.jpg" width="30px"><span>简之语</span> 👍（0） 💬（0）<div>此次细看真的是行云流水一般通畅的文章，信息密度还不低，👍</div>2023-07-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/49/a9/225c041f.jpg" width="30px"><span>陈彦祖</span> 👍（0） 💬（0）<div>井字棋只需要一个状态用于记录棋盘内容即可。需要可读性的好就是一个 3×3 的数组，也可以用一个一维数组来表示。一维数组在计算的时候麻烦一些。例如：
let chessStatus: number[] = [1,null,0,null,null,null,null,null,null]
1. 从左至右，从上到下分别对应数组索引 0~8
2. 数组元素 1 表示 X 在这个位子落子，0 表示圈在这个位子落子；null 表示该位置没有落子


</div>2023-04-27</li><br/><li><img src="" width="30px"><span>Geek_7831b0</span> 👍（0） 💬（0）<div>接口似乎失效了，有人能给个example json吗？</div>2022-10-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/e7/35/ba2cc0d7.jpg" width="30px"><span>王昭策</span> 👍（0） 💬（0）<div>老师能不能讲一下作业啊？光布置不讲我也不知道自己想法对不对。
</div>2022-10-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/fa/ea/344d0f73.jpg" width="30px"><span>叶子</span> 👍（0） 💬（1）<div>个人感觉2个状态，一个用来记录9个格子的内容（比如数组，按序号位置填值，那个用户下在哪里就把数组对应位置值写入用户的名字），还有一个用来记录游戏的状态（开始状态；位置重复状态；获胜状态：有人站的位置达到三个且符合获胜的排列组合（组合用枚举来提前准备好）；平手：所有位置下满但无人获胜）</div>2022-08-28</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKTcgPkeGEEYks7Kgd1zstn9rFjsXfDLwRLTfEIXh5TZtU9yIeibBXIsFQAbFxlGPUI0ZqptrDOPOA/132" width="30px"><span>Geek_bb718b</span> 👍（0） 💬（1）<div>关于为什么Hooks不能在if else 里使用，还是没太理解</div>2022-08-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2e/10/bd/aafba045.jpg" width="30px"><span>Geek_874d38</span> 👍（0） 💬（1）<div>项目代码不匹配，请重新上传代码，谢谢！</div>2022-06-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/60/a1/45ffdca3.jpg" width="30px"><span>静心</span> 👍（0） 💬（0）<div>不错不错👍讲的挺明白</div>2022-05-27</li><br/>
</ul>