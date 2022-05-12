# python libraries ------------------------------------------
import pygame
import time

# project libraries -----------------------------------------
from board import Board

# resources -------------------------------------------------
from flowingconfig import *
raw_board = pygame.image.load("res/images/eq_chessboard.png")
icon = pygame.image.load("res/images/icon.png")
board = pygame.transform.scale(raw_board, (width - padding_absolute, height - padding_absolute))


# functinos -------------------------------------------------
def redraw_gamewindow(win, bo, p1time, p2time, statewhite, stateblack):
    pygame.font.init()
    pygame.draw.rect(win, (0, 0, 0), (0, 0, width, width))
    win.blit(board, (padding_abs_half, padding_abs_half))
    bo.draw(win)
    font = pygame.font.SysFont("console", 17)
    font2 = pygame.font.SysFont("console", 25)
    f1time = str(p1time//60)+":"+str(p1time%60)
    f2time = str(p2time//60)+":"+str(p2time%60)
    if p1time % 60 < 10:
        f1time = str(p1time // 60) + ":" + "0" + str(p1time % 60)
    elif p1time % 60 == 0:
        f1time += "0"
    if p2time % 60 < 10:
        f2time = str(p2time // 60) + ":" + "0" + str(p2time % 60)
    elif p2time % 60 == 0:
        f2time += "0"
    txttime1 = font.render("Player 1 Time: " + str(f1time), True, (255, 255, 255), (0, 0, 0))
    txttime2 = font.render("Player 2 Time: " + str(f2time), True, (255, 255, 255), (0, 0, 0))
    if statewhite == 1:
        txtstate1 = font2.render("White King is under check!", True, (255, 255, 255), (0, 0, 0))
    else:
        txtstate1 = font2.render("White King is under check!", True, (0, 0, 0), (0, 0, 0))
    if stateblack == 1:
        txtstate2 = font2.render("Black King is under check!", True, (255, 255, 255), (0, 0, 0))
    else:
        txtstate2 = font2.render("Black King is under check!", True, (0, 0, 0), (0, 0, 0))
    win.blit(txttime1, (width - padding_abs_half - txttime1.get_width(), width - padding_abs_half + txttime1.get_height()))
    win.blit(txttime2, (padding_abs_half, padding_abs_half - txttime2.get_height() * 2))
    win.blit(txtstate1, (padding_abs_half, width - padding_abs_half / 1.5))
    win.blit(txtstate2, (width - padding_abs_half - txtstate2.get_width(), padding_abs_half - txtstate2.get_height() * 1.5))
    pygame.display.update()


def end_screen(win, text, total_time):
    pygame.font.init()
    font = pygame.font.SysFont("arial", 70)
    font.set_bold(True)
    txt = font.render(text, True, (255, 0, 0))

    font2 = pygame.font.SysFont("arial", 35)
    font2.set_bold(True)
    total_time = int(total_time)
    ftime = str(total_time//60)+":"+str(total_time%60)
    if total_time % 60 < 10:
        ftime = str(total_time // 60) + ":" + "0" + str(total_time % 60)
    elif total_time % 60 == 0:
        ftime += "0"
    txttime = font2.render(ftime, True, (255, 0, 0))

    win.blit(txt, (width / 2 - txt.get_width() / 2, width / 2 - txt.get_height()))
    win.blit(txttime, (width / 2 - txttime.get_width() / 2, width / 2))
    pygame.display.update()
    pygame.time.set_timer(pygame.USEREVENT+1, 3000)
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    run = False
                    quit()
                    pygame.quit()
                if event.key == pygame.K_r:
                    main()

def click(pos):
    x = pos[0]
    y = pos[1]
    if top_left_corner[0] < x < top_left_corner[0] + bottom_right_corner[0]:
        if top_left_corner[1] < y < top_left_corner[1] + bottom_right_corner[1]:
            divx = x - top_left_corner[0]
            divy = y - top_left_corner[0]
            i = int(divx / (bottom_right_corner[0] / 8))
            j = int(divy / (bottom_right_corner[1] / 8))
            return i, j

# main ------------------------------------------------------
def main():
    p1time = time_restriction_seconds
    p2time = time_restriction_seconds
    wide_timer = time.time()
    start_time = time.time()
    turn = "w"
    bo = Board(8, 8)
    bo.update_moves()
    clock = pygame.time.Clock()
    run = True
    statewhite = 0
    stateblack = 0
    count_white = 0
    count_black = 0
    while run:
        clock.tick(fps_max)
        if turn == "w":
            p1time -= (time.time() - wide_timer)
            if p1time <= 0:
                end_screen(win, "Black Wins!", time.time() - start_time)
        else:
            p2time -= (time.time() - wide_timer)
            if p2time <= 0:
                end_screen(win, "White Wins!", time.time() - start_time)
        wide_timer = time.time()
        redraw_gamewindow(win, bo, int(p1time), int(p2time), statewhite, stateblack)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                quit()
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    run = False
                    quit()
                    pygame.quit()
                if event.key == pygame.K_s:
                    if turn == "w":
                        end_screen(win, "Black Wins!", time.time() - start_time)
                    else:
                        end_screen(win, "White Wins!", time.time() - start_time)
                if event.key == pygame.K_p:
                    if turn == "w":
                        count_white = 1
                    if turn == "b":
                        count_black = 1
                    if count_black and count_white:
                        end_screen(win, "Draw!", time.time() - start_time)

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                bo.update_moves()
                if padding_abs_half < pos[0] < width - padding_abs_half and padding_abs_half < pos[1] < width - padding_abs_half:
                    i, j = click(pos)
                    try:
                        change = bo.select(i, j, turn)
                        bo.update_moves()
                    except AttributeError:
                        change = False
                    if change:
                        wide_timer = time.time()
                        if turn == "w":
                            bo.reset_selected()
                            # print("log: time", time.time() - start_time)
                            if bo.is_checked("w") and statewhite == 1:
                                end_screen(win, "Black Wins!", time.time() - start_time)
                            if bo.is_checked("b") and stateblack == 1:
                                end_screen(win, "White Wins!", time.time() - start_time)
                            turn = "b"
                        else:
                            bo.reset_selected()
                            # print("log: time", time.time() - start_time)
                            if bo.is_checked("b") and stateblack == 1:
                                end_screen(win, "White Wins!", time.time() - start_time)
                            if bo.is_checked("w") and statewhite == 1:
                                end_screen(win, "Black Wins!", time.time() - start_time)
                            turn = "w"

                if bo.is_checked("w"):
                    # print("log: White check")
                    statewhite = 1
                else:
                    statewhite = 0
                if bo.is_checked("b"):
                    # print("log: Black check")
                    stateblack = 1
                else:
                    stateblack = 0


win = pygame.display.set_mode((width, height), vsync=True)
pygame.display.set_caption("PyChess")
pygame.display.set_icon(icon)
main()
