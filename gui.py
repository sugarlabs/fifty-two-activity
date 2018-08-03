#! /usr/bin/env python
# -*- coding: utf-8 -*-

############################################################################
#    Copyright (C) 2007 by kawk                                            #
#    kawk@theprogrammingsite.com                                           #
#                                                                          #
#    This file is a generic GUI library for the FiftyTwo card game set.    #
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
#    along with this library; if not, write to the Free Software           #
#    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301 #
#    USA                                                                   #
############################################################################

import pygame
from pygame.locals import *

from gettext import gettext as _

import fiftytwo

class widget(pygame.sprite.Sprite):
    def __init__(self, position, size):
        pygame.sprite.Sprite.__init__(self)
        self.visible = 0
        self.rect = Rect(((0, 0), (0, 0)))
        self.rect.move_ip(position)
        self.rect.w = size[0]
        self.rect.h = size[1]
        self.special = 0

    def detect_click(self, mouseposition):
        if mouseposition[0] > self.rect.left and mouseposition[0] < self.rect.right:
            if mouseposition[1] > self.rect.top and mouseposition[1] < self.rect.bottom:
                return True

        return False

class container(pygame.sprite.OrderedUpdates):
    def __init__(self, widgets, position, size):
        pygame.sprite.OrderedUpdates.__init__(self, widgets)
        self.rect = Rect((position, size))

    def draw(self, surface, mouseposition):
        for s in self.sprites():
            if s.special and mouseposition[0] > s.rect.left and mouseposition[0] < s.rect.right \
                and mouseposition[1] > s.rect.top and mouseposition[1] < s.rect.bottom:
                    if mouseposition[2] is not 0:
                        surface.blit(s.clickimage, s.rect)
                    else:
                        surface.blit(s.hoverimage, s.rect)
            else:
                surface.blit(s.image, s.rect)

class label(widget):
    def __init__(self, position, size, title, color, textsize=38):
        widget.__init__(self, position, size)
        font = pygame.font.Font(None, textsize)
        self.image = font.render(title, 1, color)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]


class image(widget):
    def __init__(self, position, size, file, trans=None):
        widget.__init__(self, position, size)
        self.image, self.rect = fiftytwo.load_image(file, trans)
        self.rect.x = position[0]
        self.rect.y = position[1]
        self.rect.w = size[0]
        self.rect.h = size[1]

class button(widget):
    def __init__(self, position, size, title):
        widget.__init__(self, position, size)
        self.special = 1
        self.label = label(position, size, title, (255, 255, 255))
        self.image = pygame.Surface(size)
        self.hoverimage = pygame.Surface(size)
        self.clickimage = pygame.Surface(size)
        leftrect = self.image.get_rect()
        leftrect.x = 0
        leftrect.y = 0
        leftrect.w = 32
        leftrect.h = size[1]
        pygame.draw.ellipse(self.image, (128, 128, 128), leftrect)
        pygame.draw.ellipse(self.hoverimage, (176, 176, 176), leftrect)
        pygame.draw.ellipse(self.clickimage, (208, 208, 208), leftrect)
        leftrect.x = size[0]-32
        pygame.draw.ellipse(self.image, (128, 128, 128), leftrect)
        pygame.draw.ellipse(self.hoverimage, (176, 176, 176), leftrect)
        pygame.draw.ellipse(self.clickimage, (208, 208, 208), leftrect)
        self.image.fill((128, 128, 128), ((16, 0), (size[0]-32, size[1])))
        self.hoverimage.fill((176, 176, 176), ((16, 0), (size[0]-32, size[1])))
        self.clickimage.fill((208, 208, 208), ((16, 0), (size[0]-32, size[1])))
        self.image.blit(self.label.image, (10, 4))
        self.hoverimage.blit(self.label.image, (10, 4))
        self.clickimage.blit(self.label.image, (10, 4))
        self.image.set_colorkey((0, 0, 0), pygame.RLEACCEL)
        self.hoverimage.set_colorkey((0, 0, 0), pygame.RLEACCEL)
        self.clickimage.set_colorkey((0, 0, 0), pygame.RLEACCEL)

class frame(container):
    def __init__(self, widgets, position, size):
        container.__init__(self, widgets, position, size)

    def draw(self, surface, mouseposition):
        container.draw(self, surface, mouseposition)
        pygame.draw.rect(surface, (32, 32, 32), self.rect, 5)

class popup(frame):
    def __init__(self, widgets, position, size):
        frame.__init__(self, widgets, position, size)

    def draw(self, surface, mouseposition):
        surface.fill((48, 48, 48), self.rect)
        frame.draw(self, surface, mouseposition)
