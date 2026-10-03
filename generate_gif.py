import os
import random
from PIL import Image, ImageDraw, ImageFont

W, H = 800, 401
HEADER_H = 45
STATUS_Y0 = 327
STATUS_Y1 = 401

TITLE_DEFAULT = "abdochiguer_v1.0.0"

WORDS = [
    ("welcome_visitor", "NODE_LOADED"),
    ("compile_res", "MEMORY_ALLOCATED"),
    ("verify_connections", "STACK_OVERFLOW_AVOIDED"),
    ("synchronize_threads", "THREADS_SYNCHRONIZED"),
    ("scan_memory", "GARBAGE_COLLECTION_ACTIVE")
]

def get_glitched_title(title, glitch_level=0.3):
    chars = list(title)
    symbols = "!@#$%^&*()_+{}[]:;<>?/~"
    for i in range(len(chars)):
        if random.random() < glitch_level:
            chars[i] = random.choice(symbols)
    return "".join(chars)

def create_frame(title, typed_cmd, cursor_visible, status_text, fonts, mask):
    window = Image.new('RGBA', (W, H), (0, 0, 0, 255))
    w_draw = ImageDraw.Draw(window)

    # Header bar
    w_draw.rectangle([0, 0, W, HEADER_H], fill=(30, 30, 30, 255))

    # macOS window buttons
    # Red
    w_draw.ellipse([18, 17, 30, 29], fill=(255, 95, 86))
    # Yellow
    w_draw.ellipse([42, 17, 54, 29], fill=(255, 189, 46))
    # Green
    w_draw.ellipse([66, 17, 78, 29], fill=(39, 201, 63))

    font_header, font_term, font_term_bold, font_status = fonts

    # Header Title
    bbox = w_draw.textbbox((0, 0), title, font=font_header)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    w_draw.text(((W - tw) // 2, (HEADER_H - th) // 2 - 2), title, font=font_header, fill=(160, 160, 160))

    # Terminal logs
    start_x = 28
    y = 75
    line_spacing = 38

    # Line 1: prompt + ./init-server.sh
    cur_x = start_x
    w_draw.text((cur_x, y), "abdochiguer@main-node", font=font_term_bold, fill=(46, 204, 113))
    cur_x += w_draw.textlength("abdochiguer@main-node", font=font_term_bold)

    w_draw.text((cur_x, y), ":/home", font=font_term_bold, fill=(59, 130, 246))
    cur_x += w_draw.textlength(":/home", font=font_term_bold)

    w_draw.text((cur_x, y), " $ ", font=font_term_bold, fill=(255, 255, 255))
    cur_x += w_draw.textlength(" $ ", font=font_term_bold)

    w_draw.text((cur_x, y), "./init-server.sh", font=font_term, fill=(255, 107, 129))

    # Logs
    logs = [
        "[2026-10-04 00:30:03]: » Fetching abdochiguer's server config...",
        "[2026-10-04 00:30:05]: » Compiling Abdo's web server. Initializing caffeine protocol",
        "[2026-10-04 00:30:06]: » CPU approaching 95°C. Either you're on a microwave, or using Chrome.",
        "[2026-10-04 00:30:06]: » Running on 127.0.0.1:3000"
    ]

    for log in logs:
        y += line_spacing
        w_draw.text((start_x, y), log, font=font_term, fill=(224, 224, 224))

    # Line 6: Active Interactive Prompt
    y += line_spacing + 5
    cur_x = start_x
    w_draw.text((cur_x, y), "abdochiguer@main-node", font=font_term_bold, fill=(46, 204, 113))
    cur_x += w_draw.textlength("abdochiguer@main-node", font=font_term_bold)

    w_draw.text((cur_x, y), ":/home", font=font_term_bold, fill=(59, 130, 246))
    cur_x += w_draw.textlength(":/home", font=font_term_bold)

    w_draw.text((cur_x, y), " $ ", font=font_term_bold, fill=(255, 255, 255))
    cur_x += w_draw.textlength(" $ ", font=font_term_bold)

    if typed_cmd:
        w_draw.text((cur_x, y), typed_cmd, font=font_term, fill=(255, 107, 129))
        cur_x += w_draw.textlength(typed_cmd, font=font_term)

    if cursor_visible:
        w_draw.text((cur_x + 1, y - 1), "|", font=font_term_bold, fill=(255, 107, 129))

    # Status Bar at bottom
    w_draw.rectangle([0, STATUS_Y0, W, STATUS_Y1], fill=(28, 28, 28, 255))

    sb_bbox = w_draw.textbbox((0, 0), status_text, font=font_status)
    sb_w = sb_bbox[2] - sb_bbox[0]
    sb_h = sb_bbox[3] - sb_bbox[1]
    sb_x = (W - sb_w) // 2
    sb_y = STATUS_Y0 + (STATUS_Y1 - STATUS_Y0 - sb_h) // 2 - 2
    w_draw.text((sb_x, sb_y), status_text, font=font_status, fill=(0, 230, 118))

    # Rounded window mask
    final_img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    final_img.paste(window, (0, 0), mask)
    return final_img

def main():
    print("Generating animated GIF...")

    # Load Fonts
    font_header = ImageFont.truetype('C:/Windows/Fonts/consola.ttf', 14)
    font_term = ImageFont.truetype('C:/Windows/Fonts/consola.ttf', 15)
    font_term_bold = ImageFont.truetype('C:/Windows/Fonts/consolab.ttf', 15)
    font_status = ImageFont.truetype('C:/Windows/Fonts/consolab.ttf', 16)
    fonts = (font_header, font_term, font_term_bold, font_status)

    mask = Image.new('L', (W, H), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, W - 1, H - 1], radius=10, fill=255)

    frames = []
    durations = []

    global_frame_count = 0

    for word, status in WORDS:
        # Phase 1: Typing characters
        for char_idx in range(1, len(word) + 1):
            cmd_sub = word[:char_idx]
            global_frame_count += 1
            is_glitch = (global_frame_count % 32 in [1, 2])
            title = get_glitched_title(TITLE_DEFAULT) if is_glitch else TITLE_DEFAULT

            f = create_frame(title, cmd_sub, cursor_visible=True, status_text=status, fonts=fonts, mask=mask)
            frames.append(f)
            durations.append(75)

        # Phase 2: Pause at full word with blinking cursor
        for pause_idx in range(10):
            global_frame_count += 1
            cursor_vis = (pause_idx % 4 < 2)
            is_glitch = (global_frame_count % 32 in [1, 2])
            title = get_glitched_title(TITLE_DEFAULT) if is_glitch else TITLE_DEFAULT

            f = create_frame(title, word, cursor_visible=cursor_vis, status_text=status, fonts=fonts, mask=mask)
            frames.append(f)
            durations.append(90)

        # Phase 3: Backspacing characters (faster)
        for char_idx in range(len(word) - 1, -1, -2):
            cmd_sub = word[:char_idx]
            global_frame_count += 1
            is_glitch = (global_frame_count % 32 in [1, 2])
            title = get_glitched_title(TITLE_DEFAULT) if is_glitch else TITLE_DEFAULT

            f = create_frame(title, cmd_sub, cursor_visible=True, status_text=status, fonts=fonts, mask=mask)
            frames.append(f)
            durations.append(45)

        # Phase 4: Small pause empty before next word
        for pause_idx in range(4):
            global_frame_count += 1
            cursor_vis = (pause_idx % 2 == 0)
            is_glitch = (global_frame_count % 32 in [1, 2])
            title = get_glitched_title(TITLE_DEFAULT) if is_glitch else TITLE_DEFAULT

            f = create_frame(title, "", cursor_visible=cursor_vis, status_text=status, fonts=fonts, mask=mask)
            frames.append(f)
            durations.append(70)

    print(f"Total generated frames: {len(frames)}")

    # Optimize and save as GIF
    # Convert frames to 'P' mode with adaptive palette to keep GIF crisp and small
    print("Converting frames to palette mode...")
    p_frames = []
    for f in frames:
        # Create solid black background behind transparent corners
        bg = Image.new('RGB', (W, H), (13, 17, 23)) # GitHub dark mode background #0d1117
        bg.paste(f, (0, 0), f)
        p_frames.append(bg.quantize(colors=128, method=Image.Resampling.LANCZOS))

    out_path = "assets/main-intro_animation.gif"
    print(f"Saving to {out_path}...")
    p_frames[0].save(
        out_path,
        save_all=True,
        append_images=p_frames[1:],
        duration=durations,
        loop=0,
        optimize=True
    )
    print(f"GIF saved successfully at {out_path}!")

if __name__ == "__main__":
    main()
