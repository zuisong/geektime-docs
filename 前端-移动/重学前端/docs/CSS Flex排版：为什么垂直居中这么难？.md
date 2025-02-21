你好，我是winter。今天我们来谈谈Flex排版。

我们在前面多次讲过，正常流排版的设计来源于数百年来出版行业的排版经验，而HTML诞生之初，也确实是作为一种“超文本”存在的。

但是，自上世纪90年代以来，Web标准和各种Web应用蓬勃发展，网页的功能逐渐从“文本信息”向着“软件功能”过渡，这个思路的变化导致了：CSS的正常流逐渐不满足人民群众的需求了。

这是因为文字排版的思路是“改变文字和盒的相对位置，把它放进特定的版面中”，而软件界面的思路则是“改变盒的大小，使得它们的结构保持固定”。

因此，在早年的CSS中，“使盒按照外部尺寸变化”的能力非常弱。在我入行前端的时间（大约2006年），CSS三大经典问题：垂直居中问题，两列等高问题，自适应宽问题。这是在其它UI系统中最为基本的问题，而到了CSS中，却变成了困扰工程师的三座大山。

机智的前端开发者们，曾经创造了各种黑科技来解决问题，包括著名的table布局、负margin、float与clear等等。在这种情况下，Flex布局被随着CSS3一起提出（最初叫box布局），可以说是解决了大问题。

