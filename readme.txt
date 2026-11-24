- IClone: 
- export igs with ambiant light (5233): no spot or directional lights, only tab visual > IGL ambiant. No roof because light comes from above.
- export igs with spot light, with roof (5234).
If outside, export with sun directional light only.

Export to folder name 5233 for example, export cam1.igs, cam2.igs in a subfoler called cams.
Copy 5322 to Indigo dir.
Run ./process_folder_spotlight on spolight 
Run ./process_folder_sunlight on sunlight
Run ./process_folder_ambiant on ambiant

Open each igs file to set the camera settings, and save the scene.

Merge meshes and create the tarball:
./mergeAndTar.sh 6042
