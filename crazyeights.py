#! /usr/bin/env python3
# -*- coding: utf-8 -*-

############################################################################
#    Copyright (C) 2007 by kawk                                            #
#    kawk@theprogrammingsite.com                                           #
#                                                                          #
#    This file is a Crazy Eights card game for the FiftyTwo card game set. #
#    FiftyTwo is a set of card games for the OLPC XO laptop.               #
#                                                                          #
#    This program is free software; you can redistribute it and/or modify  #
#    it under the terms of the GNU General Public License as published by  #
#    the Free Software Foundation; either version 2 of the License, or     #
#    (at your option) any later version.                                   #
#                                                                          #
#    This program is distributed in the hope that it will be useful,       #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of        #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         #
#    GNU General Public License for more details.                          #
#                                                                          #
#    You should have received a copy of the GNU General Public License     #
#    along with this program; if not, write to the                         #
#    Free Software Foundation, Inc.,                                       #
#    51 Franklin St, Fifth Floor, Boston, MA  02110-1301 USA               #
############################################################################

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import fiftytwo
from fiftytwo import card_width, card_height, UP, DOWN
import math, random
import pygame
from pygame.locals import *

from gettext import gettext as _

import run

LOCALPLAYER = 0
AIPLAYER = 1
REMOTEPLAYER = 2

BGCOL = (0, 32, 64)

class player(fiftytwo.cardgroup):
    """
    Basic player class -- not much to it. Inherits from fiftytwo.cardgroup
    """
    def __init__(self, position):
        fiftytwo.cardgroup.__init__(self, (), position[0], position[1])
        self.name = _("Unnamed")
        self.number = 0

    def next_turn(self, topcardid):
        pass

    def render_name(self):
        font = pygame.font.Font(None, 28)
        self.id = font.render(self.name, 1, (255, 255, 0))

class localplayer(player):
    def __init__(self, position):
        player.__init__(self, position)
        self.ai = 0
        self.type = LOCALPLAYER

    def next_turn(self, topcardid):
        return 0

class remoteplayer(player):
    def __init__(self, position):
        player.__init__(self, position)
        self.ai = 0
        self.type = REMOTEPLAYER

    def next_turn(self, topcardid):
        return 0

class aiplayer(player):
    def __init__(self, position):
        player.__init__(self, position)
        self.ai = 1
        self.type = AIPLAYER

    def next_turn(self, topcardid, currentsuit):
        list = []
        for tc in self.sprites():
            if check_valid(topcardid, tc.cardid, currentsuit):
                list.insert(0, tc)

        highvalue = 0
        highcard = None
        for tc in list:
            if tc.cardid == 'JS':
                highvalue = 100
                highcard = tc
            elif tc.cardid[0] == '8':
                if highvalue <= 1:
                    highvalue = 1
                    highcard = tc
            elif tc.cardid[0] == '2':
                if highvalue <= 75 and tc.cardid[1] != topcardid[1]:
                    highvalue = 50
                    highcard = tc
                elif highvalue <= 75 and tc.cardid[1] == topcardid[1]:
                    highvalue = 76
                    highcard = tc
            else:
                highcard = tc

        return highcard

    def choose_new_suit(self):
        """
        Chooses a new suit based on the player's current hand.

        BUGS: If the player has an equal number of different suits, the
        first suit in the list "1, 2, 3, 4" will be chosen.
        """
        list = [['1', 0], ['2', 0], ['3', 0], ['4', 0]]

        for sprite in self.sprites():
            if sprite.cardid[0] == '8':
                continue

            if sprite.cardid[1] == '1':
                list[0][1] += 1
            elif sprite.cardid[1] == '2':
                list[1][1] += 1
            elif sprite.cardid[1] == '3':
                list[2][1] += 1
            elif sprite.cardid[1] == '4':
                list[3][1] += 1

        highest = ['!', 0]
        for x in list:
            if x[1] > highest[1]:
                highest[1] = x[1]
                highest[0] = x[0]

        return highest[0]


def check_valid(topcard, tocheck, currentsuit):
    if tocheck[0] == '8':
        return 1
    elif topcard[0] == '8':
        if tocheck[1] == currentsuit:
            return 1
        else:
            return 0
    elif tocheck[1] == topcard[1]:
        return 1
    elif tocheck[0] == topcard[0]:
        return 1
    else:
        return 0