React Native则更为大胆地使用了纯粹的Flex排版，不再支持正常流，最终也很好地支持了大量的应用界面布局，这一点也证明了Flex排版的潜力。
<div><strong>精选留言（14）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/13/db/26/54f2c164.jpg" width="30px"><span>靠人品去赢</span> 👍（11） 💬（2）<div>flex是我刚开始做小程序，学到的第一个东西，真的好用，结合一些别的属性能解决很多兼容问题，而不再出现一机一况的情况，但是有的的时候，在做安卓和苹果的时候还是会遇到兼容性问题，能不能讲一下安卓和苹果的一些不同，比如在一个安卓上正常，在苹果上会出现边框被吃掉一部分的情况。</div>2019-06-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/55/cb/1efe460a.jpg" width="30px"><span>渴望做梦</span> 👍（3） 💬（3）<div>老师，为何最后一个宽度自适应的例子用 flex: 1 呢，flex: 1 表示什么含义呢？</div>2019-08-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a0/2b/efa6dc2e.jpg" width="30px"><span>KingSwim</span> 👍（53） 💬（4）<div>希望可以图文并茂一些</div>2019-08-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（14） 💬（3）<div>flex好用，gird更好用。会讲一下吗？</div>2019-04-13</li><br/><li><img src="" width="30px"><span>Geek_920664</span> 👍（11） 💬（0）<div>分享一个学习flex的小游戏：http:&#47;&#47;flexboxfroggy.com&#47;</div>2021-10-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/35/d0/f2ac6d91.jpg" width="30px"><span>阿成</span> 👍（11） 💬（2）<div>https:&#47;&#47;gist.github.com&#47;aimergenge&#47;e26193440fa38ebbb9a54847540c29c7</div>2019-04-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/d0/de/689f48c6.jpg" width="30px"><span>北拉</span> 👍（6） 💬（0）<div>试过好多次，找了很多方法flex兼容ie9以下，每次都失败，有什么好的解决办法吗</div>2019-04-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b8/11/26838646.jpg" width="30px"><span>彧豪</span> 👍（5） 💬（0）<div>gird布局如果后面winter老师没有讲到，推荐你找找大漠老师的文章来看看，另外阮一峰老师也写了一篇，二者可以结合起来看看</div>2019-04-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/1b/5d/1d5d1c00.jpg" width="30px"><span>cjd</span> 👍（4） 💬（0）<div>直接calc(100%  - n)</div>2019-04-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1a/e5/6899701e.jpg" width="30px"><span>favorlm</span> 👍（3） 💬（0）<div>自动填充剩余宽度
&lt;!DOCTYPE html&gt;
&lt;html lang=&quot;en&quot;&gt;
  &lt;head&gt;
    &lt;meta charset=&quot;UTF-8&quot; &#47;&gt;
    &lt;meta name=&quot;viewport&quot; content=&quot;width=device-width, initial-scale=1.0&quot; &#47;&gt;
    &lt;meta http-equiv=&quot;X-UA-Compatible&quot; content=&quot;ie=edge&quot; &#47;&gt;
    &lt;title&gt;自适应宽&lt;&#47;title&gt;
    &lt;style&gt;
      .box {
        position: absolute;
        width: 300px;
        height: 100px;
        background-color: cyan;
      }
      .childbox1Attr {
        position: absolute;
        background-color: bisque;
        width: 35px;
        height: 35px;
      }
      .childbox2Attr {
        position: absolute; 
        background-color: beige;
        width: 35px;
        height: 35px;
      }
    &lt;&#47;style&gt;
  &lt;&#47;head&gt;
  &lt;body&gt;
    &lt;div class=&quot;box&quot;&gt;
      &lt;div class=&quot;childbox1Attr&quot;&gt;&lt;&#47;div&gt;
      &lt;div class=&quot;childbox2Attr&quot;&gt;&lt;&#47;div&gt;
    &lt;&#47;div&gt;
    &lt;script&gt;
        
            const childbox1Attr = {
                width: &#39;100&#39;
            };
            const childbox2Attr = {
                width: &#39;100&#39;,
                flex: &#39;1&#39;
            };
            const box = document.getElementsByClassName(&#39;box&#39;)[0];
            const childbox1Ele = document.getElementsByClassName(&#39;childbox1Attr&#39;)[0];
            const childbox2Ele = document.getElementsByClassName(&#39;childbox2Attr&#39;)[0];
            const boxcomputedStyle = window.getComputedStyle(box, null);
            const child1ComputedStyle = window.getComputedStyle(childbox1Ele, null);
            childbox1Ele.style.width = childbox1Attr.width+&#39;px&#39;;
            if(childbox2Attr.flex !== null || childbox2Attr.flex!==&#39;&#39;){
                if(childbox2Attr.flex === &#39;1&#39;){
                    &#47;&#47; 利用一下不安全特性，实在不知道怎么写
                    const childbox2EleWidth = boxcomputedStyle[&quot;width&quot;].substring(0,3) - child1ComputedStyle[&quot;width&quot;].substring(0,3);
                    childbox2Ele.style.width = childbox2EleWidth + &#39;px&#39;;
                    childbox2Ele.style.left = child1ComputedStyle[&quot;width&quot;]
                }
            }
        
        &lt;&#47;script&gt;
  &lt;&#47;body&gt;
&lt;&#47;html&gt;
</div>2019-04-14</li><br/><li><img src="" width="30px"><span>坎坷的程序媛</span> 👍（2） 💬（0）<div>align-items默认值为stretch，所以平时没设置也自动等高了</div>2020-12-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/1f/bd/04100cb4.jpg" width="30px"><span>困到清醒</span> 👍（2） 💬（1）<div>老师也太棒了，每次垂直居中都奔溃，各种查百度，给我一种错觉，css靠经验靠运气，有时候都不知道为什么就成功了，然后下次又重新查。这一波从设计的讲解，豁然开朗，再也不会是无头苍蝇了。</div>2020-01-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/9e/72/8edab2e3.jpg" width="30px"><span>Geek_59f56b</span> 👍（0） 💬（0）<div>老师，把 Flex 延伸的方向称为“主轴”，flex延伸的方向是什么了？</div>2022-02-24</li><br/><li><img src="" width="30px"><span>Jenny</span> 👍（0） 💬（0）<div> 超文本 应该怎么理解？</div>2022-01-11</li><br/>
</ul>