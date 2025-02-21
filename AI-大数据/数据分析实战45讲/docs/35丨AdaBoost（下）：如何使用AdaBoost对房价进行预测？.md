今天我带你用AdaBoost算法做一个实战项目。AdaBoost不仅可以用于分类问题，还可以用于回归分析。

我们先做个简单回忆，什么是分类，什么是回归呢？实际上分类和回归的本质是一样的，都是对未知事物做预测。不同之处在于输出结果的类型，分类输出的是一个离散值，因为物体的分类数有限的，而回归输出的是连续值，也就是在一个区间范围内任何取值都有可能。

这次我们的主要目标是使用AdaBoost预测房价，这是一个回归问题。除了对项目进行编码实战外，我希望你能掌握：

1. AdaBoost工具的使用，包括使用AdaBoost进行分类，以及回归分析。
2. 使用其他的回归工具，比如决策树回归，对比AdaBoost回归和决策树回归的结果。

## 如何使用AdaBoost工具

我们可以直接在sklearn中使用AdaBoost。如果我们要用AdaBoost进行分类，需要在使用前引用代码：

```
from sklearn.ensemble import AdaBoostClassifier
```

我们之前讲到过，如果你看到了Classifier这个类，一般都会对应着Regressor类。AdaBoost也不例外，回归工具包的引用代码如下：

```
from sklearn.ensemble import AdaBoostRegressor
```

我们先看下如何在sklearn中创建AdaBoost分类器。
<div><strong>精选留言（24）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/62/a5/43aa0c27.jpg" width="30px"><span>TKbook</span> 👍（18） 💬（1）<div>源代码中：
# 从 12000 个数据中取前 2000 行作为测试集，其余作为训练集
test_x, test_y = X[2000:],y[2000:]
train_x, train_y = X[:2000],y[:2000]

这个部分的代码写错了吧
应该是：
test_x, test_y = x[: 2000], y[: 2000]
train_x, train_y = x[2000:], y[2000:]</div>2019-03-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a4/5a/e708e423.jpg" width="30px"><span>third</span> 👍（7） 💬（1）<div>结果仍然为AdaBoost算法最优。
个人发现，前两个分类器出结果很快
分析最优：
1.AdaBoost算法经过了更多运算，特别是在迭代弱分类器和组合上
2.良好组合起来的个体，能够创造更大的价值。

决策树弱分类器准确率为 0.7867
决策树分类器准确率为 0.7891
AdaBoost 分类器准确率为 0.8138

import numpy as np
import pandas as pd
from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.feature_extraction import DictVectorizer

