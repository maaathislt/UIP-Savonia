import flet as ft
import datetime

def main(page: ft.Page):
    page.title = "Homework 5 UIP Mathis LE TEXIER_s2520833"

    # Variables to save data in form
    form_data = {
        "name": "",
        "dob": "",
        "gender": "",
        "address": "",
        "country": ""
    }

    # Route change
    def route_change(e: ft.RouteChangeEvent) -> None:
        page.views.clear()

        # Login page
        page.views.append(
            ft.View(
                route="/",
                controls=[
                    ft.AppBar(title=ft.Text("Flet App"), bgcolor="grey", color="white"),
                    ft.Column(
                        [
                            ft.TextField(label="Email", width=300, border_color="white", color="white",
                                         label_style=ft.TextStyle(color="white")),
                            ft.TextField(label="Password", password=True, can_reveal_password=True, width=300,
                                         border_color="white", color="white", label_style=ft.TextStyle(color="white")),
                            ft.ElevatedButton(text="Login", on_click=lambda _: page.go('/form'))
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        horizontal_alignment=ft.CrossAxisAlignment.START,
                        spacing=20,
                    ),
                ],
                vertical_alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.START,
                padding=40
            )
        )

        # Form page
        if page.route == "/form":

            name_field = ft.TextField(
                label="Name", width=300, border_color="white", color="white",
                label_style=ft.TextStyle(color="white")
            )
            address_field = ft.TextField(
                label="Address", width=300, border_color="white", color="white",
                label_style=ft.TextStyle(color="white")
            )
            gender_group = ft.RadioGroup(
                content=ft.Column([
                    ft.Radio(value="Man", label="Man"),
                    ft.Radio(value="Woman", label="Woman"),
                    ft.Radio(value="Other", label="Other"),
                ])
            )

            countries_europe = [
                "Albania", "Andorra", "Armenia", "Austria", "Azerbaijan", "Belarus",
                "Belgium", "Bosnia and Herzegovina", "Bulgaria", "Croatia", "Cyprus",
                "Czech Republic", "Denmark", "Estonia", "Finland", "France", "Georgia",
                "Germany", "Greece", "Hungary", "Iceland", "Ireland", "Italy", "Kosovo",
                "Latvia", "Liechtenstein", "Lithuania", "Luxembourg", "Malta", "Moldova",
                "Monaco", "Montenegro", "Netherlands", "North Macedonia", "Norway", "Poland",
                "Portugal", "Romania", "Russia", "San Marino", "Serbia", "Slovakia",
                "Slovenia", "Spain", "Sweden", "Switzerland", "Turkey", "Ukraine",
                "United Kingdom", "Vatican City"
            ]

            country_dropdown = ft.Dropdown(
                editable=True, label="European Country", width=300,
                border_color="white", color="white",
                label_style=ft.TextStyle(color="white"),
                options=[ft.dropdown.Option(country) for country in countries_europe],
            )

            dob_picker = ft.DatePicker(
                first_date=datetime.datetime(year=2000, month=10, day=1),
                last_date=datetime.datetime(year=2025, month=10, day=1),
            )

            def open_dob(e):
                page.open(dob_picker)

            def create_clicked(e):
                form_data["name"] = name_field.value
                form_data["address"] = address_field.value
                form_data["gender"] = gender_group.value
                form_data["country"] = country_dropdown.value
                form_data["dob"] = dob_picker.value.strftime("%m/%d/%Y") if dob_picker.value else ""
                page.go("/form/result")

            page.views.append(
                ft.View(
                    route="/form",
                    controls=[
                        ft.AppBar(
                            title=ft.Text("Form"),
                            bgcolor="grey", color="white",
                            leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda _: page.go("/")),
                        ),
                        ft.Column(
                            [
                                name_field,
                                ft.ElevatedButton("Date of Birth", icon=ft.Icons.CALENDAR_MONTH, on_click=open_dob),
                                ft.Text("Gender:", color="white"),
                                gender_group,
                                address_field,
                                country_dropdown,
                                ft.ElevatedButton(text="Create", on_click=create_clicked)
                            ],
                            alignment=ft.MainAxisAlignment.START,
                            horizontal_alignment=ft.CrossAxisAlignment.START,
                            spacing=20,
                        )
                    ],
                    vertical_alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.CrossAxisAlignment.START,
                    padding=40
                )
            )

        # Result page
        if page.route == "/form/result":
            page.views.append(
                ft.View(
                    route="/form/result",
                    controls=[
                        ft.AppBar(
                            title=ft.Text("Result"),
                            bgcolor="grey", color="white",
                            leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda _: page.go("/form")),
                        ),
                        ft.Column(
                            [
                                ft.Row(
                                    [
                                        ft.Text(f"Name: {form_data['name']}", color="white"),
                                        ft.Text(f"Date of Birth: {form_data['dob']}", color="white"),
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    spacing=60,
                                ),
                                ft.Row(
                                    [
                                        ft.Text(f"Gender: {form_data['gender']}", color="white"),
                                        ft.Text(f"Address: {form_data['address']}", color="white"),
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    spacing=60,
                                ),
                                ft.Row(
                                    [
                                        ft.Text(f"Country: {form_data['country']}", color="white"),
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    spacing=60,
                                ),
                                ft.Row(
                                    [
                                        ft.ElevatedButton(text="Go back", on_click=lambda _: page.go('/')),
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    spacing=60,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=20,
                        )
                    ],
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    padding=40
                )
            )
        page.update()

    # View pop to be able to go back to the preceding view
    def view_pop(e: ft.ViewPopEvent) -> None:
        if page.route == "/form":
            page.go("/")
        elif page.route == "/form/result":
            page.go("/form")

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


if __name__ == "__main__":
    ft.app(target=main)