# R5 L4 FAILURE — Original C# mod loader gate (2026-11-04)

Owner screenshot of R5 shows the Toxicology Laboratory room-list icon missing and a native red-test-tube floor glyph instead of the approved private isometric flask. **Both are L4 FAIL**, not an art rework request.

**Reproduced root cause in original game source:** `TitleScreenController` requires `File.Exists(Path.Combine(modFolder, "0Harmony.dll"))` *before* it calls `Assembly.LoadFrom` to activate any other .dll and instantiate `ModEntryPoint`. The distributed R5 ZIP contains `ModABCLG1LeadTest.dll` but does **not** contain `0Harmony.dll`; its room/floor adapters therefore cannot run. This explains both visual failures without editing a single PNG. The game also requires Code Mods enabled in settings; this cannot be detected from R5 screenshot.

**Corrective test-only dependency:** genuine publisher `pardeike/Harmony` **v1.2.0.1** `Release/net35/0Harmony.dll`, 113152 bytes, SHA-256 `e271d22a7c32bfca105d0e471c04eee14eec6142d37a30cd73cb7d32c7d1dd0f`. Official upstream `Release.zip` SHA-256 `caedf2b27256a3205ff0788a68afb02bd7ce9cf53cd248fde361be46ae329d55`; MIT license included. The loader excludes `0Harmony.dll` itself from scanning; ABCL does not apply Harmony patches and must not bundle Harmony2, fake PE, or zero-byte marker.

Frozen D016: **no artwork changes**. The approved 64x64 opaque menu PNGs, private floor glyph tile 376 atlas, equipment atlas, two free-standing instruments and new 8×6/12×6 prefab XML are byte-pinned and unchanged. Existing genuine net35/CLR2 G1 compilation remains SHA `aada123989f835feb38d8a7d38b1b338e14cc75f` / DLL `72cf86abb5bbb539a5b364aaf314b8f36a4746ca2caab955b191de754ff602c7`. A new bundled loader is packaging, not game-core code modification; a new G1 compile is unnecessary.

R6 is **not** L4-approved: offline archive and code-loader gates can PASS, but the exact native room/floor visual effect still needs one targeted in-game confirmation. Never treat the previous green ZIP audit as a runtime pass.
