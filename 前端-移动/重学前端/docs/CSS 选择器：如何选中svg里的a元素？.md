你好，我是winter。

我们在之前CSS语法课程中，已经介绍了关于选择器的一部分基础知识。在今天的这一课里，我们来系统学习一下CSS选择器。

在CSS语法课程中，我们已经见过一些选择器了，但在进入到具体的选择器介绍之前，我们首先要对选择器有一个整体的认识。

我先来讲讲选择器是什么，选择器是由CSS最先引入的一个机制（但随着document.querySelector等API的加入，选择器已经不仅仅是CSS的一部分了）。我们今天这一课，就重点讲讲CSS选择器的一些机制。

**选择器的基本意义是：根据一些特征，选中元素树上的一批元素。**

我们把选择器的结构分一下类，那么由简单到复杂可以分成以下几种。

- 简单选择器：针对某一特征判断是否选中元素。
- 复合选择器：连续写在一起的简单选择器，针对元素自身特征选择单个元素。
- 复杂选择器：由“（空格）”“ &gt;”“ ~”“ +”“ ||”等符号连接的复合选择器，根据父元素或者前序元素检查单个元素。
- 选择器列表：由逗号分隔的复杂选择器，表示“或”的关系。

我们可以看到，选择器是由简单选择器逐级组合而成的结构，那么我们就来首先看一下简单选择器。

## 简单选择器

我们在前面说过，简单选择器是针对某一特征判断是否为选中元素。今天我会为你介绍一系列常见的简单选择器，我们把相似的简单选择器放在一起，这样更易于你去记忆。
<div><strong>精选留言（21）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/de/3e/2e87843c.jpg" width="30px"><span>不曾潇洒</span> 👍（61） 💬（1）<div>老师这儿描述有点问题:
属性选择器第四种[attr|=value]
应该是表示带有以 attr 命名的属性的元素，属性值为“value”或是以“value-”为前缀（&quot;-&quot;为连字符，Unicode编码为U+002D）开头。典型的应用场景是用来来匹配语言简写代码（如zh-CN，zh-TW可以用zh作为value）。

[attr^=value]
表示带有以 attr 命名的属性，且属性值是以&quot;value&quot;开头的元素。

出处:https:&#47;&#47;developer.mozilla.org&#47;zh-CN&#47;docs&#47;Web&#47;CSS&#47;Attribute_selectors</div>2019-03-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（31） 💬（0）<div>
选择器	描述
[attribute]	用于选取带有指定属性的元素。
[attribute=value]	用于选取带有指定属性和值的元素。
[attribute~=value]	用于选取属性值中包含指定词汇的元素。
[attribute|=value]	用于选取带有以指定值开头的属性值的元素，该值必须是整个单词。
[attribute^=value]	匹配属性值以指定值开头的每个元素。
[attribute$=value]	匹配属性值以指定值结尾的每个元素。
[attribute*=value]	匹配属性值中包含指定值的每个元素。</div>2019-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/46/da/25f48aba.jpg" width="30px"><span>GETStrongBENice</span> 👍（12） 💬（1）<div>属性以某值开头不是[attr^=xxx]吗（捂脸</div>2019-03-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/35/d0/f2ac6d91.jpg" width="30px"><span>阿成</span> 👍（12） 💬（2）<div>没想到写个 querySelector 这么费劲...
还有很多情况没处理到的...
emmm... 选择器字符串解析的部分应该上词法和语法分析的..
差不多能用吧就...
https:&#47;&#47;github.com&#47;aimergenge&#47;my-querySelector</div>2019-03-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/94/56/4b8395f6.jpg" width="30px"><span>CC</span> 👍（7） 💬（0）<div>namespace 和 of-type 系列的选择器的知识点，没想到之前居然完全被自己忽略。

