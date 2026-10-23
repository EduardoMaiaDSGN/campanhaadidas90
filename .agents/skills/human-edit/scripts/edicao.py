"""Orquestra uma edição: corte -> faixas do split -> telas cheias -> sobreposições -> render -> voz -> som.

O projeto de cada vídeo (projeto.py, a partir de modelos/projeto.py) só declara as decisões (PLANO, PLANOS de tela,
FAIXAS, TELAS_CHEIAS, sobreposições, efeitos sonoros) e chama esta classe. Tudo o que é pesado fica no cache e é
reaproveitado pelo conteúdo: se um trecho não mudou, ele não é renderizado de novo; se mudou, o nome do arquivo
muda junto e o cache velho é simplesmente ignorado (não precisa apagar nada à mão).
"""
import hashlib, json, os, shutil, subprocess, sys
import corte, compor, montagem, tela, som as _som

FPS = 30
BH = montagem.BH                      # altura da faixa 4:3 do split (1080x810)
SCRIPTS = os.path.dirname(os.path.abspath(__file__))

def _h(*xs):
    return hashlib.sha1(repr(xs).encode()).hexdigest()[:12]

def _abs(p):
    return os.path.abspath(os.path.expanduser(p))

class Edicao:
    def __init__(self, src, pasta, cache, transcricao="transcricao.json", cap_gap=-12, grade=None, maxrate=None):
        """src: vídeo bruto. pasta: o _projeto (projeto.py, transcrição, edl.json, vozes).
        cache: renders pesados (fora do Desktop). cap_gap: px entre a borda da faixa e o topo do boné (negativo = a
        faixa 'come um pouquinho' do boné, como ele pediu)."""
        self.src, self.pasta, self.cache = _abs(src), _abs(pasta), _abs(cache)
        os.makedirs(self.cache, exist_ok=True)
        self.transcricao = os.path.join(self.pasta, transcricao)
        self.audio16k = os.path.join(self.cache, "audio16k.wav")
        if not os.path.exists(self.audio16k):
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", self.src, "-vn", "-ac", "1", "-ar", "16000",
                            "-c:a", "pcm_s16le", self.audio16k], check=True)
        self.edl = os.path.join(self.pasta, "edl.json")
        self.cap_gap = cap_gap
        if grade:                                  # grade de cor do projeto (padrão em compor.GRADE)
            compor.GRADE = grade
        self.maxrate = maxrate                     # teto de bitrate da entrega (ex.: "20M"); folhagem em movimento estoura o crf
        self.clips, self.duracao, self.montado = [], 0.0, None
        os.chdir(self.cache)                       # arquivos temporários (detecção de rosto etc.) ficam no cache
        corte.carregar(self.transcricao, self.audio16k)

    # ---------------- corte e linha do tempo ----------------
    def cortar(self, plano):
        """PLANO -> clipes (edl.json no _projeto). Imprime a linha do tempo."""
        clips = corte.build(plano)
        t = 0.0
        for c in clips:
            c["t0"] = t
            t += c["out"] - c["in"]
            c["t1"] = t
        self.clips, self.duracao = clips, t
        corte.save(clips, self.edl, self.src)
        return clips

    def of(self, p):
        r = [c for c in self.clips if c["label"] == p or c["label"].startswith(p + ".")]
        if not r:
            raise KeyError(f"nenhum clipe '{p}' no corte")
        return r

    def start(self, p): return self.of(p)[0]["t0"]
    def end(self, p): return self.of(p)[-1]["t1"]

    def tl(self, s):
        """tempo da fonte -> tempo da edição. As bordas dos clipes são alinhadas ao quadro (1/30 s): use um tempo de
        dentro do clipe (ex.: 253.75 e não 253.73 se o clipe começa em 253.7333)."""
        for c in self.clips:
            if c["in"] <= s < c["out"]:
                return c["t0"] + s - c["in"]
        raise ValueError(f"tempo da fonte {s} não está no corte")

    @staticmethod
    def fq(x):
        return round(x * FPS) / FPS

    # ---------------- faixas do split ----------------
    def _resolver_plano(self, spec, s0, s1):
        """Plano de tela com âncoras na fala -> plano com offsets numéricos (o que o tela.py entende)."""
        spec = dict(spec)
        n = round(s1 * FPS) - round(s0 * FPS)
        dur = n / FPS
        keys = []
        for a, cx, cy, w in spec["keys"]:
            off = 0.0 if a == "S" else dur if a == "E" else self.tl(a) - self.fq(s0)
            keys.append((min(max(off, 0.0), dur), cx, cy, w))
        spec["keys"] = keys
        if spec.get("sync"):                           # (tempo na gravação, tempo da fala) que devem coincidir
            scr, src = spec.pop("sync")
            spec["t"] = scr - (self.tl(src) - self.fq(s0))
        return spec, n

    def _segmento(self, s0, s1, conteudo, planos, full=False):
        n = round(s1 * FPS) - round(s0 * FPS)
        if isinstance(conteudo, str) and not full:     # nome de um plano de gravação de tela
            spec, n = self._resolver_plano(planos[conteudo], s0, s1)
            p = os.path.join(self.cache, f"tela_{_h(spec, n)}.mov")
            if not os.path.exists(p):
                tela.render(spec, n, p)
        elif isinstance(conteudo, str):                # um arquivo já renderizado (sobreposição de tela cheia)
            p = conteudo
        elif callable(conteudo):                       # renderizador próprio: conteudo(n, saida)
            p = os.path.join(self.cache, f"proprio_{_h(getattr(conteudo, '__name__', ''), s0, s1, full)}.mov")
            conteudo(n, p)
        elif conteudo[0] == "montagem":                # ("montagem", picks, primeiro)
            _, picks, first = conteudo
            p = os.path.join(self.cache, f"mont_{_h(picks, first, n, full)}.mov")
            if not os.path.exists(p):
                montagem.build(n, p, picks, work=p[:-4] + "_partes", first=first, full=full)
        elif conteudo[0] == "video":                   # ("video", arquivo, a partir de (s)[, velocidade])
            _, path, off, *rest = conteudo
            speed = rest[0] if rest else 1.0
            p = os.path.join(self.cache, f"video_{_h(path, os.path.getmtime(path), off, speed, n, full)}.mov")
            if not os.path.exists(p):
                mode = rest[1:] if len(rest) > 1 else ()          # ("video", arquivo, de, vel, "fit"): inteiro sobre desfoque
                vf = montagem.vf_full(path) if full else (montagem.vf(mode) if mode else
                     f"fps={FPS},scale={montagem.BW}:{montagem.BH}:force_original_aspect_ratio=increase:flags=lanczos,"
                     f"crop={montagem.BW}:{montagem.BH},setsar=1,format=yuv420p")    # preenche a faixa 4:3 sem distorcer
                subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{off:.3f}", "-i", path, "-an",
                                "-vf", f"setpts=PTS/{speed:.5f}," + vf + ",tpad=stop_mode=clone:stop=6",
                                "-frames:v", str(n), "-c:v", "libx264", "-preset", "fast", "-crf", "12", p], check=True)
        else:
            raise ValueError(f"conteúdo desconhecido: {conteudo!r}")
        return p, n

    def _montar(self):
        """Clipes do corte (rosto sempre no enquadramento original) concatenados. Cache pelo próprio corte."""
        key = _h([(c["in"], c["out"], c["zoom"]) for c in self.clips], self.src)
        work = os.path.join(self.cache, f"clipes_{key}")
        montado = os.path.join(work, "assembled.mov")
        if not os.path.exists(montado):
            compor.render_clips(json.load(open(self.edl)), work)
        self.montado = montado
        return montado

    # ---------------- vídeo ----------------
    def video(self, saida, faixas=(), telas_cheias=(), planos=None, sobreposicoes=None):
        """faixas: [(início, [(fim do segmento, conteúdo), ...], entra deslizando, sai deslizando)]
        telas_cheias: [(início, fim, conteúdo[, por_cima_da_grade])]
        sobreposicoes(E) -> [(início, fim, arquivo[, por_cima_da_grade])], chamada depois do corte montado
        (para quem precisa da posição do rosto)."""
        runs = []
        for ri, (r0, segs, ain, aout) in enumerate(faixas):
            parts, s0 = [], r0
            for s1, conteudo in segs:
                p, n = self._segmento(s0, s1, conteudo, planos or {})
                print(f"faixa {ri}: {str(conteudo)[:40]:<40} {self.fq(s0):6.2f} -> {self.fq(s1):6.2f} ({n} quadros)", flush=True)
                parts.append(p)
                s0 = s1
            lst = os.path.join(self.cache, f"faixa{ri}.txt")
            with open(lst, "w") as fh:
                fh.writelines(f"file '{p}'\n" for p in parts)
            band = os.path.join(self.cache, f"faixa{ri}.mov")
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", band], check=True)
            runs.append([self.fq(r0), self.fq(segs[-1][0]), band, ain, aout])
        fulls = []
        for a, b, conteudo, *pos in telas_cheias:
            p, n = self._segmento(a, b, conteudo, planos or {}, full=True)
            print(f"tela cheia: {str(conteudo)[:40]:<40} {self.fq(a):6.2f} -> {self.fq(b):6.2f} ({n} quadros)", flush=True)
            fulls.append((self.fq(a), self.fq(b), p, *pos))
        montado = self._montar()
        for r in runs:                                  # empurra o rosto para baixo da faixa, clipe a clipe
            pushes = []
            for c in self.clips:
                a, b = max(c["t0"], r[0]), min(c["t1"], r[1])
                if b - a < 0.02:
                    continue
                y, fh = compor.face_y(montado, c["t0"], c["t1"]) or (compor.FACE_Y * compor.H, 480.0)
                # topo do boné ~0.95 alturas de rosto acima do centro: fica cap_gap px abaixo da faixa no ponto mais alto
                push = int(min(max(BH + self.cap_gap + 0.95 * fh - y, 0), 800))
                pushes.append((self.fq(a), self.fq(b), push))
                print(f"  rosto {c['label']:<12} y={y:6.1f} h={fh:5.1f} desce={push}")
            r.append(pushes)
        if sobreposicoes:
            fulls += sobreposicoes(self)
        compor.finalize(montado, saida, runs=[tuple(r) for r in runs], band_h=BH, fulls=fulls, maxrate=self.maxrate)
        json.dump({"runs": runs, "fulls": fulls}, open(os.path.join(self.cache, "ultimo_render.json"), "w"), indent=1)
        print("vídeo ->", saida)

    # ---------------- sobreposições prontas ----------------
    def rosto(self, a, b):
        """[(cx, cy, altura do rosto)] em 3 pontos do trecho [a, b] da edição."""
        return compor.vision_faces(self._montar(), [a + 0.2, (a + b) / 2, b - 0.2], "sobre")

    def pasta_mac(self, a, b, rotulo, size=330):
        """Pasta do Finder com nome, aparecendo sobre a cabeça entre a e b (tempos da edição)."""
        import pasta_mac
        a, b = self.fq(a), self.fq(b)
        pts = self.rosto(a, b)
        cx = sum(p[0] for p in pts) / len(pts)
        cy = min(p[1] for p in pts)
        fh = sum(p[2] for p in pts) / len(pts)
        y = max(cy - 0.95 * fh - 150, 170)
        p = os.path.join(self.cache, f"pasta_{_h(rotulo, a, b, size, round(cx), round(y))}.mov")
        pasta_mac.render(round(b * FPS) - round(a * FPS), p, cx, y, size=size, rotulo=rotulo)
        print(f"pasta '{rotulo}' em ({cx:.0f},{y:.0f}) {a:.2f}->{b:.2f}")
        return (a, b, p)

    def sobre_cabeca(self, a, b, video, largura=640, velocidade=1.0, acima=320):
        """Vídeo sobre fundo preto (personagens, logo animado) aparecendo sobre a cabeça, sem fundo, entre a e b."""
        import sobre_cabeca
        a, b = self.fq(a), self.fq(b)
        pts = self.rosto(a, b)
        cx = sum(p[0] for p in pts) / len(pts)
        cy = min(p[1] for p in pts)
        fh = sum(p[2] for p in pts) / len(pts)
        y = max(cy - 0.95 * fh - acima, 280)              # nunca em cima do rosto; acima = do topo do boné ao centro
        p = os.path.join(self.cache, f"cabeca_{_h(video, a, b, largura, velocidade, round(cx), round(y))}.mov")
        if not os.path.exists(p):
            sobre_cabeca.render(round(b * FPS) - round(a * FPS), p, video, cx, y, largura, velocidade)
        print(f"sobre a cabeça '{os.path.basename(video)}' em ({cx:.0f},{y:.0f}) {a:.2f}->{b:.2f}")
        return (a, b, p, True)

    def lettering(self, a, b, linhas, **kw):
        import lettering
        a, b = self.fq(a), self.fq(b)
        p = os.path.join(self.cache, f"lettering_{_h(linhas, a, b, kw)}.mov")
        lettering.render(p, b - a, linhas, **kw)
        print(f"lettering {a:.2f}->{b:.2f}")
        return (a, b, p)

    def grade_storyboard(self, a, b, quadros, **kw):
        import grade_storyboard
        a, b = self.fq(a), self.fq(b)
        p = os.path.join(self.cache, f"storyboard_{_h(quadros, a, b, kw)}.mp4")
        grade_storyboard.render(round(b * FPS) - round(a * FPS), p, quadros, **kw)
        print(f"storyboard {a:.2f}->{b:.2f}")
        return (a, b, p, True)                         # por cima da grade de cor: o fundo dos quadros fica limpo

    def legendas(self, correcoes=None, prompt="", trocas=None, **estilo):
        """Legenda simples do vídeo inteiro (scripts/legenda.py). O texto fica em _projeto/legendas.json: edite ali para
        corrigir palavras; enquanto o corte não mudar, o arquivo editado é respeitado. Se o corte mudar, a legenda é
        refeita (a versão anterior fica em legendas_antigas.json para copiar as correções)."""
        import legenda
        corte_id = _h([(c["in"], c["out"]) for c in self.clips])
        arq = os.path.join(self.pasta, "legendas.json")
        bls = None
        if os.path.exists(arq):
            dado = json.load(open(arq))
            if dado.get("corte") == corte_id:
                bls = dado["blocos"]
            else:
                shutil.copy(arq, os.path.join(self.pasta, "legendas_antigas.json"))
        if bls is None:
            wav = os.path.join(self.cache, f"corte16k_{corte_id}.wav")
            if not os.path.exists(wav):
                subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", self._montar(), "-vn", "-ac", "1", "-ar", "16000",
                                "-c:a", "pcm_s16le", wav], check=True)
            pal = os.path.join(self.cache, f"palavras_{corte_id}_{_h(prompt)}.json")   # a transcrição do corte fica guardada
            if not os.path.exists(pal):
                json.dump(legenda.transcrever_corte(wav, prompt), open(pal, "w"), ensure_ascii=False)
            bls = legenda.blocos(json.load(open(pal)), correcoes, trocas)
            json.dump({"corte": corte_id, "blocos": bls}, open(arq, "w"), ensure_ascii=False, indent=1)
            print(f"legendas.json: {len(bls)} blocos (revise o texto)")
        p = os.path.join(self.cache, f"legenda_{_h(bls, estilo, self.duracao)}.mov")
        if not os.path.exists(p):
            legenda.render(p, self.duracao, bls, **estilo)
        return (0.0, self.fq(self.duracao), p, True)    # por cima da grade de cor

    def checar(self, prompt="", rapido=False):
        """Checagem tripla da fala (scripts/checar_fala.py) do corte atual -> _projeto/checagem_fala.md + pranchas."""
        cmd = [sys.executable, os.path.join(SCRIPTS, "checar_fala.py"), self.edl, self.transcricao, self.audio16k,
               "--aceitos", os.path.join(self.pasta, "checagem_aceitos.json"),
               "--saida", os.path.join(self.pasta, "checagem_fala.md")]
        if prompt:
            cmd += ["--prompt", prompt]
        if rapido:
            cmd += ["--so-bordas"]
        subprocess.run(cmd, check=True)

    # ---------------- voz e som ----------------
    def voz_bruta(self, saida, para_isolar=True):
        """Voz bruta do corte atual. para_isolar: guarda também o corte correspondente (edl_isolada.json), que o
        voz.py usa depois para remontar a voz isolada em cortes novos."""
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", self._montar(), "-vn", "-ac", "1", "-ar", "48000",
                        "-c:a", "pcm_s16le", saida], check=True)
        if para_isolar:
            shutil.copy(self.edl, os.path.join(self.pasta, "edl_isolada.json"))
        print("voz bruta ->", saida, "| corte dela -> edl_isolada.json" if para_isolar else "")

    def voz(self, saida, isolada, bruta=None, edl_isolada=None):
        """Voz limpa do corte atual a partir da voz isolada de um corte anterior (voz.py)."""
        cmd = [sys.executable, os.path.join(SCRIPTS, "voz.py"), "--src", self.src,
               "--edl-antiga", edl_isolada or os.path.join(self.pasta, "edl_isolada.json"),
               "--isolada", isolada, "--edl-nova", self.edl, "--saida", saida]
        if bruta:
            cmd += ["--bruta", bruta]
        subprocess.run(cmd, check=True)

    def som(self, video, voz, saida, eventos, lib, stems=None):
        """stems: pasta onde salvar a voz e os efeitos separados (npy), para medir um trecho."""
        _som.mixar(video, voz, saida, eventos, lib, self.duracao, stems=stems)
