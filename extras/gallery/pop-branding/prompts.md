# Pop branding — generation prompts

内蔵の画像生成ツールを使用。アイコンとバナーの参照画像は、採用テイストの [pop trio cover](../spotify-cover/proposals/kaberadio_spotify_cover_proposal_gen_04_pop_trio.png)。以下は各生成に渡した全文です。

## Pop trio cover — original prompt

参照順：あまかわちゃんの秋アイコン、モブ子の秋エンドカード、モブ美のキャラクター原画。モブ美の原画はAmakawachan Systemのcharacter-builder/jobs/mobumi/source/source.pngを使用しました。

```text
Create a completely new square podcast jacket for 「壁ラジ」. This is a bold, simple POP cartoon graphic, with immediate recognition as a tiny podcast thumbnail. Use the references ONLY to identify the three fictional characters. Radically simplify their rendering into charming flat editorial cartoon mascots with chunky slightly hand-drawn dark teal outlines, large graphic hair shapes, small simple faces, flat colors, and almost no shading. Do NOT retain the detailed anime painting style, lighting, poses, backgrounds, or clothing textures of the references.

Layout: solid warm sunflower-yellow background. Huge playful custom Japanese lettering 「壁ラジ」 across the upper 40 percent, coral-red fill with bold dark teal outline. Title must be spelled exactly and immediately readable. Bottom half: three friendly front-facing cartoon busts together in a neat row, overlapping shoulders slightly, drawn as one cohesive ensemble. Left is Mobuko (reference 2): long pale-blonde wavy hair simplified into broad shapes, green eyes, a few freckles, brown beret, simple cream top. Center is Amakawachan (reference 1): dark green-black bob, round glasses, sleepy amused eyes, tiny fangs, one or two ear piercings, dark shirt. Right is Mobumi (reference 3): copper-red shoulder-length curled hair, pale gray eyes, freckles, simple cream blouse. All three face the viewer. Distinct warm casual expressions, gently mischievous and approachable. Upright poses, no hands resting on cheeks. Big heads and small shoulders, stylized illustration characters, not detailed anime pin-ups.

Keep the design extremely economical: three faces, one huge title, a single tiny speech-bubble doodle. Plenty of clean yellow negative space. Dark teal, coral red, yellow and cream as the main palette, with only necessary hair and eye colors. A little uneven hand-drawn character in outlines is welcome. No gradients, no glow, no shadows, no texture-rich rendering, no recording studio, no scenery, no props, no microphones, no headphones, no ornate frames, no subtitle, no small text, no cat mascot, no 3D, no collage. An original cheerful character-led podcast cover, confident and simple.
```

## Banner safe-area revision

初回バナーを参照して以下の編集を行いました。

```text
Edit the supplied YouTube banner. Preserve the exact Mobuko illustration, Japanese 壁ラジ logo, speech bubble, colors and overall design. Scale the ENTIRE central illustration-and-logo group uniformly to 62 percent of its current size, centered both vertically and horizontally in the same full 16:9 yellow canvas. The group currently occupies about 56% of width and 40% of height; the final group must occupy only about 35% of canvas width and 25% of height. All the other space is continuous plain yellow matching the existing background. At 1672x941 the complete group should fit inside x=535..1137 and y=350..591. Do not enlarge or reframe the canvas around the group. Preserve the large empty top and bottom areas. Do not add anything or change typography or character design. Output one full 16:9 banner, ideally 2560x1440, no guides.
```

## Radio motif background revision

参照画像：youtube_banner_2560x1440.png。内蔵画像生成ツールで外側のラジオモチーフを追加。出力原本はyoutube_banner_radio_pattern_original.png、設定用はyoutube_banner_radio_pattern_2560x1440.png。

