// Front v2 pass 2 (critic on 5903abb): no bare stems under the entry tree's crown.
// The critic reads ELEV-FRONT's entry planting as one bushy mass from the low wall up, with no visible trunks; the model showed thin stems
// between the wall top and the crown. A leafy shrub mass behind the low front wall (x 11.4-15.2, z 28.9, top 2.2 m, small dark-olive clumps (r 0.32; r 0.55 read as big faceted balls); image-read
// assumption) fills that band so the stems are hidden below the crown line. Tree and crown unchanged. Concept visualisation, not survey-verified.
(window.MODEL_OVERRIDES = window.MODEL_OVERRIDES || {remove:[], add:[]});
window.MODEL_OVERRIDES.shrubRows = (window.MODEL_OVERRIDES.shrubRows || []).concat([
  {id:'front-v2-entry-tree-understorey', x0:11.4, z0:28.95, x1:15.2, z1:28.95, h:2.2, r:0.32, color:0x3f5c2a, status:'front_v2_pass2 image-read assumption (hides stems below the crown)'}
]);
