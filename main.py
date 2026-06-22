import json
import os
from datetime import datetime
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp
from kivy.core.window import Window

Window.clearcolor = (0.043, 0.071, 0.125, 1)

DATA_FILE = "gestao_estoque.json"
OPERADORES = ["Iveraldo Silva", "Leandro Ferreira", "Leandro Barboza", "Wagner Pereira", "Carlos Silva"]
CATEGORIAS = ["Insumos", "Matéria-prima", "Produto Acabado"]
SUBCATS = ["Master", "Resina", "Moído", "PCR"]

def get_subcat(nome):
    n = nome.upper()
    if "MASTER" in n: return "Master"
    if "RESINA" in n: return "Resina"
    if "REGRIND" in n: return "Moído"
    if "PCR" in n: return "PCR"
    return "Outros"

ITENS_INICIAIS = {
    "Insumos": [
        {"id": 201, "nome": "CAIXA 500ml / 1L - VIBRA", "qty": 0},
        {"id": 202, "nome": "PALLET 500ml / 1L - VIBRA", "qty": 0},
        {"id": 203, "nome": "MOLDURA 20L - VIBRA", "qty": 0},
        {"id": 204, "nome": "PALLET 20L - VIBRA", "qty": 0},
        {"id": 205, "nome": "TABULEIRO - 20L VIBRA", "qty": 0},
        {"id": 206, "nome": "CHAPATEX 110x140 1L - ICONIC", "qty": 0},
        {"id": 207, "nome": "PALLET 1L - ICONIC", "qty": 0},
        {"id": 208, "nome": "MOLDURA 1L - ICONIC", "qty": 0},
        {"id": 209, "nome": "CANTONEIRAS 1L - ICONIC", "qty": 0},
        {"id": 210, "nome": "FITA VERDE (ROLO)", "qty": 0},
        {"id": 211, "nome": "FILME (ROLO GRANDE)", "qty": 0},
        {"id": 212, "nome": "FIVELA PLASTICA", "qty": 0},
        {"id": 213, "nome": "FITA DUREX", "qty": 0},
        {"id": 214, "nome": "FITA BRANCA", "qty": 0},
        {"id": 215, "nome": "CAIXA 4L - VIBRA", "qty": 0},
        {"id": 216, "nome": "TAMPA 4L - VIBRA", "qty": 0},
    ],
    "Matéria-prima": [
        {"id": 101, "nome": "CO MB MASTER AVIENT AMARELO PL13601465", "lotes": []},
        {"id": 102, "nome": "CO MB MASTER AVIENT AZ. IPIR. PL54601666", "lotes": []},
        {"id": 103, "nome": "CO MB MASTER AVIENT GRAFITE PES4601044-Z", "lotes": []},
        {"id": 104, "nome": "CO MB MASTER AVIENT LARANJA CLARO PL23601450-Z", "lotes": []},
        {"id": 105, "nome": "CO MB MASTER AVIENT LARANJA T PL23601343", "lotes": []},
        {"id": 106, "nome": "CO MB MASTER AVIENT PRATA PLS3601117", "lotes": []},
        {"id": 107, "nome": "CO MB MASTER AVIENT VERDE CLARO PE63601193-ZA", "lotes": []},
        {"id": 108, "nome": "CO MB MASTER AVIENT VERDE ESCURO PE64601192-ZT", "lotes": []},
        {"id": 109, "nome": "CO MB MASTER AVIENT VERDE PL63601609", "lotes": []},
        {"id": 110, "nome": "CO MB MASTER CROMEX PRATA PE-AG 22758", "lotes": []},
        {"id": 111, "nome": "CO MB MASTER CROMEX PRATA PE-AG 625", "lotes": []},
        {"id": 112, "nome": "CO MB MASTER ENGEFLEX BRANCO 9062A", "lotes": []},
        {"id": 113, "nome": "CO MB MASTER ENGEFLEX DOURADO 7148E", "lotes": []},
        {"id": 114, "nome": "CO MB MASTER ENGEFLEX LARANJA T LJ12262A", "lotes": []},
        {"id": 115, "nome": "CO MB MASTER ENGEFLEX PLATINA 9288A", "lotes": []},
        {"id": 116, "nome": "CO MB MASTER ENGEFLEX PRETO PR 3795", "lotes": []},
        {"id": 117, "nome": "CO MB MASTER ENGEFLEX VERDE VD 10058B", "lotes": []},
        {"id": 118, "nome": "CO MB MASTER AVIENT AZUL NAUTICO PL53602", "lotes": []},
        {"id": 119, "nome": "RE PCR PEAD CLEAN BOTTLE PRETO PR0001", "lotes": []},
        {"id": 120, "nome": "RE PCR PEAD WISE BRANCO 3001.S", "lotes": []},
        {"id": 121, "nome": "RE PCR PEAD WISE NATURAL 4000.S", "lotes": []},
        {"id": 122, "nome": "RE PCR PEAD WISE PRETO 1002.S", "lotes": []},
        {"id": 123, "nome": "RE REGRIND BORRA PEAD", "lotes": []},
        {"id": 124, "nome": "RE REGRIND VARREDURA", "lotes": []},
        {"id": 125, "nome": "RE REGRIND ICONIC AZUL", "lotes": []},
        {"id": 126, "nome": "RE REGRIND ICONIC DOURADO 7148E", "lotes": []},
        {"id": 127, "nome": "RE REGRIND ICONIC PLATINA 9288A", "lotes": []},
        {"id": 128, "nome": "RE REGRIND ICONIC PRATA PE-AG 625", "lotes": []},
        {"id": 129, "nome": "RE REGRIND ICONIC PRETO PR 3795", "lotes": []},
        {"id": 130, "nome": "RE REGRIND VIBRA AMARELO PL13601465", "lotes": []},
        {"id": 131, "nome": "RE REGRIND VIBRA AMARELO PCR PL13601465", "lotes": []},
        {"id": 132, "nome": "RE REGRIND VIBRA LARAN. T PCR PL23601343", "lotes": []},
        {"id": 133, "nome": "RE REGRIND VIBRA LARANJA T PL23601343", "lotes": []},
        {"id": 134, "nome": "RE REGRIND VIBRA PRATA PCR PE-AG 22758", "lotes": []},
        {"id": 135, "nome": "RE REGRIND VIBRA PRATA PL3601117", "lotes": []},
        {"id": 136, "nome": "RE REGRIND VIBRA VERDE PL63601609", "lotes": []},
        {"id": 137, "nome": "RE REGRIND VIBRA VERDE PCR PL63601609", "lotes": []},
        {"id": 138, "nome": "RE REGRIND VIBRA VERDE ESCURO", "lotes": []},
        {"id": 139, "nome": "RE REGRIND VIBRA VERDE CLARO", "lotes": []},
        {"id": 140, "nome": "RE REGRIND VIBRA GRAFITE (PRATA)", "lotes": []},
        {"id": 141, "nome": "RE REGRIND VIBRA LARANJA CLARO", "lotes": []},
        {"id": 142, "nome": "RE RESINA PEAD HS 5502", "lotes": []},
        {"id": 143, "nome": "RESINA HDPE 35060L", "lotes": []},
    ],
    "Produto Acabado": [
        {"id": 5,  "nome": "BT 0,5L VIBRA VERDE ESCURO NS", "lotes": []},
        {"id": 6,  "nome": "BT 0,5L VIBRA VERDE CLARO NS", "lotes": []},
        {"id": 7,  "nome": "BT 0,5L VIBRA LARANJA NS", "lotes": []},
        {"id": 8,  "nome": "BT 0,5L VIBRA GRAFITE NS", "lotes": []},
        {"id": 9,  "nome": "BT 0,5L VIBRA AZUL NAUTICO", "lotes": []},
        {"id": 10, "nome": "BT 4L VIBRA VERDE ESCURO", "lotes": []},
        {"id": 11, "nome": "BT 4L VIBRA VERDE CLARO", "lotes": []},
        {"id": 12, "nome": "BT 4L VIBRA LARANJA", "lotes": []},
        {"id": 13, "nome": "BT 4L VIBRA GRAFITE", "lotes": []},
        {"id": 14, "nome": "BT 20L VIBRA LARANJA PCR NC VEICULO", "lotes": []},
        {"id": 15, "nome": "BT 20L VIBRA VD ESCURO PCR NC VEICULO", "lotes": []},
        {"id": 16, "nome": "BT 20L VIBRA VD CLARO PCR NC VEICULO", "lotes": []},
        {"id": 17, "nome": "BT 20L VIBRA GRAFITE PCR NC VEICULO", "lotes": []},
        {"id": 18, "nome": "BT 20L VIBRA PRATA PCR VEICULO", "lotes": []},
        {"id": 19, "nome": "BT 20L VIBRA VERDE PCR VEICULO", "lotes": []},
        {"id": 20, "nome": "BT 20L VIBRA AMARELO PCR VEICULO", "lotes": []},
        {"id": 21, "nome": "BT 20L VIBRA PRETO PCR VEICULO", "lotes": []},
        {"id": 22, "nome": "BT 20L VIBRA NATURAL PCR VEICULO", "lotes": []},
        {"id": 23, "nome": "BT 20L VIBRA LARANJA T. PCR VEICULO ANTIGO", "lotes": []},
        {"id": 24, "nome": "BT 20L VIBRA GRAFITE PCR NC COEX VEICULO", "lotes": []},
        {"id": 25, "nome": "BT 20L VIBRA VD ESCU PCR NC COEX VEICULO", "lotes": []},
        {"id": 26, "nome": "BT 20L VIBRA VD CLAR PCR NC COEX VEICULO", "lotes": []},
        {"id": 27, "nome": "BT 20L VIBRA LARANJA PCR NC COEX VEICULO", "lotes": []},
        {"id": 28, "nome": "BT 20L VIBRA PRATA PCR COEX VEICULO", "lotes": []},
        {"id": 29, "nome": "BT 20L VIBRA VERDE PCR COEX VEICULO", "lotes": []},
        {"id": 30, "nome": "BT 20L VIBRA LARANJA PCR COEX VEICULO ANTIGO", "lotes": []},
        {"id": 31, "nome": "BT 20L VIBRA PRETO PCR COEX VEICULO", "lotes": []},
        {"id": 32, "nome": "BT 20L VIBRA NATURAL COEX VEICULO", "lotes": []},
        {"id": 33, "nome": "BT 20L VIBRA AMARELO PCR COEX VEICULO", "lotes": []},
        {"id": 34, "nome": "BT 1L VIBRA MONO GRAFITE NEW SHAPE VEICULO", "lotes": []},
        {"id": 35, "nome": "BT 1L VIBRA MONO VERDE ESCURO NEW SHAPE VEICULO", "lotes": []},
        {"id": 36, "nome": "BT 1L VIBRA MONO LARAN NEW SHAPE VEICULO", "lotes": []},
        {"id": 37, "nome": "BT 1L VIBRA MONO VD CLA NEW SHAPE VEICULO", "lotes": []},
        {"id": 38, "nome": "BT 1L ICONIC PRETO 53G 6511801", "lotes": []},
        {"id": 39, "nome": "BT 1L ICONIC AZUL 53G 6511901", "lotes": []},
        {"id": 40, "nome": "BT 1L ICONIC PLATINA 53G 6512401", "lotes": []},
        {"id": 41, "nome": "BT 1L ICONIC DOURADO 53G 6512201", "lotes": []},
        {"id": 42, "nome": "BT 1L ICONIC PRATA 53G 6512001", "lotes": []},
    ],
}

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"itens": ITENS_INICIAIS, "historico": [], "contagens": []}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def now():
    return datetime.now().strftime("%d/%m/%Y %H:%M")

