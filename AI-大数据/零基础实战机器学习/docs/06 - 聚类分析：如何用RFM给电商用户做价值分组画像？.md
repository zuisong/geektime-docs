你好，我是黄佳。欢迎来到零基础实战机器学习。

在上一讲中，我们从一份互联网电商“易速鲜花”的历史订单数据集中，求出了每一个用户的R、F、M值。你可能会问，从这些值中，我们又能看出什么有价值的信息呢？

别着急，在这一讲中，我们继续往前走，看看如何从这些枯燥且不容易观察的数据中，得到更为清晰的用户分组画像。通过这节课，我希望你能理解聚类算法的原理和最优化过程，这可以帮你建立起针对问题选择算法的直觉。

## 怎么给用户分组比较合适？

这是我们在上节课中得出的用户层级表，表中有每位用户的R、F、M值。

![](https://static001.geekbang.org/resource/image/13/c2/13bc1375b789e5173ce3016b84a01dc2.png?wh=260x208)

这里，我们希望看看R值、F值和M值的分布情况，以便为用户分组作出指导。代码是接着上一讲的基础上继续构建，我就不全部贴上来了，完整的代码和数据集请你从[这里](https://github.com/huangjia2019/geektime/tree/main/%E8%8E%B7%E5%AE%A2%E5%85%B306)下载。

```typescript
df_user['R值'].plot(kind='hist', bins=20, title = '新进度分布直方图') #R值直方图
```

```typescript
df_user.query('F值 < 800')['F值'].plot(kind='hist', bins=50, title = '消费频率分布直方图') #F值直方图
```

```typescript
df_user.query('M值 < 20000')['M值'].plot(kind='hist', bins=50, title = '消费金额分布直方图') #M值直方图
```
<div><strong>精选留言（16）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/d6/97/035a237b.jpg" width="30px"><span>Jove</span> 👍（34） 💬（3）<div>1、绘制三维图
df_user[&#39;三维价值&#39;] = KMeans(n_clusters=3).fit(df_user[[&#39;R值&#39;, &#39;F值&#39;, &#39;M值&#39;]]).predict(df_user[[&#39;R值&#39;, &#39;F值&#39;, &#39;M值&#39;]])

ax = plt.subplot(111, projection=&#39;3d&#39;)
ax.scatter(df_user.query(&quot;三维价值 == 0&quot;)[&#39;F值&#39;],
           df_user.query(&quot;三维价值 == 0&quot;)[&#39;R值&#39;],
           df_user.query(&quot;三维价值 == 0&quot;)[&#39;M值&#39;], c=&#39;y&#39;)
ax.scatter(df_user.query(&quot;三维价值 == 1&quot;)[&#39;F值&#39;],
           df_user.query(&quot;三维价值 == 1&quot;)[&#39;R值&#39;],
           df_user.query(&quot;三维价值 == 1&quot;)[&#39;M值&#39;], c=&#39;r&#39;)
ax.scatter(df_user.query(&quot;三维价值 == 2&quot;)[&#39;F值&#39;],
           df_user.query(&quot;三维价值 == 2&quot;)[&#39;R值&#39;],
           df_user.query(&quot;三维价值 == 2&quot;)[&#39;M值&#39;], c=&#39;g&#39;)

ax.set_zlabel(&#39;F&#39;)  # 坐标轴
ax.set_ylabel(&#39;R&#39;)
ax.set_xlabel(&#39;M&#39;)
plt.show()

2、我从事的行业的是信贷，也可以从用户征信情况、借贷金额、违约次数等来聚合为用户划分评级</div>2021-09-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/6a/74/c39efead.jpg" width="30px"><span>吴悦</span> 👍（14） 💬（1）<div>多维数据输入时怎么做 无量纲化好呀</div>2021-09-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/f7/ee/f7f45ca9.jpg" width="30px"><span>吃鱼</span> 👍（6） 💬（2）<div>我把 R、F、M 三个特征同时输入 K-Means 算法，并与文中提到的先分别聚类再求和两种方法进行比较，结果如下：
1） 直接聚类和分别聚类的结果很近似，只有28（共980）个实例分组不同。
2） 直接聚类会面临无法人为定义价值高低的情况，也就是聚类结果无法概念化，这次实验中就存在分组结果的三个指标并非都能按照某种顺序排序的情况。尤其是在特征维度过高时，可能得到无意义的结果。
3）分别聚类再求和的方式有更强的灵活性，更方便人为操作，比如人为赋予权重，人为划定总分的分组区间，从而得到我们想要的结果。
4）第一次实验没有使用归一化，但当我们使用MinMaxScaler规范化之后，结果反而变得很奇怪，三维图像的分簇结果不如不规范化的清晰。猜测可能是因为RFM三个值本身就时不同尺度，强行化为同一尺度并不一定会让结果看起来更合理。另一方面也说明，聚类最好用在相同或相似的尺度特征下，比如图像处理时的RBG颜色分组就很适合使用聚类。</div>2022-12-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/66/8f/02be926d.jpg" width="30px"><span>在路上</span> 👍（6） 💬（1）<div>佳哥好，今天是教师节，祝你节日快乐。我看了下kmeans的API，fit函数支持多维数组，应该可以把RFM三个维度的值同时传给fit进行拟合，而不是把RFM三个维度的值降维到一个值进行拟合，通过predict函数就可能直接得到聚类后的层级，从predict函数的名称可以得知，它不仅能计算训练集的聚类层级，也能预测新数据的聚类层级。
我从事游戏行业，策划会根据玩家充值金额来定义大中小R，充值区间的定义全凭经验，如果用今天教的k-means方法就非常合适。我最近在学习大数据，想统计HDSF上文件大小的分布情况，也可以用k-means算法。
最后说一下我发现这节课的文本和表格的部分数据有出入。文本：上次购物距今是0天到91天，表格：是94天。文本：0层级的用户平均新近度是295天，表格：是298天。文本：R值最高的用户组（2层级）平均新近度仅有31天，表格：是32天。</div>2021-09-10</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJbR7zvuCTdqo679ghibNZ2NJ9gXEaNvlw4zau6mex0sUAo3wvtvyUJspUAVmhfVXqiaSYVXrGpRJ7w/132" width="30px"><span>Geek_8629f4</span> 👍（2） 💬（1）<div>老师，请问， 当把 R、F、M 三个特征同时输入 K-Means 算法，为用户整体做聚类时， 发现 分为3 组， 但是 每组人数相差很大， A 组 7 人 B 组 60 , C 组913人，如果时这样，这种分组意思不大， 没有好的办法制定marketing 的策略。请问是我们必须要分别分类聚类才能得到更好的效果， 我的聚类方法有什么不对的地方。实际分析中，应该如何操作呢？</div>2022-11-17</li><br/><li><img src="" width="30px"><span>庞亮</span> 👍（1） 💬（1）<div>“最后，我们还讲到用 K- 均值算法来给 R 值做聚类，这也非常简单，就是创建模型、拟合模型、用模型进行聚类，这些过程加一块也就是几行代码的事儿，你不用有负担。”
这句说了两遍</div>2022-06-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/dd/6a/c47ef5aa.jpg" width="30px"><span>Yaohong</span> 👍（1） 💬（2）<div>请问 order_cluster函数中new_cluster_name = &#39;new_&#39; + cluster_name #新的聚类名称，这个有什么作用？后面分组中用mean()方法而不用max（）方法有什么考量？</div>2022-04-23</li><br/><li><img src="" width="30px"><span>Geek_7ba002</span> 👍（1） 💬（1）<div>这节课让我真正理解了什么是聚类</div>2022-03-02</li><br/><li><img src="" width="30px"><span>Geek_7ba002</span> 👍（1） 💬（1）<div>这堂课我真正理解了sklearn</div>2022-03-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/0c/18/298a0eab.jpg" width="30px"><span>小强</span> 👍（1） 💬（1）<div>这章的代码在哪可以看到</div>2021-10-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/02/42/e8ef9639.jpg" width="30px"><span>蝶舞清风寒</span> 👍（1） 💬（2）<div>R、F、M 三个特征同时输入 K-Means 算法，为用户整体做聚类程序代码如下，是否正确呢？
train_x=df_user[[&quot;R值&quot;,&quot;F值&quot;,&quot;M值&quot;]]#将RFM数值转变为训练数据
# 规范化到[0,1]空间
min_max_scaler=preprocessing.MinMaxScaler()
train_x=min_max_scaler.fit_transform(train_x)
kmeans_RFM = KMeans(n_clusters=3) #设定K=3
kmeans_RFM.fit(train_x) #拟合模型
RFM_label = kmeans_RFM.predict(train_x) #通过聚类模型求出R值的层级
df_user[&#39;标签&#39;]= RFM_label #通过聚类模型求出R值的层级
df_user = order_cluster(&#39;标签&#39;, [&quot;R值&quot;,&quot;F值&quot;,&quot;M值&quot;], df_user, False) #调用簇排序函数
df_user = df_user.sort_values(by=&#39;用户码&#39;,ascending=True).reset_index(drop=True) #根据用户码排序
</div>2021-09-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/bf/6f/1916fba0.jpg" width="30px"><span>贝贝</span> 👍（0） 💬（1）<div>如果不用数据可视化，如何通过手肘法找到K值呢？</div>2024-03-29</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83epbtcXw5PHzibHcXlupLmnZOYXBLR10U4Hvn5tib14EYlkMBERYgGlgZ63BxgFSBTQmUErfSXibcKl6w/132" width="30px"><span>Geek_maxwell</span> 👍（0） 💬（1）<div>kmeans = kmeans.fit(df) #拟合模型 这个好像不能重新赋值给kmeans， 不然后面的kmeans.inertia_就没有了</div>2022-08-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/d6/f8/cb21b43c.jpg" width="30px"><span>松饼Muffin</span> 👍（0） 💬（1）<div> 老师， 我算出来的`R值` 是 timedelta64[ns] 格式， 如`70 days 20:39:00`, 如何转成70呢？我是用很土的方法硬转，应该有更优雅的办法吧？
 RFM[&#39;recency&#39;] = RFM[&#39;recency&#39;] .astype(&#39;str&#39;).str.split(&#39; days&#39;).str.get(0).astype(&#39;int&#39;)</div>2022-03-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/16/cb/680635e2.jpg" width="30px"><span>wiki</span> 👍（1） 💬（0）<div>还有个问题，手肘法选质点。如果是数据很大的情况下，show_elbow 这种方式应该会负担很大吧。主要考虑质点的range范围和模型拟合的数据量</div>2024-08-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/d9/ce/4528cb4b.jpg" width="30px"><span>呼呼</span> 👍（1） 💬（2）<div>老师我有个疑问，为聚类的层级做排序（R值），按理说不应该改变R值本身吧？那为什么课程中前后R值统计出来的count、mean等值不一样了呢？</div>2024-03-02</li><br/>
</ul>