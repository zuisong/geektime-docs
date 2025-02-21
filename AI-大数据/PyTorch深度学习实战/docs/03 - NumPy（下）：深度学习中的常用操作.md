你好，我是方远。

通过上节课的学习，我们已经对NumPy数组有了一定的了解，正所谓实践出真知，今天我们就以一个图像分类的项目为例，看看NumPy的在实际项目中都有哪些重要功能。

我们先从一个常见的工作场景出发，互联网教育推荐平台，每天都有千万量级的文字与图片的广告信息流入。为了给用户提供更加精准的推荐，你的老板交代你设计一个模型，让你把包含各个平台Logo（比如包含极客时间Logo）的图片自动找出来。

![图片](https://static001.geekbang.org/resource/image/1e/5d/1ecb3ccdd0b408b0350e255f7e0c875d.png?wh=318x116)

想要解决这个图片分类问题，我们可以分解成数据加载、训练与模型评估三部分（其实基本所有深度学习的项目都可以这样划分）。其中数据加载跟模型评估中，就经常会用到NumPy数组的相关操作。

那么我们先来看看数据的加载。

## 数据加载阶段

这个阶段我们要做的就是把训练数据读进来，然后给模型训练使用。训练数据不外乎这三种：图片、文本以及类似二维表那样的结构化数据。

不管使用PyTorch还是TensorFlow，或者是传统机器学习的scikit-learn，我们在读入数据这一块，都会先把数据转换成NumPy的数组，然后再进行后续的一系列操作。

对应到我们这个项目中，需要做的就是把训练集中的图片读入进来。对于图片的处理，我们一般会使用Pillow与OpenCV这两个模块。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/27/fc/ca/c1b8d9ca.jpg" width="30px"><span>IUniverse</span> 👍（22） 💬（1）<div>import numpy as np 

scores=np.random.rand(256,256,2)
scores[:,:,0]=1-scores[:,:,1]
mask=np.argmax(scores,axis=2)
print(mask)</div>2021-10-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/3a/d2/cbd2c882.jpg" width="30px"><span>Yuhan</span> 👍（12） 💬（2）<div>方法一：
result = np.argmax(scores, axis=2)
方法二：
result = (scores[:, :, 0] &lt; scores[:, :, 1]).astype(&#39;int&#39;)</div>2021-10-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/05/17/63887353.jpg" width="30px"><span>王骥</span> 👍（5） 💬（5）<div>    im_pillow_c1_3ch = im_pillow.copy()
    im_pillow_c2_3ch = im_pillow.copy()
    im_pillow_c3_3ch = im_pillow.copy()
    # 只留 r 通道
    im_pillow_c1_3ch[:, :, 1:] = 0
    im_pillow_c1_3ch[:, :, 2:] = 0
    # 只留 g 通道 
    im_pillow_c2_3ch[:, :, 0:] = 0
    im_pillow_c2_3ch[:, :, 2:] = 0
    # 只留 b 通道 
    im_pillow_c3_3ch[:, :, 0:] = 0
    im_pillow_c3_3ch[:, :, 1:] = 0

老师，尝试用深拷贝来实现RGB通道过滤。R 显示没有问题，不过在显示 GB 通道的时候，获得的图片背景是黑色的。是我哪里理解出了问题吗？还是代码有问题？</div>2021-10-24</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJ0F94uoYZQicSOIfEfSr9gH7CTKibNBsS6d9PRDd8cy7bdTCF9jibXYtf0esGqsQAItHnElejIFovxg/132" width="30px"><span>cab</span> 👍（2） 💬（1）<div>OpenCV提取RGB通道很方便:
b, g, r = cv2.split(image)</div>2021-10-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2e/5b/ec/c667c792.jpg" width="30px"><span>nico</span> 👍（1） 💬（1）<div>请问下为什么这样合并下来都是红色底图的，第二种方式是可以的
im_pillow_c1_3ch = np.concatenate((im_pillow_c1, zeros), axis=2)
im_pillow_c2_3ch = np.concatenate((im_pillow_c2, zeros), axis=2)
im_pillow_c3_3ch = np.concatenate((im_pillow_c3, zeros), axis=2)</div>2022-06-27</li><br/><li><img src="" width="30px"><span>clee</span> 👍（1） 💬（2）<div>你好，为什么我执行 im_pillow_c1 = im_pillow_c1[:, :, np.newaxis] 后打印im_pillow_c1的shape变量，输出是  (116, 318, 1, 1, 1)， 而不是 (116, 318, 1,) 呢

</div>2021-10-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/15/26/f973aa31.jpg" width="30px"><span>平常心</span> 👍（1） 💬（3）<div>老师，您好！想请教一下，下边这个问题：

课程中，您提到：“其实我们还有一种更加简单的方式获得三个通道的 BGR 数据，只需要将图片读入后，直接将其中的两个通道赋值为 0 即可。”

im_pillow = np.array(im)
im_pillow[:,:,1:]=0

这个出来的结果是：R通道的图像，想请教一下，G、B通道的图像，用同样的办法实现，代码im_pillow[:,:,:]=0应该是什么？谢谢
</div>2021-10-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/2d/5d/49f92fac.jpg" width="30px"><span>文森特没有眼泪</span> 👍（1） 💬（1）<div>mask = (s[:,:,0] &gt; s[:,:,1])
mask = mask.astype(&#39;int&#39;)</div>2021-10-15</li><br/><li><img src="" width="30px"><span>Geek_f3b405</span> 👍（0） 💬（1）<div>用PIL和opencv打开同一张图片得到的图片一个是4维的一个是3维的是什么情况</div>2023-11-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/39/0e/b2/192fbab4.jpg" width="30px"><span>Difer</span> 👍（0） 💬（1）<div>方法一遍历了整个数组(可能在某些条件下有用，但相对耗时)，方法二则采用求特定轴上最大索引的方法
## mthod1
a = scores[:, :, [0]]
b = scores[:, :, [1]]
mask_flat = []
for x, y in zip(a.flat, b.flat):
	if x &gt; y:
		mask_flat.append(0)
	else:
		mask_flat.append(1)
   
mask_m1 = np.asarray(mask_flat).reshape(256, 256)

## method2
mask_m2 = np.argmax(scores, axis=2)

if (mask_m1 == mask_m2).all():
    print(True)
</div>2023-11-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/39/0e/b2/192fbab4.jpg" width="30px"><span>Difer</span> 👍（0） 💬（1）<div>我发现使用&quot;列表&quot;的形式进行取值，就可以直接获得shape为三维的数组，不知道方老师认可这样的操作吗？
im_pillow_c0 = im_pillow[:, :, [0]]   ### 注意 im_pillow[:, :, [0]] 与 原文的im_pillow[:, :, 0] 是不一样的
im_pillow_c1 = im_pillow[:, :, [1]]
im_pillow_c2 = im_pillow[:, :, [2]]

im_pillow_c0_3ch_m3 = np.concatenate((im_pillow_c0, z, z),axis=2)
im_pillow_c1_3ch_m3 = np.concatenate((z, im_pillow_c1, z),axis=2)
im_pillow_c2_3ch_m3 = np.concatenate((z, z, im_pillow_c2),axis=2)</div>2023-11-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/4b/f8/918870c5.jpg" width="30px"><span>峰老板牛逼</span> 👍（0） 💬（1）<div>课后习题没看懂</div>2022-08-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2e/e3/c4/68bf7e23.jpg" width="30px"><span>醒狮</span> 👍（0） 💬（1）<div>另有一点想向您说：
我是一名大二的学生，虽然和向您一样的业界佼佼者比不了，但是我把您的课程从头到尾学了一遍，每一个代码我都自己复现了一次，如果您有后面想继续出课的打算，我可以无偿帮您做一些力所能及的事情（比如一些基础部分的理解，和一些代码的操作，运行，翻译等工作），希望您做出的这么好的课程可以被更多人看见！</div>2022-08-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2e/e3/c4/68bf7e23.jpg" width="30px"><span>醒狮</span> 👍（0） 💬（1）<div>谢谢老师一直以来的回复，您之前说有没有就是进阶课程的建议。
我是这样理解的：
就比如您在18|图像分类（下）中提到的

“我先给你解读一下EfficientNet的这篇论文，这里我着重分享论文的核心思路还有我的理解，学有余力的同学可以在课后自行阅读原文。”

整篇文章通过您的解读看下来之后就发现很流畅，整体的思路很明晰，读了一遍都觉得读不够那种，虽然现在也在学习论文的撰写和理解，可是有很多时候还是找不到核心或者说读完一篇文章下来磕磕绊绊的，但是就是您这么加入自己的理解让后抽提论文的核心要素之后就觉得整篇文章很好理解了。就是怎么讲.......在我看来，我觉得如果日后您能出一个论文导读，或者说是不同模型的演练，我觉得效果可能会很好。不过无论如何，这套课程中真的很感谢您能分享这么多知识，从您的文字当中可以看出您是一个博学且友善的人！</div>2022-08-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2e/e3/c4/68bf7e23.jpg" width="30px"><span>醒狮</span> 👍（0） 💬（1）<div>老师，很感谢您的文档，请问日后会更新进阶版的课程以供参考学习吗，因为感觉咱们这个课程是入门，您讲得很好，希望可以能再讲一讲如何从1到无穷，谢谢老师！</div>2022-08-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2e/e3/c4/68bf7e23.jpg" width="30px"><span>醒狮</span> 👍（0） 💬（1）<div>from PIL import Image
im = Image.open(&#39;C:\\Users\\Pride\\Desktop\\uio.jfif&#39;)


import numpy as np
im_pillow = np.array(im)

im_pillow_R = im_pillow[:,:,0]
im_pillow_G = im_pillow[:,:,1]
im_pillow_B = im_pillow[:,:,2]

zeros = np.zeros(shape=(im_pillow.shape[0],im_pillow.shape[1],1))

im_pillow_R = im_pillow_R[:,:,np.newaxis]
im_pillow_G = im_pillow_G[:,:,np.newaxis]
im_pillow_B = im_pillow_B[:,:,np.newaxis]

im_pillow_R_p = np.concatenate((im_pillow_R,zeros,zeros),axis=2)

from matplotlib import pyplot as plt
plt.imshow(im_pillow_R_p.astype(np.uint8))
plt.savefig(&#39;.&#47;rgb_pillow.png&#39;, dpi=150)
plt.show()

老师好，想请教您一下，为什么这么打印我无论换上述提到的RBG哪种都会是红色的底，只是中间图像的颜色会改变，谢谢您</div>2022-07-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/93/65/6016b046.jpg" width="30px"><span>清风明月</span> 👍（0） 💬（1）<div>老师，我对c3也采用拼接数组方式一，生成一个3ch的对象，但是打印出来不是蓝色的，是红色通道，但是又不完全一样（那个橘色的Logo，红色通道是浅白，这个是黑色），是为什么？
im_pillow_c3= im_pillow_c3[:,:,np.newaxis]
im_pillow_c3_3ch = np.concatenate((im_pillow_c3,zeros),axis=2)</div>2022-07-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2e/5b/ec/c667c792.jpg" width="30px"><span>nico</span> 👍（0） 💬（1）<div>完整的代码：
im = Image.open(&#39;src&#47;jk.jpg&#39;)
print(im.size)

im_pillow = np.asarray(im)
print(im_pillow.shape)

im_pillow_c1 = im_pillow[:, :, 0]
im_pillow_c2 = im_pillow[:, :, 1]
im_pillow_c3 = im_pillow[:, :, 2]

zeros = np.zeros((im_pillow.shape[0], im_pillow.shape[1], 2))

# im_pillow_c1 = im_pillow_c1[:,:,np.newaxis]
# im_pillow_c2 = im_pillow_c2[:,:,np.newaxis]
# im_pillow_c3 = im_pillow_c3[:,:,np.newaxis]

# im_pillow_c1_3ch = np.concatenate((im_pillow_c1, zeros), axis=2)
# im_pillow_c2_3ch = np.concatenate((im_pillow_c2, zeros), axis=2)
# im_pillow_c3_3ch = np.concatenate((im_pillow_c3, zeros), axis=2)

im_pillow_c1_3ch = np.zeros(im_pillow.shape)
im_pillow_c1_3ch[:,:,0] = im_pillow_c1

im_pillow_c2_3ch = np.zeros(im_pillow.shape)
im_pillow_c2_3ch[:,:,1] = im_pillow_c2

im_pillow_c3_3ch = np.zeros(im_pillow.shape)
im_pillow_c3_3ch[:,:,2] = im_pillow_c3</div>2022-06-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/29/ba/3e11e36f.jpg" width="30px"><span>明天出发</span> 👍（0） 💬（2）<div>这里我使用OpenCV抽取了Ｂ、Ｇ、Ｒ通道，使用matploylib显示原图是按ＢＧＲ显示的，对每个通道显示时，反而显示出了Ｒ、Ｇ、Ｂ，是不是matploylib会自动检测识别？

import cv2
import numpy as np
from matplotlib import pyplot as plt

im = cv2.imread(&#39;images&#47;IMG_9324.PNG&#39;)
im_cv_c1 = np.array(im)
im_cv_c1[:, :, 1:] = 0
im_cv_c2 = np.array(im)
im_cv_c2[:, :, ::2] =0 #保留Green通道
im_cv_c3 = np.array(im)
im_cv_c3[:, :, :2] = 0

plt.subplot(2, 2, 1)
plt.title(&#39;Origin Image&#39;)
plt.imshow(im)
plt.axis(&#39;off&#39;)
plt.subplot(2, 2, 2)
plt.title(&#39;Blue Channel&#39;)
plt.imshow(im_cv_c1)
plt.axis(&#39;off&#39;)
plt.subplot(2, 2, 3)
plt.title(&#39;Green Channel&#39;)
plt.imshow(im_cv_c2)
plt.axis(&#39;off&#39;)
plt.subplot(2, 2, 4)
plt.title(&#39;Red Channel&#39;)
plt.imshow(im_cv_c3)
plt.axis(&#39;off&#39;)
plt.show()</div>2022-05-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/0f/53/92a50f01.jpg" width="30px"><span>徐洲更</span> 👍（0） 💬（1）<div>之前用plt.show展示OpenCV读取进来的图，发现颜色和原图不对，还以为是matplotlib的特性，经过老师提醒才意识到，原来是读取模式为BGR导致的。</div>2021-12-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/22/23/16c3ea01.jpg" width="30px"><span>zoob</span> 👍（0） 💬（2）<div>老师，为什么我用opencv读取的jpg图片时，im_cv2 = cv2.imread(&quot;JPG1.jpg&quot;),type(im_cv2)显示的是NoneType</div>2021-12-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e3/56/5fc6c92c.jpg" width="30px"><span>小伟</span> 👍（0） 💬（3）<div>img = Image.open(&quot;jike.jpg&quot;)
img_arr = np.asarray(img)
img_arr[:, :, 1:] = 0
print(img_arr)

老师 我在pycharm里面执行上面的代码可以正常的修改数组并打印，并没有报错，numpy的版本是1.21.4</div>2021-11-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/13/3e/d028cddd.jpg" width="30px"><span>王珎</span> 👍（0） 💬（1）<div>mask可以用argmax求，也可以直接用布尔运算
mask = np.argmax(scores)
mask = (scores[:,:,0] &lt; scores[:,:,1]).astype(int)</div>2021-11-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/13/3e/d028cddd.jpg" width="30px"><span>王珎</span> 👍（0） 💬（1）<div>用cv2读取图片后分3通道显示出来的图像与pillow读取的一致，通道顺序都是R、G、B，没有不一样哦

import cv2
im_cv2 = cv2.imread(&#39;jk.jpg’)
# R通道
im_cv2_c1 = im_cv2.copy()
im_cv2_c1[:,:,1:]=0
# G通道
im_cv2_c2 = im_cv2.copy()
im_cv2_c2[:,:,0]=0
im_cv2_c2[:,:,2]=0
# B通道
im_cv2_c3 = im_cv2.copy()
im_cv2_c3[:,:,:1]=0
</div>2021-11-03</li><br/><li><img src="" width="30px"><span>魔流剑风之痕</span> 👍（0） 💬（1）<div>plt.subplot(2, 2, 2)
plt.title(&#39;Red Channel&#39;)
plt.imshow(im_pillow_c1_3ch.astype(np.uint8))
plt.axis(&#39;off&#39;)
这里为什么一定要指定类型为无符号8位整型，不指定就不能出图</div>2021-10-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/0c/18/298a0eab.jpg" width="30px"><span>小强</span> 👍（0） 💬（1）<div>&quot;获得了每个通道的数据，接下来就需要生成一个 3 维全 0 数组，全 0 数组的形状除了最后一维为 2&quot;

为什么这里是2？一定是2吗？</div>2021-10-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/f3/d7/ae84f9b8.jpg" width="30px"><span>李柠檬🍋</span> 👍（0） 💬（1）<div>老师您好能麻烦您解释一下zeros = np.zeros((im_pillow.shape[0], im_pillow.shape[1], 2))中的shape[0]和shape[1]分别代表的是什么吗？</div>2021-10-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/13/3c/564938a9.jpg" width="30px"><span>xw</span> 👍（0） 💬（1）<div>mask=np.argmax(scores,axis=2)
老师，请问这样写对吗？</div>2021-10-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/63/cb/7c004188.jpg" width="30px"><span>和你一起搬砖的胡大爷</span> 👍（0） 💬（1）<div>老师，哪个仓库可以找到课程用到的代码呢？</div>2021-10-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/63/cb/7c004188.jpg" width="30px"><span>和你一起搬砖的胡大爷</span> 👍（0） 💬（1）<div>老师我觉得这就是个broadcasting...
mask = (scores[:, :, 0] &lt;= scores[:, :, 1])*1</div>2021-10-19</li><br/>
</ul>