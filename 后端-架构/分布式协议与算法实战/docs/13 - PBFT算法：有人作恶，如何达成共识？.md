你好，我是韩健。

学完了[01讲](https://time.geekbang.org/column/article/195662)的拜占庭将军问题之后，有同学在留言中表达了自己的思考和困惑：口信消息型拜占庭问题之解在实际项目中是如何落地的呢？先给这位同学点个赞，很棒！你能在学习的同时思考落地实战。

不过事实上，它很难在实际项目落地，因为口信消息型拜占庭问题之解是一个非常理论化的算法，没有和实际场景结合，也没有考虑如何在实际场景中落地和实现。

比如，它实现的是在拜占庭错误场景下，忠将们如何在叛徒干扰时，就一致行动达成共识。但是它并不关心结果是什么，这会出现一种情况：现在适合进攻，但将军们达成的最终共识却是撤退。

很显然，这不是我们想要的结果。因为在实际场景中，我们需要就提议的一系列值（而不是单值），即使在拜占庭错误发生的时候也能被达成共识。那你要怎么做呢？答案就是掌握PBFT算法。

PBFT算法非常实用，是一种能在实际场景中落地的拜占庭容错算法，它在区块链中应用广泛（比如Hyperledger Sawtooth、Zilliqa）。为了帮助你更好地理解PBFT算法，在今天的内容中，我除了带你了解PBFT达成共识的原理之外，还会介绍口信消息型拜占庭问题之解的局限。相信学习完本讲内容后，你不仅能理解PBFT达成共识的基本原理，还能理解算法背后的演化和改进。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/13/95/d1/7d3834ef.jpg" width="30px"><span>笑若海</span> 👍（19） 💬（3）<div>如果接收到小于f+1个消息就认可服务返回结果，可能都是来自f个恶意节点的消息，导致客户端接受恶意结果。f+1保证至少一个正确结果，如果其中存在恶意消息，客户端会发现不一致性，认为请求处理失败。
这又引发一个新问题，客户端怎么确定f值？</div>2020-03-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/14/9f/1146fb91.jpg" width="30px"><span>DFW</span> 👍（18） 💬（3）<div>对于 pbft 算法，核心过程有三个阶段，分别是 pre-prepare （预准备）阶段，prepare （准备）阶段和 commit （提交）阶段。对于 pre-prepare 阶段，主节点广播 pre-prepare 消息给其它节点即可，因此通信次数为 n-1 ；对于 prepare 阶段，每个节点如果同意请求后，都需要向其它节点再 广播 parepare 消息，所以总的通信次数为 n*（n-1），即 n^2-n ；对于 commit 阶段，每个节点如果达到 prepared 状态后，都需要向其它节点广播 commit 消息，所以总的通信次数也为 n*（n-1） ，即 n^2-n 。所以总通信次数为 （n-1）+（n^2-n）+（n^2-n） ，即 2n^2-n-1 ，因此pbft算法复杂度为 O（n^2） 。</div>2020-05-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/f6/e3/e4bcd69e.jpg" width="30px"><span>沉淀的梦想</span> 👍（12） 💬（2）<div>客户端要收到 f+1 个结果，我理解这个是为了防止 f 个叛徒直接给客户端返回 ok。不太理解的是为什么准备阶段要收到 2f 个一致的包含作战指令的准备消息，提交阶段需要 2f+1 个验证通过呢？这两个也设置成 f+1，不可以吗？</div>2020-03-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/83/39/f9623363.jpg" width="30px"><span>竹马彦四郎的好朋友影法師</span> 👍（10） 💬（1）<div>我按照老师第一讲的OM算法写了个简单的递归（https:&#47;&#47;yfscfs.gitee.io&#47;post&#47;极客时间之分布式协议与算法实战-01-拜占庭将军问题有叛徒的情况下如何才能达成共识&#47;） 几乎不可用，22个节点的拜占庭将军问题，至少要吃掉2个G的内存才能跑出结果~</div>2020-05-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/87/30/4626c8c0.jpg" width="30px"><span>Fs</span> 👍（4） 💬（1）<div>这就是为什么区块链的效率提升不上去？达成共识的时间效率太低</div>2020-03-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/b7/50/233b2d12.jpg" width="30px"><span>6 7 8 9 10</span> 👍（4） 💬（1）<div>最后消息数的算法，看不懂呢</div>2020-03-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c5/00/37ef050e.jpg" width="30px"><span>superfq</span> 👍（3） 💬（1）<div>请问老师，f值是怎么确定的？在一个动态集群中怎么确定f值</div>2020-06-17</li><br/><li><img src="" width="30px"><span>myrfy</span> 👍（3） 💬（1）<div>老师，可以详细解释一下视图变更是什么意思吗</div>2020-03-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/98/3b/5af90c80.jpg" width="30px"><span>右耳听海</span> 👍（2） 💬（1）<div>麻烦老师补充下pbft实现一系列共识值pbft做了些什么优化，消息数是随一系列值倍数增加吗</div>2020-03-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/10/e8/ec11e306.jpg" width="30px"><span>Purson</span> 👍（2） 💬（1）<div>如果将军数为 n、叛将数为 f，那么算法需要递归协商 f+1 轮，消息复杂度为 O(n ^ (f + 1))，是怎样算出来的，第一讲说了两轮的能看明白，但是没有说3轮的，找不到递推关系，希望老师详细说一下BFT和PBFT两者区别</div>2020-03-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/55/d8/610fae56.jpg" width="30px"><span>～～</span> 👍（1） 💬（1）<div>假如文中赵作为叛徒发送三个假消息给韩另外三个将军那么最终会不会最终执行的是这个假消息</div>2020-05-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4d/54/9c214885.jpg" width="30px"><span>kylexy_0817</span> 👍（1） 💬（1）<div>韩老师你好，有个细节文中好像没有提及，就是如何在真实的环境中，确定叛军的数量呢？如果一个节点被hack了，签名也能被破解吧？通过回复的消息内容感觉也不太靠谱，例如当叛军比较多时。求解答~</div>2020-05-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/98/3b/5af90c80.jpg" width="30px"><span>右耳听海</span> 👍（1） 💬（1）<div>老师能具体说下pbft实现的是一系列值的共识而不是单值的共识具体指什么吗，一系列值的共识不也可以包装成一个值吗，不如:进攻，准备粮草，这是两个值，但是也可以是在一个消息中</div>2020-03-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/10/e8/ec11e306.jpg" width="30px"><span>Purson</span> 👍（1） 💬（2）<div>口信型的O(n ^ (f + 1))是怎样推导出来的，我看第一章说2轮，第一轮A向 B C D 分别发一个消息，记3，第二轮剩下的3个分别向对方发2消息，记6，加起来总共9，用 4^2好像不太对。除非第一轮的苏秦不是将军，或者n就是忠诚将军数，n=3，就对。但是如果是f=2，一共有7名将军，第二轮协商到底是怎样的顺序？</div>2020-03-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/16/bd/e14ba493.jpg" width="30px"><span>翠羽香凝</span> 👍（1） 💬（2）<div>“口信消息型拜占庭问题之解的局限我想说的是，这个算法有个非常致命的缺陷。如果将军数为 n、叛将数为 f，那么算法需要递归协商 f+1 轮，” 这里看不懂，01讲不是说算法一共是两轮吗？</div>2020-03-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/47/31/f35367c8.jpg" width="30px"><span>小晏子</span> 👍（1） 💬（1）<div>课后思考：因为有f个坏的节点，如果客户端收到的结果小于f，最坏的情况是这f个结果都是坏节点发回来的，所以这就导致了客户端判断错误。所以客户端收到的结果必须大于f个，最少就是f+1个，也就是说最少要有一个好的节点发出来的结果来做判断。</div>2020-03-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/82/3d/356fc3d6.jpg" width="30px"><span>忆水寒</span> 👍（1） 💬（1）<div>PBFT 算法通过视图变更（View Change）的方式，来处理主节点作恶，当发现主节点在作恶时，会以“轮流上岗”方式，推举新的主节点。
老师能详细补充一下吗？</div>2020-03-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4d/54/9c214885.jpg" width="30px"><span>kylexy_0817</span> 👍（0） 💬（1）<div>“当苏秦收到 f+1 个相同的响应（Reply）消息时，说明各位将军们已经就作战指令达成了共识”。韩老师好，对这句话有点困惑，因为f是叛徒数，例子中的叛徒数为1，所以f+1=1+1=2，但忠诚的跟随者就有3个，故此，不应该是接收到3个响应消息才说明将军们达成共识吗？</div>2020-07-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/db/03/67fbb09d.jpg" width="30px"><span>杨冬</span> 👍（0） 💬（1）<div>老师，如果苏秦给赵发送撤退消息，但是叛徒赵会给其他三个将军发送进攻指令，这类问题pbft可以解决吗</div>2020-06-11</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Pr8laRQY3skrzzgen37ZIt4HQvtaThAcqvyK8eAzc9DRiak803q5HS7gCnXFxpx6CWibqT1Sic0h1TLMmVNUpJRibA/132" width="30px"><span>nico</span> 👍（0） 💬（1）<div>老师我有几个问题，客户端如何判断出f?超时时间内没收到指定数量的消息计算吗？这样是不是会产生误判？另外，交互的消息量，如果叛将不是不发消息而是发了消息，交互的消息量也会暴增吧？</div>2020-05-30</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Pr8laRQY3skrzzgen37ZIt4HQvtaThAcqvyK8eAzc9DRiak803q5HS7gCnXFxpx6CWibqT1Sic0h1TLMmVNUpJRibA/132" width="30px"><span>nico</span> 👍（0） 💬（1）<div>1、消息交互过程中的超时怎么配置？网络状态不还好的时候是不是会但是很多失败？另外追后全部都需要发消息给客户端，由客户端计算然后在判断结果，这种是不是增加了客户端的难度？</div>2020-05-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/83/39/f9623363.jpg" width="30px"><span>竹马彦四郎的好朋友影法師</span> 👍（0） 💬（1）<div>韩老师，我是这样理解的——最后客户端怎么认定执行成功了客户端想要的指令呢?  这是因为master节点最多不发送消息，但是不能篡改客户端的消息，所以最后如果&gt;=f+1条响应的话，则一定是达成了客户端想要的一致的.</div>2020-05-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/83/39/f9623363.jpg" width="30px"><span>竹马彦四郎的好朋友影法師</span> 👍（0） 💬（1）<div>OM(m) 的伪代码如下
int *dfs(int x, int m, int *v) &#47;&#47; x是当前指挥官, 运行OM(m)算法, x要向其他人发出的指令集为v, v[i]就是要给i发出的指令(0表示撤退, 1表示进攻), 返回这次OM(m)算法执行完毕后每个人收到的指令
{
	vis[x] = 1; &#47;&#47; 指挥官是不会在他的OM算法中收到消息的, 它只是发送消息
	if (!m) &#47;&#47; x处跑OM(0)
	{
		vis[x] = 0;
		return v;
	}
	int *ans = new int[maxn]; &#47;&#47; ans[i] 是x处OM(m)之后i最终执行的指令
	int **Ans = new int*[maxn]; &#47;&#47; Ans[i] 是 i 处跑完OM(m-1)之后, 每个人最终执行的指令, 即 Ans[i][j] 是i处跑完OM(m-1)之后j执行的指令
	for (re i = 0; i &lt; maxn; i++)
	{
		Ans[i] = new int[maxn];
	}
	for (re i = 0; i &lt; n; i++)
	{
		if (vis[i])
		{
			continue;
		}
		int *cmd = new int[maxn];
		generatecmd(i, cmd, v[i]);
		Ans[i] = dfs(i, m - 1, cmd);
		Ans[i][i] = v[i]; &#47;&#47; i处跑OM(m-1)算法, i并不从i处的OM(m-1)算法处接收指令, 它从x获取的指令是 v[i], 这也是要参与汇总的!
	}
	&#47;&#47; 通过Ans汇总得到ans
	kk(ans, Ans);
	vis[x] = 0;
	for (re i = 0; i &lt; n; i++)
	{
		delete []Ans[i];
	}
	delete Ans; &#47;&#47; 注意回收内存
	return ans;
}
所以 T(m) = nT(m-1), 复杂度应该是O(n!) 而不是 O(n^{f+1})的</div>2020-05-05</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/4uiaFspOvPSF8tzalkP0DvCDme7v53eDGkDMsZsibcm31W99Sib2thFe9m3714d4t7qtIcSeyuR1HiaTXZs4TG8enQ/132" width="30px"><span>钟友兵</span> 👍（0） 💬（1）<div>这个时间复杂度是n^3吧，不是平方，请老师讲解下</div>2020-04-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/18/03/ef0efcc4.jpg" width="30px"><span>EidLeung</span> 👍（0） 💬（2）<div>PBFT需要提前知道叛将的数量么？实际落地过程中不可能提前知道啊，这又该怎么落地？</div>2020-03-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9e/74/6f64f4df.jpg" width="30px"><span>congyh</span> 👍（0） 💬（1）<div>有一个问题想请教韩老师: PBFT算法如何处理集群节点数的变更?</div>2020-03-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/4a/69/0c726378.jpg" width="30px"><span>梁伦</span> 👍（0） 💬（1）<div>图4下面的2f应该为2f+1</div>2020-03-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/01/83/47ba2f2d.jpg" width="30px"><span>单林敏</span> 👍（1） 💬（1）<div>老师您好，消息数最后的 3f - 1 我实在不理解，麻烦您解答：
总共加主节点是 3f + 1 个回复
假设叛徒不回复，也是 2f + 1 个回复

但是这里怎么是 3f - 1 个回复呢？</div>2022-02-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/31/7b/be/791d0f5e.jpg" width="30px"><span>Geek_595be5</span> 👍（0） 💬（0）<div>PBFT也是不完美的吧，上面的2f&#47;2f+1只能保证极端情况，f个假消息，f+1个可信节点得到确认，但并不满足集群的大多数，但此时并未确认提交，极端情况可能提交时都失败
f+1客户端确认，最极端情况其中有f个假消息，也就是流程最极端情况只能确认一个可信节点是已经提交的，此时若客户端认为成功，那仅有的一个可信节点如何在后续能完成至少过半数的共识呢？或者后续反查这个value，如何确认查到的值是否是最新且可信的呢？</div>2023-11-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/31/7b/be/791d0f5e.jpg" width="30px"><span>Geek_595be5</span> 👍（0） 💬（0）<div>感觉上面结论到客户端拿到返回之前，只能保证有效节点超过半数是达成共识的，因为可能前两个阶段有包含f个假消息的极端情况
而且客户端返回f+1只能保证提交前有超过半数的有效节点，而不是集群总数的半数以上节点，达成共识，但是否都提交成功，不确定，因为可能f+1返回有f个假消息返回情况</div>2023-11-28</li><br/>
</ul>