你好，我是蒋宏伟。这节课我们来做一次集中答疑。

我在后台留言里见到的最多的问题就是搭建环境卡住了，走不下去。为了方便新同学学习 React Native，更快地搭建好环境，今天我会从头到尾带你搭建一套新环境，帮助你快速上手。

先说结论：**没有畅通无阻的网络，搭建 React Native 环境是较为困难的，但并非不可能。**

在这节课中，我使用的是 MacBook Pro 2016 款，系统版本是 macOS Monterey。我参考的是 React Native 0.71 版的[官方文档](https://reactnative.dev/docs/next/environment-setup)，搭建的 iOS 环境。在按照官方文档搭建的过程中，我也遇到了较多的网络问题，但所有问题都通过镜像的方式解决了。

下面我就具体展示下我的搭建步骤，供你参考。如果遇到更多问题，欢迎给我留言。

## Homebrew

第一步是安装 Homebrew。Homebrew 是 Mac OS 的一个软件包管理器。

React Native 官方文档中，给了我们一个 Homebrew 的安装地址，从该地址可以进入 Homebrew 官方文档。

![图片](https://static001.geekbang.org/resource/image/fc/e1/fc55c1964cdf1848514b5cea04cdcde1.png?wh=1010x113)

该文档中会有如下命令，但执行命令后的结果会报错。

```plain
$ /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
<div><strong>精选留言（11）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/ad/fd/abb7bfe3.jpg" width="30px"><span>JawQ_</span> 👍（0） 💬（0）<div>请问有群吗？刚买了这个课程，就是希望有个共同学习rn的群可以交流一下</div>2024-08-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/af/1f/cb324542.jpg" width="30px"><span>不矫情不做作那是我</span> 👍（0） 💬（0）<div>Installing OpenSSL-Universal (1.1.1100)

[!] Error installing OpenSSL-Universal
[!] &#47;usr&#47;bin&#47;curl -f -L -o &#47;var&#47;folders&#47;dy&#47;y_3zjx6j0rdbcbzgm625f6yc0000gn&#47;T&#47;d20240119-11554-l0dvbm&#47;file.zip https:&#47;&#47;github.com&#47;krzyzanowskim&#47;OpenSSL&#47;archive&#47;1.1.1100.zip --create-dirs --netrc-optional --retry 2 -A &#39;CocoaPods&#47;1.14.3 cocoapods-downloader&#47;2.1&#39;

  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0 --:--:--  0:01:15 --:--:--     0
curl: (28) Failed to connect to github.com port 443 after 75016 ms: Couldn&#39;t connect to server
Warning: Problem : timeout. Will retry in 1 seconds. 2 retries left.
  0     0    0     0    0     0      0      0 --:--:--  0:01:15 --:--:--     0
curl: (28) Failed to connect to github.com port 443 after 75023 ms: Couldn&#39;t connect to server
Warning: Problem : timeout. Will retry in 2 seconds. 1 retries left.
  0     0    0     0    0     0      0      0 --:--:--  0:01:15 --:--:--     0
curl: (28) Failed to connect to github.com port 443 after 75019 ms: Couldn&#39;t connect to server
我这个报错怎么解决啊 哪位大佬知道 实在没办法了</div>2024-01-19</li><br/><li><img src="" width="30px"><span>花永落</span> 👍（0） 💬（0）<div>bundle exec pod install;
报错] Invalid `Podfile` file: exit.

 #  from &#47;Users&#47;luojx&#47;crossEndPro&#47;AwesomeProject&#47;ios&#47;Podfile:35
有遇到该问题的吗?</div>2023-11-19</li><br/><li><img src="" width="30px"><span>Geek_f82ad7</span> 👍（0） 💬（0）<div>Mac OS X 10.11后安装cocoapods应该用下面的命令吧？
sudo gem install -n &#47;usr&#47;local&#47;bin cocoapods</div>2023-10-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/89/6b/3a6ac90e.jpg" width="30px"><span>钙中钙</span> 👍（0） 💬（0）<div>rbenv install 2.7.6的时候， 一直停在

Downloading ruby-2.7.6.tar.bz2...
-&gt; https:&#47;&#47;cache.ruby-lang.org&#47;pub&#47;ruby&#47;2.7&#47;ruby-2.7.6.tar.bz2

请问这个要如何解决啊</div>2023-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/60/84/0f4b3669.jpg" width="30px"><span>北鸟南游</span> 👍（0） 💬（0）<div>error Failed to build iOS project. We ran &quot;xcodebuild&quot; command but it exited with error code 65. 提示这个报错，有知道怎么解决吗？</div>2023-05-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/56/80/fbbac753.jpg" width="30px"><span>Simplelicity</span> 👍（0） 💬（0）<div>Xcode14.3 里面运行不了，提示一堆错误</div>2023-04-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/82/0d/caab8ba1.jpg" width="30px"><span>孤独的二向箔</span> 👍（0） 💬（0）<div>好顶赞！</div>2023-03-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/99/44/b0f3a2cc.jpg" width="30px"><span>墨色</span> 👍（0） 💬（2）<div>老师，能来一个Android的环境搭建吗
</div>2023-03-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/ee/d4/19649482.jpg" width="30px"><span>Euterpe</span> 👍（0） 💬（1）<div>老师，可以讲解下旧的版本如何升级到最新版本么？我尝试了下，各种问题。</div>2023-03-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/96/87/bbdeb4ee.jpg" width="30px"><span>杨永安</span> 👍（0） 💬（1）<div>我半年前折腾不了了之，最近又跑了一次，居然成功了。</div>2023-03-08</li><br/>
</ul>