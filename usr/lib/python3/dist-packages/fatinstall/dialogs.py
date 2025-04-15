import gi
gi.require_version('XApp', '1.0')
from gi.repository import GLib, Gtk, GObject, Gdk, XApp, Pango

import gettext
APP = 'mint-common'
LOCALE_DIR = "/usr/share/linuxmint/locale"
t = gettext.translation(APP, LOCALE_DIR, fallback=True)
_ = t.gettext

#from aptdaemon.gtk3widgets import AptConfirmDialog

######################### Subclass Apt's dialog to keep consistency

class FlatpakProgressWindow(Gtk.Dialog):
    """
    Progress dialog for standalone flatpak installs, removals, updates.
    Intended to be used when not working as part of a parent app (like mintinstall)
    """

    def __init__(self, task, parent=None):
        Gtk.Dialog.__init__(self, parent=parent)
        self.set_default_size(400, 140)
        self.task = task
        self.finished = False

        # Progress goes directly to this window
        task.client_progress_cb = self.window_client_progress_cb

        # finished callbacks route thru the installer
        # but we want to see them in this window also.
        self.final_finished_cb = task.client_finished_cb
        task.client_finished_cb = self.window_client_finished_cb
        self.pulse_timer = 0

        self.real_progress_text = None

        # Setup the dialog
        self.set_border_width(6)
        self.set_resizable(False)
        self.get_content_area().set_spacing(6)
        # Setup the cancel button
        self.button = Gtk.Button.new_from_stock(Gtk.STOCK_CANCEL)
        self.button.set_use_stock(True)
        self.get_action_area().pack_start(self.button, False, False, 0)
        self.button.connect("clicked", self.on_button_clicked)
        self.button.show()

        # labels and progressbar
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        vbox.set_spacing(12)
        vbox.set_border_width(10)

        self.label = Gtk.Label(max_width_chars=45)
        vbox.pack_start(self.label, False, False, 0)
        self.label.set_halign(Gtk.Align.START)
        self.label.set_line_wrap(True)

        self.progress = Gtk.ProgressBar()
        vbox.pack_end(self.progress, False, True, 0)
        self.get_content_area().pack_start(vbox, True, True, 0)

        self.set_title(_("Flatpak"))
        XApp.set_window_icon_name(self, "system-software-installer")

        vbox.show_all()
        self.realize()

        self.progress.set_size_request(350, -1)
        functions = Gdk.WMFunction.MOVE | Gdk.WMFunction.RESIZE
        try:
            self.get_window().set_functions(functions)
        except TypeError:
            # workaround for older and broken GTK typelibs
            self.get_window().set_functions(Gdk.WMFunction(functions))

        # catch ESC and behave as if cancel was clicked
        self.connect("delete-event", self._on_dialog_delete_event)

    def start_progress_pulse(self):
        if self.pulse_timer > 0:
            return

        self.progress.pulse()
        self.pulse_timer = GObject.timeout_add(1050, self.progress_pulse_tick)

    def progress_pulse_tick(self):
        self.progress.pulse()

        return GLib.SOURCE_CONTINUE

    def stop_progress_pulse(self):
        if self.pulse_timer > 0:
            GObject.source_remove(self.pulse_timer)
            self.pulse_timer = 0

    def _on_dialog_delete_event(self, dialog, event):
        self.button.clicked()
        return True

    def window_client_progress_cb(self, pkginfo, progress, estimating, status_text):
        if estimating:
            self.start_progress_pulse()
        else:
            self.stop_progress_pulse()

            self.progress.set_fraction(progress / 100.0)
            XApp.set_window_progress(self, progress)

        self.label.set_text(status_text)

    def window_client_finished_cb(self, task):
        self.finished = True

        self.destroy()
        self.final_finished_cb(task)

    def on_button_clicked(self, button):
        if not self.finished:
            self.task.cancel()

def show_error(message, parent_window=None):
    Gdk.threads_add_idle(GLib.PRIORITY_DEFAULT_IDLE, _show_error_mainloop, message, parent_window)

def _show_error_mainloop(message, parent_window):
    dialog = Gtk.MessageDialog(None,
                               Gtk.DialogFlags.DESTROY_WITH_PARENT,
                               Gtk.MessageType.ERROR,
                               Gtk.ButtonsType.OK,
                               "")
    if parent_window is not None:
        dialog.set_transient_for(parent_window)
        dialog.set_modal(True)
    dialog.set_title(GLib.get_application_name())

    text = _("An error occurred")
    dialog.set_markup("<big><b>%s</b></big>" % text)

    scroller = Gtk.ScrolledWindow(min_content_height = 75, max_content_height=400, min_content_width=400, propagate_natural_height=True)
    dialog.get_message_area().pack_start(scroller, False, False, 8)

    message_label = Gtk.Label(message, lines=20, wrap=True, wrap_mode=Pango.WrapMode.WORD_CHAR, selectable=True)
    message_label.set_max_width_chars(60)
    message_label.show()
    scroller.add(message_label)

    dialog.show_all()
    dialog.run()
    dialog.destroy()

    return GLib.SOURCE_REMOVE