def total_item(item, cat):
    if cat == "Insumos":
        return item.get("qty", 0)
    return sum(l.get("qty", 0) for l in item.get("lotes", []))

def make_btn(text, bg, fg=(1,1,1,1), height=56, font_size=15):
    return Button(
        text=text, size_hint_y=None, height=dp(height),
        font_size=dp(font_size), bold=True, color=fg,
        background_normal="", background_color=bg
    )

def make_label(text, size=14, bold=False, color=(0.56,0.63,0.74,1), halign="left"):
    lbl = Label(
        text=text, font_size=dp(size), bold=bold,
        color=color, size_hint_y=None, height=dp(size*2),
        halign=halign, valign="middle"
    )
    lbl.bind(size=lambda *a: setattr(lbl, "text_size", lbl.size))
    return lbl

def make_input(hint="", height=46):
    return TextInput(
        hint_text=hint, multiline=False,
        size_hint_y=None, height=dp(height),
        background_color=(0.043,0.071,0.125,1),
        foreground_color=(0.93,0.95,0.97,1),
        hint_text_color=(0.56,0.63,0.74,1),
        cursor_color=(0.15,0.39,0.92,1),
        font_size=dp(14), padding=[dp(12), dp(10)]
    )

class SpinnerOpt(Button):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.background_normal = ""
        self.background_color = (0.063, 0.106, 0.188, 1)
        self.color = (0.93, 0.95, 0.97, 1)
        self.font_size = dp(13)
        self.height = dp(44)