系统性的学习才不会遗漏，才会有叠加效果。
</div>2019-03-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/de/3e/2e87843c.jpg" width="30px"><span>不曾潇洒</span> 👍（5） 💬（0）<div>属性选择器
第三种[attr~=val]的描述也会让人误解为选择器该表达式的val为空格分隔的序列，而实际是只匹配的目标元素上attr属性值为空格分隔的多个值:
表示带有以 attr 命名的属性的元素，并且该属性是一个以空格作为分隔的值列表，其中[至少]一个值匹配&quot;value&quot;。</div>2019-03-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/26/22/f826d202.jpg" width="30px"><span>within〃</span> 👍（4） 💬（0）<div>function querySelector (selector, rootNode = document) {
  let [first, rest] = splitSelectorStr(selector)
  let nodes = findNodes(rootNode, first)
  if (nodes.length &gt; 0) {
    if (rest.length === 0) {
      return nodes[0]
    }
    for (let node of nodes) {
      let res = querySelector(rest, node)
      if (res) {
        return res
      }
    }
  }
  return null
}
function findNodes (rootNode, selector) {
  let head = selector.charAt(0)
  let body = selector.slice(1)
  switch (head) {
    case &#39;.&#39;:
      return rootNode.getElementsByClassName(body)
    case &#39;#&#39;:
      return [rootNode.getElementById(body)]
    default:
      return rootNode.getElementsByTagName(selector)
  }
}
function splitSelectorStr (selector) {
  let s = selector.trim()
  let i = s.indexOf(&#39; &#39;)
  let first, rest
  if (i === -1) {
    first = s
    rest = &#39;&#39;
  } else {
    first = s.slice(0, i)
    rest = s.slice(i + 1)
  }
  return [first, rest]
}</div>2019-03-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/32/e3/20676888.jpg" width="30px"><span>涂涂</span> 👍（3） 💬（0）<div>引用张大佬的文章话：

HTML5允许行内SVG和MathML，这就意味着，你可以使用同一个样式文件定义行内SVG、MathML元素的样式。

HTML5的解析的好处是，如果文档是HTML(而非XHTML)，HTML5的解析器可以暗中分配命名空间到已知的词汇（到目前为止，SVG, XML和MathML）。这就意味着你无需使用xmlns为您的HTML5文档中的SVG或MathML元素明确指定命名空间。</div>2019-07-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/be/22/8bb1640f.jpg" width="30px"><span>oillie</span> 👍（2） 💬（0）<div>id可以用document.getElementById
class可以用document.getElementsByClassName
tag可以用document.getElementsByTagName
attribute没直接API可用，本人能想到的是可以先取全部document.getElementByTagName(&#39;*&#39;)再过滤</div>2019-03-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/07/3b/a74706a1.jpg" width="30px"><span>Nino</span> 👍（1） 💬（2）<div>都是平常会用到的一些特性，被老师总结一下觉得系统多了。另外，老师的英文发音好随意啊。。</div>2019-06-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/e9/c3/62e63a4f.jpg" width="30px"><span>Geek_3b2d8c</span> 👍（0） 💬（0）<div>简单实现了个：https:&#47;&#47;github.com&#47;Jarvis2018&#47;reader-response&#47;tree&#47;master&#47;%E9%87%8D%E5%AD%A6%E5%89%8D%E7%AB%AF&#47;%E4%B8%80%E4%B8%AA%E7%AE%80%E5%8D%95%E9%80%89%E6%8B%A9%E5%99%A8</div>2021-10-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/28/4c/afe2ab34.jpg" width="30px"><span>云</span> 👍（0） 💬（0）<div>关于css选择器这块，强烈推荐看张鑫旭的 《CSS选择器世界》。</div>2020-12-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/0b/b6/f4044718.jpg" width="30px"><span>益明</span> 👍（0） 💬（0）<div>There are six different kinds of elements: void elements(空内容元素), the template element, raw text elements(原始文本元素), escapable raw text elements(可转意原始文本元素), foreign elements(外来元素：来自MathML和SVG命名空间的元素), and normal elements.
Void elements包含
area, base, br, col, embed, hr, img, input, link, meta, param, source, track, wbr；
The template element包含
template；
Raw text elements包含
script, style
Escapable raw text elements包含
textarea, title
foreign elements 外来元素：
SVG，MathML中包含的元素
normal element：其余所有元素
作为SVG中包含的元素，所以要通过namespace svg命名空间去选择</div>2020-10-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/7e/fc/b132947b.jpg" width="30px"><span>不甘心的翔入非非</span> 👍（0） 💬（1）<div>老师，感觉少了:after和:before这1个重要的选择器介绍呢</div>2020-08-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/c0/6b/92a69e77.jpg" width="30px"><span>A祥瑞A</span> 👍（0） 💬（0）<div>属性选择器和伪类选择器用得特别少，这两种选择器一般在什么情况下使用?</div>2020-07-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/5b/e3/d2fa4899.jpg" width="30px"><span>薛定鄂的猫</span> 👍（0） 💬（0）<div>为什么没有将伪元素选择器？</div>2020-05-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/43/87/7604d7a4.jpg" width="30px"><span>起而行</span> 👍（0） 💬（0）<div>js的getElementById等等函数，可以实现CSS选择器的功能，通过自定义函数可以实现伪类选择器的功能</div>2020-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/fb/df/8615f2d3.jpg" width="30px"><span>kaiking</span> 👍（0） 💬（0）<div>老师，发现这节的属性选择器，讲得有点抽象，我尽管曾经用过，但对于你的描述，看完后反而疑惑更大了，像那些太过抽象的理论，建议结合案例。
好的课程在精不在多，祝愿老师越办越好，桃李满天下</div>2019-10-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/52/cc/15e57326.jpg" width="30px"><span>若如</span> 👍（0） 💬（0）<div>之前看过jquery的选择器 最后的作业有点类似 收货颇丰</div>2019-09-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/55/cb/1efe460a.jpg" width="30px"><span>渴望做梦</span> 👍（0） 💬（0）<div>老师，属性选择器第三种[att=~val]这个不是选择值里面包含有val的元素吗，好像和您的表述不太一致，我传递了多个 val 用空格分隔，并没有选中多个元素。</div>2019-07-12</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Htgf7XWRjvlImq5Ng7ud2agtQMw9YUS1xDwtNtMenwIUFRscQVPbIKicbYCf5BpialRHdBWAcrUibVEpHZ75icOmicw/132" width="30px"><span>Geek_xd2069</span> 👍（0） 💬（1）<div>查了一些资料也没太弄明白为什么 svg 就在 http:&#47;&#47;www.w3.org&#47;2000&#47;svg 这个命名空间下，好像是规范里就规定了svg属于这个命名空间？
</div>2019-03-07</li><br/>
</ul>