你好，我是景霄。

世纪之交的论坛上曾有一句流行语：在互联网上，没人知道你是一条狗。互联网刚刚兴起时，一根网线链接到你家，信息通过这条高速线缆直达你的屏幕，你通过键盘飞速回应朋友的消息，信息再次通过网线飞入错综复杂的虚拟世界，再进入朋友家。抽象来看，一台台的电脑就是一个个黑箱，黑箱有了输入和输出，就拥有了图灵机运作的必要条件。

Python 程序也是一个黑箱：通过输入流将数据送达，通过输出流将处理后的数据送出，可能 Python 解释器后面藏了一个人，还是一个史莱哲林？No one cares。

好了废话不多说，今天我们就由浅及深讲讲 Python 的输入和输出。

## 输入输出基础

最简单直接的输入来自键盘操作，比如下面这个例子。

```
name = input('your name:')
gender = input('you are a boy?(y/n)')

###### 输入 ######
your name:Jack
you are a boy?

welcome_str = 'Welcome to the matrix {prefix} {name}.'
welcome_dic = {
    'prefix': 'Mr.' if gender == 'y' else 'Mrs',
    'name': name
}

print('authorizing...')
print(welcome_str.format(**welcome_dic))

########## 输出 ##########
authorizing...
Welcome to the matrix Mr. Jack.
```

input() 函数暂停程序运行，同时等待键盘输入；直到回车被按下，函数的参数即为提示语，输入的类型永远是字符串型（str）。注意，初学者在这里很容易犯错，下面的例子我会讲到。print() 函数则接受字符串、数字、字典、列表甚至一些自定义类的输出。

我们再来看下面这个例子。

```
a = input()
1
b = input()
2

print('a + b = {}'.format(a + b))
########## 输出 ##############
a + b = 12
print('type of a is {}, type of b is {}'.format(type(a), type(b)))
########## 输出 ##############
type of a is <class 'str'>, type of b is <class 'str'>
print('a + b = {}'.format(int(a) + int(b)))
########## 输出 ##############
a + b = 3
```

这里注意，把 str 强制转换为 int 请用 int()，转为浮点数请用 float()。而在生产环境中使用强制转换时，请记得加上 try except（即错误和异常处理，专栏后面文章会讲到）。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJJOlibibPFEWOib8ib7RtfAtxND5FUqCxxoeTuLAbBI9ic23xuwdXT4IyiaWq3Fic9RgEAYI0lBTbEp2rcg/132" width="30px"><span>Jingxiao</span> 👍（60） 💬（7）<div>思考题第二题：（省略了一些异常处理，后面会讲到）
server.py
# 我们假设 server 电脑上的所有的文件都在 BASR_DIR 中，为了简化不考虑文件夹结构，网盘的路径在 NET_DIR

import os
from shutil import copyfile
import time

BASE_DIR = &#39;server&#47;&#39;
NET_DIR = &#39;net&#47;&#39;

