#



## 1. **MySQL 基础**

### **数据类型**

- **数值类型**：`INT`, `TINYINT`, `BIGINT`, `DECIMAL`, `FLOAT`, `DOUBLE`
  - **INT**：常见的整数类型，通常用于计数、ID 等。
  - **DECIMAL**：精确小数，适合金融类计算，避免浮点数误差。
- **字符类型**：`CHAR`, `VARCHAR`, `TEXT`, `ENUM`
  - **CHAR**：定长，适合存储固定长度的字符串（如：国家代码）。
  - **VARCHAR**：变长，适合存储长度不固定的字符串。
  - **TEXT**：大文本数据，适合存储大量文本（如：文章内容）。
- **日期时间类型**：`DATE`, `DATETIME`, `TIMESTAMP`, `TIME`
  - `TIMESTAMP` 和 `DATETIME` 区别：`TIMESTAMP` 是基于 UTC 存储的，而 `DATETIME` 是存储实际时间。
- **二进制类型**：`BLOB`, `BINARY`, `VARBINARY`

| 类型         | 大小                                                 | 范围（有符号）                                               | 范围（无符号）                                               | 用途            |
| :----------- | :--------------------------------------------------- | :----------------------------------------------------------- | :----------------------------------------------------------- | :-------------- |
| TINYINT      | 1 Bytes                                              | (-128，127)                                                  | (0，255)                                                     | 小整数值        |
| SMALLINT     | 2 Bytes                                              | (-32 768，32 767)                                            | (0，65 535)                                                  | 大整数值        |
| MEDIUMINT    | 3 Bytes                                              | (-8 388 608，8 388 607)                                      | (0，16 777 215)                                              | 大整数值        |
| INT或INTEGER | 4 Bytes                                              | (-2 147 483 648，2 147 483 647)                              | (0，4 294 967 295)                                           | 大整数值        |
| BIGINT       | 8 Bytes                                              | (-9,223,372,036,854,775,808，9 223 372 036 854 775 807)      | (0，18 446 744 073 709 551 615)                              | 极大整数值      |
| FLOAT        | 4 Bytes                                              | (-3.402 823 466 E+38，-1.175 494 351 E-38)，<br />0，<br />(1.175 494 351 E-38，3.402 823 466 351 E+38) | 0，(1.175 494 351 E-38，3.402 823 466 E+38)                  | 单精度 浮点数值 |
| DOUBLE       | 8 Bytes                                              | (-1.797 693 134 862 315 7 E+308，-2.225 073 858 507 201 4 E-308)，<br />0，<br />(2.225 073 858 507 201 4 E-308，1.797 693 134 862 315 7 E+308) | 0，(2.225 073 858 507 201 4 E-308，1.797 693 134 862 315 7 E+308) | 双精度 浮点数值 |
| DECIMAL      | 对DECIMAL(M,D) ，<br />如果M>D，<br />为M+2否则为D+2 | 依赖于M和D的值                                               | 依赖于M和D的值                                               | 小数值          |

### **表与索引**

- **表操作命令**
  - `CREATE TABLE`, `DROP TABLE`, `ALTER TABLE`
  - `ADD COLUMN`, `DROP COLUMN`, `MODIFY COLUMN`
  - **锁表**：`LOCK TABLES`, `UNLOCK TABLES`
- **索引操作**
  - `CREATE INDEX`, `DROP INDEX`
  - 索引类型：**B-tree**（默认）、**Hash**、**Full-Text**、**Spatial**
  - **联合索引**：多列索引，顺序非常重要。

### **常见查询**

- **SELECT** 查询：`SELECT *`, `SELECT COUNT(*)`, `SELECT DISTINCT`
- **WHERE 子句**：`=`, `>`, `<`, `BETWEEN`, `IN`, `LIKE`, `IS NULL`
- **JOIN**：`INNER JOIN`, `LEFT JOIN`, `RIGHT JOIN`, `FULL JOIN`（MySQL 不支持 FULL JOIN）
- **GROUP BY**：`GROUP BY`, `HAVING`
- **ORDER BY**：`ORDER BY`（支持多个字段排序）
- **LIMIT**：用于限制返回的记录数

------

## 2. **MySQL 高级查询与优化**

### **查询优化**

- **EXPLAIN**：查看查询计划，优化 SQL 查询。
  - `EXPLAIN SELECT * FROM users WHERE id = 1;`
  - 关注字段：`type`（访问类型）、`key`（使用的索引）、`rows`（扫描的行数）
