你好，我是黄申。

上一节，我们讲了如何使用矩阵操作，实现基于用户或者物品的协同过滤。实际上，推荐系统是个很大的课题，你可以尝试不同的想法。比如，对于用户给电影评分的案例，是不是可以使用SVD奇异值的分解，来分解用户评分的矩阵，并找到“潜在”的电影主题呢？如果在一定程度上实现这个目标，那么我们可以通过用户和主题，以及电影和主题之间的关系来进行推荐。今天，我们继续使用MovieLens中的一个数据集，尝试Python代码中的SVD分解，并分析一些结果所代表的含义。

## SVD回顾以及在推荐中的应用

在实现SVD分解之前，我们先来回顾一下SVD的主要概念和步骤。如果矩阵$X$是对称的方阵，那么我们可以求得这个矩阵的特征值和特征向量，并把矩阵$X$分解为特征值和特征向量的乘积。

假设我们求出了矩阵$X$的$n$个特征值$λ\_1，λ\_2，…，λ\_n$，以及这$n$个特征值所对应的特征向量$v\_1，v\_2，…，v\_n$，那么矩阵$X$可以表示为：

$X=VΣV^{-1}$
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/13/51/7b/191a2112.jpg" width="30px"><span>愤怒的虾干</span> 👍（11） 💬（1）<div>黄老师，你好，假设X&#39;乘X结果是矩阵A，则V是A的特征向量矩阵，根据几何意义A（i,j）表示的是列向量X,i乘X,j，即电影i和电影j的用户评分乘积；由特征向量的几何意义可知，特征值最大对应的特征向量v表示受众广且评分高（即点评的人多且分数高）的电影，次之是受众广且评分一般或受众窄且评分高的电影，最后特征值最小的表示受众窄且评分低的电影。
同理XX&#39;的特征矩阵U，当特征值最大时表示的是用户有相同审美理念（都对同一类型感兴趣且评分相近），特征值低表示用户间观影理念有较大差异。
综合上述结论，我觉得V并不能区分电影类型。比如特征值最大取出的一组电影大多是评分5且评分人数多，即受众广，第五组大多是评分是4且评分人数不如上面的，即较为受人欢迎。之所以这些数据里电影类型较为雷同，我觉得应该是受众广的电影恰好是这一类的题材导致。请老师看下我说的对吗？</div>2019-06-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/3f/2b/966c348b.jpg" width="30px"><span>zzz</span> 👍（7） 💬（1）<div>为什么SVD对电影分解出来的奇异值是“主题“（科幻类，剧情类……），而不是电影其他的概念，毕竟SVD的输入只是用户与电影的评分数据，没有别的信息。
不过想想电影除了主题好像也没什么别的。</div>2019-04-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/18/d0/49b06424.jpg" width="30px"><span>qinggeouye</span> 👍（5） 💬（0）<div># 优化下 减少运行时间
#https:&#47;&#47;github.com&#47;qinggeouye&#47;GeekTime&#47;blob&#47;master&#47;MathematicProgrammer&#47;50_recomendSystem_SVD&#47;lesson50_2.py
import pandas as pd
import numpy as np
from sklearn.preprocessing import scale


# 加载用户对电影对评分数据
df_ratings = pd.read_csv(&quot;ml-latest-small&#47;ratings.csv&quot;)

# 获取用户对数量和电影对数量 这里只取前 1&#47;10 , 减少数据规模
user_num = int(df_ratings[&quot;userId&quot;].max() &#47; 10)
movie_num = int(df_ratings[&quot;movieId&quot;].max() &#47; 10)
print(user_num, movie_num)
df_ratings = df_ratings[df_ratings[&quot;userId&quot;] &lt;= user_num]
df_ratings = df_ratings[df_ratings[&quot;movieId&quot;] &lt;= movie_num]

# 构造用户对电影对二元关系矩阵
user_rating = np.zeros((user_num, movie_num))

# 由于用户和电影对 ID 都是从 1 开始，为了和 Python 的索引一致，减去 1
df_ratings[&quot;userId&quot;] = df_ratings[&quot;userId&quot;] - 1
df_ratings[&quot;movieId&quot;] = df_ratings[&quot;movieId&quot;] - 1
# 设置用户对电影对评分
for userId in range(user_num):
    user_rating[userId][df_ratings[df_ratings[&quot;userId&quot;] == userId][&quot;movieId&quot;]] = \
        df_ratings[df_ratings[&quot;userId&quot;] == userId][&quot;rating&quot;]

# 二维数组转化为矩阵
x = np.mat(user_rating)

# 标准化每位用户的评分数据 每一行
x_s = scale(x, with_mean=True, with_std=True, axis=1)

# 进行 SVD 奇异值分解
u, sigma, vt = np.linalg.svd(x_s, full_matrices=False, compute_uv=True)
print(&quot;U 矩阵：&quot;, u)
print(&quot;Sigma 奇异值：&quot;, sigma)
print(&quot;V 矩阵：&quot;, vt)

# 加载电影元信息
df_movies = pd.read_csv(&quot;ml-latest-small&#47;movies.csv&quot;)
dict_movies = dict(zip(df_movies[&quot;movieId&quot;], df_movies[&quot;title&quot;] + &quot;, &quot; + df_movies[&quot;genres&quot;]))
print(dict_movies)

# 输出和某个奇异值高度相关的电影 这些电影代表了一个主题
# (注意：向量中电影的 ID 和原始的电影的 ID 相差 1，所以在读取 dict_movies 需要使用 i+1)
print(np.max(vt[1, :]))
print(list(zip(np.where(vt[1] &gt; 0.1)[0] + 1, vt[1][np.where(vt[1] &gt; 0.1)],
               [dict_movies[i] for i in (np.where(vt[1] &gt; 0.1)[0] + 1)])))
</div>2019-04-22</li><br/><li><img src="" width="30px"><span>Paul Shan</span> 👍（4） 💬（0）<div>方阵进行特征值分析以后，特征值表示坐标变换的伸缩部分，特征向量表示对应每个伸缩量对应的方向。非方阵右奇异分量对应的特征值的平方根反映的是该矩阵右乘一个列向量对应变换的伸缩量信息。非方阵左奇异分量对应的特征值的平方根反映的是该矩阵左乘一个行向量对应变换的伸缩信息。

用户-电影矩阵反映的是用户和电影的关系，经过特征向量分解以后，变成用户-主题-电影。因为左右奇异矩阵都是行列式值为1的方阵，主题对角阵也就完全反应了原来矩阵的分量大小，对角阵每个元素大小反映了主题的相对重要程度。主题分量对应的矢量又是原来用户和电影维度线性组合而成。线性组合的系数分别是左奇异阵和右奇异阵，这些系数也反应了用户和主题，以及电影和主题的权重系数（类似线性回归中的权重）。</div>2019-10-22</li><br/><li><img src="" width="30px"><span>013923</span> 👍（1） 💬（0）<div>推荐系统（2）学习！</div>2022-09-23</li><br/>
</ul>