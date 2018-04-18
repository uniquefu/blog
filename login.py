class Login():
    def __init__(self):
        self.db ={'u':'p'}
        self.showmenu()

    def showmenu(self):
        menu ='''
        (N)ew User Login
        (E)xisting User Login
        (D)elete User
        (S)howusers
        (Q)uit
        '''
        menu_dic = {
            'n': 'newuser',
            'e': 'olduser',
            'd': 'deluser',
            's':'showusers',
            'q': 'quit',
        }
        while True:
            print(menu)
            choice = input("请输入你的选项：").strip()
            choice=choice.lower()

            if choice in menu_dic:
                if hasattr(self,menu_dic[choice]):
                    obj = getattr(self,menu_dic[choice])
                    obj()

                else:
                    print('未定义此方法')

            else:

                print('\033[31;1m非法选项，请重新输入\033[0m')

    def newuser(self):


        while True:
            user = input('请输入用户名：').strip()
            user=user.lower()

            if user in self.db.keys():
                print ("用户名已存在，请重新输入")
                continue
            else:
                break

        pwd = input('请输入密码：').strip()
        self.db[user]=pwd


    def deluser(self):

        while True:
            user = input('请输入用户名：').strip()
            if user not in self.db.keys():
                print ("用户名不存在，请重新输入")
                continue
            else:
                print("删除用户成功")
                del self.db[user]
                break

    def olduser(self):
        while True:
            user = input('请输入用户名：').strip()
            pwd = input('请输入用户名：').strip()

            user = user.lower()

            passwd = self.db.get(user)

            if passwd == pwd:
                print ('登录成功')
                break

            else:
                print('用户名或密码错误，请重新输入')


    def showusers(self):
        u = "用户名".center(20,' ')
        p = "密码".center(20, ' ')
        print(u,p)
        for k,v in self.db.items():
            print(k.center(20,' '),v.center(20, ' '))

    def quit(self):
        exit('退出系统')



if __name__ == '__main__':
    u = Login()