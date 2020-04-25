# sqltext
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
sqltext "select c1 from a.txt seperated by ' ' where c4 = 'Euro'"
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
sqltext "select c2, ' ', group_concat(c1, ',') from a.txt seperated by '|' group by c2"
```

the output is
```
China Asia
USA Americ
Euro Germany,France

```

## Insert Into Select Example

a.txt has content below

```
China is in Asia
USA  is in America
Germany  is in Euro
France  is in Euro
```

can be queryed using follow bash cmd

```
sqltext "insert into /tmp/b.txt select c1 from a.txt seperated by ' ' where c4 = 'Euro'"
```

this will generate a new file /tmp/b.txt with content below

```
Germany
France
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
sqltext "select t1.c1, ',' t2.c2 from a.txt t1 seperated by ' ', b.txt t2 seperated by '|'  where t1.c4 = t2.c1"
```

this will generate content below

```
China,Sunny
USA,Cloudy
Germany,Rainy
France,Rainy
```
