import gi
import os

gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, GLib, Gio, Gdk, GdkPixbuf, Gst

# Inicializar el subsistema de multimedia de GStreamer
Gst.init(None)


class PomodoroTimer(Gtk.Window):
    """Ventana principal de la aplicación"""

    def __init__(self):
        Gtk.Window.__init__(self, title="Pomodoro Timer")
        self.set_resizable(False)
        # self.set_position(Gtk.WindowPosition.CENTER)
        # self.set_border_width(15)

        # Crear una caja vertical para los widgets
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(self.box)

        # Crear etiquetas y entradas para el tiempo de trabajo y descanso
        self.work_label = Gtk.Label(label="Work time (min):")
        self.box.append(self.work_label)

        self.work_entry = Gtk.Entry()
        self.work_entry.set_text("45")
        self.box.append(self.work_entry)

        self.rest_label = Gtk.Label(label="Rest time (min):")
        self.box.append(self.rest_label)

        self.rest_entry = Gtk.Entry()
        self.rest_entry.set_text("15")
        self.box.append(self.rest_entry)

        # Crear botones para iniciar y pausar el temporizador
        self.start_button = Gtk.Button(label="Start")
        self.start_button.connect("clicked", self.on_start_button_clicked)
        self.box.append(self.start_button)

        self.timer_label = Gtk.Label(label="00:00")
        self.timer_label.set_halign(Gtk.Align.CENTER)
        self.timer_label.override_font(Pango.FontDescription("Courier 30"))
        self.box.append(self.timer_label)

        self.pause_button = Gtk.Button(label="Pause")
        self.pause_button.connect("clicked", self.on_pause_button_clicked)
        self.pause_button.hide()
        self.box.append(self.pause_button)

    def on_start_button_clicked(self, button):
        """Inicia el temporizador Pomodoro"""
        self.running = True

        work_time = int(self.work_entry.get_text())
        rest_time = int(self.rest_entry.get_text())
        work_seconds = convert_to_seconds(work_time)
        rest_seconds = convert_to_seconds(rest_time)

        self.box.hide()
        self.start_button.hide()
        self.pause_button.show()
        clear_screen()

        GLib.timeout_add_seconds(0, self.countdown, work_seconds)
        GLib.timeout_add_seconds(work_seconds, self.countdown, rest_seconds)
        GLib.timeout_add_seconds(work_seconds + rest_seconds, self.box.show)
        GLib.timeout_add_seconds(work_seconds + rest_seconds, self.start_button.show)
        GLib.timeout_add_seconds(work_seconds + rest_seconds, self.pause_button.hide)

    def on_pause_button_clicked(self, button):
        """Pausa el temporizador"""
        self.running = False

    def countdown(self, t):
        """Cuenta atrás para el temporizador"""
        while t > 0:
            if not self.running:
                return False
            minutes, seconds = divmod(t, 60)
            update_timer_label(self.timer_label, minutes, seconds)
            t -= 1
            GLib.timeout_add_seconds(1, self.countdown, t)
            play_sound('clock_01.ogg')
        # Cuando se acaba el tiempo, se muestra un mensaje y se reproduce un sonido
        self.timer_label.set_text("Time's up!")
        play_sound(Gio.File.new_for_path(AUDIO_FILE).get_uri())
        return False


def main():
    """Función principal"""
    win = PomodoroTimer()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()


if __name__ == '__main__':
    running = False
    main()
