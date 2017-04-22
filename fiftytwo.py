#! /usr/bin/env python
# -*- coding: utf-8 -*-

############################################################################
#    Copyright (C) 2007 by kawk                                            #
#    kawk@theprogrammingsite.com                                           #
#                                                                          #
#    This file is a generic card library for the FiftyTwo card game set.   #
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
#    59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.             #
############################################################################

import os
import sys
import math
import random
import pygame

from gettext import gettext as _

import run

cardnumbers = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
cardsuits = ('1', '2', '3', '4')

DOWN = 0
UP = 1

def card_width():
    """
    Returns the width of the cards.
    """
    return 156

def card_height():
    """
    Returns the height of the cards.
    """
    return 244

def load_image(name, colorkey=None):
    """
    Loads an image from a file.
    """
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
         'Cannot load image:', fullname
         print "Cannot load image: ", fullname
         return None, None
         #raise SystemExit, message
    
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, pygame.RLEACCEL)
    
    image = image.convert_alpha()
    return image, image.get_rect()

def load_card(xpos, ypos, cards):
    """
    Loads a card from a cardset.
    """
    
    cardrect = cards.get_rect()
    cardrect.w = card_width()
    cardrect.h = card_height()
    cardrect.x = xpos * (cards.get_rect().w/13.0)
    cardrect.y = ypos * (cards.get_rect().h/4.0)
    subsurface = cards.subsurface(cardrect)
    return subsurface

class card(pygame.sprite.Sprite):
    """
    A basic card class.
    """
    def __init__(self, cardid, cards):
        """
        Initialization function. 
        """
        pygame.sprite.Sprite.__init__(self)
        x = 0
        for n in cardnumbers:
            if n == cardid[0]:
                xpos = x
            
            x += 1
        
        x = 0
        
        for s in cardsuits:
            if s == cardid[1]:
                ypos = x
                
            x += 1
        
        self.image = load_card(xpos, ypos, cards)
        self.rect = self.image.get_rect()
        self.prevrect = self.rect
        self.gotox = selfgotoy = 0
        self.ready = 1
        self.face = DOWN
        self.cardid = cardid
        self._tcount = 0
    
    def update(self):
        """
        Updating function. Calculates next position from the most recent
        move_to() function call, then shifts position to there.
        """
        if self.ready:
            return self.rect
        
        self.prevrect = self.rect
        
        newx = (self.gotox - self.rect.x)/4
        newy = (self.gotoy - self.rect.y)/3
        
        if math.fabs((newx + self.rect.x) - self.gotox) < 4 and math.fabs((newy + self.rect.y) - self.gotoy) < 3:
            newx = (self.gotox - self.rect.x)
            newy = (self.gotoy - self.rect.y)
            self.ready = 1
        
        self.rect.move_ip(newx, newy)
        
        return self.prevrect
    
    def check_ready(self):
        """
        The variable self.ready is set to true if the card has reached the last position required by
        move_to(). This function simply returns the value of self.ready.
        """
        return self.ready
    
    def set_pos(self, xpos, ypos):
        """
        Sets the position of the card. Moves the card directly, no fancy animation or anything.
        """
        self.rect.move_ip(xpos - self.rect.x, ypos - self.rect.y)
        self.gotox = xpos
        self.gotoy = ypos
        self.ready = 1
    
    def move_to_group(self, newgroup):
        """
        Moves the card to a specified group. First it removes itself from all cardgroups,
        then adds itself to the new group.
        """
        self.kill()
        newgroup.add(self)
    
    def move_to(self, xpos, ypos):
        """
        Initiates fancy smooth moving of the card to a different position.
        """
        #self._tcount += 1
        #if(self._tcount == 10):
        #    print "OldX: ", self.rect.x, " OldY: ", self.rect.y, " NewX: ", xpos, " NewY: ", ypos
        #    self._tcount = 0
        #if self.rect.x == xpos and self.rect.y == ypos:
        #if(self.rect.y != ypos):
        #    print "Not equal: ", self.rect.y, " ", ypos
        
        #if math.fabs(self.rect.x-xpos) < 1.0 and math.fabs(self.rect.y-ypos) < 1.0:
        #    self.ready = 1
        #else:
        self.gotox = xpos
        self.gotoy = ypos
        self.ready = 0
    
    def set_face(self, face):
        """
        Sets the direction of the face of the card, either up or down.
        """
        self.face = face
    
    def flip(self):
        """
        Flips the card face from up to down, or from down to up.
        """
        if self.face == UP:
            self.set_face(DOWN)
        else:
            self.set_face(UP)
    
    def get_prevrect(self):
        """
        Returns the previous position of the card (required for dirty rectangle animation).
        """
        return self.prevrect          

