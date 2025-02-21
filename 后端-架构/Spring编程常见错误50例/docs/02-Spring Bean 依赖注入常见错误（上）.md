你好，我是傅健，这节课我们来聊聊 Spring @Autowired。

提及Spring的优势或特性，我们都会立马想起“**控制反转、依赖注入**”这八字真言。而@Autowired正是用来支持依赖注入的核心利器之一。表面上看，它仅仅是一个注解，在使用上不应该出错。但是，在实际使用中，我们仍然会出现各式各样的错误，而且都堪称经典。所以这节课我就带着你学习下这些经典错误及其背后的原因，以防患于未然。

## 案例1：过多赠予，无所适从

在使用@Autowired时，不管你是菜鸟级还是专家级的Spring使用者，都应该制造或者遭遇过类似的错误：

> required a single bean, but 2 were found

顾名思义，我们仅需要一个Bean，但实际却提供了2个（这里的“2”在实际错误中可能是其它大于1的任何数字）。

为了重现这个错误，我们可以先写一个案例来模拟下。假设我们在开发一个学籍管理系统案例，需要提供一个API根据学生的学号（ID）来移除学生，学生的信息维护肯定需要一个数据库来支撑，所以大体上可以实现如下：

```
@RestController
@Slf4j
@Validated
public class StudentController {
    @Autowired
    DataService dataService;

    @RequestMapping(path = "students/{id}", method = RequestMethod.DELETE)
    public void deleteStudent(@PathVariable("id") @Range(min = 1,max = 100) int id){
        dataService.deleteStudent(id);
    };
}
```

其中DataService是一个接口，其实现依托于Oracle，代码示意如下：

```
public interface DataService {
    void deleteStudent(int id);
}

@Repository
@Slf4j
public class OracleDataService implements DataService{
    @Override
    public void deleteStudent(int id) {
        log.info("delete student info maintained by oracle");
    }
}
```
<div><strong>精选留言（21）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1a/ab/5b/eb3983f0.jpg" width="30px"><span>liuchao90h</span> 👍（28） 💬（2）<div>要是变量中也能做到可以包含.号就可以了，或者源码中把包分隔符的.改成下划线来解决
对于例子中的com.spring.puzzle.class2.example3.StudentController.InnerClassDataService建议换成com.spring.puzzle.class2.example3.StudentController$InnerClassDataService更规范，否则对照源码截图是会误解的，本身也不是语法规范的写法，尽管意思明白的人都能明白过来</div>2021-04-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7b/98/8f1aecf4.jpg" width="30px"><span>楼下小黑哥</span> 👍（11） 💬（1）<div>好家伙，咋一看这个问题，感觉跟 @Qualifier 注解应该是一样的，应该可以使用字段名 tudentController.InnerClassDataService 这样的方式。
但是看起来还是有点别扭，于是复制到 IDEA 试了下，原来这样语法有问题，直接就会报错😂。
大意了~
赞同 @liuchao90h 说法，内部类实际取到名字应该为 com.xxxx. StudentController$InnerClassDataService
</div>2021-04-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/43/23/d98fb8f7.jpg" width="30px"><span>Niverkk</span> 👍（6） 💬（1）<div>内部类类名：com.spring.puzzle.class2.example3.StudentController.InnerClassDataService
应该是：com.spring.puzzle.class2.example3.StudentController$InnerClassDataService, &quot;.&quot;换成&quot;$&quot;</div>2021-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/4f/26/f21afb83.jpg" width="30px"><span>暖色浮余生</span> 👍（4） 💬（0）<div>其实可以通过重写BeanNameGenerator来自己实现bean名称的实现。看了下ComponentScanAnnotationParser的源码。发现在parse方法里面会获取注解 @ComponentScan的nameGenerator属性。获取到NameGenerator的Class。然后实例化设置到ClassPathBeanDefinitionScanner这个扫描类的 BeanNameGenerator属性上面。 这样的话@AutowiredDataService innerClassDataService；通过自定义的Bean名称生成器来注入就可以了</div>2021-05-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/25/54/ef2ca14f.jpg" width="30px"><span>KK</span> 👍（3） 💬（2）<div>为什么一定要看源码? 
源码不是一种契约, 是可能变化的, 而且学习成本高.  
学习Spring的官方文档更加好, 官方文档所阐述的特性, 可以认为是spring的开发者和使用者的契约, 是相对不容易变化的. </div>2022-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/51/9b/ccea47d9.jpg" width="30px"><span>安迪密恩</span> 👍（2） 💬（0）<div>傅哥你好，现在@Autowired注解被IDEA标记为Field injection is not recommended。为什么呢？能否请傅哥扩展下@Resource的相关知识点呢，谢谢。</div>2022-03-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ce/d7/074920d5.jpg" width="30px"><span>小飞同学</span> 👍（2） 💬（3）<div>问两个问题：
1.为啥@Validated注解必须放在类上，不然就校验不住了。 傅哥引入的是hibernate那个么？
2.我的印象中 @Autowired只能按照类型注入，这里有点颠覆认知  那么问题来了，@Resource和@Autowired区别到底是啥？</div>2021-04-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2d/51/89/539096e2.jpg" width="30px"><span>可乐</span> 👍（1） 💬（2）<div>问题：

