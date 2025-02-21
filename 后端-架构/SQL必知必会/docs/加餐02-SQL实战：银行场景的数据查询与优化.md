你好，我是陈博士。今天我们来看下银行贷款业务的数据查询与优化。

贷款业务是银行的重要工作之一。通过数据查询，可以了解客户的信用风险，对后续审批贷款进行决策。同时在日常运营中，也需要做各种数据报表和统计，以便了解不同时期、不同类型用户、不同产品的经营业绩和风险情况。

针对该场景，我整理了3张数据表以及对应的查询问题。针对这些查询问题，你可以了解到这些SQL该如何撰写。

## 数据表

- 客户信息表 customer

<!--THE END-->

![图片](https://static001.geekbang.org/resource/image/65/8b/651aec6416d34f6fe7f2e1efaf7d098b.jpg?wh=1332x1190)

- 产品信息表 product

<!--THE END-->

![图片](https://static001.geekbang.org/resource/image/ac/96/acb459a209237a10b3fdf2833e411e96.jpg?wh=1316x642)

- 贷款信息表 loan

## ![图片](https://static001.geekbang.org/resource/image/4c/8c/4c8f64b404c5c12b35d1f5b68becb68c.jpg?wh=1332x1464)

## 问题设定

我从客户信息查询、产品信息查询、贷款信息查询、综合查询、聚合查询等维度，设置了一些常见的查询问题。我们一起来看一下。

### **客户信息查询**

查询身份号为 478116535425961877 的用户贷款的情况。

```plain
SELECT c.name, c.id_number, l.loan_type, l.loan_amount, l.loan_term, l.loan_issue_date, l.loan_status
FROM customer c
JOIN loan l ON c.customer_id = l.customer_id
WHERE c.id_number = '478116535425961877';
```