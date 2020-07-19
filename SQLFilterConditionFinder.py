import sqlparse

sql = '''select count(*) from users u where 
employee_type = 'Employee'  
and u.cust_id not in (1,2) 
and u.marketplace_id in (1,2,3,5)
and (u.users_stats > 0 OR u.users_listen > 0)
and cp.ACTIVITY_DT >= to_date('20160101','yyyymmdd') '''

parsed = sqlparse.parse(sql)

# Last token is where , In case of group by or order index need to be changed
where = parsed[0][-1]

sql_tokens = []
def get_tokens(where):
    identifier = None
    condition=[]
    for i in where.tokens:
        try:
            if identifier and str(i).upper() in['IN','NOT']:
                condition.append(str(i).upper())
            else:

                name = i.get_real_name()


            if name and isinstance(i, sqlparse.sql.Identifier):
                identifier = i

            elif identifier and isinstance(i, sqlparse.sql.Parenthesis):

                sql_tokens.append({
                    'key': str(identifier),
                    'value': str(identifier) +' ' + " ".join(condition) + ' '+i.value
                })
                condition.clear()
                identifier = None
            elif name is None or isinstance(i, sqlparse.sql.Parenthesis):
                identifier = None

                if isinstance(i, sqlparse.sql.Parenthesis):
                    KEY=""
                else:
                    KEY=str(i.left.value)

                sql_tokens.append({
                    'key': KEY,
                    'value':i.value
                })
            else:
                get_tokens(i)
        except Exception as e:
            pass


if __name__=="__main__":

    get_tokens(where)
    for filters in sql_tokens:
        print(filters)
