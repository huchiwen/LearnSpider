'''
 等差数列通项公式:an=a1+(n-1)*d
 a1
 d 等于page_num,page_num 就是每页的条数
  
'''
import time
import pprint


def page_code():

    a1 = 1 
    page_num = 20
    page_size = 446855
    total = page_size / page_num
    data = {}

    for i in range(1,page_size):

        list_number = a1 + (i -1) * page_num
        step =(list_number + page_num) - 1
        data[i] = {list_number,step} 
        data.update()
        
        #print(list_number,step)
    return data
   
'''
   要用遍历字典,
   再用list才可以取到字典里面的值

'''
if __name__ == '__main__':
   
   r = page_code()
   pp = pprint.PrettyPrinter(width=41, compact=True)
   #pp.pprint(type(r))
   for k,v in r.items():
      list_number = list(v)[0]
      step = list(v)[1]
      print(k,list_number,step)
      