def make_spinner(values, text="Selecione..."):
    return Spinner(
        text=text, values=values,
        size_hint_y=None, height=dp(48),
        background_normal="", background_color=(0.063,0.106,0.188,1),
        color=(0.93,0.95,0.97,1), font_size=dp(13),
        option_cls=SpinnerOpt
    )

class CardBox(BoxLayout):
    def __init__(self, **kw):
        super().__init__(orientation="vertical", padding=dp(16), spacing=dp(8), **kw)
        with self.canvas.before:
            Color(0.063, 0.106, 0.188, 1)
            self.rect = RoundedRectangle(radius=[dp(10)], pos=self.pos, size=self.size)
        self.bind(pos=self._upd, size=self._upd)

    def _upd(self, *a):
        self.rect.pos = self.pos
        self.rect.size = self.size

def make_header(title, on_back=None):
    hdr = BoxLayout(size_hint_y=None, height=dp(64), padding=dp(16), spacing=dp(8))
    with hdr.canvas.before:
        Color(0.15, 0.39, 0.92, 1)
        r = RoundedRectangle(pos=hdr.pos, size=hdr.size)
    hdr.bind(pos=lambda *a: setattr(r, "pos", hdr.pos), size=lambda *a: setattr(r, "size", hdr.size))
    if on_back:
        btn = make_btn("< Voltar", (1,1,1,0.2), height=38, font_size=12)
        btn.bind(on_press=on_back)
        hdr.add_widget(btn)
    hdr.add_widget(make_label(title, size=17, bold=True, color=(1,1,1,1)))
    return hdr

