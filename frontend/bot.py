from panda3d.core import Material, AmbientLight, WindowProperties, TransparencyAttrib, FrameBufferProperties, GraphicsPipe
from direct.showbase.ShowBase import ShowBase

class ModelViewer(ShowBase):
    def __init__(self):
        # 🖥️ Configure transparent window before initializing Panda3D
        fb_props = FrameBufferProperties()
        fb_props.set_rgba_bits(8, 8, 8, 8)  # Ensure 8-bit alpha channel
        fb_props.set_depth_bits(24)

        # 🔧 Set window properties
        win_props = WindowProperties()
        win_props.setUndecorated(True)  # Remove window borders
        win_props.setForeground(True)  # Keep window always on top

        ShowBase.__init__(self, windowType='onscreen')
        self.win.requestProperties(win_props)

        # Ensure transparency mode is enabled
        self.render.setTransparency(TransparencyAttrib.MAlpha)

        # 🎨 Load 3D model
        self.model = loader.loadModel("/Users/rishabh/Documents/Rex/Dino Bot.gltf")  # Replace with your actual model file
        self.model.reparentTo(self.render)

        # ✅ Enable auto shader to render GLTF materials properly
        self.render.setShaderAuto()

        # ✅ Ensure transparency works
        self.model.setTransparency(TransparencyAttrib.MAlpha)

        # ✅ Ensure correct colors
        self.model.setColorOff()

        # 🎥 Camera setup
        self.disableMouse()  # Prevent unwanted camera movement
        base.camera.setPos(0, -5, 2)  # Move the camera back to see the model
        base.camera.lookAt(0, 0, 1)  # Focus on the model
        self.render.setShaderAuto()

        # 🖱️ Prevent model from disappearing on cursor movement
        self.taskMgr.add(self.keep_model_visible, "KeepModelVisible")

    def fix_materials(self, model):
        """Fixes missing materials and applies them correctly."""
        for node in model.findAllMatches("**/+GeomNode"):
            geom_node = node.node()
            for i in range(geom_node.getNumGeoms()):
                state = geom_node.getGeomState(i)
                material = state.getAttrib(Material)

                if material is None:
                    # 🔥 Apply a basic material if missing
                    mat = Material()
                    mat.setShininess(10)  # Basic reflection
                    mat.setDiffuse((1, 1, 1, 1))  # White base color
                    node.setMaterial(mat, 1)

    def add_lighting(self):
        """Adds ambient lighting to the scene to make colors visible."""
        ambient = AmbientLight("ambient")
        ambient.setColor((1, 1, 1, 1))  # Bright white light
        ambient_node = render.attachNewNode(ambient)
        render.setLight(ambient_node)

    def keep_model_visible(self, task):
        """Ensures the model stays visible even if the mouse moves."""
        if base.mouseWatcherNode.hasMouse():
            mouse_x = base.mouseWatcherNode.getMouseX()
            mouse_y = base.mouseWatcherNode.getMouseY()
            base.camera.lookAt(0, 0, 1)  # Reset focus
        return task.cont  # Keep running

# 🚀 Run the application
app = ModelViewer()
app.run()