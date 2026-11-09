R=../step1_reference/generated_approved
shootall () 
{ 
    p=$1;
    for v in rear/cams/rear garden/cams/garden_back garden/cams/pool;
    do
        n=$(basename $v);
        d=$(dirname $(dirname $v));
        TO=250000 node tools/shoot.cjs rear_pass.html views/$v.json views/$d/shots/${n}_pass${p}_model.png 960 540 | tail -1 &
    done;
    wait;
    python3 tools/sbs.py views/rear/shots/rear_pass${p}_model.png $R/EXT-4b-ELEV-REAR_GENERATED-SOURCE-CONDITIONED.png views/rear/shots/rear_pass${p}_side_by_side.png "model rear_pass.html, ELEV-REAR camera, step 6 pass $p";
    python3 tools/sbs.py views/garden/shots/garden_back_pass${p}_model.png $R/EXT-4b-GARDEN-BACK_GENERATED-SOURCE-CONDITIONED.png views/garden/shots/garden_back_pass${p}_side_by_side.png "model rear_pass.html, GARDEN-BACK camera, step 6 pass $p";
    python3 tools/sbs.py views/garden/shots/pool_pass${p}_model.png $R/EXT-4b-POOL_GENERATED-SOURCE-CONDITIONED.png views/garden/shots/pool_pass${p}_side_by_side.png "model rear_pass.html, POOL camera (three.js Water2), step 6 pass $p"
}