public interface DataService {
    void deleteStudent(int id);
}

这个接口并没有注入bean，为什么可以用autowire去找这个bean呢？</div>2022-04-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/16/5b/83a35681.jpg" width="30px"><span>Monday</span> 👍（1） 💬（0）<div>1、@Priority(value=${number})看源码：值越小优先级越低,可以为负数,若存在两个候选直接抛异常.
2、思考题：不可以，命名方式不能通过</div>2021-06-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/6c/67/07bcc58f.jpg" width="30px"><span>虹炎</span> 👍（1） 💬（0）<div>不能做到，因为会报编译错误。studentController.InnerClassDataService;  这一句。</div>2021-05-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/16/5b/83a35681.jpg" width="30px"><span>Monday</span> 👍（1） 💬（1）<div>有2个问题
1、bean的依赖关系在实例化之前就应该知晓吧？然后安装顺序初始化
2、循环依赖怎么解决？
谢谢老师</div>2021-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/33/d7/739e2f6d.jpg" width="30px"><span>Utah</span> 👍（1） 💬（0）<div>这些问题之前经常遇到，解决方式就是百度，没有深入研究过原理，希望通过这次学习，以后遇到此类问题知其然知其所以然</div>2021-05-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/84/8f/a305cc1e.jpg" width="30px"><span>otakuhuang</span> 👍（0） 💬（0）<div>内部类的 Bean 名称包含了 . 符号，使用 @Qualifier 会因命名问题导致编译失败</div>2024-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/bf/3e/cdc36608.jpg" width="30px"><span>子夜枯灯</span> 👍（0） 💬（0）<div>思考题：不可以，命名方式不能通过</div>2022-01-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>思考题应该不能用方法1，变量名好像不能有点符号</div>2021-11-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/c4/ad/79b8a12c.jpg" width="30px"><span>一步</span> 👍（0） 💬（0）<div>搞懂Spring是如何找到bean，找bean的原则
搞懂Spring是如何管理内部类（bean化）
搞懂autowrie和qualiter的区别</div>2021-10-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/95/4b/9b50efe3.jpg" width="30px"><span>安眠</span> 👍（0） 💬（1）<div>请问案例一中所说“@Autowired 要求是必须注入的（即 required 保持默认值为 true），或者注解的属性类型并不是可以接受多个 Bean 的类型，例如数组、Map、集合。“如何理解呢？因为我试了一下可以注入一个集合，比如
@Autowired
 List&lt;DataService&gt; dataServices;

打印出来结果
[com.spring.puzzle.class2.example1.CassandraDataService@2a8fcfa5, com.spring.puzzle.class2.example1.OracleDataService@79330729]</div>2021-07-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/11/c8/889846a7.jpg" width="30px"><span>黑白颠倒</span> 👍（0） 💬（0）<div>案例三我觉得
@AutowiredDataService InnerClassDataService;就行</div>2021-06-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/47/65/cce8eb34.jpg" width="30px"><span>nimil</span> 👍（0） 💬（0）<div>这课程有意思，几个小问题，引出源码解析</div>2021-05-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/84/cb/f04d632a.jpg" width="30px"><span>gaohw</span> 👍（0） 💬（0）<div>继续努力 理解源码 拓宽视野</div>2021-05-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/37/2b/b32f1d66.jpg" width="30px"><span>Ball</span> 👍（0） 💬（2）<div>没想到一个简单的 bean name 的问题在源码里居然能找到这么精彩的答案！</div>2021-04-26</li><br/>
</ul>