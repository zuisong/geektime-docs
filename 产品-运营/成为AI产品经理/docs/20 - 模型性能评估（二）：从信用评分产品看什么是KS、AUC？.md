你好，我是海丰。

上节课，我们学习了混淆矩阵，以及准确率、精确率和召回率这3个基础指标的计算。这节课，我们依然会借助上节课的信用评估模型，来学习二分类模型中常用的两个综合性指标，KS和AUC。

## 构建KS和AUC的基础：TPR和FPR

首先，我们来看两个基础指标：TPR和FPR，它们是计算KS和AUC的基础指标。

在信用评分模型中，TPR（True Positive Rate）代表模型找到真坏人（对应混淆矩阵中的TP）占实际坏人（TP+FN）的比例，它的计算公式为TPR=TP/(TP+FN)。一般来说，这个指标被称为：真正率、真阳率，用来评估模型正确预测的能力。不过，因为它的计算公式和召回率是一样的，所以为了方便我们也经常叫它召回率。

FPR（False Positive Rate）代表模型误伤（认为是坏人，实际是好人）的人占总体好人的比例，它的计算公式为FPR=FP/(FP+TN)。一般来说，这个指标被称为：假正率、假阳率，它用来评估模型误判的比率或者误伤的比率，为了方便我们也叫它误伤率。

那这两个指标是怎么构建KS和AUC的呢？别着急，我们慢慢往下看。

## ROC曲线绘制和AUC的计算