```text
Edit the supplied full 16:9 YouTube banner. Preserve the existing small centered Mobuko portrait, speech bubble and exact Japanese 壁ラジ logo, with their current scale, position, colors and legibility. Do not enlarge or move the central branding: all of it must remain inside the centered 60%-wide, 29%-high mobile safe region. Keep a quiet yellow halo around this central group.
Enrich the currently empty surrounding yellow canvas with a simple cheerful POP radio-themed pattern, matching the chunky dark teal outlines and coral-red, cream and yellow palette. Scatter about 14-18 generously spaced flat doodle icons across the upper and lower outer regions: retro tabletop radios, microphones, headphones, speech bubbles, music notes, simple sound waves, circles, triangles and small stars. Mix medium-sized radio motifs with small geometric accents. Put a modest radio or headphone motif near each far left/right side at mid-height so the desktop crop also has interest. The pattern should feel intentionally balanced across the full TV view, with plenty of breathing room and no busy texture. Some icons may be partially cropped at the outer canvas edges. Central mobile crop remains clear and readable; no doodles over the face, beret or title. All motifs share the same flat cartoon finish, thick dark teal strokes, limited coral/cream fills and a few lower-contrast golden-yellow outlines. No new text or numbers, no additional characters, no detailed scenery, no gradients, no 3D, no frame, no crop guides. Whole canvas 16:9, ideally 2560x1440. The result should feel complete on TV and desktop and preserve the clean original central composition on phones.
```


## Mobuko icon

```text
Create a square profile icon matching the supplied approved 壁ラジ pop cover precisely in visual taste: sunflower-yellow background, confident chunky dark teal outlines, simple playful cartoon illustration, restrained coral-red accent, clean large shapes. Show ONLY Mobuko, the blonde character on the LEFT of the reference. Pale blonde long wavy hair, green relaxed eyes, a few freckles, brown beret, cream top. Preserve her recognizable face and hair but simplify into the same friendly cartoon style. Front-facing head-and-shoulders portrait, cheerful small open-mouth smile, no hands near face. Center the head within the middle 65% of the square so the beret, face and key hair silhouette remain fully visible inside a circular avatar crop. Comfortable yellow margin all around; shoulder tips may reach the bottom. Simple solid yellow background, one tiny coral speech bubble beside the shoulder if useful. No title, no lettering, no other people, no frame, no microphone, no elaborate background, no realistic shading, no texture. The face must read at 48 pixels. One finished square icon, no mockups.
```

## YouTube banner

```text
Create a YouTube channel banner for 壁ラジ in the SAME simple pop cartoon visual identity as the supplied approved cover. Output a 16:9 full canvas, ideally exactly 2560 x 1440 pixels. This is a full YouTube channel-art canvas with a SMALL central horizontal composition and very large empty yellow areas above and below.
CRITICAL SAFE AREA: all meaningful artwork must fit within the centered rectangle x=540..2020, y=525..915 on a 2560x1440 canvas (58% of canvas width and 27% of canvas height). Do not draw safe-area guides. The top 36% and bottom 36% of the full image should be plain sunflower yellow. The outer left and right 20% should be plain yellow.
Inside that central strip: on the left, a compact front-facing head-and-shoulders illustration of ONLY Mobuko, the blonde character on the LEFT of the reference: long pale blonde wavy hair simplified into graphic shapes, green eyes, freckles, brown beret, cream top, friendly playful smile. Her entire beret and face fit within the safe strip. On her right, very clear large coral-red Japanese lettering with dark teal outlines reading exactly 「壁ラジ」, with enough breathing space between the face and text. The logo and Mobuko form one balanced horizontal lockup. One tiny simple dark teal speech bubble is enough decoration.
Use chunky dark teal outlines, cheerful flat colors, clean simple editorial cartoon styling faithfully matching the reference. A yellow background fills the whole canvas continuously. No detailed studio, no glow, no ornate frame, no extra characters, no subtitle, no extra text, no crop marks, no 3D, no realistic rendering. Do not fill the canvas with a giant portrait or giant text: this must remain a small centered horizontal lockup suitable for the mobile YouTube banner crop.
```

