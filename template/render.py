"""Render a TrustForms poster: python3 render.py spec.json out.jpg"""
import json, sys, subprocess, tempfile, os
from PIL import Image
here = os.path.dirname(os.path.abspath(__file__))
spec = json.load(open(sys.argv[1]))
tpl = open(os.path.join(here, "poster.html")).read()
page = tpl.replace("<script>\nconst S", "<script>window.SPEC=" + json.dumps(spec) + ";</script>\n<script>\nconst S", 1)
tmp = tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, dir=here); tmp.write(page); tmp.close()
png = tmp.name + ".png"
subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                "--allow-file-access-from-files", "--force-device-scale-factor=1",
                "--window-size=1080,1350", "--virtual-time-budget=3000", f"--screenshot={png}", "file://" + tmp.name],
               check=True, capture_output=True)
Image.open(png).convert("RGB").save(sys.argv[2], "JPEG", quality=92)
os.remove(tmp.name); os.remove(png)
print("saved", sys.argv[2])
