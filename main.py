import pygame
from pygame.color import THECOLORS as col
from pygame.locals import *
from ppp_button import Button
from ppp_func import *
from ppp_player import Player
from ppp_text import Text
from sys import exit
from easygui import msgbox, ynbox
from traceback import format_exc


if __name__ == '__main__':
    try:
        bgimg = pygame.image.load(get_file('img/bg.jpg'))
        filecol = col['yellow']
        filesize = (20, 30)
        msgcol = col['red']
        msgsize = (15, 20)
        statecol = col['red']
        statesize = (15, 20)
        lrccol1 = col['brown']
        lrccol2 = col['white']
        lrcsize = (15, 50)
        progwid = 30
        progsize = (20, 20)
        progcol = col['red']
        progcol1 = col['yellow']
        progcol2 = col['blue']
        tmrwid = 30
        tmrsize = (20, 20)
        tmrcol = col['black']
        tmrcol1 = col['red']
        tmrcol2 = col['green']
        pygame.init()
        screen = pygame.display.set_mode((1000, 600))
        pygame.display.set_caption('PyPigPlayerLite')
        player = Player()
        pygame.key.set_repeat(500, 100)
        btn_back = Button(-1, 'back',
                          lambda: player.set_pos(player.get_pos() - 5000))
        btn_forward = Button(-1, 'forward',
                             lambda: player.set_pos(player.get_pos() + 5000))
        btn_minus = Button(-1, 'minus',
                           lambda: player.set_timer(player.get_timer() - 5))
        btn_plus = Button(-1, 'plus',
                          lambda: player.set_timer(player.get_timer() + 5))
        btn_search = Button(-1, 'search', player.download_lrc)
        btn_time = Button(0, 'time', player.on_off_timer)
        btn_open = Button(1, 'open', lambda: player.open_file(btn_play))
        btn_play = Button(2, 'play', lambda: player.play_pause(btn_play))
        btn_volm = Button(
            3, 'vol-', lambda: player.set_vol(player.get_vol() - 5))
        btn_volp = Button(
            4, 'vol+', lambda: player.set_vol(player.get_vol() + 5))
        d_list = [btn_time, btn_open, btn_play, btn_volm, btn_volp]
        t_file = Text(filesize, 'mu')
        t_msg = Text(msgsize, 'md')
        t_state = Text(statesize, 'md')
        t_lrc = Text(lrcsize, 'mm')
        t_prog = Text(progsize, 'mm')
        t_tmr = Text(tmrsize, 'mm')
        key_handling = {
            K_SPACE: lambda: player.play_pause(btn_play),
            K_UP: lambda: player.set_vol(player.get_vol() + 5),
            K_DOWN: lambda: player.set_vol(player.get_vol() - 5),
            K_LEFT: lambda: player.set_pos(player.get_pos() - 5000),
            K_RIGHT: lambda: player.set_pos(player.get_pos() + 5000),
        }
        mouse = False
        d_num = 5
        d_pos = [(i * 80+340, 560) for i in range(d_num)]
        ledge = 10
        redge = 990
        mid = (ledge + redge) / 2
        width = redge - ledge

    except Exception as e:
        msgbox('初始化出错:\n\n'+format_exc())
        exit()

    while True:
        try:
            for event in pygame.event.get():
                if event.type == QUIT:
                    exit()

                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse = 1
                        for button in d_list:
                            button.test_click(event.pos)
                        if player.is_timer_on():
                            btn_minus.test_click(event.pos)
                            btn_plus.test_click(event.pos)
                        if player.opened():
                            if progrt.collidepoint(event.pos):
                                player.set_prog(
                                    (event.pos[0] - progrt.left) / progrt.width)
                            btn_back.test_click(event.pos)
                            btn_forward.test_click(event.pos)
                            if not player.have_lrc():
                                btn_search.test_click(event.pos)
                    elif event.button >= 5 and event.button % 2:
                        if player.opened():
                            if progrt.collidepoint(event.pos):
                                player.set_pos(
                                    player.get_pos() + 200 * event.button)
                            if player.have_lrc():
                                if alllrcrt.collidepoint(event.pos):
                                    player.next_lrc()
                    elif event.button >= 4:
                        if player.opened():
                            if progrt.collidepoint(event.pos):
                                player.set_pos(
                                    player.get_pos() - 200 * event.button)
                            if player.have_lrc():
                                if alllrcrt.collidepoint(event.pos):
                                    player.last_lrc()

                if event.type == MOUSEBUTTONUP:
                    mouse = 0

                if event.type == MOUSEMOTION:
                    if mouse:
                        if player.opened():
                            if progrt.collidepoint(event.pos):
                                player.set_prog(
                                    (event.pos[0] - progrt.left) / progrt.width)

                if event.type == USEREVENT:
                    player.music_end(btn_play)

                if event.type == KEYDOWN:
                    if event.key in key_handling.keys():
                        key_handling[event.key]()

            screen.blit(pygame.transform.scale(
                bgimg, (1000, 600)), (0, 0))

            for button in d_list:
                button.show(screen, d_pos[button.id], 60)
            if player.opened() and not player.have_lrc():
                btn_search.show(screen, (500, 300), 60)
            statebtm = 504
            lrctop = t_file.show(screen,
                                 player.get_music_name(), filecol,
                                 (mid, 10),
                                 maxwidth=width).bottom + 10
            msg = player.get_msg()
            if msg:
                statebtm = t_msg.show(screen,
                                      msg,
                                      msgcol,
                                      (mid, statebtm),
                                      maxwidth=width).top-10

            progbtm = tmrbtm = t_state.show(
                screen,
                player.get_state(),
                statecol,
                (500, statebtm),
                maxwidth=width).top - 10

            if player.opened():
                btn_back.show(
                    screen, (progwid / 2 + 10, progbtm - progwid / 2), progwid)
                btn_forward.show(screen, (1000 - progwid / 2 - 10,
                                 progbtm - progwid / 2), progwid)
                progrt = pygame.Rect(progwid + 20,
                                     progbtm - progwid,
                                     1000 - progwid * 2 - 40,
                                     progwid)
                lrcbtm = progrt.top - 10
                pygame.draw.rect(screen,
                                 progcol2,
                                 progrt)
                pygame.draw.rect(screen,
                                 progcol1,
                                 pygame.Rect(progwid + 20,
                                             progbtm - progwid,
                                             (1000 - progwid * 2 - 40) *
                                             player.get_prog(),
                                             progwid))
                t_prog.show(screen, player.get_time(), progcol, progrt.center)
                if player.have_lrc():
                    alllrcrt = pygame.Rect(
                        ledge, lrctop, width, lrcbtm - lrctop)
                    lrcsp, lrcrt = t_lrc.show(screen,
                                              player.get_lrc(0),
                                              lrccol1,
                                              (mid,
                                               (lrctop + lrcbtm) / 2),
                                              maxwidth=width,
                                              getheight=True)
            pygame.draw.line(screen,
                             col['white'],
                             (0, 518),
                             (1000, 518),
                             4)

            pygame.display.update()

        except Exception as e:
            if not ynbox(format_exc(), 'PyPigPlayer出错了,要继续运行吗?'):
                exit()
