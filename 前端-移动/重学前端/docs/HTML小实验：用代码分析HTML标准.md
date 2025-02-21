你好，我是winter。

前面的课程中，我们已经讲解了大部分的HTML标签。

然而，为了突出重点，我们还是会忽略一些标签类型。比如表单类标签和表格类标签，我认为只有少数前端工程师用过，比如我在整个手机淘宝的工作生涯中，一次表格类标签都没有用到，表单类则只用过input，也只有几次。

那么，剩下的标签我们怎么样去了解它们呢？当然是查阅HTML标准。

由于阅读标准有一定门槛，需要了解一些机制，这节课，我为你设计了一个小实验，用JavaScript代码去抽取标准中我们需要的信息。

## HTML标准

我们采用WHATWG的living standard标准，我们先来看看标准是如何描述一个标签的，这里我们看到，有下面这些内容。

```
Categories:
    Flow content.
    Phrasing content.
    Embedded content.
    If the element has a controls attribute: Interactive content.
    Palpable content.
Contexts in which this element can be used:
    Where embedded content is expected.
Content model:
    If the element has a src attribute: zero or more track elements, then transparent, but with no media element descendants.
    If the element does not have a src attribute: zero or more source elements, then zero or more track elements, then transparent, but with no media element descendants.
Tag omission in text/html:
    Neither tag is omissible.
Content attributes:
    Global attributes
    src — Address of the resource
    crossorigin — How the element handles crossorigin requests
    poster — Poster frame to show prior to video playback
    preload — Hints how much buffering the media resource will likely need
    autoplay — Hint that the media resource can be started automatically when the page is loaded
    playsinline — Encourage the user agent to display video content within the element's playback area
    loop — Whether to loop the media resource
    muted — Whether to mute the media resource by default
    controls — Show user agent controls
    width — Horizontal dimension
    height — Vertical dimension
DOM interface:
    [Exposed=Window, HTMLConstructor]
    interface HTMLVideoElement : HTMLMediaElement {
      [CEReactions] attribute unsigned long width;
      [CEReactions] attribute unsigned long height;
      readonly attribute unsigned long videoWidth;
      readonly attribute unsigned long videoHeight;
      [CEReactions] attribute USVString poster;
      [CEReactions] attribute boolean playsInline;
    };
```

我们看到，这里的描述分为6个部分，有下面这些内容。

- Categories：标签所属的分类。
- Contexts in which this element can be used：标签能够用在哪里。
- Content model：标签的内容模型。
- Tag omission in text/html：标签是否可以省略。
- Content attributes：内容属性。
- DOM interface：用WebIDL定义的元素类型接口。
<div><strong>精选留言（11）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/15/35/d0/f2ac6d91.jpg" width="30px"><span>阿成</span> 👍（20） 💬（0）<div>这种“通过简单的文本分析，快速提炼出自己感兴趣的部分”的方法是非常值得借鉴的，我平时也会用这种方法去网页中做一些快速的统计和信息筛选。

不过，通过这样的文本分析去完成一个“检查一个元素是否能够放置在另一个元素内部”的小程序还是有点“把问题复杂化”的感觉（尽管这个过程中也可以锻炼一些能力），况且文档是会更新的，指不定有一天那些check分支就hold不住新的case了。

在我看来，如果想知道A元素是否可以放在B元素中，只要把所有元素的categories和contentModel提取出来，筛选出A元素的categories和B元素的contentModel，再去阅读比较就可以了（当然你还要对标准中的一些术语有所了解，所幸的是这些术语都有超链接指向定义，所以还是比较方便的ヾ(≧▽≦*)o）。

</div>2019-04-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（9） 💬（0）<div>老师 有个疑问： WHATWG 和 W3C 标准以哪个为准，这两个标准有什么区别？是不是相互不认可的</div>2019-04-29</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/hkBfzo6cRvbBmFZKPxlzRnKyria9gzID4WQ9mI1NdBBox5lRox7eMuhicXPB7eU1ecOa0lD9fhNTG3H6yJlII50A/132" width="30px"><span>前端男孩</span> 👍（3） 💬（0）<div>为什么我去网页控制台上Console出不来呢？</div>2020-02-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/05/18/955a972f.jpg" width="30px"><span>会飞的大猫</span> 👍（1） 💬（0）<div>Winter，刚看完文章，就在淘宝技术节视频看到了你持相机和大家自拍的图片</div>2019-04-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/3c/88/6bef27d6.jpg" width="30px"><span>大神博士</span> 👍（0） 💬（0）<div>是我的问题吗，这文档好大，滚动起来好卡啊</div>2023-04-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/01/01/897990a0.jpg" width="30px"><span>Clors</span> 👍（0） 💬（0）<div>我提出一个场景，如果vw布局网页，不使用iframe如何做到限制最大大小？</div>2020-09-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b8/2c/0f7baf3a.jpg" width="30px"><span>Change</span> 👍（0） 💬（1）<div>本想实践一下这个实验，奈何https:&#47;&#47;html.spec.whatwg.org&#47;链接打不开是什么情况？</div>2020-03-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/8e/e0/847348b1.jpg" width="30px"><span>爱学习的大叔</span> 👍（0） 💬（0）<div>没太看懂，好多语法基于这个页面https:&#47;&#47;html.spec.whatwg.org&#47;</div>2019-06-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/fb/24/d2d64acc.jpg" width="30px"><span>away</span> 👍（0） 💬（0）<div> @一步 WHATWG 和 W3C 标准若有不同，一般以 WHATWG 为准</div>2019-04-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/a9/35/2b360ff1.jpg" width="30px"><span>嗨海海</span> 👍（0） 💬（1）<div>学不到，有因果关系，工作实际需要吗？</div>2019-04-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7c/61/76b1b888.jpg" width="30px"><span>被雨水过滤的空气</span> 👍（0） 💬（0）<div>学习了</div>2019-04-11</li><br/>
</ul>