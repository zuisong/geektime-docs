你好，我是郭屹。今天我们继续手写MiniTomcat。

在前面的学习结束之后，我们引入了池化技术，还实现Processor的异步化。前者复用对象，减少构造新对象的时间开销；后者使Connector能同时服务于多个Processor。这些都是提升性能和吞吐量的常用技术手段。

这节课我们继续研究Servlet规范，对我们现有的代码进行改造，使之适配这个规范。同时我们还要解析HTTP协议中的请求信息，并把它存储到服务器内存之中。

下面就让我们一起来动手实现。

## 项目结构

这节课因为需要进行Servlet规范适配工作，还要解析头部信息，因此会新增几个类，整体结构如下：

```plain
MiniTomcat
├─ src
│  ├─ main
│  │  ├─ java
│  │  │  ├─ server
│  │  │  │  ├─ DefaultHeaders.java
│  │  │  │  ├─ HttpConnector.java
│  │  │  │  ├─ HttpHeader.java
│  │  │  │  ├─ HttpProcessor.java
│  │  │  │  ├─ HttpRequest.java
│  │  │  │  ├─ HttpRequestLine.java
│  │  │  │  ├─ HttpResponse.java
│  │  │  │  ├─ HttpServer.java
│  │  │  │  ├─ Request.java
│  │  │  │  ├─ Response.java
│  │  │  │  ├─ ServletProcessor.java
│  │  │  │  ├─ SocketInputStream.java
│  │  │  │  ├─ StatisResourceProcessor.java
│  │  ├─ resources
│  ├─ test
│  │  ├─ java
│  │  │  ├─ test
│  │  │  │  ├─ HelloServlet.java
│  │  ├─ resources
├─ webroot
│  ├─ test
│  │  ├─ HelloServlet.class
│  ├─ hello.txt
├─ pom.xml
```
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/16/0b/5a/453ad411.jpg" width="30px"><span>C.</span> 👍（4） 💬（3）<div>buf[pos++]：表示buf的pos索引加一，以便后续read操作，是个后缀递增的操作。
&amp; 0xff：位操作，字节在Java的中的范围为-128到127，是个有符号数，执行&amp; 0xff是在做一个按位与操作，转换为一个无符号数，返回的值在0-255。0xff等于十进制的255，二进制位11111111。buf[pos]字节会与11111111进行按位与操作，基本保持了原始字节的值不变。</div>2023-12-20</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTL212ET0q3e8U5xXuYe7LCBlrpdBFkrgedibfdao2fMUKnCWwxm2I05RB7EyDcgeL0g60ib88cn2dmQ/132" width="30px"><span>Clark Chen</span> 👍（1） 💬（1）<div>老师好， 关于`SocketInputStream .readRequestLine(HttpRequestLine requestLine)`   方法的这段代码
```   
   while (!space) {
            if (pos &gt;= count) {
                int val = read();
                if (val == -1) {
                    throw new IOException(&quot;requestStream.readline.error&quot;);
                }
                pos = 0;
                readStart = 0;
            }
            if (buf[pos] == SP) {
                space = true;
            }
            requestLine.method[readCount] = (char) buf[pos];
            readCount++;
            pos++;
        }
```
有些地方没想明白， 为什么要在这个方法里面对手动控制pos++，直接获取buf[]里面的值 ，而不是通过read 方法来获取值。如下面这样
```
        while (!space){
            if(pos &gt;= count ){
                readStart = 0;
            }
            int val = read();
            if(val == -1){
                throw new IOException(&quot;requestStream.readline.error&quot;);
            }
            if(val == SP){
                space =true;
            }
            requestLine.getMethod()[readCount] = (char)val;
            readCount++;
        }
```
是有效率上的原因吗？</div>2023-12-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（1）<div>请教老师两个问题：
Q1：parameters用来做什么？
HttpRequest类中定义了parameters，但好像并没有使用，这个类是用来存什么的？
Q2：parseHeaders函数用if区分有意义吗？
HttpRequest类中的parseHeaders用if … else来区分各个部分，但其实最后都是调用headers.put(name, value);
所有的分支，最后的处理结果都是一样的，这个区分还有意义吗？</div>2023-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/4c/6e/5435e214.jpg" width="30px"><span>HH🐷🐠</span> 👍（0） 💬（1）<div>😄感觉像是纠正什么数据</div>2023-12-20</li><br/>
</ul>