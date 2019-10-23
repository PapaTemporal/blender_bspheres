# BSPHERES

This tool simulates zSpheres in Blender.

zBrush has a fancy tool they call zSpheres that helps in creating quick base meshes. 
Well, Blender has been able to do the same thing for a long time but it was a little more complicated.

In Blender, you would have to create a mesh with a single vertex, then add three modifiers (Mirror, Skin, Subdivision Surface). At this point you could just extrude vertices and it would give the same effect as zSpheres.
So, all this does is flesh this out to be simpler.

A panel called "bSpheres" will show up in the Tools Panel.
1. The create button will create the single vertex mesh with all the modifiers needed and only exposes the settings we care about.
2. The Axis checkboxes will enable/disable symmetry as desired.
3. The "Mark Root" button will set the selected vertex as the root (useful if you are not going to sculpt, but create bones based on the vertices)
4. The "Mark Loose" and "Clear Loose" buttons make vertices act more like the grab brush by just pulling the skin towards them and does not set the vertex in the center of the skin
5. The "Viewport" integer lets you choose how much you want the skin to be subdivided. The higher the number, the smoother the mesh looks.
6. The apply button will apply all three modifiers, and then remesh the object with a voxel size of 0.01 (I do this so the mesh can be joined where it overlaps)

Outside of that,
1. Press E to extrude the vertices
2. Press Ctrl-A to scale the mesh at the selected vertex (like scaling the zSphere)
3. Select two vetices where you want to add another vertex and press Ctrl-R -> click in-between them
4. Press G to move the vertices to your heart's content from any view

Enjoy!

Abinadi
