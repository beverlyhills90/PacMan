import pygame as pg


class VictoryView:
    def __init__(self, screen: pg.Surface) -> None:
        self.screen: pg.Surface = screen
        main_font_path = Path(__file__).resolve(
        ).parent / "fonts" / "PressStart2P-vaV7.ttf"
        self.button_font = pg.font.Font(main_font_path, 20)
        self.button_hover_font = pg.font.Font(main_font_path, 25)

    def draw_victory(self) -> None
