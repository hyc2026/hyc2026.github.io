## C++标准库

### 顺序容器

#### 顺序容器类型：

+ `vector`: 支持快速随机访问，在尾部之外的位置插入删除可能很慢；保存在连续内存空间
+ `deque`: 支持快速随机访问，在头尾插入删除很快
+ `list`: 双向链表，支持双向顺序访问，在任何位置插入删除都很快
+ `forward_list`: 单向链表，支持单向顺序访问，在任何位置插入删除都很快
+ `array`: 固定大小数组，支持快速随机访问，不能添加或删除元素
+ `string`: 与`vector`类似的容器，专门保存字符；保存在连续内存空间

#### 容器操作：

+ 类型别名：
  + iterator
  + const_iterator
  + size_type
  + difference_type
  + value_type
  + reference
  + const_reference
+ 构造函数：
  + C c;
  + C c(c1);
  + C c(b, e);
  + C c{a, b, ...}
+ 赋值与swap
  + c1 = c2
  + c1 = {a, b, ...}
  + a.swap(b)
  + swap(a, b)
+ 大小
  + c.size()
  + c.max_size()
  + c.empty()
+ 添加删除元素
  + c.insert(args)
  + c.emplace(inits)
  + c.erase(args)
  + c.clear()
+ 关系运算符
  + ==, !=, <, <=, >, >=
+ 取迭代器
  + c.begin(), c.end()
  + c.cbegin(), c.cend()
+ 反向容器的额外成员（不支持forward_list）
  + reverse_iterator
  + const_reverse_iterator
  + c.rbegin(), c.rend()
  + c.crbegin(), c.crend()

#### 容器定义和初始化：

+ C c;
+ C c1(c2); C c1=c2; 容器类型必须匹配
+ C c{a, b, ...}
+ C c={a, b, ...}
+ C c(b, e); 容器类型可以不同，只要能转换
+ C c(n); C c(n, v); 除array外的顺序容器可以接受大小作为参数

```c++
list<string> l;
vector<const char *> v;
list<string> l1(l); // 容器类型必须匹配
vector<string> v1(v.begin(), v.end()); //容器类型可以不同，只要能转换
deque<sting> d(v.begin(), it); // 拷贝元素，直到（但不包括）it指向元素
```

#### 容器赋值：

+ c1 = c2; c = {a, b, ...}
+ seq.assign(b, e);
+ seq.assign(list);
+ seq.assign(n, v);

#### 添加元素：

array不支持这些操作
forward_list有自己专有的insert和implace，且不支持push_back和emplace_back
vector和string不支持push_front和emplace_front

+ c.push_back(v); c.emplace_back(args); 返回void
+ c.push_front(v); c.emplace_front(args); 返回void
+ c.insert(p, t); c.emplace(p, args); 在迭代器p指向的元素之前插入一个元素，并返回指向新元素的迭代器。
+ c.insert(p, b, e); b和e不能指向c中元素，返回指向先添加的第一个元素的迭代器，若范围为空，则返回p。
+ c.insert(p, list); 返回指向先添加的第一个元素的迭代器，若范围为空，则返回p。
+ c.insert(p, n, v); 返回指向先添加的第一个元素的迭代器，若范围为空，则返回p。

使用emplace时，将参数传递给构造函数

```c++
c.emplace_back(1021, 10, 1);
c.push_back(Year(1021, 10, 1));
```

#### 访问元素：

at和下标只适用于string、vector、deque和array
back不适用于forward_list

+ c.back(); c.front();
+ c[n]; c.at(n);

#### 删除元素：

array不支持这些操作
forward_list有自己专有的erase，且不支持pop_back
vector和string不支持pop_front

+ c.pop_back(); c.pop_front(); 返回void
+ c.erase(p); c.erase(b, e); 返回一个指向被删元素之后元素的迭代器
+ c.clear(); 返回void

#### forward_list操作

+ lst.before_begin(); lst.cbefore_begin(); 返回指向链表首元素之前不存在的元素的迭代器
+ lst.insert_after(p, t); lst.insert_after(p, n, t); lst.insert_after(p, b, e); lst.insert_after(p, list); 返回一个指向最后一个插入元素的迭代器，若范围为空则返回p
+ lst.emplace_after(p, args); 返回一个指向新元素的迭代器，若范围为空则返回p
+ lst.erase_after(p); lst.erase_after(b, e); 返回一个指向被删元素之后元素的迭代器

