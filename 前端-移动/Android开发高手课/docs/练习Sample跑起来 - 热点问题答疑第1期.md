你好，我是专栏的“学习委员”孙鹏飞。

专栏上线以来很多同学反馈，说在运行练习Sample的时候遇到问题。由于这些Sample多是采用C/C++来完成的，所以在编译运行上会比传统的纯Java项目稍微复杂一些。今天我就针对第1期～第4期中，同学们集中遇到的问题做一期答疑。设置练习的目的，也是希望你在学习完专栏的内容后，可以快速上手试验一下专栏所讲的工具或方法，帮你加快掌握技术的精髓。所以希望各位同学可以多参与进来，有任何问题也可以在留言区给我们反馈，后面我还会不定期针对练习再做答疑。

## 编译环境配置

首先是同学们问得比较多的运行环境问题。

前几期的练习Sample大多是使用C/C++开发的，所以要运行起来需要先配置好SDK和NDK，SDK我们一般都是配置好的，NDK环境的配置有一些特殊的地方，一般我们的Sample都会使用最新的NDK版本，代码可能会使用C++11/14的语法进行编写，并且使用CMake进行编译，我这里给出NDK环境的配置项。

首先需要去NDK官网下载[最新版本](http://developer.android.com/ndk/downloads/)，下载后可以解压到合适的地方，一般macOS可以存放在 ANDROID\_SDK\_HOME/ndk\_bundle目录下，Android Studio可以默认找到该目录。如果放到别的目录，可能需要自己指定一下。
<div><strong>精选留言（8）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/4a/1e/2cbc8d78.jpg" width="30px"><span>CathyChen</span> 👍（3） 💬（0）<div>非常感谢你们的分享，帮助其他人快速成长，虽然有些地方看不懂，还是会坚持下去，(*^__^*) 嘻嘻……</div>2018-12-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/de/15/035d7e8e.jpg" width="30px"><span>peedeep</span> 👍（2） 💬（1）<div>请问下老师，这篇文中提到：5. 如果我们没有原始的 obj，那么需要通过libcrash-lib.so 的导出符号来进行解析。我有以下疑问：这里原始的obj指的是Chapter01&#47;sample&#47;build&#47;intermediates&#47;cmake&#47;debug&#47;obj目录下面的so库吗？什么情况下会变成非原始的呢？
</div>2019-01-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/59/a6/4e185fcb.jpg" width="30px"><span>曹昆</span> 👍（0） 💬（1）<div>请问下老师:Chapter01&#47;sample&#47;build&#47;intermediates&#47;cmake&#47;debug&#47;obj目录下面的so库，
ample&#47;build&#47;intermediates&#47;transforms&#47;mergeJniLibs&#47;debug&#47;0&#47;lib和apk包里的so，这三个so有什么区别呢？还有正式包的so去掉debug info，那aarch64-linux-android-addr2line工具执行之后就没效果了，那正式包怎么看native的crash呢？</div>2019-03-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a3/97/25a2d4f2.jpg" width="30px"><span>Lakers</span> 👍（0） 💬（1）<div>dump_syms  在mac上面怎么生成？这个要在linux下编译才行吗？</div>2018-12-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/47/27/448b5262.jpg" width="30px"><span>我的心情在荡漾</span> 👍（4） 💬（0）<div>鹏飞大佬也好厉害</div>2018-12-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/ca/42/6e0026ad.jpg" width="30px"><span>大白菜</span> 👍（0） 💬（0）<div>Breakpad 抓取闪退信息后执行DumpCallback后就马上闪退了，怎么和java log  当时堆栈关联起来？</div>2019-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/44/e7/474fa6db.jpg" width="30px"><span>wiikzhao</span> 👍（0） 💬（0）<div>gradle文件下，找不到cppFlags和arguments，请问什么原因？</div>2018-12-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/4a/ab/5d8a478f.jpg" width="30px"><span>su</span> 👍（0） 💬（0）<div>dump_syms

这个工具在哪里呢？</div>2018-12-24</li><br/>
</ul>