def end_turn(players, whosturn):
    whosturn += 1
    whosturn = int(math.fmod(whosturn, len(players)))
    return whosturn

def prev_turn(players, whosturn):
    whosturn -= 1
    whosturn = int(math.fmod(whosturn, len(players)))
    return whosturn


def choose_suit(player, choosesuitimage, discard):
    screen = pygame.display.get_surface()
    font = pygame.font.Font(None, 28)
    text = font.render(_("Choose a suit"), 1, (0, 255, 255))

    screen.fill((128, 64, 64), ((50, 50), (200, 200)))

    fpslimiter = pygame.time.Clock()

    while 1:
        fpslimiter.tick(20)

        while Gtk.events_pending():
            Gtk.main_iteration()

        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == MOUSEBUTTONDOWN:
                if event.pos[0] < 150 and event.pos[0] > 100 and event.pos[1] > 100 and event.pos[1] < 150:
                    screen.fill(BGCOL, ((50, 50), (250, 250)))
                    return '1'

                elif event.pos[0] < 200 and event.pos[0] > 150 and event.pos[1] > 100 and event.pos[1] < 150:
                    screen.fill(BGCOL, ((50, 50), (250, 250)))
                    return '2'

                elif event.pos[0] < 150 and event.pos[0] > 100 and event.pos[1] > 150 and event.pos[1] < 200:
                    screen.fill(BGCOL, ((50, 50), (250, 250)))
                    return '3'
                elif event.pos[0] < 200 and event.pos[0] > 150 and event.pos[1] > 150 and event.pos[1] < 200:
                    screen.fill(BGCOL, ((50, 50), (250, 250)))
                    return '4'

        screen.blit(choosesuitimage, (100, 100))
        screen.blit(text, (100, 50))
        clear_prev(discard)
        clear_prev(player)
        discard.next_frame(screen)
        player.next_frame(screen)

        pygame.display.flip()

    screen.fill(BGCOL, ((50, 50), (250, 250)))

def clear_prev(group):
    screen = pygame.display.get_surface()
    for s in group.sprites():
        screen.fill(BGCOL, s.get_prevrect())

def special_cards(deck, discard, players, whosturn, cardprocessed, choosesuitimage, currentsuit):
    if discard.sprites()[-1].cardid[0] == '2' and cardprocessed is 0:
        fiftytwo.draw_card(deck, players[whosturn])
        if players[whosturn].ai == 0: players[whosturn].sprites()[-1].set_face(UP)
        fiftytwo.draw_card(deck, players[whosturn])
        if players[whosturn].ai == 0: players[whosturn].sprites()[-1].set_face(UP)
        cardprocessed = 1

    elif discard.sprites()[-1].cardid[0] == '8' and cardprocessed is 0:
        whosturn = prev_turn(players, whosturn)

        if players[whosturn].ai is not 1:
            currentsuit = choose_suit(players[whosturn], choosesuitimage, discard)
        else:
            currentsuit = players[whosturn].choose_new_suit()
        cardprocessed = 1

        whosturn = end_turn(players, whosturn)

    elif discard.sprites()[-1].cardid == 'J4' and cardprocessed is 0:
        whosturn = end_turn(players, whosturn)

        cardprocessed = 1

    elif cardprocessed is 1:
        pass

    else:
        cardprocessed = 1

    return cardprocessed, whosturn, currentsuit