class HomeScreen(Screen):
    def __init__(self, app, **kw):
        super().__init__(name="home", **kw)
        self.app = app
        self.build()

    def build(self):
        root = BoxLayout(orientation="vertical")
        hdr = BoxLayout(size_hint_y=None, height=dp(70), padding=dp(16), spacing=dp(8))
        with hdr.canvas.before:
            Color(0.15, 0.39, 0.92, 1)
            self.hdr_rect = RoundedRectangle(pos=hdr.pos, size=hdr.size)
        hdr.bind(pos=lambda *a: setattr(self.hdr_rect, "pos", hdr.pos),
                 size=lambda *a: setattr(self.hdr_rect, "size", hdr.size))
        hdr.add_widget(make_label("Gestão de Estoque", size=19, bold=True, color=(1,1,1,1)))
        btn_gestora = make_btn("Gestora", (1,1,1,0.2), height=36, font_size=12)
        btn_gestora.bind(on_press=lambda *a: setattr(self.app.sm, "current", "gestora"))
        hdr.add_widget(btn_gestora)
        root.add_widget(hdr)

        sv = ScrollView()
        body = BoxLayout(orientation="vertical", padding=dp(16), spacing=dp(12), size_hint_y=None)
        body.bind(minimum_height=body.setter("height"))

        card = CardBox(size_hint_y=None, height=dp(110))
        card.add_widget(make_label("QUEM ESTÁ OPERANDO?", size=11, bold=True))
        self.sp_op = make_spinner(OPERADORES)
        card.add_widget(self.sp_op)
        body.add_widget(card)

        btn_e = make_btn("Entrada de Item", (0.15,0.39,0.92,1), height=62, font_size=16)
        btn_e.bind(on_press=lambda *a: self.go("entrada"))
        body.add_widget(btn_e)

        btn_s = make_btn("Saída de Item", (0.86,0.15,0.15,1), height=62, font_size=16)
        btn_s.bind(on_press=lambda *a: self.go("saida"))
        body.add_widget(btn_s)

        btn_c = make_btn("Contagem de Estoque", (0.2,0.25,0.33,1), height=62, font_size=16)
        btn_c.bind(on_press=lambda *a: self.go("contagem"))
        body.add_widget(btn_c)

        sv.add_widget(body)
        root.add_widget(sv)
        self.add_widget(root)

    def go(self, tela):
        op = self.sp_op.text
        if op == "Selecione...":
            self.show_toast("Selecione o operador!")
            return
        self.app.operador = op
        self.app.sm.current = tela

    def show_toast(self, msg):
        Popup(title="", content=Label(text=msg), size_hint=(0.7, 0.2)).open()

