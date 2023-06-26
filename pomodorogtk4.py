import gi
import os

gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, GLib, Gio, Gdk, GdkPixbuf, Gst

Gst.init(None)

def load_gtk():
    try:
        gi.require_version('Gtk', '4.0')
        from gi.repository import Gtk, GLib, Pango
        return Gtk, GLib, Pango
    except:
        gi.require_version('Gtk', '3.0')
        from gi.repository import Gtk, GLib, Pango
        return Gtk, GLib, Pango

Gtk, GLib, Pango = load_gtk()

AUDIO_FILE = 'clock_01.ogg'

def clear_screen():
    """Limpia la pantalla"""
    os.system("clear||cls")

def convert_to_seconds(t):
    """Convierte minutos a segundos"""
    return t * 60

def update_timer_label(label, minutes, seconds):
    """Actualiza la etiqueta del temporizador"""
    label.set_text(f"{minutes:02d}:{seconds:02d}")

def play_sound(sound_uri):
    """Reproduce un archivo de sonido"""
    player = Gst.ElementFactory.make("playbin", "player")
    player.set_property("uri", sound_uri)
    player.set_state(Gst.State.PLAYING)

def countdown(t, label):
    """Cuenta atrás para el temporizador"""
    while t > 0:
        if not running:
            return False
        minutes, seconds = divmod(t, 60)
        update_timer_label(label, minutes, seconds)
        t -= 1
        GLib.timeout_add_seconds(1, countdown, t, label)
        play_sound(clock_01.ogg)
    # Cuando se acaba el tiempo, se muestra un mensaje y se reproduce un sonido
    label.set_text("Time's up!")
    play_sound(Gio.File.new_for_path(AUDIO_FILE).get_uri())
    return False

def pause_timer(button):
    """Pausa el temporizador"""
    global running
    running = False

def start_pomodoro(button, work_entry, rest_entry, work_box, start_button, pause_button, timer_label):
    """Inicia el temporizador Pomodoro"""
    global running
    running = True

    work_time = int(work_entry.get_text())
    rest_time = int(rest_entry.get_text())
    work_seconds = convert_to_seconds(work_time)
    rest_seconds = convert_to_seconds(rest_time)

    work_box.hide()
    start_button.hide()
    pause_button.show()
    clear_screen()

    GLib.timeout_add_seconds(0, countdown, work_seconds, timer_label)
    GLib.timeout_add_seconds(work_seconds, countdown, rest_seconds, timer_label)
    GLib.timeout_add_seconds(work_seconds + rest_seconds, work_box.show)
    GLib.timeout_add_seconds(work_seconds + rest_seconds, start_button.show)
    GLib.timeout_add_seconds(work_seconds + rest_seconds, pause_button.hide)

def main():
    """Función principal"""
    window = Gtk.Window(title="Pomodoro Timer")
    window.set_resizable(False)
    window.set_application(Gtk.WindowPosition.CENTER)
    window.set_border_width(15)

    work_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    window.add(work_box)

    work_label = Gtk.Label(label="Work time (min):")
    work_box.append(work_label)

    work_entry = Gtk.Entry()
    work_entry.set_text("45")
    work_box.append(work_entry)

    rest_label = Gtk.Label(label="Rest time (min):")
    work_box.append(rest_label)

    rest_entry = Gtk.Entry()
    rest_entry.set_text("15")
    work_box.append(rest_entry)

    start_button = Gtk.Button(label="Start")
    start_button.connect("clicked", start_pomodoro, work_entry, rest_entry, work_box, start_button, pause_button, timer_label)
    work_box.append(start_button)

    timer_label = Gtk.Label(label="00:00")
    timer_label.set_halign(Gtk.Align.CENTER)
    timer_label.override_font(Pango.FontDescription("Courier 30"))
    work_box.append(timer_label)

    pause_button = Gtk.Button(label="Pause")
    pause_button.connect("clicked", pause_timer)
    pause_button.hide()
    work_box.append(pause_button)

    window.show_all()
    Gtk.main()

if __name__ == '__main__':
    running = False
    main()
