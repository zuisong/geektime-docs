你好，我是月影。今天，我们要讲WebGL。

WebGL是最后一个和可视化有关的图形系统，也是最难学的一个。为啥说它难学呢？我觉得这主要有两个原因。第一，WebGL这种技术本身就是用来解决最复杂的视觉呈现的。比如说，大批量绘制复杂图形和3D模型，这类比较有难度的问题就适合用WebGL来解决。第二，WebGL相对于其他图形系统来说，是一个更“开放”的系统。

我说的“开放”是针对于底层机制而言的。因为，不管是HTML/CSS、SVG还是Canvas，都主要是使用其API来绘制图形的，所以我们不必关心它们具体的底层机制。也就是说，我们只要理解创建SVG元素的绘图声明，学会执行Canvas对应的绘图指令，能够将图形输出，这就够了。但是，要使用WebGL绘图，我们必须要深入细节里。换句话说就是，我们必须要和内存、GPU打交道，真正控制图形输出的每一个细节。

所以，想要学好WebGL，我们必须先理解一些基本概念和原理。那今天这一节课，我会从图形系统的绘图原理开始讲起，主要来讲WebGL最基础的概念，包括GPU、渲染管线、着色器。然后，我会带你用WebGL绘制一个简单的几何图形。希望通过这个可视化的例子，能够帮助你理解WebGL绘制图形的基本原理，打好绘图的基础。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/ab/33/75b1f724.jpg" width="30px"><span>筑梦师刘渊</span> 👍（51） 💬（2）<div>作业一   
查了下资料，webgl支持的图元类型有七种，分别是 gl.POINTS(点), gl.LINES(线段), gl.LINE_STRIP(线条), gl.LINE_LOOP(回路), gl.TRIANGLES(三角形), gl.TRIANGLE_STRIP(三角带), gl.TRIANGLE_FAN(三角扇)。
要绘制空心三角形，gl.LINE_STRIP(线条)、gl.LINES(线段)、 gl.LINE_LOOP(回路)都可以实现。 但是gl.LINES(线段)需要写入六个顶点([-1, -1, 0, 1,   0, 1, 1, -1,   1, -1,-1, -1]), gl.LINE_STRIP(线条)也需要写入四个顶点([-1, -1, 0, 1, 1, -1,-1, -1]),而gl.LINE_LOOP(回路)，只需要是三个顶点([-1, -1, 0, 1, 1, -1])，因此gl.LINE_LOOP(回路)是最佳选择

作业二
a. 先封装一个生成多边形顶点坐标数组的函数
function createCircleVertex(x, y, r, n) {
    const sin = Math.sin;
    const cos = Math.cos;
    const perAngel = (2 * Math.PI) &#47; n;
    const positionArray = [];
    for (let i = 0; i &lt; n; i++) {
        const angel = i * perAngel;
        const nx = x + r * cos(angel);
        const ny = y + r * sin(angel);
        positionArray.push(nx, ny);
    }
    return new Float32Array(positionArray);
}
b. 封装一个生成正多角星顶点的数组函数
function create2CircleVertex(x, y, r, R, n) {
    const sin = Math.sin;
    const cos = Math.cos;
    const perAngel = Math.PI &#47; n;
    const positionArray = [];
    for (let i = 0; i &lt; 2 * n; i++) {
        const angel = i * perAngel;
        if (i % 2 !== 0) {
            const Rx = x + R * cos(angel);
            const Ry = y + R * sin(angel);
            positionArray.push(Rx, Ry);
        } else {
            const rx = x + r * cos(angel);
            const ry = y + r * sin(angel);
            positionArray.push(rx, ry);
        }
    }
    return new Float32Array(positionArray);
}
1. 正四边形  const points = createCircleVertex(0, 0, 0.5, 4); 
2. 正五边形  const points = createCircleVertex(0, 0, 0.5, 5); 
3. 正六角星 const points = create2CircleVertex(0, 0, 0.3, 0.6, 6);

