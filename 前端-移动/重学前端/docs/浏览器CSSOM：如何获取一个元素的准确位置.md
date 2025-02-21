你好，我是winter。

在前面的课程中，我们已经学习了DOM相关的API，狭义的DOM API仅仅包含DOM树形结构相关的内容。今天，我们再来学习一类新的API：CSSOM。

我想，你在最初接触浏览器API的时候，应该都有跟我类似的想法：“好想要element.width、element.height这样的API啊”。

这样的API可以直接获取元素的显示相关信息，它们是非常符合人的第一印象直觉的设计，但是，偏偏 DOM API 中没有这样的内容。

随着学习的深入，我才知道，这样的设计是有背后的逻辑的，正如HTML和CSS分别承担了语义和表现的分工，DOM和CSSOM也有语义和表现的分工。

DOM中的所有的属性都是用来表现语义的属性，CSSOM的则都是表现的属性，width和height这类显示相关的属性，都属于我们今天要讲的CSSOM。

顾名思义，CSSOM是CSS的对象模型，在W3C标准中，它包含两个部分：描述样式表和规则等CSS的模型部分（CSSOM），和跟元素视图相关的View部分（CSSOM View）。

在实际使用中，CSSOM View比CSSOM更常用一些，因为我们很少需要用代码去动态地管理样式表。
<div><strong>精选留言（18）</strong></div><ul>
<li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTK6oo2CoIk3mBNfuro6TSWVCVxsWcfvt0GL1avaXbNdErjp7sussmunAU8eebbhUKcwV6Y7XeNYlA/132" width="30px"><span>Geek_ianp87</span> 👍（1） 💬（1）<div>display:inline;的元素会不会产生盒？</div>2019-10-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/02/a3/b7e7a787.jpg" width="30px"><span>Russell</span> 👍（0） 💬（1）<div>这个咋换行啊。。。 不好意思，老师好，我想咨询浏览器API的种类。 我可以认为是，DOM，BOM，CSSOM这几类么？</div>2019-04-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/35/d0/f2ac6d91.jpg" width="30px"><span>阿成</span> 👍（61） 💬（2）<div>Look via gist: https:&#47;&#47;gist.github.com&#47;aimergenge&#47;2bcf41ac4c4d2586e48ccd5cec5c9768

