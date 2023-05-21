# pylint: disable=missing-module-docstring, wildcard-import, unused-wildcard-import, missing-function-docstring, invalid-name, missing-class-docstring
from diff_match_patch import diff_match_patch

dmp = diff_match_patch()

text1 = "Hello World."
text2 = "Goodbye World."

patch = dmp.patch_make(text1, text2)
dmp.patch_toText(patch)

patchStr = dmp.patch_toText(patch)