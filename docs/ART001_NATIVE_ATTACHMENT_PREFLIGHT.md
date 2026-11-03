# ART-001 — TS native attachment and rotation preflight

**2026-11-03 — technical handoff while FA draws the two instruments.** This is a read-only, independently executed engineering gate for Issue #3. It is **not** new art, not a device install package, and does **not** change the existing G1 clinical patient/exam code or the already accepted TO-004 V3 prefabs.

## The verified game-source constraint

The owner-supplied, unmodified ILSpy sources were inspected directly before implementing this gate. No original source file or original image is committed to ABCL.

- `dll_ilspy/Lopital/Floor.cs`, `CanPlaceObject(GameDBObject, Vector2i, Direction, ...)`: native placement requires a real center-object parent with an `AttachmentSlot`. A missing parent returns `NOT_ALLOWED_ATTACHMENT_NO_PARENT`; a nonaccepting parent returns `NOT_ALLOWED_ATTACHMENT_WRONG_PARENT`.
- That same method refuses placement if `m_attachmentObject` **is already occupied**. The native tile holds **one attached child**, even if `AttachmentSlot.AllowedTags` contains several tags. The list identifies **types the parent may accept**, not simultaneous positions. In `Floor` the attached object occupies the tile's single `m_attachmentObject` field.
- `GameDBObject.AcceptsAttachment` accepts a proposed child if any of the parent's allowed tags matches `objectType.HasTag(tag)`. It does not match child object IDs and does not imply that the child can be placed in arbitrary lab rooms.
- `GameDBObject.OnPostLoad` derives NE/SE/SW use offsets from the NW offsets if unspecified. The workbench's `ForcesAttachmentOrientation=false` permits independent child orientation **only as far as the attachment parent is concerned**; neighboring `ConnectedSlots` may still impose forced directions through `Floor.GetForcedOrientation`. Neither source property proves every in-game rotation has been accepted.
- `ObjectRenderer.GetTextureCoords` supports `LAYOUT_16_X_8` and uses the respective sprite IDs; the separate `LAYOUT_8_X_8` branch is unsupported. The candidate reserves eight 128×128 tiles in an original ABCL-only 2048×1024 atlas. Avoid using any copied original-game atlas pixels.
- Source ART-001 remains `SHAPE_1_X_1` for both candidate devices and the private parent workbench. A **single workbench type** may support both device *types*, but showing both at once requires **two separately placed parent instances**; it does not require (or allow) modifying the base game to add a second attachment object.

## Implementation delivered

`tools/audit_art001_native_attachment.py` validates the existing additive, not-yet-accepted FA XML without changing it. It rejects original object ID overwrites, shared atlas registrations, wrong/duplicate private tags, unexpected connected slots, parent-forced direction, unbound instruments, invalid texture atlas mapping, changed private asset IDs and missing tentative employee-use animation references. It returns a JSON record of **source-proof-only** properties and explicitly marks workbench occupancy 1, minimum simultaneous parent instances 2, real staff access/rotation L4 NOT_RUN and four-DLC/Workshop UNTESTED.

The accompanying `tests/test_art001_native_attachment_preflight.py` uses **synthetic ABCL-only GameDB fixtures** to verify positive and negative failure paths. Its mutation tests must reject missing parent, mistaken vanilla tags, incorrect parent tag whitelist, forced orientations, cross-device tag collisions, a second/inconsistent sprite ID, and illicit original asset overrides. No original game bytes enter tests or GitHub.

The CI job checks out the exact TS PR head and the **immutable, currently committed FA art branch snapshot** `0e8ff6720402961a102a7788dd6bbfe74e9e1d14`. It reports the native contract of that existing candidate **without building or approving any 3D/2D appearance**, without starting the game, and without accessing encrypted references or requiring local programs. When FA later submits new game-ready art, TS will update the reviewed snapshot SHA after owner visual approval, rather than silently consuming a moving branch.

## Explicit still-open gates

- FA: original NW and NE directional identity, then all four views for both original devices; visible 128×128 preview approval and source manifest with consistent camera scale/attachment anchor. **Neither two separate 3D source models nor a green rendering CI job equals visual acceptance.**
- TS: establish actual parent workbench placement, staff-use offset, four orientations and native room equipment readiness in a disposable-save ART-only L4. Test **two separate workbench instances** to host both devices simultaneously and a deliberately attempted second child on one already occupied bench (expected native rejection). Do not force both objects into one cell.
- Integration: preserve original CBC/hematology/microbiology/histology, other base tables, private child tags, already-approved TO-004 V3 files and any explicitly declared supported DLC/Workshop configuration.
- Medical: no new instrument may silently inherit original `hematoanalyzer` or `RIA` tags, claim to perform the blood-lead assay, or modify a native examination until the corresponding service-to-device workflow is independently proved. Draft clinical decisions in PR #37 remain unapproved and are not changed by this test.

**Verdict boundary:** passing this automated preflight means XML and known native attachment *preconditions* align; it does **not** prove the objects can actually be placed, rotated, animated, operated by staff or restored from a save. Prior owner ART-only L4 remains **3 PASS / 2 FAIL / 3 BLOCKED**. Keep Issue #3 OPEN and PR #14 / this TS PR Draft. No auto-merge, patient respawn, installer or Alpha release.
