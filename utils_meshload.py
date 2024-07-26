import open3d as o3d


class SceneLoader:
    def __init__(self, mesh_file, scale=True, floor=True, floor_size= 20, floor_depth=0.01):
        self.mesh_file = mesh_file
        self.scale = scale
        self.floort = floor
        self.floor_size = floor_size
        self.floor_depth = floor_depth
        self.mesh, self.mesh_material = self.load_mesh()
        self.floor, self.floor_material = self.create_floor()
    
    def load_mesh(self):
      mesh = o3d.io.read_triangle_mesh(self.mesh_file + '/meshes/model.obj', True)
      if self.scale == True:
        mesh = scale_and_translate(mesh, scale_factor=0.39)
      material = o3d.visualization.rendering.MaterialRecord() # Create material
      material.albedo_img = o3d.io.read_image(self.mesh_file + '/meshes/texture.png') # Add texture
      return mesh, mesh_material

    def create_floor(self):
        floor = o3d.geometry.TriangleMesh.create_box(width=self.floor_size, height=self.floor_size, depth=self.floor_depth)
        floor.translate([-(self.floor_size/2), -(self.floor_size/2), -0.01])  # Mover el piso para que esté centrado en el origen
        floor.paint_uniform_color([0.1, 0.1, 0.7])  # Pintar el piso de color azul
        material_floor = o3d.visualization.rendering.MaterialRecord() # Create floor material
        material_floor.albedo_img = o3d.io.read_image('wood_floor_texture.png') # Add texture
        return floor, floor_material
    
    def create_offrender_scene(self):
        render = o3d.visualization.rendering.OffscreenRenderer(width=img_W, height=img_H) #Linux only
        render.scene.add_geometry('mesh', self.mesh, self.mesh_material)
        render.scene.add_geometry('floor', self.floor, self.floor_material)
        return render
    
    def create_raycast_scene(self):
        mesh1 = o3d.t.geometry.TriangleMesh.from_legacy(self.mesh)
        floor1 = o3d.t.geometry.TriangleMesh.from_legacy(self.floor)
        scene = o3d.t.geometry.RaycastingScene()
        scene.add_triangles(mesh1)
        scene.add_triangles(floor1)
        return scene

    def get_scenes(self):
        return self.create_offrender_scene(), self.create_raycast_scene()    