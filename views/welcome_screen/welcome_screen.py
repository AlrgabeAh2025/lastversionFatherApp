from flet import *

class Welcome(View):

    def __init__(self, route, page):
        super().__init__(route=route)
        self.scroll = ScrollMode.AUTO

        
        self.controls.append( 
            ResponsiveRow(
                controls=[
                    Container(height=10),
                     Column(
                        controls=[
                            ResponsiveRow(
                                controls=[
                                    Image(
                                        src="images/logo.png",
                                        fit=ImageFit.COVER,
                                        border_radius=border_radius.all(20.0),
                                         col={"xs":10 , "sm":10, "md":7 , "lg":5 , "xl":5},
                                        ),
                                ],
                                expand=False,
                                alignment=MainAxisAlignment.CENTER
                            ),
                            Container(height=10),
                            Text(
                                "وصلة",
                                size=30,
                                weight=FontWeight.BOLD,
                                font_family="ElMessiri"
                            ),
                            Container(height=10),
                            Text(
                                "حارسك لأمان عائلتك",
                                size=20,
                                weight=FontWeight.NORMAL,
                                font_family="ElMessiri"
                            ),
                            Container(height=10),
                            ResponsiveRow(
                                controls=[
                                    ElevatedButton(
                                        "تسجيل الدخول",
                                        style=ButtonStyle(
                                            shape=RoundedRectangleBorder(radius=22),
                                            bgcolor="#171335",
                                            color="#ffffff",
                                            text_style=TextStyle(
                                                size=15,
                                                weight=FontWeight.BOLD,
                                                font_family="ElMessiri"
                                            ),
                                            padding=5
                                        ),
                                        on_click=lambda e: self.page.go("/login")
                                    ),
                                ]
                            ),
                            Container(height=10),
                            ResponsiveRow(
                                controls=[
                                    ElevatedButton(
                                        "انشاء حساب",
                                        style=ButtonStyle(
                                            shape=RoundedRectangleBorder(radius=22),
                                            bgcolor="#171335",
                                            color="#ffffff",
                                            text_style=TextStyle(
                                                size=15,
                                                weight=FontWeight.BOLD,
                                                font_family="ElMessiri"
                                            ),
                                            padding=5
                                        ),
                                        on_click=lambda e: self.page.go("/signup")
                                    ),
                                ]
                            ),
                            
                        ],
                        horizontal_alignment=CrossAxisAlignment.CENTER,
                        alignment=MainAxisAlignment.CENTER,
                    ),
                ],
                expand=True
            )
        )
