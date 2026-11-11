# Lighting

## Day, terrace

- Sun from the south-west, high: warm white `0xfff1d6`, intensity about 2.7, shadow map on the house only.
- Sky: blue `0x6aaed0` falling to a pale horizon `0xd7eef8`. No sun disc in frame unless the camera looks at it.
- Fill: hemisphere, sky cool, ground a dull green, intensity under 0.4.
- Exposure around 0.9 with ACES. If the stone clips to white, lower the sun, do not raise the exposure.

## Dusk, terrace

- Sun just above the horizon behind the camera on the pool side, intensity under 0.5, colour `0xffc49a`.
- Sky: deep blue from about 15 degrees up. Orange only in the first few degrees at the horizon. A sky that is orange at the top of the frame is wrong.
- Cool fill so the limestone stays limestone. Warmth comes from the windows and two or three practicals on the terrace, not from painting the sun across the wall.
- Window practical: a warm pool of light in the lower half of the pane, strength under half the reflection, so the parasol is still visible in the glass.
- Pool: darker than the sky, and it must contain the reflection of the facade.

## Blender check

When a look is set in Blender, use one area light for the sun and an HDRI for the sky. Do not use both a strong sun and a bright HDRI. Render one 1280 px frame of the rear terrace before porting the numbers to three.js.
