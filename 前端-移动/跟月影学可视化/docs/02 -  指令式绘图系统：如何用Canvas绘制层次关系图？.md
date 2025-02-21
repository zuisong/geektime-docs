你好，我是月影。

Canvas是可视化领域里非常重要且常用的图形系统，在可视化项目中，它能够帮助我们将数据内容以几何图形的形式，非常方便地呈现出来。

今天，我们就在上一节课的基础上对Canvas进行稍微深入一些的介绍，来学习一下Canvas绘制基本几何图形的方法。

我主要会讲解如何用它的2D上下文来完成绘图，不过，我不会去讲和它有关的所有Api，重点只是希望通过调用一些常用的API能给你讲清楚，Canvas2D能做什么、要怎么使用，以及它的局限性是什么。最后，我还会带你用Canvas绘制一个表示省市关系的层次关系图（Hierarchy Graph）。希望通过这个可视化的例子，能帮你实践并掌握Canvas的用法。

在我们后面的课程中，基本上70~80%的图都可以用Canvas来绘制，所以其重要性不言而喻。话不多说，让我们正式开始今天的内容吧！

## 如何用Canvas绘制几何图形？

首先，我们通过一个绘制红色正方形的简单例子，来讲一讲Canvas的基本用法。

### 1. Canvas元素和2D上下文

