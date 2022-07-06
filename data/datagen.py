import os
import re
import numpy as np
import pandas as pd
from faker import Faker

c_category = 1
c_sku = 1000
c_products_per_sku = 50
c_hot_sale_products_ratio = 10
# if fake.pyint(0,c_hot_sale_products_ratio-1) == 0:
c_low_price_products_ratio = 10
# if fake.pyint(0,c_low_price_products_ratio-1) == 0:

c_shops = 100
# c_attribute = 20
attr_brand=50
attr_color=50
attr_weight=100
c_keyword = 4

fake=Faker()
Faker.seed(0)

b=10*1024

ofile_node_category = open('import_node_category.csv', 'w', buffering=b)
print("id,name", file=ofile_node_category)
ofile_node_sku = open('import_node_sku.csv', 'w', buffering=b)
print("id,name,attributes,brand,colour,serial", file=ofile_node_sku)
ofile_node_keyword = open('import_node_keyword.csv', 'w', buffering=b)
print("id,keywords", file=ofile_node_keyword)
ofile_node_attribute = open('import_node_attribute.csv', 'w', buffering=b)
print("id,type,value", file=ofile_node_attribute)
ofile_node_product = open('import_node_product.csv', 'w', buffering=b)
print("id,shop_id,name", file=ofile_node_product)

ofile_relation_IS_CATEGORY = open('import_relation_IS_CATEGORY.csv', 'w', buffering=b)
print("category_id,sku_id", file=ofile_relation_IS_CATEGORY)
ofile_relation_WITH_KEYWORD = open('import_relation_WITH_KEYWORD.csv', 'w', buffering=b)
print("keyword_id,sku_id", file=ofile_relation_WITH_KEYWORD)
ofile_relation_IS_SKU = open('import_relation_IS_SKU.csv', 'w', buffering=b)
print("product_id,sku_id", file=ofile_relation_IS_SKU)
ofile_relation_HAS_ATTRIBUTE = open('import_relation_HAS_ATTRIBUTE.csv', 'w', buffering=b)
print("product_id,attribute_id", file=ofile_relation_HAS_ATTRIBUTE)
ofile_relation_HOT_SALE = open('import_relation_HOT_SALE.csv', 'w', buffering=b)
print("sku_id,product_id", file=ofile_relation_HOT_SALE)
ofile_relation_SUPPLEMENT_WITH = open('import_relation_SUPPLEMENT_WITH.csv', 'w', buffering=b)
print("from_sku_id,to_sku_id", file=ofile_relation_SUPPLEMENT_WITH)
ofile_relation_LOW_PRICE = open('import_relation_LOW_PRICE.csv', 'w', buffering=b)
print("sku_id,product_id", file=ofile_relation_LOW_PRICE)

c_attributes_per_product = 3
attr_list_brand=[]
attr_list_color=[]
attr_list_weight=[]

_a=0
for i in range(attr_brand):
    _target=re.sub(r',', '', fake.company() )
    print("{0},'brand',{1}".format(_a,_target), file=ofile_node_attribute)
    attr_list_brand.append(_target)
    _a+=1
for i in range(attr_color):
    _target=re.sub(r',', '', fake.color_name() )
    print("{0},'colour',{1}".format(_a,_target), file=ofile_node_attribute)
    attr_list_color.append(_target)
    _a+=1
for i in range(attr_weight):
    _target=fake.pyint(10000,99999,1)
    print("{0},'weight',{1}".format(_a,_target), file=ofile_node_attribute)
    attr_list_weight.append(_target)
    _a+=1

_c=0
_s=0
_k=0
_p=0

for c in range(c_category):
    print("{0},category_name_{0}".format(_c), file=ofile_node_category)
    for s in range(c_sku):
        print("{0},sku_name_{0},brand:{1}#colour:{2}#serial:{3},{4},{5},{3}".format(
            _s,
            attr_list_brand[fake.pyint(0,attr_brand-1,1)],
            attr_list_color[fake.pyint(0,attr_color-1,1)],
            attr_list_weight[fake.pyint(0,attr_weight-1,1)],
            fake.pyint(0,attr_brand-1,1),
            fake.pyint(0,attr_color-1,1),
            fake.pyint(0,attr_weight-1,1)
            ), file=ofile_node_sku)
        print("{0},{1}".format(_s,_c), file=ofile_relation_IS_CATEGORY)
        for k in range(c_keyword):
            print("{0},{1}".format(_k,  re.sub(r'[,.]', '', fake.paragraph(nb_sentences=1)   )  ), file=ofile_node_keyword)
            print("{0},{1}".format(_k,_s), file=ofile_relation_WITH_KEYWORD)
            _k+=1
        for p in range(c_products_per_sku):
            print("{0},{1},'product_name_{0}'".format(_p,fake.pyint(0,c_shops-1,1) ), file=ofile_node_product)
            print("{0},{1}".format(_p,_s), file=ofile_relation_IS_SKU)
            if fake.pyint(0,c_hot_sale_products_ratio-1) == 0:
                print("{0},{1}".format(_s,_p), file=ofile_relation_HOT_SALE)
            if fake.pyint(0,c_low_price_products_ratio-1) == 0:
                print("{0},{1}".format(_s,_p), file=ofile_relation_LOW_PRICE)
            _p+=1
        _s+=1
    for i in range( int(( (c_sku)/2)) ): 
        print("{0},{1}".format(_s-c_sku+i, _s-i-1), file=ofile_relation_SUPPLEMENT_WITH)
    _c+=1

ofile_node_category.close()
ofile_node_sku.close()
ofile_node_keyword.close()
ofile_node_attribute.close()
ofile_node_product.close()

ofile_relation_IS_CATEGORY.close()
ofile_relation_WITH_KEYWORD.close()
ofile_relation_IS_SKU.close()
ofile_relation_HAS_ATTRIBUTE.close()
ofile_relation_HOT_SALE.close()
ofile_relation_SUPPLEMENT_WITH.close()

exit(0)