class GestoraScreen(Screen):
    def __init__(self, app, **kw):
        super().__init__(name="gestora", **kw)
        self.app = app

    def on_enter(self):
        self.clear_widgets()
        self.build()

    def build(self):
        root = BoxLayout(orientation="vertical")
        hdr = BoxLayout(size_hint_y=None, height=dp(64), padding=dp(16))
        with hdr.canvas.before:
            Color(0.15, 0.39, 0.92, 1)
            r = RoundedRectangle(pos=hdr.pos, size=hdr.size)
        hdr.bind(pos=lambda *a: setattr(r, "pos", hdr.pos), size=lambda *a: setattr(r, "size", hdr.size))
        hdr.add_widget(make_label("Painel da Gestora", size=17, bold=True, color=(1,1,1,1)))
        btn_op = make_btn("Operador", (1,1,1,0.2), height=36, font_size=12)
        btn_op.bind(on_press=lambda *a: setattr(self.app.sm, "current", "home"))
        hdr.add_widget(btn_op)
        root.add_widget(hdr)

        sv = ScrollView()
        body = BoxLayout(orientation="vertical", padding=dp(14), spacing=dp(12), size_hint_y=None)
        body.bind(minimum_height=body.setter("height"))

        data = self.app.data

        grid = GridLayout(cols=3, size_hint_y=None, height=dp(80), spacing=dp(8))
        for cat in CATEGORIAS:
            t = sum(total_item(i, cat) for i in data["itens"].get(cat, []))
            c = CardBox(size_hint_y=None, height=dp(76))
            c.add_widget(make_label(str(t), size=20, bold=True, color=(0.36,0.6,0.98,1), halign="center"))
            c.add_widget(make_label(cat, size=10, halign="center"))
            grid.add_widget(c)
        body.add_widget(grid)

        self.sp_cat = make_spinner(CATEGORIAS, CATEGORIAS[0])
        self.sp_cat.bind(text=lambda *a: self.refresh_estoque())
        body.add_widget(self.sp_cat)

        self.sp_sub = make_spinner(["Todos"] + SUBCATS, "Todos")
        self.sp_sub.bind(text=lambda *a: self.refresh_estoque())
        body.add_widget(self.sp_sub)

        self.estoque_card = CardBox(size_hint_y=None, height=dp(400))
        self.estoque_card.add_widget(make_label("Estoque Atual", size=15, bold=True, color=(0.93,0.95,0.97,1)))
        self.est_box = BoxLayout(orientation="vertical", spacing=dp(4), size_hint_y=None)
        self.est_box.bind(minimum_height=self.est_box.setter("height"))
        sv2 = ScrollView(size_hint_y=None, height=dp(340))
        sv2.add_widget(self.est_box)
        self.estoque_card.add_widget(sv2)
        body.add_widget(self.estoque_card)
        self.refresh_estoque()

        hist_card = CardBox(size_hint_y=None)
        hist_card.add_widget(make_label("Histórico", size=15, bold=True, color=(0.93,0.95,0.97,1)))
        for h in data["historico"][:15]:
            cor = (0.13,0.7,0.4,1) if h["tipo"] == "Entrada" else (0.86,0.2,0.2,1)
            hist_card.add_widget(make_label(f"{h['tipo']} — {h['nome']}", size=12, color=cor))
            hist_card.add_widget(make_label(
                f"{h['op']}  {h['dataHora']}  Lote: {h['lote']}  {'+' if h['tipo']=='Entrada' else '-'}{h['qty']}",
                size=11
            ))
        hist_card.height = dp(max(100, len(data["historico"][:15]) * 50 + 40))
        body.add_widget(hist_card)

        cont_card = CardBox(size_hint_y=None)
        cont_card.add_widget(make_label("Contagens", size=15, bold=True, color=(0.93,0.95,0.97,1)))
        for c in data["contagens"][:5]:
            cont_card.add_widget(make_label(f"{c['cat']} — {c['op']}  {c['dataHora']}", size=12, color=(0.85,0.55,0.1,1)))
            for r in c["regs"][:8]:
                cor = (0.13,0.7,0.4,1) if r["div"]==0 else ((0.85,0.55,0.1,1) if r["div"]>0 else (0.86,0.2,0.2,1))
                lote_txt = f" (lote {r['lote']})" if r.get("lote") and r["lote"] != "S/L" else ""
                cont_card.add_widget(make_label(
                    f"  {r['nome']}{lote_txt}: Sis {r['sis']} Con {r['con']} Dif {'+' if r['div']>0 else ''}{r['div']}",
                    size=11, color=cor
                ))
        cont_card.height = dp(max(80, len(data["contagens"][:5]) * 100 + 40))
        body.add_widget(cont_card)

        sv.add_widget(body)
        root.add_widget(sv)
        self.add_widget(root)

    def refresh_estoque(self):
        self.est_box.clear_widgets()
        cat = self.sp_cat.text
        sub = self.sp_sub.text
        items = self.app.data["itens"].get(cat, [])
        if cat == "Matéria-prima" and sub != "Todos":
            items = [i for i in items if get_subcat(i["nome"]) == sub]
        for item in items:
            t = total_item(item, cat)
            self.est_box.add_widget(make_label(f"{item['nome']}  —  {t} un", size=12, color=(0.93,0.95,0.97,1)))

