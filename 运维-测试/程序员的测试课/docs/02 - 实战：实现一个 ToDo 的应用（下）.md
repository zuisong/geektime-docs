你好，我是郑晔！

在上一讲里，我们实现了一个 ToDo 应用的核心业务部分。虽然测试都通过了，但我相信你可能还是会有一种不真实的感觉，因为它还不是一个完整的应用，既不能有命令行的输入，也不能把 Todo 项的内容真正地存储起来。

这一讲，我们就继续实现这个 ToDo 应用，把欠缺的部分都补上。不过，在开始今天的内容之前，我仍需要强调一下，之所以我要先做核心业务部分，因为它在一个系统中是最重要的。很多人写代码的时候会急着把各个部分连接起来，但却忽视了核心业务部分的构建，这样做造成的结果就是严重的耦合，这也是很多后续问题产生的根源。

在上一讲里，我们已经有了一个业务内核，现在还欠缺输入输出的部分，也就是如何将Todo 项保存起来，以及如何接受命令行参数。

接下来，我们就分别来实现这两个部分。

## 文件存储

我们先来实现 Todo 项的存储。在上一讲中，我们已经预留好了存储的接口，也就是 Repository 这个接口。现在，我们只需要给这个接口提供一个相应的实现就好了。我们先来看看 Repository 接口现在是什么样子。

```
public interface TodoItemRepository {
    TodoItem save(TodoItem item);
    Iterable<TodoItem> findAll();
}
```

出于简单的考虑，我们要实现一个基于文件的存储。也就是说，给这个接口提供一个基于文件的实现版本。
<div><strong>精选留言（19）</strong></div><ul>
<li><img src="" width="30px"><span>Geek_3b1096</span> 👍（4） 💬（1）<div>学习了封装其它程序库 ，谢谢老师</div>2021-08-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/65/21/101a7075.jpg" width="30px"><span>davix</span> 👍（3） 💬（1）<div>老師可否後面詳細講講測試金字塔各層case的設計？哪些放入哪層？
我發現team中有傾向，如果有了集成測試，甚至端到端測試，很多人就願意在集成測試裡寫，不寫單元了，認為反正單元被測到了，而且覆蓋的更多。
在本節cli例子中沒有用單元，還覆蓋了那麼多case，我擔心有人就會覺得之前單元測試可以省掉。</div>2021-08-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/6a/66/da6024e4.jpg" width="30px"><span>إ并向你招手إ祥子</span> 👍（3） 💬（1）<div>老师好，对于lombk注解生成的代码在测试覆盖不到的时候是如何处理的呢？    

在业务开发中，有很多VO,DTO之类的实体类对象，这类一部分对象内部可能会有一部分的行为方法，比如转换为别的对象，通常为了简化代码，会使用lombok注解，在单元测试覆盖率的统计中，lombok生成的代码可能是测不到的，同时由于这些对象可能是有除了get  set之外的行为的，因此也不能简单的屏蔽在测试覆盖率的检查之外，目前在团队内的做法是让大家补上未覆盖部分的测试，有没有更好的建议呢？</div>2021-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ac/87/8ed5880a.jpg" width="30px"><span>大碗</span> 👍（2） 💬（1）<div>请问老师，样例代码中数据库的测试是使用了一个todo_test的实际mysql数据库是怎么考虑的，不选择用H2是什么考虑呢？
用mysql优点是测试更接近最终的运行环境，也能测试创表语句，缺点：稍微依赖了本地的环境，第一次需要创建数据库表，建账号。用H2的优缺点就反过来。两者在影响测试速度上似乎目前看不出差距</div>2021-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/48/e4/6feec30f.jpg" width="30px"><span>X</span> 👍（2） 💬（1）<div>老师，你好，我想问下 Springboot 开发，在进行 集成测试的时候，有redis 依赖，是怎么进行测试的呢？
尝试过，embedded-redis 这些内嵌数据库，但是这些用起来不太理想，而且年久失修，有很多bug。
想问问老师这方面是怎么处理的。</div>2021-08-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/ff/77/70e567d2.jpg" width="30px"><span>程九森</span> 👍（1） 💬（1）<div>请问参看代码在哪? </div>2021-08-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8c/95/4544d905.jpg" width="30px"><span>sylan215</span> 👍（1） 💬（1）<div>这一节的收获：
1、测试环境（数据）准备，是测试中非常重要的一环。

