# Step 7: Motion

Script: `../step7_motion.py`. `build` adds the animation to the scene and saves; `render A B` renders frames A to B into `frames/`. Video: `barclay_exterior_step7.mp4`.
6 s at 24 fps (frames 1–144), 768×432, Cycles CPU, 10 samples with denoise, motion blur. Key frames: `keyframes_1_72_144.png`.

| Motion | How |
|---|---|
| Camera push-in on the corner | `CAM_MOTION`, from the Step 2 `CAM_T6_corner` framing (26, −27, 6.5) to (17.5, −23.5, 4.8), locked on the building |
| Clouds drifting | Location of the cloud noise mapping (`EXT7_cloud_mapping`) keyframed. It's shared by the lit and camera skies, so the light and the visible sky move together. |
| Traffic | A dark car westbound in the far lane, a white van eastbound in the near lane. Lanes are read from the centre markings at y −23.2. Vehicles are blockouts. |
| Signal change | Lens emission: green to frame 60, amber 61–96, red from 97 (constant keys) |
| Light flicker | Lamp 1's lantern left burning in daylight, flickering on random constant keys |

Rain was left out: the target sky is clear. It can be added as a separate grey-sky version.
