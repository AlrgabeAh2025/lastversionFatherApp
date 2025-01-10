from flet import *
import requests


class MostUsedApplications(View):
    def __init__(self, route, page):
        super().__init__(route=route)
        self.scroll = ScrollMode.AUTO
        self.apps = []

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

    def buildUi(self):
        self.scroll = ScrollMode.AUTO
        self.controls.clear()
        self.controls.append(
            ResponsiveRow(
                controls=[
                    Container(height=10),
                    Column(
                        controls=[
                            Container(height=30),
                            ResponsiveRow(
                                controls=[
                                    Text(
                                        "قائمة التطبيقات",
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
                                    self.apps
                                    if len(self.apps) > 0
                                    else [
                                        Container(
                                            content=Text(
                                                "لا يوجد تطبيقات بعد",
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
                                ),
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
        loader = self.loaderUi()
        self.controls.clear()
        self.controls.append(loader)
        self.update()
        self.loadMostUseApps()

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

    async def sendGetRequest(self, url, body={}):
        access = await self.page.client_storage.get_async("access")
        headers = {
            "Content-Length": "165",  # تأكد من أنه لا حاجة لتحديد الطول يدويًا إذا كنت تستخدم مكتبة مثل requests
            "Authorization": f"Bearer {access}",
            "User-Agent": "PostmanRuntime/7.39.1",
            "Accept": "*/*",
            "Cache-Control": "no-cache",
            "Host": "127.0.0.1:8000",  # يمكن حذف هذا إذا كنت تستخدم مكتبة requests
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
        }

        try:
            response = requests.get(
                url=f"{MostUsedApplications.baseUrl}/{url}/", data=body, headers=headers
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

    def loadMostUseApps(self):
        childId = self.page.run_task(
            self.page.client_storage.get_async, "ChildUser"
        ).result()
        state, result = self.page.run_task(
            self.sendGetRequest, "mostUseApps", {"ChildUser": childId}
        ).result()
        if state:
            self.apps = [
                Container(
                    content=ResponsiveRow(
                        controls=[
                            ListTile(
                                title=Text(
                                    f"{app['hour']}",
                                    style=TextStyle(
                                        size=10,
                                        weight=FontWeight.BOLD,
                                        font_family="ElMessiri",
                                    ),
                                ),
                                leading=Text(
                                    f"{app['appName']}",
                                    style=TextStyle(
                                        size=15,
                                        weight=FontWeight.BOLD,
                                        font_family="ElMessiri",
                                    ),
                                ),
                                trailing=Icon(icons.FACEBOOK),
                                subtitle=ProgressBar(value=0.8),
                            )
                        ],
                    ),
                    bgcolor="#ffffff",
                    border=border.all(0.5, "#110b22"),
                    border_radius=border_radius.all(5),
                    alignment=alignment.center,
                )
                for app in result
            ]
            self.buildUi()
        else:
            self.ErrorUi()
