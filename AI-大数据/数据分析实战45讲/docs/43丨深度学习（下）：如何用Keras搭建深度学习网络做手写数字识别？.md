通过上节课的讲解，我们已经对神经网络和深度学习有了基本的了解。这节课我就用Keras这个深度学习框架做一个识别手写数字的练习。

你也许还有印象，在KNN算法那节中，我讲到过Mnist手写数字识别这个数据集，当时我们采用的是mini版的手写数字数据集。实际上完整版的Mnist一共有60000个训练样本和10000个测试样本，这么庞大的数据量更适合用深度学习框架完成训练。

今天的学习目标主要有以下的几个方面：

1. 进一步了解CNN网络。CNN网络在深度学习网络中应用很广，很多网络都是基于CNN网络构建的，你有必要进一步了解CNN的网络层次，尤其是关于卷积的原理。
2. 初步了解LeNet和AlexNet。它们都是经典的CNN网络，我们今天的任务就是认识这些经典的CNN网络，这样在接触更深度的CNN网络的时候，比如VGG、GoogleNet和ResNet这些网络的时候，就会更容易理解和使用。
3. 对常用的深度学习框架进行对比，包括Tensorflow、Keras、Caffe、PyTorch、 MXnet和Theano。当选择深度学习框架的时候到底该选择哪个？
4. 使用Keras这个深度学习框架编写代码，完成第一个深度学习任务，也就是Mnist手写数字识别。
<div><strong>精选留言（21）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/a4/5a/e708e423.jpg" width="30px"><span>third</span> 👍（12） 💬（1）<div>卷积是一种操作，就像是过滤这个动作。
卷积核是卷积的一层滤网，
多个卷积核形成一个卷积层
卷积层像一个过滤层，过滤掉不需要的杂质</div>2019-03-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/33/07/8f351609.jpg" width="30px"><span>JustDoDT</span> 👍（10） 💬（1）<div>在python中，要使用OpenCV，要安装cv的package。在python代码中，看到import cv2。但pip install 的名称不是cv2、或者Opencv，而是opencv-python.

执行：

pip install opencv-python</div>2020-04-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/5d/27/74e152d3.jpg" width="30px"><span>滨滨</span> 👍（5） 💬（1）<div>1、卷积是矩阵运算。图像中不同数据窗口的数据和卷积核（一个滤波矩阵）作内积的操作叫做卷积。
2、卷积核就是图像处理时，给定输入图像，在输出图像中每一个像素是输入图像中一个小区域中像素的加权平均，其中权值由一个函数定义，这个函数称为卷积核。
3、卷积层：多个滤波器叠加便成了卷积层。</div>2019-05-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/2d/89/a01375a1.jpg" width="30px"><span>林</span> 👍（5） 💬（1）<div>讲的真好，希望老师也能出深度学习的课程</div>2019-04-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/c2/c3/da31c9c2.jpg" width="30px"><span>浩然</span> 👍（4） 💬（1）<div>至于为什么要翻转，举个例子，假如图像是这样： 0 0 0 1 0 ；卷积核是这样： 1 2 3，如果不翻转，结果就是 0 3 2 1 0，发现结果是反的。如果卷积核翻转成 3 2 1 ，那么结果就是 0 1 2 3 0 ，是正的。</div>2019-04-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/69/92/69c2c135.jpg" width="30px"><span>厚积薄发</span> 👍（2） 💬（1）<div>深度学习手写体数字识别
1.卷积，卷积核，卷积层的理解
卷积：是一种特殊的内积操作，先对卷积核进行180度的旋转，然后从第一个像素点依次与卷积核做内积操作。
卷积核：对图像做卷积操作的权重参数
卷积层：一个或多个卷积组成的过滤网

卷积的作用：提取特征，内积操作，把数据映射到线性空间。
激活函数的作用：把线性空间映射到非线性空间，让神经网络具有更强的表达能力
池化层的作用：对神经元的数据进行降维，降低的计算量
全连接层的作用：前一层的输出结果与当前神经元全部进行相连，做最后一层的分类任务，比如softmax</div>2020-11-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/c2/de/98cd7728.jpg" width="30px"><span>Lisa</span> 👍（2） 💬（2）<div>老师，配置每个层的时候填的数字有什么一般规律或范围吗？比如全连接层为什么填120呢？为什么填84呢？

