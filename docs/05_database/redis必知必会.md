#  

## 一、Redis 基础

- **是什么**：Remote Dictionary Server，开源、高性能的 **内存型 KV 数据库**。
- **特点**：
  - 单线程模型（IO 多路复用 + 事件驱动）。
  - 高性能（内存操作 + 单线程避免锁竞争）。
  - 支持多种数据结构，不止 KV。
  - 持久化支持（RDB、AOF）。
  - 支持分布式（主要包括 **主从复制**、**Redis 哨兵**、**Redis 集群** 和 **分布式锁**）。
- **应用场景**：
  - 缓存（热点数据）。
  - 分布式锁。
  - 排行榜、计数器。
  - 消息队列（Pub/Sub、Stream）。
  - 会话存储（Token、Session）。

------

## 二、Redis 数据结构 & 应用场景

1. **String（字符串）**

   - 最常见，最大 512MB。

   - 应用：缓存对象、分布式锁（setnx）、计数器（incr/decr）。
   
   **核心命令**
   
   - `SET key value [EX seconds] [NX|XX]`：设置 key（EX 设置过期，NX 不存在时才设置，XX 已存在时才设置）。
   - `GET key`：取值。
   - `MSET/MGET`：批量操作。
   - `INCR/DECR key`：自增/自减。
   - `APPEND key value`：追加。
   - `GETSET key value`：原子替换并返回旧值。
   
   **应用场景**
   
   - 缓存对象：`SET user:1 "{...}" EX 3600`
   - 分布式锁：`SET lock:order 1 NX PX 5000`
   - 计数器：`INCR page:view:123`


2. **Hash（哈希）**

   - 类似 `key -> { field : value }`。
   - 应用：存储对象属性（用户信息）。

   **核心命令**

   - `HSET key field value`：设置字段。
   - `HGET key field`：取值。
   - `HDEL key field`：删除字段。
   - `HGETALL key`：获取所有 field-value。
   - `HINCRBY key field 1`：字段自增。
   - `HEXISTS key field`：判断是否存在。

   **应用场景**

   - 存储对象：`HSET user:1 name "Tom" age 20`
   - 购物车：`HSET cart:1001 product:1 2`
   - 属性计数：`HINCRBY user:1 login_count 1`

3. **List（列表）**

   - 双向链表。
   - 应用：消息队列、时间线。

   **核心命令**

   - `LPUSH/RPUSH key value`：左/右插入。
   - `LPOP/RPOP key`：弹出。
   - `LRANGE key start stop`：获取子列表。
   - `BLPOP/BRPOP key timeout`：阻塞弹出。
   - `LREM key count value`：删除元素。

   **应用场景**

   - 消息队列：`LPUSH queue order_123`
   - 时间线：`LPUSH timeline:uid value`
   - 阻塞队列：`BLPOP task:queue 0`

4. **Set（集合）**

   - 无序、唯一。
   - 应用：标签、去重、共同好友。

   **核心命令**

   - `SADD key member`：添加。
   - `SMEMBERS key`：获取所有成员。
   - `SREM key member`：删除。
   - `SISMEMBER key member`：是否存在。
   - `SUNION/SINTER/SDIFF`：集合运算。

   **应用场景**

   - 用户标签：`SADD user:1:tags sports reading`
   - 去重：`SADD ip:set 1.1.1.1`
   - 社交关系：`SINTER user:1:friends user:2:friends` → 共同好友

5. **Sorted Set（有序集合）**

   - 元素带权重（score），按 score 排序。
   - 应用：排行榜、优先级队列。

   **核心命令**

   - `ZADD key score member`：添加。
   - `ZRANGE key start stop [WITHSCORES]`：升序。
   - `ZREVRANGE key start stop [WITHSCORES]`：降序。
   - `ZREM key member`：删除。
   - `ZINCRBY key increment member`：分数自增。
   - `ZRANK/ZREVRANK`：排名。

   **应用场景**

   - 排行榜：`ZADD rank 100 user1`
   - 延时队列：score 设为时间戳，按时间取。
   - 优先级队列。

6. **Bitmap（位图）**

   - 对 String 进行位操作。
   - 应用：用户签到、活跃状态。

7. **HyperLogLog**

   - 基数统计（近似去重，误差 0.81%）。
   - 应用：UV（独立访客统计）。

8. **Geo（地理位置）**

   - 经纬度存储与半径查询。
   - 应用：附近的人/店。

9. **Stream（流）**

   - Redis 5.0 引入，消息队列增强版。
   - 应用：日志收集、事件流。

------

## 三、持久化机制

1. **RDB（快照）**
   - 周期性保存内存快照到磁盘。
   - 优点：恢复快、文件小。
   - 缺点：可能丢数据（快照点后）。
2. **AOF（追加日志）**
   - 记录写操作日志，重放恢复。
   - 优点：数据更完整。
   - 缺点：文件大、性能差。
   - 策略：`always`、`everysec`（常用）、`no`。
3. **混合持久化**（Redis 4.0+）
   - RDB 快照 + AOF 增量。

------

## 四、内存管理

- **内存淘汰策略**（maxmemory-policy）：
  - noeviction（默认，不淘汰，直接报错）。
  - allkeys-lru（最常用，淘汰最少使用的 key）。
  - allkeys-random。
  - volatile-lru（仅带过期时间的 key）。
  - volatile-ttl（淘汰快过期的 key）。
- **内存分配器**：jemalloc，减少碎片。

------

## 五、Redis 高可用 & 集群

1. **主从复制**
   - 异步复制，读写分离。
   - 应用：提高读性能、数据备份。
2. **哨兵（Sentinel）**
   - 监控主节点，自动故障转移。
   - 提供服务发现（客户端连 sentinel，获取新主）。
3. **集群（Cluster）**
   - 数据分片，槽位（16384 个 slot）。
   - 特点：去中心化，自动分片，支持扩缩容。

------

## 六、Redis 分布式特性

- **分布式锁**：
  - `SET key value NX PX 30000`（原子操作）。
  - 常见方案：Redlock。
  - 问题：锁超时、续约、时钟漂移。
- **消息队列**：
  - List 实现：简单，但存在丢消息/重复。
  - Pub/Sub：实时，但无法持久化。
  - Stream：可靠队列，支持消费组。

------

## 七、性能优化

1. **使用建议**
   - 合理设置过期时间（避免内存爆炸）。
   - 使用 pipeline 批量操作，减少 RTT。
   - bigkey 问题（避免单个 key 数据过大）。
   - 使用 hash tag 控制集群分片。
2. **监控 & 调优**
   - `info` 命令查看性能。
   - 慢查询日志。
   - 内存分析：`memory usage / stats`。
   - 热点 key 监控。