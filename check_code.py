a = {'頁 1': 'K4D156793-0-0001.jpg', '頁 2': 'K4D156793-0-0002.jpg'}
b = {'頁 1': 'a0F', '頁 2': '1eD'}

#c= {'K4D156793-0-0001.jpg':'a0F','K4D156793-0-0002.jpg':'1eD'}
c = {}

for k,v in a.items():
	for kk,vv in b.items():
		if k == kk:
			#c = {v:vv}
			c.update({v:vv})
print(c)