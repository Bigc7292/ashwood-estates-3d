(event `Key|L`
  (params (Key))
  (:`Pressed`
    (bind mains (`GameplayStatics.GetAllActorsWithTag` "MainLight"))
    (for a mains
      (bind lt (cast `Light` a :!pure true))
      (`SceneComponent.ToggleVisibility` (`Light.LightComponent` lt) false))
    (`KismetSystemLibrary.PrintString` "Main lights switched (L)" true false _ 2.0)))

(event `Key|K`
  (params (Key))
  (:`Pressed`
    (bind lamps (`GameplayStatics.GetAllActorsWithTag` "Lamp"))
    (for a lamps
      (bind lt (cast `Light` a :!pure true))
      (`SceneComponent.ToggleVisibility` (`Light.LightComponent` lt) false))
    (`KismetSystemLibrary.PrintString` "Lamps switched (K)" true false _ 2.0)))
