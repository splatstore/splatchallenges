#!/usr/bin/env python3
"""Generate SPLAT video store HTML detail pages"""

import re
from pathlib import Path
from typing import Dict, List

# Video database
VIDEOS = [
    {"id": "AE01", "name": "AERIAL 1. Pies & Chocolate", "price": 10, "model": "AERIAL", "tags": ["Pie","Cake"]},
    {"id": "AE02", "name": "AERIAL 2. Splat Spa Salon", "price": 12, "model": "AERIAL", "tags": ["Pie","Cake","Laying down"]},
    {"id": "AE03", "name": "AERIAL 3. Shave & Shower", "price": 10, "model": "AERIAL", "tags": ["Shower"]},
    {"id": "BB01", "name": "BABY 1. Pie Challenge", "price": 10, "model": "BABY", "tags": ["Pie"]},
    {"id": "BB02", "name": "BABY 2. Vain Model", "price": 10, "model": "BABY", "tags": ["Pie","Slime"]},
    {"id": "BB03", "name": "BABY 3. SO CLUMSY! THE NERD", "price": 12, "model": "BABY", "tags": ["Pie","Laying down"]},
    {"id": "BB04", "name": "BABY 4. Messy Workout", "price": 10, "model": "BABY", "tags": ["Pie","Cake","Slime"]},
    {"id": "BB05", "name": "BABY 5. Extreme Challenge", "price": 12, "model": "BABY", "tags": ["Pie","Cake","Feet"]},
    {"id": "BK01", "name": "BIKE 1. The Audition", "price": 10, "model": "BIKE", "tags": ["Pie","Feet"]},
    {"id": "BK02", "name": "BIKE 2. Birthday Pie Party", "price": 10, "model": "BIKE", "tags": ["Pie","Cake","Slime"]},
    {"id": "BK03", "name": "BIKE 3. Vainilla Or Chocolate", "price": 10, "model": "BIKE", "tags": ["Pie","Cake","Feet"]},
    {"id": "BK04", "name": "BIKE 4. The Detention", "price": 10, "model": "BIKE", "tags": ["Pie","Cake"]},
    {"id": "BK05", "name": "BIKE 5. Splat Spa Salon", "price": 12, "model": "BIKE", "tags": ["Pie","Cake","Laying down"]},
    {"id": "BU01", "name": "BUTTERFLY 1. Pie Challenge", "price": 10, "model": "BUTTERFLY", "tags": ["Pie","Laying down","Feet"]},
    {"id": "BU02", "name": "BUTTERFLY 2. The Splatter's Joke", "price": 10, "model": "BUTTERFLY", "tags": ["Pie"]},
    {"id": "BU03", "name": "BUTTERFLY 3. The Final Test", "price": 12, "model": "BUTTERFLY", "tags": ["Pie","Cream","Laying down"]},
    {"id": "BU04", "name": "BUTTERFLY 4. Pie Techniques", "price": 10, "model": "BUTTERFLY", "tags": ["Pie","Cake"]},
    {"id": "CA01", "name": "CANDY 1. Pies & Slime", "price": 10, "model": "CANDY", "tags": ["Pie","Slime"]},
    {"id": "CA02", "name": "CANDY 2. HOW TO PIE YOURSELF", "price": 10, "model": "CANDY", "tags": ["Pie","Laying down"]},
    {"id": "CB01", "name": "CARIBBEAN 1. QUESTIONS & ANSWERS", "price": 10, "model": "CARIBBEAN", "tags": ["Pie","Cake"]},
    {"id": "CB02", "name": "CARIBBEAN 2. VAIN MODEL", "price": 12, "model": "CARIBBEAN", "tags": ["Pie","Slime","Feet"]},
    {"id": "CB03", "name": "CARIBBEAN 3. TEACHING SIGN LANGUAGE", "price": 10, "model": "CARIBBEAN", "tags": ["Pie"]},
    {"id": "CT01", "name": "CUTIE 1. Do It Better Game", "price": 10, "model": "CUTIE", "tags": ["Pie","Cake"]},
    {"id": "CT02", "name": "CUTIE 2. Feet & Pies", "price": 10, "model": "CUTIE", "tags": ["Pie","Feet"]},
    {"id": "FT01", "name": "FITNESS 1. Pies & Cakes", "price": 10, "model": "FITNESS", "tags": ["Pie","Cake"]},
    {"id": "FT02", "name": "FITNESS 2. Pie Challenge", "price": 10, "model": "FITNESS", "tags": ["Pie","Cake","Feet"]},
    {"id": "FT03", "name": "FITNESS 3. Five Questions Game", "price": 10, "model": "FITNESS", "tags": ["Pie","Slime"]},
    {"id": "GR01", "name": "GREY 1. The Audition", "price": 10, "model": "GREY", "tags": ["Pie","Slime"]},
    {"id": "GR02", "name": "GREY 2. Living in a Shaving World", "price": 10, "model": "GREY", "tags": ["Pie"]},
    {"id": "JC01", "name": "JACKSON 1. Pie Therapy", "price": 10, "model": "JACKSON", "tags": ["Pie","Feet"]},
    {"id": "JC02", "name": "JACKSON 2. Birthday Pie Party", "price": 10, "model": "JACKSON", "tags": ["Pie","Cake","Slime"]},
    {"id": "JC03", "name": "JACKSON 3. So Clumsy!", "price": 10, "model": "JACKSON", "tags": ["Pie","Laying down"]},
    {"id": "JC05", "name": "JACKSON 5. THE SPLATTER", "price": 10, "model": "JACKSON", "tags": ["Pie"]},
    {"id": "JC06", "name": "JACKSON 6. Slimy Games", "price": 10, "model": "JACKSON", "tags": ["Slime","Laying down"]},
    {"id": "JC07", "name": "JACKSON 7. Splat Spa Salon", "price": 12, "model": "JACKSON", "tags": ["Pie","Laying down"]},
    {"id": "JC08", "name": "JACKSON 8. Extreme Challenge", "price": 12, "model": "JACKSON", "tags": ["Pie","Slime"]},
    {"id": "JC09", "name": "JACKSON 9. Full Body Shaving Challenge", "price": 10, "model": "JACKSON", "tags": []},
    {"id": "JC10", "name": "JACKSON 10. New Year 2023 Special", "price": 10, "model": "JACKSON", "tags": ["Pie","Cake"]},
    {"id": "JC11", "name": "JACKSON 11. Funny Business", "price": 10, "model": "JACKSON", "tags": ["Pie"]},
    {"id": "JC12", "name": "JACKSON 12. Pies & Cakes", "price": 10, "model": "JACKSON", "tags": ["Pie","Cake"]},
    {"id": "JC13", "name": "JACKSON 13. Shave & Shower", "price": 10, "model": "JACKSON", "tags": ["Shower"]},
    {"id": "JC14", "name": "JACKSON 14. The Interrogation", "price": 10, "model": "JACKSON", "tags": ["Pie"]},
    {"id": "JS01", "name": "JISU 1. Teaching How To Pie", "price": 10, "model": "JISU", "tags": ["Pie"]},
    {"id": "JS02", "name": "JISU 2. Birthday Party Goes Wrong", "price": 10, "model": "JISU", "tags": ["Pie","Cake"]},
    {"id": "JS03", "name": "JISU 3. Feet & Pies", "price": 10, "model": "JISU", "tags": ["Pie","Feet"]},
    {"id": "JN01", "name": "JONES 1. What Do You Really Want", "price": 10, "model": "JONES", "tags": ["Pie","Cake"]},
    {"id": "JN02", "name": "JONES 2. TWELVE GRAPES", "price": 10, "model": "JONES", "tags": ["Pie"]},
    {"id": "JN03", "name": "JONES 3. Dirty Jokes", "price": 10, "model": "JONES", "tags": ["Pie","Slime"]},
    {"id": "JN04", "name": "JONES 4. Feet & Pies", "price": 10, "model": "JONES", "tags": ["Pie","Feet"]},
    {"id": "JN05", "name": "JONES 5. Messy Christmas", "price": 10, "model": "JONES", "tags": ["Pie"]},
    {"id": "KT01", "name": "KITTY 1. Pie Challenge", "price": 10, "model": "KITTY", "tags": ["Pie"]},
    {"id": "KT02", "name": "KITTY 2. Bucket Game", "price": 10, "model": "KITTY", "tags": ["Pie","Slime"]},
    {"id": "KT03", "name": "KITTY 3. Birthday Pie Party", "price": 10, "model": "KITTY", "tags": ["Pie","Cake"]},
    {"id": "KT04", "name": "KITTY 4. SPLAT SPA SALON", "price": 12, "model": "KITTY", "tags": ["Pie","Cream","Laying down"]},
    {"id": "KT05", "name": "KITTY 5. Secret Card Game", "price": 10, "model": "KITTY", "tags": ["Pie","Slime"]},
    {"id": "KT06", "name": "KITTY 6. Teaching How To Pie", "price": 10, "model": "KITTY", "tags": ["Pie","Cake"]},
    {"id": "KT07", "name": "KITTY 7. KISSING BOOTH", "price": 10, "model": "KITTY", "tags": ["Pie","Cake"]},
    {"id": "LD01", "name": "LADY 1. Pies & Cakes", "price": 10, "model": "LADY", "tags": ["Pie","Cake"]},
    {"id": "LN01", "name": "LUNA 1. Pies & Cakes", "price": 10, "model": "LUNA", "tags": ["Pie","Cake"]},
    {"id": "LN02", "name": "LUNA 2. Extreme Challenge", "price": 12, "model": "LUNA", "tags": ["Pie","Slime"]},
    {"id": "MG01", "name": "MEGA 1. Pie Therapy", "price": 10, "model": "MEGA", "tags": ["Pie","Feet"]},
    {"id": "MG02", "name": "MEGA 2. Bad Jokes", "price": 10, "model": "MEGA", "tags": ["Pie","Slime"]},
    {"id": "NU01", "name": "NURSEY 1. Pies & Chocolate", "price": 10, "model": "NURSEY", "tags": ["Pie","Cake","Feet"]},
    {"id": "NU02", "name": "NURSEY 2. LAYING DOWN NUTELLA TREATMENT", "price": 12, "model": "NURSEY", "tags": ["Cream","Laying down"]},
    {"id": "PK01", "name": "POKAR 1. Bad Jokes", "price": 10, "model": "POKAR", "tags": ["Pie","Slime","Feet"]},
    {"id": "PK02", "name": "POKAR 2. SPLAT SPA SALON: THOUGH COSTUMER", "price": 12, "model": "POKAR", "tags": ["Pie","Cream","Laying down"]},
    {"id": "PK03", "name": "POKAR 3. EXTREME CHALLENGE", "price": 12, "model": "POKAR", "tags": ["Pie","Slime"]},
    {"id": "PK04", "name": "POKAR 4. Pies & Cakes", "price": 10, "model": "POKAR", "tags": ["Pie","Cake"]},
    {"id": "PK05", "name": "POKAR 5. The Bounty Hunter", "price": 10, "model": "POKAR", "tags": ["Pie"]},
    {"id": "PK06", "name": "POKAR 6. The Kissing Booth", "price": 10, "model": "POKAR", "tags": ["Pie"]},
    {"id": "PW01", "name": "POWER 1. Teaching Spanish", "price": 10, "model": "POWER", "tags": ["Pie","Feet"]},
    {"id": "PW02", "name": "POWER 2. SPLAT PASTRY SCHOOL", "price": 12, "model": "POWER", "tags": ["Pie","Cake","Cream","Laying down"]},
    {"id": "PW03", "name": "POWER 3. School Girl", "price": 10, "model": "POWER", "tags": ["Pie","Slime"]},
    {"id": "SC01", "name": "SCHOOL 1. LEARNING PIE IN THE FACE TECHNIQUES", "price": 10, "model": "SCHOOL", "tags": ["Pie","Laying down"]},
    {"id": "SC02", "name": "SCHOOL 2. So Clumsy! Again...", "price": 10, "model": "SCHOOL", "tags": ["Pie","Laying down"]},
    {"id": "SH01", "name": "SHAY 1. Pies & Cakes", "price": 10, "model": "SHAY", "tags": ["Pie","Cake"]},
    {"id": "SH02", "name": "SHAY 2. Feet & Pies", "price": 10, "model": "SHAY", "tags": ["Pie","Feet"]},
    {"id": "SH03", "name": "SHAY 3. So Hungry", "price": 10, "model": "SHAY", "tags": ["Pie"]},
    {"id": "SM01", "name": "SOMER 1. Do It Better Game", "price": 10, "model": "SOMER", "tags": ["Pie","Cake","Feet"]},
    {"id": "SM02", "name": "SOMER 2. Keep Quiet", "price": 10, "model": "SOMER", "tags": ["Pie","Slime"]},
    {"id": "SP01", "name": "SUPERMOON 1. Messy Challenge", "price": 10, "model": "SUPERMOON", "tags": ["Pie","Slime"]},
    {"id": "SP02", "name": "SUPERMOON 2. Birthday Pie Party", "price": 10, "model": "SUPERMOON", "tags": ["Pie","Cake","Slime"]},
    {"id": "VN01", "name": "VENUS 1. PIE CHALLENGE", "price": 10, "model": "VENUS", "tags": ["Pie"]},
]

