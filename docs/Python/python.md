[返回首页](/)

# python

## 文件操作

<span id="open"></span>

`open(文件名(路径), mode="", encoding="字符集合")`

**模式**：`r`，`w`，`a`  

按字节读取，不能encoding`rb`，`wb`，`ab`  

先读后写，读光标位置，写在文件末尾`r+` 

先写后读，写完光标在最后，读不到东西(f.seek(0)将光标移动到开头)，少用，会清空内容`w+`

光标直接在最后，需要移动光标`a+`

**光标操作**：

`f.seek(offset[, whence])`

- **offset** -- 开始的偏移量，也就是代表需要移动偏移的字节数
- **whence：**可选，默认值为 0。给offset参数一个定义，表示要从哪个位置开始偏移；0代表从文件开头开始算起，1代表从当前位置开始算起，2代表从文件末尾算起。

`f.tell()`  返回光标位置

`f.truncate()`  从截断到光标位置或参数位置(没给参数)

## 函数

参数顺序：位置参数，*args，默认值参数，**kwargs  `f(a, *args, b=c, **kwargs)`

形参的\*用于打散，实参的\*用于聚合

`global`用来在函数或其他作用域中使用全局变量

`nonlocal`用来在函数或其他作用域中使用最近外层(非全局)变量，改变量必须之前使用过。

函数名是变量。

### 闭包

**闭包**可以保护变量不受侵害，可以让一个变量常驻内存

```python
def outer()
    a = 10
    def inner()
        print(a)
    return inner
fn = outer()
fn()
```

### 迭代器

**迭代器** 只能向前，节省内存

```python
s = 可迭代对象
it = s.__iter__()
print(it.__next__())
```

判断是否可迭代

"\_\_iter\_\_" in dir(it)

or

from collections import Iterable, Iterator
isinstance(it, Iterable)

### 生成器

**生成器**  惰性机制，只能向前，节省内存

```python
def func():
    a = yeild 1
    yeild 2
gen = func()
gen.__next__() # 第一个必须为__next__()
gen.send(1) # a的值为1
for i in func(): # 生成器可以迭代
    print(1)
```

函数中如果有yield，这个函数就是生成器函数。

func() 获取的是生成器，不执行函数。

yield相当于return，但不会彻底中断函数，分段执行函数。

send()与\_\_next\_\_()功能相同，还可以给上一个yield传值

### 列表推导式

**列表推导式**：用一句话生成一个列表

```python
lst = [i for i in range(1, 10)]
```

`[结果 for循环 判断]`

```python
dic = {i[0]:i[1] for i in enumerate(list)}
dic = {i:list[i] for i in range(len(list))}
dic = {v:k for k, v in dic.items()}
set = {i for i in list}
```

### 生成器表达式

**生成器表达式**  没有元祖推导式！！

```python
gen = (i for i in range(10))
gen.__next__()
```

### 内置函数

+ 面向对象相关(9)

+ 迭代器/生成器相关(3)
  + range(start, end, step)
  
    start：起始值(包括)；end：结束值(不包括)；step：步长

  + next(iterator[, default])：迭代器的下一个元素
  
    iterator：迭代器；default：可选，没有下一个元素时返回值
  
  + iter(iterable)：用于生成迭代器
  
    iterable：可迭代对象
  
