# Folha de Produção & Prompts Técnicos — Retorno Adidas Ramp 90s

## 1. Gestão de Assets e Entregáveis

| Código do Asset | Descrição do Asset | Formato Primário | Destino na Pasta | Ferramenta Recomendada |
|---|---|---|---|---|
| `KV-MASTER-01` | Key Visual Oficial da Campanha com Lettering "FEITO PRA LIXA" e Trefoil | 4:5 e 9:16 | `final/assets/kv/` | Higgsfield CLI + `gpt_image_2` |
| `STILL-PROD-01` | Still Editorial do Adidas Ramp em bloco de concreto áspero com marcas de lixa | 4:5 e 1:1 | `final/assets/principais/` | Higgsfield CLI + Nano Banana 2 |
| `ACTION-FISHEYE-02` | Skatista no ar em kickflip sobre escadaria, ângulo fisheye extremo (VX1000) | 9:16 e 4:5 | `final/assets/principais/` | Higgsfield CLI + Nano Banana 2 |
| `MACRO-DETAIL-03` | Macro close-up na língua estufada, fat laces e bordado Trefoil clássico | 1:1 e 4:5 | `final/assets/secundarias/` | Higgsfield CLI + Nano Banana 2 |
| `ZINE-COLLAGE-04` | Composição estilo fanzine com textura xerox preto e branco, grampos e fita adesiva | 9:16 (Stories) | `final/assets/secundarias/` | Higgsfield CLI + `gpt_image_2` |
| `AD-STORY-9x16` | Peça de Anúncio Vertical (Stories / TikTok / Reels) com safe zone para CTA | 9:16 | `final/ads/9x16/` | Editor / Composição Master |
| `AD-FEED-4x5` | Peça de Anúncio de Feed com hierarquia editorial forte | 4:5 | `final/ads/4x5/` | Editor / Composição Master |
| `AD-DISPLAY-16x9` | Banner Display para site Adidas Confirmed e portal de streetwear | 16:9 | `final/ads/16x9/` | Editor / Composição Master |

---

## 2. Prompts Técnicos de Geração Visual

### Prompt 01 — Key Visual Master (Com Lettering e Composição de Cartaz)
> **Engine**: `gpt_image_2` via Higgsfield CLI  
> **Aspect Ratio**: `--ar 4:5` (e desdobramento `--ar 9:16`)  
> **Prompt**:  
> `An authentic 1990s underground skateboard magazine print ad and street poster for the rerelease of the classic Adidas Ramp sneaker. Bold brutalist composition inspired by 1990s DIY punk skate fanzines and Ray Gun magazine layouts. In the center, a rugged low-angle shot of the chunky 1990s Adidas Ramp skate sneaker in rich navy-blue suede with bold white leather three stripes, puffy stuffed tongue, fat cotton laces, and a durable gum rubber cupsole, resting on a chipped urban concrete ledge dusted with skate wax and grip tape scuffs. Raw direct on-camera flash photography, harsh deep shadows, authentic 35mm film grain, slightly weathered paper texture with visible photocopy halftones, tape strips on the corners, and subtle photocopied fold marks. Across the top in heavy distressed black-and-white xerox-style typography, the headline reads: 'FEITO PRA LIXA.' In the lower right corner, a vintage Adidas Trefoil heritage skateboarding logo with a weathered red rubber stamp that says 'OFFICIAL 90s RE-ISSUE'. Atmospheric, gritty, uncompromising street culture aesthetic, cinematic realism.`

### Prompt 02 — Still de Produto Editorial (Camurça e Concreto)
> **Engine**: Nano Banana 2 via Higgsfield CLI  
> **Aspect Ratio**: `--ar 4:5`  
> **Prompt**:  
> `Editorial product photograph of the vintage 1990s Adidas Ramp chunky skateboarding shoe resting sideways on a broken weathered block of city sidewalk concrete. Macro shot showing the tactile texture of thick heavyweight navy blue suede, prominent white double-stitched leather stripes, ultra-wide puffy tongue, and textured natural gum cupsole. Subtle authentic grey grip tape scuff marks on the ollie friction zone and specks of street wax on the toe cap, proving the shoe has been skated hard. Low-key direct flashlight beam illumination cutting through darkness, heavy film grain, shot on 35mm Kodak Portra 800, authentic urban street realism, highly detailed fabric and rubber texture, zero 3D render feel, gritty and raw.`

### Prompt 03 — Ação em Lente Fisheye Noturna (Skate nos Anos 90)
> **Engine**: Nano Banana 2 via Higgsfield CLI  
> **Aspect Ratio**: `--ar 9:16`  
> **Prompt**:  
> `Extreme low-angle ground-level fisheye action shot of a young street skateboarder doing an aggressive kickflip down a 6-step marble city stair set at night. Captured with an iconic vintage Sony DCR-VX1000 video camera with Century Optics Mk1 fisheye lens, featuring pronounced circular lens barrel distortion and subtle optical aberration at the frame edges. The focus is laser-sharp on the skateboarder's feet wearing the chunky navy and white 1990s Adidas Ramp sneakers in mid-air rotation over the grip tape. Hard dual off-camera strobe flashes freezing the dynamic motion, deep pitch-black city night sky in the background with blurry streetlamps, asphalt ground texture, raw Hi8/VHS videotape aesthetic, authentic nostalgic skate video still from 1996.`

### Prompt 04 — Macro Detalhe (Fat Laces e Língua Estufada)
> **Engine**: Nano Banana 2 via Higgsfield CLI  
> **Aspect Ratio**: `--ar 1:1`  
> **Prompt**:  
> `Extreme macro detail photograph looking directly down at the tongue and lacing system of the 1990s Adidas Ramp skate shoe. Hands with weathered knuckles and calluses pulling tight the extra-wide 20mm white woven cotton fat laces. Ultra-puffy padded shoe tongue in dark navy blue mesh with the embroidered retro white and blue Adidas Trefoil badge clearly visible. Raw harsh direct camera flash, high contrast, tangible tactile cotton weave and plush foam padding textures, dust specks from skateboard grip tape, shot on 35mm point-and-shoot camera, documentary skate photography style.`

---

## 3. Diretrizes de Exportação e Formatação

1. **Perfis de Cor**: sRGB para todas as entregas digitais (web, mobile, anúncios de redes sociais).
2. **Resoluções Mínimas**:
   - Formato 9:16: `1080 x 1920 px`
   - Formato 4:5: `1080 x 1350 px`
   - Formato 16:9: `1920 x 1080 px`
   - Formato 1:1: `1080 x 1080 px`
3. **Safe Zones**:
   - Em 9:16 (Stories/Reels), manter margem de segurança de 250px no topo (área de perfil/stories) e 350px na base (área de legenda, comentários e swipe-up/CTA).
