讲完了SVM的原理之后，今天我来带你进行SVM的实战。

在此之前我们先来回顾一下SVM的相关知识点。SVM是有监督的学习模型，我们需要事先对数据打上分类标签，通过求解最大分类间隔来求解二分类问题。如果要求解多分类问题，可以将多个二分类器组合起来形成一个多分类器。

上一节中讲到了硬间隔、软间隔、非线性SVM，以及分类间隔的公式，你可能会觉得比较抽象。这节课，我们会在实际使用中，讲解对工具的使用，以及相关参数的含义。

## 如何在sklearn中使用SVM

在Python的sklearn工具包中有SVM算法，首先需要引用工具包：

```
from sklearn import svm
```

SVM既可以做回归，也可以做分类器。

当用SVM做回归的时候，我们可以使用SVR或LinearSVR。SVR的英文是Support Vector Regression。这篇文章只讲分类，这里只是简单地提一下。

当做分类器的时候，我们使用的是SVC或者LinearSVC。SVC的英文是Support Vector Classification。

我简单说一下这两者之前的差别。

从名字上你能看出LinearSVC是个线性分类器，用于处理线性可分的数据，只能使用线性核函数。上一节，我讲到SVM是通过核函数将样本从原始空间映射到一个更高维的特质空间中，这样就使得样本在新的空间中线性可分。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/15/fb/31/f0a884a3.jpg" width="30px"><span>Geek_dancer</span> 👍（46） 💬（2）<div>默认SVC训练模型，6个特征变量，训练集准确率：96.0%，测试集准确率：92.4%
默认SVC训练模型，10个特征变量，训练集准确率：98.7% ，测试集准确率：98.2%
LinearSVC训练模型， 6个特征变量， 训练集准确率：93.9%，测试集准确率：92.3%
LinearSVC训练模型， 10个特征变量， 训练集准确率：99.4%，测试集准确率：96.0%

