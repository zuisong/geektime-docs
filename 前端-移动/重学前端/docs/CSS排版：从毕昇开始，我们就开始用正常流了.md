你好，我是winter。今天我们来聊聊CSS的正常流。

我想，在CSS中，大家最讨厌的大概就是排版部分了。因为早年的CSS设计上不能够很好地支持软件排版需求，导致大家需要使用很多黑科技，让很多新人望而却步。

现在CSS提供了很多种排版方式，我们有很多选项可以选择自己适合的那一种，然而，正常流却是我们绕不开的一种排版。

我们能够在网上看到关于正常流的各种资料，比如：块级格式化上下文、margin折叠等等……这一系列的概念光是听起来就令人非常头痛。

所以我相信很多同学一定会奇怪：正常流到底正常在哪里。事实上，我认为正常流本身是简单和符合直觉的东西。

我们之所以会觉得它奇怪，是因为如果我们从严苛的CSS标准角度去理解正常流，规定排版的算法，就需要引入上述那些复杂的概念。但是，如果我们单纯地从感性认知的层面去理解正常流，它其实是简单的。

下面，就让我们先抛弃掉所有的已知概念，从感性认知的角度出发，一起去理解一下正常流。

## 正常流的行为

首先，我们先从词源来讲一讲排版这件事。

在毕昇发明活字印刷之前，排版这项工作是不存在的，相应的操作叫做“雕版”。人们要想印刷书籍，就需要依靠雕版工人去手工雕刻印版。

活字印刷的出现，将排版这个词引入进来，排版是活字印刷的15道工序之一，不论是古代的木质活字印刷，还是近代的铅质活字印刷，排版的过程是由排版工人一个字一个字从字架捡出，再排入版框中。实际上，这个过程就是一个流式处理的过程。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/15/05/48/a62045cb.jpg" width="30px"><span>芝草晟林💦</span> 👍（0） 💬（1）<div>感觉 formatting那一段有点难理解...</div>2019-07-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/f9/bc/cbc0207b.jpg" width="30px"><span>Scorpio</span> 👍（112） 💬（5）<div>我大flex天下第一！！！😂 </div>2019-03-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/93/4a/de82f373.jpg" width="30px"><span>AICC</span> 👍（56） 💬（1）<div>试了一下，发现上面第二个例子的代码并不能实现想要的效果
首先，因为hmtl代码的换行使得在inline-block的布局下两个盒子不能被放在一行这个通过父级font-size:0可解决
第二，由于auto在html的上的顺序是比fixed后面的，想像中的层级是高于fixed的，当auto是一个有背景的盒子，fixed就被完全遮挡了,可以通过transform：translateZ(0)把它提起来</div>2019-03-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f1/15/8fcf8038.jpg" width="30px"><span>William</span> 👍（17） 💬（2）<div>1. 等宽布局，不用外层font-size:0的方法的话，应该是.inner:not(last-child) {
  margin-right: -5px;
}吧，前面元素均添加一个负外边距抵消掉空格大小。
2. 因为也是用inline-block，所以自适应宽需要加上
.outer {
  font-size: 0;
}</div>2019-03-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/35/d0/f2ac6d91.jpg" width="30px"><span>阿成</span> 👍（15） 💬（2）<div>Sir, have a look at this...
https:&#47;&#47;github.com&#47;aimergenge&#47;inline-block-layout</div>2019-03-16</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/ZgSq766pXNp6mZsW4Q6XBHy4sXFfZVwbrdOnLiavtIqodRkm2GL970vibJ2xA8wZmPvdwwOIPt9kDV3b6BSPVz7Q/132" width="30px"><span>ycswaves</span> 👍（10） 💬（0）<div>.auto {
  width: calc(100% - 200px);
  &#47;&#47; ... rest of the necessary styles
}</div>2019-03-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/00/d6/3eff7492.jpg" width="30px"><span>王天狗</span> 👍（7） 💬（0）<div>为什么不用 calc 呢</div>2020-01-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/17/63/241cb09b.jpg" width="30px"><span>我要飞</span> 👍（7） 💬（0）<div>一个元素规定了自身周围至少需要的空间,这个解释深有体会,无可挑剔啊
</div>2019-05-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/f8/f6/3e2db176.jpg" width="30px"><span>七月有风</span> 👍（7） 💬（1）<div>在 CSS 标准中，规定了如何排布每一个文字或者盒的算法，这个算法依赖一个排版的“当前状态”，CSS 把这个当前状态称为“格式化上下文（formatting context）”。
还是没有理解这句话</div>2019-03-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b8/11/26838646.jpg" width="30px"><span>彧豪</span> 👍（7） 💬（0）<div>grid写大的整体的布局框架，flex写一维的可线性化的布局，这两种布局的兼容性已经更好了，再加上一些模块和脚手架打包的时候能自动为你添加浏览器前缀，布局变得越来越容易了</div>2019-03-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/c9/96/4577c1ef.jpg" width="30px"><span>沉默的话唠</span> 👍（4） 💬（2）<div>为什么我写后面的完整版的，不会自动排布，宽度总是不够。被撑下去了。</div>2019-03-20</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/3XbCueYYVWTiclv8T5tFpwiblOxLphvSZxL4ujMdqVMibZnOiaFK2C5nKRGv407iaAsrI0CDICYVQJtiaITzkjfjbvrQ/132" width="30px"><span>有铭</span> 👍（3） 💬（1）<div>为什么三栏平分的那个样式里，给 outer 添加一个特定宽度和给最后一个 div 加上一个负的右 margin，我用chrome试验的结果，是变成了3个宽度很窄的盒子，而且第三个盒子在第二排？</div>2019-03-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/a4/ac/fc9e3981.jpg" width="30px"><span>梧桐</span> 👍（2） 💬（1）<div>给 outer 添加一个特定宽度， 没有看到什么实际效果啊，下面这段代码还是会换行。

