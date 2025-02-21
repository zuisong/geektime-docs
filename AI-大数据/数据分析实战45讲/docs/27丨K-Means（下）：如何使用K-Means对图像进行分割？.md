上节课，我讲解了K-Means的原理，并且用K-Means对20支亚洲球队进行了聚类，分成3个梯队。今天我们继续用K-Means进行聚类的实战。聚类的一个常用场景就是对图像进行分割。

图像分割就是利用图像自身的信息，比如颜色、纹理、形状等特征进行划分，将图像分割成不同的区域，划分出来的每个区域就相当于是对图像中的像素进行了聚类。单个区域内的像素之间的相似度大，不同区域间的像素差异性大。这个特性正好符合聚类的特性，所以你可以把图像分割看成是将图像中的信息进行聚类。当然聚类只是分割图像的一种方式，除了聚类，我们还可以基于图像颜色的阈值进行分割，或者基于图像边缘的信息进行分割等。

## 将微信开屏封面进行分割

上节课，我讲了sklearn工具包中的K-Means算法使用，我们现在用K-Means算法对微信页面进行分割。微信开屏图如下所示：

![](https://static001.geekbang.org/resource/image/50/a2/50457e4e1fbd288c125364a6904774a2.png?wh=762%2A1355)  
我们先设定下聚类的流程，聚类的流程和分类差不多，如图所示：

![](https://static001.geekbang.org/resource/image/8a/78/8af94562f6bd3ac42036ec47f5ad2578.jpg?wh=2373%2A1087)  
在准备阶段里，我们需要对数据进行加载。因为处理的是图像信息，我们除了要获取图像数据以外，还需要获取图像的尺寸和通道数，然后基于图像中每个通道的数值进行数据规范化。这里我们需要定义个函数load\_data，来帮我们进行图像加载和数据规范化。代码如下：
<div><strong>精选留言（20）</strong></div><ul>
<li><img src="" width="30px"><span>淡魂</span> 👍（14） 💬（1）<div>请问老师。自己写Min-Max规范化公式的时候为什么不直接除以255，这样得到的数据也是在[0,1]之间，是因为那个值不可以为0吗？什么原因呢？</div>2019-02-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/26/53/60fe31fb.jpg" width="30px"><span>深白浅黑</span> 👍（7） 💬（2）<div>老师下面函数中，最后的参数代表什么意思？手册上显示的是n_feature，但没说具体的意义，不是很明白。
        c1 = kmeans.cluster_centers_[label[x, y], 2]
        c2 = kmeans.cluster_centers_[label[x, y], 1]
        c3 = kmeans.cluster_centers_[label[x, y], 0]</div>2019-02-19</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/icpJJI5qPlVwaZoOk6zKicZU9lFGkYyMJXmUXRBicibqBrrEvn7vKsL49ESrkibumd7qXUsXs7Yzj3Dib6npR6hB4ryQ/132" width="30px"><span>cua</span> 👍（4） 💬（4）<div>为什么会出现这个错误呢ValueError: too many values to unpack (expected 3)</div>2019-02-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/0c/0f/93d1c8eb.jpg" width="30px"><span>mickey</span> 👍（2） 💬（1）<div># -*- coding: utf-8 -*-
# 使用K-means对图像进行聚类，显示分割标识的可视化
import numpy as np
import PIL.Image as image
from sklearn.cluster import KMeans
from sklearn import preprocessing
from skimage import color

# 加载图像，并对数据进行规范化
def load_data(filePath):
    # 读文件
    f = open(filePath,&#39;rb&#39;)
    data = []
    # 得到图像的像素值
    img = image.open(f)
    # 得到图像尺寸
    width, height = img.size
    for x in range(width):
        for y in range(height):
            # 得到点(x,y)的三个通道值
            c1, c2, c3 = img.getpixel((x, y))
            data.append([c1, c2, c3])
    f.close()
    # 采用Min-Max规范化
    mm = preprocessing.MinMaxScaler()
    data = mm.fit_transform(data)
    return np.mat(data), width, height

# 加载图像，得到规范化的结果img，以及图像尺寸
img, width, height = load_data(&#39;.&#47;baby2.jpg&#39;)

# 用K-Means对图像进行16聚类
kmeans =KMeans(n_clusters=16)
kmeans.fit(img)
label = kmeans.predict(img)
# 将图像聚类结果，转化成图像尺寸的矩阵
label = label.reshape([width, height])
# 将聚类标识矩阵转化为不同颜色的矩阵
label_color = (color.label2rgb(label)*255).astype(np.uint8)
label_color = label_color.transpose(1,0,2)
images = image.fromarray(label_color)
images.save(&#39;baby_16.jpg&#39;)</div>2019-02-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a4/5a/e708e423.jpg" width="30px"><span>third</span> 👍（2） 💬（1）<div>问题：已经使用mm进行数据拟合转换了，为何还要使用np.mat()转换呢？作用在哪里？方便后面使用np.uint8吗？

注意：实战的时候，保存图片为jpg格式
如果是png格式的话，会出现4个值，导致赋值错误，(R, G, B, A)

import PIL.Image as image
import numpy as np
import pandas as pd
#载入数据
def load_data(file):
    with open(file,&#39;rb&#39;) as f:
        data=[]
        #打开文件
        img=image.open(f)
        width,height=img.size
        #获取特征数据
        for x in range(width):
            for y in range(height):
                c1,c2,c3=img.getpixel((x,y))
                data.append([c1,c2,c3])
        #进行mm规范化
        from sklearn.preprocessing import MinMaxScaler
        mm=MinMaxScaler()
        data=mm.fit_transform(data)
        return np.mat(data),width,height
data,width,height=load_data(&#39;.&#47;27&#47;baby.jpg&#39;)

#进行聚类
from sklearn.cluster import KMeans
kmeans=KMeans(n_clusters=16)
label=kmeans.fit_predict(data)

#可视化
#转换成图像矩阵
label=label.reshape([width,height])
#生成一张新图片
# pic_1=image.new(&quot;L&quot;,(width,height))
# #把像素信息写入
# #方法1写入灰度值
# for x in range(width):
#     for y in range(height):
#         #按照分类确定灰度值
#         pic_1.putpixel((x,y),int(label[x][y]*256&#47;16))
# pic_1.save(&#39;.&#47;27&#47;baby.jpg&#39;)

# #方法2
# # 使用模组，将表示矩阵转换为各种颜色的矩阵
# #使用label2rgb(label)*255转化,再把矩阵转化为unit8类型，无符号整数
# from skimage import color
# label_color=(color.label2rgb(label)*255).astype(np.uint8)
# #似乎都需要进行颠倒处理
# label_color=label_color.transpose(1,0,2)
# #使用fromarray把矩阵生成图片
# images=image.fromarray(label_color)
# images.save(&#39;.&#47;27&#47;baby_color_2.jpg&#39;)

#方法3获取对应原图
#创建新的图片
imges1=image.new(&#39;RGB&#39;,(width,height))
#写入图片
for x in  range(width):
    for y in range(height):
        #吧范围为0-255的数值投射到1-256
        #获取第一列即r的值
        c1=kmeans.cluster_centers_[label[x,y],0]
        c2 = kmeans.cluster_centers_[label[x, y], 1]
        c3 = kmeans.cluster_centers_[label[x, y], 2]
        imges1.putpixel((x,y),(int(c1*256)-1,int(c2*256)-1,int(c3*256)-1))
imges1.save(&#39;.&#47;27&#47;baby_yasuo.jpg&#39;)</div>2019-02-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/b5/98/ffaf2aca.jpg" width="30px"><span>Ronnyz</span> 👍（1） 💬（1）<div>import numpy as np
import PIL.Image as Image
from sklearn import preprocessing
from sklearn.cluster import KMeans
from skimage import color

#加载图片，并进行规范化
def load_data(filepath):
    #读图片
    f=open(filepath,&#39;rb&#39;)
    #获取图片像素
    img=Image.open(f)
    #获取图片尺寸和像素矩阵
    width,height =img.size
    data=[]
    for x in range(width):
        for y in range(height):
            #得到点（x,y）的R,G,B通道值
            r,g,b=img.getpixel((x,y))
            data.append([r,g,b])
    f.close()
    #采用min-max规范化
    mm=preprocessing.MinMaxScaler()
    print(&#39;原位置列表：&#39;)
    print(type(data))
    print(len(data))
    data=mm.fit_transform(data)
    return np.mat(data),width,height

#加载图片，得到规范化结果
img,width,height = load_data(&#39;.&#47;kmeans-master&#47;baby.jpg&#39;)
print(&#39;\n规范化的像素矩阵：&#39;)
print(type(img))
print(img.shape)
#用K-Means进行16聚类
kmeans = KMeans(n_clusters=16)
label=kmeans.fit_predict(img)

#将图像结果，转化成图像尺寸矩阵
label=label.reshape([width,height])

#创建颜色表示矩阵图
label_color = (color.label2rgb(label)*255).astype(np.uint8)
label_color=label_color.transpose(1,0,2)
print(&#39;\n像素颜色矩阵：&#39;)
print(label_color.shape)
images=Image.fromarray(label_color)
images.save(&#39;.&#47;kmeans-master&#47;baby_mark.jpg&#39;)

#创建新图像，保存聚类压缩之后的结果
img=Image.new(&#39;RGB&#39;,(width,height))
for x in range(width):
    for y in range(height):
        r1=kmeans.cluster_centers_[label[x, y],0]
        g1=kmeans.cluster_centers_[label[x, y], 1]
        b1=kmeans.cluster_centers_[label[x, y], 2]
        img.putpixel((x,y),(int(r1*256)-1,int(g1*256)-1,int(b1*256)-1))
img.save(&#39;.&#47;kmeans-master&#47;baby_new.jpg&#39;)</div>2019-11-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/7d/2a/4c7e2e2f.jpg" width="30px"><span>§mc²ompleXWr</span> 👍（0） 💬（2）<div>为什么要用np.mat(data)??
我用array()跑出来的结果完全是一样的啊。。</div>2020-07-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/7e/8b/3cc461b3.jpg" width="30px"><span>宋晓明</span> 👍（0） 💬（1）<div>极客时间 pc界面终于改了。。之前的界面找某篇文章费死个劲</div>2019-03-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/a1/74/3dfa4436.jpg" width="30px"><span>Rickie</span> 👍（0） 💬（1）<div>老师好，想请问下您聚类后得到的那张灰度图像有其他的设置吗？我使用跟您一样的代码，最后生成的图尺寸非常小，且一些细节并没有分类正确...不知道是什么原因？</div>2019-02-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/0c/0f/93d1c8eb.jpg" width="30px"><span>mickey</span> 👍（18） 💬（1）<div>import PIL.Image as image
导入的是pillow包，而非pil包。
pil包不支持64位，但是有pillow包代替用。</div>2019-02-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/34/13/d43ff5ed.jpg" width="30px"><span>vortual</span> 👍（9） 💬（0）<div>衷心希望老师能开一讲讲下数据规范化的问题。从之前的几讲总是遇到有些是minmax规范化，有些是需要正态分布，希望老师能讲下具体什么时候用哪种，而且规范化的好处，目前知道的是加快收敛和降低维度，但为啥还不是很清楚</div>2019-03-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7d/05/4bad0c7c.jpg" width="30px"><span>Geek_hve78z</span> 👍（3） 💬（2）<div>新概念总结
1、图像分割就是把图像分成若干个特定的、具有独特性质的区域并提出感兴趣目标的技术和过程。它是由图像处理到图像分析的关键步骤

有一个问题，最后一个案例中，图像分割，输出原图有什么意义</div>2019-02-23</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/0M3kK7d2sLapYh9VgqzQargLNkiaJbJZTDNjzLhm9s9FYbFUVDSKa74yvcvH5IHWgknuibmh9fObbrHXvfAib28IQ/132" width="30px"><span>手指饼干</span> 👍（1） 💬（0）<div>np.mat 已经废弃，需要用 np.array 替代</div>2024-06-17</li><br/><li><img src="" width="30px"><span>Neo</span> 👍（1） 💬（1）<div>这里好像没有设置评估聚类表现的环节？请问如何比较不同k值的表现呢</div>2020-02-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/5d/27/74e152d3.jpg" width="30px"><span>滨滨</span> 👍（1） 💬（0）<div>图像分割的主要工作在于数据的预处理，同时分割为几类需要人工指定这个很不方便</div>2019-04-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/38/4f/61/018352d4.jpg" width="30px"><span>静静呀</span> 👍（0） 💬（0）<div>老师，这个算法是不是可以用来压缩图片呢，通过聚类后图片确实变小了很多，也变模糊了，QQ相册里的图片是通过类似方式处理的吗</div>2023-10-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/17/01/1c5309a3.jpg" width="30px"><span>McKee Chen</span> 👍（0） 💬（0）<div>学习本节课的体会：
1.运用K-Means进行图像分割需要灵活运用矩阵与图像之间的转换，以及label2rgb、fromarray、transpose函数的使用和理解；
2.在数据规范化这一处理上可以使用kmeans自带的函数，也可以自行进行数据规范化(前提是知道数值所处的范围)；
3.对图像通道、灰度值等有了了解；
4.还是得多写代码，才能熟能生巧，将知识吸收成自己的。

#用 K-Means 聚类方法将 baby.jpg 的图片分割成 16 个部分
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
from skimage import color
import PIL.Image as image
import numpy as np

def load_data(filepath):
    #读取文件
    f = open(filepath, &#39;rb&#39;)
    data = []
    #得到图像的像素值
    img = image.open(f)#输入文件路径，选择可读写二进制文件模式
    #得到图像尺寸
    width, height = img.size
    for x in range(width):
        for y in range(height):
            #得到点 (x, y) 的三个通道值
            c1, c2, c3 = img.getpixel((x, y))
            data.append([c1, c2, c3])
    f.close()
    #采用MinMax规范化
    mm = MinMaxScaler()
    data = mm.fit_transform(data)
    return np.mat(data), width, height
#加载图像，得到规范化结果 img，以及图像尺寸 width， height
img, width, height = load_data(r&#39;C:\Users\Desktop\baby.jpg&#39;)
#用 K-Means 对图像进行16聚类
kmeans = KMeans(n_clusters=16)
label = kmeans.fit_predict(img)#获得聚类结果
#将图像聚类结果，转化成图像尺寸的矩阵
label = label.reshape([width, height])
#将聚类表示转化成不同颜色的矩阵
label_color = (color.label2rgb(label)*255).astype(np.uint8)
label_color = label_color.transpose(1, 0, 2)
images = image.fromarray(label_color)
#图片保存
images.save(r&#39;C:\Users\Desktop\baby_new_color.jpg&#39;)</div>2021-01-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/e2/c4/25acaa38.jpg" width="30px"><span>苹果</span> 👍（0） 💬（0）<div>聚类处理后，比如n_claster = 16 ,比较原图片更模糊些，可见，k值取越小，图片更模糊，用聚类算法使图片模糊，好像杀鸡焉用牛刀呀</div>2020-02-10</li><br/><li><img src="" width="30px"><span>三硝基甲苯</span> 👍（0） 💬（0）<div> 一开始对那个baby的图进行16份用Kmeans分类后的颜色感觉到怪怪的，折腾了好久才反应过来，这个是个分类，还好醒悟的早，不然这个要纠结好久，以为自己哪里有问题。。</div>2019-03-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/df/f0/ea4d36a7.jpg" width="30px"><span>梁利文</span> 👍（0） 💬（0）<div>那连接只能在手机上看，在电脑上看不到，不方便看案例和操作</div>2019-02-14</li><br/>
</ul>