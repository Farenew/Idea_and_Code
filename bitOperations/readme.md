# 通过位运算实现基础的遍历

## 0. 排序

在说遍历前需要说一下排序, 排序主要有两种序列, 一种是Lexicographic order(Lex), 一种是Colexicographic order(CoLex)。遍历的时候结果就要遵循对应的排序方法。

这些排序方法都可以用笛卡尔积进行定义, 但是这样定义太过于数学化, 不好理解, 这里不介绍。以下的序列生成方法都用直观的定义。

首先, 对于序列来讲, 有两种体现方法: (1) 排列, (2) 组合。

- 排列, 排列的序列很好理解, ABC和ACB是不同的排列方法, 也就构成了序列。
- 组合, 组合用在子集里, 例如{a}, {b}, {a,b}构成的不同集合, 也体现了序列。

下面以组合介绍为主, 排列类似。

排序应用的地方很多, 比如Lex和CoLex组成[Walsh矩阵](https://en.wikipedia.org/wiki/Walsh_matrix), 用在数字信号处理。比如[超正方体](https://en.wikipedia.org/wiki/Tesseract)的研究等。

### 0.1 Lexicographic order

这种排序也叫字典序, 就是最容易理解的一种序列。给出{a,b,c}, 那么字典序就是:

> {}, {a}, {b}, {a,b,c}, {a,c}, {b}, {b,c}, {c}

想象一下查字典, 这个就很好理解了。

### 0.2 Reverse lexicographic order

就是字典序的逆序, 把排列反过来:

> {c}, {b,c}, {b}, {a,c}, {a,b,c}, {b}, {a}, {}

### 0.3 Reflected lexicographic order

字典序的反序, 把排列内部的顺序反过来:

> {}, {a}, {b}, {c,b,a}, {c,a}, {b}, {c,b}, {c}

### 0.4 Reverse reflected lexicographic order

字典序的反逆序, 同时对字典序进行反序和逆序:

> {c}, {c,b}, {b}, {c,a}, {c,b,a}, {b}, {a}, {}

### 0.5 Colexicographic order

这个序列在排列的时候很好辨认, 例如123的字典序是:

> 123, 132, 213, 231, 312, 321

对应Colexicographic order就是

> 321, 231, 312, 132, 213, 123

从右往左读, 是一种自然数大小的增序。

用在集合中也一样, 按照集合中**最大元素**进行排序。这里用集合{1,2,3}来表示, 那么Colexicographic order就是:

> {}, {1}, {2}, {1,2}, {3}, {1,3}, {2,3}, {1,2,3}

### 0.6 Reverse colexicographic order

把colexicographic order逆序排列:

> {1,2,3}, {2,3}, {1,3}, {3}, {1,2}, {2}, {1}, {}

### 0.7 Reflected colexicographic order

把colexicographic order反序排列:

> {}, {1}, {2}, {2,1}, {3}, {3,1}, {3,2}, {3,2,1}

### 0.8 Reverse reflected colexicographic order

把colexicographic order逆反序排列:

> {3,2,1}, {3,2}, {3,1}, {3}, {2,1}, {2}, {1}, {}


## 1. 求幂集(所有子集)

求一个集合的所有子集是非常常用的操作, 在算法中经常遇到。例如很多DP问题就可以通过这种方式进行暴力求解。

如果一个集合包含n个元素, 那么用位串表示就是111111....(n个1)。对于每个位来说:

- `0`可以表示这个元素没有选择
- `1`可以表示选择了这个元素

因此来讲, 那么就是从`000000....`到`111111.....`的一个循环即可:

```C++
for (unsigned long i = 0; i < (1UL << n); ++i){

}
```

这样生成的顺序是colexicographic order。

通过这样的构造, 就可以构造出序列对应的位串了, 具体要取每一个元素的话, 还要再加一个循环:

```C++
int main(){
    int arr[3] = {1,2,3};

    const unsigned int a = 3;
    const unsigned int t = 2;

    for(unsigned int i=0; i<(1U << a); i++){
        for(unsigned int j=0; j<a; j++){
            if(((1<<j) & i) != 0){
                cout << arr[j] << ' ';
            }
        }
        cout << '\n';
    }
}
```

其中内层循环是确定对list中元素进行判断。

## 2. 求组合

有时候还需要给出所有的组合, 比如求一个集合所有的大小为2的子集。这个用到的技巧称为`Gosper’s hack`, 最早出自MIT的一个技术报告集合[`HAKMEM`](http://home.pipeline.com/~hbaker1/hakmem/hacks.html#item175)。

对于一个数字x, 以bit表示的情况下, 要找到它的下一个和它bit为1个数相同的数字n, 方法如下: 

```
x;
y = x & -x;
c = x + y;
n = (((x ^ c) >> 2) / y) | c;
```

例如0b0011, 那么下一个就是0b0101, 其中1的个数相同。

使用这个技巧, 就可以找到集合中所有固定大小的子集的排列。完整示例代码如下:

```C++
unsigned int next(unsigned int x){
    unsigned int y, c, n;
    y = x & -x;
    c = x + y;
    n = (((x ^ c) >> 2) / y) | c;
    return n;
}
int main(){
    int arr[3] = {1,2,3};

    const unsigned int a = 3;
    const unsigned int t = 2;

    unsigned int high = 1U << (t-1);
    unsigned int first = high | (high -1);
    unsigned int last = first << (a-t);

    cout << high << " " << bitset<4>(high) << '\n';
    cout << first << " " << bitset<4>(first) << '\n';
    cout << last << " " << bitset<4>(last) << '\n';


    auto i = first;
    while(true){

        for(unsigned int j=0; j<3; j++){
            if(((1<<j) & i) != 0){
                cout << arr[j] << ' ';
            }
        }
        cout << '\n';
        i = next(i);

        if(i > last)
            break;
    }
}
```

关于Gosper’ hack, 解释一下, 假设`x=0b10101100`, 为了更加清楚, 有些地方用16位来写:


- 第一条语句：`y = x & -x`， 用于标识出x最低位的1, 假设1后面有a个0(这里a为2)。例如x为`0b0000000010101100`, 那么取负就是`0b1111111101010100`, 然后且运算就得到了`0b0000000000000100`. 所以得到`y = 0b00000100`

- 第二条语句: `c = x + y`; 这个语句**把x从右面开始的所有的连续的1全部清0, 然后进位设为1**. 这里假设有b个连续的1(这里b为2), 因为x是`0b10101100`, 那么加上`0b00000100`, 那么右边的1就被清掉了。变成`10110000`。所以此时`c = 0b10110000`

- 第三条语句: 首先`x ^ c`, 因为c右边的连续的b个1都被清0了, 所以这部分和x做异或就都是1了, 而且c还有一个进位是1, 因此这一步可以得到b+1个1.

    然后右移两位, 得到了: `0b00000111`, 再除以y, 相当于又右移了c位。此时得到了b-1个1. 之后再和`c`进行或运算, 相当于把最后一个1添加到后面。最后得到`10110001`;

这样生成的顺序也是colexicographic order。

## 参考

- [OEIS: Orderings](https://oeis.org/wiki/Orderings)
- [Lexicographic and colexicographic order](https://en.wikiversity.org/wiki/Lexicographic_and_colexicographic_order)
- [wikipedia: Lexicographical order](https://en.wikipedia.org/wiki/Lexicographical_order)
- [harvard: CS 207 Systems Development for Computational Science](https://read.seas.harvard.edu/~kohler/class/cs207-s12/lec12.html)
- [atyuwen: 位运算与组合搜索（一）](https://www.cnblogs.com/atyuwen/archive/2010/07/19/bit_combinatorics.html)
- [atyuwen: 位运算与组合搜索（二）](https://www.cnblogs.com/atyuwen/archive/2010/08/05/bit_comb_2.html)