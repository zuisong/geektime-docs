你好，我是郑建勋。

由于项目一开始就需要涉及到依赖的管理，因此在下一节课正式书写项目代码前，我们先来看一看和依赖管理的一些重要知识。

我们知道，一个大型程序会引入大量必要的第三方库，这就让这个程序形成了复杂的依赖关系网络。这种复杂性可能引发一系列问题，例如**依赖过多、多重依赖、依赖冲突、依赖回圈等**。因此，需要有专门的工具对程序的依赖进行管理。

Go语言中的依赖管理经历了长时间的演进过程。在Go1.5之前，Go官方通过GOPATH对依赖进行管理。但是由于GOPATH存在诸多问题，社区和官方尝试了诸多新的依赖管理工具，中间出现的Godep、Glide、Vendor等工具都不如人意，最终笑到最后的是在Go 1.11后引入，并在Go 1.13之后成为Go依赖管理主流的Go Modules。

让我们先来看看GOPATH和它的不足之处。

## GOPATH

### 什么是GOPATH？

在Go 1.8及以上版本中，如果用户不指定GOPATH，GOPATH的路径就是默认的。我们可以通过输入go env或者go env gopath查看GOPATH的具体配置：

```plain
C:\\Windows\\system32> go env
set GOPATH=C:\\Users\\jackson\\go
...
```
<div><strong>精选留言（10）</strong></div><ul>
<li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83ep075ibtmxMf3eOYlBJ96CE9TEelLUwePaLqp8M75gWHEcM3za0voylA0oe9y3NiaboPB891rypRt7w/132" width="30px"><span>shuff1e</span> 👍（1） 💬（3）<div>能不能上github的项目代码链接？</div>2022-11-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/2e/0c/b6180a5f.jpg" width="30px"><span>风铃</span> 👍（4） 💬（0）<div> 主要是现在大家都习惯了快速上手，突然间讲了这么多理论还没有开始编码，大家就不太理解了，老师最好的有一个大纲展示。</div>2022-11-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/e9/09/e39fde92.jpg" width="30px"><span>cczywyc</span> 👍（3） 💬（0）<div>和Java不同，go编译器不允许循环依赖（编译不会通过）。避免循环依赖就需要一个好的项目结构设计，我目前在开发过程中，会根据业务功能划分模块，设计良好的项目结构，组织好不同包之前的关系，避免循环依赖。</div>2022-11-23</li><br/><li><img src="" width="30px"><span>Geek_2087ad</span> 👍（0） 💬（1）<div>如果使用内网git服务器，仓库前面往往有多级group，
这时怎么用go mod创建或者如何配置才能使用自己的依赖库。
如: 有一个kit的仓库，
路径为：https:&#47;&#47;git.xxx.com&#47;code&#47;go&#47;go-kit.git 
goprivate=&quot;git.xxx.com&#47;*&quot;
然后在另一个仓库中使用这个依赖， 使用go get git.xxx.com&#47;code&#47;go&#47;go-kit
报错：
go: module git.xxx.com&#47;code&#47;go&#47;go-kit: git ls-remote -q origin in &#47;path&#47;xxxxxxx: exit status 128:
        remote: The project you were looking for could not be found or you don&#39;t have permission to view it.
        fatal: repository &#39;https:&#47;&#47;git.xxx.com&#47;code&#47;go.git&#47;&#39; not found</div>2024-07-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f0/6d/3e570bb8.jpg" width="30px"><span>一打七</span> 👍（0） 💬（0）<div>想咨询一下老师，对于伪版本的依赖，每次执行 go mod tidy 时，伪版本都会更新成最新的 commit 吗</div>2024-01-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2e/a3/18/39bdb7ff.jpg" width="30px"><span>列奥纳多是勇者</span> 👍（0） 💬（0）<div>看了十章多理论，感觉有点没劲就没看了，现在积到47章然后再看hh</div>2023-01-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ce/6d/530df0dd.jpg" width="30px"><span>徐石头</span> 👍（0） 💬（0）<div>我觉得最关键的是分清楚每一层的功能和依赖关系，在拆分微服务的时候也是这样，循环依赖都是因为每层的作用没有梳理清楚，如果实在要依赖，就把依赖部分代码拆的更细，不调用业务方法，而是调用底层的存储或者第三方包，少量的重复代码没关系</div>2022-11-21</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaEIqvYMQ1yscgB6xS4nDkoOuP6KiaCiaichQA1OiaQ9rFmNtT9icgrZxeH1WRn5HfiaibDguj8e0lBpo65ricA/132" width="30px"><span>Geek_crazydaddy</span> 👍（0） 💬（0）<div>好菜不怕晚，老师还是按自己的节奏来啊，道与术都很重要啊，甚至有些时候不知道“道”，“术”理解起来就很难，而且知识很难一次就理解透彻，前面说了原理后面代码遇到不懂的地方回头对着看肯定比自己百度谷歌有效率啊，至于循环依赖，个人感觉大部分是由于项目结构或者代码只能不够明确导致的，小面积循环可以复制一份，大面积的就要考虑下项目结构了</div>2022-11-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（0） 💬（0）<div>Go 项目中如果存在循环依赖，编译器是不允许通过的</div>2022-11-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/55/e7/86ae89f0.jpg" width="30px"><span>Jack</span> 👍（0） 💬（0）<div>打卡</div>2022-11-19</li><br/>
</ul>