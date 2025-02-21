你好，我是月影。这一节课开始，我们学习3D图形的绘制。

之前我们主要讨论的都是2D图形的绘制，实际上WebGL真正强大之处在于，它可以绘制各种3D图形，而3D图形能够极大地增强可视化的表现能力。

用WebGL绘制3D图形，其实在基本原理上和绘制2D图形并没有什么区别，只不过是我们把绘图空间从二维扩展到三维，所以计算起来会更加复杂一些。

今天，我们就从绘制最简单的三维立方体，讲到矩阵、法向量在三维空间中的使用，这样由浅入深地带你去了解，如何用WebGL绘制出各种3D图形。

## 如何用WebGL绘制三维立方体

首先，我们来绘制熟悉的2D图形，比如矩形，再把它拓展到三维空间变成立方体。代码如下：

```
// vertex shader  顶点着色器
attribute vec2 a_vertexPosition;
attribute vec4 color;

varying vec4 vColor;

void main() {
  gl_PointSize = 1.0;
  vColor = color;
  gl_Position = vec4(a_vertexPosition, 1, 1);
}
```

```
// fragment shader   片元着色器 
#ifdef GL_ES
precision highp float;
#endif

varying vec4 vColor;

void main() {
  gl_FragColor = vColor;
}
```

```
...
// 顶点信息
renderer.setMeshData([{
  positions: [
    [-0.5, -0.5],
    [-0.5, 0.5],
    [0.5, 0.5],
    [0.5, -0.5],
  ],
  attributes: {
    color: [
      [1, 0, 0, 1],
      [1, 0, 0, 1],
      [1, 0, 0, 1],
      [1, 0, 0, 1],
    ],
  },
  cells: [[0, 1, 2], [0, 2, 3]],
}]);
renderer.render();
```

上面的3段代码，分别对应顶点着色器、片元着色器和基本的顶点信息。通过它们，我们就在画布上绘制出了一个红色的矩形。接下来，要想把2维矩形拓展到3维，我们的第一步就是要把顶点扩展到3维。这一步的操作比较简单，我们只需要把顶点从vec2扩展到vec3就可以了。

```
// vertex shader
attribute vec3 a_vertexPosition;
attribute vec4 color;

varying vec4 vColor;

void main() {
  gl_PointSize = 1.0;
  vColor = color;
  gl_Position = vec4(a_vertexPosition, 1);
}
```

**然后，我们需要计算立方体的顶点数据**。我们知道一个立方体有8个顶点，这8个顶点能组成6个面。在WebGL中，我们就需要用12个三角形来绘制它。如果每个面的属性相同，我们就可以复用8个顶点来绘制。而如果属性不同，比如每个面要绘制成不同的颜色，或者添加不同的纹理图片，我们还得把每个面的顶点分开。这样的话，我们一共需要24个顶点。
<div><strong>精选留言（6）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/c5/e9/4013a191.jpg" width="30px"><span>阿鑫</span> 👍（3） 💬（2）<div>正四面体光照效果，https:&#47;&#47;stupidehorizon.github.io&#47;graphics&#47;demo&#47;07_3d_box&#47; 一开始没注意每个面的法向量方向，结果有的面发向量朝里了，还 debugger 了半天。</div>2020-08-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/34/c1/4e4917f5.jpg" width="30px"><span>有一种踏实</span> 👍（1） 💬（0）<div>正四面体，就是取正立方体的四个非共棱顶点组成

function tetrahedron(size, colors = [[1, 0, 0, 1]]) {
      const h = 0.5 * size;
      const vertices = [
        [-h, -h, -h], &#47;&#47; 0
        [-h, h, -h], &#47;&#47; 1
        [h, h, -h], &#47;&#47; 2
        [h, -h, -h], &#47;&#47; 3
        [-h, -h, h], &#47;&#47; 4
        [-h, h, h], &#47;&#47; 5
        [h, h, h], &#47;&#47; 6
        [h, -h, h], &#47;&#47; 7
      ];

      const positions = [];
      const color = [];
      const cells = [];
      const normal = [];

      let colorIdx = 0;
      let cellsIdx = 0;
      const colorLen = colors.length;

      function triangle(a, b, c) {
        [a, b, c].forEach((i) =&gt; {
          positions.push(vertices[i]);
          color.push(colors[colorIdx % colorLen]);
        });
        cells.push([0, 1, 2].map(i =&gt; i + cellsIdx));

        const tmp1 = [];
        const tmp2 = [];
        const norm = [];
        cross(norm, subtract(tmp1, vertices[b], vertices[a]), subtract(tmp2, vertices[c], vertices[a]));
        normalize(norm, norm);
        normal.push(norm, norm, norm);

        colorIdx++;
        cellsIdx += 3;
      }

      triangle(1, 4, 6);
      triangle(1, 6, 3);
      triangle(1, 3, 4);
      triangle(6, 4, 3);

      return { positions, color, cells, normal };
    }</div>2024-02-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/11/b1/4379e143.jpg" width="30px"><span>H</span> 👍（1） 💬（0）<div>老师写的文章还不错！！！</div>2022-01-07</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83epcs6PibsP9vEXv4EibUw3bhQPUK04zRTOvfrvF08TwM67xPb1LBh2uRENHQwo2VqYfC5GhJmM7icxHA/132" width="30px"><span>蹦哒</span> 👍（0） 💬（0）<div>老师、同学们，立方体每个面的颜色为啥不会插值，而是同一个颜色呢？</div>2023-03-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/c2/77/3af6693c.jpg" width="30px"><span>JackWang</span> 👍（0） 💬（0）<div>老师，为什么我按照您的方法渲染后，发现圆柱体两个圆经常会被截断啊</div>2022-03-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/c1/64/3b994bd5.jpg" width="30px"><span>卖烧烤夫斯基</span> 👍（0） 💬（0）<div>老师是不是隐藏了一些webgl原始的细节。例如缓冲处理，着色器的初始化编译等。</div>2021-03-17</li><br/>
</ul>