#!/usr/bin/env python
# coding: utf-8
"""
  PasswordMaker - Creates and manages passwords
  Copyright (C) 2005 Eric H. Jung and LeahScape, Inc.
  http://passwordmaker.org/
  grimholtz@yahoo.com

  This library is free software; you can redistribute it and/or modify it
  under the terms of the GNU Lesser General Public License as published by
  the Free Software Foundation; either version 2.1 of the License, or (at
  your option) any later version.

  This library is distributed in the hope that it will be useful, but WITHOUT
  ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
  FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License
  for more details.

  You should have received a copy of the GNU Lesser General Public License
  along with this library; if not, write to the Free Software Foundation,
  Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

  Written by Miquel Burns and Eric H. Jung

  PHP version written by Pedro Gimeno Fortea
      <http://www.formauri.es/personal/pgimeno/>
  and updated by Miquel Matthew 'Fire' Burns
      <miquelfire@gmail.com>
  Ported to Python by Aurelien Bompard
      <http://aurelien.bompard.org>
  Updated by Richard Beales
      <rich@richbeales.net>

  This version should work with python > 2.3. The pycrypto module enables
  additional algorithms.

  Can be used both on the command-line and with a GUI based on TKinter
"""
from pwmlib import PWM, PWM_Settings

def gui():
    import tkinter as tk

    class Application(tk.Frame):

        def __init__(self, master=None):
            self.PWmaker = PWM()
            tk.Frame.__init__(self, master)
            self.grid(sticky="nsew")
            self.top = root.winfo_toplevel()
            self.top.rowconfigure( 0, weight=1 )
            self.top.columnconfigure( 0, weight=1 )
            self.rowconfigure( 0, weight=1 )
            self.rowconfigure( 1, weight=1000 )
            self.columnconfigure( 0, weight=1 )
            self.settings = PWM_Settings()
            self.createWidgets()

        def createWidgets(self):
            settings = self.settings

            # Create the widgets
            self.url_label = tk.Label(self, justify="left", text="URL")
            self.url_text = tk.Entry(self)
            self.url_text.insert(0, settings.URL)
            self.mpw_label = tk.Label(self, justify="left", text="Master PW")
            self.mpw_text = tk.Entry(self, show="*")
            self.mpw_text.insert(0, "")
            self.alg_label = tk.Label(self, justify="left", text="Algorithm")
            self.alg = tk.StringVar(self)
            self.alg.set(settings.Algorithm)
            self.alg_combo = tk.OptionMenu(*(self, self.alg) + tuple(self.PWmaker.valid_algs))
            self.user_label = tk.Label(self, justify="left", text="Username")
            self.user_text = tk.Entry(self)
            self.user_text.insert(0, settings.Username)
            self.mod_label = tk.Label(self, justify="left", text="Modifier")
            self.mod_text = tk.Entry(self)
            self.mod_text.insert(0, settings.Modifier)
            self.len_label = tk.Label(self, justify="left", text="Length")
            self.len_spinner = tk.Spinbox(self,from_=1,to=128)
            self.len_spinner.delete(0,"end")
            self.len_spinner.insert(0,settings.Length)
            self.charset_label = tk.Label(self, justify="left", text="Characters")
            self.charset_text = tk.Entry(self)
            self.charset_text.insert(0, settings.CharacterSet)
            self.pfx_label = tk.Label(self, justify="left", text="Prefix")
            self.pfx_text = tk.Entry(self)
            self.pfx_text.insert(0, settings.Prefix)
            self.sfx_label = tk.Label(self, justify="left", text="Suffix")
            self.sfx_text = tk.Entry(self)
            self.sfx_text.insert(0, settings.Suffix)
            self.generate_button = tk.Button (self, text="Generate", command=self.generate)
            self.load_button = tk.Button (self, text="Load", command=self.load)
            self.save_button = tk.Button (self, text="Save", command=self.save)
            self.passwd_label = tk.Label(self, justify="left", text="Password")
            self.passwd_text = tk.Entry(self, fg="blue")

            # Place on the grid
            self.url_label.grid(row=0, column=0, sticky="w")
            self.url_text.grid(row=0, column=1, sticky="e")
            self.mpw_label.grid(row=1, column=0, sticky="w")
            self.mpw_text.grid(row=1, column=1, sticky="e")
            self.alg_label.grid(row=2, column=0, sticky="w")
            self.alg_combo.grid(row=2, column=1, sticky="e")
            self.user_label.grid(row=3, column=0, sticky="w")
            self.user_text.grid(row=3, column=1, sticky="e")
            self.mod_label.grid(row=4, column=0, sticky="w")
            self.mod_text.grid(row=4, column=1, sticky="e")
            self.len_label.grid(row=5, column=0, sticky="w")
            self.len_spinner.grid(row=5, column=1, sticky="e")
            self.charset_label.grid(row=6, column=0, sticky="w")
            self.charset_text.grid(row=6, column=1, sticky="e")
            self.pfx_label.grid(row=7, column=0, sticky="w")
            self.pfx_text.grid(row=7, column=1, sticky="e")
            self.sfx_label.grid(row=8, column=0, sticky="w")
            self.sfx_text.grid(row=8, column=1, sticky="e")
            self.generate_button.grid(row=9, column=0, columnspan=2, pady=5)
            self.load_button.grid(row=10, column=0, columnspan=1, pady=5)
            self.save_button.grid(row=10, column=1, columnspan=1, pady=5)
            self.passwd_label.grid(row=11, column=0)
            self.passwd_text.grid(row=11, column=1, sticky="nsew")

        def getsettings(self):
            settings = PWM_Settings()
            settings.URL = self.url_text.get()
            settings.Algorithm = self.alg.get()
            settings.Username = self.user_text.get()
            settings.Modifier = self.mod_text.get()
            settings.Length = int(self.len_spinner.get())
            settings.CharacterSet = self.charset_text.get()
            settings.Prefix = self.pfx_text.get()
            settings.Suffix = self.sfx_text.get()
            settings.MasterPass = self.mpw_text.get()
            return settings

        def save(self):
            self.settings = self.getsettings()
            self.settings.MasterPass = '' # blank this out when saving for now
            self.settings.save()

        def load(self):
            self.settings = self.settings.load()
            self.createWidgets()

        def generate(self):
            self.generate_button.flash()
            try:
                print(self.getsettings())
                pw = self.PWmaker.generatepasswordfrom(self.getsettings())
            except PWM_Error as e:
                pw = str(e)
            current_passwd = self.passwd_text.get()
            if len(current_passwd) > 0:
                self.passwd_text.delete(0,len(current_passwd))
            self.passwd_text.insert(0,pw)
            self.clipboard_clear()
            self.clipboard_append(pw)

    root = tk.Tk()
    app = Application(master=root)
    app.master.title("PasswordMaker")
    app.mainloop()

