#!/usr/bin/env python3
import json
import re

with open("imgbed-upload-map.json", "r", encoding="utf-8") as f:
    upload_map = json.load(f)

def replace_in_file(filepath, replacements):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    modified = False
    for old, new in replacements.items():
        if old in content:
            content = content.replace(old, new)
            modified = True
            print(f"[{filepath}] Replaced: {old} -> {new}")
        else:
            print(f"[{filepath}] Warning: could not find target to replace: {old}")
            
    if modified:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Saved changes to {filepath}")

# 1. src/config/backgroundWallpaper.ts
bg_replacements = {}
for i in range(1, 7):
    old_d = f'"assets/images/DesktopWallpaper/d{i}.avif"'
    key_d = f"src/assets/images/DesktopWallpaper/d{i}.avif"
    if key_d in upload_map:
        bg_replacements[old_d] = f'"{upload_map[key_d]}"'
        
    old_m = f'"assets/images/MobileWallpaper/m{i}.avif"'
    key_m = f"src/assets/images/MobileWallpaper/m{i}.avif"
    if key_m in upload_map:
        bg_replacements[old_m] = f'"{upload_map[key_m]}"'

replace_in_file("src/config/backgroundWallpaper.ts", bg_replacements)

# 2. src/config/profileConfig.ts
replace_in_file("src/config/profileConfig.ts", {
    'avatar: "assets/images/avatar.avif"': f'avatar: "{upload_map["src/assets/images/avatar.avif"]}"'
})

# 3. src/config/siteConfig.ts
replace_in_file("src/config/siteConfig.ts", {
    'logo: {\n\t\t\ttype: "image",\n\t\t\tvalue: "assets/images/logo/firefly-light.png",\n\t\t\tvalueDark: "assets/images/logo/firefly-dark.png",\n\t\t\talt: "🍀",\n\t\t}': 
    f'logo: {{\n\t\t\ttype: "url",\n\t\t\tvalue: "{upload_map["src/assets/images/logo/firefly-light.png"]}",\n\t\t\tvalueDark: "{upload_map["src/assets/images/logo/firefly-dark.png"]}",\n\t\t\talt: "🍀",\n\t\t}}'
})

# 4. src/config/sponsorConfig.ts
replace_in_file("src/config/sponsorConfig.ts", {
    'qrCode: "/assets/images/sponsor/alipay.jpg"': f'qrCode: "{upload_map["public/assets/images/sponsor/alipay.jpg"]}"',
    'qrCode: "/assets/images/sponsor/wechat.png"': f'qrCode: "{upload_map["public/assets/images/sponsor/wechat.png"]}"'
})

# 5. src/config/agentRotationConfig.ts
agent_replacements = {}
agents = ["ellen", "anby", "jane", "nicole", "zhuyuan"]
for ag in agents:
    key_anim = f"public/assets/images/agents/{ag}.webp"
    key_static = f"public/assets/images/agents/{ag}-static.png"
    if key_anim in upload_map:
        agent_replacements[f'avatarAnimated: "/assets/images/agents/{ag}.webp"'] = f'avatarAnimated: "{upload_map[key_anim]}"'
    if key_static in upload_map:
        agent_replacements[f'avatarStatic: "/assets/images/agents/{ag}-static.png"'] = f'avatarStatic: "{upload_map[key_static]}"'

replace_in_file("src/config/agentRotationConfig.ts", agent_replacements)

# 6. src/config/sidebarConfig.ts
replace_in_file("src/config/sidebarConfig.ts", {
    'src: "/assets/images/ad/ad1.webp"': f'src: "{upload_map["public/assets/images/ad/ad1.webp"]}"'
})

# 7. src/config/musicConfig.ts
replace_in_file("src/config/musicConfig.ts", {
    'cover: "/assets/music/cover/109951169585655912.webp"': f'cover: "{upload_map["public/assets/music/cover/109951169585655912.webp"]}"'
})

# 8. src/config/booknavConfig.ts
replace_in_file("src/config/booknavConfig.ts", {
    'icon: "/favicon/firefly-32.png"': f'icon: "{upload_map["public/favicon/firefly-32.png"]}"'
})

# 9. src/components/features/BangbooWidget.astro
idle_url = upload_map["public/assets/images/bangboo/bangboo-idle.webp"]
active_url = upload_map["public/assets/images/bangboo/bangboo-active.webp"]
replace_in_file("src/components/features/BangbooWidget.astro", {
    'src={url("/assets/images/bangboo/bangboo-idle.webp")}': f'src={{{{url("{idle_url}")}}}}',
    'src={url("/assets/images/bangboo/bangboo-active.webp")}': f'src={{{{url("{active_url}")}}}}'
})

# 10. src/components/features/SakuraEffect.astro & worker
replace_in_file("src/components/features/SakuraEffect.astro", {
    'this.img.src = "/assets/images/effects/sakura.png"': f'this.img.src = "{upload_map["public/assets/images/effects/sakura.png"]}"'
})

replace_in_file("src/workers/sakura.worker.ts", {
    'await fetch("/assets/images/effects/sakura.png")': f'await fetch("{upload_map["public/assets/images/effects/sakura.png"]}")'
})

# 11. Post covers
replace_in_file("src/content/posts/guide/index.md", {
    'image: "./cover.webp"': f'image: "{upload_map["src/content/posts/guide/cover.webp"]}"'
})

replace_in_file("src/content/posts/inputMD/tiger-code.md", {
    'image: "./cover.webp"': f'image: "{upload_map["src/content/posts/inputMD/cover.webp"]}"'
})

# 12. Dynamic memos
dyn_replacements = {}
ax1x_urls = [
    "https://s41.ax1x.com/2026/05/13/peXsfit.webp",
    "https://s41.ax1x.com/2026/05/13/peXs2dA.webp",
    "https://s41.ax1x.com/2026/05/13/peXshJP.webp",
    "https://s41.ax1x.com/2026/05/13/peXsRII.webp",
    "https://s41.ax1x.com/2026/05/13/peXyWm4.jpg",
    "https://s41.ax1x.com/2026/05/13/peXyf0J.jpg",
    "https://s41.ax1x.com/2026/05/13/peXyh79.jpg"
]
for u in ax1x_urls:
    if u in upload_map:
        dyn_replacements[u] = upload_map[u]

replace_in_file("src/content/dynamic/2026-07-15-010756.md", dyn_replacements)
replace_in_file("public/gallery/firefly-2026/urls.txt", dyn_replacements)
replace_in_file("public/gallery/encrypted-test/urls.txt", dyn_replacements)

# 13. README docs
docs_replacements = {
    './docs/images/1131.png': upload_map["docs/images/1131.png"],
    './docs/images/1.webp': upload_map["docs/images/1.webp"],
    './docs/images/2.webp': upload_map["docs/images/2.webp"],
    './docs/images/3.webp': upload_map["docs/images/3.webp"],
    './docs/images/4.webp': upload_map["docs/images/4.webp"],
    './docs/images/Lighthouse.png': upload_map["docs/images/Lighthouse.png"]
}

for doc_file in ["README.md", "README.en.md", "docs/README.ja.md", "docs/README.zh-TW.md"]:
    replace_in_file(doc_file, docs_replacements)

print("\nFinished replacing all image links!")
