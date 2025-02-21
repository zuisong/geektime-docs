你好，我是陈博士。今天我们来看下麦当劳如何通过数据查询与分析来优化其业务运营。

麦当劳每天处理大量的交易，涉及数以百万计的顾客订单。有效的数据分析不仅有助于理解顾客消费行为和偏好，还能够为管理层提供决策支持。

针对该场景，我整理了5张数据表以及对应的查询问题。针对这些查询问题，你可以了解到这些SQL该如何撰写。

## **数据表**

- **订单表 orders**  
  ![](https://static001.geekbang.org/resource/image/0f/b1/0f331b0d7d23b90fd78ce6cbb0d69cb1.jpg?wh=1798x1520)

<!--THE END-->

- **订单明细表 order\_details**  
  ![](https://static001.geekbang.org/resource/image/05/a1/05f2a4bc77b0aa12aed302dbb18f77a1.jpg?wh=1800x810)

<!--THE END-->

- **产品表 products**  
  ![](https://static001.geekbang.org/resource/image/37/e5/374ec704448b03f990a0d7a9fyy402e5.jpg?wh=1802x1220)

<!--THE END-->

- **门店表 stores**  
  ![](https://static001.geekbang.org/resource/image/68/fa/6832ccaba343ab13b05c1a4d95c576fa.jpg?wh=1808x1502)

<!--THE END-->

- **会员表 (members)**  
  ![](https://static001.geekbang.org/resource/image/f8/a0/f8eaba74a4a4219a693e12911ae646a0.jpg?wh=1820x1222)

## **问题设定**

我从门店分析、销售分析、产品分析、会员分析、订单分析、组合分析等维度设置了一些常见的查询问题，一起来看一下。

### **门店分析**

- 各城市门店数量分布

```plain
 SELECT city, COUNT(*) as store_count
FROM stores
GROUP BY city
ORDER BY store_count DESC
LIMIT 10;
 
// 说明：使用 GROUP BY 对城市进行分组，COUNT(*) 统计各城市门店数量，ORDER BY 和 LIMIT 限制结果，展示门店数量最多的前10个城市。
```

- 查找最近30天新开业的门店

```plain
SELECT store_name, city, address, created_time
FROM stores
WHERE created_time >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
ORDER BY created_time DESC;
 
// 说明：使用 DATE_SUB 和 CURDATE() 函数计算最近30天的时间范围，WHERE 子句筛选新开业的门店，ORDER BY 按创建时间降序排列。
```