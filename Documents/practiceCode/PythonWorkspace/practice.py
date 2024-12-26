# from random import *

# print(int(random()*45)+1)
# print(int(random()*45)+1)
# print(int(random()*45)+1)
# print(int(random()*45)+1)
# print(int(random()*45)+1)
# print(int(random()*45)+1)

# print(randrange(1, 46))
# print(randint(1,100))


# offLineDay = randint(4,28)
# print("오프라인 스터디 모임 날짜는 매월",offLineDay,"일로 선정되었습니다.")

# sent = """hola me llamo joohee. como estas. 
# hohoho pelis navidad"""

# print(sent)

# jumin = "940406-1234567"
# print("sex:",jumin[7])
# print("year:",jumin[0:2])
# print("month:",jumin[2:4])
# print("day:",jumin[4:6])
# print("birth:",jumin[:6])
# print("birth:",jumin[7:])
# print("birth:",jumin[-7:])
# print(len(jumin))

# python = "Python is Amazing"
# print(python.lower())
# print(python.upper())
# print(python.capitalize())
# print(python.title())
# print(python.replace("Python", "Java"))
# print(python.find("Amazing"))
# index = python.index('n')
# print(index)
# index = python.index('n', index+1)
# print(index)

# print("i am %d years old" %20)
# print("i am %s years old" %"twenty")
# print("i am %f years old" %20.5)
# print("i am %s years old" %20.5)
# print('Apple starts %c' %'A')
# print('i like %s color and %s color and %d number and %s animal' %('blue','yellow', 20, 'dog'))
# print('i like {3} color and {2} color and {1} number and {0} animal' .format('blue','yellow', 20, 'dog'))
# print('i like {color} color and {number} number' .format(color='blue', number = 20))

# text='yellow'
# num=30
# print(f'i like {text} color and {num} number')

# from random import *
# users = range(1, 21)
# print(type(users))
# users = list(users)
# print(type(users))
# print(users)
# shuffle(users)
# print(users)
# winners = sample(users, 4)
# print(winners)
# print("win1 : {0}".format(winners[0]))
# print("win2,3,4 : {0}".format(winners[1:]))


# weather = input("오늘 날씨는? ")
# if weather == "비" or weather == "눈":
#     print("비가 내리고 있습니다.")
# elif weather == "안개":
#     print("안개가 내리고 있습니다.")
# else:
#     print("아무것도 필요없어요")

# for num in range(1,6):
#     print("waiting...",format(num))

# customer = 'thor'
# index = 5
# while index >= 1:
#   print('{0}, ready for coffee. last {1}'.format(customer, index))
#   index -= 1
#   if(index==0):
#     print("coffee is discarded")

# people = ["kim", "joohee", "new man"]
# people = [len(i) for i in people]
# print(people)

# from random import *

# boardCustomer = 0
# num = 1
# while num <=50:
#   driveTime = randint(5, 50)
#   title = '['
#   if 5 <= driveTime <= 15:
#     title += 'O'
#     boardCustomer += 1
#   else:
#     title += ' '
#   title += '] {0}번째 손님 (소요시간 : {1}분)'.format(num, driveTime)
#   print(title)
#   num += 1
  
# print('총 탑승 승객 : {0}분'.format(boardCustomer))



# def open():
#   print("open door")


# def deposit(balance, money):
#   print("입금완료. 잔액은 {0}".format(balance+money))
#   return balance + money

# balance = 0
# balance = deposit(balance, 1000)
# print(balance)

#가변인자
# def profile(*language, name):
#   print("name : {0}\t".format(name), end=" ")
#   for lang in language:
#     print(lang, end=" / ")
#   print()
# profile("java", "python", "c", "c++", "js", "kotlin",name="woolfie")
# profile(name="kim")

# scores = {"math":0, "english": 50, "code": 100}
# for subject, score in scores.items():
#   # print(subject, score)
#   print(subject.ljust(8), str(score).rjust(7), sep=":")

# for num in range(1,21):
#   print("waiting... : " + str(num).zfill(4))

# print("{0: >10}".format(500))
# print("{0: >+10}".format(500))
# print("{0: >+10}".format(-500))
# print("{0: >-10}".format(500))
# print("{0:_<10}".format(500))
# print("{0:,}".format(100000000))
# print("{0:+,}".format(100000000))
# print("{0:,}".format(-100000000))
# print("{0:+,}".format(-100000000))
# print("{0:^<+30,}".format(100000000))
# print("{0:f}".format(5/3))
# print("{0:.2f}".format(5/3))

# score_file = open("score.txt", "w", encoding="utf8")
# print("math:0", file=score_file)
# print("english:50", file=score_file) 
# score_file.close()

# score_file = open("score.txt", "a", encoding="utf8")
# score_file.write("science:80")
# score_file.write("\ncoding:100")
# score_file.close()

# score_file = open("score.txt", "a", encoding="utf8")
# score_file.write("science:80")
# score_file.write("\ncoding:100")
# score_file.close()

# score_file = open("score.txt", "r", encoding="utf8")
# print(score_file.read())
# score_file.close()

# score_file = open("score.txt", "r", encoding="utf8")
# print(score_file.readline(), end="")
# print(score_file.readline(), end="")
# print(score_file.readline(), end="")
# print(score_file.readline(), end="")
# score_file.close()

# score_file = open("score.txt", "r", encoding="utf8")
# while True:
#   line = score_file.readline()
#   if not line:
#     break
#   print(line, end="")
# score_file.close()
# lines = score_file.readlines()
# for line in lines:
#   print(line, end="")
# score_file.close()

# import pickle
# profile_file = open("profile.pickle", "wb")
# profile = {"name": "woolfie", "age": 28, "city": "seoul", "hobby": ["soccer", "golf", "coding"]}
# print(profile)
# pickle.dump(profile, profile_file)
# profile_file.close()

# profile_file = open("profile.pickle", "rb")
# profile = pickle.load(profile_file)
# print(profile)
# profile_file.close()

# import pickle
# with open("profile.pickle", "rb") as profile_file:
#   print(pickle.load(profile_file))

# with open("study.txt", "w", encoding="utf8") as study_file:
#   study_file.write("Python\n")
#   study_file.write("Java\n")
#   study_file.write("JavaScript\n")  

# with open("{0}study.txt".format("hard"), "w", encoding="utf8") as study_file:
#   study_file.write("Python\n")
#   study_file.write("Java\n")
#   study_file.write("JavaScript\n")

# with open("study.txt", "r", encoding="utf8") as study_file:
#   print(study_file.read())

# for num in range(1,51):
#   with open("{0}주차.txt".format(num), "w", encoding="utf8") as report_file:
#   with open(str(i)+"주차.txt", "w", encoding="utf8") as report_file:
#     report_file.write("- {0}주차 주간보고 -\n".format(num))
#     report_file.write("부서 : \n")
#     report_file.write("이름 : \n")
#     report_file.write("업무 요약 : \n")