class EntradaScreen(Screen):
    def __init__(self, app, **kw):
        super().__init__(name="entrada", **kw)
        self.app = app

    def on_enter(self):
        self.clear_widgets()
        self.build()

    def build(self):
        root = BoxLayout(orientation="vertical")
        root.add_widget(make_header("Entrada de Item", on_back=lambda *a: setattr(self.app.sm, "current", "home")))

        sv = ScrollView()
        body = BoxLayout(orientation="vertical", padding=dp(14), spacing=dp(10), size_hint_y=None)
        body.bind(minimum_height=body.setter("height"))

        card = CardBox(size_hint_y=None, height=dp(650))

        card.add_widget(make_label("CATEGORIA", size=11, bold=True))
        self.sp_cat = make_spinner(CATEGORIAS)
        self.sp_cat.bind(text=self.on_cat_change)
        card.add_widget(self.sp_cat)

        card.add_widget(make_label("SUBCATEGORIA (Matéria-prima)", size=11, bold=True))
        self.sp_sub = make_spinner(["Todos"] + SUBCATS, "Todos")
        self.sp_sub.bind(text=self.on_sub_change)
        card.add_widget(self.sp_sub)

        card.add_widget(make_label("ITEM", size=11, bold=True))
        self.sp_item = make_spinner([])
        card.add_widget(self.sp_item)

        card.add_widget(make_label("Nº DO LOTE (vazio para Insumos)", size=11, bold=True))
        self.inp_lote = make_input("Ex: L001")
        card.add_widget(self.inp_lote)

        card.add_widget(make_label("QUANTIDADE", size=11, bold=True))
        self.inp_qty = make_input("Ex: 50")
        card.add_widget(self.inp_qty)

        card.add_widget(make_label("DATA DE ENTRADA (DD/MM/AAAA)", size=11, bold=True))
        self.inp_data = make_input("Ex: 15/06/2026")
        card.add_widget(self.inp_data)

        card.add_widget(make_label("FABRICAÇÃO (Matéria-prima)", size=11, bold=True))
        self.inp_fab = make_input("Ex: 01/01/2026")
        card.add_widget(self.inp_fab)

        card.add_widget(make_label("VENCIMENTO (Matéria-prima)", size=11, bold=True))
        self.inp_venc = make_input("Ex: 01/01/2027")
        card.add_widget(self.inp_venc)

        card.add_widget(make_label("Nº DA NF", size=11, bold=True))
        self.inp_nf = make_input("Ex: 123456")
        card.add_widget(self.inp_nf)

        btn = make_btn("Confirmar Entrada", (0.15,0.39,0.92,1), height=52)
        btn.bind(on_press=self.confirmar)
        card.add_widget(btn)

        self.msg = make_label("", size=13, color=(0.13,0.7,0.4,1), halign="center")
        card.add_widget(self.msg)

        body.add_widget(card)
        sv.add_widget(body)
        root.add_widget(sv)
        self.add_widget(root)
        self.on_cat_change(self.sp_cat, self.sp_cat.text)

    def get_items(self):
        cat = self.sp_cat.text
        items = self.app.data["itens"].get(cat, [])
        if cat == "Matéria-prima" and self.sp_sub.text != "Todos":
            items = [i for i in items if get_subcat(i["nome"]) == self.sp_sub.text]
        return items

    def on_cat_change(self, sp, cat):
        self.sp_item.values = [i["nome"] for i in self.get_items()]
        self.sp_item.text = "Selecione..."

    def on_sub_change(self, sp, sub):
        self.sp_item.values = [i["nome"] for i in self.get_items()]
        self.sp_item.text = "Selecione..."

    def confirmar(self, *a):
        cat = self.sp_cat.text
        item_nome = self.sp_item.text
        qty_str = self.inp_qty.text.strip()
        lote = self.inp_lote.text.strip()
        data = self.inp_data.text.strip()
        nf = self.inp_nf.text.strip()

        if cat == "Selecione..." or item_nome == "Selecione...":
            self.msg.text = "Selecione categoria e item!"; self.msg.color=(0.86,0.2,0.2,1); return
        if not qty_str or not data:
            self.msg.text = "Preencha quantidade e data!"; self.msg.color=(0.86,0.2,0.2,1); return

        qty = int(qty_str)
        items = self.app.data["itens"][cat]
        idx = next((i for i,x in enumerate(items) if x["nome"]==item_nome), None)
        if idx is None: return

        if cat == "Insumos":
            items[idx]["qty"] = items[idx].get("qty",0) + qty
            lote_desc = "S/L"
        else:
            novo_lote = {"lote": lote or "S/L", "qty": qty, "data": data,
                         "fabrico": self.inp_fab.text.strip(), "vencimento": self.inp_venc.text.strip()}
            lotes = items[idx].get("lotes", [])
            ei = next((i for i,l in enumerate(lotes) if l["lote"]==novo_lote["lote"]), None)
            if ei is not None:
                lotes[ei]["qty"] += qty
            else:
                lotes.append(novo_lote)
            items[idx]["lotes"] = lotes
            lote_desc = novo_lote["lote"] + "(" + str(qty) + ")"

        self.app.data["historico"].insert(0, {
            "tipo": "Entrada", "cat": cat, "nome": item_nome,
            "lote": lote_desc, "qty": qty, "op": self.app.operador,
            "nf": nf, "dataHora": now()
        })
        save_data(self.app.data)
        self.msg.text = "Entrada registrada!"; self.msg.color=(0.13,0.7,0.4,1)
        self.inp_qty.text=""; self.inp_lote.text=""; self.inp_data.text=""; self.inp_nf.text=""
        self.inp_fab.text=""; self.inp_venc.text=""