+ 其他(12)
  + 字符串类型代码的执行(3)
    + eval：执行字符串类型的代码，并返回最终结果

    + exec：执行字符串类型的代码

    + compile(source, filename, mode)：将一个字符串编译为字节代码

      source：字符串或者AST(Abstract Syntax Trees)对象；filename：代码文件名称，如果不是从文件读取代码则传递一些可辨认的值；mode：指定编译代码的种类，可以指定为 exec, eval, single
  + 输入输出(2)
    + input
    + print
  + 内存相关(2)
    + hash(object)：获取对象的哈希值
    + id(object)：获取对象的内存地址
  + 文件操作相关(1)
    + open：见[文件操作](#open)相关内容
  + 模块相关(1)
    + \_\_import\_\_：用于动态加载类和函数
  + 帮助(1)
    + help([object])：查看帮助信息
  + 调用相关(1)
    + callable：是否可被调用
  + 查看内置属性(1)
    + dir([object])：获取对象的名字、属性或方法列表
+ 反射相关(4)
+ 基础数据类型相关(38)
  + 和数字相关(14)
    + 数据类型(4)
      + bool([x])
      
        x：可选，要转换的对象  bool([])->True bool({})->True bool()->False bool(0)->False bool(None)->False
      
      + int(x[, base])
      
        x：数字或字符串；base：进制数，默认为10
      
      + float(x)
      
      + complex：复数
    + 进制转换(3)
      + bin(x)：转换为二进制
      + oct(x)：转换为十进制
      + hex(x)：转换为十六进制
    + 数学运算(7)
      + abs(x)：求绝对值
      
      + divmod(x, y)：
      
        x：被除数；y：除数，不能为0
      
      + round(number[, ndigits])
      
        number：四舍五入的数值；ndigits：小数点后的位数
      
      + pow(x, y[, z])
      
        x：底数；y：指数，z：最结果取模
      
      + sum(iterable[, start])
      
        iterable：可迭代对象；start：指定相加的参数
      
      + min(iterable)
      
        iterable：可迭代对象
      
      + max(iterable)
      
        iterable：可迭代对象
  + 和数据结构相关(24)
    + 序列(13)
      + 列表和元祖(2)
        + list
        + tuple
      + 相关内置函数(2)
        + reversed(seq)：反转序列
        
        + slice(start, stop[, step])
        
          start：开始裁剪的位置；end：结束裁剪的位置；step：步长
      + 字符串(9)
        + str(object)：对象转换为字符串

        + format

          ```python
          format('test', '<20') # 左对齐
          format('test', '>20') # 右对齐
          format('test', '^20') # 居中
          format('11', 'b') # 二进制
          format('11', 'c') # 转换成Unicode字符
          format('11', 'd') # 十进制
          format('11', 'o') # 八进制
          format('11', 'x') # 十六进制(小写字母)
          format('11', 'X') # 十六进制(大写字母)
          format('11', 'n') # 十进制
          format(123456789, 'e') # 科学计数法，默认保留6位小数
          format(123456789, '0.2e') # 科学计数法，保留2位小数(小写)
          format(123456789, '0.2E') # 科学计数法，保留2位小数(大写)
          format(1.23456789, 'f') # 小数点计数法，保留6位小数
          format(1.23456789, '0.2f') # 小数点计数法，保留2位小数
          format(1.23456789, '0.10f') # 小数点计数法，保留10位小数
          format(1.23456789e+10000, 'F') # 小数点计数法
          ```

        + bytes([source[, encoding[, errors]]])

          source：整数、字符可迭代对象；encoding：字符编码；errors：错误处理方法

          ​	如果 source 为整数，则返回一个长度为 source 的初始化数组；

          ​	如果 source 为字符串，则按照指定的 encoding 将字符串转换为字节序列；

          ​	如果 source 为可迭代类型，则元素必须为[0 ,255] 中的整数；

          ​	如果 source 为与 buffer 接口一致的对象，则此对象也可以被用于初始化 bytearray。

        + bytearry([source[, encoding[, errors]]])

          source：整数、字符可迭代对象；encoding：字符编码；errors：错误处理方法

        + memoryview(object)：返回内存查看对象。

        + ord(c)：字符串转换为ASCII

        + chr(i)：ASCII转换为字符串

          i：十进制或十六进制形式

        + ascii(object)：返回ascii编码或Unicode编码

        + repr(object)：将对象转为可转义字符(原样输出，不转义)
    + 数据集合(3)
      + 字典(1)
        + dict
      + 集合(2)
        + set
        + frozenset
    + 相关内置函数(8)
      + len(s)：可迭代对象长度或个数
      
      + sorted(iterable, key=None, reverse=False)
      
        iterable：可迭代对象；key：可选，排序规则；reverse：可选，升序或降序
      
      + enumerate(iterable, start=0)：创建枚举对象
      
        iterable：一个序列、迭代器；start：下标起始值
      
      + all(iterable)：and，判断可迭代对象是否包括假值
      
      + any(iterable)：or，判断可迭代对象是否全为假值
      
      + zip(iterable1, iterable2, ...)：可迭代对象打包成元祖
      
      + fiter(function, iterable)：过滤序列
      
        function：判断的函数；iterable：可迭代对象
      
      + map(function, iterable, ...)：函数操作可迭代对象
+ 作用域相关(2)
  + locals：函数会以字典的类型返回当前位置的全部局部变量
  + globals：函数以字典的类型返回全部全局变量

### 匿名函数

```python
lambda 参数: 返回值  # __name__都为lambda
```

## 模块

https://www.cnblogs.com/Eva-J/articles/7228075.html

https://www.cnblogs.com/Eva-J/articles/7292109.html

## 面向对象

## 补充

### 小数据池

小数据池字面值相同用`is`返回True

数字：-5~256

字符串中如果有特殊字符，内存的值就不同
