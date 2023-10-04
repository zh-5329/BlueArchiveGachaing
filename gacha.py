from game import*
pg.display.set_caption("gacha")
screen = pg.display.set_mode((W, H))
tb=TextBox((200, 20), (100, 100))
page=Page(pic_1, (0, 0), (1280, 300))
page.add_textbox(tb)
page.add_scrollbar()
page.add_text(Text("Hello World!!!!!"))
print(calc_pos((0, 0), (1280, 300), (20, 200), -1))
for b in page.button:
    b.switch()
for s in page.scrollbar:
    s.switch()
A, B=Rect((100, 100), (200, 20)), Rect((0, 0), (1280, 300))
while T:
    page.blitme(screen)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
        page.deal(event)
    page.update()
    pg.display.update()
    CLOCK.tick(fps)
    screen.fill(WHITE)