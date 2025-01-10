from flet import *
import requests


class Devices(View):
    def __init__(self, route, page):
        super().__init__(route=route)
        self.scroll = ScrollMode.AUTO
        self.page = page
        self.baseUrl = "http://127.0.0.1:8000"
        self.devices = []
        self.keyTextbox = Ref[TextField]()

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

    def did_mount(self):
        self.loaderUi()
        self.getDevices()

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

    def buildUi(self):
        self.controls.clear()
        self.controls.append(
            ResponsiveRow(
                controls=[
                    Container(height=10),
                    Column(
                        controls=[
                            ResponsiveRow(
                                controls=[
                                    Text(
                                        "اضافة المزيد الاجهزة",
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
                            ResponsiveRow(
                                controls=[
                                    Container(
                                        content=ListTile(
                                            title=TextField(
                                                label="ادخل المفتاح الذي نسخته من هاتف الابن",
                                                text_style=TextStyle(
                                                    size=15, font_family="ElMessiri"
                                                ),
                                                label_style=TextStyle(
                                                    size=12, font_family="ElMessiri"
                                                ),
                                                ref=self.keyTextbox,
                                                border=None,
                                                border_width=0,
                                            ),
                                            trailing=IconButton(
                                                icon=icons.SEND,
                                                on_click=self.addNewChild,
                                                icon_size=15,
                                            ),
                                        ),
                                        bgcolor="#ffffff",
                                        border=border.all(0.5, "#110b22"),
                                        border_radius=border_radius.all(5),
                                    ),
                                ],
                            ),
                            Container(height=30),
                            ResponsiveRow(
                                controls=[
                                    Text(
                                        "الاجهزة التي اضفتها سابقا",
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
                            Column(
                                controls=(
                                    self.devices
                                    if len(self.devices) > 0
                                    else [
                                        Container(
                                            content=Text(
                                                "لا يوجد اجهزة  بعد",
                                                style=TextStyle(
                                                    size=12,
                                                    weight=FontWeight.BOLD,
                                                    font_family="ElMessiri",
                                                ),
                                                color="#666666",
                                                text_align=TextAlign.START,
                                            ),
                                            padding=20,
                                        )
                                    ]
                                )
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

    def showMessage(self, message):
        snack_bar = SnackBar(
            content=Text(
                f"{message}",
                style=TextStyle(size=15, font_family="ElMessiri"),
            ),
            show_close_icon=True,
        )
        self.page.open(snack_bar)

    def deleteUser(self, e):
        self.loaderUi()
        if e.control.data:
            _, result = self.page.run_task(
                self.sendDeleteRequest, "Children", {"key": e.control.data}
            ).result()
            self.did_mount()
            self.showMessage(f"{result['key']}")

    def checkTextBoxData(self):
        if not self.keyTextbox.current.value:
            self.keyTextbox.current.error = Text(
                f"الرجاء ادخال  المفتاح اولا",
                style=TextStyle(size=10, font_family="ElMessiri"),
            )
            self.update()
            return self.keyTextbox.current.value, False
        else:
            return self.keyTextbox.current.value, True

    def addNewChild(self, e):
        values, state = self.checkTextBoxData()
        if state:
            self.loaderUi()
            state, result = self.page.run_task(
                self.sendPostRequest, "Children", {"key": values}
            ).result()
            if state:
                self.showMessage(result["key"])
                self.did_mount()
            else:
                self.did_mount()
                self.showMessage(result["key"])

    def getDevices(self):
        state, result = self.page.run_task(self.sendGetRequest, "Children").result()
        if state:
            devices = []
            for childData in result.values():
                devices.append(
                    ResponsiveRow(
                        controls=[
                            Container(
                                content=ListTile(
                                    leading=Icon(
                                        icons.PHONE_ANDROID_OUTLINED,
                                        color="#110b22",
                                    ),
                                    title=Text(
                                        f"جهاز  {childData[0]['child_first_name']}",
                                        style=TextStyle(
                                            size=15,
                                            weight=FontWeight.BOLD,
                                            font_family="ElMessiri",
                                        ),
                                    ),
                                    subtitle=Text(
                                        f"{childData[0]['key']}",
                                        style=TextStyle(
                                            size=8,
                                            weight=FontWeight.BOLD,
                                            font_family="ElMessiri",
                                        ),
                                    ),
                                    trailing=PopupMenuButton(
                                        icon=icons.MORE_VERT,
                                        items=[
                                            PopupMenuItem(
                                                text="حذف",
                                                data=childData[0]["key"],
                                                icon=icons.DELETE,
                                                on_click=self.deleteUser,
                                            ),
                                        ],
                                        menu_position=PopupMenuPosition.UNDER,
                                        icon_color="#110b22",
                                        tooltip="خيارات",
                                    ),
                                ),
                                bgcolor="#ffffff",
                                border=border.all(0.5, "#110b22"),
                                border_radius=border_radius.all(5),
                            ),
                        ],
                    )
                )
            self.devices = devices
            self.buildUi()
        else:
            self.buildUi()
            self.showMessage("حدث خطا غير متوقع")

    async def sendDeleteRequest(self, url, body={}):
        access = await self.page.client_storage.get_async("access")
        headers = {
            "Authorization": f"Bearer {access}",
            "Accept": "*/*",
            "Cache-Control": "no-cache",
        }
        try:
            response = requests.delete(
                url=f"{self.baseUrl}/{url}/", data=body, headers=headers
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

    async def sendPostRequest(self, url, body={}):
        access = await self.page.client_storage.get_async("access")
        headers = {
            "Authorization": f"Bearer {access}",
            "Accept": "*/*",
            "Cache-Control": "no-cache",
        }
        try:
            response = requests.post(
                url=f"{self.baseUrl}/{url}/", data=body, headers=headers
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

    async def sendGetRequest(self, url, body={}):
        access = await self.page.client_storage.get_async("access")
        headers = {
            "Authorization": f"Bearer {access}",
            "Accept": "*/*",
            "Cache-Control": "no-cache",
        }
        try:
            response = requests.get(
                url=f"{self.baseUrl}/{url}/", data=body, headers=headers
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
