# TO-001 R13 — genuine Windows L3 verified; full 34-file package pending (2026-11-04)

Owner-approved [PR #63](https://github.com/guitar0788/A-Better-Clinical-Laboratory/pull/63) was squash-merged to G1 development source `9511fc9da495c0c015f383c4950666bff776176e`. Source Verify, CodeQL and installer smoke pass.

**Authentic exact-head Windows net35/CLR2 L3: PASS.** [GitHub Actions run #41861168911](https://github.com/guitar0788/A-Better-Clinical-Laboratory/actions/runs/41861168911) authorized the exact R13 source, compiled `ModABCLG1LeadTest.dll` (31,744 bytes) and successfully uploaded test-only artifact **13340101305**. The downloaded artifact was independently opened, and the DLL SHA-256 was recomputed from its actual bytes: `cbea9b466007f1cd87a153ef3d744fc0c72775d854d8b1d39e34036279de3902` (matching `BUILD_INFO.txt`). Outer artifact ZIP SHA-256: `fe80eb1b484b2e222cd9fcccdc9a23557bfefe0f36268d7daa4828401b02e2ea`.

The workflow itself was marked FAILED **only because the downstream report job could not POST an issue comment to PR #7**. Its GitHub Actions `GITHUB_TOKEN` log declares `Issues: write` and `PullRequests: read`, but the comment API returned **403 Resource not accessible by integration**. This is a reporting permission/runtime failure, **not** a failed Windows compile. Do not assume a permission change resolves it without an actual test.

The isolated compiler archive contains a **zero-byte `0Harmony.dll` placeholder**. It is **NOT** an installable package, and must not be distributed as a complete Mod. The independent full-package builder and auditor now pin the exact R13 source and verified DLL SHA. Next, assemble and audit all **34 exact members**, substituting only the authenticated compiled DLL while preserving the legitimate Harmony1 net35 runtime, MIT license, original approved room icon PNG hashes, private floor tile 376, equipment atlas, both owner-provided TO-004 previews and both prefab XML files byte-for-byte. Do not modify original game files or other mods.

**Current acceptance:** R13 L3 PASS; complete R13 package L2 **PENDING**; user game L4 **NOT RUN**; Alpha/release **NOT AUTHORIZED**. R12 test packages and DLLs are stale and must not be relabeled R13.

---

# TO-001 R12 — accepted shadowed room icon and exact package gate (2026-11-04)

**Owner-approved art supersession:** The owner approved two ACTUAL game PNGs, with
slightly thickened flask strokes, vanilla red / gray opaque colored faces, and
soft bottom-right shadow. This supersedes the active/inactive room-list icons
only from ABCL-D016. The floor isometric icon remains owner L4 PASS.

- Active original 64x64 PNG SHA-256: `c2c6c83cb0f8c2ca49dce7184bdd4f71df1c71a20ecf0c38e05337df6a48f62b`;
  red face (201,63,61), alpha 255 on colored block, translucent shadow margin.
- Inactive original 64x64 PNG SHA-256: `eb37ce261299f7df2ac87c61272168f71b5faca5de1578b71a172a8d75e861eb`;
  gray face (153,153,153), alpha 255 on colored block, translucent shadow.
- Both original PNGs are staged at
  `assets/to001/owner_approved_20261104/` in code/art integration Draft PR #62,
  with Git blob identity verified against the owner's reviewed artifacts.
- Runtime C# now SHA-verifies and uses the **entire original Sprite**;
  old on-the-fly redraw/recolor and shadow stripping were removed. Target-only
  row size was adapted for the inset face, without modifying other rooms.

**Verified real compiler:** net35/CLR2 Windows Actions
[#41840826634](https://github.com/guitar0788/A-Better-Clinical-Laboratory/actions/runs/41840826634),
source SHA `62450307ae36b5104f3a3634d0612592f743afff`, G1 DLL SHA-256 `15aef1736dfd70f34d9fede073140360c754f5c7d9d10eac3639e54d78012f9c`,
31744 bytes, artifact `13329370917`. Official net35 Harmony1
1.2.0.1 and MIT license are retained in the COMPLETE bundle; the isolated
compiler artifact's 0-byte placeholder is forbidden from a user build.

**Integrated full R12 test-only candidate:** 34 ZIP entries,
SHA-256 `ff1cb0bd88cab9928c70e11d4e5e4d2fa29f08987552f683d10866801e7c6d75`.
L2 ZIP CRC, manifest and source SHA checks PASS. Compared to R11, only
the two approved room-list PNGs, the exact compiled DLL, BUILD_INFO.json and
the readme changed; the remaining 29 entries are **byte-identical**, including
the fully approved private floor atlas tile 376, two preview PNGs, both
uploaded room XMLs, independent two-device atlas, genuine Harmony1,
clinical resources and installer. Old/R11 DLLs and room icon PNG SHA are
REJECTED by builder and independent auditor.

**Evidence limit:** R12 complete package L2 PASS, true Windows L3 PASS,
but **new room-list icon L4 NOT RUN**. Original floor L4 PASS remains the
regression target; do not claim R12 appearance correct until a single targeted
native game check. No auto merge, no release, no other Mods or original game
files touched.
