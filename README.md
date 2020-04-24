# sqltext
Process text files in relational way, using SQL.

# features
- support projection, filter, group by order by, limit-offset
- support join, set op, subquery like in/not in, exist, not exist, = etc
- support time functions, string functions

# architecture

```
- Parser 
 - Plan
  - Relational Operator
    - DataSource
```

# demo

## 1st Examle

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

## 2st Example
a.txt has content below

```
China | Asia
USA | America
Germany | Euro
France | Euro
```

can be queryed using follow bash cmd

```
sqltext "select c2, group_concat(c1, ',') from a.txt seperated by '|' group by c2"
```

the output is
```
China Asia
USA Americ
Euro Germany,France

```

## 3rd Example

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
