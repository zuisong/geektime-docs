你好，我是winter。

在上一篇文章中，我已经给你介绍了一些简单选择器，这一节课我会继续给你介绍选择器的几个机制：选择器的组合、选择器的优先级和伪元素。

## 选择器的组合

在CSS规则中，选择器部分是一个选择器列表。

选择器列表是用逗号分隔的复杂选择器序列；复杂选择器则是用空格、大于号、波浪线等符号连接的复合选择器；复合选择器则是连写的简单选择器组合。

根据选择器列表的语法，选择器的连接方式可以理解为像四则运算一样有优先级。

- 第一优先级
  
  - 无连接符号
- 第二优先级
  
  - “空格”
  - “~”
  - “+”
  - “&gt;”
  - “||”
- 第三优先级
  
  - “,”

例如以下选择器：

```
.c,.a>.b.d {
    /*......*/
}
```

我们应该理解为这样的结构。

- .c,.a&gt;.b.d
  
  - .c
  - .a&gt;.b.d
    
    - .a
    - .b.d
      
      - .b
      - .d

复合选择器表示简单选择器中“且”的关系，例如，例子中的“ .b.d ”，表示选中的元素必须同时具有b和d两个class。

复杂选择器是针对节点关系的选择，它规定了五种连接符号。

- **“空格”**：后代，表示选中所有符合条件的后代节点， 例如“ .a .b ”表示选中所有具有class为a的后代节点中class为b的节点。
- **“&gt;”** ：子代，表示选中符合条件的子节点，例如“ .a&gt;.b ”表示：选中所有“具有class为a的子节点中，class为b的节点”。
- **“~”** : 后继，表示选中所有符合条件的后继节点，后继节点即跟当前节点具有同一个父元素，并出现在它之后的节点，例如“ .a~.b ”表示选中所有具有class为a的后继中，class为b的节点。
- **“+”**：直接后继，表示选中符合条件的直接后继节点，直接后继节点即nextSlibling。例如 “.a+.b ”表示选中所有具有class为a的下一个class为b的节点。
- **“||”**：列选择器，表示选中对应列中符合条件的单元格。
<div><strong>精选留言（23）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/16/61/f6/40731f37.jpg" width="30px"><span>德育处主任</span> 👍（9） 💬（3）<div>在《css重构》这本书里面建议一般情况下class用来给css提供选择入口，id则为js提供选择入口。尽量不要用js直接修改元素样式，而是通过js修改元素的class从而修改样式。这样能很好的划分样式与逻辑</div>2019-06-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4c/4f/858a8a70.jpg" width="30px"><span>o.O君程</span> 👍（3） 💬（2）<div>BEM</div>2019-11-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/f9/bc/cbc0207b.jpg" width="30px"><span>Scorpio</span> 👍（115） 💬（0）<div>我们团队没有规范。。。</div>2019-03-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/6b/ad/cf2e924e.jpg" width="30px"><span>Levix</span> 👍（38） 💬（0）<div>行内属性的优先级永远高于 CSS 规则，浏览器提供了一个“口子”，就是在选择器前加上“!import”。应该是 important 吧</div>2019-03-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/35/d0/f2ac6d91.jpg" width="30px"><span>阿成</span> 👍（13） 💬（0）<div>有两个问题想请教一下winter老师：
1. 您对styled-component类似的方案怎么看
2. 您对使用属性选择器代替class怎么看</div>2019-03-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/94/56/4b8395f6.jpg" width="30px"><span>CC</span> 👍（12） 💬（0）<div>如果是注重复用的开发，一般采用组件化的形式，给组件一套命名空间；

如果是页面较少的网页开发，不太在意复用和扩展，一般采用 BEM 的规则。

”根据 id 选单个元素，class 和 class 的组合选择成组元素，tag 选择器确定页面风格。“ 从这个原则中收获很大。
</div>2019-03-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/db/26/54f2c164.jpg" width="30px"><span>靠人品去赢</span> 👍（8） 💬（0）<div>我放一个伪类和伪元素的链接吧，这两者属于见过但是没注意更没区分过，估计有人会需要https:&#47;&#47;developer.mozilla.org&#47;zh-CN&#47;docs&#47;Learn&#47;CSS&#47;Introduction_to_CSS&#47;Pseudo-classes_and_pseudo-elements</div>2019-04-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/b0/de/0e75d3c2.jpg" width="30px"><span>bradleyzhou</span> 👍（7） 💬（1）<div>MDN 上有一个图解优先级的材料 https:&#47;&#47;specifishity.com&#47;</div>2019-05-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/b5/7a/a126c48f.jpg" width="30px"><span>巨龙的力量啊</span> 👍（5） 💬（1）<div>遇事不决就!important🤪</div>2019-12-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/bc/e8/43109d54.jpg" width="30px"><span>Peter</span> 👍（4） 💬（0）<div>后半段关于::first-line对非块元素不生效的理解和标准有些偏差，不太好理解其远离。
花时间重新研究了下。把p标签换成span之后为什么变成绿色的原因知识因为样式覆盖，和只作用于块状元素没有对应关系，具体可参考原始标准文档：https:&#47;&#47;drafts.csswg.org&#47;selectors-3&#47;#first-line

