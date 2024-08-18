#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import pygame
import pygame.camera

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk

from sugar3.activity import activity
from sugar3.graphics.toolbarbox import ToolbarBox
from sugar3.activity.widgets import ActivityToolbarButton
from sugar3.activity.widgets import StopButton
from sugar3.graphics.objectchooser import ObjectChooser
from sugar3.graphics.style import GRID_CELL_SIZE

import sugargame.canvas

import run

from gettext import gettext as _

class Activity(activity.Activity):

    def __init__(self, handle):
        activity.Activity.__init__(self, handle)

        self.game = run.Game(self)
        self.build_toolbar()
        self.game.canvas = self._pygamecanvas = sugargame.canvas.PygameCanvas(
            self, main=self.game.run, modules=[pygame.display, pygame.font,
            pygame.camera])
        self.set_canvas(self._pygamecanvas)
        Gdk.Screen.get_default().connect('size-changed',
                                         self.__configure_cb)

    def __configure_cb(self, event):
        ''' Screen size has changed '''
        pygame.display.set_mode((Gdk.Screen.width(),
                                 Gdk.Screen.height() - GRID_CELL_SIZE),
                                pygame.RESIZABLE)

    def build_toolbar(self):
        toolbar_box = ToolbarBox()
        self.set_toolbar_box(toolbar_box)
        toolbar_box.show()

        activity_button = ActivityToolbarButton(self)
        toolbar_box.toolbar.insert(activity_button, -1)
        activity_button.show()

        separator = Gtk.SeparatorToolItem()
        separator.props.draw = False
        separator.set_expand(True)
        toolbar_box.toolbar.insert(separator, -1)
        separator.show()

        stop_button = StopButton(self)
        toolbar_box.toolbar.insert(stop_button, -1)
        stop_button.show()
        stop_button.connect('clicked', self._stop_cb)

        self.show_all()
    
    def _stop_cb(self, button):
        self.game.playing = False
        self.game.running = False

    def read_file(self, file_path):
        pass

    def write_file(self, file_path):
        pass

    def load_image_from_journal(self):
        chooser = None
        name = None
        jobject = None
        try:
            chooser = ObjectChooser(parent=self, what_filter=None)
        except TypeError:
            chooser = ObjectChooser(
                None, self,
                Gtk.DialogFlags.MODAL | 0)
        if chooser is not None:
            try:
                result = chooser.run()
                if result == Gtk.ResponseType.ACCEPT:
                    jobject = chooser.get_selected_object()
                    if jobject and jobject.file_path:
                        name = jobject.metadata['title']
                        #mime_type = jobject.metadata['mime_type']
                        #_logger.debug('result of choose: %s (%s)' % \(name, str(mime_type)))
            finally:
                chooser.destroy()
                del chooser
        
        return jobject
