
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

import os
import subprocess
from typing import List  # noqa: F401
from libqtile import qtile
from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile.widget import TextBox

mod = "mod4"
terminal = "alacritty"
browser = "brave"

colors = {
    'bg':           '#202020',
    'fg':           '#dfdfdf',
    'dark-red':     '#ea7171',
    'red':          '#ed8682',
    'dark-green':   '#96a171',
    'green':        '#b1d094',
    'dark-yellow':  '#e7a55f',
    'yellow':       '#ecb983',
    'dark-blue':    '#7196a1',
    'blue':         '#9fb8bf',
    'dark-magenta': '#c28490',
    'magenta':      '#d7adb5',
    'dark-cyan':    '#80ab96',
    'cyan':         '#9fbfaf',
    'dark-gray':    '#3d3d3d',
    'gray':         '#666666',
}

keys = [
    # Aplication spawn
    Key([mod], "Return", lazy.spawn(terminal)),  # Launches Alacritty
    Key([mod], "b", lazy.spawn(browser)),
    Key([mod], "p", lazy.spawn("pcmanfm")),
    Key([mod], "t", lazy.spawn('xterm')),
    Key([mod], "d", lazy.spawn("nwggrid -p -o 0.4")),
    Key([mod, "shift"], "Return", lazy.spawn(
        "dmenu_run -i -nb '#191919' -nf '#fea63c' -sb '#fea63c' -sf '#191919' -fn 'NotoMonoRegular:bold:pixelsize=14'")),
    Key(["control"], "space", lazy.spawn("rofi -show drun")),
    Key([mod, "shift"], "Tab", lazy.spawn("rofi -show window")),

    # SUPER + FUNCTION KEYS

    Key([mod], "f", lazy.window.toggle_fullscreen()),
    Key([mod], "q", lazy.window.kill()),

    # SUPER + SHIFT KEYS

    Key([mod, "shift"], "q", lazy.window.kill()),
    Key([mod, "shift"], "r", lazy.restart()),

    # QTILE LAYOUT KEYS
    Key([mod], "n", lazy.layout.normalize()),
    Key([mod], "space", lazy.next_layout()),

    # CHANGE FOCUS
    Key([mod], "Up", lazy.layout.up()),
    Key([mod], "Down", lazy.layout.down()),
    Key([mod], "Left", lazy.layout.left()),
    Key([mod], "Right", lazy.layout.right()),
    Key([mod], "k", lazy.layout.up()),
    Key([mod], "j", lazy.layout.down()),
    Key([mod], "h", lazy.layout.left()),
    Key([mod], "l", lazy.layout.right()),

    # RESIZE UP, DOWN, LEFT, RIGHT
    Key([mod, "control"], "l",
        lazy.layout.grow_right(),
        lazy.layout.grow(),
        lazy.layout.increase_ratio(),
        lazy.layout.delete(),
        ),
    Key([mod, "control"], "Right",
        lazy.layout.grow_right(),
        lazy.layout.grow(),
        lazy.layout.increase_ratio(),
        lazy.layout.delete(),
        ),
    Key([mod, "control"], "h",
        lazy.layout.grow_left(),
        lazy.layout.shrink(),
        lazy.layout.decrease_ratio(),
        lazy.layout.add(),
        ),
    Key([mod, "control"], "Left",
        lazy.layout.grow_left(),
        lazy.layout.shrink(),
        lazy.layout.decrease_ratio(),
        lazy.layout.add(),
        ),
    Key([mod, "control"], "k",
        lazy.layout.grow_up(),
        lazy.layout.grow(),
        lazy.layout.decrease_nmaster(),
        ),
    Key([mod, "control"], "Up",
        lazy.layout.grow_up(),
        lazy.layout.grow(),
        lazy.layout.decrease_nmaster(),
        ),
    Key([mod, "control"], "j",
        lazy.layout.grow_down(),
        lazy.layout.shrink(),
        lazy.layout.increase_nmaster(),
        ),
    Key([mod, "control"], "Down",
        lazy.layout.grow_down(),
        lazy.layout.shrink(),
        lazy.layout.increase_nmaster(),
        ),


    # FLIP LAYOUT FOR MONADTALL/MONADWIDE
    Key([mod, "shift"], "f", lazy.layout.flip()),

    # FLIP LAYOUT FOR BSP
    Key([mod, "mod1"], "k", lazy.layout.flip_up()),
    Key([mod, "mod1"], "j", lazy.layout.flip_down()),
    Key([mod, "mod1"], "l", lazy.layout.flip_right()),
    Key([mod, "mod1"], "h", lazy.layout.flip_left()),

    # MOVE WINDOWS UP OR DOWN BSP LAYOUT
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "h", lazy.layout.shuffle_left()),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right()),

    # MOVE WINDOWS UP OR DOWN MONADTALL/MONADWIDE LAYOUT
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "Left", lazy.layout.swap_left()),
    Key([mod, "shift"], "Right", lazy.layout.swap_right()),

    # TOGGLE FLOATING LAYOUT
    Key([mod, "shift"], "space", lazy.window.toggle_floating()),

]

