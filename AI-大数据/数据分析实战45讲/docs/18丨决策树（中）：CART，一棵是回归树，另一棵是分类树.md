上节课我们讲了决策树，基于信息度量的不同方式，我们可以把决策树分为ID3算法、C4.5算法和CART算法。今天我来带你学习CART算法。CART算法，英文全称叫做Classification And Regression Tree，中文叫做分类回归树。ID3和C4.5算法可以生成二叉树或多叉树，而CART只支持二叉树。同时CART决策树比较特殊，既可以作分类树，又可以作回归树。

那么你首先需要了解的是，什么是分类树，什么是回归树呢？

我用下面的训练数据举个例子，你能看到不同职业的人，他们的年龄不同，学习时间也不同。如果我构造了一棵决策树，想要基于数据判断这个人的职业身份，这个就属于分类树，因为是从几个分类中来做选择。如果是给定了数据，想要预测这个人的年龄，那就属于回归树。

![](https://static001.geekbang.org/resource/image/af/cf/af89317aa55ac3b9f068b0f370fcb9cf.png?wh=624%2A259)  
分类树可以处理离散数据，也就是数据种类有限的数据，它输出的是样本的类别，而回归树可以对连续型的数值进行预测，也就是数据在某个区间内都有取值的可能，它输出的是一个数值。

## CART分类树的工作流程

通过上一讲，我们知道决策树的核心就是寻找纯净的划分，因此引入了纯度的概念。在属性选择上，我们是通过统计“不纯度”来做判断的，ID3是基于信息增益做判断，C4.5在ID3的基础上做了改进，提出了信息增益率的概念。实际上CART分类树与C4.5算法类似，只是属性选择的指标采用的是基尼系数。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/13/8c/3d/77b9abbb.jpg" width="30px"><span>rainman</span> 👍（39） 💬（1）<div>对于 CART 回归树的可视化，可以先在电脑上安装 graphviz；然后 pip install graphviz，这是安装python的库，需要依赖前面安装的 graphviz。可视化代码如下：

----
from sklearn.tree import export_graphviz
import graphviz

# 参数是回归树模型名称，不输出文件。
dot_data = export_graphviz(dtr, out_file=None)
graph = graphviz.Source(dot_data)
# render 方法会在同级目录下生成 Boston PDF文件，内容就是回归树。
graph.render(&#39;Boston&#39;)
----

具体内容可以去 sklearn(https:&#47;&#47;scikit-learn.org&#47;stable&#47;modules&#47;generated&#47;sklearn.tree.export_graphviz.html)
和 graphviz(https:&#47;&#47;graphviz.readthedocs.io&#47;en&#47;stable&#47;) 看看。</div>2019-02-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/2f/e2/3640e491.jpg" width="30px"><span>小熊猫</span> 👍（16） 💬（1）<div>ID3：以信息增益作为判断标准，计算每个特征的信息增益，选取信息增益最大的特征，但是容易选取到取值较多的特征
C4.5：以信息增益比作为判断标准，计算每个特征的信息增益比，选取信息增益比最大的特征
CART：分类树以基尼系数为标准，选取基尼系数小的的特征
            回归树以均方误差或绝对值误差为标准，选取均方误差或绝对值误差最小的特征

练习题：
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn import tree
from sklearn.metrics import accuracy_score
import graphviz 

# 准备手写数字数据集
digits = datasets.load_digits()
# 获取特征和标识
features = digits.data
labels = digits.target
# 选取数据集的33%为测试集，其余为训练集
train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size=0.33)
# 创建CART分类树
clf = tree.DecisionTreeClassifier()
# 拟合构造CART分类树
clf.fit(train_features, train_labels)
# 预测测试集结果
test_predict = clf.predict(test_features)
# 测试集结果评价
print(&#39;CART分类树准确率:&#39;, accuracy_score(test_labels, test_predict))
# 画决策树
dot_data = tree.export_graphviz(clf, out_file=None)
graph = graphviz.Source(dot_data)
graph.render(&#39;CART&#47;&#47;CART_practice_digits&#39;)

CART分类树准确率: 0.8636363636363636</div>2019-02-15</li><br/><li><img src="" width="30px"><span>jake</span> 👍（7） 💬（2）<div>
首先想问一个问题 就是在讲到基尼系数那里 有一个图那里的例子 什么D: 9个打篮球 3个不打篮球那里
那里的D的基尼系数用到了子节点归一化基尼系数之和这个方法求 请问D的基尼系数不能直接用 上面那个公式 也就是&quot;1 - [p(ck|t)]^2&quot;那个公式计算吗 我用这个公式计算出D的基尼系数为 1 - (9&#47;12 * 9&#47;12 + 3&#47;12 * 3&#47;12) = 6&#47;16。 我也想问一下上面那个同学提的这个问题</div>2019-02-24</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erBSoNm28CNCYpvytDbhfSYpgCo6T9vuzKkSoflr3sX8VucMz8ykrichKDY9vVoMVomUIakXSQq9icw/132" width="30px"><span>xfoolin</span> 👍（4） 💬（1）<div>ID3 是通过信息增益，选取信息增益最大的特征；C4.5 是通过信息增益率，选取，CART 是通过基尼系数，选取基尼系数最小的特征。


from sklearn.model_selection import train_test_split#训练集和测试集
from sklearn.metrics import mean_squared_error#二乘偏差均值
from sklearn.metrics import mean_absolute_error#绝对值偏差均值
from sklearn.datasets import load_digits#引入 digits 数据集
from sklearn.metrics import accuracy_score#测试结果的准确性
from sklearn import tree
import graphviz
#准备数据集
digits = load_digits()
#获取数据集的特征集和分类标识
features = digits.data
labels = digits.target
#随机抽取 33% 的数据作为测试集，其余为训练集
train_features,test_features,train_labels,test_labels = \
train_test_split(features,labels,test_size = 0.33,random_state = 0)
#创建 CART 分类树
clf = tree.DecisionTreeClassifier(criterion = &#39;gini&#39;)
#拟合构造分类树
clf = clf.fit(train_features,train_labels)
#用 CART 分类树做预测
test_predict = clf.predict(test_features)
#预测结果与测试集作对比
score = accuracy_score(test_labels,test_predict)
#输出准确率
print(&#39;准确率 %.4f&#39;%score)
dot_data = tree.export_graphviz(clf,out_file = None)
graph = graphviz.Source(dot_data)
#输出分类树图示
graph.view()
</div>2019-02-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/0a/eb/6d6a94d2.jpg" width="30px"><span>Lee</span> 👍（3） 💬（1）<div># encoding=utf-8
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import load_digits

# 准备数据集
digits=load_digits()
# 获取特征集和分类标识
features = digits.data
labels = digits.target
# 随机抽取 33% 的数据作为测试集，其余为训练集
train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size=0.33, random_state=0)
# 创建 CART 分类树
clf = DecisionTreeClassifier(criterion=&#39;gini&#39;)
# 拟合构造 CART 分类树
clf = clf.fit(train_features, train_labels)
# 用 CART 分类树做预测
test_predict = clf.predict(test_features)
# 预测结果与测试集结果作比对
score = accuracy_score(test_labels, test_predict)
print(&quot;CART 分类树准确率 %.4lf&quot; % score)

CART 分类树准确率 0.8620</div>2019-01-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/03/3f/09308258.jpg" width="30px"><span>雨先生的晴天</span> 👍（2） 💬（1）<div>scikit learn package 确实非常好用，很简洁。推荐大家也去官网看一看，请问一下怎样可以把decision tree 可视化呀？ </div>2019-01-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/64/76/0da71882.jpg" width="30px"><span>Mi compaero de armas</span> 👍（1） 💬（1）<div>老师您好，请问采用CART算法时，如果离散型属性的值不止两种还能使用CART算法吗</div>2019-11-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/b5/98/ffaf2aca.jpg" width="30px"><span>Ronnyz</span> 👍（1） 💬（1）<div>第二问
```
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import load_digits

digits = load_digits()

# print(digits)

features=digits.data
labels = digits.target

train_features,test_features,train_labels,test_labels=train_test_split(features,labels,test_size =0.33,random_state=0)

clf = DecisionTreeClassifier(criterion=&#39;gini&#39;)
clf=clf.fit(train_features,train_labels)

predict_labels=clf.predict(test_features)

print(&#39;分类准确度：&#39;,accuracy_score(test_labels,predict_labels))
```
分类准确度： 0.8619528619528619</div>2019-11-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e5/bc/e5ff2613.jpg" width="30px"><span>许宇宝</span> 👍（1） 💬（1）<div>老师，看了两遍还是不明白分类的这个决策树是依据什么画出来的？</div>2019-07-18</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJYEdMwBDUC6gYrUoI7092ocWJPyw1aP8xNOFXxOv7LEw1xj5a4icDibV7pd9vN45lXicXYjB7oYXVqg/132" width="30px"><span>羊小看</span> 👍（1） 💬（1）<div>1、为什么CRAT的基尼系数比C4.5的信息增益率好呢？既然sklearn库默认用的基尼系数，应该是这个好一些吧？
2、from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
#from sklearn.datasets import load_iris
from sklearn.datasets import load_digits

# 准备数据集
#iris=load_iris()
digits=load_digits()
# 获取特征集和分类标识
#features = iris.data
#labels = iris.target
features = digits.data
labels = digits.target
# 随机抽取 33% 的数据作为测试集，其余为训练集
train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size=0.33, random_state=0)
# 创建 CART 分类树
clf = DecisionTreeClassifier(criterion=&#39;gini&#39;)
# 拟合构造 CART 分类树
clf = clf.fit(train_features, train_labels)
# 用 CART 分类树做预测
test_predict = clf.predict(test_features)
# 预测结果与测试集结果作比对
score = accuracy_score(test_labels, test_predict)
print(&quot;CART 分类树准确率 %.4lf&quot; % score)

CART 分类树准确率 0.8636</div>2019-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/c7/a3/1e2f9f5a.jpg" width="30px"><span>圆圆的大食客</span> 👍（1） 💬（1）<div>from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import load_digits
#准备数据集
digits=load_digits()
#获取特征集和分类标识
features = digits.data
labels = digits.target
#随机抽取33%的数据作为测试集，其余为训练集
train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size=0.33, random_state=0)
#创建CART分类树
clf = DecisionTreeClassifier(criterion=&#39;gini&#39;)
#拟合构造CART分类树
clf = clf.fit(train_features, train_labels)
#用CART分类树做预测
test_predict = clf.predict(test_features)
#预测结果与测试集结果作对比 
score = accuracy_score(test_labels, test_predict)
print (&quot;CART分类树准确率%.4lf&quot;% score)</div>2019-02-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/8e/6d/c68e07ef.jpg" width="30px"><span>Chino</span> 👍（1） 💬（1）<div>首先想问一个问题 就是在讲到基尼系数那里 有一个图那里的例子 什么D: 9个打篮球 3个不打篮球那里
那里的D的基尼系数用到了子节点归一化基尼系数之和这个方法求 请问D的基尼系数不能直接用 上面那个公式 也就是&quot;1 - [p(ck|t)]^2&quot;那个公式计算吗  我用这个公式计算出D的基尼系数为 1 - (9&#47;12 * 9&#47;12 + 3&#47;12 * 3&#47;12) = 6&#47;16

# ID3,C4.5,CART在做节点划分的区别
# 我认为是三者的共同之处就是得出每个类别的某个属性值 然后根据这个属性值
# 来选取哪个类型当节点 因此不同之处就是这个属性值.
# ID3 根据 信息增益 判断 哪个节点的信息增益最大就当节点
# C4.5 根据 信息增益率 判断 跟ID3相似
# CART分类树 根据 基尼系数 判断 越小代表越稳定

from sklearn.datasets import load_digits
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


digit = load_digits()

# 把数据集中的数据和结果拿出来
features = digit.data
target = digit.target

# 把数据集中的数据分33%当作测试数据 其他用来训练
train_features,test_features,train_target,test_target = train_test_split(features,target,test_size=0.33)

# 定义CART分类树
clf = DecisionTreeClassifier()

# 把训练数据弄到分类数中 构造树
clf = clf.fit(train_features,train_target)

# 把测试数据放进树中得出预测结果
predict_target = clf.predict(test_features)

# 对比预测出来的数据和实际结果
score = accuracy_score(predict_target,test_target)

print(score)

</div>2019-02-01</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/yZKYKNcLpTJDspoDPEXEJ1w6VSpziaicvXDWauo1k1qAm9Ac9eEWurheHw5AOzoYCtPfZJ53ibqJNH6zoibkq5fWXg/132" width="30px"><span>Melons</span> 👍（0） 💬（1）<div>如果按照第一个公式，数据集D的基尼系数计算方法为1-（9&#47;12 * 9&#47;12 + 3&#47;12 * 3&#47;12）=3&#47;8；请问为什么不能这样算呢？</div>2021-01-14</li><br/><li><img src="" width="30px"><span>lemonlxn</span> 👍（0） 💬（1）<div>使用CART树，做回归或者分类，样本数据类型 有无规定，只能是 分类 或 数值 数据类型，还是两者都可以存在？</div>2020-09-21</li><br/><li><img src="" width="30px"><span>freedomwl</span> 👍（0） 💬（3）<div>老师，波士顿房价代码每次运行结果不一样是因为训练集和测试集每运行一次都会重新随机选取的原因吗？</div>2020-07-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/b5/0d/df1f17b5.jpg" width="30px"><span>哎哟哟</span> 👍（0） 💬（1）<div>1、ID3，C4.5，以及 CART 分类树划分带来信息纯度提高，信息熵下降，ID3、C4.5分别是信息增益和信息增益率越高信息纯度越高，CART是基尼系数越小差距越小
2、照着老师的案例改了一下
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import load_digits

hd = load_digits()
# print(handWrite)
features = hd.data
labels = hd.target

train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size=0.33, random_state=0)

# 创建CART分类树
clf = DecisionTreeClassifier(criterion=&#39;gini&#39;)
# 拟合构造CART分类树
clf = clf.fit(train_features, train_labels)
# 用CART分类树做预测
test_predict = clf.predict(test_features)
# 预测结果与测试集结果作比对
score = accuracy_score(test_labels, test_predict)
print(&quot;CART分类树准确率 %.4lf&quot; % score)</div>2020-04-29</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/ziaN7rOONp15HJm6A9JoAYicJL8VA59x10DX4JZyvcfqmmpCnumXgAkNn37aFoALftyTaQNlUF7te54LibvVm20TQ/132" width="30px"><span>Geek_c9fa4e</span> 👍（0） 💬（1）<div>from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error,mean_squared_error,accuracy_score
from sklearn.tree import DecisionTreeRegressor
data=load_digits()
labels=data.data
features=data.target
x_train,x_test,y_train,y_test=train_test_split(labels,features,test_size=0.2)
dtr=DecisionTreeRegressor()
dtr.fit(x_train,y_train)
data_predict=dtr.predict(x_test)
print(&quot;分类准确率为:&quot;,accuracy_score(y_test,data_predict))</div>2020-04-25</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/1ornnGqSaTxRdbxhUHibeylvYngHvK64ebMaBso6vwXD9I3OEic75dZXxypvwfoCKeKutkpK2d7Xte8Gqh0UH4QA/132" width="30px"><span>Geek_5d8f2f</span> 👍（0） 💬（3）<div>那请问如何应用呢？比方分类树我得出了 0.9600， 那这时候我有一个新数据，如何传入去判别这个新数据呢？？一个头两个大</div>2020-04-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/bf/e3/2aa8ec84.jpg" width="30px"><span>鱼非子</span> 👍（0） 💬（1）<div>
# encoding=utf-8
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
# from sklearn.datasets import load_iris
from sklearn.datasets import load_digits
# 准备数据集
# iris = load_iris()
digits = load_digits()
# 获取特征集和分类标识
# features = iris.data
features = digits.data
labels = digits.target
# labels = iris.target
# 随机抽取33%的数据作为测试集，其余为训练集
train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size=0.33, random_state=0)
# 创建CART分类树
clf = DecisionTreeClassifier(criterion=&#39;gini&#39;)
# 拟合构造CART分类树
clf = clf.fit(train_features, train_labels)
# 用CART分类树做预测
test_predict = clf.predict(test_features)
# 预测结果与测试集结果作比对
score = accuracy_score(test_labels, test_predict)
print(&quot;CART分类树准确率 %.4lf&quot; % score)</div>2020-02-08</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKGRpeljInKj7fUQvwrB9v6kmTOkJlG9ghUoWCXquaDDFmtXeDrEL4p8Gscfx4ZmfeSs2GbZgwwibg/132" width="30px"><span>GodlikeJy</span> 👍（0） 💬（1）<div>对于模型评价，这里需要学习一些统计学知识，混淆矩阵
1. 真阳性（True Positive，TP）：样本的真实类别是正例，并且模型预测的结果也是正例
2. 真阴性（True Negative，TN）：样本的真实类别是负例，并且模型将其预测成为负例
3. 假阳性（False Positive，FP）：样本的真实类别是负例，但是模型将其预测成为正例
4. 假阴性（False Negative，FN）：样本的真实类别是正例，但是模型将其预测成为负例
正确率（Accuracy）：被正确分类的样本比例或数量  (TP+TN)&#47;total</div>2019-12-28</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIx9A2J1pCWjnsg5drDCp1zgYpfwIARUwicIWofKsy0ECMk39iaWltn4lUwJn1GK6OC7jbjicGBBx0tA/132" width="30px"><span>微澜gao</span> 👍（0） 💬（1）<div>请问cart决策树剪枝CCP方法中为什么希望剪枝前后误差最小

</div>2019-09-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/42/f7/67a2e6ee.jpg" width="30px"><span>内存爆了</span> 👍（0） 💬（1）<div>思考题
1、ID3和C4.5，以及CART分类树在做结点划分的时候的区别：
ID3和C4.5在做结点划分的时候，构建成的数可以是多叉树或者二叉树，但是CART算法只能构成二叉树，对于取多个值的属性变量，需要将多个类别合并成两个类别，形成超类，然后计算两个“超类”下样本测试输出取得的差异性。
2、构建分类树
# encoding=utf-8
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import load_digits

# 准备数据集
digits = load_digits()
# 获取特征集和分类标识
features = digits.data
labels = digits.target
# 随机抽取 33% 的数据作为测试集，其余为训练集
train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size=0.33, random_state=0)
# 创建CART 分类树
clf = DecisionTreeClassifier(criterion=&#39;gini&#39;)
# 拟合构造CART分类树
clf = clf.fit(train_features, train_labels)
# 用CART 分类树做预测
test_predict = clf.predict(test_features)
# 预测结果与测试结果做对比
score = accuracy_score(test_labels, test_predict)
print(&quot;CART 分类树准确率 %.4lf&quot; % score)

# 结果：CART 分类树准确率 0.8687</div>2019-07-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/97/77/a01ebefc.jpg" width="30px"><span>Wei_强</span> 👍（0） 💬（1）<div>p(C1|t) 表示节点 t 属于类别 Ck 的概率。这个和条件概率的表达形式有点像，但是意思不一样。我的理解是否正确？</div>2019-07-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/fd/71/2c66cbdd.jpg" width="30px"><span>David</span> 👍（0） 💬（1）<div>为啥CART只支持二叉树呢？</div>2019-07-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/8e/76/6d55e26f.jpg" width="30px"><span>张晓辉</span> 👍（0） 💬（1）<div>#encoding=utf-8
from sklearn.datasets import load_digits
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

digits = load_digits()
features = digits.data 
targets = digits.target 
train_features, test_features, train_digits, test_digits = train_test_split(features, targets, test_size = 0.33)
clf = DecisionTreeClassifier()
clf = clf.fit(train_features, train_digits)
predict_digits = clf.predict(test_features)
print(&quot;The predict accuracy is:&quot;, accuracy_score(test_digits, predict_digits))</div>2019-05-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a3/87/c415e370.jpg" width="30px"><span>滢</span> 👍（0） 💬（1）<div>语言版本：Python 3.6 环境：IDLE

&gt;&gt;&gt;from sklearn.model_selection import train_test_split
&gt;&gt;&gt;from sklearn.metrics import accuracy_score
&gt;&gt;&gt;from sklearn.tree import DecisionTreeClassifier
&gt;&gt;&gt;from sklearn.datasets import load_digits
&gt;&gt;&gt;import ssl
&gt;&gt;&gt;ssl._create_default_https_context = ssl._create_unverified_context
&gt;&gt;&gt;#准备数据
&gt;&gt;&gt;digits = load_gigits()
&gt;&gt;&gt;#获取特征集和分类标识
&gt;&gt;&gt;features = digits.data
&gt;&gt;&gt;labels = digits.target
&gt;&gt;&gt; #随机抽取40%作为测试数据，其余作为训练集
&gt;&gt;&gt;train_features,test_features,train_labels,test_labels = train_test_split(features,labels, test_size = 0.40, random_state = 0)
&gt;&gt;&gt;#创建CART分类树
&gt;&gt;&gt;clf = DecisionTreeClassifier(criterion=&#39;gini&#39;)
&gt;&gt;&gt;#拟合构建CART分类树
&gt;&gt;&gt;clf.fit(train_features, train_labels)
&gt;&gt;&gt;#用CART分类树做预测
&gt;&gt;&gt;test_predic = clf.predict(test_features)
&gt;&gt;&gt;#预测结果与测试结果做比对
&gt;&gt;&gt;score = accuracy_score(test_labels, test_predic)
&gt;&gt;&gt;print (&#39;CART分类树准确率%.4lf&#39;, %score)
CART分类树准确率0.8164</div>2019-04-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f9/81/54b1a5a8.jpg" width="30px"><span>littlePerfect</span> 👍（0） 💬（1）<div>探索数据那一行代码有什么作用?
print(boston.feature_names)</div>2019-02-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7d/05/4bad0c7c.jpg" width="30px"><span>Geek_hve78z</span> 👍（20） 💬（0）<div>1、ID3，C4.5，以及 CART 分类树在做节点划分时的区别吗？
ID3是基于信息增益来判断，信息增益最大的，选取作为根节点。
C4.5采用信息增益率来判断，信息增益率最大的，选取作为根节点。
CART分类树采用基尼系数最小的属性作为属性划分
2、sklearn 中有个手写数字数据集，调用的方法是 load_digits()，你能否创建一个 CART 分类树，对手写数字数据集做分类？另外选取一部分测试集，统计下分类树的准确率？
# 手写数据集load_digits()建立CART分类树
# encoding= utf-8
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import load_digits

#准备数据
digits=load_digits()
#获取特征集和分类标识
features=digits.data
labels=digits.target
#随机抽取33%的数据作为测试集，其余为训练集
train_features,test_features,train_labels,test_labels=train_test_split(features,labels,test_size=0.33,random_state=0)
#创建cart分类树
clf=DecisionTreeClassifier(criterion=&#39;gini&#39;)
#拟合构造cart分类树
clf=clf.fit(train_features,train_labels)
# 用cart分类树做预测
test_predict=clf.predict(test_features)
#预测结果与测试集结果做比对
score=accuracy_score(test_labels,test_predict)
print(&quot;CART 分类树准确率 %.4lf&quot;%score)
-----------
运算结果：CART 分类树准确率 0.8603</div>2019-02-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/a7/f0/e3212f18.jpg" width="30px"><span>胡</span> 👍（18） 💬（2）<div>cart分类树的决策树那副图看不懂。</div>2019-01-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/77/be/1f2409e8.jpg" width="30px"><span>梁林松</span> 👍（4） 💬（0）<div>老师 那个打篮球的例子里 D1&#47;D和D2&#47;D为什么是6&#47;9和2&#47;9呢？如果是子节点占父节点的比例不是应该是各1&#47;2吗？</div>2019-01-23</li><br/>
</ul>