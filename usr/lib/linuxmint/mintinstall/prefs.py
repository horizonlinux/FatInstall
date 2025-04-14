#!/usr/bin/python3

import gettext

from gi.repository import Gtk

from xapp.SettingsWidgets import SettingsPage, Text
from xapp.GSettingsWidgets import GSettingsSwitch, GSettingsComboBox

# GSettings
SCHEMA_ID = "com.linuxmint.install"

SEARCH_IN_SUMMARY = "search-in-summary"
SEARCH_IN_DESCRIPTION = "search-in-description"
INSTALLED_APPS = "installed-apps"
SEARCH_IN_CATEGORY = "search-in-category"
HAMONIKR_SCREENSHOTS = "hamonikr-screenshots"
ALLOW_UNVERIFIED_FLATPAKS = "allow-unverified-flatpaks"

_ = gettext.gettext

class PrefsWidget(Gtk.Box):
    def __init__(self, warning_box):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(box)

        # Settings
        page = SettingsPage()
        box.pack_start(page, True, True, 0)

        section = page.add_section(_("General search options"))

        widget = GSettingsSwitch(_("Search in packages summary (slower search)"), SCHEMA_ID, SEARCH_IN_SUMMARY)
        section.add_row(widget)
        widget = GSettingsSwitch(_("Search in packages description (even slower search)"), SCHEMA_ID, SEARCH_IN_DESCRIPTION)
        section.add_row(widget)

        section = page.add_section(_("Flatpaks"))


        widget = GSettingsSwitch(_("Show unverified Flatpaks (not recommended)"), SCHEMA_ID, ALLOW_UNVERIFIED_FLATPAKS)
        section.add_row(widget)

        section.add(warning_box)

        self.show_all()
