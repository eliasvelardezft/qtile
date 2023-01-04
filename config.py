# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import subprocess, os

from typing import List  # noqa: F401

from libqtile import bar, layout, widget, hook, qtile
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

mod = "mod4"
terminal = "kitty"
browser = "brave-browser"

##### HOOKS #####
# @hook.subscribe.startup_once
# def autostart():
#     qtile.cmd_spawn("compton --opacity-rule \"99:class_g='kitty'\"")




keys = [
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(),
        desc="Move window focus to other window"),

    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(),
        desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(),
        desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(),
        desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),

    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(),
        desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(),
        desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(),
        desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack"),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch kitty"),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),

    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(),
        desc="Spawn a command using a prompt widget"),
]

##### COLORS #####
colors = [
    ["#282c34", "#282c34"], # panel background
    ["#3d3f4b", "#434758"], # background for current screen tab
    ["#ffffff", "#ffffff"], # font color for group names
    ["#eb7b6c", "#eb7b6c"], # border line color for current tab
    ["#74438f", "#74438f"], # border line color for 'other tabs' and color for 'odd widgets'
    ["#4f76c7", "#4f76c7"], # color for the 'even widgets'
    ["#e1acff", "#e1acff"], # window name
    ["#ecbbfb", "#ecbbfb"] # backbround for inactive screens
] 

##### WORKSPACES #####
groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend([
        # mod1 + letter of group = switch to group
        Key([mod], i.name, lazy.group[i.name].toscreen(),
            desc="Switch to group {}".format(i.name)),

        # mod1 + shift + letter of group = switch to & move focused window to group
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True),
            desc="Switch to & move focused window to group {}".format(i.name)),
        # Or, use below if you prefer not to switch to that group.
        # # mod1 + shift + letter of group = move focused window to group
        # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
        #     desc="move focused window to group {}".format(i.name)),
    ])
##### LAYOUTS DEFAULTS #####
layout_theme = {
    'border_width': 2,
    'margin': 8,
    'border_focus': 'e1acff',
    'border_normal': '1D2330'
}


layouts = [
    layout.Columns(**layout_theme),
    layout.Max(**layout_theme),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font="monospace",
    fontsize = 12,
    padding = 4,
    background=colors[0]
)

extension_defaults = widget_defaults.copy()



##### MOUSE CALLBACKS #####
def mouse_callback(qtile, command):
    qtile.cmd_spawn(command)

def open_play_pause_spotify(qtile):
    try:
        subprocess.check_output(['pgrep', 'spotify'])
    except:
        qtile.cmd_spawn('spotify')
    else:
        qtile.cmd_spawn(
            '''dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify
            /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.PlayPause'''
        )

def change_audio_output(qtile):
    qtile.cmd_spawn("pacmd set-card-profile alsa_card.pci-0000_03_00.1 off")
    qtile.cmd_spawn(
        '''pacmd set-card-profile alsa_card.pci-0000_00_1f.3
        output:analog-stereo+input:analog-stereo'''
    )

    card_name = "alsa_card.usb-C-Media_INC._USB_Sound_Device-00"

    # list_cards_array = "pacmd list-cards".split(' ')
    speakers_on_cmd = f"pacmd set-card-profile {card_name} output:analog-stereo"
    speakers_off_cmd = f"pacmd set-card-profile {card_name} off"

    # cards = subprocess.run(list_cards_array, capture_output=True).stdout.decode('utf-8')

    # la siguiente linea obtiene todas las cards con sus active profile
    cards = subprocess.check_output(
        "pacmd list-cards | grep -e 'active profile:' -e 'index:'",
        shell=True
    ).decode('utf-8')
    # aca busco el primer > porque ahi es donde termina la primera card
    # ya que el active profile termina con >
    # i = cards.find('>') + 1
    # # aca corto la variable cards para q solo incluya la primera card
    # cards = cards[:i]

    if 'active profile: <output:analog-stereo>' in cards:
        qtile.cmd_spawn(speakers_off_cmd)
    else:
        qtile.cmd_spawn(speakers_on_cmd)
    



##### KEYBINDING CALLBACKS #####

def screenshot(qtile):
    shot = subprocess.run(['maim', '-s'], stdout=subprocess.PIPE)
    subprocess.run(
        ['xclip', '-selection', 'clipboard', '-t', 'image/png'],
        input=shot.stdout
    )

def increase_decrease_volume(qtile, direction):
    qtile.cmd_spawn(f"amixer -D pulse sset Master 10%{direction}")




##### TOPBAR #####
screens = [
    Screen(
        top=bar.Bar(
            [
                widget.CurrentLayout(),
                widget.GroupBox(),
                widget.Prompt(),
                widget.WindowName(
                       font = "monospace semibold",
                       foreground = colors[6],
                       background = colors[0],
                       padding = 0
                ),
                widget.Image(
                    filename='~/qtile/images/spotify-byn.svg',
                    mouse_callbacks={
                        'Button1': lazy.function(
                            open_play_pause_spotify
                        )
                    },
                    margin=4
                ),
                widget.Chord(
                    chords_colors={
                        'launch': ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                widget.Systray(),
                widget.Clock(format='%d/%m/%Y, %H:%M:%S'),
                widget.QuickExit(),
                widget.Volume(
                       foreground=colors[2],
                       background=colors[5],
                       padding=5,
                       mouse_callbacks={
                           'Button1': lazy.function(
                               mouse_callback,
                               'amixer -D pulse set Master 1+ toggle'
                           ),
                           'Button3': lazy.function(
                               change_audio_output
                           ),
                       }
                ),
            ],
            24,
        ),
        wallpaper='~/wallpapers/nuevo.jpg',
        wallpaper_mode='stretch'
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
])
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

# CUSTOM KEYBINDINGS
keys.extend([
    Key([mod, "shift"], "p", lazy.spawn("rofi -show run"), desc="Run rofi"),
    Key([mod], "p", lazy.function(open_play_pause_spotify), desc="Run/Play/Pause spotify"),
    Key([mod, "shift"], "b", lazy.spawn(browser), desc="Launch brave"),
    Key([mod, "shift"], "c", lazy.spawn("clementine"), desc="Launch clementine music player"),
    Key([mod, "shift"], "s", lazy.spawn("slack"), desc="Launch slack"),
    Key([mod], "a", lazy.function(screenshot), desc="copy area screenshot to clipboard"),
    # Sound
    Key(
        [mod], "i",
        lazy.function(
            increase_decrease_volume,
            "+"
        ),
        desc="+10% volume"
    ),
    Key(
        [mod], "u",
        lazy.function(
            increase_decrease_volume,
            "-"
        ),
        desc="-10% volume"
    ),    
])
