你好，我是winter，今天我们来学习一下CSS的渲染相关的属性。

我们在布局篇讲到，CSS的一些属性决定了盒的位置，那么今天我讲到的属性就决定了盒如何被渲染。

按照惯例，还是先从简单得讲起，首先我们来讲讲颜色。

## 颜色的原理

首先我们来讲讲颜色，最常见的颜色相关的属性就是 `color` 和 `background-color`。

这两个属性没什么好讲的，它们分别表示文字颜色和背景颜色，我们这里重点讲讲颜色值。

### RGB颜色

我们在计算机中，最常见的颜色表示法是RGB颜色，**它符合光谱三原色理论：红、绿、蓝三种颜色的光可以构成所有的颜色。**

![](https://static001.geekbang.org/resource/image/7f/a1/7f5bf39cbe44e36758683a674f9fcfa1.png?wh=1268%2A1268)

为什么是这三种颜色呢？这跟人类的视神经系统相关，人类的视觉神经分别有对红、绿、蓝三种颜色敏感的类型。

顺便提一下，人类对红色的感觉最为敏感，所以危险信号提示一般会选择红色；而红绿色盲的人，就是红和绿两种神经缺失一种。其它的动物视觉跟人可能不太一样，比如皮皮虾拥有16种视锥细胞，所以我猜它们看到的世界一定特别精彩。

现代计算机中多用 0 - 255 的数字表示每一种颜色，这正好占据了一个字节，每一个颜色就占据三个字节。

这个数字远远超过了人体的分辨能力，因此，上世纪90年代刚推出这样的颜色系统的时候，它被称作真彩色。早年间还有更节约空间，但是精度更低的16色、256色、8位色和16位色表示法。
<div><strong>精选留言（14）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/15/35/d0/f2ac6d91.jpg" width="30px"><span>阿成</span> 👍（35） 💬（7）<div>怎么说呢，要想完美的转换... 好难... 仅靠单像素颜色来识别出鹦鹉的轮廓还是不太可行... 
也许把周围像素的颜色考虑进去是个办法... 不过这图挺大的...

&lt;!DOCTYPE html&gt;
&lt;html lang=&quot;en&quot;&gt;
&lt;head&gt;
  &lt;meta charset=&quot;UTF-8&quot;&gt;
  &lt;title&gt;Document&lt;&#47;title&gt;
  &lt;style type=&quot;text&#47;css&quot;&gt;
    .bird {
      width: 400px;
      height: calc(1440 * 400 &#47; 1920 * 1px);
    }
    canvas.bird {
      background: #ccc;
    }
  &lt;&#47;style&gt;
&lt;&#47;head&gt;
&lt;body&gt;
  &lt;img id=&quot;img&quot; class=&quot;bird&quot; src=&quot;.&#47;bird.jpg&quot;&gt;
  &lt;canvas id=&quot;canvas&quot; width=&quot;1920&quot; height=&quot;1440&quot; class=&quot;bird&quot;&gt;&lt;&#47;canvas&gt;

  &lt;script type=&quot;text&#47;javascript&quot;&gt;
    let canvas = document.getElementById(&#39;canvas&#39;)
    let ctx = canvas.getContext(&#39;2d&#39;)
    let img = document.getElementById(&#39;img&#39;)
    img.addEventListener(&#39;load&#39;, () =&gt; {
      ctx.drawImage(img, 0, 0)

      let imageData = ctx.getImageData(0, 0, canvas.width, canvas.height)
      let data = imageData.data

      for (let i = 0; i &lt; data.length; i += 4) {
        if (isBird(data, i, canvas.width, canvas.height)) {
          ;[data[i], data[i + 1]] = [data[i + 1] * 1.2, data[i]]
        }
      }

      ctx.putImageData(imageData, 0, 0)
    })

    function isBird (data, i, width, height) {
      let r = data[i]
      let g = data[i + 1]
      let b = data[i + 2]

      let [h, s, l] = rgb2hsl(r, g, b)
      return h &lt; 200 &amp;&amp; h &gt; 80 &amp;&amp; s &gt; 0.23 &amp;&amp; l &lt; 0.84
    }

    function rgb2hsl (r, g, b) {
      let r1 = r &#47; 255
      let g1 = g &#47; 255
      let b1 = b &#47; 255

      let min = Math.min(r1, g1, b1)
      let max = Math.max(r1, g1, b1)

      let l = (min + max) &#47; 2
      let s
      let h

      if (l &lt; 0.5) {
        s = (max - min) &#47; (max + min)
      } else {
        s = (max - min) &#47; (2 - max - min)
      }

      if (max === r1) {
        h = (r1 - b1) &#47; (max - min)
      } else if (max === g1) {
        h = 2 + (b1 - r1) &#47; (max - min)
      } else if (max === b1) {
        h = 4 + (r1 - g1) &#47; (max - min)
      }

      h *= 60

      while (h &lt; 0) {
        h += 360
      }

      return [h, s, l]
    }
  &lt;&#47;script&gt;
&lt;&#47;body&gt;
&lt;&#47;html&gt;
</div>2019-04-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/bc/e8/43109d54.jpg" width="30px"><span>Peter</span> 👍（24） 💬（2）<div>一步到位：filter: hue-rotate(240deg);
根据HSL色环，绿色在120deg的位置，要变成红色，把色相顺时针旋转240deg或者逆时针120deg即可。</div>2020-06-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/4d/90/b34f4a91.jpg" width="30px"><span>GGFGG</span> 👍（8） 💬（0）<div>CMYK，为什么有K，一方面是成本，另一方面是因为自然界的CMY不能合成纯黑的颜色，所以需要纯黑</div>2019-07-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ce/c6/958212b5.jpg" width="30px"><span>sugar</span> 👍（7） 💬（2）<div>我来给个答案吧，乍一看 感觉需要用到很多cv领域的技术，模式识别判定轮廓，然后根据色值不同进行greenToRed转译。后来想了一下，这明明是前端的课程嘛，按cv的解决方案，难道还要把opencv编译到wasm里？转念一想，其实css滤镜就能做这事儿，试了试 几行css代码能做的事 在opencv要引一大堆库 改一大堆参数了</div>2019-11-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/77/9b/c18f4047.jpg" width="30px"><span>Geek_8rfqh9</span> 👍（2） 💬（0）<div>&lt;!DOCTYPE html&gt;
&lt;html&gt;
  &lt;head&gt;
    &lt;title&gt;鹦鹉变成红色&lt;&#47;title&gt;
    &lt;script&gt;
    	function loadImg() {
           let img = new Image
           img.src = &quot;yingwu.jpg&quot;
           
           img.onload = function () {
           	  drawCanvas(img)
           }
    	}

    	function drawCanvas(img) {
          let canvas = document.getElementById(&#39;canvas&#39;)
          canvas.width = img.width
          canvas.height = img.height
          let context = canvas.getContext(&#39;2d&#39;)

          context.drawImage(img, 0, 0);
          
         &#47;&#47;context.clearRect(200,432, 1110, 670);
          let sectionImg = context.getImageData(200, 432, 1110, 75	0);
          let imgData = sectionImg.data;

          for(let i =1; i &lt; imgData.length;i += 4) {
          	  if (imgData[i-1] &lt; imgData[i]) {
                 let temp = imgData[i-1]
                 imgData[i - 1] = imgData[i]
                 imgData[i] = temp
          	  }
          	
          }

          context.putImageData(sectionImg, 200, 432); &#47;&#47; 复制代码

    	}
    	document.addEventListener(&#39;DOMContentLoaded&#39;, function(){
          loadImg()
    	})
    	
    &lt;&#47;script&gt;
  &lt;&#47;head&gt;
  &lt;body&gt;
    &lt;canvas id=&quot;canvas&quot;&gt;&lt;&#47;canvas&gt;
  &lt;&#47;body&gt;
&lt;&#47;html&gt;</div>2020-03-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/01/8e/48e7c474.jpg" width="30px"><span>一路向北</span> 👍（2） 💬（4）<div>老师在末尾提到了border、box-shadow、border-radius可以产生一些CSS黑魔法，而不是只定义边框、阴影和圆角，这里我很想知道，除了基本用途，他们可以产生什么样的黑魔法呢？有没有一些推荐的资料呢？</div>2020-01-03</li><br/><li><img src="" width="30px"><span>猫总</span> 👍（1） 💬（0）<div>原本实现控制RGB范围来手动抠图，不过在使用的时候发现并不直观，调整起来很随缘，回看了一遍课程才发现重点是HSL调色，改进之后还是能比较精准（主要是直观）的把鹦鹉给单独替换颜色了</div>2019-07-12</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJDSY5xBJ2PH4lqNtWJqhe1HcYkP7S9ibAXChONgCBX5pJ2gaU3icXhltQgqhzDyML3EzFicxPeE4Tiag/132" width="30px"><span>Geek_0bb537</span> 👍（1） 💬（0）<div>winter老师给我讲一下那个presentational attributes 看不懂</div>2019-04-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/7c/42/bcdbaaf7.jpg" width="30px"><span>Izayoizuki</span> 👍（1） 💬（0）<div>HSL感觉还是绘画游戏原画之类用得多，编程领域反而挺少，无论h5游戏还是客户端游戏理解一般都是rgb&#47;rgba</div>2019-04-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/61/c1/93031a2a.jpg" width="30px"><span>Aaaaaaaaaaayou</span> 👍（1） 💬（0）<div>canvas可以得到每个像素的rgb分量，是不是把蓝色和红色的值换一下就可以了？</div>2019-04-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/bb/47/b60ae3eb.jpg" width="30px"><span>你好，阳光</span> 👍（0） 💬（0）<div>老师，datauri+svg产生形状能举个例子吗？</div>2021-05-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/42/32/92d4a6b6.jpg" width="30px"><span>Corazon</span> 👍（0） 💬（0）<div>&lt;!DOCTYPE html&gt;
&lt;html lang=&quot;en&quot;&gt;

&lt;head&gt;
    &lt;meta charset=&quot;UTF-8&quot;&gt;
    &lt;meta name=&quot;viewport&quot; content=&quot;width=device-width, initial-scale=1.0&quot;&gt;
    &lt;title&gt;text&lt;&#47;title&gt;
    &lt;style&gt;
        &#47;* #canvas {
            width: 200px;
            height: 100px;
        } *&#47;
    &lt;&#47;style&gt;
&lt;&#47;head&gt;

&lt;body&gt;
    &lt;canvas id=&quot;canvas&quot; width=&quot;400&quot; height=&quot;400&quot;&gt;&lt;&#47;canvas&gt;
    &lt;button onclick=&quot;changeColor()&quot;&gt;Change Color&lt;&#47;button&gt;
    &lt;script&gt;
        let canvas = document.getElementById(&quot;canvas&quot;);
        let ctx = canvas.getContext(&quot;2d&quot;);
        let img = new Image();
        img.crossOrigin = &#39;anonymous&#39;;
        img.src = &quot;https:&#47;&#47;static001.geekbang.org&#47;resource&#47;image&#47;0f&#47;ac&#47;0f6f4cc6d564df9986e0108cb8a427ac.jpg&quot;;
        img.onload = function () {
            console.log(canvas.clientWidth);
            console.log(canvas.clientWidth &#47; img.width * img.height);
            ctx.drawImage(img, 0, 0, canvas.clientWidth, canvas.clientWidth &#47; img.width * img.height);
        }
        function changeColor() {
            let imgData = ctx.getImageData(0, 0, canvas.clientWidth, canvas.clientWidth &#47; img.width * img.height);
            let data = imgData.data;
            for (let i = 0; i &lt; data.length; i = i + 4) {
                if (data[i + 1] - data[i] &gt; 40 || data[i] + data[i + 1] + data[i + 2] &lt; 110) {
                    let temp = data[i]
                    data[i] = data[i + 1];
                    data[i + 1] = temp;
                }
            }
            ctx.putImageData(imgData, 0, 0);
        }

    &lt;&#47;script&gt;
&lt;&#47;body&gt;

&lt;&#47;html&gt;</div>2020-12-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e6/e5/b6980a7a.jpg" width="30px"><span>无双</span> 👍（0） 💬（0）<div>请问老师，我后台用的是Tomcat服务器，前端用ajax请求静态资源时会间隔会报412，也就是一次成功进入后台，一次报412，这该怎么解决呢？</div>2019-04-29</li><br/><li><img src="" width="30px"><span>Mupernb</span> 👍（0） 💬（0）<div>for(var i=0;i&lt;imgData.data.length;i++){
                [imgData.data[4*i+0],imgData.data[4*i+1]]=[imgData.data[4*i+1],imgData.data[4*i+0]]
            }</div>2019-04-28</li><br/>
</ul>