EXISTING_FILES = {"AE01", "AE02", "AE03", "BB03", "CA02", "CB01", "CB02", "CB03", "JC00", "JN02", "KT04", "KT07", "NU01", "PK02", "PK03", "PW02", "SC01", "VN01", "AERIAL"}


def load_image_urls() -> Dict[str, List[str]]:
    """Load image URLs from liens.html"""
    liens_file = Path("/Users/antoninaladenise/Downloads/splat7/liens.html")
    urls_map = {}
    
    with open(liens_file, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip() and "img" in line]
    
    current_set = []
    current_key = None
    
    for line in lines:
        match = re.search(r'/([A-Z0-9]+)-img\d+\.jpg', line)
        if match:
            key = match.group(1)
            if current_key and current_key != key and len(current_set) == 5:
                urls_map[current_key] = current_set[:]
                current_set = []
            
            current_key = key
            current_set.append(line)
            
            if len(current_set) == 5:
                urls_map[current_key] = current_set[:]
                current_set = []
                current_key = None
    
    return urls_map


def get_images(video_id: str, urls_map: Dict[str, List[str]]) -> List[str]:
    """Get 5 image URLs for a video"""
    if video_id in urls_map:
        return urls_map[video_id]
    
    video = next((v for v in VIDEOS if v["id"] == video_id), None)
    if not video:
        return urls_map.get("AE01", [])
    
    model = video["model"]
    if model + "1" in urls_map:
        return urls_map[model + "1"]
    if model in urls_map:
        return urls_map[model]
    
    return urls_map.get("AE01", [])