def main(playertypes, screensize):
    running = True
    sw = screensize[0]
    sh = screensize[1]

    localplayers = 0

    # Reduce load
    pygame.event.set_blocked(pygame.MOUSEMOTION)

    #positions = (((5, -card_height()/2), (sw-5, card_height()-(card_height()/2))), ((5, sh-card_height()/2), (sw-5, sh+card_height()/2)))
    positions = (((int(card_width()*1.5), -card_height()/2), (sw-int(card_width()*1.5), card_height()-(card_height()/2))),
        ((sw-int(card_width()*0.5), 5), (sw+int(card_width()*0.5), sh-5)),
        ((int(card_width()*1.5), sh-card_height()/2), (sw-int(card_width()*1.5), sh+card_height()/2)),
        ((-int(card_width()*0.5), 5), (int(card_width()*0.5), sh-5)))


    idpositions = ((sw/2, card_height()*0.75), (sw-card_width()*1.5+15, int(sh*(2/3.0))),
        (sw/2, sh-card_height()*0.75), (card_width()*0.75, int(sh*(2/3.0))))

    screen = pygame.display.get_surface()

    font = pygame.font.Font(None, 48)

    loading = font.render(_("Loading, please wait!"), 1, (255, 255, 255))

    screen.blit(loading, (450, 350))

    pygame.display.flip()

    suit1, temprect = fiftytwo.load_image('suit1.' + run.deck.deck + '.png', -1)
    suit2, temprect = fiftytwo.load_image('suit2.' + run.deck.deck + '.png', -1)
    suit3, temprect = fiftytwo.load_image('suit3.' + run.deck.deck + '.png', -1)
    suit4, temprect = fiftytwo.load_image('suit4.' + run.deck.deck + '.png', -1)

    deck = fiftytwo.cardgroup(fiftytwo.shuffledeck(), (sw / 6, (sh - card_height()) / 2),
        (sw / 6 + sw / 4, (sh + card_height()) / 2))
    discard = fiftytwo.cardgroup((), (sw - int(card_width()*3), (sh - card_height()) / 2),
        (sw - int(card_width()*1.5), (sh + card_height()) / 2))

    players = []

    num = -1

    for c in playertypes:
        num += 1

        if len(playertypes) == 2 and num == 1:
            num = 2

        if c[0] == 'l':
            players += [localplayer(positions[num])]
            players[-1].name = c[1:len(c)]
            players[-1].number = num
            players[-1].render_name()
            localplayers += 1

        elif c[0] == 'a':
            players += [aiplayer(positions[num])]
            players[-1].name = c[1:len(c)]
            players[-1].number = num
            players[-1].render_name()

    fpslimiter = pygame.time.Clock()

    #choosesuitimage, unused = fiftytwo.load_image('suits.' + run.deck.deck + '.png', -1)
    choosesuitimage = pygame.Surface((suit1.get_width()*2, suit1.get_height()*2))
    choosesuitimage.fill((255, 255, 255))
    choosesuitimage.set_colorkey((255, 255, 255), pygame.RLEACCEL)
    choosesuitimage.blit(suit1, (0, 0))
    choosesuitimage.blit(suit2, (suit1.get_width(), 0))
    choosesuitimage.blit(suit3, (0, suit1.get_height()))
    choosesuitimage.blit(suit4, (suit1.get_width(), suit1.get_height()))

    fiftytwo.draw_card(deck, discard)
    cardprocessed = 0
    currentsuit = discard.sprites()[0].cardid[1]
    discard.sprites()[0].set_face(UP)

    for p in players:
        for x in range(0, 8):
            fiftytwo.draw_card(deck, p)
            p.sprites()[-1].set_face(UP)


    whosturn = random.randint(0, len(playertypes)-1)

    for p in players:
        if p.type == LOCALPLAYER:
            p.set_all_faces(UP)
        elif p.type == AIPLAYER:
            p.set_all_faces(DOWN)

    screen.fill(BGCOL)

    while running:
        fpslimiter.tick(20)

        # Check for win
        for x in players:
            if len(x.sprites()) == 0:
                screen.fill(BGCOL)
                gameover = font.render(_("Game over,"), 1, (0, 255, 255))
                m = _('%s won the game!')
                message = font.render(m % x.name, 1, (255, 255, 0))

                for p in players:
                    p.set_all_faces(UP)
                    p.next_frame(screen)
                    pygame.display.flip()

                for x in range(100):
                    fpslimiter.tick(15)

                    clear_prev(deck)
                    clear_prev(discard)
                    for p in players:
                        clear_prev(p)

                    deck.next_frame(screen)
                    discard.next_frame(screen)

                    for p in players:
                        p.next_frame(screen)

                    screen.fill((32, 64, 64), (((sw/2)-(600/2), (sh/2)-(100/2)), (600, 100)) )
                    screen.blit(gameover, ((sw/2)-((600/2)-((600-gameover.get_rect().w)/2)), (sh/2)-50))
                    screen.blit(message, ((sw/2)-((600/2)-((600-message.get_rect().w)/2)), (sh/2)))

                    pygame.display.flip()

                    for event in pygame.event.get():
                        if event.type == KEYDOWN:
                            if event.key == K_ESCAPE:
                                return

                return

        if len(deck.sprites()) is 0:
            while len(discard.sprites()) > 1:
                sprite = discard.sprites()[0]
                sprite.set_face(DOWN)
                sprite.move_to_group(deck)

            deck.shuffle()

        while Gtk.events_pending():
            Gtk.main_iteration()

        if not running:
            break

        for event in pygame.event.get():

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return
                elif event.key == K_SPACE:
                    for s in discard.sprites():
                        s.set_pos(s.gotox, s.gotoy)

                    for s in deck.sprites():
                        s.set_pos(s.gotox, s.gotoy)

                    for p in players:
                        for s in p.sprites():
                            s.set_pos(s.gotox, s.gotoy)

                    screen.fill(BGCOL)

            elif event.type == MOUSEBUTTONDOWN:
                if players[whosturn].type != LOCALPLAYER:
                    continue
                r = players[whosturn].detect_click(event.pos)
                if r is not None:
                    if check_valid(discard.sprites()[-1].cardid, r.cardid, currentsuit):
                        r.move_to_group(discard)
                        whosturn = end_turn(players, whosturn)

                        currentsuit = discard.sprites()[-1].cardid[1]

                        cardprocessed = 0
                else:
                    r = deck.detect_click(event.pos)
                    if r is not None and players[whosturn].type == LOCALPLAYER:
                        fiftytwo.draw_card(deck, players[whosturn])
                        players[whosturn].sprites()[-1].set_face(UP)
                        whosturn = end_turn(players, whosturn)

            elif event.type == QUIT:
                running = False
                return running

            """elif event.type == olpcgames.CONNECT:
                print "Connect event."
                pass

            elif event.type == olpcgames.PARTICIPANT_ADD:
                print "Add event."
                pass

            elif event.type == olpcgames.PARTICIPANT_REMOVE:
                print "Remove event."
                pass"""

        if players[whosturn].ai is 1 and cardprocessed is 1:
            cready = 1

            for p in players:
                if p.check_ready() == 0:
                    cready = 0

            if discard.check_ready() == 0:
                cready = 0

            if deck.check_ready() == 0:
                cready = 0

            if cready == 1:
                r = players[whosturn].next_turn(discard.sprites()[-1].cardid, currentsuit)
                if r is None:
                    fiftytwo.draw_card(deck, players[whosturn])
                    whosturn = end_turn(players, whosturn)
                else:
                    r.move_to_group(discard)
                    r.set_face(UP)
                    cardprocessed = 0
                    whosturn = end_turn(players, whosturn)
                    currentsuit = r.cardid[1]

        # Gameplay stuff

        cardprocessed, whosturn, currentsuit = special_cards(deck, discard, players, whosturn, cardprocessed, choosesuitimage, currentsuit)

        clear_prev(deck)
        clear_prev(discard)
        for p in players:
            #p.sort()
            clear_prev(p)

        if currentsuit == '1':
            screen.fill(BGCOL, (((sw/2)-(suit1.get_width()/2), (sh/2)-(suit1.get_height()/2)), (suit1.get_width(), suit1.get_height())))
            screen.blit(suit1, ((sw/2)-(suit1.get_width()/2), (sh/2)-(suit1.get_height()/2)))
        elif currentsuit == '2':
            screen.fill(BGCOL, (((sw/2)-(suit2.get_width()/2), (sh/2)-(suit2.get_height()/2)), (suit2.get_width(), suit2.get_height())))
            screen.blit(suit2, ((sw/2)-(suit2.get_width()/2), (sh/2)-(suit2.get_height()/2)))
        elif currentsuit == '3':
            screen.fill(BGCOL, (((sw/2)-(suit3.get_width()/2), (sh/2)-(suit3.get_height()/2)), (suit3.get_width(), suit3.get_height())))
            screen.blit(suit3, ((sw/2)-(suit3.get_width()/2), (sh/2)-(suit3.get_height()/2)))
        elif currentsuit == '4':
            screen.fill(BGCOL, (((sw/2)-(suit4.get_width()/2), (sh/2)-(suit4.get_height()/2)), (suit4.get_width(), suit4.get_height())))
            screen.blit(suit4, ((sw/2)-(suit4.get_width()/2), (sh/2)-(suit4.get_height()/2)))

        deck.next_frame(screen)
        for p in players:
            p.next_frame(screen)
            screen.blit(p.id, idpositions[p.number])

        discard.next_frame(screen)

        pygame.display.flip()