#################

def cmd():
    usage = "Usage: %prog [options]"
    settings = PWM_Settings()
    settings.load()
    parser = optparse.OptionParser(usage=usage)
    parser.add_option("-a", "--alg", dest="alg", default=settings.Algorithm, help="Hash algorithm [hmac-] md4/md5/sha1/sha256/rmd160 [_v6] (default " + settings.Algorithm + ")")
    parser.add_option("-m", "--mpw", dest="mpw", help="Master password (default: ask)", default="")
    parser.add_option("-r", "--url", dest="url", help="URL (default blank)", default=settings.URL)
    parser.add_option("-u", "--user", dest="user", help="Username (default blank)", default=settings.Username)
    parser.add_option("-d", "--modifier", dest="mod", help="Password modifier (default blank)", default=settings.Modifier)
    parser.add_option("-g", "--length", dest="len", help="Password length (default 8)", default=settings.Length, type="int")
    parser.add_option("-c", "--charset", dest="charset", help="Characters to use in password (default [A-Za-z0-9])", default=settings.CharacterSet)
    parser.add_option("-p", "--prefix", dest="pfx", help="Password prefix (default blank)", default=settings.Prefix)
    parser.add_option("-s", "--suffix", dest="sfx", help="Password suffix (default blank)", default=settings.Suffix)
    (options, args) = parser.parse_args()
    if options.mpw == "":
        import getpass
        options.mpw = getpass.getpass("Master password: ")
    # we don't support leet yet
    leet = None
    leetlevel = 0
    try:
        PWmaker = PWM()
        print(PWmaker.generatepassword(options.alg,
                               options.mpw,
                               options.url + options.user + options.mod,
                               leet,
                               leetlevel - 1,
                               options.len,
                               options.charset,
                               options.pfx,
                               options.sfx,
                              ))
    except PWM_Error as e:
        print(e)
        sys.exit(1)


# Main
if __name__ == "__main__":
    if len(sys.argv) == 1:
        gui()
    else:
        cmd()



