你好，我是李玥。

在之前《[04 | 如何利用事务消息实现分布式事务？](https://time.geekbang.org/column/article/111269)》这节课中，我通过一个小例子来和大家讲解了如何来使用事务消息。在这节课的评论区，很多同学都提出来，非常想了解一下事务消息到底是怎么实现的。不仅要会使用，还要掌握实现原理，这种学习态度，一直是我们非常提倡的，这节课，我们就一起来学习一下，在RocketMQ和Kafka中，事务消息分别是如何来实现的？

## RocketMQ的事务是如何实现的？

首先我们来看RocketMQ的事务。我在之前的课程中，已经给大家讲解过RocketMQ事务的大致流程，这里我们再一起通过代码，重温一下这个流程。

```
public class CreateOrderService {

  @Inject
  private OrderDao orderDao; // 注入订单表的DAO
  @Inject
  private ExecutorService executorService; //注入一个ExecutorService

  private TransactionMQProducer producer;

  // 初始化transactionListener 和 producer
  @Init
  public void init() throws MQClientException {
    TransactionListener transactionListener = createTransactionListener();
    producer = new TransactionMQProducer("myGroup");
    producer.setExecutorService(executorService);
    producer.setTransactionListener(transactionListener);
    producer.start();
  }

  // 创建订单服务的请求入口
  @PUT
  @RequestMapping(...)
  public boolean createOrder(@RequestBody CreateOrderRequest request) {
    // 根据创建订单请求创建一条消息
    Message msg = createMessage(request);
    // 发送事务消息
    SendResult sendResult = producer.sendMessageInTransaction(msg, request);
    // 返回：事务是否成功
    return sendResult.getSendStatus() == SendStatus.SEND_OK;
  }

  private TransactionListener createTransactionListener() {
    return new TransactionListener() {
      @Override
      public LocalTransactionState executeLocalTransaction(Message msg, Object arg) {
        CreateOrderRequest request = (CreateOrderRequest ) arg;
        try {
          // 执行本地事务创建订单
          orderDao.createOrderInDB(request);
          // 如果没抛异常说明执行成功，提交事务消息
          return LocalTransactionState.COMMIT_MESSAGE;
        } catch (Throwable t) {
          // 失败则直接回滚事务消息
          return LocalTransactionState.ROLLBACK_MESSAGE;
        }
      }
      // 反查本地事务
      @Override
      public LocalTransactionState checkLocalTransaction(MessageExt msg) {、
        // 从消息中获得订单ID
        String orderId = msg.getUserProperty("orderId");

        // 去数据库中查询订单号是否存在，如果存在则提交事务；
        // 如果不存在，可能是本地事务失败了，也可能是本地事务还在执行，所以返回UNKNOW
        //（PS：这里RocketMQ有个拼写错误：UNKNOW）
        return orderDao.isOrderIdExistsInDB(orderId)?
                LocalTransactionState.COMMIT_MESSAGE: LocalTransactionState.UNKNOW;
      }
    };
  }

    //....
}
```

在这个流程中，我们提供一个创建订单的服务，功能就是在数据库中插入一条订单记录，并发送一条创建订单的消息，要求写数据库和发消息这两个操作在一个事务内执行，要么都成功，要么都失败。在这段代码中，我们首先在init()方法中初始化了transactionListener和发生RocketMQ事务消息的变量producer。真正提供创建订单服务的方法是createOrder()，在这个方法里面，我们根据请求的参数创建一条消息，然后调用RocketMQ producer发送事务消息，并返回事务执行结果。
<div><strong>精选留言（1）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/dc/08/64f5ab52.jpg" width="30px"><span>陈斌</span> 👍（0） 💬（0）<div>Kafka事务的怎么使用呢，我这边刚好有一个topic A到 topic B的场景，我怎么利用Kafka的事务和幂等保证消息的 Exactly Once ?</div>2022-05-03</li><br/>
</ul>