groups = [
    Group('1', label='WWW'),
    Group('2', label='DEV', matches=[Match(wm_class=['code'])]),
    Group('3', label='SYS', matches=[Match(wm_class=['nemo'])]),
    Group('4', label='CHAT', matches=[Match(wm_class=['zoom',
                                                   'discord',
                                                   'telegram-desktop',
                                                   'slack'])]),
    Group('5', label='MUS', matches=[Match(wm_class=['spotify'])]),
    Group('6', label='GFX'),
    Group('7', label='VID'),
    Group('8', label='DOC'),
    Group('9', label='VBOX'),
]

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

layout_theme = {"border_width": 2,
                "margin": 10,
                "border_focus": "e7a55f",
                "border_normal": "1D2330"
                }

layouts = [
    layout.MonadTall(**layout_theme),
    layout.MonadWide(**layout_theme),
    layout.Tile(**layout_theme),
    layout.TreeTab(**layout_theme),
    layout.Floating(**layout_theme)
]

widget_defaults = dict(
    font='Ubuntu Mono',
    fontsize=12,
    background=colors['bg'],
    foreground=colors['fg']
)

extension_defaults = widget_defaults.copy()


screens = [
    Screen(
        top=bar.Bar(
            [
                widget.Image(
                    filename="~/.config/qtile/icons/logo.png",
                    background=colors['dark-red'],
                    foreground=colors['fg'],
                    margin=3
                ),
                # display groups
                widget.GroupBox(
                    active=colors['fg'],
                    inactive=colors['dark-gray'],
                    disable_drag=True,
                    borderwidth=0,
                    margin_x=0,
                    padding_x=10,
                    highlight_method='line',
                    block_highlight_text_color=colors['red'],
                    highlight_color=colors['bg']),

                # display the current wm layout
                widget.CurrentLayout(
                    background=colors['dark-yellow'],
                    fmt='[{}]',
                    padding=10),

                widget.WindowCount(
                    background=colors['yellow'],
                    padding=5,
                    fmt=' {}'),
                widget.WindowName(
                    foreground=colors['cyan'],
                    padding=10),

                # display total available updates
                widget.CheckUpdates(
                    distro="Arch_checkupdates",
                    margin=30,
                    padding=10,
                    colour_have_updates=colors['cyan'],
                    colour_no_updates=colors['fg'],
                    no_update_string='No updates',
                    display_format='累 {updates} updates',
                    background=colors['dark-blue'],
                    mouse_callbacks={'Button1': lambda: qtile.cmd_spawn(terminal + ' -e sudo pacman -Syu')}),

                # display memory usage
                widget.Memory(
                    background=colors['blue'],
                    padding=10,
                    measure_mem='G',
                    format=' {MemUsed:.0f}{mm}/{MemTotal:.0f}{mm}',
                    mouse_callbacks={'Button1': lambda: qtile.cmd_spawn(terminal + ' -e htop')}),

                # display cpu usage
                widget.CPU(
                    background=colors['dark-magenta'],
                    padding=10,
                    format=' {freq_current}GHz {load_percent}%'),

                widget.PulseVolume(
                    background=colors['dark-cyan'],
                    fmt=' {}',
                    padding=10,
                    volume_app='pavucontrol'),

                widget.Clock(
                    format='%Y-%m-%d %a %I:%M %p',
                    background=colors['cyan'],
                    padding=10),

                widget.Systray(
                    background=colors['dark-cyan'],
                    padding=10),

                widget.Spacer(
                    length=30,
                    background=colors['dark-cyan']
                ),

                widget.QuickExit(
                    background=colors['green'],
                    foreground=colors['bg'],
                    default_text='',
                    fontsize=17,
                )
            ],
            size=24,
            margin=5,
            background=colors['bg'],
        ),
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

main = None


@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/scripts/autostart.sh'])


@hook.subscribe.startup
def start_always():
    # Set the cursor to something sane in X
    subprocess.Popen(['xsetroot', '-cursor_name', 'left_ptr'])


@hook.subscribe.client_new
def set_floating(window):
    if (window.window.get_wm_transient_for()
            or window.window.get_wm_type() in floating_types):
        window.floating = True


floating_types = ["notification", "toolbar", "splash", "dialog"]


dgroups_key_binder = None
dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    *layout.Floating.default_float_rules,
    Match(wm_class='confirm'),
    Match(wm_class='dialog'),
    Match(wm_class='download'),
    Match(wm_class='error'),
    Match(wm_class='file_progress'),
    Match(wm_class='notification'),
    Match(wm_class='splash'),
    Match(wm_class='toolbar'),
    Match(wm_class='confirmreset'),
    Match(wm_class='makebranch'),
    Match(wm_class='maketag'),
    Match(wm_class='Arandr'),
    Match(wm_class='feh'),
    Match(wm_class='Galculator'),
    Match(title='branchdialog'),
    Match(title='Open File'),
    Match(title='pinentry'),
    Match(wm_class='ssh-askpass'),
    Match(wm_class='lxpolkit'),
    Match(wm_class='Lxpolkit'),
    Match(wm_class='yad'),
    Match(wm_class='Yad'),
    Match(wm_class='Cairo-dock'),
    Match(wm_class='cairo-dock'),


],  fullscreen_border_width=0, border_width=0)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

focus_on_window_activation = "focus"  # or smart

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True


@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/autostart.sh'])


# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
