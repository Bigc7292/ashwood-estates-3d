(event `Key|O`
  (params (Key))
  (:`Pressed`
    (bind found (`GameplayStatics.GetActorOfClass` "/Game/Villa/Walkthrough/BP_OrbitPawn.BP_OrbitPawn_C"))
    (bind orbit (cast `Pawn` found))
    (`Controller.Possess` (`GameplayStatics.GetPlayerController` 0) orbit)))
