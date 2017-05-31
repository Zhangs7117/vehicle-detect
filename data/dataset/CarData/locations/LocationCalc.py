f1 = open('trueLocations.txt')
f2 = open('Locations.txt')


# KK=20
KK=170
correct = 0
x_percentage=0.3
y_percentage=0.3
num=0.0
error=0.0

flag = 0
for i in range(KK):
	line_1 = f1.readline()
	line_2 = f2.readline()
	s1 = line_1.split()
	s2 = line_2.split()
	if len(s2)==1:
		continue
	elif len(s1)!=len(s2):
		ss1 = s1[1:]
		ss2 = s2[1:]
		s1_x=[]
		s1_y=[]
		s2_x=[]
		s2_y=[]
		for j in range(len(ss1)):
			sss1 = ss1[j].strip('(').strip(')')
			sss1_x = sss1.split(',')[0]
			s1_x.append(sss1_x)
			sss1_y = sss1.split(',')[1]
			s1_y.append(sss1_y)

		for jj in range(len(ss2)):
			sss2 = ss2[jj].strip('(').strip(')')
			sss2_x = sss2.split(',')[0]
			s2_x.append(sss2_x)
			sss2_y = sss2.split(',')[1]
			s2_y.append(sss2_y)
	
		error+=max(0,len(ss2)-len(ss1))
		for k in range(len(ss1)):
			flag = 0
			num+=1
			for m in range(len(ss2)):
				delt_x = abs(  int(s1_x[k]) - int(s2_x[m])  )
				delt_y = abs(  int(s1_y[k]) - int(s2_y[m])  )
				print 'delt_x= '+str(delt_x)
				print 'delt_y= '+str(delt_y)
				if delt_x<40*x_percentage and delt_y<100*y_percentage:
					correct+=1
					flag = 1
					print 'kk= '+str(i)
			if flag ==0:
				error+=1
			flag=0

	else:
		ss1 = s1[1:]
		ss2 = s2[1:]
		s1_x=[]
		s1_y=[]
		s2_x=[]
		s2_y=[]
		for j in range(len(ss1)):
			num+=1

			sss1 = ss1[j].strip('(').strip(')')
			sss1_x = sss1.split(',')[0]
			# print sss1_x
			s1_x.append(sss1_x)

			sss1_y = sss1.split(',')[1]
			s1_y.append(sss1_y)

			sss2 = ss2[j].strip('(').strip(')')
			sss2_x = sss2.split(',')[0]
			s2_x.append(sss2_x)

			sss2_y = sss2.split(',')[1]
			s2_y.append(sss2_y)
	
		
		for k in range(len(ss1)):
			flag = 0
			for m in range(len(ss1)):
				delt_x = abs(  int(s1_x[k]) - int(s2_x[m])  )
				delt_y = abs(  int(s1_y[k]) - int(s2_y[m])  )
				print 'delt_x= '+str(delt_x)
				print 'delt_y= '+str(delt_y)
				if delt_x<40*x_percentage and delt_y<100*y_percentage:
					correct += 1
					flag = 1
					print 'kk= ' + str(i)
			if flag == 0:
				error += 1
			flag = 0
	# print ss1
	# print ss2
	# print s1_x
	# print s1_y
	# print s2_x
	# print s2_y
print correct
# print correct/num
print correct/(num+error*0.5)
