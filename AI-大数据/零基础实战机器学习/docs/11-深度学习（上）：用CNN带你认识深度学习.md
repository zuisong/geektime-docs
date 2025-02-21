你好，我是黄佳。

随着课程的不断深入，我们已经成功闯过两个关卡，获客关和变现关，学到了多种机器学习算法和模型的优化方法。今天这一讲，我们正式进入“激活关”。在这一关中，我们的主要任务是根据易速鲜花App的历史记录，借助深度学习神经网络，来预测它的日激活数趋势。通过“激活关”，相信你会对深度学习神经网络的原理和用法有一个比较深入的理解。

![](https://static001.geekbang.org/resource/image/a0/38/a02545b94937eaf80701766acf6d7038.jpg?wh=2284x1033)

不过，在正式进入这个项目之前呢，我们需要先打打基础，解决两个问题：1. 深度学习的原理是什么？2. 怎么搭建起一个深层神经网络CNN？这两个问题，我们将通过一个完整的小项目来搞定。

## 问题定义

易速鲜花的供应商每天都会发来大量的鲜花图片，不过，这些图片都没有按鲜花的类别进行分门别类，要是由人工来做的话，比较麻烦，成本也比较高。现在，我们需要根据易速鲜花大量已归类的鲜花图片，来建立一个能识别鲜花的模型，给未归类的图片自动贴标签。

![](https://static001.geekbang.org/resource/image/b9/44/b9b26c72c613730ccdf5a908771a9144.png?wh=585x386)

这是一个典型的分类问题，同时也是一个计算机视觉领域的图片识别问题。那么下面我们先来看看在哪里可以找到这些花的图片。

## 数据收集和预处理

不知道你是否还记得，在[第2讲](https://time.geekbang.org/column/article/413648)中我曾经说过，在深度学习的实战部分，我会带你去Kaggle网站用一用GPU、TPU等加速器。Kaggle网站是一个在线Jupyter Notebook平台，同时也是数据科学爱好者最好的学校交流场所，里面有数据集、源代码、课程资料等。我们这个项目会在Kaggle网站上完成。
<div><strong>精选留言（15）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/19/70/67/0c1359c2.jpg" width="30px"><span>qinsi</span> 👍（4） 💬（2）<div>opencv默认像素通道顺序是BGR，而matplotlib默认是RGB，直接画出来颜色就不对</div>2021-10-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ed/85/fb525a71.jpg" width="30px"><span>遂行</span> 👍（3） 💬（4）<div>kaggle导入keras的时候报错了，看了下环境预装的是TensorFlow
需要改成：from tensorflow.keras.utils import to_categorical
</div>2021-09-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/0b/f2/a8b0d8a6.jpg" width="30px"><span>千里马</span> 👍（2） 💬（2）<div>请问老师，神经网络里的参数，比如案例里的输出滤波器的数量64,2D卷积窗口的高度和宽度（2,2），这些参数的选择有什么依据吗？虽说是参数，可以变更，但总不能乱试吧</div>2022-03-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/3a/a3/696ab5af.jpg" width="30px"><span>黄小胖</span> 👍（1） 💬（1）<div>佳哥， label转化成one hot编码后，怎样反正返回原来的label，例如：结果显示第一个图片被 CNN 网络模型分类为第 4 种花（索引从 0 开始，所以类别 3 就是第 4 种花），也就是 Tulip（郁金香）。
这个是怎么知道第4种花就是Tulip（郁金香）。什么函数可以返回0是？？？，1是？？？，2是？？？，3是Tulip。</div>2021-10-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/38/4f/61/018352d4.jpg" width="30px"><span>静静呀</span> 👍（0） 💬（1）<div>已解决GPU找不到的问题</div>2023-11-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/38/4f/61/018352d4.jpg" width="30px"><span>静静呀</span> 👍（0） 💬（1）<div>老师，现在kaggle打开界面和您的不一样，没有直接勾选GPU的地方，可以帮忙看一下吗</div>2023-11-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/da/d9/f051962f.jpg" width="30px"><span>浩仔是程序员</span> 👍（0） 💬（2）<div>老师。你好，深度学习的模型让我有点困惑，不像传统机器学习是一个线性回归等比较具体的算法。而深度学习像是搭了一个网络，而一个网络怎么处理输入，更新内部的参数像是一个黑盒。另外，文中举例的是图片识别的，如果是文本分类的问题也是用同样的模型吗？</div>2023-03-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/36/80/81/791d0f5e.jpg" width="30px"><span>jinsiang_sh</span> 👍（0） 💬（1）<div>感觉还是比较懵诶？可能需要重复多理解一下</div>2023-03-23</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/uOByCQXa9iawXcJsqiaZuiaiakmDuPfs42zibzMWa0xdBNdANbxkI7hVwAJWHsFV4scI0P8qJUTGxlIhehRqiaE0bYMw/132" width="30px"><span>zoey</span> 👍（0） 💬（2）<div>有讨论群吗</div>2022-11-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/30/94/12c20983.jpg" width="30px"><span>宏伟</span> 👍（0） 💬（3）<div>kaggle注册时无法输入验证码，Hoxx也登不上。</div>2021-09-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/3a/a3/696ab5af.jpg" width="30px"><span>黄小胖</span> 👍（0） 💬（2）<div>佳哥，代码放在自己环境里跑有报错。
(&#39;You must install pydot (`pip install pydot`) and install graphviz (see instructions at https:&#47;&#47;graphviz.gitlab.io&#47;download&#47;) &#39;, &#39;for plot_model&#47;model_to_dot to work.&#39;)
---------------------------------------------------------------------------
AttributeError                            Traceback (most recent call last)
&lt;ipython-input-8-862f9ddda4a5&gt; in &lt;module&gt;
      1 from IPython.display import SVG # 实现神经网络结构的图形化显示
      2 from tensorflow.keras.utils import model_to_dot # 导入model_to_dot工具
----&gt; 3 SVG(model_to_dot(cnn).create(prog=&#39;dot&#39;, format=&#39;svg&#39;)) # 绘图
AttributeError: &#39;NoneType&#39; object has no attribute &#39;create&#39;
这两个包pydot  graphviz 已经用pip安装上了。</div>2021-09-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/66/8f/02be926d.jpg" width="30px"><span>在路上</span> 👍（0） 💬（1）<div>佳哥好，今天的课程帮助我了解了深度学习的整个流程，虽然还不知道卷积和池化的参数为什么是这样设置的，但是图示的过程很容易理解。体验了下kaggle，新建notebook之后，一直处于editor loading状态。</div>2021-09-22</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKO5hYDafHiapDIric7JpDOMsicrribkGh4UugsGkps4icOpBSM8G3sLKuQ5HuuskyiaWsAibyPXuibg7dBaA/132" width="30px"><span>davidhuxiangwei</span> 👍（0） 💬（1）<div>老师，我用kaggle 的 notebook，打开后一直出现 editor loading ，所有操作按钮都不能用，是什么原因呢？</div>2021-09-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/3d/dd/ad/2ce52eee.jpg" width="30px"><span>丶七分而已</span> 👍（0） 💬（0）<div>关于CNN准确率的计算这里，佳哥给的代码为：print(&#39;CNN的测试准确率为&#39;,&quot;{0:.2f}%&quot;.format(result[1]))
但我看result的结果里准确度为0.6730左右，是不是应该把代码改成print(&#39;CNN的测试准确率为&#39;,&quot;{0:.2f}%&quot;.format(result[1] * 100))，这样输出的准确率才是正确的(67.30%)，不然准确率就变成0.67%了，这好像不对吧</div>2024-12-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/32/2b/b9424077.jpg" width="30px"><span>aaaaa</span> 👍（0） 💬（0）<div>好多概念能够更加清晰</div>2021-09-22</li><br/>
</ul>