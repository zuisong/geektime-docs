你好，我是景霄。

这是基础版块的最后一节。到目前为止，你已经掌握了 Python 这一门当代武功的基本招式和套路，走出了新手村，看到了更远的世界，有了和这个世界过过招的冲动。

于是，你可能开始尝试写一些不那么简单的系统性工程，或者代码量较大的应用程序。这时候，简单的一个 py 文件已经过于臃肿，无法承担一个重量级软件开发的重任。

今天这节课的主要目的，就是化繁为简，将功能模块化、文件化，从而可以像搭积木一样，将不同的功能，组件在大型工程中搭建起来。

## 简单模块化

说到最简单的模块化方式，你可以把函数、类、常量拆分到不同的文件，把它们放在同一个文件夹，然后使用 `from your_file import function_name, class_name` 的方式调用。之后，这些函数和类就可以在文件内直接使用了。

```
# utils.py

def get_sum(a, b):
    return a + b
```

```
# class_utils.py

class Encoder(object):
    def encode(self, s):
        return s[::-1]

class Decoder(object):
    def decode(self, s):
        return ''.join(reversed(list(s)))
```

```
# main.py

from utils import get_sum
from class_utils import *

print(get_sum(1, 2))

encoder = Encoder()
decoder = Decoder()

print(encoder.encode('abcde'))
print(decoder.decode('edcba'))

########## 输出 ##########

3
edcba
abcde
```

我们来看这种方式的代码：get\_sum() 函数定义在 utils.py，Encoder 和 Decoder 类则在 class\_utils.py，我们在 main 函数直接调用 from import ，就可以将我们需要的东西 import 过来。

非常简单。

但是这就足够了吗？当然不，慢慢地，你会发现，所有文件都堆在一个文件夹下也并不是办法。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJJOlibibPFEWOib8ib7RtfAtxND5FUqCxxoeTuLAbBI9ic23xuwdXT4IyiaWq3Fic9RgEAYI0lBTbEp2rcg/132" width="30px"><span>Jingxiao</span> 👍（254） 💬（3）<div>思考题答案：
很多回复说的很对，from module_name import * 会把 module 中所有的函数和类全拿过来，如果和其他函数名类名有冲突就会出问题；import model_name 也会导入所有函数和类，但是调用的时候必须使用 model_name.func 的方法来调用，等于增加了一层 layer，有效避免冲突。</div>2019-06-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/93/93/c84fe253.jpg" width="30px"><span>上梁山</span> 👍（16） 💬（4）<div>文章中有这么一句话：“import 同一个模块只会被执行一次，这样就可以防止重复导入模块出现问题。”
“import 同一个模块只会被执行一次”，这句话让我这个新手有点困惑。
这里的只会被执行一次，指的是导入模块的语句只执行一次，还是指被导入的模块中的语句只执行一次。
我相信很多向我这样的新手，都会认为是前者。
但是，经过代码实验，这里指的是被导入的模块中的语句只执行一次。

