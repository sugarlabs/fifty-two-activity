#! /usr/bin/env python3
# -*- coding: utf-8 -*-

############################################################################
#    Copyright (C) 2007 by kawk                                            #
#    kawk@theprogrammingsite.com                                           #
#                                                                          #
#    This file is the main menu for the FiftyTwo card game set.            #
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
import pygame
import pygame.camera
import pygame.time

gi.require_version('Gtk','3.0')
from gi.repository import Gtk
from sugar3.graphics.style import GRID_CELL_SIZE

from gettext import gettext as _

import gui
import crazyeights



#CARDBACK_IMAGE = 'back.regular.png'
#DECK_IMAGE = 'cards.regular.png'

MMCOL = (192, 64, 255)

class deckinfoclass():
    def __init__(self):
        self.deck = 'regular'

deck = deckinfoclass()

class Game():

    def __init__(self, parent):
        self.parent = parent
        pass

    def run(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.VIDEORESIZE:
                pygame.display.set_mode(
                    (event.size[0], event.size[1] - GRID_CELL_SIZE),
                    pygame.RESIZABLE)
                break
        pygame.init()

        self.screen = pygame.display.get_surface()
        if self.screen:
            self.screensize = self.screen.get_size()
        else:
            info = pygame.display.Info()
            self.screensize = (info.current_w, info.current_h)
            self.screen = pygame.display.set_mode(self.screensize)

        screensize = self.screensize

        decksel = False
        c8sheader = gui.label((100, 300), (200, 75), _('Crazy Eights'), (0, 128, 0))
        c8s2p = gui.button((100, 400), (200, 35), _("Two players"))
        c8s3p = gui.button((100, 450), (200, 35), _("Three players"))
        c8s4p = gui.button((100, 500), (200, 35), _("Four players"))

        c8sframe = gui.frame((c8sheader, c8s2p, c8s3p, c8s4p), (75, 275), (250, 275))

        maindeck = gui.button((50, screensize[1]-75), (85, 35), _("Deck"))
        mainphoto = gui.button((screensize[0]-200, screensize[1]-75), (160, 35), _("Photo deck"))
        mainheader = gui.image((50, 25), (screensize[0]-100, 200), 'fiftytwo.png', -1)

        mainframe = gui.frame((mainheader, maindeck, mainphoto), (25, screensize[1]-100), (screensize[0]-50, 75))

        deckselexit = gui.button((screensize[0]-215, screensize[1]-145), (115, 35), _("Cancel"))
        deckfromjournal = gui.button((screensize[0]-445, screensize[1]-145), (200, 35), _("from Journal"))
        deckselregular = gui.image((115, 115), (crazyeights.card_width(), crazyeights.card_height()), 'back.regular.png')
        deckselgnome = gui.image((300, 115), (crazyeights.card_width(), crazyeights.card_height()), 'back.gnome.png')
        deckselparis = gui.image((485, 115), (crazyeights.card_width(), crazyeights.card_height()), 'back.paris.png')
        deckselshapes = gui.image((670, 115), (crazyeights.card_width(), crazyeights.card_height()), 'back.shapes.png')
        self.deckseluser = gui.image((855, 115), (crazyeights.card_width(), crazyeights.card_height()), 'back.user.png')

        deckselpopup = gui.popup((deckselexit, deckfromjournal, deckselregular, deckselgnome, deckselparis, deckselshapes, self.deckseluser), (100, 100), (screensize[0]-200, screensize[1]-200))

        mouseposition = [0, 0, 0]

        self.screen.fill((192, 64, 255))

        # Set the name of the players
        names = []
        names.append('l' + _('You'))
        names.append('a' + _('XO player #1'))
        names.append('a' + _('XO player #2'))
        names.append('a' + _('XO player #3'))
        names.append('a' + _('The XO'))

        fpslimiter = pygame.time.Clock()
        self.playing = True

        while self.playing:
            fpslimiter.tick(20)

            while Gtk.events_pending():
                Gtk.main_iteration()

            for event in pygame.event.get():

                if event.type == pygame.MOUSEMOTION:
                    mouseposition[0] = event.pos[0]
                    mouseposition[1] = event.pos[1]
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouseposition[2] = 1
                elif event.type == pygame.MOUSEBUTTONUP:
                    mouseposition[2] = 0
                    if not decksel and c8s2p.detect_click(event.pos):
                        crazyeights.main((names[4], names[0]), screensize)
                        self.screen.fill(MMCOL)
                        pygame.event.set_allowed(pygame.MOUSEMOTION)
                    elif not decksel and  c8s3p.detect_click(event.pos):
                        crazyeights.main((names[1], names[2], names[0]), screensize)
                        self.screen.fill(MMCOL)
                        pygame.event.set_allowed(pygame.MOUSEMOTION)
                    elif not decksel and  c8s4p.detect_click(event.pos):
                        crazyeights.main((names[1], names[2], names[0], names[3]), screensize)
                        self.screen.fill(MMCOL)
                        pygame.event.set_allowed(pygame.MOUSEMOTION)
                    elif not decksel and maindeck.detect_click(event.pos):
                        decksel = True
                    elif not decksel and mainphoto.detect_click(event.pos):
                        self.photo()
                        self.screen.fill(MMCOL)
                    elif decksel and deckselexit.detect_click(event.pos):
                        decksel = False
                        self.screen.fill(MMCOL)
                    elif decksel and deckfromjournal.detect_click(event.pos):
                        picture = self.parent.load_image_from_journal()
                        if picture:
                            self.update_user_deck(picture.file_path)
                        self.screen.fill(MMCOL)
                    elif decksel and deckselgnome.detect_click(event.pos):
                        deck.deck = 'gnome'
                        decksel = False
                        self.screen.fill(MMCOL)
                    elif decksel and deckselregular.detect_click(event.pos):
                        deck.deck = 'regular'
                        decksel = False
                        self.screen.fill(MMCOL)
                    elif decksel and deckselparis.detect_click(event.pos):
                        deck.deck = 'paris'
                        decksel = False
                        self.screen.fill(MMCOL)
                    elif decksel and deckselshapes.detect_click(event.pos):
                        deck.deck = 'shapes'
                        decksel = False
                        self.screen.fill(MMCOL)
                    elif decksel and self.deckseluser.detect_click(event.pos):
                        deck.deck = 'user'
                        decksel = False
                        self.screen.fill(MMCOL)


            if not decksel:
                c8sframe.update()
                c8sframe.draw(self.screen, mouseposition)

                mainframe.update()
                mainframe.draw(self.screen, mouseposition)
            else:
                deckselpopup.update()
                deckselpopup.draw(self.screen, mouseposition)

            pygame.display.flip()

    def flush_queue(self):
        flushing = True
        while flushing:
            flushing = False
            while Gtk.events_pending():
                Gtk.main_iteration()
            for event in pygame.event.get():
                flushing = True

    def photo(self):
        screensize = self.screensize
        mouseposition = [0, 0, 0]
        self.screen = pygame.display.get_surface()
        fpslimiter = pygame.time.Clock()
        photodynamic = gui.image((125, 125), (640, 480), 'back.regular.png')
        photoreturn = gui.button((screensize[0]-300, screensize[1]-175), (150, 35), _("Cancel"))
        photopopup = gui.popup((photodynamic, photoreturn), (100, 100), (screensize[0]-200, screensize[1]-200))

        pygame.camera.init()
        cams = pygame.camera.list_cameras()
        if cams:
            photocamera = pygame.camera.Camera(cams[0], (640, 480), 'RGB')
            photocamera.start()
            photocamera.set_controls(True, False)
            camera_size = photocamera.get_size()
            capture = pygame.surface.Surface(camera_size, 0, self.screen)
            photodynamic.image = photocamera.get_image(capture)

            self.running = True

            while self.running:
                fpslimiter.tick(20)

                photodynamic.image = photocamera.get_image(capture)

                while Gtk.events_pending():
                    Gtk.main_iteration()

                for event in pygame.event.get():

                    """if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            photodynamic.image = photocamera.get_image(capture)"""
                    if event.type == pygame.MOUSEMOTION:
                        mouseposition[0] = event.pos[0]
                        mouseposition[1] = event.pos[1]
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        mouseposition[2] = 1
                        self.flush_queue()
                    elif event.type == pygame.MOUSEBUTTONUP:
                        mouseposition[2] = 0
                        if photoreturn.detect_click(event.pos):
                            self.running = False
                        elif photodynamic.detect_click(event.pos):
                            r = photodynamic.image.get_rect()
                            r.x = mouseposition[0]-125
                            r.y = mouseposition[1]-125
                            r.w = 156
                            r.h = 244
                            sub = photodynamic.image.subsurface(r)
                            # borde negro
                            pygame.draw.rect(sub, (0,0,0), (0,0,r.w,r.h), 3)
                            pygame.image.save(sub, 'data/back.user.png')
                            self.deckseluser.image = sub
                            deck.deck = 'user'
                            self.running = False

                photopopup.update()
                photopopup.draw(self.screen, mouseposition)
                r = self.screen.get_rect()
                r.x = 125
                r.y = 125
                r.w = 640
                r.h = 480
                self.screen.set_clip(r)

                r.x = mouseposition[0]
                r.y = mouseposition[1]
                r.w = 156
                r.h = 244

                pygame.draw.rect(self.screen, (255, 0, 0), r, 4)
                self.screen.set_clip()

                pygame.display.flip()

            photocamera.stop()

    def update_user_deck(self, path):
        try:
            raw_deck = pygame.image.load(path)
            deck = pygame.transform.scale(raw_deck, (156, 244))
            pygame.image.save(deck, 'data/back.user.png')
            self.deckseluser.image = deck
        except:
            pass