- **索引优化**
  - 使用合适的索引：通常查询中用到的字段应加索引（尤其是 `WHERE`, `ORDER BY`, `JOIN` 中的字段）。
  - **覆盖索引**：查询的所有字段都在索引中，可以避免回表，减少 IO。
- **避免全表扫描**：选择合适的索引，避免使用 `SELECT *`，减少数据的加载。

### **子查询 vs 联接**

- **子查询**：通常情况下性能较差，尤其是使用在 `WHERE` 子句中的时候。
  - 优化：将子查询转换为 `JOIN` 查询，尽量避免在 `SELECT` 中嵌套子查询。
- **联接（JOIN）**：
  - **INNER JOIN**：只返回两表中匹配的记录。
  - **LEFT JOIN**：返回左表所有记录，即使右表没有匹配。
  - **JOIN 顺序优化**：MySQL 会根据 `JOIN` 表的顺序来执行查询，确保最小的表先进行查询，避免较大的表先进行扫描。

------

## 3. **事务与锁**

### **事务**

- **ACID 特性**
  - **原子性（Atomicity）**：事务要么全部完成，要么全部回滚。
  - **一致性（Consistency）**：事务开始和结束时，数据库的一致性被保持。
  - **隔离性（Isolation）**：事务间的操作互不干扰，默认 `REPEATABLE READ` 隔离级别。
  - **持久性（Durability）**：事务一旦提交，数据永久保存。
- **事务控制命令**
  - `START TRANSACTION` 或 `BEGIN`
  - `COMMIT`：提交事务
  - `ROLLBACK`：回滚事务
  - **隔离级别**：
    - `READ UNCOMMITTED`（最低）
    - `READ COMMITTED`
    - `REPEATABLE READ`（默认）
    - `SERIALIZABLE`（最高）

### **锁**

- **行锁 vs 表锁**
  - **行锁**：InnoDB 提供，锁定的是特定的行，支持并发操作。
  - **表锁**：MyISAM 提供，锁定整个表，限制了并发性能。
- **常见锁类型**
  - **共享锁（S锁）**：允许其他事务读，但不能修改。
  - **排他锁（X锁）**：不允许其他事务读取或修改。
- **死锁**：两个或更多事务因为持有对方需要的锁而相互等待，造成死锁。MySQL 会自动检测死锁并回滚其中一个事务。

------

## 4. **MySQL 存储引擎**

### **InnoDB vs MyISAM**

- **InnoDB**：支持事务、行级锁、外键、崩溃恢复。
  - 默认的存储引擎。
  - 适合高并发的 OLTP 系统。
- **MyISAM**：不支持事务、表级锁、没有外键。
  - 适合以查询为主的系统，读多写少。

### **存储引擎的选择**

- 使用 **InnoDB** 存储引擎时，确保事务性和行级锁的优势，适合多并发操作。
- 使用 **MyISAM** 时，适用于读多写少的系统，可以提高读取性能。

## 5. **MySQL 性能优化**

### **查询优化**

- **合理使用索引**：选择合适的字段进行索引创建，尤其是大表中常用的 `WHERE`, `ORDER BY` 和 `JOIN` 字段。
- **避免 SELECT ***：选择具体的字段，减少不必要的 IO 操作。
- **缓存机制**：使用 MySQL 的查询缓存（注意：从 MySQL 5.7.20 开始，默认查询缓存已废弃）。

### **数据库设计优化**

- **表的设计**：避免使用过多的 `TEXT` 和 `BLOB` 类型，减少索引大小。
- **范式与反范式**：适当使用范式（3NF）来减少冗余数据，但在性能要求极高时可以适度反范式化。

### **硬件与系统优化**

- **内存优化**：根据 MySQL 的内存使用情况配置合适的 `innodb_buffer_pool_size`，使其适应数据库大小。
- **磁盘优化**：使用 SSD 磁盘，提高磁盘的读写性能。

------

## 6. **备份与恢复**

### **备份方式**

- **物理备份**：`mysqldump`（逻辑备份），`Xtrabackup`（物理备份）
  - **mysqldump**：适合小数据量的备份，可以导出 SQL 文件。
  - **Xtrabackup**：不需要停机，适用于大规模备份。
- **增量备份**：使用 `binlog` 来记录增量变更，实现增量备份。

### **恢复方式**

- 使用 `mysql` 命令恢复备份：

  ```
  mysql -u root -p < backup.sql
  ```