假如现在有main.py和foo.py两个文件，
foo.py中内容如下：
def bar():
    print(&#39;bar&#39;)
print(&#39;hello&#39;)

main.py中内容如下：
from foo import bar
import foo
bar()
foo.bar()
执行python main.py后的结果是：
hello
bar
bar</div>2019-12-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/97/14/20087885.jpg" width="30px"><span>萧潇风</span> 👍（10） 💬（2）<div>export PYTHONPATH=&quot;&#47;home&#47;ubuntu&#47;workspace&#47;your_projects&quot;

在windows系统 中 亲测无效 T_T</div>2019-06-07</li><br/><li><img src="" width="30px"><span>Paul Shan</span> 👍（7） 💬（1）<div>思考题
两者的前缀不同。第一种，把目录下的文件都倒入了，每个文件有各自前缀。第二种，只是倒入了一个前缀，所有文件都通过这个相同前缀。第一种类似于拷贝一个目录下所有文件。第二种类似于拷贝整个目录。</div>2019-11-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/43/2d/af86d73f.jpg" width="30px"><span>enjoylearning</span> 👍（7） 💬（1）<div>作者写的都是原来疑惑的地方，如有时候要新建一个模块总是纠结于是添加文件夹还是包，怀疑加文件夹是不是不如加包规范，有时面对每个文件夹一个空的__init__.py，觉得真是不够优雅，现在好了，原来是2和3的区别，以后可以大胆的用文件夹来组织模块了。另外就是觉得python 命名模块名不能像java和.net那样以公司名.application.web.api格式，觉得还是有点别扭。</div>2019-06-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/30/29/d6816ebf.jpg" width="30px"><span>小侠龙旋风</span> 👍（3） 💬（1）<div>在pycharm里，我会使用“Mark Directory as -&gt; Sources Root”来设置当前文件夹为根目录。
思考题：
1.from module_name import * 能够导入模块下所有的类&#47;函数等内容，使用时不需要包含模块名。容易出现重名现象，发生错误；
2.import module_name 只是将模块名导入，调用时必须模块名.xxx。
3.from  module_name  import  class_name 需要用模块中的哪个类就导入哪个类，比较推荐。</div>2019-06-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/5b/13/6db9ba58.jpg" width="30px"><span>Kevin</span> 👍（2） 💬（1）<div>“import 在导入文件的时候，会自动把所有暴露在外面的代码全都执行一遍。因此，如果你要把一个东西封装成模块，又想让它可以执行的话，你必须将要执行的代码放在 if __name__ == &#39;__main__&#39;下面。”
导入的模块if __name__ == &#39;__main__&#39;下面的语句没有被执行。</div>2020-06-22</li><br/><li><img src="" width="30px"><span>Paul Shan</span> 👍（2） 💬（1）<div>树状结构是大多数项目的组织方式，树状结构本身不复杂，从根节点到每个节点有唯一路径，这条路径可以用一致的方式来引用文件。树状结构可以表达的文件上限是层数的指数，对于大型项目也没问题。如果目录是线性结构，文件一多，查找就费力。文件直接的调用如果用相对路径，这就相当于在树状的结构中引入了中间节点的边，几乎让树成图，复杂度大大增加。</div>2019-11-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/49/8a/3f5af969.jpg" width="30px"><span>大象</span> 👍（2） 💬（1）<div>请教老师一个问题：如果我们所有的项目（项目A，项目B，项目C）都在一个文件夹底下，每个项目都有自己的虚拟运行环境。如果我项目A是公共库，项目B要引用项目A，那么我需要怎么做？谢谢</div>2019-10-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/19/37/e0a9bf99.jpg" width="30px"><span>Geek_59f23e</span> 👍（2） 💬（1）<div>class_utils.py那儿应该是reversed吧，而不是reverse。</div>2019-06-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/96/d5/23fecf33.jpg" width="30px"><span>Hy</span> 👍（1） 💬（1）<div>老师您好，请问这个函数后面的参数是什么意思，没见过这种写法，中间加一个冒号

def mat_mul(matrix_1: Matrix, matrix_2: Matrix)</div>2020-06-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/00/4e/be2b206b.jpg" width="30px"><span>吴小智</span> 👍（1） 💬（1）<div>老师的基础模块，帮助自己扫清了一下知识盲区，期待老师接下来的进阶篇，up,up,up。老师端午节快乐。</div>2019-06-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/f6/0f/0499db2c.jpg" width="30px"><span>ShmilyVidian</span> 👍（0） 💬（1）<div>from module_name import * 是导入module_name 中的所有内容，可以直接调用内部方法容易引入冲突；import module_name，则是导入module_name，在代码中调用必须写成module_name.function的，减少引起冲突，通过module_name做了一层桥接隔离。</div>2020-05-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/b1/16/dd11930c.jpg" width="30px"><span>徐旭</span> 👍（0） 💬（1）<div>赞赞，老师讲得不错</div>2020-03-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/49/8a/3f5af969.jpg" width="30px"><span>大象</span> 👍（0） 💬（1）<div>“事实上，在 Facebook 和 Google，整个公司都只有一个代码仓库，全公司的代码都放在这个库里。”不太理解这里的意思是啥？是类似于在git的同一个组底下么？还是说所有的项目在同一个文件夹底下？</div>2019-10-25</li><br/><li><img src="" width="30px"><span>Sky</span> 👍（0） 💬（1）<div>&gt; 所有文件都堆在一个文件夹下也并不是办法
所以真正的工程化的解法是？</div>2019-06-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/f7/64/03d8154f.jpg" width="30px"><span>可乐泡枸杞</span> 👍（0） 💬（1）<div>端午节快乐。
还没从搜索引擎那缓过来。。先不求甚解一下。</div>2019-06-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/53/af/e5bf5d08.jpg" width="30px"><span>lllong33</span> 👍（0） 💬（1）<div>不推荐使用 *，会导入过多不需要的内容。

from module_name import *，可以直接使用类、函数、变量等
import module_name，需module_name.func()</div>2019-06-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/bc/29/022905e6.jpg" width="30px"><span>SCAR</span> 👍（0） 💬（1）<div>思考题：
from module_name import * 是把module_name下的所有变量或对象映射到当前命名空间，访问调用的话直接写变量或者变量对象调用即可。这种调用方式要注意一点的是如果变量和调用者里变量对象同名或者调用者import其他模块而来的变量同名的话，该变量会覆盖其他同名变量或者被其他同名变量所覆盖。
而import module_name是把module_name映射到当前命名空间，要访问其下的变量或变量对象调用必须加上module_name，比如module_name.xx()。</div>2019-06-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/4b/53/67c08006.jpg" width="30px"><span>John Si</span> 👍（0） 💬（1）<div>老师端午节快乐！

from import module_name import * 和 import module_的主要分别是 from import module_name import * 可直接调用module内的函数或值，假如不是用这种方式import的话，则需透过module_name.xxxxx 方式去调用。

如有错请老师跟各位同学指正或补充。</div>2019-06-07</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eoT9nVNcyrunC5RjsOZwLObffWPgKnsCVcjctqFPNSK6j1XHNibDPQpBVmO6jyIemnepILyTIJ7SQw/132" width="30px"><span>canownu</span> 👍（0） 💬（1）<div>大家端午安康</div>2019-06-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/46/c0/01292b08.jpg" width="30px"><span>GentleCP</span> 👍（0） 💬（1）<div>from module import *之后，module里的函数类都可以直接用该名字调用，而import module调用其类和函数需要在前面加module.函数名（类名）的方式，建议采用第二种，因为这样可以知道某个函数，类是从哪个模块来的，第一种方式万一你有两个模块都有一个同名函数，调用就会出问题</div>2019-06-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/2d/5a/cc637589.jpg" width="30px"><span></span> 👍（0） 💬（1）<div>from module_name import *   是倒入mpdule_name文件中所有的函数、类


import module_name    是倒入文件名，底层的模块需要以  module_name.  的方式进行调用</div>2019-06-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/dd/09/feca820a.jpg" width="30px"><span>helloworld</span> 👍（38） 💬（1）<div>本文中说在 Python 3 规范中，包目录下的__init__.py 并不是必须的，这个我想补充一下，这个__init__.py最好还是有，并且在这个文件里面通过from . import module的形式把该目录下的所有模块文件都写上，如果不这样做，我们只能通过from 包目录 import 模块 的方式来正确使用，而如果直接 import 包目录 的话，虽然import过程不会报错，但是我们在使用该包目录下的模块的时候就会报找不到模块的错误了！</div>2019-07-16</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83er3Yia2VGLEvBfCLWI5NoBn2dlqmY0GdXiadwY8Tofnq6AoRHy7rVicnz7U4R8DUxynpicTp4lZ8K0OcA/132" width="30px"><span>jim</span> 👍（30） 💬（0）<div>from module_name import * 是导入module_name 内的所有内容，可以直接调用内部方法；import module_name，则是导入module_name，在代码中必须写成module_name.function的形式。</div>2019-06-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ce/6d/915ce951.jpg" width="30px"><span>Kuzaman</span> 👍（14） 💬（2）<div>找到一种通用的加载环境变量的方法，很适用于 python虚拟环境virtualenvwrapper-win：
原理：python运行时都会先去site-packages目录下寻找.pth文件，如果有就先加载里面的路径到环境变量中。
操作：在X:\Python36\Lib\site-packages目录下增加一个 xxx.pth文件文件内容是要运行项目的绝对地址，windows操作系统记得使用   \\   作为分隔符。
如果项目路径中有中文，运行python会报错：“UnicodeDecodeError: &#39;gbk&#39; codec can&#39;t decode byte 0xaa in position 42: illegal multibyte sequence”。
解决方案：修改python环境源码 X:\Python36\lib\site.py的159行，由【f = open(fullname, &quot;r&quot;)】修改为【f = open(fullname, &quot;r&quot;,encoding=&#39;utf-8&#39;)】</div>2019-06-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/f3/38/a2e2a81f.jpg" width="30px"><span>书了个一</span> 👍（10） 💬（0）<div>老师端午节快乐！</div>2019-06-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/48/75/02b4366a.jpg" width="30px"><span>乘坐Tornado的线程魔法师</span> 👍（8） 💬（1）<div>老师，对于文中“项目模块化”的段落，有关二维矩阵相乘运算，您给的例子是行与列维度相同的，所以代码运行没有问题；如果您试一下3 x 2的矩阵与2 x 3的矩阵相乘, 例如：[[1, 2], [3, 4], [5, 6]] 与[[5, 6, 7]， [7, 8, 9]]，代码则会报错（索引溢出）。

我改写了一下mat_nul方法：
def mat_mul(matrix_1: Matrix, matrix_2: Matrix):
    assert matrix_1.m == matrix_2.n
    n, s, m = matrix_1.n, matrix_1.m, matrix_2.m
    result = [[0 for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for j in range(s):
            for k in range(m):
                print(i, j, k)
                result[i][k] += matrix_1.data[i][j] * matrix_2.data[j][k]
    return Matrix(result)

我自测通过，请您帮忙验证下！不胜感激!</div>2019-06-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/c5/b7/87e7e865.jpg" width="30px"><span>Smirk</span> 👍（7） 💬（0）<div>这节不错，目录结构那个之前一直用相对路径，但是觉得不干净，也奇怪为什么pycharm可以，但没深究，终于等到老师的文字，赞</div>2019-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/c2/b8/ec758482.jpg" width="30px"><span>Cynthia🌸</span> 👍（6） 💬（0）<div>1. 在 Python 3 规范中，__init__.py 并不是必须的，这只是python2的规范。
2. 项目中，import可以用相对路径，是pycharm的黑魔法。自己也可以通过虚拟环境配置path实现。强烈建议一个项目用一个虚拟环境以保持纯净！
3. import在导入时会把暴露在外面的代码都执行一遍，因此不想执行的话，请加上 if __main__ 的条件判断。</div>2019-07-02</li><br/>
</ul>