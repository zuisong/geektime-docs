你好，我是winter。

我们都知道，HTML已经是一个完整的语义系统。在前面的课程中，我们围绕着HTML本身做了讲解，但是在实际应用中，我们还会用到一些它的扩展。今天我们要讲的ARIA就是其中重要的一部分。

ARIA全称为Accessible Rich Internet Applications，它表现为一组属性，是用于可访问性的一份标准。关于可访问性，它被提到最多的，就是它可以为视觉障碍用户服务，但是，这是一个误解。

实际上，可访问性其实是一个相当大的课题，它的定义包含了各种设备访问、各种环境、各种人群访问的友好性。不单单是永久性的残障人士需要用到可访问性，健康的人也可能在特定时刻处于需要可访问性的环境。

我们今天讲的ARIA，是以交互形式来标注各种元素的一类属性，所以，在ARIA属性中，你可以看到很多熟悉的面孔，交互形式往往跟我们直觉中的“控件”非常相似。

所以我们的课程，特意把ARIA加入还有一个原因：ARIA的角色对于我们UI系统的设计有重要的参考意义。

## 综述

我们先整体来看看，ARIA给HTML元素添加的一个核心属性就是role，我们来看一个例子：

```HTML
<span role="checkbox" aria-checked="false" tabindex="0" aria-labelledby="chk1-label">
</span> <label id="chk1-label">Remember my preferences</label>
```
<div><strong>精选留言（6）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/fe/38/b6995d69.jpg" width="30px"><span>王小贱</span> 👍（20） 💬（0）<div>几年前有改造过无障碍网站....真滴是枯燥，不过不改的话在美国会被投诉下架</div>2019-11-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a9/58/9324f5cc.jpg" width="30px"><span>Artyhacker</span> 👍（10） 💬（0）<div>感觉ARIA应该算一份前端UI组件库的实现标准吧，实际项目中除了一些简单的网页以外，大都直接用组件库了。以前专门学习了mdn里可访问性相关的文档，但实际项目还是从来没用到过，可能也和项目并非面向大众有关吧。。感觉很多东西你知道它好，也花时间学习了，但是实际项目就是不会去用。。</div>2019-05-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/26/22/dd505e6d.jpg" width="30px"><span>Yully</span> 👍（9） 💬（1）<div>看完了这篇文章，恍然大悟，原来公司大佬写的ui组件库里的那些看上去乱七八糟的东西是这个…大佬之前写的代码规规整整，尤其是ARIA这一块写的超级有条理，希望以后我再封装的时候也能用上ARIA</div>2020-06-03</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/rqh9unBPg1VnibWWplUtEm2GXuqd0Ye3yCF5MIuxvojXIzY0TOvbdXbGp7N8lw0vrmPS7jVj1BS2gdy3WQX9VAQ/132" width="30px"><span>亮亮</span> 👍（6） 💬（0）<div>可访问性在开发中还是用的比较少，项目没要求，开发时间紧，没咋注重过！</div>2019-05-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/6c/ee/2ec78dbc.jpg" width="30px"><span>Apep</span> 👍（0） 💬（1）<div>最近react项目有这个需求 头痛</div>2019-05-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/1b/5d/1d5d1c00.jpg" width="30px"><span>cjd</span> 👍（0） 💬（0）<div>沙发</div>2019-05-07</li><br/>
</ul>