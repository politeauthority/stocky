import sys

sys.path.append("../..")
from app import app
from app.collections import companies


# cs = [57, 943, 1931, 2838, 3583]
# for c_id in cs:
#     c = Company.query.filter(Company.id == c_id).one()
#     print c.name
#     print c.meta
#     cm = CompanyMeta()
#     cm.company_id = c.id
#     cm.key = 'oldest_quote'
#     cm.val_type = 'datetime'
#     cm.val_dateteime = datetime(2016, 9, 9)
#     cm.save()

# print 'testing'


def collection_test():
    symbols = ['BAC', 'AAPL']
    cs = companies.get_companies_by_symbol(symbols)
    print cs
    for c in cs:
        print c

collection_test()