以上要绘制空心用gl.LINE_LOOP图元，实心用gl.TRIANGLE_FAN图元   
1)空心:gl.drawArrays(gl.LINE_LOOP, 0, points.length &#47; 2);
2)实心:gl.drawArrays(gl.TRIANGLE_FAN, 0, points.length &#47; 2);
</div>2020-06-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/14/66/57b04294.jpg" width="30px"><span>Cailven</span> 👍（17） 💬（1）<div>补充：vs不仅仅只有postion值，一般通过attribute 进行属性赋值。在图形学管顶点操作叫做VAO(vertex array object)，而vao操作的float数据底层是vbo。不过如果用了threejs后很多图元操作就依赖引擎直接就解决了，但在Threejs中依然可以通过shaderMatiral通过setAttribute给bufferGeometry的顶点赋值。

不过个人在这几年的图形学学习中觉得vs相对还是简单的，fs对于像素的操作很像当年给photoshop写滤镜的过程。不过如果真的是玩片元着色炫技可以看看shadertoy里关于用remaching技术构建距离场用体素算法在片元里构建另一个三维引擎的效果。希望月影大大回头可以针对这方面有所加餐。感谢！

不过这课程来的太晚，如果几年前能早点接触到这门课，估计会在图形学方面少走很多弯路，谢谢月影大大。</div>2020-06-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a9/71/78796fd5.jpg" width="30px"><span>xiao豪</span> 👍（8） 💬（2）<div>老师，将数据存入缓存再拿出来是有什么意义呢？</div>2020-07-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f1/18/63b9bd3c.jpg" width="30px"><span>宁康</span> 👍（5） 💬（1）<div>正n边型，r是外接圆半径

getPolygonPoints( n, r ){
      const stepAngle = 2*Math.PI &#47; n
      let initAngle = 0
      const pointArray = []
      for(let i = 0; i &lt; n; i++) {
        &#47;&#47; 存储x坐标
        pointArray.push(r * Math.cos(initAngle))
        &#47;&#47; 存储y坐标
        pointArray.push(r * Math.sin(initAngle))

        initAngle += stepAngle
      }

      return pointArray
    }

&#47;&#47; 正十边型坐标点
const ponitsArray = getPolygonPoints(10, 1)

const ponits = new Float32Array(ponitsArray)

gl.drawArrays(gl.TRIANGLE_FAN, 0, ponits.length &#47; 2)</div>2020-06-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f1/18/63b9bd3c.jpg" width="30px"><span>宁康</span> 👍（3） 💬（1）<div>1、gl_Position 设置顶点，这个我查了一下，第四个值设置为2.0也可以实现缩小一倍。
gl_Position = vec4(position, 0.0, 2.0);

2、空心三角形：
gl.drawArrays(gl. LINE_LOOP, 0, ponits.length &#47; 2)

3、绘制多边形
a.定义多边形的(x, y)坐标
const ponits = new Float32Array([
        -1, -1,
        0, -2,
        1, -1,
        1, 1,
        -1, 1
      ])
b.绘制多边形
gl.drawArrays(gl.TRIANGLE_FAN, 0, ponits.length &#47; 2)
</div>2020-06-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/5b/13/6db9ba58.jpg" width="30px"><span>Kevin</span> 👍（2） 💬（1）<div>实现了一个正多边形的样例，动态修改边数。
https:&#47;&#47;codesandbox.io&#47;s&#47;practice-canvas-vme4k?file=&#47;src&#47;pages&#47;RegularPolygonWebGL.vue</div>2020-07-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/5b/13/6db9ba58.jpg" width="30px"><span>Kevin</span> 👍（2） 💬（1）<div>问题一：
绘制空心三角形使用回路线条：gl.LINE_LOOP
    gl.drawArrays(gl.LINE_LOOP, 0, points.length &#47; 2);

WebGL可绘制的图元有以下7种，来源网络查找：https:&#47;&#47;www.jianshu.com&#47;p&#47;1e750f20ec23

点	gl.POINTS	
线段	gl.LINES	
线条	gl.LINE_STRIP
回路线条	gl.LINE_LOOP
三角形	gl.TRIANGLES
三角带	gl.TRIANGLE_STRIP	
三角扇	gl.TRIANGLE_FAN </div>2020-07-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/8d/94/a04cf407.jpg" width="30px"><span>国旗</span> 👍（1） 💬（1）<div>老师问下MDN文档里WebGL常数这儿，表格里十六进制的‘Value’表示的意思是类似于CPU指令寄存器么？
Getting GL parameter information这节BLEND_EQUATION，BLEND_EQUATION_RGB的value都是0x8009，也有点不理解
https:&#47;&#47;developer.mozilla.org&#47;en-US&#47;docs&#47;Web&#47;API&#47;WebGL_API&#47;Constants</div>2020-09-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a1/d6/9d99e5ef.jpg" width="30px"><span>不见飞刀</span> 👍（1） 💬（3）<div>&quot;图形中有多少个像素点，着色器程序在 GPU 中就会被同时执行多少次。&quot;

顶点着色器是否一样还是有几个顶点就执行多少次呢？
传给片元的varying变量会线性差值，那么插值这一步发生在哪呢？</div>2020-08-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e1/a5/ad8b5829.jpg" width="30px"><span>Geek_gmfq9e</span> 👍（1） 💬（1）<div>请问编写glsl有什么智能提示插吗，我用的vscode？</div>2020-08-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/ed/a9/662318ab.jpg" width="30px"><span>我母鸡啊！</span> 👍（1） 💬（1）<div>作业1 ： gl.drawArrays传入gl.LINE_LOOP</div>2020-07-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/ed/a9/662318ab.jpg" width="30px"><span>我母鸡啊！</span> 👍（1） 💬（1）<div>所以在webgl中最小的图元是三角形？</div>2020-07-03</li><br/><li><img src="" width="30px"><span>miaomiao</span> 👍（1） 💬（4）<div>月影老师，你好，有个问题想请教下，如果我想实现12条心电波形折线图，每条波形图的每个脉搏段会依据脉搏类型展示不同的颜色，用户交互：用户可以选择特定的脉搏段，统一修改这个脉搏段类型，这样类型变化，12条心电图的对应脉搏段颜色也变化。这种用canvas好还是webgl好？用canvas的话，需要去获取用户选定的范围，对画布元素进行局部重绘，目前有没有可以只通过更改数据，根据数据变化进行自动重绘的图形库？</div>2020-07-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/35/b5/a139a821.jpg" width="30px"><span>王子晨</span> 👍（1） 💬（2）<div>老师请问用webGL绘制复杂的图形，会不会设置多个顶点和片元着色程序？还是说一直在修改一个顶点和片元着色程序？</div>2020-07-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/81/aa/1f7a8e88.jpg" width="30px"><span>量子蔷薇</span> 👍（1） 💬（1）<div>我在codepen写了作业，https:&#47;&#47;codepen.io&#47;quantum-rose&#47;pen&#47;QWyqexL
不确定自己对WebGL绘图的机制理解对了没，关于封装复用代码那部分，感觉我可能复用了一些不需要复用的代码。期待之后的学习！
我的六角星只有描边，本质是在不清空画布的情况下画了两个三角形，不知道有没有更好的做法，如果是实心六角星，把我的代码中drawStar函数里的LINE_LOOP换成TRIANGLE_FAN就能画出来，但是其他n角星并不能正确画出来。</div>2020-06-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/f4/80/ed4f3bd9.jpg" width="30px"><span>DARLY</span> 👍（0） 💬（1）<div>还需要另外再学一下webGL的基础应用吗？或者在课程中会带着我们慢慢熟悉？</div>2021-10-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/d9/5c/4f8732e8.jpg" width="30px"><span>很好吃</span> 👍（0） 💬（1）<div>哈哈哈，太枯燥了，大大我学不下去了。</div>2020-11-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a1/d6/9d99e5ef.jpg" width="30px"><span>不见飞刀</span> 👍（0） 💬（2）<div>webgl的坐标系跟canvas的坐标系不一样嘛？ canvas的长宽设置的300，为什么points的坐标是1和-1</div>2020-08-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/8d/24/a2f886d3.jpg" width="30px"><span>Rexxar</span> 👍（0） 💬（1）<div>请问老师:
gl_Position = vec4(position, 1.0, 1.0);
在一个三维坐标系中用一个四维向量描述位置?
这思维向量里的三个参数position, 1.0, 1.0应该怎么理解?</div>2020-07-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/35/5d/be04d914.jpg" width="30px"><span>ailan</span> 👍（0） 💬（1）<div>老师，您好。我一开始未设置画布大小，画出的是等腰直角三角形；设置宽高相等时才能画出与示例相同的等腰三角形。那我是否可以这样理解，X轴的1单位长度 &#47; Y轴的1单位长度 = 画布的宽 &#47; 画布的高？</div>2020-06-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/fa/de/e927c333.jpg" width="30px"><span>浩荡如空气</span> 👍（1） 💬（1）<div>请问JS数据存入的Buffer和FrameBuffer是什么关系啊</div>2021-11-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b8/11/26838646.jpg" width="30px"><span>彧豪</span> 👍（1） 💬（1）<div>话说月影大大, 这个缓冲区和内存有什么关系?是一回事吗?那缓存呢, 缓冲区 内存 缓存这三者怎么理解呢?页面仔表示对这些计算机结构 原理方面的东西不是太了解, 求解答</div>2021-05-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/a5/ce/e4fae1bb.jpg" width="30px"><span>Gyrate</span> 👍（1） 💬（0）<div>老师，请问GLSL有什么方法可以debug吗？</div>2021-04-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/44/5e/a882dc64.jpg" width="30px"><span>北国风光</span> 👍（0） 💬（0）<div>1. 画空心的三角形: 将gl.drawArrays中的gl.TRIANGLES参数修改为gl.LINE_LOOP
2. 画四边形：布局合适的点，比如（-1，1）（-1，1）（1，-1）（1， 1）,然后将gl.drawArrays中的gl.TRIANGLES参数修改为gl.TEIANGLE_FAN
画其它四边形，布局位置上的点，然后选择合适的mode</div>2023-10-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/fd/25/8c9bf859.jpg" width="30px"><span>就像曹操贪慕着小乔</span> 👍（0） 💬（0）<div>光栅化的过程和渲染管线的概念怎么感觉有点相似</div>2023-03-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/12/b1/3a112b27.jpg" width="30px"><span>段帅帅</span> 👍（0） 💬（0）<div>```js
&#47;&#47; 步骤1
const bufferId = gl.createBuffer();
gl.bindBuffer(gl.ARRAY_BUFFER, bufferId);
gl.bufferData(gl.ARRAY_BUFFER, points, gl.STATIC_DRAW);
&#47;&#47; 步骤2
const vPosition = gl.getAttribLocation(program, &#39;position&#39;);获取顶点着色器中的position变量的地址gl.vertexAttribPointer(vPosition, 2, gl.FLOAT, false, 0, 0);给变量设置长度和类型gl.enableVertexAttribArray(vPosition);激活这个变量
```
搞不懂为啥这样就把points赋值给了position变量？或者position字段与points字段关联到一起？
</div>2022-07-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/cd/6d/928b0ffd.jpg" width="30px"><span>、轻</span> 👍（0） 💬（0）<div>这节课脑容量拉满</div>2022-03-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/3a/8d/f5e7a20d.jpg" width="30px"><span>何以解忧</span> 👍（0） 💬（0）<div>看了一下，推荐的shader book ,还有后面的内容，似乎很多操作都是在片元着色器中进行的，一版顶点着色器，我们只要传入顶点数据，不进行其他的处理么</div>2021-12-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/f2/01/fc1aad31.jpg" width="30px"><span>Leon two✌🏻</span> 👍（0） 💬（1）<div>老师你好，下面的 buffer 的数据绑定给顶点着色器的 position 变量这一步有些疑问

const bufferId = gl.createBuffer();
gl.bindBuffer(gl.ARRAY_BUFFER, bufferId);
gl.bufferData(gl.ARRAY_BUFFER, points, gl.STATIC_DRAW);

const vPosition = gl.getAttribLocation(program, &#39;position&#39;);获取顶点着色器中的position变量的地址
gl.vertexAttribPointer(vPosition, 2, gl.FLOAT, false, 0, 0);给变量设置长度和类型
gl.enableVertexAttribArray(vPosition);激活这个变量

获取position变量之后，好像也没有看到具体的赋值操作，他是怎么关联到 points 的buffer数据呢，而且如果我之前创建了多个 buffer，position变量又是指向的哪个呢

</div>2021-12-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/cb/87/0b727d00.jpg" width="30px"><span>我最爱吃大西瓜</span> 👍（0） 💬（0）<div>老师我想请教一个问题，就是web端，移动端，他们这些地图到底是怎么去绘制的呢，好像是加载的什么资源，直接就渲染出来了，我不知道它底层和原理到底是什么，如果我自己想做一个地图，是不是要用C++去开发引擎呢</div>2021-08-17</li><br/>
</ul>