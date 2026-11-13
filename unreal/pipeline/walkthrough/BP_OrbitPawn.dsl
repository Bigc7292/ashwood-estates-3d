(event `self.ReceiveTick`
  (params (DeltaSeconds))
  ; Everything below only runs while this orbit view is the one being controlled
  (if (`Pawn.IsPlayerControlled` self)
    (bind pc (`GameplayStatics.GetPlayerController` 0))
    ; Orbit the villa: mouse or A/D (Left/Right) turn, W/S (Up/Down) tilt, Q/E or mouse wheel zoom
    (bind (mx my) (`PlayerController.GetInputMouseDelta` pc))
    (bind turn (- (+ (`KismetMathLibrary.Conv_BoolToDouble` (`PlayerController.IsInputKeyDown` pc (struct :`KeyName` "D"))) (`KismetMathLibrary.Conv_BoolToDouble` (`PlayerController.IsInputKeyDown` pc (struct :`KeyName` "Right")))) (+ (`KismetMathLibrary.Conv_BoolToDouble` (`PlayerController.IsInputKeyDown` pc (struct :`KeyName` "A"))) (`KismetMathLibrary.Conv_BoolToDouble` (`PlayerController.IsInputKeyDown` pc (struct :`KeyName` "Left"))))))
    (bind tilt (- (+ (`KismetMathLibrary.Conv_BoolToDouble` (`PlayerController.IsInputKeyDown` pc (struct :`KeyName` "W"))) (`KismetMathLibrary.Conv_BoolToDouble` (`PlayerController.IsInputKeyDown` pc (struct :`KeyName` "Up")))) (+ (`KismetMathLibrary.Conv_BoolToDouble` (`PlayerController.IsInputKeyDown` pc (struct :`KeyName` "S"))) (`KismetMathLibrary.Conv_BoolToDouble` (`PlayerController.IsInputKeyDown` pc (struct :`KeyName` "Down"))))))
    (bind zoom (- (`KismetMathLibrary.Conv_BoolToDouble` (`PlayerController.IsInputKeyDown` pc (struct :`KeyName` "Q"))) (`KismetMathLibrary.Conv_BoolToDouble` (`PlayerController.IsInputKeyDown` pc (struct :`KeyName` "E")))))
    (bind rot (`SceneComponent.K2_GetComponentRotation` (`self.SpringArm`)))
    (bind yaw (+ (.yaw rot) (* turn 60.0 DeltaSeconds) (* mx 1.5)))
    (bind pitch (`KismetMathLibrary.FClamp` (+ (.pitch rot) (* tilt -40.0 DeltaSeconds) (* my 1.5)) -80.0 -3.0))
    (`SceneComponent.K2_SetWorldRotation` (`self.SpringArm`) (`KismetMathLibrary.MakeRotator` 0.0 pitch yaw) false false)
    (set `SpringArmComponent.TargetArmLength` :`self` (`self.SpringArm`) :`TargetArmLength` (`KismetMathLibrary.FClamp` (+ (`SpringArmComponent.TargetArmLength` (`self.SpringArm`)) (* zoom 2500.0 DeltaSeconds)) 900.0 9000.0))
    ; Permanent reminder while in this view
    (`KismetSystemLibrary.PrintString` "OUTSIDE VIEW  -  press O, I or Enter to go back inside  |  mouse / WASD orbit, wheel or Q/E zoom" true false _ 0.0 "OrbitHint")
    ; Back inside with O, I or Enter (only after those keys were released once, so the O that opened this view does not bounce back)
    (bind inkey (or (`PlayerController.IsInputKeyDown` pc (struct :`KeyName` "O")) (`PlayerController.IsInputKeyDown` pc (struct :`KeyName` "I")) (`PlayerController.IsInputKeyDown` pc (struct :`KeyName` "Enter"))))
    (if (not inkey)
      (set `self.InsideKeysArmed` true)
      (elif `self.InsideKeysArmed`
        (`self.GoInside`)))))

; Back to walking, at the front gate facing the house
(event `GoInside`
  (set `self.InsideKeysArmed` false)
  (bind found (`GameplayStatics.GetActorOfClass` "/Game/FirstPerson/Blueprints/BP_FirstPersonCharacter.BP_FirstPersonCharacter_C"))
  (bind walker (cast `Pawn` found))
  (`self.K2_TeleportTo` walker (985.0 2860.0 130.0) (struct :`Yaw` -90.0))
  (`Controller.Possess` (`GameplayStatics.GetPlayerController` 0) walker)
  (`Controller.SetControlRotation` (`GameplayStatics.GetPlayerController` 0) (struct :`Yaw` -90.0))
  (`KismetSystemLibrary.PrintString` "" true false _ 0.0 "OrbitHint")
  (`KismetSystemLibrary.PrintString` "Walking (front gate). O = outside orbit view" true false _ 5.0))

(event `Key|MouseScrollUp`
  (params (Key))
  (:`Pressed` (set `SpringArmComponent.TargetArmLength` :`self` (`self.SpringArm`) :`TargetArmLength` (`KismetMathLibrary.FClamp` (- (`SpringArmComponent.TargetArmLength` (`self.SpringArm`)) 400.0) 900.0 9000.0))))

(event `Key|MouseScrollDown`
  (params (Key))
  (:`Pressed` (set `SpringArmComponent.TargetArmLength` :`self` (`self.SpringArm`) :`TargetArmLength` (`KismetMathLibrary.FClamp` (+ (`SpringArmComponent.TargetArmLength` (`self.SpringArm`)) 400.0) 900.0 9000.0))))

(event `Key|O` :!delete)

(event `self.ReceivePossessed`
  (params (NewController))
  (set `self.InsideKeysArmed` false))