对浏览器来说，Canvas也是HTML元素，我们可以用canvas标签将它插入到HTML内容中。比如，我们可以在body里插入一个宽、高分别为512的canvas元素。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/5e/a3/9670d4b4.jpg" width="30px"><span>Spring</span> 👍（36） 💬（1）<div>老师，有点不太理解translate的平移操作，平移后画布的坐标系是怎么发生变化的呢?
平移的是画布还是坐标系。</div>2020-06-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/3f/5f/053bc2da.jpg" width="30px"><span>特异型大光头</span> 👍（24） 💬（2）<div>原理大致听懂了,学着做个打砖块练习
https:&#47;&#47;codepen.io&#47;ysosu&#47;pen&#47;MWKorYj
问题:
function draw(ctx, node, {fillStyle = &#39;rgba(0, 0, 0, 0.2)&#39;, textColor = &#39;white&#39;} = {}) {};
里面这个{fillStyle = &#39;rgba(0, 0, 0, 0.2)&#39;, textColor = &#39;white&#39;} = {}没看懂
跟这样写的差别是啥function draw(ctx, node, fillStyle = &#39;rgba(0, 0, 0, 0.2)&#39;, textColor = &#39;white&#39; ) {};</div>2020-06-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f1/18/63b9bd3c.jpg" width="30px"><span>宁康</span> 👍（18） 💬（2）<div>借鉴了之前留言的朋友的部分逻辑重新开发了一个五子棋程序，主要修改了几个地方：
- 使用二维数组记录落子情况，方便后续判断胜负
- 重新获取光标后不进行整个棋盘的渲染，而是将上一个光标处局部修复
- 根据当前落子周围八个方向4个单位距离的棋盘中是否赢了

遇到的问题：
- 光标是用1个单位线宽绘制出来的，我用同样一个单位线宽去覆盖，发现覆盖不全，还会残留线段，最后只能加大线宽去覆盖，请问老师这个是什么问题？

五子棋在线预览：https:&#47;&#47;codesandbox.io&#47;s&#47;chess-demo-d2qgt</div>2020-06-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/3c/21/58f3740d.jpg" width="30px"><span>Geek_3469f6</span> 👍（10） 💬（2）<div>老师现在讲的还可以完全听懂，学习了之后立刻实践了以下。并且，学练结合，把以前的想法实现了下。这次没有偷懒。画了个五子棋盘+棋子，输赢判定逻辑还没写。
https:&#47;&#47;codepen.io&#47;maslke&#47;pen&#47;MWKoKKp</div>2020-06-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/9b/a5/90a5c106.jpg" width="30px"><span>随遇而安</span> 👍（9） 💬（4）<div>我尝试了用canvas绘制不规则多边形，如果想要添加鼠标交互事件，获取到鼠标的坐标之后，可以利用凸包算法判断点是否在不规则多边形内。</div>2020-06-24</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/OGMflcxuxblzCaAAZ9uXn0ak6rgrlxp9N8tt7sd1L8n3CRrfiblmLG3yJsSepwdc2DnLG9ibDqGdH8cnAQuIQlCg/132" width="30px"><span>春饼sama</span> 👍（3） 💬（1）<div>老师，获取json的都挂了</div>2021-07-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ab/33/75b1f724.jpg" width="30px"><span>筑梦师刘渊</span> 👍（3） 💬（6）<div>作业2:

1. 先封装一个清除圆形方法：           
 CanvasRenderingContext2D.prototype.clearCircle = function (x, y,r) {
                context.save();
                context.fillStyle = &quot;rgba(255,255,255,255)&quot;;
                context.beginPath();
                context.arc(x, y, r, 0, TAU);
                context.fill();
                context.restore();
            };
2. 检测鼠标是否在圆内(在圆内就先清除圆再绘制名称和新颜色):
            &#47;&#47; 鼠标检测移动到小圆就变色
            function isInCircle(ctx, mx, my, node) {
                const children = node.children;
                if (children) {
                    for (let i = 0; i &lt; children.length; i++) {
                        isInCircle(ctx, mx, my, children[i]);
                    }
                } else {
                    const { x, y, r } = node;
                    if ((my - y) * (my - y) + (mx - x) * (mx - x) &lt; r * r) {
                        console.log(x, y);
                        ctx.clearCircle(x, y, r);
                        ctx.fillStyle = &quot;rgba(255,0,0,0.2)&quot;;
                        ctx.beginPath();
                        ctx.arc(x, y, r, 0, TAU);
                        ctx.fill();
                        const name = node.data.name;
                        ctx.fillStyle = &quot;white&quot;;
                        ctx.font = &quot;1.5rem Arial&quot;;
                        ctx.textAlign = &quot;center&quot;;
                        ctx.fillText(name, x, y);
                    }
                }
            }
3. 监听鼠标mousemove事件(变换页面鼠标位置与canvas内坐标的关系)：
                canvas.addEventListener(&quot;mousemove&quot;, (e) =&gt; {
                    const x = e.clientX * 2;
                    const y = e.clientY * 2;
                    isInCircle(context, x, y, root);
                });</div>2020-06-26</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJ7hqBj1WIXVJgRwxVEg7fREAwI04BKRM8ibzVA8DIOaLSLqIrjw8UYr9GDUFFZW7mhBLC4hSp5r9g/132" width="30px"><span>gltjk</span> 👍（3） 💬（2）<div>提交一下第二个作业。之前纠结了一下怎么在鼠标移出城市时恢复小圆的颜色，最后决定专门做一个新的 canvas 叠在上面。另外鼠标移动的事件是不是要做个节流比较好？我试了一下感觉又不够流畅，就去掉了…… https:&#47;&#47;codepen.io&#47;gltjk&#47;pen&#47;GRomzQE</div>2020-06-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/f8/81/bff52f91.jpg" width="30px"><span>1830</span> 👍（2） 💬（1）<div>老师，JSON数据不能用了可以解决一下不，或者把数据结构要求贴一下我们模拟一下</div>2021-07-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/73/56/9cfb1e43.jpg" width="30px"><span>sheeeeep</span> 👍（2） 💬（2）<div>交作业：https:&#47;&#47;output.jsbin.com&#47;rirahom，思路基本和大家一致。
看完评论有两个主要的优化方法：
1. 减少重绘次数：判断是否在「圆」内 或 判断结果和上次不同，才进行重绘
2. 缩小重绘区域：进行局部清除和局部重绘</div>2020-07-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/ad/36/fc989053.jpg" width="30px"><span>River</span> 👍（2） 💬（2）<div>ifInCircle(pos, node) {
        if (pos[0] &lt; node.x + node.r &amp;&amp; pos[1] &lt; node.y + node.r) {
          let result = Math.pow((node.x - pos[0]), 2) + Math.pow((node.y - pos[1]), 2) &lt; Math.pow(node.r, 2)
          if (result) {
            if (node.children) {
              for (let childNode of node.children) {
                let has = this.ifInCircle(pos, childNode)
                if (has) {
                  break
                }
              }
            } else {
              if (!node.colorful) {
                if (this.chooseNode &amp;&amp; node !== this.chooseNode) {
                  this.chooseNode.colorful = false
                  this.clearAll()
                  this.draw(this.context, this.root)
                }
                this.draw(this.context, node, {fillStyle: &#39;rgba(90, 35, 35, 0.2)&#39;})
                this.chooseNode = node
                node.colorful = true
                return true
              }
            }
          }
        }
      },
好歹是实现了。。。不卡</div>2020-07-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/04/8e/e75ecc5e.jpg" width="30px"><span>浩明啦</span> 👍（2） 💬（1）<div>老师，鼠标移动圆发生变化的前提是需要遍历整个数据结构，当找到对应变化的点之后再重绘，但是这样我还是需要渲染多次，对于这个优化应该怎么写呢，实在没什么头绪了</div>2020-06-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/3f/5f/053bc2da.jpg" width="30px"><span>特异型大光头</span> 👍（1） 💬（2）<div>初学前端,请问下 draw() 方法这个参数是什么意思{fillStyle = &#39;rgba(0, 0, 0, 0.2)&#39;, textColor = &#39;white&#39;} = {}</div>2020-06-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/35/b5/a139a821.jpg" width="30px"><span>王子晨</span> 👍（1） 💬（1）<div>老师我看你本节课案例，里面的城市名字字体单位是rem，canvas对rem和view这些单位，支持的程度是怎样的？如果都支持，那俩个单位在使用时更倾向于使用哪种？</div>2020-06-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/78/87/a70878a5.jpg" width="30px"><span>Alex🦁</span> 👍（1） 💬（1）<div>2的交作业 感觉 有点卡顿。。。    
         function caculate(dx, dy, node) {
            let children = node.children;
            const { x, y, r } = node;
            if ((dx - x) * (dx - x) + (dy - y) * (dy - y) &lt; r * r) {
                node.color = 1;
                node.parent?node.parent.color = 0:&#39;&#39;;
            } else {
                node.color = 0;
            }
            if (children) {
                for (let i = 0; i &lt; children.length; i++) {
                    caculate(dx, dy, children[i]);
                }
            }
        }
        dom.onmousemove = (e) =&gt; {
            let x = e.pageX, y = e.pageY;
            caculate(x, y, root);
            context.clearRect(0,0,800,800)
            draw(context, root);
        }</div>2020-06-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ad/dd/970e7b4a.jpg" width="30px"><span>锐锐爱南球</span> 👍（0） 💬（1）<div>老师，平移和恢复那块有个小问题。就是第一次画图的时候，坐标系平移了，然后回撤，或者再平移回去不会对原来的图形造成影响吗？是不是可以这样说，我画A图形的时候，我的指令怎么操作，都是针对A，而当调用canvas.fill()的时候，A图形就已经被定格了，后面的变化是针对后面的图形了，所以我回撤之后，再画图形B，但是因为A被定格输出在canvas上了，所以后续的任何操作都不会对A造成影响，请问老师，可以这样理解吗？</div>2021-01-29</li><br/><li><img src="" width="30px"><span>百香果蜜</span> 👍（0） 💬（1）<div>看了评论，收获好多，交拓展一二的作业：
https:&#47;&#47;github.com&#47;xsometimes&#47;visual-practices&#47;blob&#47;main&#47;src&#47;view&#47;demo1&#47;index.js</div>2021-01-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/69/ec/ba28c292.jpg" width="30px"><span>RRRRRRRR</span> 👍（0） 💬（1）<div>来交作业了，讲一下大致思路和做的优化点。
作业一 https:&#47;&#47;output.jsbin.com&#47;qehuxuq，用三角函数画圆的方式来画椭圆，圆毕竟可以看作是长轴短轴相等的椭圆。
作业二 https:&#47;&#47;output.jsbin.com&#47;rafigod，用 Map 保存所有的城市位置和半径，判断鼠标位置与所有城市间的距离，同时用 throttle 函数，减少不必要的重绘。
</div>2020-11-09</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTL1H2TOJnNTblhmzJ2p88sTjvb86PuXP7A8HpCNKrfobuOc6Cxgy1UogZMIPTmD3VDGXZfTXIaWNw/132" width="30px"><span>Geek_cd63d9</span> 👍（0） 💬（1）<div>我之前用canvas完成的饼状图，样式尺寸和坐标尺寸不一致，在移动设备上图很模糊，老师可以解答一下吗，看过别人的回答，但还不是很清晰。</div>2020-08-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/57/0d/57eed3a3.jpg" width="30px"><span>三笠耶格尔</span> 👍（0） 💬（1）<div>请问老师，canvas大小是自动适应屏幕的大小，那么怎么才能让监听的鼠标位置信息和canvas中的点一一对应呢？</div>2020-07-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/bc/d0/7a595383.jpg" width="30px"><span>l_j_dota_1111</span> 👍（0） 💬（1）<div>老师能把触发城市变色的代码发出来吗，感觉好多地方没有优化好</div>2020-07-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/bc/d0/7a595383.jpg" width="30px"><span>l_j_dota_1111</span> 👍（0） 💬（2）<div>canvas改变背景色，是只能一直在上面重新画吗，只是更改背景色，却要不断的重复画圆和字，性能不受影响吗，我一直很好奇，虽然能检测在圆内，但是如何很好的变换，因为确实无法获得这个圆，更别说更改其颜色了</div>2020-07-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/43/fd/cf190699.jpg" width="30px"><span>Geek_frank</span> 👍（0） 💬（1）<div>案例数据中每个城市的名字长度最大为4，如果超过4个字，就会溢出。这该如何解决呢？可以让圆的大小适应名字的长度吗？
甚至可以让画布大小适应整个图的宽高，而不是固定的值【1600,1600】？
</div>2020-06-29</li><br/><li><img src="" width="30px"><span>Sam</span> 👍（0） 💬（1）<div>在做老师示例的时候，想做类似svg的hover效果，不知道怎么做，希望老师指点下。</div>2020-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/24/61/ab88f481.jpg" width="30px"><span>Maker</span> 👍（0） 💬（1）<div>几年前使用canvas写过一些小游戏 俄罗斯方块、坦克大战🤣现在都忘了</div>2020-06-26</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/OCfic4TOUJjGfeVe7I7hKNYsibiazsrGyRxoRbqVPkpl5j4y8vkKjqeApPh2akhriazOiaWWEwlXeSDGas1kQ4RLRPg/132" width="30px"><span>阿辉</span> 👍（13） 💬（5）<div>就看这一节课，就能写出一个五子棋？这些留言还挺让初学者有沮丧感的</div>2021-09-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/02/0a/5d81243a.jpg" width="30px"><span>良辰美景岂虚设</span> 👍（8） 💬（1）<div>层次结构数据接口https:&#47;&#47;s5.ssl.qhres.com&#47;static&#47;b0695e2dd30daa64.json 不能用了</div>2021-06-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/d7/f9/3cc65e57.jpg" width="30px"><span>log</span> 👍（1） 💬（1）<div>老师，请问一下，国家-》省份-》城市的圆圈的颜色深浅是通过啥控制的呀？看了一圈就发现了fillStyle，但是他就是rgbs(0,0,0,0.2)，请问怎么改变的呢？</div>2021-11-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/08/a2/8b703b6c.jpg" width="30px"><span>凹凸🔥</span> 👍（1） 💬（0）<div>let isInside = false;
  function isInCircle(context, mx, my, node) {
    const children = node.children;
    const { x, y, r, data } = node;
    if (children) {
      for (let i = 0; i &lt; children.length; i++) {
        if (isInside) {
          break;
        } else {
          isInCircle(context, mx, my, children[i])
        }
      }
    } else {
      if ((my - y) * (my - y) + (mx - x) * (mx - x) &lt; r * r) {
        if (hightItemName &amp;&amp; hightItemName === data.name) {
          console.log(&#39;已经存在渲染&#39;)
        } else {
          hightItemName = data.name
          isInside = true
        }
      }
    }
    if (isInside) {
      context.clearRect(0, 0, 1600, 1600);
      draw(context, root);
      isInside = false
    }
  }

看了大部分留言的代码 感觉都不太清晰，地区的名字可以作为一个ID ，ID只要不变可以优化渲染重复数，然后根据ID，去单独渲染对于的节点背景样式</div>2021-04-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/f8/ff/ae800f6b.jpg" width="30px"><span>我叫张小咩²⁰¹⁹</span> 👍（1） 💬（0）<div>全都利用老师封装好的`draw`方法绘制就好了  
```js
const redraw = () =&gt; {
    context.clearRect(0, 0, 1600, 1600)
    draw(context, root)
  }

  function isInCircle(node, mx, my) {
    const { children, data, x, y, r } = node
    if (children) {
      children.find((v) =&gt; isInCircle(v, mx, my))
    } else if ((mx - x) * (mx - x) + (my - y) * (my - y) &lt; r * r) {
      redraw()
      draw(context, node, { fillStyle: &#39;rgba(255,0,0,0.2)&#39; })
      return data
    }
  }

  function bindMouseEvent() {
    canvas.onmousemove = (e) =&gt; {
      let { x, y } = e
      &#47;&#47;! 注意画布宽高、样式宽高的比例
      x = x * 2
      y = y * 2
      const current = isInCircle(root, x, y)
      if (current) {
        console.log(&#39;In Circle&#39;, current)
      }
    }
  }

  draw(context, root)
  bindMouseEvent()
```</div>2021-02-17</li><br/>
</ul>