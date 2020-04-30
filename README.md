# textquery
Process text files in relational way, using SQL.

# Features
- support projection, filter, group by order by, limit-offset
- support join, set op, subquery like in/not in, exist, not exist, = etc
- support time functions, string functions

# Architecture

```
- Parser 
 - Plan
  - Relational Operator
    - DataSource
```

# Demo

## Basic Example

a.txt has content below

```
China is in Asia
USA  is in America
Germany  is in Euro
France  is in Euro
```

can be queryed using follow bash cmd

```
textquery "select c1 from a.txt where c4 = 'Euro'"
```

the output is
```
Germany
France
```

## Group By Example

a.txt has content below

```
China | Asia
USA | America
Germany | Euro
France | Euro
```

can be queryed using follow bash cmd

```
textquery "select c2, ' ', group_concat(c1, ',') from a.txt group by c2"
```

the output is
```
China Asia
USA America
Euro Germany,France

```

## Subquery Example

`blacklist.txt`：

```
Tom
Jerry
Smith
Alice
Bob
```

`user.txt`：

```
Tommy
Bob
Jack
```

Want to know good guys in user.txt?  just type
```
textquery "select * from user.txt where c1 not in (select * from blacklist.txt)"
```

you will get
```
Tommy
Jack
```


## Join Example

a.txt has content below

```
China is in Asia
USA  is in America
Germany  is in Euro
France  is in Euro
```

b.txt has content below

```
Asia | Sunny
Ameria  | Cloudy
Euro |  Rainy
```

can be queryed using follow bash cmd

```
textquery "select t1.c1, ',' t2.c2 from a.txt t1, b.txt t2 where t1.c4 = t2.c1"
```

this will generate content below

```
China,Sunny
USA,Cloudy
Germany,Rainy
France,Rainy
```
