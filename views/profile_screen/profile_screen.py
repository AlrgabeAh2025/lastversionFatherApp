from flet import *
import requests


class PersonalInformation(View):

    def __init__(self, route, page):
        super().__init__(route=route)
        self.scroll = ScrollMode.AUTO
        self.page = page

        self.appbar = AppBar(
            leading=IconButton(
                icon=icons.ARROW_BACK,
                icon_color="#ffffff",
                on_click=lambda x: self.page.go("/Profile"),
            ),
            title=Text(
                "وصلة",
                size=30,
                weight=FontWeight.BOLD,
                color="#ffffff",
                font_family="ElMessiri",
            ),
            toolbar_height=100,
        )

        self.userName = Ref[TextField]()
        self.firstName = Ref[TextField]()
        self.lastName = Ref[TextField]()

    def buildUi(self):
        self.controls.clear()
        userData = self.page.client_storage.get("userData")
        self.controls.append(
            ResponsiveRow(
                controls=[
                    Column(
                        controls=[
                            Container(
                                content=Image(
                                    src=f"{PersonalInformation.baseUrl}{userData['profileImage']}",
                                    width=250,
                                ),
                                border_radius=border_radius.all(150),
                                width=200,
                                height=200,
                                border=border.all(width=0.5, color="black"),
                            ),
                            Container(height=20),
                            ResponsiveRow(
                                controls=[
                                    Text(
                                        "تعديل المعلومات الشخصية",
                                        style=TextStyle(
                                            size=12,
                                            weight=FontWeight.BOLD,
                                            font_family="ElMessiri",
                                        ),
                                        color="#666666",
                                        text_align=TextAlign.START,
                                    ),
                                ],
                            ),
                            Container(height=10),
                            ResponsiveRow(
                                controls=[
                                    TextField(
                                        label="اسم المستخدم",
                                        border_radius=border_radius.all(22),
                                        border_color="#171335",
                                        text_style=TextStyle(
                                            size=15, font_family="ElMessiri"
                                        ),
                                        label_style=TextStyle(
                                            size=14, font_family="ElMessiri"
                                        ),
                                        ref=self.userName,
                                        value=userData["username"],
                                    ),
                                ],
                            ),
                            Container(height=10),
                            ResponsiveRow(
                                controls=[
                                    TextField(
                                        label="الاسم الاول",
                                        border_radius=border_radius.all(22),
                                        border_color="#171335",
                                        text_style=TextStyle(
                                            size=15, font_family="ElMessiri"
                                        ),
                                        label_style=TextStyle(
                                            size=14, font_family="ElMessiri"
                                        ),
                                        ref=self.firstName,
                                        value=userData["first_name"],
                                    ),
                                ],
                            ),
                            Container(height=10),
                            ResponsiveRow(
                                controls=[
                                    TextField(
                                        label="الاسم الاخير",
                                        border_radius=border_radius.all(22),
                                        border_color="#171335",
                                        text_style=TextStyle(
                                            size=15, font_family="ElMessiri"
                                        ),
                                        label_style=TextStyle(
                                            size=14, font_family="ElMessiri"
                                        ),
                                        ref=self.lastName,
                                        value=userData["last_name"],
                                    ),
                                ],
                            ),
                            Container(height=10),
                            ResponsiveRow(
                                controls=[
                                    ElevatedButton(
                                        "حفظ التعديلات",
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
                                        on_click=self.changeData,
                                    ),
                                ]
                            ),
                        ],
                        horizontal_alignment=CrossAxisAlignment.CENTER,
                        alignment=MainAxisAlignment.CENTER,
                    )
                ],
                vertical_alignment=CrossAxisAlignment.CENTER,
                alignment=alignment.center,
            ),
        )
        self.update()

    def did_mount(self):
        self.buildUi()

    async def sendPatchRequest(self, url, body={}):
        body = {
            "action": "updatePersonaInfo",
            "username": f"{body[0]}",
            "first_name": f"{body[1]}",
            "last_name": f"{body[2]}",
        }
        access = await self.page.client_storage.get_async("access")
        headers = {
            "Authorization": f"Bearer {access}",
            "Accept": "*/*",
            "Cache-Control": "no-cache",
        }
        try:
            response = requests.patch(
                url=f"{PersonalInformation.baseUrl}/{url}/", data=body, headers=headers
            )
            json = response.json()
            if response.status_code == 200:
                return [True, json]
            else:
                return [False, json]
        except requests.exceptions.Timeout:
            return [False, "اتصال الانترنت بطئ"]
        except requests.exceptions.ConnectionError:
            return [False, "حدث خطأ في الاتصال بالخادم. تحقق من اتصالك بالإنترنت."]

    def ErrorUi(self):
        self.scroll = None
        self.controls.clear()
        self.controls.append(
            Column(
                controls=[
                    Container(
                        content=Text(
                            "حدث خطأ الرجاء اعادة المحاولة",
                            style=TextStyle(
                                size=15,
                                weight=FontWeight.BOLD,
                                font_family="ElMessiri",
                            ),
                        ),  # Progress ring loader
                        alignment=alignment.center,
                        expand=True,  # Ensure the container expands to fill available space
                    ),
                    Container(
                        content=TextButton(
                            icon=icons.REPLAY_OUTLINED,
                            text="اعادة المحاولة",
                            style=ButtonStyle(
                                text_style=TextStyle(
                                    size=15,
                                    weight=FontWeight.BOLD,
                                    font_family="ElMessiri",
                                ),
                            ),
                            on_click=lambda e: self.did_mount(),
                        ),  # Progress ring loader
                        alignment=alignment.center,
                    ),
                ],
                expand=True,  # Make the column expand to take up all available space
            )
        )
        self.update()

    def loaderUi(self):
        self.scroll = None
        self.controls.clear()
        self.controls.append(
            Column(
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
        )
        self.update()

    def checkTextBoxData(self):
        errors = [
            True if self.userName.current.value != "" else "الرجاء ادخال اسم المستخدم",
            True if self.firstName.current.value != "" else "الرجاء ادخال اسمك الاول",
            True if self.lastName.current.value != "" else "الرجاء ادخال اسمك الاخير",
            (
                True
                if len(self.userName.current.value) > 2 and self.userName.current.value != ""
                else "يجب ان يتكون اسم المستخدم من 3 احرف على الاقل"
            ),
        ]
        textBoxes = [
            self.userName,
            self.firstName,
            self.lastName,
            self.userName,
        ]
        state = True
        for index, error in enumerate(errors):
            if error != True:
                state = False
                textBoxes[index].current.error = Text(f"{error}")
            else:
                textBoxes[index].current.error = None
        self.update()
        textBoxes.pop()
        return [[text.current.value for text in textBoxes], state]

    def showMessage(self , message):
        snack_bar = SnackBar(
                    content=Text(
                        f"{message}",
                        style=TextStyle(size=15, font_family="ElMessiri"),
                    ),
                    show_close_icon=True,
                )
        self.page.open(snack_bar)

    def updateUserData(self , result):
        userData = {
                    "username":result["username"],
                    "gender":result["gender"],
                    "first_name":result["first_name"],
                    "last_name":result["last_name"],
                    "profileImage":result["profileImage"],
                }
        self.page.client_storage.set("userData", userData)

    def changeData(self, e):
        values, textBoxState = self.checkTextBoxData()
        if textBoxState:
            self.loaderUi()
            state, result = self.page.run_task(
                self.sendPatchRequest, "updateUser", values
            ).result()
            if state:
                self.updateUserData(result)
                self.showMessage("تم تحديث البيانات بنجاح")
                self.did_mount()
            else:
                self.did_mount()
                self.showMessage(result)

class SecurityPasswords(View):
    def __init__(self, route, page):
        super().__init__(route=route)
        self.scroll = ScrollMode.AUTO
        self.page = page

        self.appbar = AppBar(
            leading=IconButton(
                icon=icons.ARROW_BACK,
                icon_color="#ffffff",
                on_click=lambda x: self.page.go("/Profile"),
            ),
            title=Text(
                "وصلة",
                size=30,
                weight=FontWeight.BOLD,
                color="#ffffff",
                font_family="ElMessiri",
            ),
            toolbar_height=100,
        )

        self.currentPassword = Ref[TextField]()
        self.newPassword = Ref[TextField]()
        self.newRePassword = Ref[TextField]()

    def buildUi(self):  
        self.controls.clear()
        self.controls.append(
            ResponsiveRow(
                controls=[
                    Column(
                        controls=[
                            Container(height=10),
                            ResponsiveRow(
                                controls=[
                                    Text(
                                        "تغيير كلمة مرور حسابك",
                                        style=TextStyle(
                                            size=12,
                                            weight=FontWeight.BOLD,
                                            font_family="ElMessiri",
                                        ),
                                        color="#666666",
                                        text_align=TextAlign.START,
                                    ),
                                ],
                            ),
                            Container(height=10),
                            ResponsiveRow(
                                controls=[
                                    TextField(
                                        label="كلمة المرور الحالية",
                                        border_radius=border_radius.all(22),
                                        border_color="#171335",
                                        text_style=TextStyle(
                                            size=15, font_family="ElMessiri"
                                        ),
                                        label_style=TextStyle(
                                            size=14, font_family="ElMessiri"
                                        ),
                                        password=True,
                                        can_reveal_password=True,
                                        ref=self.currentPassword
                                    ),
                                ],
                            ),
                            Container(height=10),
                            ResponsiveRow(
                                controls=[
                                    TextField(
                                        label="كلمة المرور الجديدة",
                                        border_radius=border_radius.all(22),
                                        border_color="#171335",
                                        text_style=TextStyle(
                                            size=15, font_family="ElMessiri"
                                        ),
                                        label_style=TextStyle(
                                            size=14, font_family="ElMessiri"
                                        ),
                                        password=True,
                                        can_reveal_password=True,
                                        ref=self.newPassword
                                    ),
                                ],
                            ),
                            Container(height=10),
                            ResponsiveRow(
                                controls=[
                                    TextField(
                                        label="تأكيد كلمة المرور الحديدة",
                                        border_radius=border_radius.all(22),
                                        border_color="#171335",
                                        text_style=TextStyle(
                                            size=15, font_family="ElMessiri"
                                        ),
                                        label_style=TextStyle(
                                            size=14, font_family="ElMessiri"
                                        ),
                                        password=True,
                                        can_reveal_password=True,
                                        ref=self.newRePassword
                                    ),
                                ],
                            ),
                            Container(height=10),
                            ResponsiveRow(
                                controls=[
                                    ElevatedButton(
                                        "حفظ التعديلات",
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
                                        on_click=self.updatePassword
                                    ),
                                ]
                            ),
                        ],
                        horizontal_alignment=CrossAxisAlignment.CENTER,
                        alignment=MainAxisAlignment.CENTER,
                    )
                ],
                vertical_alignment=CrossAxisAlignment.CENTER,
                alignment=alignment.center,
            ),
        )
        self.update()

    def did_mount(self):
        self.buildUi()

    async def sendPatchRequest(self, url, body={}):
        body = {
            "action": "updatePassword",
            "currentPassword": f"{body[0]}",
            "newPassword": f"{body[1]}",
            "rePassword": f"{body[2]}",
        }
        access = await self.page.client_storage.get_async("access")
        headers = {
            "Authorization": f"Bearer {access}",
            "Accept": "*/*",
            "Cache-Control": "no-cache",
        }
        try:
            response = requests.patch(
                url=f"{SecurityPasswords.baseUrl}/{url}/", data=body, headers=headers
            )
            json = response.json()
            if response.status_code == 200:
                return [True, json]
            else:
                return [False, json]
        except requests.exceptions.Timeout:
            return [False, "اتصال الانترنت بطئ"]
        except requests.exceptions.ConnectionError:
            return [False, "حدث خطأ في الاتصال بالخادم. تحقق من اتصالك بالإنترنت."]

    def ErrorUi(self):
        self.scroll = None
        self.controls.clear()
        self.controls.append(
            Column(
                controls=[
                    Container(
                        content=Text(
                            "حدث خطأ الرجاء اعادة المحاولة",
                            style=TextStyle(
                                size=15,
                                weight=FontWeight.BOLD,
                                font_family="ElMessiri",
                            ),
                        ),  # Progress ring loader
                        alignment=alignment.center,
                        expand=True,  # Ensure the container expands to fill available space
                    ),
                    Container(
                        content=TextButton(
                            icon=icons.REPLAY_OUTLINED,
                            text="اعادة المحاولة",
                            style=ButtonStyle(
                                text_style=TextStyle(
                                    size=15,
                                    weight=FontWeight.BOLD,
                                    font_family="ElMessiri",
                                ),
                            ),
                            on_click=lambda e: self.did_mount(),
                        ),  # Progress ring loader
                        alignment=alignment.center,
                    ),
                ],
                expand=True,  # Make the column expand to take up all available space
            )
        )
        self.update()

    def loaderUi(self):
        self.scroll = None
        self.controls.clear()
        self.controls.append(
            Column(
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
        )
        self.update()

    def checkTextBoxData(self):
        errors = [
            True if self.currentPassword.current.value != "" else "الرجاء ادخال كلمة السر الحالية",
            True if self.newPassword.current.value != "" else "الرجاء ادخال كلمةالسر الجديدة ",
            True if self.newRePassword.current.value != "" else "الرجاء ادخال  تأكيد كلمة المرور الجديدة",
            (
                True
                if self.newPassword.current.value == self.newRePassword.current.value 
                else "كلمة المرور غير متطابقة"
            ),
        ]
        textBoxes = [
            self.currentPassword,
            self.newPassword,
            self.newRePassword,
            self.newRePassword,
        ]
        state = True
        for index, error in enumerate(errors):
            if error != True:
                state = False
                textBoxes[index].current.error = Text(f"{error}")
            else:
                textBoxes[index].current.error = None
        self.update()
        textBoxes.pop()
        return [[text.current.value for text in textBoxes], state]

    def showMessage(self , message):
        snack_bar = SnackBar(
                    content=Text(
                        f"{message}",
                        style=TextStyle(size=15, font_family="ElMessiri"),
                    ),
                    show_close_icon=True,
                )
        self.page.open(snack_bar)

    def updateUserData(self , result):
        userData = {
                    "username":result["username"],
                    "gender":result["gender"],
                    "first_name":result["first_name"],
                    "last_name":result["last_name"],
                    "profileImage":result["profileImage"],
                }
        self.page.client_storage.set("userData", userData)

    def updatePassword(self, e):
        values, textBoxState = self.checkTextBoxData()
        if textBoxState:
            self.loaderUi()
            state, result = self.page.run_task(
                self.sendPatchRequest, "updateUser", values
            ).result()
            if state:
                self.updateUserData(result)
                self.showMessage("تم تحديث كلمة المرور بنجاح")
                self.did_mount()
            else:
                self.did_mount()
                self.showMessage(result["password"])

class Profile(View):
    def __init__(self, route, page):
        super().__init__(route=route)
        self.page = page
        self.scroll = ScrollMode.AUTO

        self.selector = FilePicker(on_result=self.ChangeProfileImage)
        self.page.overlay.append(self.selector)

        self.BottomSheet = BottomSheet(
            content=Container(
                content=Column(
                    tight=True,
                    controls=[
                        TextButton(
                            text="تغيير صورة الملف الشخصي",
                            icon=icons.ADD_A_PHOTO,
                            on_click=lambda _: self.selector.pick_files(
                                allow_multiple=False,
                                allowed_extensions=["jpg", "jpeg", "png"],
                                dialog_title="اختيار صورة ملف شخصي",
                                file_type=FilePickerFileType.IMAGE,
                            ),
                            width=float("inf"),
                        ),
                    ],
                ),
                width=float("inf"),
                padding=20,
            ),
        )

        self.appbar = AppBar(
            leading=IconButton(
                icon=icons.ARROW_BACK,
                icon_color="#ffffff",
                on_click=lambda x: self.page.go("/home"),
            ),
            title=Text(
                "وصلة",
                size=30,
                weight=FontWeight.BOLD,
                color="#ffffff",
                font_family="ElMessiri",
            ),
            toolbar_height=100,
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

    def did_mount(self):
        self.controls.clear()
        loader = self.loaderUi()
        self.controls.append(loader)
        self.buildUi()

    def buildUi(self):
        self.controls.clear()
        userData = self.page.run_task(
            self.page.client_storage.get_async, "userData"
        ).result()
        self.controls.append(
            ResponsiveRow(
                controls=[
                    Container(height=10),
                    Column(
                        controls=[
                            Container(
                                content=Image(
                                    src=f"{Profile.baseUrl}{userData['profileImage']}",
                                    width=250,
                                ),
                                border_radius=border_radius.all(150),
                                on_click=lambda e: self.page.open(self.BottomSheet),
                                width=200,
                                height=200,
                                border=border.all(width=0.5, color="black"),
                            ),
                            Container(
                                content=Text(
                                    f"{userData['first_name']} {userData['last_name']}",
                                    size=20,
                                    weight=FontWeight.BOLD,
                                    color="#666666",
                                    font_family="ElMessiri",
                                ),
                            ),
                            Container(height=30),
                            Column(
                                controls=[
                                    ResponsiveRow(
                                        controls=[
                                            Container(
                                                content=ListTile(
                                                    title=Text(
                                                        "البيانات الشخصية",
                                                        style=TextStyle(
                                                            size=15,
                                                            weight=FontWeight.BOLD,
                                                            font_family="ElMessiri",
                                                        ),
                                                    ),
                                                    trailing=IconButton(
                                                        icon=icons.PERSON,
                                                    ),
                                                ),
                                                bgcolor="#ffffff",
                                                border=border.all(0.5, "#110b22"),
                                                border_radius=border_radius.all(5),
                                                on_click=lambda x: self.page.go(
                                                    "/PersonalInformation"
                                                ),
                                            ),
                                        ],
                                    ),
                                    ResponsiveRow(
                                        controls=[
                                            Container(
                                                content=ListTile(
                                                    title=Text(
                                                        "الامان وكلمة المرور",
                                                        style=TextStyle(
                                                            size=15,
                                                            weight=FontWeight.BOLD,
                                                            font_family="ElMessiri",
                                                        ),
                                                    ),
                                                    trailing=IconButton(
                                                        icon=icons.LOCK,
                                                    ),
                                                ),
                                                bgcolor="#ffffff",
                                                border=border.all(0.5, "#110b22"),
                                                border_radius=border_radius.all(5),
                                                on_click=lambda x: self.page.go(
                                                    "/SecurityPasswords"
                                                ),
                                            ),
                                        ],
                                    ),
                                    ResponsiveRow(
                                        controls=[
                                            Container(
                                                content=ListTile(
                                                    title=Text(
                                                        "تسجيل الخروج",
                                                        style=TextStyle(
                                                            size=15,
                                                            weight=FontWeight.BOLD,
                                                            font_family="ElMessiri",
                                                        ),
                                                    ),
                                                    trailing=IconButton(
                                                        icon=icons.LOGOUT,
                                                    ),
                                                ),
                                                bgcolor="#ffffff",
                                                border=border.all(0.5, "#110b22"),
                                                border_radius=border_radius.all(5),
                                                on_click=lambda e: self.logOut(),
                                            ),
                                        ],
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
        )
        self.update()

    def logOut(self):
        self.page.client_storage.clear()
        self.page.go("/")

    async def sendPutRequest(self, url, files={}):
        access = await self.page.client_storage.get_async("access")
        headers = {
            "Authorization": f"Bearer {access}",
            "Accept": "*/*",
            "Cache-Control": "no-cache",
        }
        try:
            response = requests.put(
                url=f"{Profile.baseUrl}/{url}/", files=files, headers=headers
            )
            json = response.json()
            if response.status_code == 200:
                userData = {
                    "username": json["username"],
                    "gender": json["gender"],
                    "first_name": json["first_name"],
                    "last_name": json["last_name"],
                    "profileImage": json["profileImage"],
                }
                await self.page.client_storage.set_async("userData", userData)
                return [True, json]
            else:
                return [False, json]
        except requests.exceptions.Timeout:
            return [False, "اتصال الانترنت بطئ"]
        except requests.exceptions.ConnectionError:
            return [False, "حدث خطأ في الاتصال بالخادم. تحقق من اتصالك بالإنترنت."]

    def ErrorUi(self):
        self.scroll = None
        self.controls.clear()
        self.controls.append(
            Column(
                controls=[
                    Container(
                        content=Text(
                            "حدث خطأ الرجاء اعادة المحاولة",
                            style=TextStyle(
                                size=15,
                                weight=FontWeight.BOLD,
                                font_family="ElMessiri",
                            ),
                        ),  # Progress ring loader
                        alignment=alignment.center,
                        expand=True,  # Ensure the container expands to fill available space
                    ),
                    Container(
                        content=TextButton(
                            icon=icons.REPLAY_OUTLINED,
                            text="اعادة المحاولة",
                            style=ButtonStyle(
                                text_style=TextStyle(
                                    size=15,
                                    weight=FontWeight.BOLD,
                                    font_family="ElMessiri",
                                ),
                            ),
                            on_click=lambda e: self.did_mount(),
                        ),  # Progress ring loader
                        alignment=alignment.center,
                    ),
                ],
                expand=True,  # Make the column expand to take up all available space
            )
        )
        self.update()

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

    def ChangeProfileImage(self, e):
        self.page.close(self.BottomSheet)
        if e.files:
            self.controls.clear()
            loader = self.loaderUi()
            self.controls.append(loader)
            self.update()
            files = {
                "Image": ("image.jpg", open(f"{e.files[0].path}", "rb"), "image/jpeg"),
            }
            state, result = self.page.run_task(
                self.sendPutRequest, "uploadProfileImage", files
            ).result()
            if state:
                self.did_mount()
            else:
                self.ErrorUi()
