你好，我是winter。

今天我们进入CSS的学习。CSS是前端工程师几乎每天都要用的技术了，不过CSS的学习资料却是最糟糕的，这是因为CSS并没有像HTML和JavaScript那样的一份标准文档。

如果我们到W3C的网站上搜索看看，可以得到一些信息：

- [https://www.w3.org/TR/?title=css](https://www.w3.org/TR/?title=css)

在这里，我们一共看到了98份CSS相关的标准，它们各自从一些角度规定了CSS的特性。

这里我们暂且去掉Working Draft状态的标准，可以得到22份候选标准和6份推荐标准。

既然我们的专栏内容强调去系统性学习CSS，于是，面对这22+6份标准，我们就又需要一条线索，才能把这些离散的标准组织成易于理解和记忆的形式。

在这样的需求下，我找到的线索就是CSS语法，任何CSS的特性都必须通过一定的语法结构表达出来，所以语法可以帮助我们发现大多数CSS特性。

CSS语法的最新标准，你可以戳这里查看：

- [https://www.w3.org/TR/css-syntax-3/](https://www.w3.org/TR/css-syntax-3/)

这篇文档的阅读体验其实是非常糟糕的，它对CSS语法的描述使用了类似LL语法分析的伪代码，而且没有描述任何具体的规则。

这里你就不必自己去阅读了，我来把其中一些有用的关键信息抽取出来描述一下，我们一起来看看。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://wx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJlgFmOLogkNRwKVyYbNzu79k2Y8k9d3AEiaIDmQWI3c7YNEw1RYPGmQteibthXTnwoSqBj0aibZhmfw/132" width="30px"><span>吴前端</span> 👍（3） 💬（1）<div>toggle()函数试了下在google 火狐打开都没用呢显示无效属性值</div>2019-02-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/78/d6/89227ea0.jpg" width="30px"><span>小夜</span> 👍（0） 💬（1）<div>@namespace svg url(http:&#47;&#47;www.w3.org&#47;2000&#47;svg)
请问这个 声明这个 namespace 的必要性在哪里，在什么情况下会需要使用这个规则</div>2019-10-25</li><br/><li><img src="" width="30px"><span>比利利</span> 👍（0） 💬（1）<div>查阅了一些资料发现，目前CSS中toggle()这个函数在任何主流浏览器中都不支持，所以无论是Chrome还是Firefox里用这个函数都是无效的。</div>2019-02-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/94/56/4b8395f6.jpg" width="30px"><span>CC</span> 👍（386） 💬（2）<div>在网站上搜索了一下，发现 css 函数有不少，尤其是近三年，增加的函数几乎超过过去的总和。

按照 winter 老师提到「知识完备性」的思路，尝试整理了一下 CSS 函数。

按照功能，分成以下 5 个类别（可能并不完全准确）：

# 1. 图片

* filter
    * blur()
    * brightness()
    * contrast()
    * drop-shadow()
    * grayscale()
    * hue_rotate()
    * invert()
    * opacity()
    * saturate()
    * sepia()
* cross-fade()
* element()
* image-set()
* imagefunction()

# 2. 图形绘制
* conic-gradient()
* linear-gradient()
* radial-gradient()
* repeating-linear-gradient()
* repeating-radial-gradient()
* shape()

# 3. 布局
* calc()
* clamp()
* fit-content()
* max()
* min()
* minmax()
* repeat()

# 4. 变形&#47;动画
* transform
    * matrix()
    * matrix3d()
    * perspective()
    * rotate()
    * rotate3d()
    * rotateX()
    * rotateY()
    * rotateZ()
    * scale()
    * scale3d()
    * scaleX()
    * scaleY()
    * scaleZ()
    * skew()
    * skewX()
    * skewY()
    * translate()
    * translate3d()
    * translateX()
    * translateY()
    * translateZ()

# 5. 环境与元素
* var()
* env()
* attr()
</div>2019-02-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/9d/52/9793e3ba.jpg" width="30px"><span>Sevens 些粉</span> 👍（80） 💬（1）<div>推荐一下《css世界》这本书，有理论基础也有实战应用和常遇坑，看了两章感觉不错。</div>2019-02-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/39/30/f7df6ba7.jpg" width="30px"><span>米斯特菠萝</span> 👍（34） 💬（1）<div>我看到winter老师讲解这些冷门的知识，忽然意识到什么叫做精通？要精通就要抠这种细节，这样才能做到精通

做就要做精通，前端是一种手艺人</div>2019-02-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/37/64/dfba5f1c.jpg" width="30px"><span>文全</span> 👍（15） 💬（0）<div>@import 用于引入一个 CSS 文件，除了 @charset 规则不会被引入，@import 可以引入另一个 JavaScript 文件的全部内容。这段写错了 应该是css 文件全部内容</div>2019-02-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/61/c1/93031a2a.jpg" width="30px"><span>Aaaaaaaaaaayou</span> 👍（12） 💬（0）<div>“只有伪类可以出现在伪元素之后”是不是写反了</div>2019-02-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/3a/fa/21f64eaa.jpg" width="30px"><span>mimof9</span> 👍（8） 💬（4）<div>试了一下 toggle这个函数 并没有效果。clac实测下来是有效果的。</div>2019-02-08</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/hkBfzo6cRvbBmFZKPxlzRnKyria9gzID4WQ9mI1NdBBox5lRox7eMuhicXPB7eU1ecOa0lD9fhNTG3H6yJlII50A/132" width="30px"><span>前端男孩</span> 👍（7） 💬（0）<div>本来想发张思维导图的，但是貌似不支持发图，想想算了，也就整理了67个css函数，也不知道够不够。</div>2019-06-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/40/0f/76b2e320.jpg" width="30px"><span>无痕</span> 👍（7） 💬（1）<div>“||”这个选择器我怎么没搜到，是什么意思</div>2019-03-04</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTI2icbib62icXtibTkThtyRksbuJLoTLMts7zook2S30MiaBtbz0f5JskwYicwqXkhpYfvCpuYkcvPTibEaQ/132" width="30px"><span>xuanyuan</span> 👍（4） 💬（1）<div>每篇文章希望增加一些预备知识，后端程序员表示看不懂</div>2019-02-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/61/f5/3a36af36.jpg" width="30px"><span>瓶盖</span> 👍（3） 💬（0）<div>css函数：https:&#47;&#47;www.w3cplus.com&#47;css&#47;css-functions.html</div>2019-02-28</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/XSnxM4uP67kdzzCRW8KxhS5jkHiaaSrgkuLh1Z5BxawvQase46pbGAL4Bngmd3eFHckQml6zexyukFoWpeNENTg/132" width="30px"><span>Rushan-Chen</span> 👍（3） 💬（0）<div>@mimof9 
文章的链接是CSS4 working draft状态的文档，是很新的文档。

看了下CSS3 Candidate Recommendation状态的文档，没有toggle()、min()、max()、clamp()，这几个函数应该是css4新加的，基本上浏览器都还不支持。

attr()虽然css3文档有，查了下，浏览器也都不支持。😂

等浏览器支持估计还要一段时间吧，现在先知道有这个东西就好，我是这样想的。
</div>2019-02-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/43/87/7604d7a4.jpg" width="30px"><span>起而行</span> 👍（2） 💬（0）<div>发现对于css体系还不太了解，比如动画，伪选择器等等。打算在这几天准备一下绘图，布局，伪选择器的知识，为面试做准备</div>2020-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/bc/16/787bffde.jpg" width="30px"><span>南蓝</span> 👍（2） 💬（0）<div>@ counter-style 只在火狐上有用

    &lt;style&gt;
        @counter-style circled-alpha {
            system: fixed;
            symbols: &quot;\7532&quot;&quot;\4E59&quot;&quot;\4E19&quot;&quot;\4E01&quot;&quot;\620A&quot;&quot;\5DF1&quot;&quot;\5E9A&quot;&quot;\8F9B&quot;&quot;\58EC&quot;&quot;\7678&quot;;
            &#47;* 甲 乙 丙 丁 戊 己 庚 辛 壬 癸 *&#47;
            suffix: &quot; &quot;;
        }

        ul li {
            list-style: circled-alpha;

        }
    &lt;&#47;style&gt;
&lt;&#47;head&gt;

&lt;body&gt;
    &lt;ul&gt;
        &lt;li&gt;1&lt;&#47;li&gt;
        &lt;li&gt;2&lt;&#47;li&gt;
        &lt;li&gt;3&lt;&#47;li&gt;
        &lt;li&gt;4&lt;&#47;li&gt;
        &lt;li&gt;5&lt;&#47;li&gt;
    &lt;&#47;ul&gt;
&lt;&#47;body&gt;</div>2019-02-12</li><br/><li><img src="" width="30px"><span>程序员讲道理</span> 👍（1） 💬（0）<div>作为一个客户端+后端开发，看到 css 真的头疼</div>2022-03-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/ad/3a/55fe4b27.jpg" width="30px"><span>躲啊躲</span> 👍（1） 💬（0）<div>https:&#47;&#47;css-tricks.com&#47;complete-guide-to-css-functions&#47;</div>2020-10-26</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIYg80llu8nzJn5x394p9WsKuac5qgCU506tBXIqUvTbe19YYMLEzo46rf2FQJvNLzcx9lnmYjDeg/132" width="30px"><span>ssaylo</span> 👍（1） 💬（0）<div># CSS function

1. ###  Common CSS Functions

   1. #### `url()`

   2. #### `attr()`

   3. #### `calc()`

   4. #### `lang()`

   5. #### `:not()`

2. ###  CSS Custom Properties

   1. `var()`

3. ### Color Functions

   1. #### `rgb()` and `rgba()`

   2. #### `hsl()` and `hsla()`

4. ### Pseudo Class Selector Functions

   1. #### `:nth-child()`

   2. #### `:nth-last-child()`

   3. #### `:nth-of-type()`

   4. #### `:nth-last-of-type()`

5. ### Animation Functions

   1. #### `cubic-bezier()`

   2. #### `path()`

   3. #### `steps()`

6. ### Sizing &amp; Scaling Functions

   1. #### `scaleX()`, `scaleY()`, `scaleZ()`, `scale3d()`, and `scale()`

   2. #### `translateX()`, `translateY()`, `translateZ()`, `translate3d()`, and `translate()`

   3. #### `perspective()`

   4. #### `rotateX()`, `rotateY()`, `rotateZ()`, `rotate3d()`, and `rotate()`

   5. #### `skewX()`, `skewY()`, and `skew()`

7. ### Filter Functions

   1. #### `brightness()`

   2. #### `blur()`

   3. #### `contrast()`

   4. #### `grayscale()`

   5. #### `invert()`

   6. #### **`opacity()`**

   7. #### **`saturate()`**

   8. #### **`sepia()`**

   9. #### **`drop-shadow()`**

   10. #### **`hue-rotate()`**

   11. #### **SVG filters** 

8. ### Gradient Functions

   1. #### `linear-gradient()` and `repeating-linear-gradient()`

   2. #### `radial-gradient()` and `repeating-radial-gradient()`

   3. #### `conic-gradient()` and `repeating-conical-gradi

9. ### Gradient Functions

   1. #### `linear-gradient()` and `repeating-linear-gradient()`

   2. #### `radial-gradient()` and `repeating-radial-gradient()`

   3. #### `conic-gradient()` and `repeating-conical-gradient`

10. ### Grid Functions

    1. #### `fit-content()`

    2. #### `minmax()`

    3. #### `repeat()`

11. ### Shape Functions

    1. #### `circle()`

    2. #### `ellipse()`

    3. #### **`polygon()`**

    4.  **`inset()`**

12. ### Miscellaneous Functions

    1.  `element()`

    2.  `image-set()`

    3.  `::slotted()`</div>2020-07-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/bb/5a/5b37caff.jpg" width="30px"><span>饼</span> 👍（1） 💬（0）<div>不少函数还没法用，目前还是var clac比较接近实用了</div>2019-06-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/08/38/37570dc0.jpg" width="30px"><span>王峰</span> 👍（1） 💬（0）<div>选择器还有一种情况就是*通配符，它不属于标签选择器，也没有优先级</div>2019-04-17</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJByxt4cWqx8Aru7iaOPk2sibeWhwBfES6EKACnN2AvSyFC9DN5ibbWezicd6lA13Siaa3JyYjjSnY9BIg/132" width="30px"><span>🚂🚂🚂</span> 👍（1） 💬（0）<div>CSS Functions
Alphabetical list of CSS functions included in CSS3.

attr()
blur()
brightness()
calc()
circle()
contrast()
counter()
counters()
cubic-bezier()
drop-shadow()
ellipse()
grayscale()
hsl()
hsla()
hue-rotate()
hwb()
image()
inset()
invert()
linear-gradient()
matrix()
matrix3d()
opacity()
perspective()
polygon()
radial-gradient()
repeating-linear-gradient()
repeating-radial-gradient()
rgb()
rgba()
rotate()
rotate3d()
rotateX()
rotateY()
rotateZ()
saturate()
sepia()
scale()
scale3d()
scaleX()
scaleY()
scaleZ()
skew()
skewX()
skewY()
symbols()
translate()
translate3d()
translateX()
translateY()
translateZ()
url()</div>2019-03-04</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/XSnxM4uP67kdzzCRW8KxhS5jkHiaaSrgkuLh1Z5BxawvQase46pbGAL4Bngmd3eFHckQml6zexyukFoWpeNENTg/132" width="30px"><span>Rushan-Chen</span> 👍（1） 💬（0）<div>@南蓝 @counter-style 的兼容性不佳，除了firefox 能部分支持，其它浏览器都还不支持，可以上 https:&#47;&#47;caniuse.com 搜索@counter-style查看浏览器的兼容情况。</div>2019-02-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/51/9f/1840385e.jpg" width="30px"><span>胡永</span> 👍（1） 💬（0）<div>Pseudo class selector</div>2019-02-12</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/gvfibNc3Bol6DzLMG5ia9wSLVYseoq326iae7TczmgmBj9u3Jwt8c0hl9KSzY4GNTFn0ic9m1ibzicqJ3aGzeQemec2Q/132" width="30px"><span>hhk</span> 👍（1） 💬（0）<div>css语法：at 规则 + 普通规则
普通规则：选择器 + 声明区块

另外，margin 的读音好像读错了</div>2019-02-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/51/9f/1840385e.jpg" width="30px"><span>胡永</span> 👍（0） 💬（0）<div>sayWoof()
countDogs()
drop-shadow()
url()
attr()
calc()
lang()
:not()
var()
rgb()
rgba()
hsl()
hsla()
lab()
lch()
:nth-child()
nth-child()
:nth-last-child()
:nth-of-type()
:nth-last-of-type()
cubic-bezier()
path()
steps()
scaleX()
scaleY()
scaleZ()
scale3d()
scale()
translateX()
translateY()
translateZ()
translate3d()
translate()
perspective()
rotateX()
rotateY()
rotateZ()
rotate3d()
rotate()
skewX()
skewY()
skew()
brightness()</div>2021-05-14</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTI7iakTvMwXWBHCK6WicIV2M3yQMZ8BtBgYgzARcEjbEtcWfKsQ2JqpZianKibZ2D7l1D3rwyTOL56Pzw/132" width="30px"><span>Jackchoumine</span> 👍（0） 💬（0）<div>按照规范，应该使用双冒号（::）而不是单个冒号（:），以便区分伪类和伪元素。但是，由于旧版本的 W3C 规范并未对此进行特别区分，因此目前绝大多数的浏览器都同时支持使用这两种方式来表示伪元素。</div>2019-09-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/7b/f0/ccc11dec.jpg" width="30px"><span>Cris</span> 👍（0） 💬（0）<div>Winter老师的课程，给我的帮助就是能够让我宏观上建立知识框架，至于细枝末节，也需要自己私下里再下功夫</div>2019-09-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c4/bd/72180435.jpg" width="30px"><span>融梨</span> 👍（0） 💬（0）<div>为什么，我没想到，学习CSS的完备性，也就是不管中规豹。</div>2019-07-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/0f/52/9003edf6.jpg" width="30px"><span>Te Fuir　　༽</span> 👍（0） 💬（0）<div>ul { list-style-type: toggle(circle, square); }
这块设置列表项的样式圆点和方点间的切换并没有生效</div>2019-05-09</li><br/>
</ul>