model.add(Dense(120, activation=&#39;relu&#39;))
model.add(Dense(84, activation=&#39;relu&#39;))</div>2019-09-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/5d/27/74e152d3.jpg" width="30px"><span>滨滨</span> 👍（2） 💬（1）<div>CNN 网络结构中每一层的作用：它通过卷积层提取特征，通过激活函数让结果映射到非线性空间，增强了结果的表达能力，再通过池化层压缩特征图，降低了网络复杂度，最后通过全连接层归一化，然后连接 Softmax 分类器进行计算每个类别的概率。</div>2019-05-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a3/87/c415e370.jpg" width="30px"><span>滢</span> 👍（2） 💬（1）<div>个人对于卷积、卷积核、卷积层的理解是：
卷积是一种做内积运算的操作；
卷积核就是要做内积运算的规则；
卷积层是融合了一个或多个卷积核（即多个运算规则）的过滤网络</div>2019-04-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7d/05/4bad0c7c.jpg" width="30px"><span>Geek_hve78z</span> 👍（2） 💬（1）<div>参考链接：https:&#47;&#47;www.cnblogs.com&#47;readingintheway&#47;p&#47;4977669.html
卷积核为何要翻转才能计算的原因：
所谓的翻转只是因为你站立的现在是过去的未来，而因为h(t)始终不变，故h(1)其实是前一秒的h(1)，而前一秒的h(1)就是现在，所以从当前x(4)的角度往左看，你看到的是过去的作用。h(t)未翻转前，当从h(0)往右看，你看到的是现在对于未来的影响，当翻转h(t)之后，从h(0)往左看，你依次看到的越来越远的过去对现在的影响，而这个影响，与从x=4向左看的作用影响相对应（都是越来越远的过去），作用与作用的响应就对应起来了，这一切的本质，是因为你站立的时间观察点和方向在变。</div>2019-03-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/15/c6/f5c543ef.jpg" width="30px"><span>Switch</span> 👍（1） 💬（1）<div>老师，训练出来的模型，怎么用于实际使用呢？</div>2019-04-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/a5/e8/ca96d759.jpg" width="30px"><span>zy</span> 👍（1） 💬（1）<div>我是用pytorch，这几天的内容好熟悉呀</div>2019-03-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7d/05/4bad0c7c.jpg" width="30px"><span>Geek_hve78z</span> 👍（1） 💬（1）<div>参考链接：https:&#47;&#47;blog.csdn.net&#47;cheneykl&#47;article&#47;details&#47;79740810

1、卷积是矩阵运算。图像中不同数据窗口的数据和卷积核（一个滤波矩阵）作内积的操作叫做卷积。
2、卷积核就是图像处理时，给定输入图像，在输出图像中每一个像素是输入图像中一个小区域中像素的加权平均，其中权值由一个函数定义，这个函数称为卷积核。
3、卷积层：多个滤波器叠加便成了卷积层。</div>2019-03-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/05/fc/bceb3f2b.jpg" width="30px"><span>开心哥</span> 👍（0） 💬（1）<div>train_x = train_x &#47; 255   &#47;&#47; 这个是要干啥？</div>2020-05-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/0c/0f/93d1c8eb.jpg" width="30px"><span>mickey</span> 👍（15） 💬（0）<div>请教以下几个问题：
1、卷积核是怎么来的？
2、为什么卷积核要翻转180度？为什么不一开始就设置为已经转好的？
3、为什么要做这样乘？其背后的数学理论、思想和原理是什么？</div>2019-04-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/c2/c3/da31c9c2.jpg" width="30px"><span>浩然</span> 👍（5） 💬（0）<div>1、不同的卷积核应该对应不用的图像操作，比如可以通过改变卷积核实现图像锐化等操作
2、不旋转180的操作是滤波器，旋转后是卷积
</div>2019-04-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/94/6d/5cd6e8c7.jpg" width="30px"><span>张贺</span> 👍（2） 💬（0）<div>keras大概就是对tensorflow的再封装</div>2020-03-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/03/b5/61258e9b.jpg" width="30px"><span>wanghao</span> 👍（1） 💬（0）<div>文章可以系列了解一下各个知识点内容，但确实授人以渔的内容</div>2021-07-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a3/87/c415e370.jpg" width="30px"><span>滢</span> 👍（0） 💬（2）<div>有个疑问，卷积核翻转180度后，应该是
1     1     0
1     0    -1
0    -1   -1
但是在做运算的时候 ，为何成了
10*1   10*1  10*1
10*1   5*0   5*-1
10*0   5*-1 5 *-1
第一行第三个数不应该是10*0 吗 ？ 想问下这里是在怎么回事嘛？刚接触神经网络，对卷积还不太了解</div>2019-04-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/24/d5/04d68bc0.jpg" width="30px"><span>我不造⊙_⊙</span> 👍（0） 💬（1）<div>老师，对于多列文字的数据，想要分析出字段之间的关联关系应该怎么做啊？</div>2019-04-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/26/53/60fe31fb.jpg" width="30px"><span>深白浅黑</span> 👍（0） 💬（1）<div>CNN卷积网络神经结构
CNN卷积网络由三种层次构成，分别是卷积层、池化层和全连接层。
卷积
卷积是一种举证运算，在深度学习中，以图像识别为例，个人理解可以把卷积操作理解为，提取矩阵数据特征的一种手段。
卷积核
在进行卷积操作时，会用到卷积核，在图像识别中，个人理解可以将卷积核理解为一种滤波器，可以将图像中符合卷积核特性的特征进行提取。
卷积层
卷积层的作用是提取数据多维特征，方法是：使用卷积核，运用矩阵相乘的方式对二维数据进行卷积运算，提取数据的特征。通常卷积层使用多个卷积核，提取数据中的多种数据特征。

问题：
1、在卷积层与池化层之间，需要使用激活函数对数据体征进行非线性变换，对于激活函数的选取，有没有详细的说明，或者说，哪些激活函数适用于哪些非线性变化的情况？
2、有没有其他的实际项目经验，可以分享o(∩_∩)o </div>2019-03-22</li><br/>
</ul>