简单总结下就是伪元素其实是有虚拟结构的，样式也是基于这个虚拟结构进行应用的。然后对于一个div来说，内部元素是一个大的行内元素还是1或n个block-like元素，会导致两种“dom结构”，也就是包括内容的节点位置不一样，这会导致样式的优先级变掉，样式自然是不一样的。

对细节感兴趣的可以看下https:&#47;&#47;www.petershi.net&#47;archives&#47;3305</div>2020-06-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/4e/c7/cb93c786.jpg" width="30px"><span>Ranjay</span> 👍（4） 💬（0）<div>BEM规范实际上就已经是很好的实践</div>2019-03-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/65/36/4b0f6629.jpg" width="30px"><span>阿歡。</span> 👍（4） 💬（2）<div>老师您好,下面例子中 把&lt;br&gt;去掉，会变成First paragraph为绿色，Second paragraph为蓝色，这是为何？
&lt;div&gt;
            &lt;span id=&quot;a&quot;&gt;First paragraph&lt;&#47;span&gt;&lt;br&gt;
            &lt;span&gt;Second paragraph&lt;&#47;span&gt;
 &lt;&#47;div&gt;

           div&gt;span#a {
                color:green;
            }
            div::first-line { 
                color:blue; 
            }</div>2019-03-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/5b/e3/d2fa4899.jpg" width="30px"><span>薛定鄂的猫</span> 👍（3） 💬（1）<div>后代和子代这两个词真的不好，完全就是一个词</div>2020-05-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/1f/04/1cddf65b.jpg" width="30px"><span>不二</span> 👍（3） 💬（1）<div>first-line和first-letter那部分的代码，刚在浏览器端试了一下，div内部不管是span还是p，都是可以生效的，我理解这两个属性都是作用于 块元素， 所以如果将外面的div改成span可能就没有效果了，这块实际得到的效果为什么和老师将的不太一样？</div>2020-02-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5c/c2/8ffd2ad0.jpg" width="30px"><span>qqq</span> 👍（2） 💬（0）<div>提醒下：伪元素那部分说的是子元素 color 覆盖父元素 color，而非 CSS 规则覆盖</div>2019-03-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/04/dc/cae4e6c5.jpg" width="30px"><span>²⁰¹9😋</span> 👍（1） 💬（0）<div>用的是csslint</div>2020-02-22</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJ43ULj7ID91wpahz9hrlU7v0yqBE2ItzxiaBibZYPtgMTT0FskvEAvdI3YXfjTMoDhGxSgmTNahmFw/132" width="30px"><span>per</span> 👍（1） 💬（0）<div>img、br等不能包含子元素的标签不能创建::before和::after。但一个例外是hr，不知道为什么。或许是我的理解有问题？</div>2019-03-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ad/dd/970e7b4a.jpg" width="30px"><span>锐锐爱南球</span> 👍（0） 💬（0）<div>团队制定了sass的编码规范，但是在代码review的时候，reviewer比较少看sass代码，都是让提交代码的人截个图看下，主要精力放在js上。</div>2022-04-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/1a/5d/3c8004c6.jpg" width="30px"><span>*</span> 👍（0） 💬（0）<div>我们团队就是用BEM规范</div>2022-03-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/c0/6b/92a69e77.jpg" width="30px"><span>A祥瑞A</span> 👍（0） 💬（0）<div>我选择器都是随便用的.........</div>2020-07-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/e0/6b/f61d7466.jpg" width="30px"><span>prader26</span> 👍（0） 💬（0）<div>伪元素是通过css往html文本中添加的一些元素。 因为这些元素原本不存在所以称为伪元素，伪元素也能改变html 文本的样式。</div>2020-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/42/39/aa8cd514.jpg" width="30px"><span>旅途。👣👣</span> 👍（0） 💬（0）<div>评论亦精彩</div>2019-05-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/fe/5e/9b723d19.jpg" width="30px"><span>空山鸟语</span> 👍（0） 💬（1）<div>选择器的优先级那块，是不是还缺 属性选择器？
 比如  input[type=text] 等</div>2019-04-17</li><br/>
</ul>