#### 改变容器大小

+ c.resize(n); c.resize(n, v);

#### 容器大小管理

shrink_to_fit只适用于vector、string和deque
capacity和reserve只适用于vector和string

+ c.shrink_to_fit(); 将capacity减少为与size同样大小
+ c.capacity(); 不重新分配内存空间的话，c可以保存多少元素
+ c.reserve(n); 分组至少能容纳n个元素的内存空间

#### string的特殊操作

+ string s(cp, n); s是指向数组中前n个字符的拷贝
+ string s(s2, pos2); s是s2从下标pos2开始的字符的拷贝
+ string s(s2, pos2, len2); s是s2从下标pos2开始的长为len2的字符的拷贝
+ s.substr(pos, n); 返回一个string，包含s从pos开始的n个字符的拷贝

args可以是下列形式之一；append和assign可以使用所有形式。
str不能与s相同，迭代器b和e不能指向s

|     args      |                说明                |
| :-----------: | :--------------------------------: |
|      str      |             字符串str              |
| str, pos, len |    str中从pos开始最多len个字符     |
|    cp, len    |   cp指向的字符数组的前len个字符    |
|      cp       |   cp指向的以空字符结尾的字符数组   |
|     n, c      |              n个字符c              |
|     b, e      |     迭代器b和e指定范围内的字符     |
|  初始化列表   | 花括号包围的，以逗号分隔的字符列表 |

+ s.insert(pos, args); 在pos之前插入args指定的字符；pos是下标则指向s的引用，pos是迭代器则返回指向第一个插入字符的迭代器
+ s.erase(pos, len); 删除pos开始的n个字符
+ s.assign(args); 返回一个指向s的引用
+ s.append(args); 返回一个指向s的引用
+ s.replace(range, args); 删除range内的字符，替换为args指定的字符。range或者是下标加长度，或者是指向s的迭代器。返回一个指向s的引用

每个搜索操作返回一个string::size_type，表示匹配发生位置的下标

|    args    |                     说明                      |
| :--------: | :-------------------------------------------: |
|   c, pos   |           中s中位值pos开始查找字符c           |
|  s2, pos   |         中s中位值pos开始查找字符串s2          |
|  cp, pos   | 中s中位值pos开始查找指针cp指向的C风格的字符串 |
| cp, pos, n |   中s中位值pos开始查找cp指向的数组前n个字符   |

+ s.find(args)
+ s.rfind(args)
+ s.find_first_of(args)
+ s.find_last_of(args)
+ s.find_first_not of(args)
+ s.find_last_not_of(args)

比较函数返回0、正数或负数

|          args          |                           说明                            |
| :--------------------: | :-------------------------------------------------------: |
|           s2           |                         比较s和s2                         |
|      pos1, n1, s2      |               s中pos1开始的n1个字符与s2比较               |
| pos1, n1, s2, pos2, n2 |    cs中pos1开始的n1个字符与s2中pos2开始的n2个字符比较     |
|           cp           |           比较s和cp指向的以空字符结尾的字符数组           |
|      pos1, n1, cp      | s中pos1开始的n1个字符与cp指向的以空字符结尾的字符数组比较 |
|    pos1, n1, cp, n2    |   s中pos1开始的n1个字符与cp指向的字符数组前n2个字符比较   |

s.compare(args);

数值转换

+ to_string(val); 返回数值val的string表示
+ stoi(s, p, b); stol(s, p, b); stoul(s, p, b); stoll(s, p, b); stoull(s, p, b); 返回s字符串表示的数值，b表示转换所用的基数，默认是10，p是size_t指针，用于保存s中第一个非数值字符的下标
+ stof(s, p); stod(s, p);stold(s, p); 返回s字符串表示的数值

#### 容器适配器

适配器是一种机制，是某种事物的行为看起来像另一种事物一样。包括stack、queue和priority_queue。

所有适配器都支持的操作

+ container_type 实现适配器的底层容器的类型
+ value_type 元素类型
+ size_type 保存当前类型的最大对象大小的类型
+ A a; A a(c); 构造函数
+ a.empty();
+ a.size();
+ swap(a, b);
+ a.swap(b);

