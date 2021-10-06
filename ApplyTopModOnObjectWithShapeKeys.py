# Apply Top Modifier On Object With Shapekeys
# 10-5-21
# ClusterTrace

# This script applies the modifier on the selected object while also allowing it to keep its shapekeys
# This is done by duplicating the object, then using the duplications to store the shapekeys to then add them back
# Requires no objects share the names of the shapekeys on the object in order to work properly

import bpy;

#name = bpy.context.active_object.name; #gets the name of the object the script is being applied to
object = bpy.context.active_object; # gets the selected object
shapeKeys = bpy.context.active_object.data.shape_keys.key_blocks.keys(); # gets an array of strings of the names of the shape keys
shapeCount = len(shapeKeys) - 1; # Doesn't include basis
shapeKeyObjects = []; #creates an array to store the shapekey objects in

if len(bpy.context.object.modifiers.values()) > 0:
    # sets all shapekeys to 0 on selected object
    i = 1; #starts at 1 to skip the basis
    while shapeCount > i:
        bpy.context.object.active_shape_key_index = i; #Grabs the shapekey in slot i
        bpy.context.object.active_shape_key.value = 0; #makes it not active
        i = i + 1;

    #Duplicates the object to create ones that store the shapekeys
    i = 1; #starts at 1 to skip the basis
    while shapeCount >= i:
        bpy.ops.object.duplicate(); #duplicates the selected object then selects it
        bpy.context.object.active_shape_key_index = i; #Grabs the shapekey in slot i
        bpy.context.object.active_shape_key.value = 1; #makes it an active shapekey
        j = i
        #removes other shapekeys
        while shapeCount > j: # deletes shapekeys after wanted one
            bpy.context.object.active_shape_key_index = i + 1; #Grabs the shapekey in slot i + 1
            bpy.ops.object.shape_key_remove(all=False); # deletes it
            j = j + 1
        j = 0
        while i >= j: # deletes all shapekeys left
            bpy.context.object.active_shape_key_index = 0; #Grabs the shapekey in slot 0
            bpy.ops.object.shape_key_remove(all=False);
            j = j + 1
        type = bpy.context.object.modifiers.active.type.capitalize();
        bpy.ops.object.modifier_apply(modifier=type); #applies the first modifier
        bpy.context.object.name = shapeKeys[i]; #names object the shapekey to ensure name stays in list correctly
        shapeKeyObjects.append(bpy.context.active_object); # adds object to the list
        bpy.ops.object.select_all(action='DESELECT'); # deselects everything
        object.select_set(1); # selects the original object
        bpy.context.view_layer.objects.active = object;
        i = i + 1;

    #applies the first modifier
    bpy.context.view_layer.objects.active = object; # sets active object as the original
    bpy.context.object.shape_key_clear(); # clears all shakekeys on the selected object
    bpy.context.object.modifiers.active = bpy.context.object.modifiers.values()[0]; # sets the first modifier as active
    type = bpy.context.object.modifiers.active.type.capitalize();
    bpy.ops.object.modifier_apply(modifier=type); #applies the first modifier

    # Readds shapekeys
    i = 0;
    while shapeCount > i:
        shapeKeyObjects[i].select_set(1); #adds object to selection
        bpy.ops.object.join_shapes(); #joins as shapes
        shapeKeyObjects[i].select_set(0); #removes object from selection
        i = i + 1;

    # Deletes created objects
    bpy.ops.object.select_all(action='DESELECT'); # deselects everything
    i = 0;
    while shapeCount > i:
        shapeKeyObjects[i].select_set(1); #adds object to selection
        i = i + 1;
    bpy.ops.object.delete(); #deletes selected objects

    # reselects base object to appear like nothing has changed selection wise
    bpy.ops.object.select_all(action='DESELECT'); # deselects everything
    object.select_set(1); # selects the original object
    bpy.context.view_layer.objects.active = object; # sets active object as the original