在实际工作中，我们最希望的模型一定是找到的坏人足够多，并且误伤的好人足够少，也就是TPR尽量高、FPR尽量低。为了形象地表达它们之间的关系，我们引入了ROC曲线。
<div><strong>精选留言（16）</strong></div><ul>
<li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/ajNVdqHZLLCVPh0bcCMJAwtxBx0cCLlkqB9NckSp3I0LYSTlRezuRV0gpXGB0BCZbFDpvLbhBbzsk8cHvczZ7g/132" width="30px"><span>Sandflass</span> 👍（11） 💬（1）<div>交作业：
以30分作为第一个阈值计算，有100个n，900个p，tn=93，fn=7，tp=5+32+35+48+55+67+88+95+99=524，fp=95+68+65+52+45+33+12+5+1=376，这样换算出tpr=tp&#47;(tp+fn)=0.987，fpr=fp&#47;(fp+tn)=0.802，tpr-fpr=0.185；
同理可算得，
40分阈值tp=519，fp=281，tn=188，fn=12，tpr-fpr=0.977-0.599=0.378
50分阈值tp=487，fp=213，tn=256，fn=44，tpr-fpr=0.917-0.454=0.463
55分阈值tp=452，fp=148，tn=321，fn=79，tpr-fpr=0.851-0.316=0.535
60分阈值tp=404，fp=96，tn=373，fn=127，tpr-fpr=0.761-0.205=0.556
65分阈值tp=349，fp=51，tn=481，fn=182，tpr-fpr=0.657-0.109=0.548
70分阈值tp=282，fp=18，tn=451，fn=249，tpr-fpr=0.531-0.038=0.493
75分阈值tp=194，fp=6，tn=463，fn=337，tpr-fpr=0.365-0.013=0.352
80分阈值tp=99，fp=1，tn=468，fn=432，tpr-fpr=0.186-0.002=0.184
因此，可求得，KS=max(tpr-fpr)=0.556，满足KS的阈值分数为60分。</div>2021-08-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/5d/1c/f2d45010.jpg" width="30px"><span>橙gě狸</span> 👍（5） 💬（0）<div>老师，roc曲线的那个图错了。。。曲面积的边缘没有标蓝，也没有阴影……=3=</div>2021-07-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d3/6e/281b85aa.jpg" width="30px"><span>永光</span> 👍（4） 💬（0）<div>老师你好，同学的疑问，我发现我也有同样的疑问
1、@蓝白胖子 说的OOT 测试的 KS 是 40，测试集的 KS 是 39，训练集的 KS 是 35。虽然我们用的都是真实数据，但结果依然不合理    这个是为什么呀，不理解。
2、@ AsyDong 说的，三条曲线，一定是平滑的曲线吗，可能是折线等吗？
3、@ Rosa rugosa 说的  作业中，没有真实的好人与坏人，怎么计算TPR FPR 呀？
还请老师多多讲解，谢谢</div>2021-05-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/3c/f4/4013984e.jpg" width="30px"><span>gjbbjj</span> 👍（3） 💬（0）<div>看不懂，一头雾水</div>2021-04-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/98/4e/f42d27e8.jpg" width="30px"><span>Rosa rugosa</span> 👍（2） 💬（1）<div>1，老师，作业的表格中人数比例是真实好人的人数比例吗？
2，预测好人坏人为（32,68）时不知预测中有多少好人是真的好人，有多少坏人是真的坏人。怎么计算TPR,FPR呢？</div>2021-03-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/76/17/f931f7ba.jpg" width="30px"><span>Pale Blue</span> 👍（1） 💬（0）<div>根据表格可知：在1000个样本中共有531个good，469个bad。
当30为阈值时：有900个positive， 100个negative。此时，TP = 524, FN= 7, FP = 376, TN=93。
TPR = 524&#47;531 = 0.987,  FPR = 0.802, TPR - FPR = 0.185;
当40为阈值时：有800个positive，200个negative。此时， TP = 519, FN= 12, FP = 281,  TN = 188.
TPR - FPR = 0.977-0.599=0.378;
阈值为50：TPR - FPR = 0.917 - 0.454 = 0.463
阈值为55：TPR - FPR = 0.851- 0.316 = 0.535
阈值为60：TPR - FPR = 0.761- 0.205 = 0.556
阈值为65：TPR - FPR = 0.657- 0.109 = 0.548
阈值为70：TPR - FPR = 0.531- 0.038 = 0.493
阈值为75：TPR - FPR = 0.365- 0.013 = 0.352
阈值为80：TPR - FPR = 0.186- 0.002 = 0.184
得，KS = max（TPR - FPR） = 0.556
所以阈值分数取60</div>2021-11-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/5d/71/4f6aad17.jpg" width="30px"><span>Sophia-百鑫</span> 👍（0） 💬（0）<div>数据表的含义如下：
最大值列 - 阈值即各个分切点， 30 ，40 ，50 …
人数列 -  各个分切范围下的预测值 
goods (negative） 和 bads （positive）是 各个分切范围内的真实值， 真实的好人数和真实的坏人数 
在1000个样本中，真实的好人数 = TN+ FP = 上表中 所有 goods列的总和 即 531 
在1000个样本中，真实的坏人数 = TP+ FN= 上表中 所有  bads列的总和 即 469

以40为阈值，即大于40 是 好人，小于等于40  是坏人 。
模型预测出坏人数 =  200 ， 预测出好人数 = 800
混淆矩阵中关键数据如下：
	TP =93+95=188
	FP= 7+5=12
计算TPR 和FPR 如下：（备注如下值 小数点后做了位数保留。大家关注逻辑即可）
TPR =188&#47;469 =0.401
FPR =12&#47;531 = 0.0226  
KS =TPR-FPR = 0.378

同逻辑计算 ，分切点 是 30 ，50，55，60 …..  的 KS
得到 分切点是60 时，ks 最大 0.556 
</div>2024-01-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/5d/9f/4cfa4918.jpg" width="30px"><span>Baymax</span> 👍（0） 💬（0）<div>P=469    
N=531
TPR=TP&#47;(TP+FN)=TP&#47;P=TP&#47;469
FPR=FP&#47;(FP+TN)=FP&#47;N=FP&#47;531

如果切分点为30，TP=93，FP=7，则TPR=93&#47;469=0.198，FPR=7&#47;531=0.013

切分点     TPR                     FPR         
0              0                          0  
30            0.013182674       0.198294243
40            0.02259887         0.400852878
50            0.082862524       0.545842217
55            0.148775895       0.684434968
60            0.239171375       0.795309168
65            0.342749529       0.891257996
70            0.468926554       0.961620469
75            0.634651601       0.987206823
80            0.813559322       0.997867804
100          1                          1

根据以上离散的点绘制曲线，然后找到FPR- TPR最大的切分点，如果只以以上离散点判断的话，切分点为60，KS=max（FPR-TPR）=0.556137794</div>2024-01-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/38/55/b6/8673d349.jpg" width="30px"><span>潘平</span> 👍（0） 💬（0）<div>这里讲的对分类模型的评估，看起来只适用于二分类，多分类的如何评估呢？</div>2023-08-28</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/sgEfkeMSIIibeH4l0HS8uwGB5PKKDCLgo0RbV8QTfY6am1OYxBEY8g74WUnWkWl9azUX5XqvcbrMxSxmJXSibCcw/132" width="30px"><span>Geek_23daec</span> 👍（0） 💬（0）<div>为什么不同测试集的KS值不同就不合理呢？这不是很正常吗？KS主要是召回率和误伤率的最大值，那么不同的测试集TPR和FPR有偏差不是也正常么，还是说这样代表模型的泛化能力太差</div>2023-01-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/01/88/9b0e2912.jpg" width="30px"><span>299号女孩</span> 👍（0） 💬（0）<div>题目里的最小值和最大值是什么意思？</div>2022-12-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/61/15/41d914d8.jpg" width="30px"><span>啊哈小可爱</span> 👍（0） 💬（0）<div>同问，@ Rosa rugosa 说的  作业中，没有真实的好人与坏人，怎么计算TPR FPR 呀？</div>2022-10-12</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLjrPm3HE2KwDk2P2MhR8NourkC9lgFH7M3D0NEJaVkzoYR2stx83XicWciazq9J3pUzglN6c6fHPPw/132" width="30px"><span>Geek_bf0a76</span> 👍（0） 💬（0）<div>KS=55</div>2022-05-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ee/c6/bebcbcf0.jpg" width="30px"><span>俯瞰风景.</span> 👍（0） 💬（0）<div>在贷前信用评分场景下，KS 值大于 50 或者 AUC 大于 80 时，我们就需要注意一下数据的准确性了。

KS 越大，业务收益越大；
AUC越大，模型的区分能力越好；

为什么要注意数据的准确性呢？是因为模型太理想了么？和数据关联太强，拟合度太高了？</div>2021-08-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/76/de/922aaaf4.jpg" width="30px"><span>蓝白胖子</span> 👍（0） 💬（3）<div>“OOT 测试的 KS 是 40，测试集的 KS 是 39，训练集的 KS 是 35。虽然我们用的都是真实数据，但结果依然不合理”  为什么呢？不是很理解</div>2021-05-08</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKGNb0iaXNtliaO2UYrzn6j7DgoH4PC9UCQ1euV7xuI92GQ779IIBhI99GCDASBQ1C7RE7dz2nMPibLg/132" width="30px"><span>AsyDong</span> 👍（0） 💬（0）<div>我想问一下ROC曲线、TPR曲线、FPR曲线，这三条线一定是曲线吗？还是说他们有可能也是不规则的图形？他们也是通过算法建模得出来的嘛？</div>2021-04-21</li><br/>
</ul>