class SaidaScreen(Screen):
    def __init__(self, app, **kw):
        super().__init__(name="saida", **kw)
        self.app = app

    def on_enter(self):
        self.clear_widgets()
        self.build()

    def build(self):
        root = BoxLayout(orientation="vertical")
        root.add_widget(make_header("Saída de Item (FIFO)", on_back=lambda *a: setattr(self.app.sm, "current", "home")))

        sv = ScrollView()
        body = BoxLayout(orientation="vertical", padding=dp(14), spacing=dp(10), size_hint_y=None)
        body.bind(minimum_height=body.setter("height"))

        card = CardBox(size_hint_y=None, height=dp(520))

        card.add_widget(make_label("CATEGORIA", size=11, bold=True))
        self.sp_cat = make_spinner(CATEGORIAS)
        self.sp_cat.bind(text=self.on_cat_change)
        card.add_widget(self.sp_cat)

        card.add_widget(make_label("SUBCATEGORIA (Matéria-prima)", size=11, bold=True))
        self.sp_sub = make_spinner(["Todos"] + SUBCATS, "Todos")
        self.sp_sub.bind(text=self.on_sub_change)
        card.add_widget(self.sp_sub)

        card.add_widget(make_label("ITEM", size=11, bold=True))
        self.sp_item = make_spinner([])
        self.sp_item.bind(text=self.on_item_change)
        card.add_widget(self.sp_item)

        self.lbl_lotes = make_label("", size=11, color=(0.56,0.63,0.74,1))
        card.add_widget(self.lbl_lotes)

        card.add_widget(make_label("Nº DO LOTE", size=11, bold=True))
        self.sp_lote = make_spinner([])
        card.add_widget(self.sp_lote)

        card.add_widget(make_label("QUANTIDADE", size=11, bold=True))
        self.inp_qty = make_input("Ex: 10")
        card.add_widget(self.inp_qty)

        card.add_widget(make_label("Nº DA NF", size=11, bold=True))
        self.inp_nf = make_input("Ex: 123456")
        card.add_widget(self.inp_nf)

        btn = make_btn("Confirmar Saída", (0.15,0.39,0.92,1), height=52)
        btn.bind(on_press=self.confirmar)
        card.add_widget(btn)

        self.msg = make_label("", size=13, halign="center")
        card.add_widget(self.msg)

        body.add_widget(card)
        sv.add_widget(body)
        root.add_widget(sv)
        self.add_widget(root)
        self.on_cat_change(self.sp_cat, self.sp_cat.text)

    def get_items(self):
        cat = self.sp_cat.text
        items = self.app.data["itens"].get(cat, [])
        if cat == "Matéria-prima" and self.sp_sub.text != "Todos":
            items = [i for i in items if get_subcat(i["nome"]) == self.sp_sub.text]
        return items

    def on_cat_change(self, sp, cat):
        self.sp_item.values = [i["nome"] for i in self.get_items()]
        self.sp_item.text = "Selecione..."
        self.sp_lote.values = []
        self.lbl_lotes.text = ""

    def on_sub_change(self, sp, sub):
        self.sp_item.values = [i["nome"] for i in self.get_items()]
        self.sp_item.text = "Selecione..."

    def on_item_change(self, sp, nome):
        cat = self.sp_cat.text
        items = self.app.data["itens"].get(cat, [])
        item = next((i for i in items if i["nome"]==nome), None)
        if not item: return
        if cat == "Insumos":
            self.lbl_lotes.text = f"Disponível: {item.get('qty',0)} un"
            self.sp_lote.values = ["S/L"]
            self.sp_lote.text = "S/L"
        else:
            disp = [l for l in item.get("lotes",[]) if l["qty"]>0]
            self.lbl_lotes.text = "Lotes: " + " | ".join([f"{l['lote']}: {l['qty']}un" for l in disp])
            self.sp_lote.values = [l["lote"] for l in disp]
            self.sp_lote.text = disp[0]["lote"] if disp else "Selecione..."

    def confirmar(self, *a):
        cat = self.sp_cat.text
        nome = self.sp_item.text
        lote = self.sp_lote.text
        qty_str = self.inp_qty.text.strip()
        nf = self.inp_nf.text.strip()

        if cat=="Selecione..." or nome=="Selecione...":
            self.msg.text="Selecione categoria e item!"; self.msg.color=(0.86,0.2,0.2,1); return
        if not qty_str:
            self.msg.text="Informe a quantidade!"; self.msg.color=(0.86,0.2,0.2,1); return

        qty = int(qty_str)
        items = self.app.data["itens"][cat]
        idx = next((i for i,x in enumerate(items) if x["nome"]==nome), None)
        if idx is None: return

        if cat == "Insumos":
            if items[idx].get("qty",0) < qty:
                self.msg.text="Quantidade insuficiente!"; self.msg.color=(0.86,0.2,0.2,1); return
            items[idx]["qty"] -= qty
        else:
            lotes = items[idx].get("lotes",[])
            li = next((i for i,l in enumerate(lotes) if l["lote"]==lote), None)
            if li is None:
                self.msg.text="Lote não encontrado!"; self.msg.color=(0.86,0.2,0.2,1); return
            if lotes[li]["qty"] < qty:
                self.msg.text=f"Só {lotes[li]['qty']} disponíveis!"; self.msg.color=(0.86,0.2,0.2,1); return
            lotes[li]["qty"] -= qty
            items[idx]["lotes"] = [l for l in lotes if l["qty"]>0]

        self.app.data["historico"].insert(0, {
            "tipo": "Saída", "cat": cat, "nome": nome,
            "lote": lote, "qty": qty, "op": self.app.operador,
            "nf": nf, "dataHora": now()
        })
        save_data(self.app.data)
        self.msg.text="Saída registrada!"; self.msg.color=(0.13,0.7,0.4,1)
        self.inp_qty.text=""; self.inp_nf.text=""

