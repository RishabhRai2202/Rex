from panda3d.core import WindowProperties, TransparencyAttrib

# Make the window borderless and always on top
wp = WindowProperties()
wp.setUndecorated(True)
wp.setForeground(True)
wp.setZOrder(WindowProperties.ZTop)
wp.setTransparent(True)  # Enables window transparency

base.win.requestProperties(wp)

# Set model transparency
model.setTransparency(TransparencyAttrib.M_alpha)