2、从黑盒测试的角度来说，异常测试用例的比率要远大于正常用例的，那么白盒角度也是一样。

3、对于异常类型的覆盖，也需要根据代码实现来选取，比如 catch 所有异常的话，一条异常用例就可以覆盖了，而如果 catch 的是某一个具体用例的话，一定要记得再触发一个没有 catch 的异常哈。

4、要把可测性，作为程序设计的基本要求。

5、测试数据准备，是一个很关键，也很常见的内容，除了mock，一些必须的数据准备还是要做的，所以要自动化，也需要提供数据自动准备的实现，同时在完成后要进行数据清理。</div>2021-08-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/c7/1c/e59a699b.jpg" width="30px"><span>海朋森</span> 👍（1） 💬（1）<div>老师，你说的覆盖率是通过jacoco来获取的吗？
这个专栏是给开发看的还是qa也可以呢？</div>2021-08-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/54/16/1df5d5ed.jpg" width="30px"><span>Insist</span> 👍（1） 💬（1）<div>是否有maven版本的代码？</div>2021-08-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/4b/66/bac3697b.jpg" width="30px"><span>lamb</span> 👍（0） 💬（1）<div> 《代码之丑》讲尽可能不要使用静态方法，上来就封装一层静态方法 ？？？</div>2022-05-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/57/2a/cb7e3c20.jpg" width="30px"><span>Nio</span> 👍（12） 💬（2）<div>老师，感觉代码实现只用Java比较难全部理解，能增加其他语言比如Python或者golang语言的实现吗，这样会更完善一点，对其他语言编程的同学也更友好些。</div>2021-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1c/cd/8d552516.jpg" width="30px"><span>Gojustforfun</span> 👍（7） 💬（0）<div>控制台输出如何测试？在内存中构造一个与std.out拥有相同接口的buffer对象（标准库一般都有现成的），这样所本该输出的内容都写在buffer中，再对buffer中的内容进行断言。</div>2021-08-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/51/8d/c5e93d59.jpg" width="30px"><span>李勇</span> 👍（1） 💬（0）<div>确实是一个比较直观的感受；</div>2022-11-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/67/6e/ec7299ec.jpg" width="30px"><span>达芬奇</span> 👍（0） 💬（0）<div>这一篇的内容感觉很多</div>2023-11-30</li><br/><li><img src="" width="30px"><span>你好，Java</span> 👍（0） 💬（1）<div>請問你這段到底在寫什麼? 沒人看得懂阿

为了保证组装过程的一致，我们可以把组装过程单独拿出来，让最终的代码和测试代码复用同样的逻辑。
public class ObjectFactory { public CommandLine createCommandLine(final File repositoryFile) { return new CommandLine(createTodoCommand(repositoryFile)); } private TodoCommand createTodoCommand(final File repositoryFile) { final TodoItemService service = createService(repositoryFile); return new TodoCommand(service); } public TodoItemService createService(final File repositoryFile) { final TodoItemRepository repository = new FileTodoItemRepository(repositoryFile); return new TodoItemService(repository); }}</div>2023-05-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/6b/b9/9b0630b1.jpg" width="30px"><span>Geek_9c3134</span> 👍（0） 💬（0）<div>老师 我有个疑问  为了方便测试 而去修改代码   会不会对正常的代码 带来不好的影响 副作用  比如 为了方便测试容易  调用的接口修改了的不合理了</div>2022-11-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>隔离变化，逐步编写稳定的代码--记下来</div>2022-06-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/24/5d/65e61dcb.jpg" width="30px"><span>学无涯</span> 👍（0） 💬（0）<div>像RedisTemplate这种的类库，有必要封装到一个单独的类中吗</div>2022-01-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1d/de/62bfa83f.jpg" width="30px"><span>aoe</span> 👍（0） 💬（0）<div>万能的中间层，封装异常还可以这样用！</div>2021-11-07</li><br/>
</ul>