class ContagemScreen(Screen):
    def __init__(self, app, **kw):
        super().__init__(name="contagem", **kw)
        self.app = app

    def on_enter(self):
        self.clear_widgets()
        self.build()

    def build(self):
        root = BoxLayout(orientation="vertical")
        root.add_widget(make_header("Contagem de Estoque", on_back=lambda *a: setattr(self.app.sm, "current", "home")))

        sv = ScrollView()
        body = BoxLayout(orientation="vertical", padding=dp(14), spacing=dp(10), size_hint_y=None)
        body.bind(minimum_height=body.setter("height"))

        card = CardBox(size_hint_y=None)
        card.add_widget(make_label("CATEGORIA", size=11, bold=True))
        self.sp_cat = make_spinner(CATEGORIAS)
        self.sp_cat.bind(text=self.on_cat_change)
        card.add_widget(self.sp_cat)

        self.sp_sub = make_spinner(["Todos"] + SUBCATS, "Todos")
        self.sp_sub.bind(text=lambda *a: self.on_cat_change(self.sp_cat, self.sp_cat.text))
        card.add_widget(self.sp_sub)

        self.items_box = BoxLayout(orientation="vertical", spacing=dp(6), size_hint_y=None)
        self.items_box.bind(minimum_height=self.items_box.setter("height"))
        card.add_widget(self.items_box)
        self.inputs = {}

        btn = make_btn("Salvar Contagem", (0.15,0.39,0.92,1), height=52)
        btn.bind(on_press=self.salvar)
        card.add_widget(btn)
        self.msg = make_label("", size=13, halign="center")
        card.add_widget(self.msg)
        card.height = dp(650)
        body.add_widget(card)
        sv.add_widget(body)
        root.add_widget(sv)
        self.add_widget(root)
        self.on_cat_change(self.sp_cat, self.sp_cat.text)

    def on_cat_change(self, sp, cat):
        self.items_box.clear_widgets()
        self.inputs = {}
        items = self.app.data["itens"].get(cat, [])
        if cat == "Matéria-prima" and self.sp_sub.text != "Todos":
            items = [i for i in items if get_subcat(i["nome"]) == self.sp_sub.text]
        self.sp_sub.disabled = (cat != "Matéria-prima")

        for item in items:
            t = total_item(item, cat)
            if cat != "Produto Acabado":
                row = BoxLayout(size_hint_y=None, height=dp(72), spacing=dp(8))
                row.add_widget(make_label(item["nome"], size=11, color=(0.93,0.95,0.97,1)))
                inp = make_input(f"Contado (sis: {t})")
                self.inputs[item["nome"]] = {"input": inp, "sis": t, "lote": None}
                row.add_widget(inp)
                self.items_box.add_widget(row)
            else:
                lotes = item.get("lotes", [])
                if not lotes:
                    row = BoxLayout(size_hint_y=None, height=dp(72), spacing=dp(8))
                    row.add_widget(make_label(item["nome"] + " (sem lote)", size=11, color=(0.93,0.95,0.97,1)))
                    inp = make_input("Contado (sis: 0)")
                    self.inputs[item["nome"] + "|S/L"] = {"input": inp, "sis": 0, "nome": item["nome"], "lote": "S/L"}
                    row.add_widget(inp)
                    self.items_box.add_widget(row)
                else:
                    for l in lotes:
                        row = BoxLayout(size_hint_y=None, height=dp(72), spacing=dp(8))
                        row.add_widget(make_label(f"{item['nome']} — Lote {l['lote']}", size=11, color=(0.93,0.95,0.97,1)))
                        inp = make_input(f"Contado (sis: {l['qty']})")
                        key = item["nome"] + "|" + l["lote"]
                        self.inputs[key] = {"input": inp, "sis": l["qty"], "nome": item["nome"], "lote": l["lote"]}
                        row.add_widget(inp)
                        self.items_box.add_widget(row)

    def salvar(self, *a):
        cat = self.sp_cat.text
        if cat == "Selecione...":
            self.msg.text="Selecione a categoria!"; return
        regs = []
        for key, info in self.inputs.items():
            inp = info["input"]
            sis = info["sis"]
            con = int(inp.text) if inp.text.strip() else sis
            nome = info.get("nome", key)
            lote = info.get("lote") or "S/L"
            regs.append({"nome": nome, "lote": lote, "sis": sis, "con": con, "div": con - sis})
        self.app.data["contagens"].insert(0, {
            "cat": cat, "op": self.app.operador, "dataHora": now(), "regs": regs
        })
        save_data(self.app.data)
        self.msg.text="Contagem salva!"; self.msg.color=(0.13,0.7,0.4,1)
        for info in self.inputs.values():
            info["input"].text = ""

class GestaoEstoqueApp(App):
    def build(self):
        self.data = load_data()
        self.operador = ""
        self.sm = ScreenManager()
        self.sm.add_widget(HomeScreen(self))
        self.sm.add_widget(GestoraScreen(self))
        self.sm.add_widget(EntradaScreen(self))
        self.sm.add_widget(SaidaScreen(self))
        self.sm.add_widget(ContagemScreen(self))
        return self.sm

if __name__ == "__main__":
    GestaoEstoqueApp().run()