def count_tags(v1: Dict, v2: Dict) -> int:
    """Count common tags"""
    return len(set(v1.get("tags", [])) & set(v2.get("tags", [])))


def get_suggestions(video_id: str) -> List[Dict]:
    """Get 10 related videos"""
    current = next((v for v in VIDEOS if v["id"] == video_id), None)
    if not current:
        return []
    
    scored = [(count_tags(current, v), VIDEOS.index(v), v) for v in VIDEOS if v["id"] != video_id]
    scored = [v for s, i, v in sorted(scored, key=lambda x: (-x[0], x[1]))[:10]]
    return scored


def generate_html(video: Dict, template: str, urls_map: Dict[str, List[str]]) -> str:
    """Generate HTML for a video"""
    images = get_images(video["id"], urls_map)
    if len(images) < 5:
        images = get_images("AE01", urls_map)
    
    main_img = images[0] if images else "https://i.ibb.co/nsVx06nW/AE01-img1.jpg"
    thumbs = images[:5] if len(images) >= 5 else (images + images)[:5]
    tags_str = ", ".join(video.get("tags", []))
    
    html = template
    html = re.sub(r'<title>.*?— SPLAT Store</title>', f'<title>{video["name"]} — SPLAT Store</title>', html)
    html = re.sub(r'id="main-img"[^>]*src="[^"]*"', f'id="main-img" class="gallery-main"\n        src="{main_img}"', html)
    html = re.sub(r'<div class="detail-title">[^<]*</div>', f'<div class="detail-title">{video["name"]}</div>', html)
    html = re.sub(r'Code: <strong>[^<]*</strong>', f'Code: <strong>{video["id"]}</strong>', html)
    html = re.sub(r'Model: <strong>[^<]*</strong>', f'Model: <strong>{video["model"]}</strong>', html)
    html = re.sub(r'Tags: <strong>[^<]*</strong>', f'Tags: <strong>{tags_str}</strong>', html)
    html = re.sub(r'<div class="price-big">\$[0-9]+ USD</div>', f'<div class="price-big">${video["price"]} USD</div>', html)
    
    for i in range(5):
        active = 'active' if i == 0 else ''
        pattern = r'<img class="gallery-thumb[^"]*"\s+src="[^"]*"\s+alt="Image ' + str(i+1) + '"'
        repl = f'<img class="gallery-thumb {active}"\n          src="{thumbs[i]}"\n          alt="Image {i+1}"'
        html = re.sub(pattern, repl, html, count=1)
    
    related = get_suggestions(video["id"])
    suggestions_js = "[\n      " + ",\n      ".join([
        f'{{ href: "{r["id"]}.html", img: "{get_images(r["id"], urls_map)[0]}", title: "{r["name"]}", price: "${r["price"]} USD" }}'
        for r in related
    ]) + "\n    ]"
    
    old_sugg = re.search(r'const allSuggestions = \[[\s\S]*?\];', html)
    if old_sugg:
        html = html.replace(old_sugg.group(0), f'const allSuggestions = {suggestions_js};')
    
    return html


def main():
    print("🎬 SPLAT Video Store HTML Generator")
    print("=" * 50)
    
    template_file = Path("/Users/antoninaladenise/Downloads/splat7/AE01.html")
    with open(template_file, "r") as f:
        template = f.read()
    
    print(f"✅ Template loaded")
    
    urls_map = load_image_urls()
    print(f"✅ Loaded {len(urls_map)} image sets")
    
    output_dir = Path("/Users/antoninaladenise/Downloads/splat7")
    created, skipped, errors = 0, 0, 0
    
    for video in VIDEOS:
        vid = video["id"]
        
        if vid in EXISTING_FILES:
            print(f"⏭️  {vid}")
            skipped += 1
            continue
        
        try:
            html = generate_html(video, template, urls_map)
            (output_dir / f"{vid}.html").write_text(html, encoding="utf-8")
            print(f"✅ {vid}: {video['name'][:40]}")
            created += 1
        except Exception as e:
            print(f"❌ {vid}: {e}")
            errors += 1
    
    print("\n" + "=" * 50)
    print(f"✅ Created: {created} | ⏭️  Skipped: {skipped} | ❌ Errors: {errors}")


if __name__ == "__main__":
    main()
