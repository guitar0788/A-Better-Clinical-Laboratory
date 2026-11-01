ABCL G1 TEST ONLY — NOT ALPHA

1. Exit Project Hospital completely. Use a disposable hospital test save.
2. Download the ONE compiled GitHub Actions artifact after a verified real DLL build.
3. Extract ABCL_G1_Compiled_Install_TestOnly.zip.
4. Double-click INSTALL_G1.cmd and enter the Project Hospital game root directory.
5. The installer builds the three required original-data overrides LOCALLY and creates ONLY
   ProjectHospital_Data/StreamingAssets/Addons/ModABCLG1LeadTest. It never changes base files.
6. Enable code mods in game settings and restart. Use the ABCL G1 [Test] panel to request
   exactly one lead poisoning patient (TRM_LDP). The hospital still needs operating departments.
7. Test the independent ABCL blood-lead sampling/analysis and confirm vanilla CBC still works.
8. Save/reload with addon still installed; DO NOT open a save depending on G1 after uninstall.
9. Never ship test patient spawning in an Alpha or Stable package.
10. A successful GitHub DLL build is L3 only; gameplay L4 remains a separate gate.
