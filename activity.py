#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys

import gtk
from sugar.activity import activity
from sugar.graphics.toolbarbox import ToolbarBox
from sugar.graphics.toolbutton import ToolButton
from sugar.activity.widgets import ActivityToolbarButton
from sugar.activity.widgets import StopButton
from sugar.graphics.toolbarbox import ToolbarButton
from sugar.graphics.objectchooser import ObjectChooser
from sugar.datastore import datastore
import sugargame.canvas

import run

from gettext import gettext as _

class Activity(activity.Activity):

    def __init__(self, handle):
        activity.Activity.__init__(self, handle)

        self._activity = run.Game(self)
        self.build_toolbar()
        self._pygamecanvas = sugargame.canvas.PygameCanvas(self)
        self.set_canvas(self._pygamecanvas)
        self._pygamecanvas.run_pygame(self._activity.loop)

    def build_toolbar(self):
        toolbar_box = ToolbarBox()
        self.set_toolbar_box(toolbar_box)
        toolbar_box.show()

        activity_button = ActivityToolbarButton(self)
        toolbar_box.toolbar.insert(activity_button, -1)
        activity_button.show()


        separator = gtk.SeparatorToolItem()
        separator.props.draw = False
        separator.set_expand(True)
        toolbar_box.toolbar.insert(separator, -1)
        separator.show()

        stop_button = StopButton(self)
        toolbar_box.toolbar.insert(stop_button, -1)
        stop_button.show()

        self.show_all()

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
                gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT)
        if chooser is not None:
            try:
                result = chooser.run()
                if result == gtk.RESPONSE_ACCEPT:
                    jobject = chooser.get_selected_object()
                    if jobject and jobject.file_path:
                        name = jobject.metadata['title']
                        #mime_type = jobject.metadata['mime_type']
                        #_logger.debug('result of choose: %s (%s)' % \(name, str(mime_type)))
            finally:
                chooser.destroy()
                del chooser
        
        return jobject