def main():
    filenames = os.listdir(BASE_DIR)
    for i, filename in enumerate(filenames):
        print(&#39;copying {} into net drive...  {}&#47;{}&#39;.format(filename, i + 1, len(filenames)))
        copyfile(BASE_DIR + filename, NET_DIR + filename)
        print(&#39;copied {} into net drive, waiting client complete...  {}&#47;{}&#39;.format(filename, i + 1, len(filenames)))

        while os.path.exists(NET_DIR + filename):
            time.sleep(3)

    print(&#39;transferred {} into client.  {}&#47;{}&#39;.format(filename, i + 1, len(filenames)))

if __name__ == &quot;__main__&quot;:
	main()

++++++++++++++++++++++
client.py
# 我们假设 client 电脑上要输出的文件夹在 BASR_DIR ，网盘的路径在 NET_DIR

import os
from shutil import copyfile
import time

BASE_DIR = &#39;client&#47;&#39;
NET_DIR = &#39;net&#47;&#39;

def main():
    while True:
        filenames = os.listdir(NET_DIR)
        for filename in filenames:
            print(&#39;downloading {} into local disk...&#39;.format(filename))
            copyfile(NET_DIR + filename, BASE_DIR + filename)
            os.remove(NET_DIR + filename) # 我们需要删除这个文件，网盘会提我们同步这个操作，从而 server 知晓已完成
            print(&#39;downloaded {} into local disk.&#39;.format(filename))
        time.sleep(3)

if __name__ == &quot;__main__&quot;:
	main()</div>2019-05-26</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJJOlibibPFEWOib8ib7RtfAtxND5FUqCxxoeTuLAbBI9ic23xuwdXT4IyiaWq3Fic9RgEAYI0lBTbEp2rcg/132" width="30px"><span>Jingxiao</span> 👍（53） 💬（20）<div>思考题第一题：

import re

CHUNK_SIZE = 100 # 这个数表示一次最多读取的字符长度

# 这个函数每次会接收上一次得到的 last_word，然后和这次的 text 合并起来处理。
# 合并后判断最后一个词有没有可能连续，并分离出来，然后返回。
# 这里的代码没有 if 语句，但是仍然是正确的，可以想一想为什么。
def parse_to_word_list(text, last_word, word_list):
    text = re.sub(r&#39;[^\w ]&#39;, &#39; &#39;, last_word + text)
    text = text.lower()
    cur_word_list = text.split(&#39; &#39;)
    cur_word_list, last_word = cur_word_list[:-1], cur_word_list[-1]
    word_list += filter(None, cur_word_list)
    return last_word

def solve():
    with open(&#39;in.txt&#39;, &#39;r&#39;) as fin:
        word_list, last_word = [], &#39;&#39;
        while True:
            text = fin.read(CHUNK_SIZE)
            if not text: 
                break # 读取完毕，中断循环
            last_word = parse_to_word_list(text, last_word, word_list)

        word_cnt = {}
        for word in word_list:
            if word not in word_cnt:
                word_cnt[word] = 0
            word_cnt[word] += 1

        sorted_word_cnt = sorted(word_cnt.items(), key=lambda kv: kv[1], reverse=True)
        return sorted_word_cnt

print(solve())</div>2019-05-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/51/ea/d9a83bb3.jpg" width="30px"><span>古明地觉</span> 👍（63） 💬（15）<div>from collections import defaultdict
import re

f = open(&quot;ini.txt&quot;, mode=&quot;r&quot;, encoding=&quot;utf-8&quot;)
d = defaultdict(int)

for line in f:
    for word in filter(lambda x: x, re.split(r&quot;\s&quot;, line)):
        d[word] += 1


print(d)</div>2019-05-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/94/6a/fed08431.jpg" width="30px"><span>逆光飞翔</span> 👍（31） 💬（3）<div>老师，为什么filter（none，list）可以过滤空值，不是保留空值嘛</div>2019-05-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7a/d9/4feb4006.jpg" width="30px"><span>lmingzhi</span> 👍（12） 💬（2）<div># 第一题， 修改parse函数，使其可以更新word_cnt
import re
def parse(text, word_cnt):
    # 转为小写
    text = text.lower()    
    # 生成所有单词的列表
    word_list = re.findall(r&#39;\w+&#39;, text) 
    # 更新单词和词频的字典
    for word in word_list:
        word_cnt[word] = word_cnt.get(word,0) + 1
    return word_cnt

# 初始化字典
word_cnt = dict()
with open(&#39;in.txt&#39;, &#39;r&#39;) as fin:
    for text in fin.readlines():
        word_cnt = parse(text, word_cnt)
        print(len(word_cnt))

# 按照词频排序
sorted_word_cnt = sorted(word_cnt.items(), key=lambda kv: kv[1], reverse=True)

# 导出
with open(&#39;out.txt&#39;, &#39;w&#39;) as fout:
    for word, freq in word_and_freq:
        fout.write(&#39;{} {}\n&#39;.format(word, freq))</div>2019-05-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f8/99/8e760987.jpg" width="30px"><span>許敲敲</span> 👍（11） 💬（1）<div>这门课太值了 哈哈哈 我以前学到的真的toy python</div>2019-05-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/38/d7/de6832df.jpg" width="30px"><span>Python高效编程</span> 👍（9） 💬（1）<div>第一问:
with open(&quot;in.txt&quot;, &quot;rt&quot;) as f:
    for line in f:
        Counter.update(line)</div>2019-05-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9b/9f/2cbc2a4f.jpg" width="30px"><span>人间乐园</span> 👍（4） 💬（1）<div>第一道，for.line in fin读取单行，使用result = yied line进行双向传递，直接把line给计数器，先判断line结尾处，如果是单词或者半个单词，则返回result给生成器，拼接到下一个line前，如果是None则不拼接，继续生成这个line。</div>2019-05-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/44/a4/7a45d979.jpg" width="30px"><span>IT蜗壳-Tango</span> 👍（4） 💬（1）<div>第七天打卡。</div>2019-05-22</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKCNH9kd9GibX3vibX9osjtWBvP5ibe8iciacMREk4bcDEgfrDQ9EKs8bQlHoVVhW9CXO8WHM5Ag26S9cA/132" width="30px"><span>mykgzy</span> 👍（3） 💬（1）<div>看着有点费力，但感觉超值，看到了好多python 书都没提到的生产网中涉及的知识。</div>2019-05-22</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83epc3c8hB9Lg0I1NibzH6h9qjur8XvG9Tto0NRp1Q0udCgmS7C7vUb4z5bnXMqy91GB76iaYP0icPiaqgg/132" width="30px"><span>edward0079</span> 👍（2） 💬（1）<div>判断是否为None的情况

if not x

if x is None

if not x is None

 

if x is not None`是最好的写法，清晰，不会出现错误，以后坚持使用这种写法。

使用if not x这种写法的前提是：必须清楚x等于None,  False, 空字符串&quot;&quot;, 0, 空列表[], 空字典{}, 空元组()时对你的判断没有影响才行</div>2020-02-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/5b/53/200fda62.jpg" width="30px"><span>vivien_zh</span> 👍（2） 💬（1）<div>努力跟上老师的进度。</div>2019-05-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/09/13/d762ce74.jpg" width="30px"><span>🌻</span> 👍（1） 💬（1）<div>第一问：

import re
from collections import defaultdict
from pathlib import Path


def parse(text, count):
    words = re.split(r&#39;\W&#39;, text.lower())

    for word in words:
        count[word] += 1
    return count

count = defaultdict(int)
with open(&#39;in.txt&#39;, &#39;r&#39;) as f:
    for line in f.readlines():
        count = parse(line, count)
        
# 排序
count.pop(&#39;&#39;)
sort_by_value = sorted(count.items(), key=lambda x: x[1] * -1)


Path(&#39;out.txt&#39;).touch()

with open(&#39;out.txt&#39;, &#39;w&#39;) as f:
    for word, count in sort_by_value:
        f.writelines(&#39;{}: {}\n&#39;.format(word, count))</div>2020-04-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/46/c0/01292b08.jpg" width="30px"><span>GentleCP</span> 👍（1） 💬（1）<div>老师github链接还没放出吗</div>2019-05-23</li><br/><li><img src="" width="30px"><span>Geek_Stone</span> 👍（1） 💬（1）<div>差不多10年了，还是个初学者。希望尽快摆脱初学者状态。</div>2019-05-22</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/3hZfficKPGCq2kjFBu9SgaMjibJTEl7iaW1ta6pZNyiaWP8XEsNpunlnsiaOtBpWTXfT5BvRP3qNByml6p9rtBvqewg/132" width="30px"><span>夜路破晓</span> 👍（1） 💬（1）<div>这节有点意思了，渐入佳境，值得细读。</div>2019-05-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/46/c0/01292b08.jpg" width="30px"><span>GentleCP</span> 👍（1） 💬（1）<div>老师，github的链接是多少呀</div>2019-05-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/43/2d/af86d73f.jpg" width="30px"><span>enjoylearning</span> 👍（1） 💬（1）<div>为什么字典 **dict_varname 就能平铺解析，是formate的作用吗</div>2019-05-22</li><br/><li><img src="" width="30px"><span>Geek_7d0f6b</span> 👍（0） 💬（1）<div>import re
import time

#定义一个全局变量word_cnt
word_cnt = {}

def parse(text):
    text = re.sub(r&#39;[^\w]&#39;, &#39; &#39;, text) #去除标点和换行符
    text = text.lower()
    word_list = text.split(&#39; &#39;)
    word_list = filter(None, word_list)

    #生成词频字典
    global word_cnt
    for word in word_list:
        if word not in word_cnt:
            word_cnt[word] = 0
        word_cnt[word] += 1

start_time = time.perf_counter()
with open(&#39;in.txt&#39;, &#39;r&#39;, encoding=&#39;UTF-8&#39;) as full:
    text = full.readline()
    while text:
        parse(text)
        text = full.readline()

sorted_word_cnt = sorted(word_cnt.items(), key=lambda kv: kv[1], reverse=True) #按照词频排序
with open(&#39;out.txt&#39;, &#39;w&#39;) as out:
    for word, freq in sorted_word_cnt:
        out.write(&#39;{} {}\n&#39;.format(word, freq))
end_time = time.perf_counter()
print(end_time - start_time)
定义全局变量，稍微修改了一下parse函数，处理小说《飘》总共花费0.25秒</div>2020-06-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/b4/94/2796de72.jpg" width="30px"><span>追风筝的人</span> 👍（0） 💬（1）<div>老师    最后一行print(welcome_str.format(**welcome_dic))输出  为什么要加上2个*呢？

name = input(&#39;your name:&#39;)
gender = input(&#39;you are a boy?(y&#47;n)&#39;)

###### 输入 ######
your name:Jack
you are a boy?

welcome_str = &#39;Welcome to the matrix {prefix} {name}.&#39;
welcome_dic = {
    &#39;prefix&#39;: &#39;Mr.&#39; if gender == &#39;y&#39; else &#39;Mrs&#39;,
    &#39;name&#39;: name
}

print(&#39;authorizing...&#39;)
print(welcome_str.format(**welcome_dic))

########## 输出 ##########
authorizing...
Welcome to the matrix Mr. Jack.</div>2019-10-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/51/86/b5fd8dd8.jpg" width="30px"><span>建强</span> 👍（0） 💬（1）<div>思考题2的server.py源程序如下：
import json
import time

&#39;&#39;&#39;
SERVER端处理流程：
1.读取config.json文件
2.判断状态，若status=1,表示文件已经上传，需要等待下载，仍然回到第1步
3.若status=0,表示可上传文件到网盘，则读取要上传的源文件，大小不超过5G，并写入网盘文件
4.判断断源文件是否已经读完，若未读完，修改status=1，写回config.json，仍然回到第1步
5.否则，修改status=2，写回config.json,Server端程序结束。
&#39;&#39;&#39;
def getFileStatus():

    #因第一次写Python，不知道怎么获取网盘文件，暂时用本地文件代替
    with open(&#39;F:\\temp\\config.json&#39;, &#39;r&#39;) as jsonfin:
        filestatus = json.load(jsonfin)

    return filestatus

def setFileStatus(filestatus):

    #因第一次写Python，不知道怎么获取网盘文件，暂时用本地文件代替
    with open(&#39;F:\\temp\\config.json&#39;, &#39;w&#39;) as jsonfout:
        json.dump(filestatus,jsonfout)

    return

#参数filename：要上传的文件名
#参数filesize：要上传的文件大小,默认为10M大小
def upLoadFile(filename,filesize=10485760):

    #从上传文件中读取文件内容
    with open(filename, &#39;rb&#39;) as fin:

        uploadtimes = 0

        while(True):
            
            #读取文件状态，判断是否可上传
            filestatus = getFileStatus()
            netfile = filestatus[&#39;filename&#39;]
            status = filestatus[&#39;status&#39;]

            #print(&quot;server: status=&quot;,status)

            if status == 2: #文件上传已经结束，则退出
                break

            if status == 1: #文件已经上传，等待下载后才能继续上传
                #为避免和客户端产生冲突，延迟1秒，再读状态
                time.sleep(1)
                continue
            
            filevalue = fin.read(filesize)

            if not filevalue:
                filestatus[&#39;filesize&#39;] = 0
                filestatus[&#39;status&#39;] = 2
                print(&quot;文件上传结束&quot;)
            else:
                #把读取的内容写入网盘文件，并设置状态
                with open(netfile, &#39;wb&#39;) as fout:
                    fout.write(filevalue)
                filestatus[&#39;filesize&#39;] = filesize
                filestatus[&#39;status&#39;] = 1

                uploadtimes += 1
                print(&quot;Server: 第&quot;,uploadtimes,&quot;次上传&quot;)

            #把文件状态写回config.json
            setFileStatus(filestatus)

    return

upLoadFile(&#39;F:\\temp\\move\\move.rar&#39;)
</div>2019-06-08</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLX6H7yN2PnwkCYlAV83jIh5P5cBUHnq4hqkib5RSktgqpMJBiaccGsZUzcagWLiaVG1ve3cqanicwPxg/132" width="30px"><span>Geek_16b077</span> 👍（0） 💬（1）<div>第一题，按每次读取CHUNK_SIZE=100，可能会有问题，比如  ：  ......I have a dream ...     ，如果have后面的空格刚好是第100个字符，那么此时产生的 last_word 为 have ，在与下一轮取得100个字符结合，得到 havea dream.......    出现&quot;havea&quot; 这一不合理得单词</div>2019-05-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/21/c0/38816c31.jpg" width="30px"><span>春之绿野</span> 👍（0） 💬（1）<div>老师，我看你的示例代码中也没有错误处理啊？</div>2019-05-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/58/94/c8bc2b59.jpg" width="30px"><span>yshan</span> 👍（0） 💬（1）<div>继续打开，继续学习</div>2019-05-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/96/7d/c7e8cd34.jpg" width="30px"><span>干布球</span> 👍（0） 💬（1）<div>老师的github地址是哪个呢？</div>2019-05-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/86/71/52017f48.jpg" width="30px"><span>林泽楷</span> 👍（0） 💬（1）<div>如果是汉字，怎么提取词组，或者人名，或者专有名词什么的，大概思路怎样的？哪位神有想法</div>2019-05-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/09/42/1f762b72.jpg" width="30px"><span>Hurt</span> 👍（0） 💬（1）<div>github地址是多少啊</div>2019-05-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a1/d6/9d99e5ef.jpg" width="30px"><span>不见飞刀</span> 👍（0） 💬（1）<div>我觉得一行一行读不太好
因为换行是会把单词分割的 
我觉得应该是按字数读  
然后spilt分割单词之间的空格 生成一个list
然后去掉list的最后一项  记住这一项的长度
用counter统计list
然后下一次就从上次去掉的最后一项那个位置开始按字数读取</div>2019-05-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fe/44/3e3040ac.jpg" width="30px"><span>程序员人生</span> 👍（0） 💬（1）<div>第一题，初步思路是，给read函数设定一个size，表示读取最大长度。（老师文中已提到）等一下写段代码试试
第二题，似乎要涉及到线程方面的内容......</div>2019-05-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/44/06/4372fd00.jpg" width="30px"><span>Geek_212b85</span> 👍（0） 💬（1）<div>打卡，初学者</div>2019-05-22</li><br/>
</ul>