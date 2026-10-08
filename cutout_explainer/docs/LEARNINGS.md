# Learnings log

An append-only log of rule changes. Each entry: date · change · reason / evidence · approved by.
Process: at the end of every job, the working model proposes entries. The human approves or rejects each one. Approved entries
are applied to the affected files and logged here in the same commit. Don't change rules on the strength of a single run unless the human approves.

## 2026-10-08 (founding session)
- **Assets must be recognizable reconstructions of the real thing, with signature features listed before drawing.** Evidence: v1's Stanford was a generic box house and was rejected by the user. Approved: user.
- **Screens, books and papers face their user. Typing shots are side-on or over-the-shoulder.** Evidence: v1 had a computer facing the camera while the kid typed. Approved: user.
- **Rig: hands can't cross the body midline (prints a warning). The far arm goes behind the torso in side view, both arms in back view.** Evidence: v2 showed crossed hands, and hands over a back-view character. Approved: user.
- **Pose presets (`pose()`) replace raw arm numbers.** Same evidence as above. Approved: user.
- **Faces resemble real people via hair, jaw, brows, nose and accessories.** Evidence: the user asked for faces closer to the real people. Approved: user.
- **Self-review checklist: re-read the brief and tick every stated requirement.** Evidence: Qwen run 1 seated two characters on the same side despite a brief saying "across". Approved: user.
- **Added rocket_rumble and engine_roar sound effects.** Evidence: Qwen's launch had no low end because the library had no rumble. Approved: user.
- **Reference images downscaled. Added a slim production prompt.** Evidence: Qwen run 1 used 7.2M input tokens for 3 shots, mostly re-sent context. Approved: user.
- **Learning happens through proposals the human approves, committed to this repo.** Approved: user.