- 使用 `Xtrabackup` 恢复物理备份。

------

## 7. **MySQL 分区与分表**

### **分区（Partitioning）**

- **范围分区**（Range Partitioning）：根据值的范围进行分区（例如日期）。
- **哈希分区**（Hash Partitioning）：根据哈希算法将数据分配到不同分区。

### **分表（Sharding）**

- **垂直分表**：按业务功能分表（例如：一个表存储用户信息，另一个表存储订单信息）。
- **水平分表**：按数据量分表（例如：按用户 ID 范围分表）。





## 4 检索：

```
select column from table;
select * from table;
select distinct column from table;
select column from table limit 5;
select column from table 5,5;   #  从行5开始的5行
```

## 5 排序检索数据

默认以数据底层表中出现的顺序展示，不应该假定检索出来的顺序有意义。
```
select column from table order by column;   # 使用非检索的列排序也是合法的
select column from table order by column, column2;  # 多列排序，只有当第一列不同时，才会使用第二列
select column from table order by column desc;  # 降序排列
select column from table order by column desc, column2; # desc 直接作用它前边的列，多列降序需要每个列都指定 desc
select column from table order by column desc limit 1; # limit 放最后，这里找到最大的值
```


## 6 过滤数据

where子句操作符： = , != , <, <=, >, >=, BETWEEN

```
select name, price from products where price=2;
select name, price from products where price is null;  # 空值 NULL 检查
select name, price from products where price BETWEEN 3 and 5;  # 找到3和5之间，包括3和5
```


## 7 数据过滤
组合 where 子句。注意 AND 优先级高于 OR，如果必要应该使用括号，尽量都用括号防止歧义。

`select prod_name, prod_price from products where (vend_id=1002 or vend_id=1003) and prod_price>=10`

```
select name, price from products where price > 3 and price < 5;
select name, price from products where price in (3,5);  # in 比使用 or 更快
select name, price from products where price not in (3,5);  # 使用 not 否定条件
select Concat(vend_name, '(', vend_country, ')') from vendors order by vend_name;    # 计算字段
```


## 8 用通配符过滤

LIKE操作符(谓词)。

```
# %表示任何字符出现任意次数，不会匹配 NULL
select prod_id,prod_name from products where prod_name LIKE 'jet%';   # 注意尾空格可能会 干扰通配符
select prod_id,prod_name from products where prod_name LIKE '%anvil%';

# _ 只能匹配单个字符
select prod_id,prod_name from products where prod_name LIKE '% ton anvil';
```

注意：不要过度使用通配符；尽量不要把通配符放在开始位置；


## 9 使用正则表达式搜索

mysql 支持正则表达式的子集 REGEXP, LIKE匹配整串

```
# 搜索prod_name 包含文本 1000 的所有行
select prod_id,prod_name from products where prod_name REGEXP '1000' order by prod_name;
select prod_id,prod_name from products where prod_name REGEXP '1000|2000' order by prod_name; # 搜索两个串之一
```

## 10 创建计算字段

拼接字段： concat()

```
select concat(vend_name, ' (', vend_country, ')') from vendors order by vend_name;
select concat(vend_name, ' (', RTrim(vend_country), ')') from vendors order by vend_name;  # RTrim/LTrim/TRim 去除空格
```

别名：使用 as 支持列 别名

```
select Concat(RTrim(vend_name), ' (', RTrim(vend_country), ')') AS vend_title from vendors order by vend_name;
```

算数计算：对检索出的数据进行算数计算


```
select prod_id,quantity,item_price,quantity*item_price AS expanded_price from orderitems where order_num=20005;
```


## 11 使用数据处理函数

文本、数值计算、日期处理、系统函数等

```
# 文本：Left, Length, Locate, Lower, LTrim, Right, RTrim, Soundex(替换为描述语音表示的字母数字模式), SubString, Upper
select vned_name,Upper(vend_name) as vend_name_upcase from vendors order by vend_name;

# 日期：CurDate, Date, Day, Hour, Minute, Month, Now, Second, Time, Year
select cust_id,order_num from orders where order_date ='2005-09-01';
select cust_id,order_num from orders where Date(order_date) ='2005-09-01';  # use Date，更准确
select cust_id,order_num from orders where Date(order_date) BETWEEN '2005-09-01' and '2005-09-30';
select cust_id,order_num from orders where Year(order_date) =2005 and Month(order_date) =9;

# 数值：Abs, Cos, Exp, Mod, Pi, Rand, Sin, Sqrt, Tan
```


