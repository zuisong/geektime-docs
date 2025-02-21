今天我来带你进行KNN的实战。上节课，我讲了KNN实际上是计算待分类物体与其他物体之间的距离，然后通过统计最近的K个邻居的分类情况，来决定这个物体的分类情况。

这节课，我们先看下如何在sklearn中使用KNN算法，然后通过sklearn中自带的手写数字数据集来进行实战。

之前我还讲过SVM、朴素贝叶斯和决策树分类，我们还可以用这个数据集来做下训练，对比下这四个分类器的训练结果。

## 如何在sklearn中使用KNN

在Python的sklearn工具包中有KNN算法。KNN既可以做分类器，也可以做回归。如果是做分类，你需要引用：

```
from sklearn.neighbors import KNeighborsClassifier
```

如果是做回归，你需要引用：

```
from sklearn.neighbors import KNeighborsRegressor

```

从名字上你也能看出来Classifier对应的是分类，Regressor对应的是回归。一般来说如果一个算法有Classifier类，都能找到相应的Regressor类。比如在决策树分类中，你可以使用DecisionTreeClassifier，也可以使用决策树来做回归DecisionTreeRegressor。

好了，我们看下如何在sklearn中创建KNN分类器。

这里，我们使用构造函数KNeighborsClassifier(n\_neighbors=5, weights=‘uniform’, algorithm=‘auto’, leaf\_size=30)，这里有几个比较主要的参数，我分别来讲解下：
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/5c/86/97bb7338.jpg" width="30px"><span>Ricardo</span> 👍（31） 💬（1）<div>accuracy_score的参数顺序都错了，由于是计算真实标签和预测标签重合个数与总个数的比值，总能得到正确的答案，但是官方文档中写明的正确顺序应该是(y_true,y_pred)</div>2019-04-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/9d/93/945393c1.jpg" width="30px"><span>不做键盘侠</span> 👍（28） 💬（6）<div>为什么test只需要使用transform就可以了？test_ss_x = ss.transform(test_x）
</div>2019-02-08</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/KQpJHrQFQnezpyMlffXh9m9Dh6o8Z2yZXw8lEN73TyltgMGgDjhAz2cTbMpe2jgwWzkPr5Ribf2LgIDOE77kLdA/132" width="30px"><span>牛奶布丁</span> 👍（13） 💬（1）<div>老师，为什么做多项式朴素贝叶斯分类的时候，传入的数据不能有负数呢，之前老师讲文本分类的时候好像没有提到这一点？</div>2019-02-13</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaELDJp8RFJKyxHymHsQwJ9EKibjSPZGjxGPZcnxbbdMd4vHfMqLVPyvqOv0SEO1aibvSsydabFibnQDeA/132" width="30px"><span>Geek_12bqpn</span> 👍（12） 💬（2）<div>在做项目的时候，应该什么时候用Min-Max,什么时候用Z-Score呢？当我不做规范化的时候，反而准确率更高，这是为什么呢？在数据规范化该什么时候做不太理解，希望得到回复！</div>2019-09-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a3/87/c415e370.jpg" width="30px"><span>滢</span> 👍（7） 💬（1）<div>用代码计算来以下准确率：
knn默认k值为5 准确率:0.9756
knn的k值为200的准确率:0.8489
SVM分类准确率:0.9867
高斯朴素贝叶斯准确率:0.8111
多项式朴素贝叶斯分类器准确率:0.8844
CART决策树准确率:0.8400

K值的选取如果过大，正确率降低。 
算法效率排行 SVM &gt; KNN(k值在合适范围内) &gt;多项式朴素贝叶斯 &gt; CART &gt; 高斯朴素贝叶斯
</div>2019-04-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/0a/eb/6d6a94d2.jpg" width="30px"><span>Lee</span> 👍（3） 💬（1）<div>KNN 中的 K 值设置为 200，KNN 准确率: 0.8489，k值过大，导致部分未知物体没有分类出来，所以准确率下降了</div>2019-02-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/b8/21/c03839f1.jpg" width="30px"><span>FORWARD―MOUNT</span> 👍（2） 💬（2）<div>train_x与train_y都是训练集？
</div>2019-02-16</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/wJphZ3HcvhjVUyTWCIsCugzfQY5NAy6VJ0XoPLibDlcHWMswFmFe678zd0lUjFETia80NQhyQcVnGDlKgKPcRGyw/132" width="30px"><span>JingZ</span> 👍（2） 💬（1）<div>#knn 将K值调为200，准确率变为0.8489了，相比较默认K=5的准确率 0.9756，下降13%

from sklearn.datasets import load_digits
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

#加载数据
digits = load_digits()
data = digits.data

#数据探索
print(data.shape)

#查看第一幅图像
print(digits.images[0])
print(digits.target[0])

#数据可视化
plt.gray()
plt.imshow(digits.images[0])
plt.show()

#训练集 测试集
train_x, test_x, train_y, test_y = train_test_split(data, digits.target, test_size=0.25, random_state=33)

#采用 Z-Score 规范化
ss = preprocessing.StandardScaler()
train_ss_x = ss.fit_transform(train_x)
test_ss_x = ss.transform(test_x)

#创建 KNN 分类器
knn = KNeighborsClassifier(n_neighbors=200)

#用训练集训练
knn.fit(train_ss_x, train_y)

#用测试集预测
predict_y = knn.predict(test_ss_x)

#模型评估
print(&#39;KNN 准确率：%.4lf&#39; % accuracy_score(predict_y, test_y))</div>2019-02-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/b5/98/ffaf2aca.jpg" width="30px"><span>Ronnyz</span> 👍（1） 💬（1）<div>老师能解释下数据分割时random_state的取值有什么规范吗？
我自己测试的random_state=666与老师=33得出的准确度还是有一些差距的：
KNN准确率：0.9778
SVM准确率：0.9733
多项式朴素贝叶斯准确率：0.9067
CART决策树准确率：0.8489</div>2019-11-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/ab/5d/430ed3b6.jpg" width="30px"><span>从未在此</span> 👍（1） 💬（1）<div>那个标准化函数已经在训练集上拟合并产生了平均值和标准差。所以测试集用同样的标准直接拿来用就行了</div>2019-02-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/d4/78/66b3f2a2.jpg" width="30px"><span>斯盖丸</span> 👍（0） 💬（1）<div>老师，这个z-score规范化，把数据变成标准正态分布，在这个例子里的作用是什么？也就是说数据变化前是什么样的，变化后又是什么样的……如果不这么变化会带来什么结果？</div>2020-11-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/7d/2a/4c7e2e2f.jpg" width="30px"><span>§mc²ompleXWr</span> 👍（0） 💬（1）<div>为什么每次计算KNN和SVM分类器的准确率都是一样的？而朴素贝叶斯和决策树分类器每次计算的准确率都不一样呢？</div>2020-06-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/48/0b/9400afbb.jpg" width="30px"><span>LiLi</span> 👍（0） 💬（1）<div>“因为 KNN 算法和距离定义相关，我们需要对数据进行规范化处理，采用 Z-Score 规范化” 
--这里不是很明白，为何跟距离相关就选择Z-Score规范化？距离符合高斯分布？希望老师和同学们指点一下，谢谢！</div>2020-05-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/9d/eb/2c7f3d3b.jpg" width="30px"><span>Ricky</span> 👍（0） 💬（1）<div>问个问题：digits数据集中描述图像的格式什么？如果有一张外部的图片需要用这个模型来判断，应该怎么转化？
谢谢！</div>2020-04-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/bf/e3/2aa8ec84.jpg" width="30px"><span>鱼非子</span> 👍（0） 💬（1）<div>import numpy as np
import pandas as pd
from sklearn.datasets import load_digits
from sklearn import svm
from sklearn.neighbors import KNeighborsClassifier
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn import metrics
from sklearn.model_selection import train_test_split


digits = load_digits()
data = digits.data
print(data.shape)
print(digits.images[0])
plt.gray()
plt.imshow(digits.images[0])
plt.show()


# 分割数据，将25%的数据作为测试集，其余作为训练集（你也可以指定其他比例的数据作为训练集）
train_x, test_x, train_y, test_y = train_test_split(data, digits.target, test_size=0.25, random_state=33)
# 采用Z-Score规范化
ss = preprocessing.StandardScaler()
train_ss_x = ss.fit_transform(train_x)
test_ss_x = ss.transform(test_x)

model = KNeighborsClassifier()
model.fit(train_x,train_y)
predict = model.predict(test_x)
print(&quot;knn准确率：&quot;,metrics.accuracy_score(predict,test_y))

knn准确率： 0.9844444444444445</div>2020-03-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a3/87/c415e370.jpg" width="30px"><span>滢</span> 👍（0） 💬（1）<div>老师，想问个问题，KNeighborsClassifier的默认k值为5，我们可以给其设置默认k值。在上一节中讲到K值的选取用交叉验证，如果用sklearn实现的话，我们需要给KNeighborsClassifier设定不同的k值来寻找最优K值吗？</div>2019-04-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/5d/27/74e152d3.jpg" width="30px"><span>滨滨</span> 👍（0） 💬（1）<div>knn算法就是说，邻居大多数是什么你就是什么。
n_neighbors是邻居的数目

weights是权重
uniform是权重相同，求平均值
distance是根据距离的倒数
自定义

algorithm规定邻居选择的方式
auto根据数据自动选择
kd_tree，类似平衡二叉树，提高查找效率，多维空间的数据结构，一般不超过20维，对关键数据检索很方便
ball_tree，适用于维度大的
brute 暴力搜索，线性扫描

leaf_size是叶子数

k为200的时候准确率降低。
多项式分布没有负数，高斯分布可以有负数。
</div>2019-03-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/c1/1f/cc77944d.jpg" width="30px"><span>叮当猫</span> 👍（0） 💬（1）<div>n_neighbors =5时，准确率是0.9756，当n_neighbors =200时，准确率是0.8489，K值大不一定效果好，可能会欠拟合。

KNeighborsClassifier(n_neighbors=5, weights=&#39;uniform&#39;, algorithm=&#39;auto&#39;, leaf_size=30)
#参数n_neighbors，即knn中的k值，k值选取过小容易过拟合，k值选取过大鲁棒性强但欠拟合
#参数weights，用来确定邻居的权重，uniform表示所有邻居权重相同，distance代表权重是距离的倒数，与距离成反比，自定义函数表示可以自定义不同距离对应的权重。
#参数algorithm，用来规定计算邻居的方法，
#参数algorithm=auto根据数据情况自动选择合适的算法
#参数algorithm=kd_tree，kd树，多维空间的数据结构，方便对关键数据进行检索，适用维度少的情况，不超过20，大于20后效率下降
#参数algorithm=ball_tree，球树，和kd树医院都是多维空间数据结果，适用于维度大的情况
#参数algorithm=brute，暴力所搜，采用线性扫描，而不是通过构造树结果进行快速检索，训练集大的时候效率低
#参数leaf_size，代表构造kd树或球树时的叶子树，默认是30，调整它会影响到树的构造和搜索速度</div>2019-03-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f8/1e/0d5f8336.jpg" width="30px"><span>fancy</span> 👍（0） 💬（1）<div>1. KNN分类器的常用构造参数：
n_neighbors := k = 5(默认下)
weights = &#39;uniform&#39;&#47;&#39;distance&#39;&#47;自定义函数
algorithm=&#39;auto&#39;&#47;&#39;ball_tree&#39;&#47;&#39;kd_tree&#39;&#47;&#39;brute&#39;
leaf_size
2. 功能函数
fit(train_x,train_y)--训练分类器
predict(test_x)--用分类器预测测试集
3.改变K值
当k=200时，预测结果的准确性从97%左右下降到了84.89%</div>2019-03-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/62/a5/43aa0c27.jpg" width="30px"><span>TKbook</span> 👍（0） 💬（1）<div>from sklearn.metrics import accuracy_score
# 创建KNN分类器
knn = KNeighborsClassifier(n_neighbors=200)
knn.fit(train_ss_x, train_y)
predict_y = knn.predict(test_ss_x)
print(&#39;KNN准确率：%.4lf&#39; % accuracy_score(predict_y, test_y))

KNN准确率：0.8489</div>2019-02-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7d/05/4bad0c7c.jpg" width="30px"><span>Geek_hve78z</span> 👍（0） 💬（1）<div>1、项目中 KNN 分类器的常用构造参数，功能函数都有哪些
1）n_neighbors：即 KNN 中的 K 值，代表的是邻居的数量。
2）weights：是用来确定邻居的权重，有三种方式：
weights=uniform，代表所有邻居的权重相同；
weights=distance，代表权重是距离的倒数，即与距离成反比；
自定义函数，你可以自定义不同距离所对应的权重。大部分情况下不需要自己定义函数。
3）algorithm：用来规定计算邻居的方法，它有四种方式：
algorithm=auto，根据数据的情况自动选择适合的算法，默认情况选择 auto；
algorithm=kd_tree，也叫作 KD 树，适用于维度少的情况
algorithm=ball_tree，也叫作球树，球树更适用于维度大的情况；
algorithm=brute，也叫作暴力搜索，它和 KD 树不同的地方是在于采用的是线性扫描，而不是通过构造树结构进行快速检索。
4）leaf_size：代表构造 KD 树或球树时的叶子数，默认是 30，调整 leaf_size 会影响到树的构造和搜索速度。

2、KNN使用过程分为3步
1. 数据加载：我们可以直接从 sklearn 中加载自带的手写数字数据集；
2. 准备阶段：需要对数据集有个初步的了解，比如样本的个数、图像长什么样、识别结果是怎样的。你可以通过可视化的方式来查看图像的呈现。通过数据规范化可以让数据都在同一个数量级的维度。
3. 分类阶段：通过训练可以得到分类器，然后用测试集进行准确率的计算。

3、如果把 KNN 中的 K 值设置为 200，数据集还是 sklearn 中的手写数字数据集，再跑一遍程序，看看分类器的准确率是多少？
在创建KNN分类器的代码：
knn=KNeighborsClassifier(n_neighbors=200)
KNN 准确率：0.8489</div>2019-02-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a4/5a/e708e423.jpg" width="30px"><span>third</span> 👍（5） 💬（0）<div>KNN常用的构造参数
KNeighborsClassifier(n_neighbors=5,weights=&#39;uniform&#39;,algorithm=&#39;auto&#39;,leaf_size=30)
n_neighbors是邻居的数目

weights是权重
uniform是权重相同，求平均值
distance是根据距离的倒数
自定义

algorithm规定邻居的方式
auto根据数据自动选择
kd_tree，多维空间的数据结构，一般不超过20维，对关键数据检索很方便
ball_tree，适用于维度大的
brute包里搜索，线性扫描

leaf_size是叶子数

</div>2019-02-18</li><br/><li><img src="" width="30px"><span>Geek_dd384f</span> 👍（3） 💬（1）<div>#preprocessing.StandardScaler 和preprocessing.scale的区别
#使用sklearn.preprocessing.StandardScaler类，使用该类的好处在于可以保存训练集中的参数（均值、方差）直接使用其对象转换测试集数据。
ss = preprocessing.StandardScaler()
train_ss_x = ss.fit_transform(train_x)  #这里的fit_transform相当于先fit 再 transform
test_ss_x = ss.transform(test_x)     #这里没有使用fit_transform 就是因为使用了StandardScaler()
#使用sklearn.preprocessing.scale()函数，可以直接将给定数据进行标准化。
#train_ss_x = preprocessing.scale(train_x)
#test_ss_x = preprocessing.scale(test_x)
</div>2019-07-01</li><br/><li><img src="" width="30px"><span>Geek_35a6a8</span> 👍（1） 💬（0）<div>运行出的图像是什么意思，应该怎么看呢
</div>2022-05-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/04/60/64d166b6.jpg" width="30px"><span>Fan</span> 👍（0） 💬（0）<div>train_x, test_x, train_y, test_y = train_test_split(data, target, test_size=0.25, random_state=33) 这句代码中random_state=33 是什么意思呢？</div>2021-07-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/04/60/64d166b6.jpg" width="30px"><span>Fan</span> 👍（0） 💬（0）<div>贴下代码

from operator import imod
from scipy.sparse.construct import random
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn.metrics import accuracy_score
from sklearn.datasets import load_digits
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.tree import DecisionTreeClassifier
import matplotlib.pyplot as plt

#加载数据
digits = load_digits()
data = digits.data

# 数据探索
print(data.shape)
# print(data[0])

# 查看第一幅图像
print(digits.images[0])
print(digits.target[0])

plt.gray()
plt.imshow(digits.images[0])
plt.show()

train_x, test_x, train_y, test_y = train_test_split(data, digits.target, test_size=0.25, random_state=33)
# 采用Z-Score规范化
ss = preprocessing.StandardScaler()
train_ss_x = ss.fit_transform(train_x)
test_ss_x=ss.transform(test_x)

# 创建KNN分类器
knn=KNeighborsClassifier()
knn.fit(train_ss_x, train_y)
predict_y=knn.predict(test_ss_x)
print(&quot;KNN准确率: %.4lf&quot; % accuracy_score(test_y, predict_y))

# 创建SVM分类器
svm = SVC()
svm.fit(train_ss_x, train_y)
predict_y=svm.predict(test_ss_x)
print(&quot;SVM准确率: %0.4lf&quot; % accuracy_score(test_y, predict_y))

# 采用Min-Max规范化
mm=preprocessing.MinMaxScaler()
train_mm_x=mm.fit_transform(train_x)
test_mm_x=mm.transform(test_x)
# 创建Naive Bayes分类器
mnb=MultinomialNB()
mnb.fit(train_mm_x, train_y)
predict_y=mnb.predict(test_mm_x)
print(&quot;多项式朴素贝叶斯准确率: %.4lf&quot; % accuracy_score(test_y, predict_y))

# 创建CART决策树分类器
dtc=DecisionTreeClassifier()
dtc.fit(train_mm_x, train_y)
predict_y=dtc.predict(test_mm_x)
print(&quot;CART决策树准确率: %.4lf&quot; % accuracy_score(test_y, predict_y))

===============
KNN准确率: 0.9756
SVM准确率: 0.9867
多项式朴素贝叶斯准确率: 0.8844
CART决策树准确率: 0.8578</div>2021-07-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/da/2c/783413de.jpg" width="30px"><span>彭涛</span> 👍（0） 💬（1）<div>老师您好，请问这里的 KNN 分类器没看见 K 值是如何设置的，请问是使用了默认值吗？</div>2021-06-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/4a/35/66caeed9.jpg" width="30px"><span>完美坚持</span> 👍（0） 💬（0）<div>1. 如何实现用CV来选择合适的k
2. 深度学习+GPU运算怎么实现</div>2021-04-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/17/01/1c5309a3.jpg" width="30px"><span>McKee Chen</span> 👍（0） 💬（0）<div>KNN常用构造函数为KNeighborsClassifier(n_neighbors=5, weights=&#39;uniform&#39;, algorithm=&#39;auto&#39;, leaf_size=30)
其中:
n_neighbors代表K值，K值不宜太大，会欠拟合；也不宜太小，会过拟合；
weights代表邻居的权重；
algorithm代表计算邻居的方法
leaf_size达标构造KD树或球树的叶子数

计算逻辑: 对样本数据集按一定比例进行划分，训练集通过fit函数对模型进行训练，然后将测试集的数据输入训练好的模型中，再通过predict函数预测测试集的分类结果，最后通过accuracy_score计算模型的准确率

KNN是一种监督学习，可以用于图像识别、字符识别、文本分类，K值通过交叉验证得出，且K值不能太大

#当K值=200时，计算KNN分类器的准确率
#导入包
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.datasets import load_digits
from sklearn.naive_bayes import MultinomialNB
from sklearn.tree import DecisionTreeClassifier
#数据加载
digits = load_digits()
#获得图像和分类结果
data = digits.data
target = digits.target
#将样本集进行划分，选取25%作为测试集，其余为训练集
train_x, test_x, train_y, test_y = train_test_split(data, target, test_size=0.25, random_state=33)
#由于数据量级不统一，对数据进行标准化处理
ss = StandardScaler()
train_ss_x = ss.fit_transform(train_x)
test_ss_x = ss.transform(test_x)
#创建KNN分类器
knn = KNeighborsClassifier(n_neighbors=200)#取K值=200
#训练分类器
knn.fit(train_ss_x, train_y)
#预测测试集结果
predict_y = knn.predict(test_ss_x)
#计算准确率
print(&#39;KNN分类器准确率为:&#39;, accuracy_score(test_y, predict_y))

#输出结果
KNN分类器准确率为: 0.8488888888888889



        
</div>2020-12-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/33/07/8f351609.jpg" width="30px"><span>JustDoDT</span> 👍（0） 💬（0）<div>交作业：https:&#47;&#47;github.com&#47;LearningChanging&#47;Data-analysis-in-action&#47;tree&#47;master&#47;25-KNN%EF%BC%88%E4%B8%8B%EF%BC%89%EF%BC%9A%E5%A6%82%E4%BD%95%E5%AF%B9%E6%89%8B%E5%86%99%E6%95%B0%E5%AD%97%E8%BF%9B%E8%A1%8C%E8%AF%86%E5%88%AB%EF%BC%9F</div>2020-03-31</li><br/>
</ul>