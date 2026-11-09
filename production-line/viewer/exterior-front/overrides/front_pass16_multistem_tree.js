// Front view, step 6 pass 16 (lane 2 self-critique, awaiting independent critic):
// "looks unnatural": the shrub mass behind the front-right low wall read as three faceted green balls.
// ELEV-FRONT shows ONE open, multi-stem small tree there (thin stems from behind the wall, spreading airy canopy, sky/stone visible through it).
// Replace the clumped-sphere row with a procedural multi-stem tree at the same image-read position and height (assumptions, not survey; species unknown).
(window.MODEL_OVERRIDES = window.MODEL_OVERRIDES || {remove:[], add:[]});
window.MODEL_OVERRIDES.shrubRows = (window.MODEL_OVERRIDES.shrubRows || []).filter(r => r.id !== 'shrub-mass-behind-wall');
window.MODEL_OVERRIDES.multiStemTrees = [
  {id:'front-right-multistem-tree', x:12.85, z:28.6, top:3.4, spread:3.6, stems:6, clusters:420, color:0x4a6a30, status:'pass16_image_read_assumption (replaces shrub-mass-behind-wall)'}
];