void function () {
  const canvas = document.createElement(&#39;canvas&#39;)

  canvas.width = document.documentElement.offsetWidth
  canvas.height = document.documentElement.offsetHeight

  canvas.style.position = &#39;absolute&#39;
  canvas.style.left = &#39;0&#39;
  canvas.style.right = &#39;0&#39;
  canvas.style.top = &#39;0&#39;
  canvas.style.bottom = &#39;0&#39;
  canvas.style.zIndex = &#39;99999&#39;

  document.body.appendChild(canvas)

  const ctx = canvas.getContext(&#39;2d&#39;)
  draw(ctx, getAllRects())

  function draw (ctx, rects) {
    let i = 0
    ctx.strokeStyle = &#39;red&#39;
    window.requestAnimationFrame(_draw)

    function _draw () {
      let {x, y, width, height} = rects[i++]
      ctx.strokeRect(x, y, width, height)
      if (i &lt; rects.length) {
        window.requestAnimationFrame(_draw)
      } else {
        console.log(&#39;%cDONE&#39;, &#39;background-color: green; color: white; padding: 0.3em 0.5em;&#39;)
      }
    }
  }

  function getAllRects () {
    const allElements = document.querySelectorAll(&#39;*&#39;)
    const rects = []
    const {x: htmlX, y: htmlY} = document.documentElement.getBoundingClientRect()
    allElements.forEach(element =&gt; {
      const eachElRects = Array.from(element.getClientRects()).filter(rect =&gt; {
        return rect.width || rect.height
      }).map(rect =&gt; {
        return {
          x: rect.x - htmlX,
          y: rect.y - htmlY,
          width: rect.width,
          height: rect.height
        }
      })
      rects.push(...eachElRects)
    })
    return rects
  }
}()
</div>2019-03-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/fb/29/aaa16933.jpg" width="30px"><span>welkin</span> 👍（14） 💬（6）<div>希望作者能讲一下虚拟dom
还有浏览器的重绘和重排
以及性能优化，跨域的常用操作(希望细致一点)
包括一些漏洞和攻击，比如xss，sql注入
还有一些技术栈，和一些对于前端需要了解的方案，比如离线方案等</div>2019-03-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/7b/85/385fe515.jpg" width="30px"><span>热心网友好宅💫</span> 👍（3） 💬（0）<div>一直忍着没问，哪来这么多猫片🤣</div>2019-04-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/60/de/5c67895a.jpg" width="30px"><span>周飞</span> 👍（3） 💬（0）<div>&lt;body&gt;
 &lt;canvas id=&quot;rect&quot;&gt;&lt;&#47;canvas&gt; 
&lt;script type=&quot;text&#47;javascript&quot;&gt;    
             const canvas = document.getElementById(&#39;rect&#39;);
             canvas.width =document.documentElement.getBoundingClientRect().width;
             canvas.height = document.documentElement.getBoundingClientRect().height;
             canvas.style.position=&quot;absolute&quot;;
             canvas.style.top=0;
             canvas.style.left=0;
             canvas.style.border=&#39;1px solid red&#39;;
             const ctx = canvas.getContext(&#39;2d&#39;);
             function travaldom(root){                    
               if(root.tagName &amp;&amp; root.tagName !==&#39;text&#39; &amp;&amp; root.tagName!==&#39;canvas&#39;){
                  const startX = root.getBoundingClientRect().x;
                  const startY = root.getBoundingClientRect().y;
                  const width = root.getBoundingClientRect().width;
                  const height = root.getBoundingClientRect().height;
                  ctx.beginPath();
                  ctx.lineWidth=&quot;1&quot;;
                  ctx.strokeStyle=&quot;blue&quot;;
                  ctx.rect(startX,startY,width,height);
                  ctx.stroke();
               }
               root.childNodes.forEach(node=&gt;{
                   travaldom(node);
               });
             }
             travaldom(document);
        &lt;&#47;script&gt;	
&lt;&#47;body&gt;</div>2019-04-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d6/dc/c454588f.jpg" width="30px"><span>痕近痕远</span> 👍（3） 💬（0）<div>请问老师，如何解决UI自动化测试，定位标签显示元素不可见的问题</div>2019-03-17</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83ericK6f30odtlIjX0Sw5cA3v259nLp2ibba5nQdzRk8cckZlruN6XtvEmRYKblibosiaiauVxh1NDxicESg/132" width="30px"><span>宋宋</span> 👍（3） 💬（0）<div>前面讲浏览器渲染时有讲到，CSS经过词法分析和语法分析被解析成一颗抽象语法树。
这个抽象语法树和CSSOM有什么关联么？因为很多文章都讲CSS经过词法分析和语法分析被解析成CSSOM，感觉很疑惑。</div>2019-03-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/f7/2f/10cbed82.jpg" width="30px"><span>pcxpccccx_</span> 👍（1） 💬（0）<div>冲冲冲</div>2020-03-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/02/a3/b7e7a787.jpg" width="30px"><span>Russell</span> 👍（1） 💬（0）<div>emm~~ 我又读了一遍文档，发现了对我来说很关键词，“狭义的”。 那我现在的理解是酱紫的。  广义的理解，就是BOM+DOM，CSSOM是DOM扩展的一部分；如果狭义的认为DOM就是树形结构的话，就可以分出来DOM、CSSOM两部分内容了。 我这样想对么？</div>2019-04-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/08/0f/9ed70716.jpg" width="30px"><span>非洲小白狼</span> 👍（0） 💬（0）<div>function elementTreeDFS(el, callback) {
    if (el instanceof HTMLElement) {
        callback(el);
        const children = Array.from(el.children);
        children.forEach(element =&gt; elementTreeDFS(element, callback));
    }
}
function renderCanvas() {
    const canvas = document.createElement(&#39;canvas&#39;);
    const ctx = canvas.getContext(&#39;2d&#39;);
    canvas.width = document.documentElement.offsetWidth || document.body.offsetWidth;
    canvas.height = document.documentElement.offsetHeight || document.body.offsetHeight;
    elementTreeDFS(document.documentElement, (el) =&gt; {
        const bounding = el.getBoundingClientRect();
        if (bounding.left || bounding.top || bounding.right || bounding.bottom || bounding.width || bounding.height) {
            ctx?.strokeRect(bounding.left, bounding.top, bounding.width, bounding.height);
        }
    });
    canvas.toBlob((blob) =&gt; {
        console.log(URL.createObjectURL(blob));
    }, &#39;image&#47;jpg&#39;, 1);
}
renderCanvas();
</div>2024-08-27</li><br/><li><img src="" width="30px"><span>Fiona B Y Fan</span> 👍（0） 💬（0）<div>通过document.getStyleSheets修改style以及window.getComputedStyle window.getBoundingClientRect window.getClientRects方法会导致重排和重绘，影响性能，不是应该少用吗</div>2022-04-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/98/fb/aa63be6f.jpg" width="30px"><span>pasico</span> 👍（0） 💬（0）<div>

function dfs(top, callback){
    let node = top
    let stack = Array.from(node.children).reverse()
    callback(node)
    while(stack.length){
        node = stack.pop()
        callback(node)
        stack.push(...Array.from(node.children).reverse())
    }
}

function traverse(){
    let body = document.body
    &#47;&#47; let color = 0
    let time = 0
    let count = 0
    let can = document.createElement(&#39;canvas&#39;)
    can.style.position = &#39;fixed&#39;
    can.style.top=0
    can.style.left=0
    let ctx = can.getContext(&#39;2d&#39;)
    const callback=(node)=&gt;{
        time+=50
        count++
        setTimeout(()=&gt;{            
            var {x,y,width,height} = node.getBoundingClientRect()
            console.log(&#39;count&#39;, count, node, x, y, width, height)
            if(node === body){
                can.style.width = width
                can.width = width
                can.style.height = height
                can.height = height
            }
            &#47;&#47; color++
            &#47;&#47; ctx.fillStyle=`rgb(${color%255},${color%255},${color%255})`;
            &#47;&#47; ctx.fillRect(x,y,width, height)
            ctx.strokeStyle = &#39;green&#39;;
            ctx.strokeRect(x, y, width, height);
        }, time)
    }
    dfs(body, callback)
    body.appendChild(can)
}

traverse()</div>2022-02-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/51/9f/1840385e.jpg" width="30px"><span>胡永</span> 👍（0） 💬（0）<div>
    const newWindow = window.open(&quot;about:blank&quot;, &quot;_blank&quot;, &quot;width=100,height=100,left=100,right=100&quot;)
    const canvas = newWindow.document.body.appendChild(newWindow.document.createElement(&#39;canvas&#39;));
    canvas.width = document.documentElement.offsetWidth
    canvas.height = document.documentElement.offsetHeight

    canvas.style.position = &#39;absolute&#39;
    canvas.style.left = &#39;0&#39;
    canvas.style.right = &#39;0&#39;
    canvas.style.top = &#39;0&#39;
    canvas.style.bottom = &#39;0&#39;
    canvas.style.zIndex = &#39;99999&#39;

    const ctx = canvas.getContext(&#39;2d&#39;);
    const { x: htmlX, y: htmlY } = document.documentElement.getBoundingClientRect()

    let tagsArr = new Set();
    void function getAllElementsTag() {
        const body = document.body;
        const { width, height } = document.documentElement.getBoundingClientRect();
        return recurtion(body);
    }()


    function drawCanvas(ele) {
        const offsetX = ele.getBoundingClientRect().x - htmlX;
        const offsetY = ele.getBoundingClientRect().y - htmlY;
        const { width, height } = ele.getBoundingClientRect();
        ctx.strokeStyle = &#39;red&#39;;
        ctx.strokeRect(offsetX, offsetY, width, height);
    }


    function recurtion(ele) {
        tagsArr.add(ele.nodeName.slice(0).toLowerCase());
        drawCanvas(ele)
        if (!ele.hasChildNodes()) return;
        ele.childNodes.forEach(item =&gt; {
            if (item.hasChildNodes()) {
                return recurtion(item)
            }
            if (!&#47;#&#47;.test(item.nodeName)) {
                drawCanvas(item)
            }

            tagsArr.add(item.nodeName.slice(0).toLowerCase())
        })
    }</div>2021-06-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/bc/e8/43109d54.jpg" width="30px"><span>Peter</span> 👍（0） 💬（0）<div>
&#47;&#47; 创建覆盖在网页上方的canvas
const cvs = document.createElement(&#39;canvas&#39;)
cvs.width = document.documentElement.scrollWidth;
cvs.height = document.documentElement.scrollHeight;
cvs.style.position = &#39;absolute&#39;;
cvs.style.zIndex = 1000;
cvs.style.left = 0;
cvs.style.top = 0;
ctx = cvs.getContext(&#39;2d&#39;);
ctx.strokeStyle=&quot;red&quot;;

&#47;&#47; 查找所有块元素，计算位置并在对应坐标绘制边框在canvas上。
const BlockLevel = [&#39;block&#39;, &#39;inline-block&#39;, &#39;inline-table&#39;, &#39;table&#39;, &#39;flex&#39;, &#39;grid&#39;, &#39;flow-root&#39;];
[].forEach.call(document.body.getElementsByTagName(&#39;*&#39;), (item) =&gt; {
    if (BlockLevel.indexOf(getComputedStyle(item).display) &gt; -1) {
        const rect = item.getBoundingClientRect();
        const { x, y, width, height } = rect;
        ctx.strokeRect(x, y, width, height);
    }
})

document.body.append(cvs);
</div>2020-06-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/26/22/dd505e6d.jpg" width="30px"><span>Yully</span> 👍（0） 💬（0）<div>removeRule被deleteRule取代了，建议用deleteRule，用法都一样</div>2020-06-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/ee/18/802b61e5.jpg" width="30px"><span>西伯利亚雪橇犬</span> 👍（0） 💬（0）<div>IE的edge版本scroll事件，事件中一个元素进行定位，有残影，谷歌就是平滑移动</div>2020-02-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/02/a3/b7e7a787.jpg" width="30px"><span>Russell</span> 👍（0） 💬（0）<div>不对，我觉得我这么理解不对。。。</div>2019-04-03</li><br/>
</ul>