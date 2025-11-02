
import asyncio
import flet as ft

class Countdown:
    def __init__(self, name: str, start_value: int):
        self.name = name
        self.start_value = start_value
        self.remaining = start_value
        self.running = False
        self.task = None
        self.update_ui_callback = None

    async def on_start(self):
        if self.running or self.remaining <= 0:
            return
        self.running = True
        # Here, we start the countdown
        self.task = asyncio.create_task(self.run_timer())

    # Here, we define how to timer works
    async def run_timer(self):
        while self.running and self.remaining > 0:
            await asyncio.sleep(1)
            self.remaining -= 1
            if self.update_ui_callback:
                self.update_ui_callback()
        self.running = False
        if self.update_ui_callback:
            self.update_ui_callback()

    def on_stop(self):
        self.running = False

    def reset(self):
        self.running = False
        self.remaining = self.start_value
        if self.update_ui_callback:         #update_ui_callback_ let us go back to the inital value of the countdown
            self.update_ui_callback()


def main(page: ft.Page):
    page.title = "Home Work 6 LE TEXIER Mathis s2520833 Async Countdowns"

    # We call the class Countdown three times, we give the name of the counter and the starting time 
    timers = [
        Countdown("Timer 1", 100),
        Countdown("Timer 2", 110),
        Countdown("Timer 3", 120),
    ]

    #This fonction will be used three times, the idea is that the content is roughly the same, so we can call it and just change the name and value of the timer
    def build_timer_content(timer: Countdown):
        
        title = ft.Text(timer.name, size=24)
        remaining_label = ft.Text(f"Remaining: {timer.remaining}s", size=18)
        progress = ft.ProgressBar(value=(timer.remaining / timer.start_value), width=350)


        def update_ui():
            # We don't want to devide by 0
            progress.value = (timer.remaining / timer.start_value) if timer.start_value > 0 else 0
            remaining_label.value = f"Remaining: {timer.remaining}s"

            page.update()

        timer.update_ui_callback = update_ui

        # The three buttons needed to start, stop and reset the timer, they will be used on every pages, so we put them here
        start_btn = ft.ElevatedButton("Start", on_click=lambda e, t=timer: page.run_task(t.on_start))
        stop_btn = ft.ElevatedButton("Stop", on_click=lambda e, t=timer: t.on_stop())
        reset_btn = ft.ElevatedButton("Reset", on_click=lambda e, t=timer: t.reset())

        controls = ft.Column(
            [
                title,
                remaining_label,
                progress,
                ft.Row([start_btn, stop_btn, reset_btn], alignment=ft.MainAxisAlignment.CENTER),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            tight=True,
        )

        return controls

    # We create the tabs using the fontion that we created just before
    tab_contents = [build_timer_content(t) for t in timers]

    tabs = ft.Tabs(
        selected_index=0,
        tabs=[
            ft.Tab(text="Timer 1", content=tab_contents[0]),    
            ft.Tab(text="Timer 2", content=tab_contents[1]),
            ft.Tab(text="Timer 3", content=tab_contents[2]),
        ],
        expand=True,
    )
    #We add the tabs on the page
    page.add(tabs)

ft.app(target=main)