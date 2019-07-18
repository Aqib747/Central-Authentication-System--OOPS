import Main

# Set up a test user and permission
Main.authenticator.add_user("joe", "joepassword")
Main.authorizor.add_permissions("test program")
Main.authorizor.add_permissions("change program")
Main.authorizor.permit_user("test program", "joe")

class Editor:

    def __init__(self):
        self.username = None
        self.menu_map = {
                    "login" : self.login,
                    "test" : self.test,
                    "change": self.change,
                    "quit" : self.quit}

    def login(self):
        logged_in = False
        while not logged_in:
            username = input("Enter the Username : ")
            password = input("Enter the Password: ")

            try:
                logged_in = Main.authenticator.login(username, password)

            except Main.InvalidUsername:
                print("Soory the user does not exist")

            except Main.InvalidPassword:
                print("Sorry password is incorrect")

            else:
                self.username = username

    def is_permitted(self, permission):
        try:
            Main.authorizor.check_permission(permission, self.username)
        except Main.NotLoggedInError as e:
            print("{} is not logged in".format(e.username))
            return False
        except Main.NotPermittedError as e :
            print("{} cannot {} ".format(e.username, permission))
            return False
        else:
            return True

    def test(self):
        if self.is_permitted("test program"):
            print("Testing Program now.....")

    def change(self):
        if self.is_permitted("change program"):
            print("changing program noe...")

    def quit(self):
        raise SystemExit()

    def menu(self):
        try:
            answer = ""
            while True:
                print( """
Please enter a command:
\tlogin\tLogin
\ttest\tTest the program
\tchange\tChange the program
\tquit\tQuit
""")

                answer = input("enter a command: ").lower()
                try:
                    func =  self.menu_map[answer]
                except KeyError:
                    print("{} this is not an valid option".format(answer))

                else:
                    func()

        finally:
            print("Thanks for Testing Auth Module")

Editor().menu()
