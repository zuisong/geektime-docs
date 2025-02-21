你好，我是陈航。

在上一篇文章中，我带你一起学习了Dart中异步与并发的机制及实现原理。与其他语言类似，Dart的异步是通过事件循环与队列实现的，我们可以使用Future来封装异步任务。而另一方面，尽管Dart是基于单线程模型的，但也提供了Isolate这样的“多线程”能力，这使得我们可以充分利用系统资源，在并发Isolate中搞定CPU密集型的任务，并通过消息机制通知主Isolate运行结果。

异步与并发的一个典型应用场景，就是网络编程。一个好的移动应用，不仅需要有良好的界面和易用的交互体验，也需要具备和外界进行信息交互的能力。而通过网络，信息隔离的客户端与服务端间可以建立一个双向的通信通道，从而实现资源访问、接口数据请求和提交、上传下载文件等操作。

为了便于我们快速实现基于网络通道的信息交换实时更新App数据，Flutter也提供了一系列的网络编程类库和工具。因此在今天的分享中，我会通过一些小例子与你讲述在Flutter应用中，如何实现与服务端的数据交互，以及如何将交互响应的数据格式化。

## Http网络编程

我们在通过网络与服务端数据交互时，不可避免地需要用到三个概念：定位、传输与应用。

其中，**定位**，定义了如何准确地找到网络上的一台或者多台主机（即IP地址）；**传输**，则主要负责在找到主机后如何高效且可靠地进行数据通信（即TCP、UDP协议）；而**应用**，则负责识别双方通信的内容（即HTTP协议）。
<div><strong>精选留言（27）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/04/37/aa04f997.jpg" width="30px"><span>和小胖</span> 👍（19） 💬（2）<div>第一个问题解决方法：
dio.interceptors.add(InterceptorsWrapper(
      onRequest: (Options options) async {
        if (options.headers[&#39;token&#39;] == null) {
          print(&quot;no token，request token firstly...&quot;);
          &#47;&#47;lock the dio.
          dio.lock();
          return new Dio().get(&quot;http:&#47;&#47;xxxx.com&#47;token&quot;).then((d) {
            options.headers[&quot;token&quot;] = d.data[&#39;token&#39;];
            print(&quot;request token succeed, value: &quot; + d.data[&#39;token&#39;]);
            print(
                &#39;continue to perform request：path:${options.path}，baseURL:${options.path}&#39;);
            return options;
          }).whenComplete(() =&gt; dio.unlock()); &#47;&#47; unlock the dio
        }
        return options;
      }
  ));</div>2019-10-09</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83epxMjZcn8LFy6PIT7uGzUOHTCZosTwh39jBKlyW3Ffzyscm14PQGh3QZ1GrEGF4UWxwKZrAib8AXCA/132" width="30px"><span>江宁彭于晏</span> 👍（15） 💬（1）<div>分享一个json转dart类的工具，理解了原理后，实际项目中可以省不少时间https:&#47;&#47;javiercbk.github.io&#47;json_to_dart&#47;</div>2019-09-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/04/37/aa04f997.jpg" width="30px"><span>和小胖</span> 👍（6） 💬（2）<div>第二道题解决方法：

class Student {
  String id;
  String name;
  int score;
  List&lt;Teacher&gt; teachers;

  Student({this.id, this.name, this.score, this.teachers});

  factory Student.fromJson(Map&lt;String, dynamic&gt; parsedJson) {
    return Student(
        id: parsedJson[&#39;id&#39;],
        name: parsedJson[&#39;name&#39;],
        score: parsedJson[&#39;score&#39;],
        teachers: getTeacher(parsedJson[&#39;teachers&#39;]));
  }

  static List&lt;Teacher&gt; getTeacher(dynamic list) {
    List&lt;Teacher&gt; teachers = new List();
    list.forEach((f) {
      teachers.add(Teacher.fromJson(f));
    });
    return teachers;
  }
}

class Teacher {
  String name;
  int age;

  Teacher({this.age, this.name});

  factory Teacher.fromJson(Map&lt;String, dynamic&gt; parsedJson) {
    return Teacher(name: parsedJson[&#39;name&#39;], age: parsedJson[&#39;age&#39;]);
  }
}</div>2019-10-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/4f/c1/7f596aba.jpg" width="30px"><span>给我点阳光就灿烂</span> 👍（4） 💬（2）<div>如何进行socket通信</div>2019-08-22</li><br/><li><img src="" width="30px"><span>Geek_0793f1</span> 👍（2） 💬（2）<div>使用这种方式，我们需要先将 JSON 字符串传递给 JSON.decode 方法解析成一个 Map，然后把这个 Map 传给自定义的类，进行相关属性的赋值。

前端一般把json字符串解析成map之后，就直接用这个map进行相关的属性赋值了，老师能解释一下，传给自定义类的做法的好处吗？</div>2019-09-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/12/3c/2e7fd24f.jpg" width="30px"><span>Geek_0d3a08</span> 👍（1） 💬（1）<div>重定向监听有吗？</div>2019-08-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/31/5e/d7cdc1d6.jpg" width="30px"><span>江厚宏</span> 👍（1） 💬（1）<div>老师能不能介绍一下反序列化工具，比如json_serializable和 built_value，建议用哪一个，如果遇到泛型，该如何处理</div>2019-08-22</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTI1KQOU2VruV0ibibrTUIicHpXiaGHlvMkzZ1jPCSb9TLKcibb4YbJbyGtlec7pjbt8fdicxtQTic5bDwibCA/132" width="30px"><span>Geek_4s70e3</span> 👍（0） 💬（1）<div>json_model 怎么生成纯数组的解析代码？</div>2019-11-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/3c/88/6bef27d6.jpg" width="30px"><span>大神博士</span> 👍（0） 💬（2）<div>想问下 Flutter 中 JSONP 的请求怎么处理</div>2019-09-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/f2/1e/679789f7.jpg" width="30px"><span>米米呀👧</span> 👍（0） 💬（1）<div>import &#39;dart:convert&#39;;

import &#39;package:flutter&#47;material.dart&#39;;
import &#39;package:http&#47;http.dart&#39; as http;
[...]
  loadData() async {
    String dataURL = &quot;https:&#47;&#47;jsonplaceholder.typicode.com&#47;posts&quot;;
    http.Response response = await http.get(dataURL);
    setState(() {
      widgets = JSON.decode(response.body);
    });
  }
}

官网Demo里面是用的这个，跟HttpClient有什么区别？我该用哪个？</div>2019-09-10</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLFbNiaADSSo6SQhsoDRX95ey8zngVaj2fHqaVc6JAd1uXJFAle1sl4SaicicpSzcKwa4JjLvkpKItZQ/132" width="30px"><span>Geek_joestar</span> 👍（0） 💬（1）<div>static List&lt;Teacher&gt; fromJsonList(List&lt;dynamic&gt; listJson){
    var list = List&lt;Teacher&gt;();
    for(Map&lt;String, dynamic&gt; parsedJson in listJson) {
      list.add(Teacher.fromJson(parsedJson));
    }
    return list;
  }</div>2019-09-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/67/d1/1c69ad22.jpg" width="30px"><span>C</span> 👍（0） 💬（1）<div>class Teacher {
  String name;
  int age;

  Teacher({this.name, this.age});

  factory Teacher.fromJson(Map&lt;String, dynamic&gt; parsedJson) {
    return Teacher(
      name: parsedJson[&#39;name&#39;],
      age: parsedJson[&#39;age&#39;],
    );
  }

  static List&lt;Teacher&gt; parseTeachers(List&lt;dynamic&gt; mapList) {
    List&lt;Teacher&gt; teachers = List&lt;Teacher&gt;();
    for(Map&lt;String, dynamic&gt; map in mapList) {
      teachers.add(Teacher.fromJson(map));
    }
    return teachers;
  }
}

class Student {
  String id;
  String name;
  int score;
  List&lt;Teacher&gt; teachers;

  Student({this.id, this.name, this.score, this.teachers});

  factory Student.fromJson(Map&lt;String, dynamic&gt; parsedJson) {
    return Student(
      id: parsedJson[&#39;id&#39;],
      name: parsedJson[&#39;name&#39;],
      score: parsedJson[&#39;score&#39;],
      teachers: Teacher.parseTeachers(parsedJson[&#39;teachers&#39;]),
    );
  }
}</div>2019-09-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8b/c3/bf56f46c.jpg" width="30px"><span>大和</span> 👍（0） 💬（1）<div>dio.interceptors.add(InterceptorsWrapper(
        onRequest: (RequestOptions options) async {
          if (options.headers[&quot;token&quot;] == null) {
            try {
              var token = await new Dio().get(&quot;https:&#47;&#47;xxx.com&#47;token&quot;);
              options.headers[&quot;token&quot;] = token;
            }catch(e) {
              return dio.reject(&quot;Error: 请先登录...&quot;);
            }
          }
          return options;
        }
    ));</div>2019-09-04</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/oawDPl6RMSNz5Br5hLUBZzdicRPshXVJyTe2runPeBiby76BqRa8ibs99xxZ7EcBnkLeRPvt4gSGfqEibz1bpzWuoA/132" width="30px"><span>宁缺</span> 👍（0） 💬（1）<div>请问老大，课后作业的答案啥时候给参考一下</div>2019-09-03</li><br/><li><img src="" width="30px"><span>秋</span> 👍（0） 💬（1）<div>使用Dio发送post请求，data数据是map，但是服务端接收不到，请问老师这是什么原因？</div>2019-09-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/4b/71/591ae170.jpg" width="30px"><span>大恒</span> 👍（0） 💬（1）<div>请问json如何解析泛型？</div>2019-08-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5e/bd/e28f8ce5.jpg" width="30px"><span>ls</span> 👍（0） 💬（1）<div>还是不大理解 await 和 async，当发起网络请求的时候，不会阻塞主线程吗。当调用 async 的函数时，是另外起了一个线程去等待网络请求返回？这个异步怎么理解好。</div>2019-08-24</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqr5ibqxYwcSgqPA7s49MZb1vEKKXT4mPTojwiclXkJf3ug26NuzTa6A5gbicR2rAUHdEkUAn13Rr2KQ/132" width="30px"><span>吴小安</span> 👍（0） 💬（1）<div>这个反射引起的安全问题在移动端和前端现在有解决？</div>2019-08-23</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIR6WDJVpJ103eeu54rLia1uhJO8sWUW1QJRZQqDCbgfSsSBYFWZFB7EleVmSUvZfhEbx6eLkzRhNA/132" width="30px"><span>右手边</span> 👍（0） 💬（2）<div>老师您好，JSON 的解析确实有点复杂了，真的没有类似Gson那样方便的库么？</div>2019-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5a/75/4e0d7419.jpg" width="30px"><span>飓风</span> 👍（2） 💬（0）<div>https:&#47;&#47;github.com&#47;trevorwang&#47;retrofit.dart&#47;  
这个库配合dio，网络请求转换这一步我觉得更简单点？</div>2020-07-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/47/8a/13d4cb82.jpg" width="30px"><span>感恩的心</span> 👍（0） 💬（0）<div>class Student {
  String? id;
  String? name;
  int? score;
  List&lt;Teachers&gt;? teachers;

  Student({this.id, this.name, this.score, this.teachers});

  Student.fromJson(Map&lt;String, dynamic&gt; json) {
    id = json[&#39;id&#39;];
    name = json[&#39;name&#39;];
    score = json[&#39;score&#39;];
    if (json[&#39;teachers&#39;] != null) {
      teachers = &lt;Teachers&gt;[];
      json[&#39;teachers&#39;].forEach((v) {
        teachers!.add(new Teachers.fromJson(v));
      });
    }
  }

  Map&lt;String, dynamic&gt; toJson() {
    final Map&lt;String, dynamic&gt; data = new Map&lt;String, dynamic&gt;();
    data[&#39;id&#39;] = this.id;
    data[&#39;name&#39;] = this.name;
    data[&#39;score&#39;] = this.score;
    if (this.teachers != null) {
      data[&#39;teachers&#39;] = this.teachers!.map((v) =&gt; v.toJson()).toList();
    }
    return data;
  }
}

class Teachers {
  String? name;
  int? age;

  Teachers({this.name, this.age});

  Teachers.fromJson(Map&lt;String, dynamic&gt; json) {
    name = json[&#39;name&#39;];
    age = json[&#39;age&#39;];
  }

  Map&lt;String, dynamic&gt; toJson() {
    final Map&lt;String, dynamic&gt; data = new Map&lt;String, dynamic&gt;();
    data[&#39;name&#39;] = this.name;
    data[&#39;age&#39;] = this.age;
    return data;
  }
}</div>2024-03-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/d6/7d/4b09b0bf.jpg" width="30px"><span>李鑫鑫</span> 👍（0） 💬（0）<div>带有泛型 的bean 这么转json????</div>2022-02-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/2a/7e/6d2e703b.jpg" width="30px"><span>小何</span> 👍（0） 💬（0）<div>老师好，问一个问题，flutter怎么做回调啊，我想封装一个工具类，网络请求的时候传入callback，然后成功就调用callback.onSuccess(t),失败就调用callback.onFailed(t)</div>2021-07-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/2a/7e/6d2e703b.jpg" width="30px"><span>小何</span> 👍（0） 💬（1）<div>老师好，compute和Future区别是什么啊， 不是用Future也可以实现异步嘛</div>2021-07-21</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIFgmmBXRltzZDa6lvibrCouDvOQYkfT2tJibZ97tJvNhGdfibntJdwmQ4BSzqr4bRB4m2SFxyAHBPsQ/132" width="30px"><span>任逍遥</span> 👍（0） 💬（0）<div>最近遇到一个问题，问一下老师服务器更新SSL证书时使用了pem格式，发现安卓端请求失败，iOS端正常，flutter应该如何兼容pem证书呢</div>2021-07-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/65/e8/d1e52dbb.jpg" width="30px"><span>IF-Processing</span> 👍（0） 💬（0）<div>请问，flutter对于网络服务（比如Samba，NFS共享）的访问有支持吗？</div>2020-02-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（0） 💬（0）<div>习惯了用js直接获取属性，这样先定义模型确实会更废时间一些，但先定义模型其实会更规范、出bug更容易调试，也要求开发人员不能随便变更数据结构。</div>2019-08-22</li><br/>
</ul>