#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from gi.repository import Gtk, Gio, GdkPixbuf, Gdk

class PhotoViewer(Gtk.Window):
	"""
	main class 
	"""
	def __init__(self):
		"""
		initialization
		"""
		Gtk.Window.__init__(self)
		self.set_title("PyGi Photo-Viewer")
		height = 900
		width = 500
		self.set_default_size(height, width)
		self.set_position(Gtk.WindowPosition.CENTER)
		self.set_icon_from_file("images/photo-viewer.png")
		#self.set_decorated(0) # Remove decoration of window

		# CSS Theme
		self.set_name("Photo-Viewer")
		style_provider = Gtk.CssProvider()
		css = open("style.css", "rb")
		css_data = css.read()
		css.close()
		style_provider.load_from_data(css_data)
		Gtk.StyleContext.add_provider_for_screen(
			Gdk.Screen.get_default(),
			style_provider,
			Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

		#Path of pictures / index picture / picture paths / zoom in/out
		self.file_name = ""
		self.path = []
		self.index = 0
		self.picture_paths = []
		self.zoom_in = 1

		#Menu item
		menu = Gtk.Menu()

		menu_items_close = Gtk.ImageMenuItem("close")
		img_icon = Gio.ThemedIcon(name="insert-image")
		img = Gtk.Image.new_from_gicon(img_icon, Gtk.IconSize.BUTTON)
		menu_items_close.set_image(img)
		menu_items_close.connect("activate", Gtk.main_quit)

		menu_items_open = Gtk.ImageMenuItem("Open")
		img_icon = Gio.ThemedIcon(name="insert-image")
		img = Gtk.Image.new_from_gicon(img_icon, Gtk.IconSize.BUTTON)
		menu_items_open.set_image(img)
		menu_items_open.connect("activate", self.load_image)

		menu.append(menu_items_open)
		menu.append(menu_items_close)

		file_menu = Gtk.MenuItem("Image")
		file_menu.set_submenu(menu)

		
		menu = Gtk.Menu()

		menu_items_next = Gtk.ImageMenuItem("Next Picture")
		img_icon = Gio.ThemedIcon(name="go-next")
		img = Gtk.Image.new_from_gicon(img_icon, Gtk.IconSize.BUTTON)
		menu_items_next.set_image(img)
		menu_items_next.connect("activate", self.next_prev_photo, "next")

		menu_items_prev = Gtk.ImageMenuItem("Previous Picture")
		img_icon = Gio.ThemedIcon(name="go-previous")
		img = Gtk.Image.new_from_gicon(img_icon, Gtk.IconSize.BUTTON)
		menu_items_prev.set_image(img)
		menu_items_prev.connect("activate", self.next_prev_photo, "prev")

		menu_items_zoom_in = Gtk.ImageMenuItem("Zoom in")
		img_icon = Gio.ThemedIcon(name="zoom-in")
		img = Gtk.Image.new_from_gicon(img_icon, Gtk.IconSize.BUTTON)
		menu_items_zoom_in.set_image(img)
		menu_items_zoom_in.connect("activate", self.zoom_in_out, "zoom-in")

		menu_items_zoom_out = Gtk.ImageMenuItem("Zoom out")
		img_icon = Gio.ThemedIcon(name="zoom-out")
		img = Gtk.Image.new_from_gicon(img_icon, Gtk.IconSize.BUTTON)
		menu_items_zoom_out.set_image(img)
		menu_items_zoom_out.connect("activate", self.zoom_in_out, "zoom-out")

		menu_items_zoom_original = Gtk.ImageMenuItem("Zoom Original")
		img_icon = Gio.ThemedIcon(name="zoom-original")
		img = Gtk.Image.new_from_gicon(img_icon, Gtk.IconSize.BUTTON)
		menu_items_zoom_original.set_image(img)
		menu_items_zoom_original.connect("activate", self.zoom_in_out, "zoom-original")

		menu_items_rot_right = Gtk.ImageMenuItem("Rotation Right")
		img_icon = Gio.ThemedIcon(name="object-rotate-right")
		img = Gtk.Image.new_from_gicon(img_icon, Gtk.IconSize.BUTTON)
		menu_items_rot_right.set_image(img)
		menu_items_rot_right.connect("activate", self.rotation, "droite")

		menu_items_rot_left = Gtk.ImageMenuItem("Rotation Left")
		img_icon = Gio.ThemedIcon(name="object-rotate-left")
		img = Gtk.Image.new_from_gicon(img_icon, Gtk.IconSize.BUTTON)
		menu_items_rot_left.set_image(img)
		menu_items_rot_left.connect("activate", self.rotation, "gauche")

		menu.append(menu_items_next)
		menu.append(menu_items_prev)
		menu.append(menu_items_zoom_in)
		menu.append(menu_items_zoom_out)
		menu.append(menu_items_zoom_original)
		menu.append(menu_items_rot_right)
		menu.append(menu_items_rot_left)

		edition_menu = Gtk.MenuItem("Edit")
		edition_menu.set_submenu(menu)

		menu = Gtk.Menu()
		item = Gtk.MenuItem("Image Proprieties")
		menu.append(item)
		prop_menu = Gtk.MenuItem("Proprieties")
		item.connect("activate", self.prop_img)
		prop_menu.set_submenu(menu)

		menu = Gtk.Menu()
		about_item = Gtk.MenuItem("About")
		about_item.connect("activate", self.about)
		visit_item = Gtk.MenuItem("Visit us")
		visit_item.connect("activate", self.contact_us)
		menu.append(about_item)
		menu.append(visit_item)
		about_menu = Gtk.MenuItem("Help")
		about_menu.set_submenu(menu)

		menubar = Gtk.MenuBar()
		menubar.append(file_menu)
		menubar.append(edition_menu)
		menubar.append(prop_menu)
		menubar.append(about_menu)

		headerbar = Gtk.HeaderBar()

		self.image = Gtk.Image()
		scrolled = Gtk.ScrolledWindow()
		scrolled.add(self.image)

		# icon list : https://developer.gnome.org/icon-naming-spec/
		# Button next and last
		icon_next = Gio.ThemedIcon(name="go-next")
		icon_last = Gio.ThemedIcon(name="go-previous")
		image_next = Gtk.Image.new_from_gicon(icon_next, Gtk.IconSize.BUTTON)
		image_last = Gtk.Image.new_from_gicon(icon_last, Gtk.IconSize.BUTTON)

		button_next = Gtk.Button()
		button_next.add(image_next)
		button_next.connect("clicked", self.next_prev_photo,"next")
		button_last = Gtk.Button()
		button_last.connect("clicked", self.next_prev_photo, "prev")
		button_last.add(image_last)

		# Button pivoter
		icon_piv_droite = Gio.ThemedIcon(name='object-rotate-right')
		icon_piv_gauche = Gio.ThemedIcon(name='object-rotate-left')
		image_piv_droite = Gtk.Image.new_from_gicon(icon_piv_droite, Gtk.IconSize.BUTTON)
		image_piv_gauche = Gtk.Image.new_from_gicon(icon_piv_gauche, Gtk.IconSize.BUTTON)

		button_piv_droite = Gtk.Button()
		button_piv_droite.connect("clicked", self.rotation, "droite")
		button_piv_droite.add(image_piv_droite)
		button_piv_gauche = Gtk.Button()
		button_piv_gauche.connect("clicked", self.rotation, "gauche")
		button_piv_gauche.add(image_piv_gauche)

		# Zoom button
		icon_zoom_in = Gio.ThemedIcon(name="zoom-in")
		icon_zoom_out = Gio.ThemedIcon(name="zoom-out")
		icon_zoom_original = Gio.ThemedIcon(name="zoom-original")
		image_zoom_in = Gtk.Image.new_from_gicon(icon_zoom_in, Gtk.IconSize.BUTTON)
		image_zoom_out = Gtk.Image.new_from_gicon(icon_zoom_out, Gtk.IconSize.BUTTON)
		image_zomm_originnal = Gtk.Image.new_from_gicon(icon_zoom_original, Gtk.IconSize.BUTTON)

		button_zoom_in = Gtk.Button()
		button_zoom_in.add(image_zoom_in)
		button_zoom_in.connect("clicked", self.zoom_in_out,"zoom-in")
		button_zoom_out = Gtk.Button()
		button_zoom_out.connect("clicked", self.zoom_in_out, "zoom-out")
		button_zoom_out.add(image_zoom_out)
		button_zoom_original = Gtk.Button()
		button_zoom_original.connect("clicked", self.zoom_in_out, "zoom-original")
		button_zoom_original.add(image_zomm_originnal)

		# Add buttons to headerbar
		headerbar.pack_start(button_last)
		headerbar.pack_start(button_next)
		headerbar.pack_start(button_piv_gauche)
		headerbar.pack_start(button_piv_droite)
		headerbar.pack_start(button_zoom_in)
		headerbar.pack_start(button_zoom_out)
		headerbar.pack_start(button_zoom_original)
		

		hbox = Gtk.HBox()
		self.label_window = Gtk.Label()
		self.label_image_av = Gtk.Label()
		self.label_image_ap = Gtk.Label()
		hbox.pack_start(self.label_window, False, False, 0)
		hbox.pack_end(self.label_image_av, False, False, 0)
		hbox.pack_start(self.label_image_ap, False, False, 0)

		box = Gtk.VBox()
		self.add(box)
		box.pack_start(menubar, False, False, 0)
		box.pack_start(headerbar, False, False, 0)
		box.pack_start(scrolled, True, True, 0)
		box.pack_end(hbox, False, False, 0)

		self.show_all()

	def rotation(self, widget, data):
		"""
		Rotation angle = 90°
		"""
		try:
			pixbuf = self.image.get_pixbuf()
		except:
			pass

		if data == "gauche":
			try:
				pix = pixbuf.rotate_simple(90)
				self.image.set_from_pixbuf(pix)
			except:
				pass
		if data == "droite":
			try:
				pix = pixbuf.rotate_simple(270)
				self.image.set_from_pixbuf(pix)
			except:
				pass


	def zoom_in_out(self, widget, data):
		"""
		Zoom in x8
		Zoom out /8
		"""
		try:

			pixbuf = GdkPixbuf.Pixbuf.new_from_file(self.picture_paths[self.index])
			pixbuf_loaded = self.image.get_pixbuf()
			init_width, init_height = pixbuf.get_width(), pixbuf.get_height()

			if data == "zoom-in":

				if self.zoom_in < 8:
					self.zoom_in *=2

				width = init_width * self.zoom_in
				height = init_height * self.zoom_in

				scaled_buf = pixbuf.scale_simple(width, height, GdkPixbuf.InterpType.BILINEAR)
				self.image.set_from_pixbuf(scaled_buf)
				self.label_window.set_markup("  {}x{} ".format(int(width), int(height)))
				self.label_image_ap.set_markup("            Zoom x{}".format(self.zoom_in))

			if data == "zoom-out":

				if float(self.zoom_in) > 0.125:
					self.zoom_in = float(self.zoom_in) /2

				width = init_width * self.zoom_in
				height = init_height * self.zoom_in

				scaled_buf = pixbuf.scale_simple(width, height, GdkPixbuf.InterpType.BILINEAR)
				self.image.set_from_pixbuf(scaled_buf)
				self.label_window.set_markup("  {}x{} ".format(int(width), int(height)))
				self.label_image_ap.set_markup("            Zoom x{}".format(self.zoom_in))
			if data == "zoom-original":
				self.check_image(self.picture_paths[self.index])
				self.zoom_in = 1
				self.label_image_ap.set_markup("            Zoom x{}".format(self.zoom_in))

		except:
			pass

	def next_prev_photo(self, widget, data):
		"""
		print next & prev picture from directory
		"""
		try:
			
			if data == "next":

				self.index +=1
				if self.index >= len(self.picture_paths):
					self.index = 0
			if data == "prev":

				self.index -=1
				if self.index < 0:
					self.index = len(self.picture_paths) -1

			name = self.picture_paths[self.index].split("/")
			title = name[len(name)-1]
			self.set_title(title)
			self.check_image(self.picture_paths[self.index])
			self.zoom_in = 1

		except:
			pass

	
	def load_image(self, widget):
		"""
		load_image
		"""
		dialog = Gtk.FileChooserDialog("Choisir une photo", self, Gtk.FileChooserAction.OPEN,
			(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, "Validate", Gtk.ResponseType.OK))
		dialog.set_default_size(500,600)

		#Filtre images by extension
		filtre = Gtk.FileFilter()
		filtre.set_name("Images")
		filtre.add_pattern("*.png")
		filtre.add_pattern("*.jpg")
		filtre.add_pattern("*.gif")
		filtre.add_pattern("*.jpeg")
		dialog.add_filter(filtre)

		response = dialog.run()

		if response == Gtk.ResponseType.OK:

			self.file_name = dialog.get_filename()
			name = dialog.get_filename().split("/")
			self.path = os.path.dirname(os.path.realpath(self.file_name))
			self.picture_paths = self.load_image_path(self.path)
			self.index = self.picture_paths.index(self.file_name)
			self.check_image(self.file_name)
			self.set_title(name[len(name)-1])
			dialog.destroy()

		if response == Gtk.ResponseType.CANCEL:
			dialog.destroy()

	def get_file_path(self,directory):
		"""
		Get path's files
		"""
		file_paths = os.listdir(directory)

		return file_paths, directory

	def load_image_path(self,path):
		"""
		load image in a directory
		"""

		full_file_paths, path = self.get_file_path(path)
		tab_of_path = []
		for f in full_file_paths:
			if f.endswith(".jpg") or f.endswith(".jpeg") or f.endswith(".gif") or f.endswith(".png") or f.endswith(".PNG")\
			or f.endswith(".JPG") or f.endswith(".JPEG") or f.endswith("GIF"):
				tab_of_path.append(os.path.join(path,f))
		return sorted(tab_of_path)
		
	def check_image(self, file_name):
		"""
		check_image + check width & height
		"""
		image_format = ['.jpg', '.JPG','.png', '.PNG', 'jpeg','JPEG']
		animation_format = ['.gif', '.GIF']
		width, height = self.get_size()

		try:
			#Load images
			if file_name[len(file_name)-4:] in image_format:

				pixbuf = GdkPixbuf.Pixbuf.new_from_file(file_name)
				hauteur = pixbuf.get_height()
				largeur = pixbuf.get_width()
				image_width, image_height = self.pour_image(hauteur, height, largeur, width)
				type_image = "image"
				self.process_image(pixbuf, image_height, image_width, type_image)
				
			if file_name[len(file_name)-4:] in animation_format:
				"""
				we can use : GdkPixbuf.PixbufAnimation(file_path)
				"""
				loader = GdkPixbuf.PixbufLoader()
				f = open(file_name, 'rb')
				pic = f.read()
				loader.write(pic)
				f.close()
				loader.close()
				pixbuf = loader.get_animation()

				type_image = "animation"
				image_height= -1
				image_width= -1
				self.process_image(pixbuf,image_height, image_width, type_image)

			self.label_image_av.set_markup("file {}/{}  ".format(self.index+1, len(self.picture_paths)))
		
		except:
			pass

	def pour_image(self, hauteur, height, largeur, width):
		"""
		return pourcentage of difference in image scale 

		window_width, window_height = width, height
		image_width, image_height = largeur, hauteur
		"""
		ratio = float(largeur)/hauteur
		if largeur >= width:
			largeur = width 
			hauteur = (largeur/ratio) 
			if hauteur > height:
				hauteur = height
			if largeur > width:
				largeur = width
		if hauteur >= height:
			hauteur = height 
			largeur = (hauteur*ratio)
			if largeur > width:
				largeur = width
			if hauteur > height:
				hauteur = height
		
		return largeur, hauteur

	def process_image(self, pixbuf, image_height, image_width, type_image):
		"""
		Processing image 
		"""
		if type_image == "image":
			scaled_buf = pixbuf.scale_simple(image_width, image_height, GdkPixbuf.InterpType.HYPER)
			self.image.set_from_pixbuf(scaled_buf)
		if type_image == "animation":
			self.image.set_from_animation(pixbuf)
		self.label_window.set_markup("  {}x{} ".format(int(pixbuf.get_width()), int(pixbuf.get_height())))
		self.label_image_ap.set_markup("            Zoom x{}".format(self.zoom_in))

	def about(self, widget):
		"""
		About dialog 
		"""
		about = Gtk.AboutDialog()
		about.set_program_name("PyGi Photo-Viewer ")
		about.set_version("<b>Version :</b> 0.1")
		about.set_copyright('Chiheb NeXus© - 2015')
		about.set_comments("This program is a simple Photo Viewer created with PyGObject (PyGi)")
		about.set_website("http://www.nexus-coding.blogspot.com")
		author = ["Chiheb Nexus http://www.nexus-coding.blogspot.com"]
		image = GdkPixbuf.Pixbuf.new_from_file('images/photo-viewer.png')
		about.set_icon_from_file("images/photo-viewer.png")
		about.set_logo(image)
		about.set_authors(author)
		about.set_license(" \
PyGi Photo-Viewer Gui is a simple photo viewer created with PyGi  \n \
Copyright (C) 2015  Chiheb Nexus\n \
This program is free software: you can redistribute it and/or modify \n\
it under the terms of the GNU General Public License as published by\n\
the Free Software Foundation, either version 3 of the License. \n \
This program is distributed in the hope that it will be useful, \n\
but WITHOUT ANY WARRANTY; without even the implied warranty of \n\
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.\n \
See the GNU General Public License for more details. \n \
You should have received a copy of the GNU General Public License \n\
along with this program.  If not, see <http://www.gnu.org/licenses/>.")

		about.run()
		about.destroy()

	def contact_us (self, widget):
		"""
		Contact us dialog
		"""
		contact = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK)
		txt = "<b>Contact us</b>\n\n<u>blog:</u> http://www.nexus-coding.blogspot.com\n<u>Github :</u> http://www.github.com/Chiheb-Nexus"
		contact.set_markup(txt)
		contact.run()
		contact.destroy()

	def prop_img(self, widget):
		"""
		Proprieties
		"""
		dialog = Dialog(self)

	def get_name_format_size(self):
		"""
		return name / format / size
		"""
		return self.get_title(), self.label_window.get_text(), self.file_name


