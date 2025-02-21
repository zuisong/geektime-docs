你好，我是孔令飞。

今天我们更新一期特别放送作为加餐。在部署和使用IAM的过程中，难免会出现一些异常(也称为故障、问题)。这时候，就需要我们能够定位故障，并修复故障。这里，我总结了一些IAM的排障方法，以及一些常见故障的解决方法，供你参考。

## 如何排障？

首先，我们需要发现问题，然后定位问题。我们可能需要经过多轮分析排查才能定位到问题的根因，最后去解决问题。排障流程如下图所示：

![](https://static001.geekbang.org/resource/image/73/0f/7330d836e7c4b5052c79bbd365abdd0f.jpg?wh=2248x535)

如果想排查问题并解决问题，你还需要具备这两个基本能力：能够理解错误日志的内容；根据错误日志，找出解决方案。

我们举个例子来说吧。有以下错误：

```bash
[going@dev iam]$ mysql -h127.0.0.1 -uroot -p'iam59!z$'
bash: /usr/bin/mysql: 没有那个文件或目录
[going@dev iam]$
```

对于这个错误，我们首先来理解错误内容：mysql命令没有找到，说明没有安装mysql，或者安装mysql失败。

那么，我们的解决方案就是重新执行 [03讲](https://time.geekbang.org/column/article/378082) 中安装MariaDB的步骤：

```bash
$ cd $IAM_ROOT
$ ./scripts/install/mariadb.sh iam::mariadb::install
```
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/28/83/17/df99b53d.jpg" width="30px"><span>随风而过</span> 👍（2） 💬（1）<div>借助前面讲过的日志工具辅助快速定位，token为空这个是最常见的错误，生成token的重要信息显示日志，为空的情况做一些处理，禁止token 值为空</div>2021-09-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/dd/09/feca820a.jpg" width="30px"><span>helloworld</span> 👍（1） 💬（1）<div>文中提到添加已存在用户导致的500错误db error，个人认为用户已存在这种是否应该加一层校验，返回400错误，直接提示用户已存在信息</div>2021-11-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/80/b2/2e9f442d.jpg" width="30px"><span>文武木子</span> 👍（1） 💬（1）<div>systemtcl和supervisor哪个好点，我们公司运维都用supervisor管理部署发布的应用进程</div>2021-10-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9d/a4/e481ae48.jpg" width="30px"><span>lesserror</span> 👍（1） 💬（1）<div>多谢老师，这些排障技巧在日常开发中也很用。</div>2021-09-18</li><br/>
</ul>