## 12 汇总数据

汇总而不是检索数据，确定行数、获取和、找出最大最小平均值。


五个聚集函数（运行在行组上，计算和返回单个值的函数）: avg, count, max, min, sum

```
# avg
select avg(price) as avg_price from products;  # avg会忽略列值为 NULL 的行

# count
select count(*) as num_cust from customers;   # count(*)对表中的行数计算，不管包含的是 NULL 还是非空
select count(cust_email) as num_cust from customers;   # count(column) 忽略 NULL 的值

# max、min, 忽略 NULL 值
select max(prod_price) as max_price FROM products;

# sum
select sum(quantity) as items_ordered from orderitems where order_num = 20005; # ignore NULL

# distince
select avg(quantity) as items_ordered from orderitems where order_num = 20005; # ignore NULL
```

## 13 分组数据
group by and having，分组允许把数据分为多个逻辑组，以便能够对每个组进行聚集计算。

```
# 分组
select vend_id,count(*) as num_prods from products group by vend_id;
# 使用 having 过滤分组，where 过滤行，having 支持所有的where子句条件
select cust_id, count(*) as orders from orders group by cust_id having count(*)>=2;
# having and where 一起用
select cust_id, count(*) as orders from orders where prod_price>=10 group by cust_id having count(*)>=2;

# order by and group by
select order_num, sum(quantity*item_price) as ordertotal from orderitems group by order_num
having sum(quantity*item_price)>=50
order by ordertotal;
```

## 14 使用子查询


子查询： 在SELECT语句中，子查询总是从内向外处理。

```
# 利用子查询进行过滤。可以把一条 select 语句返回的结果用于另一条 select 语句的 where 子句
select cust_name, cust_contact
from customers
where cust_id in (select cust_id
                  from orders
                  where order_num in (select
                      order_num from orderitems where prod_id='TNT2')); # 参考15章使用join 处理


# 作为计算字段使用子查询，相关子查询需要限定列名
select cust_name, cust_state, (select count(*) from orders where orders.cust_id=customers.cust_id) as orders
from customers order by cust_name;
```


## 15 联结表

```
# 引用的列可能出现二义性时，必须使用完全限定列名
select vend_name, prod_name, prod_price from vendors, products where vendors.vend_id=products.vend_id order by vend_name,prod_name;
# 内部联结（等值联结）
select vend_name, prod_name, prod_price from vendors INNER JOIN products on vendors.vend_id = products.vend_id;
# 连接多个表，sql 对一条 select 中的连接的表数目没有限制。先列出所有表，然后定义表之间的关系
select prod_name,vend_name,prod_price,quantity

# 14章的例子使用 join 处理
select cust_name,cust_contact, from customers,orders,orderitems
where customers.cust_id=orders.cust_id and orderitems.order_num=orders.order_num and prod_id='TNT2';
```


## 16 创建高级联结

何时使用表别名？允许单条 select 中多次引用相同的表

自连接：用 as 语句别名

`select p1.prod_id,p1.prod_name from products as p1, products as p2 where p1.vend_id=p2.vend_id and p2.prod_id='DTNTR';`

外部联结：联结包含了那些在相关表中没有关联行的行。这种类型的联结称为外部联结。
与内部联结关联两个表中的行不同的是，外部联结还包括没有关联行的行。在使用OUTER JOIN语法时，必须使用RIGHT或LEFT关键字指定包括其所有行的表（RIGHT指出的是OUTER JOIN右边的表，而LEFT指出的是OUTER JOIN左边的表）。上面的例子使用LEFT OUTER JOIN从FROM子句的左边表（customers表）中选择所有行。为

复合查询：
多数SQL查询都只包含从一个或多个表中返回数据的单条SELECT语句。MySQL也允许执行多个查询（多条SELECT语句），并将结果作为单个查询结果集返回。这些组合查询通常称为并（union）或复合查询（compound query）。
也可以用 or 条件实现相同功能。简化复杂 where


## 17 组合查询
可以用 union 操作符来组合多个 SQL 查询，把结果合并成单个结果集。使用 union 可以使用多个 where 条件替换。

```
# union 必须是相同的列，并且返回的是不重复的行。可以使用 union all 返回所有的行(这个 where 无法完成)
select vend_id,prod_id,prod_price from products where prod_price<=5 union
select vend_id,prod_id,prod_price from products wehre vend_id in (1002,1002);
```