class Dialog(Gtk.Window):
	"""
	Dialog popup
	"""
	def __init__(self, parent):
		Gtk.Window.__init__(self)
		self.set_title("Proprieties")
		self.set_position(Gtk.WindowPosition.CENTER)
		self.set_default_size(200, 100)

		try:
			name, size , file_path = parent.get_name_format_size()
			largeur, hauteur = size.split("x")
			format_img = name.split(".")

			notebook = Gtk.Notebook()

			self.label_nom = Gtk.Label()
			self.label_nom.set_markup("<b>Name:</b> {}".format(name))
			self.label_largeur = Gtk.Label()
			self.label_largeur.set_markup("<b>Width: </b>{} pixels".format(largeur))
			self.label_hauteur = Gtk.Label()
			self.label_hauteur.set_markup("<b>Height: </b>{} pixels".format(hauteur))
			self.label_format = Gtk.Label()
			self.label_format.set_markup("<b>Format: </b>{} image".format(format_img[len(format_img)-1] ))
			self.label_size = Gtk.Label()
			self.label_size.set_markup("<b>Size:</b> {}ko".format(float(os.path.getsize(file_path))/1000))

			vbox = Gtk.VBox()
			vbox.pack_start(self.label_nom, False, False, 0)
			vbox.pack_start(self.label_largeur, False, False, 0)
			vbox.pack_start(self.label_hauteur, False, False, 0)
			vbox.pack_start(self.label_format, False, False, 0)
			vbox.pack_start(self.label_size, False, False, 0)

			notebook.append_page(vbox, Gtk.Label("General"))
			self.add(notebook)

		except:
			self.add(Gtk.Label("Please load an image"))

		self.show_all()

if __name__ == '__main__':
	win = PhotoViewer()
	win.connect("delete-event", Gtk.main_quit)
	Gtk.main()