栈适配器：默认基于deque实现，也可用list或vector

+ s.pop();
+ s.push(item);
+ s.emplace(args);
+ s.top()

队列适配器：queue基于deque实现，，也可用list或vector；priority_queue基于vector实现，也可用deque

+ q.pop();
+ q.front();
+ q.back(); 只适用于queue
+ q.top(); 只适用于priority_queue
+ q.push(item);
+ q.emplace(args);

### 泛型算法(generic algorithm)

这些算法不直接操作容器（不会执行容器的操作），而是遍历由两个迭代器指定的元素范围。迭代器令算法不依赖于容器，但依赖于元素类型。算法可能改变容器中保存元素的值，但不会改变底层容器的大小，不会直接添加或删除元素。

### 关联容器

#### 关联容器类型：

+ map
+ set
+ multimap
+ multiset
+ unordered_map
+ unordered_set
+ unordered_multimap
+ unordered_multiset

#### 定义关联容器：

```c++
map<string, size_t> word_count;
set<string> = {"a", "bb"};
map<string, string> authors = { {"LeBron Jaames", "Lakers"},
                                {"Stephen Curry", "Warriors"} };
```

对于有序容器，关键字类型必须定义元素的比较方法，默认情况下，标准库使用关键字类型的<运算符来比较两个关键词。关键字需要**严格弱序**

pair定义在头文件utility中，一个pair保存两个数据成员，pair是一个用来生成特定类型的模板。
pair的数据成员是public的，两个成员分别命名为first和second。

+ pair<T1, T2> p; pair<T1, T2> p(v1, v2); pair<T1, T2> p = {v1, v2}; 初始化
+ make_pair(v1, v2); 返回由v1和v2初始化的pair，其类型由v1和v2推断出来
+ p.first; p.second;

#### 容器操作：

+ key_type 容器的关键字类型
+ mapped_type 每个关键字关联的类型
+ value_type 对于set，与key_value相同；对于map，为pair<const key_type, mapped_type>

set的迭代器是const的

#### 添加元素：

+ c.insert(v); {word, 1}、make_pair(word, 1)、pair<string, size_t>(word, 1)、map<string, size_t>::value_type(word, 1)
+ c.emplace(args);
+ c.insert(b, e);
+ c.insert(il);
+ c.insert(p, v);
+ c.emplace(p, args);

insert和emplace返回一个pair，pair的first指向具有给定关键字的元素，second成员是bool值。若关键字不存在，元素被插入，bool为true；若关键字存在，bool为false。

#### 删除元素：

+ c.erase(k); 删除关键字k，返回删除的个数
+ c.erase(p); 返回指向p后的迭代器
+ c.erase(b, e); 返回e

#### 访问元素：

+ c[k]; 若k不存在，添加一个关键字为k的元素，对其进行值初始化
+ c.at(k);  访若k不存在，抛出out_of_range异常

对于不允许重复关键字的容器，find和count没有区别；对于允许重复关键字的容器，count返回关键字的个数。
lower_bount和upper_bound不适用于无序容器；下标和at只适用于非const的map和unordered_map

+ c.find(k); 指向第一个关键字为k的元素或end
+ c.count(k);
+ c.lower_bound(k); c.upper_bound(k); 指向第一个不小于（大于）k的元素
+ c.equal_range(k); 返回一个迭代器pair，表示关键字等于k的元素范围

#### 无序容器：

桶接口

+ c.bucket_count(); 正在使用的桶数目
+ c.max_bucket_count(); 容器能容纳的最多的桶数量
+ c.bucket_size(); 第n个桶中有多少个元素
+ c.bucket(k); 关键字为k的桶在哪个桶中

桶迭代

+ local_iterator const_local_iterator
+ c.begin(n); c.end(n); c.cbegin(n); c.cend(n);

哈希策略

+ c.load_factor(); 每个桶的平均元素数量
+ c.max_load_factor(); c在需要时添加新的桶，使得load_factor<max_load_factor
+ c.rehash(n); 重组存储，使得bucket_count>=n且bucket_count>size/max_load_factor
+ c.reserve(n); 重组存储，使得c可以保存n个元素且不必rehash

### 动态内存

