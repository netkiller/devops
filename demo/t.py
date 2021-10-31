class Human:
    def __init__(self,n,a):
        self.name = n
        self.age = a
        print("Human种的init函数被调用")

    def show_info(self):
        print("姓名:",self.name)
        print("年龄:",self.age)

class Student(Human):
    def __init__(self,n,a,s = 0):
        super().__init__(n,a)   #显式调用父类的初始化方法
        #super(Human,self)._init_(n,a)  #也可以这样显式的调用
        self.score = s
        print("Student中的init函数被调用")
    class ss(Human):
        def __init__(self,n,a):
            super().__init__(n,a) 
            Student.score = 1000
    def show_info(self):
        super().show_info() 
        print("成绩为：",self.score)
    def test(self):
        print(self.name)

student = Student('neo','25')

student.show_info()

student1 = Student('jam','27')
student1.show_info()

student.ss('netkiller','30').show_info()
student.show_info()
#.name='netkiller'
student.test()