结论：
1. 增加特征变量可以提高准确率，可能是因为模型维度变高，模型变得更加复杂。可以看出特征变量的选取很重要。
2. 训练集拟合都比较好，但是测试集准确率出现不同程度的下降。
3. 模型训练的准确率与人类水平之间偏差可以通过增加特征变量或采用新的训练模型来降低；模型训练的准确率与测试集测试的准确率之间的方差可以通过正则化，提高泛化性能等方式来降低。</div>2019-02-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a3/87/c415e370.jpg" width="30px"><span>滢</span> 👍（14） 💬（1）<div>利用SVM做分类，特征选择影响度大，要想SVM分类准确，人工处理数据这一步很重要</div>2019-04-18</li><br/><li><img src="" width="30px"><span>hlz-123</span> 👍（11） 💬（1）<div>首先要说，老师的课讲得非常好，深奥的算法和理论通过生动有趣的例子让人通俗易懂，兴趣盎然。
老师的本课案例中，对特征数据都做了Z-Score规范化处理（正态分布），准确率在90%以上，如果数据不做规范化处理，准确率在88%左右，我的问题：
1、数据规范化处理，是不是人为地提供了准确率？实际情况，数据不一定是正态分布。
2、模型建好后，在实际应用中去评估某个案例时，该案例数据是不是也要规范化，这样做是不是很麻烦并且数据对比不是很直观呢？</div>2019-03-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/a1/74/3dfa4436.jpg" width="30px"><span>Rickie</span> 👍（7） 💬（1）<div>思考题：
使用全部数据进行训练得到的准确率为0.9766，高于示例中的准确率。是否是由于多重共线性，使得测试结果偏高？</div>2019-02-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4d/49/28e73b9c.jpg" width="30px"><span>明翼</span> 👍（4） 💬（3）<div>老师我利用了结果和特征的相关性，选择特征，发现结果更好：
# 特征选择 按照结果和数据相关性选择特征准确率0.9707602339181286
features_remain = [&#39;radius_mean&#39;,&#39;perimeter_mean&#39;,&#39;area_mean&#39;,&#39;concave points_mean&#39;,&#39;radius_worst&#39;,&#39;perimeter_worst&#39;,&#39;area_worst&#39;,&#39;concave points_worst&#39;]</div>2019-11-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/9d/eb/2c7f3d3b.jpg" width="30px"><span>Ricky</span> 👍（2） 💬（1）<div>谢谢，提2个问题，
1）在实际应用中如何平衡特征变量和准确率的关系？有没有方法论？
增加特征变量意味着增加运算时间，提高准确率，但是这个得失怎么把握？同时如何评估会增加多少运算时间，一个一个尝试似乎比较费劲吧
2）此文的案例是选用平均值，丢弃了最大值和标准差，这个是多少案例的通用做法么？

谢谢</div>2020-04-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e3/d9/bda5e991.jpg" width="30px"><span>恬恬</span> 👍（2） 💬（2）<div>对比几组feature后，发现用feature_worst进行训练，效果更好。
1）SVC(kernel=&#39;linear&#39;)的测试集准确率为：99.42%；
2)  LinearSVC()的测试集准确率为：97.07%
2）SVC()的测试集准确率为：96.49%
觉得建模过程中，特征选择很重要，不同的数据集划分，正负样本是否平衡也会对结果有一定的影响，所以最好是可以采用交叉验证来训练模型。这个地方多次测试SVC(kernel=&#39;linear&#39;）和LinearSVC()，感觉还是会存在2个百分点左右的差异，这两个都算是线性分类，是因为采用了不同的线性核函数吗？还是其他参数或是方法差异的原因呢？</div>2020-03-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a3/87/c415e370.jpg" width="30px"><span>滢</span> 👍（2） 💬（1）<div>语言Python3.6  没有z-score规范化数据以及规范化后两种情况前提预测准确率，使用LinearSVC，选取所有mean属性

import  pandas as  pd
import  matplotlib.pyplot as  plt
import  seaborn as  sns
from sklearn.model_selection import  train_test_split
from sklearn import  svm
from sklearn import  metrics
from sklearn.preprocessing import  StandardScaler

#导入数据
path = &#39;&#47;Users&#47;apple&#47;Desktop&#47;GitHubProject&#47;Read mark&#47;数据分析&#47;geekTime&#47;data&#47;&#39;
data = pd.read_csv(path + &#39;breast_cancer&#47;data.csv&#39;)

#数据探索
pd.set_option(&#39;display.max_columns&#39;, None)
print(data.columns)
print(data.head(5))
print(data.describe())

#将特征字段进行分组
features_mean = list(data.columns[2:12])
features_se = list(data.columns[12:22])
features_worst = list(data.columns[22:32])

#数据清洗
#删除ID列
data.drop(&#39;id&#39;,axis=1,inplace=True)
#将良性B替换为0，将恶性替换为1
data[&#39;diagnosis&#39;] = data[&#39;diagnosis&#39;].map({&#39;B&#39;:0,&#39;M&#39;:1})

#将肿瘤诊断结果可视化
sns.countplot(data[&#39;diagnosis&#39;],label=&#39;count&#39;)
plt.show()
#计算相关系数
corr = data[features_mean].corr()
plt.figure(figsize=(14,14))

#用热力图呈现相关性，显示每个方格的数据
sns.heatmap(corr,annot=True)
plt.show()

#特征选择，选择所有的mean数据
feature_remain = [&#39;radius_mean&#39;, &#39;texture_mean&#39;, &#39;perimeter_mean&#39;,
       &#39;area_mean&#39;, &#39;smoothness_mean&#39;, &#39;compactness_mean&#39;, &#39;concavity_mean&#39;,
       &#39;concave points_mean&#39;, &#39;symmetry_mean&#39;, &#39;fractal_dimension_mean&#39;]

#抽取30%特征选择作为测试数据，其余作为训练集
train,test = train_test_split(data,test_size=0.3)
#抽取特征选择作为训练和测试数据
train_data = train[feature_remain]
train_result = train[&#39;diagnosis&#39;]
test_data = test[feature_remain]
test_result = test[&#39;diagnosis&#39;]

#创建SVM分类器
model = svm.LinearSVC()
#用训练集做训练
model.fit(train_data,train_result)
#用测试集做预测
prediction = model.predict(test_data)
#准确率
print(&#39;准确率:&#39;, metrics.accuracy_score(prediction,test_result))

#规范化数据，再预估准确率
z_score = StandardScaler()
train_data = z_score.fit_transform(train_data)
test_data = z_score.transform(test_data)
#用新数据做训练
new_model = svm.LinearSVC()
new_model.fit(train_data,train_result)
#重新预测
new_prediction = new_model.predict(test_data)
#准确率
print(&#39;准确率:&#39;,metrics.accuracy_score(new_prediction,test_result))</div>2019-04-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/b5/98/ffaf2aca.jpg" width="30px"><span>Ronnyz</span> 👍（1） 💬（1）<div>选取全部特征：
SVM分类器准确率： 0.9824561403508771
cross_val_score的准确率为：0.9727
linearSVM分类器的准确率： 0.9766081871345029
cross_val_score的准确率为：0.9652

选取mean相关特征：
SVM分类器准确率： 0.9239766081871345
cross_val_score的准确率为：0.9321
linearSVM分类器的准确率： 0.9298245614035088
cross_val_score的准确率为：0.9247

数据结果上看：
SVM的结果要好于linearSVM;
选取多特征的结果要好于选取少特征的结果</div>2019-11-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a4/5a/e708e423.jpg" width="30px"><span>third</span> 👍（1） 💬（1）<div>第二个，准确率 0.935672514619883。

感觉还蛮好用的，只是不是很熟练的使用各个算法做分类和回归</div>2019-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/79/9a/4f907ad6.jpg" width="30px"><span>Python</span> 👍（1） 💬（1）<div>老师可以用PCA进行特征选择吗？如果可以，那和你这种手动的方法比有什么差别</div>2019-02-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/8f/9e/a0a36b1c.jpg" width="30px"><span>晨曦</span> 👍（0） 💬（1）<div>老师，如果这个病症改为不得病，轻症，重症三个分类，不是二分类问题，对应改成分类序号，0,1,2。那么这套算法是不是也不算错</div>2021-01-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/a9/67/b53898d7.jpg" width="30px"><span>邹洲</span> 👍（0） 💬（1）<div># coding=utf-8
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
#导入sklearn中的SVM库
from sklearn import svm, metrics

#构造线性分类模型
model = svm.SVC(kernel=&quot;rbf&quot;,C=1.0,gamma=&quot;auto&quot;)
model2 = svm.LinearSVC()
&quot;&quot;&quot;
kernel :
    linear:线性模型，当模型为linearsvm时，就表明没有kernel参数
    poly：多项式模型
    rbf:高斯函数
    sigmoid:sigmoid核函数
C：目标函数的惩罚系数
gamma :核函数系数
&quot;&quot;&quot;

#实战开始--加载数据
data = pd.read_csv(&#39;data.csv&#39;,engine=&#39;python&#39;)
# pd.set_option(&#39;display.max_columns&#39;,None)
#查看一下数据信息
# print(data.columns)
# print(data.info())
# print(data.head(5))
# print(data[&#39;diagnosis&#39;].value_counts())

#数据处理
#id字段对于分类无用，删除即可
data.drop(&#39;id&#39;,axis=1,inplace=True)
#diagnosis字段为字符型，组需转换为数值型0 1
data[&#39;diagnosis&#39;] = data[&#39;diagnosis&#39;].map({&#39;M&#39;:1,&#39;B&#39;:0})

feature_mean = data.columns[1:11]
feature_se = data.columns[11:21]
feature_max = data.columns[21:31]


#统计一下肿瘤人数情况
sns.countplot(data[&#39;diagnosis&#39;],label=&#39;Count&#39;)
# plt.show()

#查看各个特征的相关度
corr = data[feature_mean].corr()
plt.figure(figsize=(14,14))
sns.heatmap(corr,annot=True)
# plt.show()

feature_sel = [&#39;radius_mean&#39;,&#39;texture_mean&#39;,&#39;smoothness_mean&#39;,&#39;compactness_mean&#39;,&#39;symmetry_mean&#39;,&#39;fractal_dimension_mean&#39;]


train_data,test_data = train_test_split(data,test_size=0.3)

train_feature = train_data[feature_sel]
train_label = train_data[&#39;diagnosis&#39;]
test_feature = test_data[feature_sel]
test_label = test_data[&#39;diagnosis&#39;]

#开始训练数据和测试数据
#采用Z-Score规范化处理，保证每一个特征维度的数据均值为0，方差为1
ss = StandardScaler()
train_feature = ss.fit_transform(train_feature)
test_feature = ss.transform(test_feature)

#开始预测
model.fit(train_feature,train_label)
model2.fit(train_feature,train_label)
predict_label = model.predict(test_feature)
predict_label2 = model2.predict(test_feature)
#准确度 -- 每次运行不一样
print(&quot;高斯准确率：&quot;,metrics.accuracy_score(test_label,predict_label))
print(&quot;线性准确度：&quot;,metrics.accuracy_score(test_label,predict_label2))


</div>2020-08-26</li><br/><li><img src="" width="30px"><span>朱一江</span> 👍（0） 💬（1）<div>我们所测的准确率是与train_y进行比较的吗
</div>2020-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/bf/e3/2aa8ec84.jpg" width="30px"><span>鱼非子</span> 👍（0） 💬（1）<div>import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn import svm
from sklearn import metrics


data = pd.read_csv(&quot;.&#47;data.csv&quot;)
pd.set_option(&#39;display.max_columns&#39;, None)
# print(data.head(5))
# print(data.columns)
# print(data.describe())

features_mean = list(data.columns[2:12])
features_se = list(data.columns[12:22])
features_worst = list(data.columns[22:32])

data.drop(&quot;id&quot;,axis=1,inplace=True)
data[&#39;diagnosis&#39;] = data[&#39;diagnosis&#39;].map({&#39;M&#39;:1,&#39;B&#39;:0})
# print(data.head(5))

sns.countplot(data[&#39;diagnosis&#39;],label=&quot;Count&quot;)
plt.show()

corr = data[features_mean].corr()
plt.figure(figsize=(14,14))
sns.heatmap(corr,annot=True)
plt.show()

features_remain = [&#39;radius_mean&#39;,&#39;texture_mean&#39;, &#39;smoothness_mean&#39;,&#39;compactness_mean&#39;,&#39;symmetry_mean&#39;, &#39;fractal_dimension_mean&#39;]
X_train, X_test, y_train, y_test = train_test_split(data[features_remain], data[&#39;diagnosis&#39;], test_size=0.3,random_state=0)

# 采用Z-Score规范化数据，保证每个特征维度的数据均值为0，方差为1
ss = StandardScaler()
X_train = ss.fit_transform(X_train)
X_test = ss.transform(X_test)

model = svm.SVC()
model.fit(X_train,y_train)

prediction = model.predict(X_test)
print(&quot;准确率：&quot;,metrics.accuracy_score(prediction,y_test))

准确率： 0.9239766081871345
</div>2020-03-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/10/57/1adfd4f7.jpg" width="30px"><span>追梦</span> 👍（0） 💬（1）<div>老师，请问用什么方法可以判定数据集是否为线性可分的呢</div>2019-10-14</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/3hZfficKPGCq2kjFBu9SgaMjibJTEl7iaW1ta6pZNyiaWP8XEsNpunlnsiaOtBpWTXfT5BvRP3qNByml6p9rtBvqewg/132" width="30px"><span>夜路破晓</span> 👍（0） 💬（1）<div>features_mean=list(data.columns[2:12]) 
这行报错:
TypeError: &#39;DataFrame&#39; object is not callable
如何改善?</div>2019-07-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/8e/76/6d55e26f.jpg" width="30px"><span>张晓辉</span> 👍（0） 💬（1）<div>采用linearSVC, 预测准确率更高。
import pandas as pd 
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler

data = pd.read_csv(&#39;data.csv&#39;)
data.drop(&#39;id&#39;, axis=1, inplace=True)

feature_names = list(data.columns)
feature_names.remove(&#39;diagnosis&#39;)

traindata, testdata = train_test_split(data, test_size=0.3)
train_x = traindata[feature_names]
train_y = traindata[&#39;diagnosis&#39;]
test_x = testdata[feature_names]
test_y = testdata[&#39;diagnosis&#39;]

ss = StandardScaler()
train_x = ss.fit_transform(train_x)
test_x = ss.transform(test_x)
                    
model = svm.LinearSVC()
model.fit(train_x, train_y)
prediction = model.predict(test_x)
print(&quot;The accuracy is %f&quot; % accuracy_score(prediction, test_y))</div>2019-05-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7d/05/4bad0c7c.jpg" width="30px"><span>Geek_hve78z</span> 👍（0） 💬（1）<div>import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn import svm
from sklearn import metrics

# 加载数据集，你需要把数据放到目录中
data = pd.read_csv(&quot;.&#47;breast_cancer_data-master&#47;data.csv&quot;)

# 数据探索
# 因为数据集中列比较多，我们需要把 dataframe 中的列全部显示出来
pd.set_option(&#39;display.max_columns&#39;, None)
print(data.columns)
print(data.head(5))
print(data.describe())

# 将特征字段分成 3 组
features_mean= list(data.columns[2:12])
features_se= list(data.columns[12:22])
features_worst=list(data.columns[22:32])

# 数据清洗
# ID 列没有用，删除该列
data.drop(&quot;id&quot;,axis=1,inplace=True)
# 将 B 良性替换为 0，M 恶性替换为 1
data[&#39;diagnosis&#39;]=data[&#39;diagnosis&#39;].map({&#39;M&#39;:1,&#39;B&#39;:0})

# 将肿瘤诊断结果可视化
sns.countplot(data[&#39;diagnosis&#39;],label=&quot;Count&quot;)
plt.show()
# 用热力图呈现 features_mean 字段之间的相关性
corr = data[features_mean].corr()
plt.figure(figsize=(14,14))
# annot=True 显示每个方格的数据
sns.heatmap(corr, annot=True)
plt.show()

# 特征选择
#features_remain = [&#39;radius_mean&#39;,&#39;texture_mean&#39;, &#39;smoothness_mean&#39;,&#39;compactness_mean&#39;,&#39;symmetry_mean&#39;, &#39;fractal_dimension_mean&#39;] 
features_remain = data.columns[1:31]
print(features_remain)
print(&#39;-&#39;*100)

# 抽取 30% 的数据作为测试集，其余作为训练集
train, test = train_test_split(data, test_size = 0.3)# in this our main data is splitted into train and test
# 抽取特征选择的数值作为训练和测试数据
train_X = train[features_remain]
train_y=train[&#39;diagnosis&#39;]
test_X= test[features_remain]
test_y =test[&#39;diagnosis&#39;]

# 采用 Z-Score 规范化数据，保证每个特征维度的数据均值为 0，方差为 1
ss = StandardScaler()
train_X = ss.fit_transform(train_X)
test_X = ss.transform(test_X)


# 创建 SVM 分类器
model = svm.LinearSVC()
# 用训练集做训练
model.fit(train_X,train_y)
# 用测试集做预测
prediction=model.predict(test_X)
print(&#39;准确率: &#39;, metrics.accuracy_score(prediction,test_y))

------
准确率:  0.9649122807017544</div>2019-04-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/c7/a3/1e2f9f5a.jpg" width="30px"><span>圆圆的大食客</span> 👍（0） 💬（1）<div># -*- coding: utf-8 -*-
&quot;&quot;&quot;
Created on Sun Mar 17 23:18:31 2019

@author: xcma1
&quot;&quot;&quot;
 
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn import metrics

# 加载数据集，你需要把数据放到目录中
data = pd.read_csv(&quot;.&#47;data.csv&quot;)
# 数据探索
# 因为数据集中列比较多，我们需要把 dataframe 中的列全部显示出来
pd.set_option(&#39;display.max_columns&#39;, None)
# 将特征字段分成 3 组
features_mean= list(data.columns[2:12])
features_se= list(data.columns[12:22])
features_worst=list(data.columns[22:32])
# 数据清洗

# ID 列没有用，删除该列
data.drop(&quot;id&quot;,axis=1,inplace=True)

# 将 B 良性替换为 0，M 恶性替换为 1
data[&#39;diagnosis&#39;]=data[&#39;diagnosis&#39;].map({&#39;M&#39;:1,&#39;B&#39;:0})

# 特征选择
features_remain = [&#39;radius_mean&#39;, &#39;texture_mean&#39;, &#39;perimeter_mean&#39;,
       &#39;area_mean&#39;, &#39;smoothness_mean&#39;, &#39;compactness_mean&#39;, &#39;concavity_mean&#39;,
       &#39;concave points_mean&#39;, &#39;symmetry_mean&#39;, &#39;fractal_dimension_mean&#39;,
       &#39;radius_se&#39;, &#39;texture_se&#39;, &#39;perimeter_se&#39;, &#39;area_se&#39;, &#39;smoothness_se&#39;,
       &#39;compactness_se&#39;, &#39;concavity_se&#39;, &#39;concave points_se&#39;, &#39;symmetry_se&#39;,
       &#39;fractal_dimension_se&#39;, &#39;radius_worst&#39;, &#39;texture_worst&#39;,
       &#39;perimeter_worst&#39;, &#39;area_worst&#39;, &#39;smoothness_worst&#39;,
       &#39;compactness_worst&#39;, &#39;concavity_worst&#39;, &#39;concave points_worst&#39;,
       &#39;symmetry_worst&#39;, &#39;fractal_dimension_worst&#39;] 

# 抽取 30% 的数据作为测试集，其余作为训练集
train, test = train_test_split(data, test_size = 0.3)# in this our main data is splitted into train and test

# 抽取特征选择的数值作为训练和测试数据
train_X = train[features_remain]
train_y=train[&#39;diagnosis&#39;]
test_X= test[features_remain]
test_y =test[&#39;diagnosis&#39;]

# 采用 Z-Score 规范化数据，保证每个特征维度的数据均值为 0，方差为 1
ss = StandardScaler()
train_X = ss.fit_transform(train_X)
test_X = ss.transform(test_X)

# 创建 SVM 分类器
model = svm.SVC()
# 用训练集做训练
model.fit(train_X,train_y)
# 用测试集做预测
prediction=model.predict(test_X)
print(&#39;准确率: &#39;, metrics.accuracy_score(prediction,test_y))


</div>2019-03-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/70/eb/e7a2dba9.jpg" width="30px"><span>ldw</span> 👍（0） 💬（1）<div>陈老师，这堂课留的课后任务，包括可能使用的数据清洗，您会期望您团队的人用多长时间完成？超过多长时间以上，就是不合格的？谢谢🙏</div>2019-02-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/0c/0f/93d1c8eb.jpg" width="30px"><span>mickey</span> 👍（0） 💬（1）<div>勘误：热力学图中的第一个蓝色框框应该是标记在第1列第3-4行上，而不是第1列第1行。</div>2019-02-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/62/a5/43aa0c27.jpg" width="30px"><span>TKbook</span> 👍（0） 💬（1）<div># 特征选择
features_all = [&#39;radius_mean&#39;, &#39;texture_mean&#39;, &#39;perimeter_mean&#39;,
       &#39;area_mean&#39;, &#39;smoothness_mean&#39;, &#39;compactness_mean&#39;, &#39;concavity_mean&#39;,
       &#39;concave points_mean&#39;, &#39;symmetry_mean&#39;, &#39;fractal_dimension_mean&#39;,
       &#39;radius_se&#39;, &#39;texture_se&#39;, &#39;perimeter_se&#39;, &#39;area_se&#39;, &#39;smoothness_se&#39;,
       &#39;compactness_se&#39;, &#39;concavity_se&#39;, &#39;concave points_se&#39;, &#39;symmetry_se&#39;,
       &#39;fractal_dimension_se&#39;, &#39;radius_worst&#39;, &#39;texture_worst&#39;,
       &#39;perimeter_worst&#39;, &#39;area_worst&#39;, &#39;smoothness_worst&#39;,
       &#39;compactness_worst&#39;, &#39;concavity_worst&#39;, &#39;concave points_worst&#39;,
       &#39;symmetry_worst&#39;, &#39;fractal_dimension_worst&#39;]
from sklearn.model_selection import train_test_split
# 抽取30%的数据作为测试集，其余作为训练集
train, test = train_test_split(data, test_size=0.3)
# 抽取特征选择的的数据作为训练和测试数据
train_X = train[features_all]
train_y = train[&#39;diagnosis&#39;]
test_X = test[features_all]
test_y = test[&#39;diagnosis&#39;]
from sklearn.preprocessing import StandardScaler
# 采用Z-Score规范化数据，保证每个特征维度的数据均值为0，方差为1
ss = StandardScaler()
train_X = ss.fit_transform(train_X)
test_X = ss.transform(test_X)
from sklearn import svm
from sklearn.metrics import accuracy_score
# 创建SVM分类器
model = svm.LinearSVC()
# 用训练集做训练
model.fit(train_X, train_y)
# 用测试集做预测
prediction = model.predict(test_X)
print(&#39;准确率：&#39;, accuracy_score(prediction, test_y))
准确率： 0.9824561403508771</div>2019-02-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/26/53/60fe31fb.jpg" width="30px"><span>深白浅黑</span> 👍（0） 💬（1）<div>使用全部特征：（相同训练集和测试集）
LinearSVC准确率:  0.9298245614035088
SVC高斯核准确率: 0.9415204678362573
SVM首先是有监督的学习模型，需要数据有较好的分类属性。其次依据硬间隔、软间隔和核函数的应用，可以解决线性分类和非线性分类的问题。最后在使用过程中，需要对数据的特征进行有针对性的降维，利用数据的相关性，对相关性较大的类别属性选择其中一个作为特征，在特征选取后，要进行标准化处理。</div>2019-02-15</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/wJphZ3HcvhjVUyTWCIsCugzfQY5NAy6VJ0XoPLibDlcHWMswFmFe678zd0lUjFETia80NQhyQcVnGDlKgKPcRGyw/132" width="30px"><span>JingZ</span> 👍（0） 💬（1）<div>#svm 使用还是蛮方便的，完全特征，准确率达到97%以上

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn import svm
from sklearn import metrics

#加载数据
data = pd.read_csv(‘.&#47;data.csv&#39;)

#数据探索
pd.set_option(&#39;display.max_columns&#39;, None)
print(data.columns)
print(data.head(5))
print(data.describe())

#数据清洗
data.drop(&#39;id&#39;, axis=1, inplace=True)
data[&#39;diagnosis&#39;]=data[&#39;diagnosis&#39;].map({&#39;M&#39;:1, &#39;B&#39;:0})

#特征选择
features_remain = [&#39;radius_mean&#39;, &#39;texture_mean&#39;, &#39;perimeter_mean&#39;,
       &#39;area_mean&#39;, &#39;smoothness_mean&#39;, &#39;compactness_mean&#39;, &#39;concavity_mean&#39;,
       &#39;concave points_mean&#39;, &#39;symmetry_mean&#39;, &#39;fractal_dimension_mean&#39;,
       &#39;radius_se&#39;, &#39;texture_se&#39;, &#39;perimeter_se&#39;, &#39;area_se&#39;, &#39;smoothness_se&#39;,
       &#39;compactness_se&#39;, &#39;concavity_se&#39;, &#39;concave points_se&#39;, &#39;symmetry_se&#39;,
       &#39;fractal_dimension_se&#39;, &#39;radius_worst&#39;, &#39;texture_worst&#39;,
       &#39;perimeter_worst&#39;, &#39;area_worst&#39;, &#39;smoothness_worst&#39;,
       &#39;compactness_worst&#39;, &#39;concavity_worst&#39;, &#39;concave points_worst&#39;,
       &#39;symmetry_worst&#39;, &#39;fractal_dimension_worst&#39;]

#30% 测试集、训练集
train, test = train_test_split(data, test_size = 0.3)

#抽取特征选择的数值作为训练和测试数据
train_X = train[features_remain]
train_y = train[&#39;diagnosis&#39;]
test_X = test[features_remain]
test_y = test[&#39;diagnosis&#39;]

#采用 Z-score 规范化数据
ss = StandardScaler()
train_X = ss.fit_transform(train_X)
test_X = ss.transform(test_X)

#创建 LinearSVC 分类器
model = svm.LinearSVC()

#用训练集做训练
model.fit(train_X, train_y)

#用测试集做预测
prediction = model.predict(test_X)
print(&#39;准确率：&#39;, metrics.accuracy_score(prediction, test_y))</div>2019-02-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ec/4a/40a2ba79.jpg" width="30px"><span>reverse</span> 👍（32） 💬（2）<div>极客时间数据分析实战45讲的详细笔记(包含markdown、图片、思维导图 代码) github地址： https:&#47;&#47;github.com&#47;xiaomiwujiecao&#47;DataAnalysisInAction</div>2019-03-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/0c/0f/93d1c8eb.jpg" width="30px"><span>mickey</span> 👍（7） 💬（1）<div># encoding=utf-8
from sklearn import svm
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pandas as pd
import seaborn  as sns
import matplotlib.pyplot as plt

# 加载数据集，你需要把数据放到目录中
data = pd.read_csv(&quot;.&#47;data.csv&quot;)
# 数据探索
# 因为数据集中列比较多，我们需要把dataframe中的列全部显示出来
pd.set_option(&#39;display.max_columns&#39;, None)
#print(data.columns)
#print(data.head(5))
#print(data.describe())

# 将特征字段分成3组
features_mean= list(data.columns[2:12])
features_se= list(data.columns[12:22])
features_worst=list(data.columns[22:32])
# 数据清洗
# ID列没有用，删除该列
data.drop(&quot;id&quot;,axis=1,inplace=True)
# 将B良性替换为0，M恶性替换为1
data[&#39;diagnosis&#39;]=data[&#39;diagnosis&#39;].map({&#39;M&#39;: 1, &#39;B&#39;: 0})

# 特征选择
features_remain = [&#39;radius_mean&#39;, &#39;texture_mean&#39;, &#39;perimeter_mean&#39;,
       &#39;area_mean&#39;, &#39;smoothness_mean&#39;, &#39;compactness_mean&#39;, &#39;concavity_mean&#39;,
       &#39;concave points_mean&#39;, &#39;symmetry_mean&#39;, &#39;fractal_dimension_mean&#39;,
       &#39;radius_se&#39;, &#39;texture_se&#39;, &#39;perimeter_se&#39;, &#39;area_se&#39;, &#39;smoothness_se&#39;,
       &#39;compactness_se&#39;, &#39;concavity_se&#39;, &#39;concave points_se&#39;, &#39;symmetry_se&#39;,
       &#39;fractal_dimension_se&#39;, &#39;radius_worst&#39;, &#39;texture_worst&#39;,
       &#39;perimeter_worst&#39;, &#39;area_worst&#39;, &#39;smoothness_worst&#39;,
       &#39;compactness_worst&#39;, &#39;concavity_worst&#39;, &#39;concave points_worst&#39;,
       &#39;symmetry_worst&#39;, &#39;fractal_dimension_worst&#39;]

# 抽取30%的数据作为测试集，其余作为训练集
train, test = train_test_split(data, test_size = 0.3)# in this our main data is splitted into train and test
# 抽取特征选择的数值作为训练和测试数据
train_X = train[features_remain]
train_y=train[&#39;diagnosis&#39;]
test_X= test[features_remain]
test_y =test[&#39;diagnosis&#39;]

# 采用Z-Score规范化数据，保证每个特征维度的数据均值为0，方差为1
ss = StandardScaler()
train_X = ss.fit_transform(train_X)
test_X = ss.transform(test_X)

# 创建SVM分类器
model = svm.LinearSVC()
# 用训练集做训练
model.fit(train_X,train_y)
# 用测试集做预测
prediction=model.predict(test_X)
print(&#39;准确率: &#39;, metrics.accuracy_score(prediction,test_y))

准确率: 0.9707602339181286</div>2019-02-26</li><br/><li><img src="" width="30px"><span>yanyu-xin</span> 👍（1） 💬（0）<div>将肿瘤诊断结果可视化的柱状图出现显示错误。应该是seaborn新旧版本导致的。
将：sns.countplot(data[&#39;diagnosis&#39;],label=&quot;Count&quot;)
改为：sns.countplot(x=&#39;diagnosis&#39;,data=data,label=&quot;Count&quot;)  
柱状图显示正确柱状图。</div>2024-04-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/35/7d/c1/1e6158f6.jpg" width="30px"><span>秉全</span> 👍（1） 💬（0）<div>怎么看分类结果</div>2023-08-21</li><br/><li><img src="" width="30px"><span>三硝基甲苯</span> 👍（1） 💬（0）<div>用K折交叉验证，LinearSVC的准确率是92.64% SVC是92.98% 
至于SVC的使用，我一开始直接按照自己的想法写完以后，会有聚合警告，然后看了一下，是数据没有进行StandardScaler，我觉得这个步骤容易忘记。</div>2019-03-10</li><br/>
</ul>