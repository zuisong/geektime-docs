你好，我是展晓凯。今天我们来继续学习移动平台的视频渲染。

在[第4讲](https://time.geekbang.org/column/article/545953)中，我们学习了OpenGL ES的基础概念，并且用OpenGL ES提供给我们的接口构建出了一个GLProgram；[第5讲](https://time.geekbang.org/column/article/546501)，我们学习了如何在移动平台搭建OpenGL ES的上下文环境。有了之前的准备，我们终于迎来了收获成果的时刻——让GLProgram在上下文环境中跑起来。

## GLSL语法与内建函数

在让GLProgram跑起来之前，我们还需要学习一下GLSL的语法和内建函数，这样才能够学会用GLSL书写着色器。

> GLSL是OpenGL的着色器语言，开发者自己能够编写着色器来完成渲染管线的顶点变换阶段和片元处理阶段。——第4讲内容回顾

我们这个部分的目标就是实现一组着色器来完成增强对比度的功能，但是这组着色器还不能直接看到效果，因为着色器是需要运行到显卡中的，要想看到效果还得等这节课学完之后，所以不要着急，我们慢慢来。

前面我们已经粗略地介绍过GLSL是什么了，但是一直没有准确地给它下过定义，其实就是担心你看到它的定义之后，觉得难以理解，而学到这里我们已经了解了[渲染管线以及着色器的职责](https://time.geekbang.org/column/article/545953)，GLSL理解起来也就容易多了。

GLSL（OpenGL Shading Language）就是OpenGL为了实现着色器给开发人员提供的一种开发语言。接触一门新的编程语言，一般要先看一下它的数据类型和修饰符，然后再学习这种语言的内嵌函数，最终再构建一个完整的程序，让它跑起来。我们先来看一下基本的数据类型。
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/eb/19/19e706a5.jpg" width="30px"><span>cc</span> 👍（0） 💬（1）<div>老师，咨询个问题：


glActiveTexture(GL_TEXTURE0);  &#47;&#47; 第一行
glBindTexture(GL_TEXTURE_2D, texId); &#47;&#47; 第二行
glUniform1i(mGLUniformTexture, 0); &#47;&#47; 第三行 

我自己实测不要第一行和第三行，也能绘制出来，请问下是什么原因。
</div>2022-10-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/f6/8b/c0bb693d.jpg" width="30px"><span>冰冰的冻结</span> 👍（0） 💬（3）<div>老师 android 平台部分设备在执行 GLES20.glDrawArrays 函数时 报 fault addr 0x0 问题 一般这种问题 你是怎么解决的呢</div>2022-08-10</li><br/><li><img src="" width="30px"><span>geek</span> 👍（0） 💬（2）<div>我们这个部分的目标就是实现一组着色器来完成增强对比度的功能，但是这组着色器还不能直接看到效果，因为着色器是需要运行到显卡中的，要想看到效果还得等这节课学完之后，所以不要着急，我们慢慢来。


老师这节课的GLSL代码，也没有实现增强对比度的功能。还要在片段shader中加上对比度的操作呀？</div>2022-08-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（3）<div>请教老师几个问题啊：
Q1：客户端是相对谁的？
文中几次提到了“客户端”，有“客户端”，就要有“server”。请问Server是谁？ （我的理解：”Server”是指OpgenGL ES，“客户端”是指调用OpenGL ES的上层应用）
Q2：安卓坐标系怎么会是0到1？
安卓两个坐标轴表示像素个数，像素个数都是几百的整数值，怎么会是0到1？
Q3：GL_NEAREST 的过滤方式，缩小的时候，效果是什么？</div>2022-08-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/8f/76/0ca1131c.jpg" width="30px"><span>臭屁哎</span> 👍（0） 💬（0）<div>老师，我想在实时播放视频（正在录制的视频）上显示自定义文字，为什么会报错glClear: GL error: 0x502，绘制的内容需要放在线程里面执行吗？是不是最后没有执行这句话glDeleteTextures(1, &amp;texId)？还有就是我的顶点着色器和片段着色器这么定义是对的吗？
1）顶点着色器代码：
&quot;uniform mat4 uMVPMatrix;\n&quot; +
                    &quot;attribute vec4 aPosition;\n&quot; +
                    &quot;attribute vec2 aTextureCoordinate;\n&quot; +
                    &quot;varying vec2 vTextureCoordinate;\n&quot; +
                    &quot;void main() {\n&quot; +
                    &quot;  gl_Position = uMVPMatrix * aPosition;\n&quot; +
                    &quot;  vTextureCoordinate = aTextureCoordinate;\n&quot; +
                    &quot;}&quot;;
2）片段着色器代码：
     &quot;precision mediump float;\n&quot; +
                    &quot;uniform sampler2D uTexture;\n&quot; +
                    &quot;varying vec2 vTextureCoordinate;\n&quot; +
                    &quot;void main() {\n&quot; +
                    &quot;  gl_FragColor = texture2D(uTexture, vTextureCoordinate);\n&quot; +
                    &quot;}&quot;;</div>2023-04-14</li><br/>
</ul>