class cardgroup(pygame.sprite.OrderedUpdates):
    def __init__(self, cards, ulpos, lrpos, visible = 1):
        """
        Init the cardgroup at a set position with a list of cards.
        """
        pygame.sprite.OrderedUpdates.__init__(self, cards)
        
        self.ulpos = ulpos
        self.lrpos = lrpos
        self.visible = visible
        self.blank_card = pygame.Surface((lrpos[0], lrpos[1]))
        self.blank_card.convert()
        self.blank_card.fill((0, 0, 0))
        temp = self.blank_card.get_rect()
        temp.move_ip(ulpos[0], ulpos[1])
        self.back, unused = load_image('back.' + run.deck.deck + '.png')
        if self.back is None:
            self.back, unused = load_image('back.' + run.deck.deck + '.tga')

        list = self.sprites()
        length = len(list)
        
        if length == 0:
            pass
        elif length == 1:
            self.sprites()[0].set_pos(self.ulpos[0], self.ulpos[1])
        else:
            xstep, ystep = self.calc_steps()
            
            num = 0
            while num < length:
                list[num].set_pos(self.ulpos[0] + num * xstep, self.ulpos[1] + num * ystep)
                num += 1

    
    def calc_steps(self):
        """
        Calculates the pixels between cards.
        """
        list = self.sprites()
        if len(list) <= 1:
            return 0, 0
        xstep = (self.lrpos[0] - self.ulpos[0] - card_width()) / (len(list) - 1.0)
        ystep = (self.lrpos[1] - self.ulpos[1] - card_height()) / (len(list) - 1.0)
        if xstep > card_width()/2:
            xstep = card_width()/2
        
        if ystep > card_height()/2:
            ystep = card_height()/2
        return xstep, ystep
    
    def update(self):
        """
        Moves the cards into the proper formation.
        """
        
        list = self.sprites()
        length = len(list)
        
        if length == 0:
            pass
        elif length == 1:
            self.sprites()[0].move_to(self.ulpos[0], self.ulpos[1])
        else:
            xstep, ystep = self.calc_steps()
            
            num = 0
            while num < length:
                list[num].move_to(self.ulpos[0] + num * xstep, self.ulpos[1] + num * ystep)                
                num += 1
        
        
        pygame.sprite.OrderedUpdates.update(self)
        
    
    def next_frame(self, surface):
        """
        Calculates, updates, and draws the next frame.
        """
        if self.visible == 0: return
        self.update()
        
        self.draw(surface)
    
    def draw(self, surface):
        """
        Draws the cardgroup.
        """
        #pygame.sprite.OrderedUpdates.draw(self, surface)
        xstep, unused = self.calc_steps()
        num = len(self.sprites())
        list = self.sprites()
        for x in range(len(list)):
            num -= 1
            rect = list[x].rect.move(0, 0)
            #rect.w = xstep 
            if num == 0:
                rect.w = card_width()
            
            elif list[x+1].rect.y == list[x].rect.y:
                rect.w = list[x+1].rect.x - list[x].rect.x
                if rect.w > card_width():
                    rect.w = card_width()
            
            elif list[x+1].rect.x == list[x].rect.x:
                rect.h = list[x+1].rect.y - list[x].rect.y
                if rect.h > card_height():
                    rect.h = card_height()
            
            #elif list[x-1].check_ready() == 0:
            #    rect.w = card_width()
                        
            rect.x = rect.y = 0
            if list[x].face == UP:
                surface.blit(list[x].image, list[x].rect, rect)
            else:
                surface.blit(self.back, list[x].rect, rect)
                #surface.fill((0, 0, 255), s.rect)

    
    def shuffle(self):
        """
        Shuffles the cardgroup, by switching random cards.
        """
        list = self.sprites()
        x = 0
        while x < len(list) - 1:
            pos = random.randint(0, x)
            
            t = list[pos]
            list[pos] = list[x + 1]
            list[x + 1] = t
            x += 1
        
        self.empty()
        self.add(list)
    
    def detect_click(self, mouseposition):
        """
        Detects what card the mouse is over, if any.
        """
        lrpos = self.newlr()
        
        if len(self.sprites()) is 0 or mouseposition[0] <= self.ulpos[0] or mouseposition[0] >= self.lrpos[0] or mouseposition[1] <= self.ulpos[1] or mouseposition[1] >= self.lrpos[1]:
            return None
        
        xstep, ystep = self.calc_steps()
        x = mouseposition[0]
        y = mouseposition[1]
        
        if (xstep == 0 and ystep == 0) or (lrpos[0]-x <= card_width() and lrpos[1]-y <= card_height()):
            return self.sprites()[-1]
        
        x += card_width()
        y += card_height()
        
        n = -2
        while lrpos[0]-x > xstep or lrpos[1]-y > ystep:
            n -= 1
            x += xstep
            y += ystep
        
        if n > len(self.sprites()):
            return None
                
        n = int(math.fmod(math.fabs(n), len(self.sprites())) * (n / math.fabs(n)))
                
        return self.sprites()[n]
    
    def set_all_faces(self, face):
        for s in self.sprites():
            s.set_face(face)
    
    def sort(self):
        list = self.sprites()
        if len(list) == 0:
            return
        
        newlist = [list[0]]
        did = 0
        
        for c in range(1, len(list)):
            best = -1
            for n in range(len(newlist)):
                #if list[c].cardid[1] >= newlist[n].cardid[1]:
                #    if best == -1:
                #        best = n
                #    
                #    newlist.insert(best, list[c])
                #    did = 1
                #    break
                if list[c].cardid[1] == newlist[n].cardid[1]:
                    cn = cardnumbers.find(list[c].cardid[0])
                    nn = cardnumbers.find(newlist[n].cardid[0])
                    if cn < nn:
                        best = n
                    #elif cn >= nn:
                    #    if best == -1:
                    #        best = n
                    #    
                    #    newlist.insert(best, list[c])
                    #    did = 1
                    #    break
            if 1: #did == 0:
                if best == -1:
                    newlist.append(list[c])
                else:
                    newlist.insert(best, list[c])
        
        
        for s in self.sprites():
            s.kill()
        
        for n in newlist:
            self.add(n)
    
    def check_ready(self):
        ready = 1
        for s in self.sprites():
            if s.check_ready() == 0:
                return 0
        
        return 1
    
    def newlr(self):
        rect = self.sprites()[-1].rect
        return rect.right, rect.bottom
    

def shuffledeck():
    """
    Loads and shuffles the deck of cards.
    """
    cardset, unused = load_image('cards.' + run.deck.deck + '.png')
        
    decklist = []

    for s in cardsuits:
        for n in cardnumbers:
            num = random.randint(0, len(decklist))
            decklist.insert(num, card(n+s, cardset))
    return decklist

def draw_card(deck, group):
    """
    Draws the top card from the cardgroup and moves it to another.
    """
    temp = deck.sprites()
    if len(temp) < 1:
        return None
    
    drawncard = temp[-1]
    drawncard.kill()
    group.add(drawncard)
