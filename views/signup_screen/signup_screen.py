from flet import *
import requests

class SignUp(View):
    def __init__(self, route, page):
        super().__init__(route=route)
        self.scroll = ScrollMode.AUTO

        self.firstNameTextBox = TextField(
            label="الاسم الاول",
            border_radius=border_radius.all(22),
            border_color="#171335",
            text_style=TextStyle(size=15, font_family="ElMessiri"),
            label_style=TextStyle(size=14, font_family="ElMessiri"),
        )

        self.lastNameTextBox = TextField(
            label="الاسم الاخير",
            border_radius=border_radius.all(22),
            border_color="#171335",
            text_style=TextStyle(size=15, font_family="ElMessiri"),
            label_style=TextStyle(size=14, font_family="ElMessiri"),
        )

        self.userNameTextBox = TextField(
            label="اســـم المــستخدم",
            border_radius=border_radius.all(22),
            border_color="#171335",
            text_style=TextStyle(size=15, font_family="ElMessiri"),
            label_style=TextStyle(size=14, font_family="ElMessiri"),
        )

        self.genderOptionMenu = Dropdown(
            label="الجنس",
            width=100,
            options=[
                dropdown.Option(content=Text("ذكر"), text=1),
                dropdown.Option(content=Text("انثى"), text=2),
            ],
            label_style=TextStyle(
                size=13,
                weight=FontWeight.NORMAL,
                font_family="ElMessiri",
            ),
            border_radius=border_radius.all(22),
        )

        self.passwordTextBox = TextField(
            label="كــلمة المــرور",
            password=True,
            can_reveal_password=True,
            border_radius=border_radius.all(22),
            border_color="#171335",
            text_style=TextStyle(size=15, font_family="ElMessiri"),
            label_style=TextStyle(size=14, font_family="ElMessiri"),
        )

        self.rePasswordTextBox = TextField(
            label="تأكيد كــلمة المــرور",
            password=True,
            can_reveal_password=True,
            border_radius=border_radius.all(22),
            border_color="#171335",
            text_style=TextStyle(size=15, font_family="ElMessiri"),
            label_style=TextStyle(size=14, font_family="ElMessiri"),
        )

        self.content = self.SignUpUi()
        self.controls.append(self.content)

    def SignUpUi(self):
        self.scroll = ScrollMode.AUTO
        return ResponsiveRow(
            controls=[
                Row(
                    controls=[
                        IconButton(
                            icon=icons.ARROW_BACK, on_click=lambda x: self.page.go("/")
                        )
                    ],
                    expand=False,
                    alignment=MainAxisAlignment.START,
                ),
                Column(
                    controls=[
                        ResponsiveRow(
                            controls=[
                                Image(
                                    src="images/logo.png",
                                    fit=ImageFit.COVER,
                                    border_radius=border_radius.all(20.0),
                                    col={"xs": 10, "sm": 10, "md": 7, "lg": 5, "xl": 5},
                                ),
                            ],
                            expand=False,
                            alignment=MainAxisAlignment.CENTER,
                        ),
                        Container(height=5),
                        Text(
                            "وصلة",
                            size=30,
                            weight=FontWeight.BOLD,
                            font_family="ElMessiri",
                        ),
                        ResponsiveRow(
                            controls=[self.firstNameTextBox],
                        ),
                        Container(height=5),
                        ResponsiveRow(
                            controls=[self.lastNameTextBox],
                        ),
                        Container(height=5),
                        ResponsiveRow(
                            controls=[self.genderOptionMenu],
                        ),
                        Container(height=5),
                        self.userNameTextBox,
                        Container(height=5),
                        self.passwordTextBox,
                        Container(height=5),
                        self.rePasswordTextBox,
                        Container(height=20),
                        ResponsiveRow(
                            controls=[
                                ElevatedButton(
                                    "انــشاء حــساب",
                                    style=ButtonStyle(
                                        shape=RoundedRectangleBorder(radius=22),
                                        bgcolor="#171335",
                                        color="#ffffff",
                                        text_style=TextStyle(
                                            size=15,
                                            weight=FontWeight.BOLD,
                                            font_family="ElMessiri",
                                        ),
                                        padding=5,
                                    ),
                                    on_click=lambda e: self.SignUpEvent(),
                                ),
                            ]
                        ),
                    ],
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    alignment=MainAxisAlignment.CENTER,
                ),
            ],
            expand=True,
        )

    # Function to generate and return the loader UI (Progress Ring)
    def loaderUi(self):
        self.scroll = None
        return Column(
            controls=[
                Container(
                    content=ProgressRing(visible=True),  # Progress ring loader
                    alignment=alignment.center,
                    height=float("inf"),  # Make the container take full height
                    expand=True,  # Ensure the container expands to fill available space
                ),
            ],
            expand=True,  # Make the column expand to take up all available space
        )

    def checkTextBoxData(self):
        errors = [
            True if self.firstNameTextBox.value != "" else "الرجاء ادخال اسمك الاول",
            True if self.lastNameTextBox.value != "" else "الرجاء ادخال اسمك الاخير",
            True if self.genderOptionMenu.value != None else "الرجاء اختيار الجس",
            (
                True
                if len(self.userNameTextBox.value) > 2
                and self.userNameTextBox.value != ""
                else "يجب ان يتكون اسم المستخدم من 3 احرف على الاقل"
            ),
            (
                True
                if len(self.passwordTextBox.value) > 5
                and self.passwordTextBox.value != ""
                else "يجب ان تتكون كلمة المرور  من 6 احرف على الاقل"
            ),
            (
                True
                if self.rePasswordTextBox.value != ""
                else "الرجاء ادخال تاكيد كلمة المرور"
            ),
            (
                True
                if self.passwordTextBox.value == self.rePasswordTextBox.value
                else "كلمة المرور غير متطابقة"
            ),
        ]

        textBoxes = [
            self.firstNameTextBox,
            self.lastNameTextBox,
            self.genderOptionMenu,
            self.userNameTextBox,
            self.passwordTextBox,
            self.rePasswordTextBox,
            self.rePasswordTextBox,
        ]
        state = True
        for index, error in enumerate(errors):
            if error != True:
                state = False
                textBoxes[index].error = Text(f"{error}")
            else:
                textBoxes[index].error = None
        self.update()
        textBoxes.pop()
        return [[text.value for text in textBoxes], state]

    async def SignUpRequest(self, data):
        body = {
            "first_name": data[0],
            "last_name": data[1],
            "gender": data[2],
            "username": data[3],
            "password": data[4],
            "userType": 0,
        }
        try:
            response = requests.post(url=f"{SignUp.baseUrl}/signup/", data=body)
            json = response.json()
            if response.status_code == 200:
                await self.page.client_storage.set_async("access", json["access"])
                await self.page.client_storage.set_async("refresh", json["refresh"])
                userData = {
                    "username":json["username"],
                    "gender":json["gender"],
                    "first_name":json["first_name"],
                    "last_name":json["last_name"],
                    "profileImage":json["profileImage"],
                }
                await self.page.client_storage.set_async("userData", userData)
                return [True, "تم تسجيل الدخول بنجاح"]
            else:
                return [False, json["username"][0]]
        except requests.exceptions.Timeout:
            return [False, "اتصال الانترنت بطئ"]
        except requests.exceptions.ConnectionError:
            return [False, "حدث خطأ في الاتصال بالخادم. تحقق من اتصالك بالإنترنت."]

    def SignUpEvent(self):
        data, state = self.checkTextBoxData()
        if state:
            self.controls.clear()  # Clear the current controls from the view
            self.controls.append(self.loaderUi())  # Add the loader UI to show progress
            self.update()
            authState = self.page.run_task(self.SignUpRequest , data).result()
            if authState[
                0
            ]:  # If authentication is successful, navigate to the home page
                self.page.go("/home")
            else:
                self.controls.clear()  # Clear the controls again
                self.controls.append(self.SignUpUi())  # Add the login form UI back
                snack_bar = SnackBar(
                    content=Text(
                        f"{authState[1]}",
                        style=TextStyle(size=15, font_family="ElMessiri"),
                    ),
                    show_close_icon=True,
                )
                self.page.open(snack_bar)
                self.update()  # Update the view to reflect the changes