.outer {
    width:101px
}

.inner {
    width:33.33%;
    height:300px;
    display:inline-block;
    outline:solid 1px blue;
}

.inner:last-child {
    margin-right:-5px;
}</div>2020-01-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/b6/a9/bdf6f6cd.jpg" width="30px"><span>Sticker</span> 👍（2） 💬（0）<div>感觉自适应宽还是浮动更爽一点！</div>2019-04-30</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/EJZoM46wR6QqTeibhPZsO5wJTeUia4RndGicWfDZLw153WibjsnJXqEtGZICxAa8icb36pDkficTic3FViaySd1z9HmQBw/132" width="30px"><span>翰弟</span> 👍（2） 💬（0）<div>日拱一卒</div>2019-03-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/72/fc/6a799bc4.jpg" width="30px"><span>C阳</span> 👍（2） 💬（0）<div>自适应宽例子中，是否应该在.fixed, .auto中加入float:left才能正确显示效果呢？</div>2019-03-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/6e/b9/9d5aad7a.jpg" width="30px"><span>雨落下的声音</span> 👍（1） 💬（0）<div>第二个实现：
.fixed, .auto {
            height: 300px;
            outline: solid 1px blue;
        }

        .fixed {
            width: 200px;
            display: inline-block;
            vertical-align: top;
        }

        .auto {
            margin-left: -205px;
            padding-left: 200px;
            box-sizing: border-box;
            width: 100%;
            display: inline-block;
            vertical-align: top;
            margin-right: -5px;

        }</div>2020-09-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/59/21/d2efde18.jpg" width="30px"><span>布凡</span> 👍（1） 💬（0）<div>老师，请教一下，等分的那个例子中，如果&lt;div class=&quot;inner&quot;&gt;内容&lt;&#47;div&gt;中包含内容整个div就会往下掉，这是什么原因导致的呢？另外如果设置.outer { font-size:0;}而.inner中没有设置样式font-size:30px; 这个宽度也不对，能再解释一下吗？</div>2020-02-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/fb/24/d2d64acc.jpg" width="30px"><span>away</span> 👍（1） 💬（2）<div>formatting context + boxes&#47;charater = positions 单词charater拼写错误，应是charcter</div>2019-05-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/b3/24/1ee8fe0e.jpg" width="30px"><span>a小磊。จุ๊บ 🌹</span> 👍（1） 💬（0）<div>最后一个例子刚好是圣杯布局和双飞翼布局的原理</div>2019-04-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/f9/2b/afa78ed8.jpg" width="30px"><span>孙清海</span> 👍（1） 💬（1）<div>大师你好！今天再看一本书《数据结构与算法描述JavaScript》 偶然发现了熟悉的名字 ，程劭非 大师作序  !感觉好熟悉，哇这不是!!!我要好好看书了……</div>2019-03-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/1a/5d/3c8004c6.jpg" width="30px"><span>*</span> 👍（0） 💬（0）<div>思考题好难&#47;(ㄒoㄒ)&#47;~~</div>2022-03-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/89/15/381ce65f.jpg" width="30px"><span>不曾相识</span> 👍（0） 💬（0）<div>利用定义，模拟了一个- -
https:&#47;&#47;github.com&#47;RanmanticOfMonicaKS&#47;inline-block-demo</div>2020-09-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/43/87/7604d7a4.jpg" width="30px"><span>起而行</span> 👍（0） 💬（0）<div>js，如果检测到float和每个元素一行的block,就转换成inline-block,前者可以变成固定，后者去自动调整每个元素的间距</div>2020-03-20</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqIfEYDAV0pko0B4CichMictTiah9ZhEdV1fdIEpmgDaoOlkDl5foSZodCe6sibT1OgeGeKETTT7Wm8gg/132" width="30px"><span>Geek_fc9b29</span> 👍（0） 💬（0）<div>三等分、自适应宽度，可以考虑强大的table-cell布局，自带bfc</div>2019-12-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/40/d7/369c9fea.jpg" width="30px"><span>金海烛光</span> 👍（0） 💬（0）<div>最后一段的代码并不是完整版，说最后代码无法换行的小伙伴要把上面消除空白那部分的css加上</div>2019-06-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1a/e5/6899701e.jpg" width="30px"><span>favorlm</span> 👍（0） 💬（0）<div>老师您好，最大的恐惧就是排版，还请赐教，如何克服</div>2019-03-25</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIsxrBp1AmKHq3daCP1D8CmFicm46EIM1aX664U7CXMT5cb6ee4oByp7XZWcqUzUATIlDJIbwqvy2g/132" width="30px"><span>Geek_eea87d</span> 👍（0） 💬（0）<div>请问下(行盒是块级)，和一个浏览器是如何工作的 阶段四中的(浏览器对行的排版，一般是先行内布局...)这句话的 两个 行是您说的同一个行吗

</div>2019-03-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/78/f5/6821ac5f.jpg" width="30px"><span>ezra.xu</span> 👍（0） 💬（0）<div>老师的每节课都像是在划重点，很赞！</div>2019-03-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/79/c5/4098108b.jpg" width="30px"><span>夏超</span> 👍（0） 💬（0）<div>请问老师，JavaScript 的call stack size是多少，这个size的单位是啥，是调用栈中函数的个数，还是 一个存储单位，比如mb  之类的。如果调用栈中就一个函数，这个函数的参数有100万个，浏览器端依然会溢出，看起来是存储单位，但是没得到验证，请教老师</div>2019-03-15</li><br/>
</ul>