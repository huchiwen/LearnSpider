'''
 等差数列通项公式:an=a1+(n-1)*d
 a1
 d 等于page_num,page_num 就是每页的条数
  
'''
import pprint

def page_code():

    a1 = 1 
    page_num = 20
    page_size = 1001
    #total = page_size / page_num
    data = []

    for i in range(1,page_size):
        list_number = a1 + (i -1) * page_num
        step = (list_number + page_num) -1
        data.append([list_number,step])
    return data

if __name__ == '__main__':
   
   r = page_code()
   pp = pprint.PrettyPrinter(width=41, compact=True)
   #pp.pprint(type(r))

   for i in r :
       print(i)

