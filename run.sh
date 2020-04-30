./textquery.py "select t1.c1,', ', t1.c2 from t1 where t1.c1 not in (select c1 from t2)";