# 1.数据加载
train_data=pd.read_csv(&#39;.&#47;Titanic_Data&#47;train.csv&#39;)
test_data=pd.read_csv(&#39;.&#47;Titanic_Data&#47;test.csv&#39;)

# 2.数据清洗
# 使用平均年龄来填充年龄中的 NaN 值
train_data[&#39;Age&#39;].fillna(train_data[&#39;Age&#39;].mean(),inplace=True)
test_data[&#39;Age&#39;].fillna(test_data[&#39;Age&#39;].mean(),inplace=True)
# 均价填充
train_data[&#39;Fare&#39;].fillna(train_data[&#39;Fare&#39;].mean(),inplace=True)
test_data[&#39;Fare&#39;].fillna(test_data[&#39;Fare&#39;].mean(),inplace=True)
# 使用登陆最多的港口来填充
train_data[&#39;Embarked&#39;].fillna(&#39;S&#39;,inplace=True)
test_data[&#39;Embarked&#39;].fillna(&#39;S&#39;,inplace=True)

# 特征选择
features=[&#39;Pclass&#39;,&#39;Sex&#39;,&#39;Age&#39;,&#39;SibSp&#39;,&#39;Parch&#39;,&#39;Fare&#39;,&#39;Embarked&#39;]
train_features=train_data[features]
train_labels=train_data[&#39;Survived&#39;]
test_features=test_data[features]

# 将符号化的Embarked对象抽象处理成0&#47;1进行表示
dvec=DictVectorizer(sparse=False)
train_features=dvec.fit_transform(train_features.to_dict(orient=&#39;record&#39;))
test_features=dvec.transform(test_features.to_dict(orient=&#39;record&#39;))

# 决策树弱分类器
dt_stump = DecisionTreeClassifier(max_depth=1,min_samples_leaf=1)
dt_stump.fit(train_features, train_labels)

print(u&#39;决策树弱分类器准确率为 %.4lf&#39; % np.mean(cross_val_score(dt_stump, train_features, train_labels, cv=10)))

# 决策树分类器
dt = DecisionTreeClassifier()
dt.fit(train_features, train_labels)

print(u&#39;决策树分类器准确率为 %.4lf&#39; % np.mean(cross_val_score(dt, train_features, train_labels, cv=10)))

# AdaBoost 分类器
ada = AdaBoostClassifier(base_estimator=dt_stump,n_estimators=200)
ada.fit(train_features, train_labels)

print(u&#39;AdaBoost 分类器准确率为 %.4lf&#39; % np.mean(cross_val_score(ada, train_features, train_labels, cv=10)))</div>2019-03-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7d/05/4bad0c7c.jpg" width="30px"><span>Geek_hve78z</span> 👍（6） 💬（1）<div>由于乘客测试集缺失真实值，采用 K 折交叉验证准确率
--------------------
运行结果：
决策树弱分类器准确率为 0.7867
决策树分类器准确率为 0.7813
AdaBoost 分类器准确率为 0.8138
-------------------------
代码：
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import  AdaBoostClassifier
import pandas as pd
from sklearn.feature_extraction import DictVectorizer
from sklearn.model_selection import cross_val_score

# 设置 AdaBoost 迭代次数
n_estimators=200

# 数据加载
train_data=pd.read_csv(&#39;.&#47;Titanic_Data&#47;train.csv&#39;)
test_data=pd.read_csv(&#39;.&#47;Titanic_Data&#47;test.csv&#39;)

# 模块 2：数据清洗
# 使用平均年龄来填充年龄中的 NaN 值
train_data[&#39;Age&#39;].fillna(train_data[&#39;Age&#39;].mean(),inplace=True)
test_data[&#39;Age&#39;].fillna(test_data[&#39;Age&#39;].mean(),inplace=True)
# 使用票价的均值填充票价中的 nan 值
train_data[&#39;Fare&#39;].fillna(train_data[&#39;Fare&#39;].mean(),inplace=True)
test_data[&#39;Fare&#39;].fillna(test_data[&#39;Fare&#39;].mean(),inplace=True)
# 使用登录最多的港口来填充登录港口Embarked的 nan 值
train_data[&#39;Embarked&#39;].fillna(&#39;S&#39;,inplace=True)
test_data[&#39;Embarked&#39;].fillna(&#39;S&#39;,inplace=True)

# 特征选择
features=[&#39;Pclass&#39;,&#39;Sex&#39;,&#39;Age&#39;,&#39;SibSp&#39;,&#39;Parch&#39;,&#39;Fare&#39;,&#39;Embarked&#39;]
train_features=train_data[features]
train_labels=train_data[&#39;Survived&#39;]
test_features=test_data[features]

# 将符号化的Embarked对象处理成0&#47;1进行表示
dvec=DictVectorizer(sparse=False)
train_features=dvec.fit_transform(train_features.to_dict(orient=&#39;record&#39;))
test_features=dvec.transform(test_features.to_dict(orient=&#39;record&#39;))

# 决策树弱分类器
dt_stump = DecisionTreeClassifier(max_depth=1,min_samples_leaf=1)
dt_stump.fit(train_features, train_labels)

print(u&#39;决策树弱分类器准确率为 %.4lf&#39; % np.mean(cross_val_score(dt_stump, train_features, train_labels, cv=10)))

# 决策树分类器
dt = DecisionTreeClassifier()
dt.fit(train_features, train_labels)

print(u&#39;决策树分类器准确率为 %.4lf&#39; % np.mean(cross_val_score(dt, train_features, train_labels, cv=10)))

# AdaBoost 分类器
ada = AdaBoostClassifier(base_estimator=dt_stump,n_estimators=n_estimators)
ada.fit(train_features, train_labels)

print(u&#39;AdaBoost 分类器准确率为 %.4lf&#39; % np.mean(cross_val_score(ada, train_features, train_labels, cv=10)))</div>2019-03-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/77/be/1f2409e8.jpg" width="30px"><span>梁林松</span> 👍（3） 💬（1）<div>跑第二块代码是需要引入两个模块
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor
</div>2019-03-04</li><br/><li><img src="" width="30px"><span>Liam</span> 👍（2） 💬（1）<div>ax = fig.add_subplot(111)ax.plot([1,n_estimators],[dt_stump_err]*2, &#39;k-&#39;, label=u&#39;决策树弱分类器 错误率&#39;)ax.plot([1,n_estimators],[dt_err]*2,&#39;k--&#39;, label=u&#39;决策树模型 错误率&#39;)ada_err = np.zeros((n_estimators,)).  疑问：这里*2是什么意思，能解析下代码吗？</div>2021-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a3/87/c415e370.jpg" width="30px"><span>滢</span> 👍（1） 💬（1）<div>得到结果：
CART决策树K折交叉验证准确率: 0.39480897860892333
AdaBoostK折交叉验证准确率: 0.4376641797318339

from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import AdaBoostRegressor
from sklearn.feature_extraction import DictVectorizer
from sklearn.model_selection import cross_val_predict
import pandas as pd
import numpy as np

#读取数据
path = &#39;&#47;Users&#47;apple&#47;Desktop&#47;GitHubProject&#47;Read mark&#47;数据分析&#47;geekTime&#47;data&#47;&#39;
train_data = pd.read_csv(path + &#39;Titannic_Data_train.csv&#39;)
test_data = pd.read_csv(path + &#39;Titannic_Data_test.csv&#39;)

#数据清洗
train_data[&#39;Age&#39;].fillna(train_data[&#39;Age&#39;].mean(),inplace=True)
test_data[&#39;Age&#39;].fillna(test_data[&#39;Age&#39;].mean(), inplace=True)
train_data[&#39;Embarked&#39;].fillna(&#39;S&#39;, inplace=True)
test_data[&#39;Embarked&#39;].fillna(&#39;S&#39;, inplace=True)

#特征选择
features = [&#39;Pclass&#39;,&#39;Sex&#39;,&#39;Age&#39;,&#39;SibSp&#39;,&#39;Parch&#39;,&#39;Embarked&#39;]
train_features = train_data[features]
train_result = train_data[&#39;Survived&#39;]
test_features = test_data[features]
devc = DictVectorizer(sparse=False)
train_features = devc.fit_transform(train_features.to_dict(orient=&#39;record&#39;))
test_features = devc.fit_transform(test_features.to_dict(orient=&#39;record&#39;))

#构造决策树，进行预测
tree_regressor = DecisionTreeRegressor()
tree_regressor.fit(train_features,train_result)
predict_tree = tree_regressor.predict(test_features)
#交叉验证准确率
print(&#39;CART决策树K折交叉验证准确率:&#39;, np.mean(cross_val_predict(tree_regressor,train_features,train_result,cv=10)))

#构造AdaBoost
ada_regressor = AdaBoostRegressor()
ada_regressor.fit(train_features,train_result)
predict_ada = ada_regressor.predict(test_features)
#交叉验证准确率
print(&#39;AdaBoostK折交叉验证准确率:&#39;,np.mean(cross_val_predict(ada_regressor,train_features,train_result,cv=10)))
</div>2019-04-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/86/d7/46842f90.jpg" width="30px"><span>小晨</span> 👍（0） 💬（1）<div>弱分类器准确率为 0.7868
决策树分类器准确率为 0.7823
AdaBoost分类器准确率为:0.8115

#!&#47;usr&#47;bin&#47;env python
# -*- coding:utf-8 -*-
# Author:Peter

import numpy as np
import pandas as pd
from sklearn.ensemble import AdaBoostClassifier
from sklearn.feature_extraction import DictVectorizer
from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeClassifier

# 迭代次数
n_estimators = 200
train_data = pd.read_csv(r&#39;data&#47;Titanic_Data_train.csv&#39;)
test_data = pd.read_csv(r&#39;data&#47;Titanic_Data_Test.csv&#39;)

# 用平均年龄将缺失的年龄补齐
train_data[&#39;Age&#39;].fillna(train_data[&#39;Age&#39;].mean(), inplace=True)
test_data[&#39;Age&#39;].fillna(test_data[&#39;Age&#39;].mean(), inplace=True)

# 用平均票价将缺失的票价补齐
train_data[&#39;Fare&#39;].fillna(train_data[&#39;Fare&#39;].mean(), inplace=True)
test_data[&#39;Fare&#39;].fillna(test_data[&#39;Fare&#39;].mean(), inplace=True)

# 用登船港口最多的S补齐缺失
train_data[&#39;Embarked&#39;].fillna(&#39;S&#39;, inplace=True)
test_data[&#39;Embarked&#39;].fillna(&#39;S&#39;, inplace=True)

# 将可用来分类的数据放到训练集中
features = [&#39;Pclass&#39;, &#39;Sex&#39;, &#39;Age&#39;, &#39;SibSp&#39;, &#39;Parch&#39;, &#39;Fare&#39;, &#39;Embarked&#39;]
train_features = train_data[features]
train_labels = train_data[&#39;Survived&#39;]
test_features = test_data[features]

# 字符串数据规范化，转为int型
dvec = DictVectorizer(sparse=False)
train_features = dvec.fit_transform(train_features.to_dict(orient=&#39;record&#39;))
test_features = dvec.transform(test_features.to_dict(orient=&#39;record&#39;))

# 弱分类器
dt_stump = DecisionTreeClassifier(max_depth=1, min_samples_leaf=1)
dt_stump.fit(train_features, train_labels)
print(u&#39;弱分类器准确率为 %.4lf&#39; % dt_stump.score(train_features, train_labels))
# 决策树分类器
dt = DecisionTreeClassifier()
dt.fit(train_features, train_labels)
print(u&#39;决策树分类器准确率为 %.4lf&#39; % np.mean(cross_val_score(dt, train_features, train_labels, cv=10)))

# AdaBoost分类器
ada = AdaBoostClassifier(base_estimator=dt_stump, n_estimators=n_estimators)
ada.fit(train_features, train_labels)
ada_score = np.mean(cross_val_score(ada, train_features, train_labels, cv=10))
print(&quot;AdaBoost分类器准确率为:%.4lf&quot; % ada_score)
</div>2021-03-10</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/J9YKHoKKd1LlzuCuKFGhnKBD1GtS9qiclsibY6vviacpCOB7uR4iaibIpdQKTzwiaVwJiaiaicB99rNx23JPQYV5wjThOWQ/132" width="30px"><span>萌辰</span> 👍（0） 💬（1）<div>在AdaBoost、决策树回归、KNN房价预测对比中发现，随机种子对决策树的预测结果有影响。
分别测试了三种不同的随机种子：
dec_regressor=DecisionTreeRegressor(random_state=1)
dec_regressor=DecisionTreeRegressor(random_state=20)
dec_regressor=DecisionTreeRegressor(random_state=30)
测试结果为：
决策树均方误差1 =  36.65
决策树均方误差20 =  25.54
决策树均方误差30 =  37.19
思考：
此处考虑这里没有限制种子的随机性，对比的结果可能过于随机了，无法真实反映算法效果，两种算法原理中随机种子的应用情况不同。思考是不是采用多次随机MSE结果求平均的方法作为【比较项】更为合适
KNN算法无随机种子影响。</div>2020-07-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/7d/2a/4c7e2e2f.jpg" width="30px"><span>§mc²ompleXWr</span> 👍（0） 💬（1）<div>使用自带的数据集就不用做数据规范化么？</div>2020-06-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/51/98/3b8de985.jpg" width="30px"><span>鲨鱼鲸鱼鳄鱼</span> 👍（0） 💬（1）<div>老师，请问AdaBoost模型在预测前需不需要对数据进行标准化或者归一化，做有什么好处，不做有什么好处呢</div>2020-05-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/94/6d/5cd6e8c7.jpg" width="30px"><span>张贺</span> 👍（0） 💬（1）<div>老师讲的很清晰</div>2020-03-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/5d/27/74e152d3.jpg" width="30px"><span>滨滨</span> 👍（0） 💬（1）<div>分类和回归都是做预测，分类是离散值，回归是连续值</div>2019-04-21</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/wJphZ3HcvhjVUyTWCIsCugzfQY5NAy6VJ0XoPLibDlcHWMswFmFe678zd0lUjFETia80NQhyQcVnGDlKgKPcRGyw/132" width="30px"><span>JingZ</span> 👍（0） 💬（1）<div># AdaBoost
一开始竟然蓦然惯性用了AdaBoostRegressor，得到0.33的准确率，最后看了小伙伴代码，立马修正

感觉算法代码不复杂，关键要自己从空白开始写，还需多实战

from sklearn.ensemble import AdaBoostClassifier

# 使用 Adaboost 分类模型
ada = AdaBoostClassifier()
ada.fit(train_features, train_labels)

pred_labels = ada.predict(test_features)

acc_ada_classifier = round(ada.score(train_features, train_labels), 6)
print(u&#39;Adaboost score 准确率为 %.4lf&#39; % acc_ada_classifier)
print(u&#39;Adaboost cross_val_score 准确率为 %.4lf&#39; % np.mean(cross_val_score(ada, train_features, train_labels, cv=10)))

运行
Adaboost score 准确率为 0.8339
Adaboost cross_val_score 准确率为 0.8104</div>2019-03-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/b8/21/c03839f1.jpg" width="30px"><span>FORWARD―MOUNT</span> 👍（0） 💬（1）<div>老师，房价预测这个算法，50个弱分类器是怎么来的？</div>2019-03-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/83/e2/297518ab.jpg" width="30px"><span>佳佳的爸</span> 👍（0） 💬（1）<div>你好老师，完整的源代码在哪里可以下载到?  我说的是每节课里边的源代码。</div>2019-03-04</li><br/><li><img src="" width="30px"><span>yanyu-xin</span> 👍（4） 💬（0）<div>在课程“AdaBoost 与决策树模型的比较”代码，ada = AdaBoostClassifier(base_estimator=dt_stump,n_estimators=n_estimators)
出现异常，TypeError AdaBoostClassifier.__init__() got an unexpected keyword argument &#39;base_estimator&#39;
这个问题是由于：由于scikit-learn库在1.2版本或更高版本中对AdaBoostClassifier的参数base_estimator进行了重命名，将其改为estimator。此外，警告信息还指出base_estimator参数将在1.4版本中被移除。

另外出现警告信息：FutureWarning: The SAMME.R algorithm (the default) is deprecated and will be removed in 1.6. Use the SAMME algorithm to circumvent this warning.
scikit-learn库中的AdaBoostClassifier默认使用的SAMME.R算法已被弃用，并且计划在1.6版本中移除。为了避免这个警告，应该在创建AdaBoostClassifier实例时显式指定使用SAMME算法，而不是默认的SAMME.R算法。SAMME和SAMME.R是两种不同的多类AdaBoost算法。SAMME.R是SAMME的一个变种，它依赖于概率估计，通常会有更好的性能，但现在由于某些原因被弃用。要在您的代码中指定使用SAMME算法，您可以在创建AdaBoostClassifier实例时设置algorithm参数为&#39;SAMME&#39;。以下是修改代码：将：
ada = AdaBoostClassifier(base_estimator=dt_stump,n_estimators=n_estimators)
改为：
ada = AdaBoostClassifier(estimator=dt_stump,n_estimators=n_estimators,algorithm=&#39;SAMME&#39;)</div>2024-04-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/26/9e/836f603b.jpg" width="30px"><span>KokutoDa</span> 👍（1） 💬（0）<div>准确率：
adaboost 交叉验证：0.81147315855181
决策树交叉验证：0.7812484394506866
adaboost（accuracy_score）：0.8484848484848485
决策树（accuracy_score）0.9820426487093153
老师，为什么交叉验证的准确率和accuracy_score的准确率计算结果相反？

import pandas as pd
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_extraction import DictVectorizer
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score
import numpy as np

# adaboost 预测泰坦尼克号生存
# 数据加载
train_data = pd.read_csv(&#39;..&#47;Titanic_Data&#47;train.csv&#39;)
test_data = pd.read_csv(&#39;..&#47;Titanic_Data&#47;test.csv&#39;)

# 数据清洗
train_data[&#39;Age&#39;].fillna(train_data[&#39;Age&#39;].mean(), inplace=True)
test_data[&#39;Age&#39;].fillna(test_data[&#39;Age&#39;].mean(),inplace=True)
train_data[&#39;Fare&#39;].fillna(train_data[&#39;Fare&#39;].mean(), inplace=True)
test_data[&#39;Fare&#39;].fillna(test_data[&#39;Fare&#39;].mean(),inplace=True)
# 使用登录最多的港口来填充登录港口的 nan 值
train_data[&#39;Embarked&#39;].fillna(&#39;S&#39;, inplace=True)
test_data[&#39;Embarked&#39;].fillna(&#39;S&#39;,inplace=True)

# 特征选择
features = [&#39;Pclass&#39;, &#39;Sex&#39;, &#39;Age&#39;, &#39;SibSp&#39;, &#39;Parch&#39;, &#39;Fare&#39;, &#39;Embarked&#39;]
X_train = train_data[features]
y_train = train_data[&#39;Survived&#39;]
X_test = test_data[features]
# 替换成计算机能理解的
dvec=DictVectorizer(sparse=False)
X_train = dvec.fit_transform(X_train.to_dict(orient=&#39;record&#39;))

# Adaboost
ada = AdaBoostClassifier(n_estimators=200)
ada.fit(X_train, y_train)
ada_pred = ada.predict(X_train)

# 决策树
clf = DecisionTreeClassifier(criterion=&#39;entropy&#39;)
clf.fit(X_train, y_train)
clf_pred = clf.predict(X_train)

print(np.mean(cross_val_score(ada, X_train, y_train, cv=10)))
print(np.mean(cross_val_score(clf, X_train, y_train, cv=10)))
print(accuracy_score(y_train, ada_pred))
print(accuracy_score(y_train, clf_pred))</div>2021-05-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/86/79/066a062a.jpg" width="30px"><span>非同凡想</span> 👍（0） 💬（0）<div>交作业：
import numpy as np
import pandas as pd
from sklearn import tree
from sklearn import feature_extraction
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import  AdaBoostClassifier

# load dataset
train_data = pd.DataFrame(pd.read_csv(&#39;~&#47;Documents&#47;titanic_data&#47;train.csv&#39;))
test_data = pd.DataFrame(pd.read_csv(&#39;~&#47;Documents&#47;titanic_data&#47;test.csv&#39;))

# data cleaning
train_data[&#39;Age&#39;].fillna(train_data[&#39;Age&#39;].mean(), inplace=True)
test_data[&#39;Age&#39;].fillna(test_data[&#39;Age&#39;].mean(), inplace=True)
test_data[&#39;Fare&#39;].fillna(test_data[&#39;Fare&#39;].mean(), inplace=True)
train_data[&#39;Embarked&#39;].fillna(&#39;S&#39;, inplace=True)
test_data[&#39;Embarked&#39;].fillna(&#39;S&#39;, inplace=True)
# select features
features = [&#39;Pclass&#39;, &#39;Sex&#39;, &quot;Age&quot;, &#39;SibSp&#39;, &#39;Parch&#39;, &#39;Fare&#39;, &#39;Embarked&#39;]
train_x = train_data[features]
train_y = train_data[&#39;Survived&#39;]
test_x = test_data[features]
# one-hot
dict_vec = feature_extraction.DictVectorizer(sparse=False)
train_x = dict_vec.fit_transform(train_x.to_dict(orient=&#39;record&#39;))
test_x = dict_vec.transform(test_x.to_dict(orient=&#39;record&#39;))
print(dict_vec.feature_names_)

# decision tree
dtc = tree.DecisionTreeClassifier()
dtc.fit(train_x, train_y)

print(&quot;决策树准确率&quot;, dtc.score(train_x, train_y))
print(&quot;决策树：k折交叉验证准确率：&quot;, np.mean(cross_val_score(dtc, train_x, train_y, cv= 10)))

# adaboost
ada = AdaBoostClassifier(n_estimators=50)
ada.fit(train_x, train_y)
print(&quot;AdaBoost准确率&quot;, ada.score(train_x, train_y))
print(&quot;AdaBoost k折交叉验证准确率：&quot;, np.mean(cross_val_score(ada, train_x, train_y, cv= 10)))

决策树准确率 0.9820426487093153
决策树：k折交叉验证准确率： 0.7744943820224719
AdaBoost准确率 0.8338945005611672
AdaBoost k折交叉验证准确率： 0.8070037453183521</div>2020-11-26</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIfCY2mvbZ2Po4efYBhMJPacb9mlOicNI6Us4ph3ianrkGlUcop8ZlzN6QiaDrnvFcNeaAfwP7XAv5fw/132" width="30px"><span>even</span> 👍（0） 💬（0）<div>不同的算法有不同的特点，老师是否可以做个总结和对比。比如在实际的工作或者项目中，根据经验和不同的算法特点，如何选择算法，为什么选择这种算法。希望老师能分享这一块实际应用场景的经验。</div>2020-06-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/0c/24/8ce78297.jpg" width="30px"><span>热水泡面不会做</span> 👍（0） 💬（0）<div>可不可以解释一下这里的学习率体现在哪里呢？之前的原理讲解里好像没有用到学习率？</div>2020-03-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/dc/68/006ba72c.jpg" width="30px"><span>Untitled</span> 👍（0） 💬（0）<div>结果：
ada train precision =  0.8338945005611672
ada 10k precison =  0.8070037453183521
clf train precision =  0.9820426487093153
clf 10k precision =  0.7767041198501872
#代码
import pandas as pd
import numpy as np
from sklearn.feature_extraction import DictVectorizer
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score
train_data = pd.read_csv(&#39;train.csv&#39;)
test_data = pd.read_csv(&#39;test.csv&#39;)

train_data[&#39;Age&#39;].fillna(train_data[&#39;Age&#39;].mean(),inplace=True)
test_data[&#39;Age&#39;].fillna(train_data[&#39;Age&#39;].mean(),inplace=True)
train_data[&#39;Fare&#39;].fillna(train_data[&#39;Age&#39;].mean(),inplace=True)
test_data[&#39;Fare&#39;].fillna(train_data[&#39;Age&#39;].mean(),inplace=True)

train_data[&#39;Embarked&#39;].fillna(&#39;S&#39;,inplace=True)
test_data[&#39;Embarked&#39;].fillna(&#39;S&#39;,inplace=True)

features = [&#39;Pclass&#39;, &#39;Sex&#39;, &#39;Age&#39;, &#39;SibSp&#39;, &#39;Parch&#39;, &#39;Fare&#39;, &#39;Embarked&#39;]
train_features = train_data[features]
train_labels = train_data[&#39;Survived&#39;]
test_features = test_data[features]

dvec=DictVectorizer(sparse=False)
train_features=dvec.fit_transform(train_features.to_dict(orient=&#39;record&#39;))
test_features=dvec.transform(test_features.to_dict(orient=&#39;record&#39;))

ada = AdaBoostClassifier()
ada.fit(train_features, train_labels)
print(&quot;ada train precision = &quot;,ada.score(train_features, train_labels))
print(&quot;ada 10k precison = &quot;, np.mean(cross_val_score(ada,train_features,train_labels,cv=10)))
clf=DecisionTreeClassifier(criterion=&#39;entropy&#39;)
clf.fit(train_features,train_labels)
print(&quot;clf train precision = &quot;, clf.score(train_features, train_labels))
print(&quot;clf 10k precision = &quot;, np.mean(cross_val_score(clf,train_features,train_labels,cv=10)))
</div>2020-03-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/7e/a6/4e331ef4.jpg" width="30px"><span>骑行的掌柜J</span> 👍（0） 💬（0）<div>打错了 陈老师是对的 是回归算法😂里没有分类算法的algorithm 参数。</div>2019-08-14</li><br/><li><img src="" width="30px"><span>hlz-123</span> 👍（0） 💬（0）<div>老师，在AdaBoost 与决策树模型的比较的例子中，弱分类器
dt_stump = DecisionTreeClassfier(max_depth=1,min_samples_leaf=1)
为什么两个参数都设置为1，相当于只有1个根节点，2个叶节点？
而普通的决策树分类器，没有设置参数，这是什么原因？</div>2019-03-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/c1/1f/cc77944d.jpg" width="30px"><span>叮当猫</span> 👍（0） 💬（0）<div>fit_transform数据统一处理，求问什么时候需要？
在我同时没有进行fit_transform的情况下，准确率：
决策树弱分类器的准确率是0.7867
决策树分类器的准确率是0.7734
AdaBoost分类器的准确率是0.8161
在我对数据同时进行fit_transform的情况下，准确率：
决策树弱分类器的准确率是0.7867
决策树分类器的准确率是0.7745
AdaBoost分类器的准确率是0.8138

以下是第一种情况：
train_data[&#39;Embarked&#39;] = train_data[&#39;Embarked&#39;].map({&#39;S&#39;:0, &#39;C&#39;:1, &#39;Q&#39;:2})
test_data[&#39;Embarked&#39;] = test_data[&#39;Embarked&#39;].map({&#39;S&#39;:0, &#39;C&#39;:1, &#39;Q&#39;:2})
train_data[&#39;Sex&#39;] = train_data[&#39;Sex&#39;].map({&#39;male&#39;:0, &#39;female&#39;:1})
test_data[&#39;Sex&#39;] = test_data[&#39;Sex&#39;].map({&#39;male&#39;:0, &#39;female&#39;:1})

train_data[&#39;Age&#39;].fillna(train_data[&#39;Age&#39;].mean(), inplace=True)
test_data[&#39;Age&#39;].fillna(test_data[&#39;Age&#39;].mean(), inplace=True)
train_data[&#39;Fare&#39;].fillna(train_data[&#39;Fare&#39;].mean(), inplace=True)
test_data[&#39;Fare&#39;].fillna(test_data[&#39;Fare&#39;].mean(), inplace=True)

features = [&#39;Pclass&#39;, &#39;Sex&#39;,&#39;Age&#39;,&#39;SibSp&#39;, &#39;Parch&#39;, &#39;Fare&#39;, &#39;Embarked&#39;]
train_features = train_data[features]
train_labels = train_data[&#39;Survived&#39;]
test_features = test_data[features]

#train_features = dvec.fit_transform(train_features.to_dict(orient=&#39;record&#39;))
#test_features = dvec.transform(test_features.to_dict(orient=&#39;record&#39;))

以下是第二种情况：
#train_data[&#39;Embarked&#39;] = train_data[&#39;Embarked&#39;].map({&#39;S&#39;:0, &#39;C&#39;:1, &#39;Q&#39;:2})
#test_data[&#39;Embarked&#39;] = test_data[&#39;Embarked&#39;].map({&#39;S&#39;:0, &#39;C&#39;:1, &#39;Q&#39;:2})
#train_data[&#39;Sex&#39;] = train_data[&#39;Sex&#39;].map({&#39;male&#39;:0, &#39;female&#39;:1})
#test_data[&#39;Sex&#39;] = test_data[&#39;Sex&#39;].map({&#39;male&#39;:0, &#39;female&#39;:1})

train_data[&#39;Age&#39;].fillna(train_data[&#39;Age&#39;].mean(), inplace=True)
test_data[&#39;Age&#39;].fillna(test_data[&#39;Age&#39;].mean(), inplace=True)
train_data[&#39;Fare&#39;].fillna(train_data[&#39;Fare&#39;].mean(), inplace=True)
test_data[&#39;Fare&#39;].fillna(test_data[&#39;Fare&#39;].mean(), inplace=True)

features = [&#39;Pclass&#39;, &#39;Sex&#39;,&#39;Age&#39;,&#39;SibSp&#39;, &#39;Parch&#39;, &#39;Fare&#39;, &#39;Embarked&#39;]
train_features = train_data[features]
train_labels = train_data[&#39;Survived&#39;]
test_features = test_data[features]

train_features = dvec.fit_transform(train_features.to_dict(orient=&#39;record&#39;))
test_features = dvec.transform(test_features.to_dict(orient=&#39;record&#39;))</div>2019-03-19</li><br/>
</ul>