import base64
import os

def generate_grand_cadre_circulaire(avatar_path="assets/avatar.png", svg_path="assets/middleLogo.svg"):
    if not os.path.exists(avatar_path):
        print(f"File {avatar_path} not found.")
        return

    with open(avatar_path, "rb") as f:
        img_bytes = f.read()

    b64_str = base64.b64encode(img_bytes).decode("ascii")
    data_uri = f"data:image/png;base64,{b64_str}"

    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 240" width="100%" height="100%">
  <defs>
    <!-- Circular clip path for portrait -->
    <clipPath id="avatarCircle">
      <circle cx="120" cy="120" r="96" />
    </clipPath>

    <!-- Navy Blue Deep Gradient for Frame -->
    <linearGradient id="navyBorder" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#001838" />
      <stop offset="35%" stop-color="#002D62" />
      <stop offset="70%" stop-color="#001F3F" />
      <stop offset="100%" stop-color="#0A192F" />
    </linearGradient>

    <!-- Glowing Accent Ring -->
    <linearGradient id="accentRing" x1="0%" y1="100%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#1E3A8A" />
      <stop offset="50%" stop-color="#2563EB" />
      <stop offset="100%" stop-color="#3B82F6" />
    </linearGradient>

    <!-- Soft Navy Glow Shadow -->
    <filter id="navyGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="5" stdDeviation="7" flood-color="#001F3F" flood-opacity="0.85" />
      <feDropShadow dx="0" dy="0" stdDeviation="3" flood-color="#1E3A8A" flood-opacity="0.5" />
    </filter>
  </defs>

  <style>
    .avatar-frame {{
      animation: popIn 1.1s cubic-bezier(0.16, 1, 0.3, 1) forwards;
      transform-origin: center;
    }}
    @keyframes popIn {{
      0% {{ opacity: 0; transform: scale(0.9); }}
      100% {{ opacity: 1; transform: scale(1); }}
    }}
    .glow-ring {{
      transition: all 0.3s ease;
    }}
  </style>

  <g class="avatar-frame">
    <!-- Outer Deep Navy Circle Frame with Glow -->
    <circle class="glow-ring" cx="120" cy="120" r="110" fill="url(#navyBorder)" stroke="url(#accentRing)" stroke-width="4.5" filter="url(#navyGlow)" />

    <!-- Inner Navy Inset Ring -->
    <circle cx="120" cy="120" r="101" fill="none" stroke="#001026" stroke-width="3.5" />

    <!-- Portrait image clipped in the large circle -->
    <image href="{data_uri}" x="24" y="24" width="192" height="192" clip-path="url(#avatarCircle)" preserveAspectRatio="xMidYMid slice" />

    <!-- Sleek Navy Inner Ring over the photo border -->
    <circle cx="120" cy="120" r="96" fill="none" stroke="#002D62" stroke-width="3" opacity="0.95" />
  </g>
</svg>'''

    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"Generated grand cadre circulaire in {svg_path} successfully!")

if __name__ == "__main__":
    generate_grand_cadre_circulaire()
