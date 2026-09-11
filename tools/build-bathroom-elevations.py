"""Build four orthographic bathroom elevations. All model dimensions are cm.

The independently authored plan.svg is the corresponding plan view.
Fixture mounting levels marked 'условно' are illustrative, not installation data.
"""
from pathlib import Path
from html import escape

OUT = Path(__file__).resolve().parents[1] / 'assets' / 'bathroom-room'
S = 2.4
H = 260
TOP = 165
FLOOR = TOP + H * S


class Drawing:
    def __init__(self, width, title, direction):
        self.width = width
        self.x0 = (1000 - width * S) / 2
        self.items = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="1060" viewBox="0 0 1000 1060" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">{escape(direction)}</desc>
<defs><pattern id="hatch" width="10" height="10" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="10" height="10" fill="#f1ede5"/><path d="M0 0V10" stroke="#dbd2c4"/></pattern></defs>
<style>text{{font-family:'Segoe UI',sans-serif;fill:#29342e}}.small{{font-size:14px}}.dim{{fill:none;stroke:#778178;stroke-width:1}}.dimtext{{font-size:16px;fill:#58635b}}.muted{{fill:#687169}}.blue{{fill:#286b81}}.projection{{fill:none;stroke:#8e9d94;stroke-width:1.5;stroke-dasharray:6 5}}.woodtext{{fill:#fff;font-size:13px}}.metal{{fill:none;stroke:#738277;stroke-width:3}}</style>
<rect width="1000" height="1060" fill="#fff"/>
<text x="45" y="39" font-size="12" letter-spacing="2" class="muted">ВАННАЯ · РАЗВЁРТКА СТЕНЫ</text>
<text x="45" y="77" font-size="27">{escape(title)}</text>
<text x="45" y="106" class="small muted">{escape(direction)}</text>''']
        self.rect(0, 0, width, H, '#faf9f5', '#879389', 1.5)

    def x(self, u): return self.x0 + u * S
    def y(self, z): return TOP + (H - z) * S
    def add(self, s): self.items.append(s)

    def rect(self, u, z, w, h, fill='#fff', stroke='#879389', sw=1.5, cls='', rx=0):
        self.add(f'<rect x="{self.x(u):g}" y="{self.y(z+h):g}" width="{w*S:g}" height="{h*S:g}" rx="{rx:g}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" class="{cls}"/>')

    def line(self, u1, z1, u2, z2, stroke='#879389', sw=1.5, cls=''):
        self.add(f'<path d="M{self.x(u1):g} {self.y(z1):g}L{self.x(u2):g} {self.y(z2):g}" fill="none" stroke="{stroke}" stroke-width="{sw}" class="{cls}"/>')

    def text(self, u, z, value, size=16, cls='', anchor='middle'):
        self.add(f'<text x="{self.x(u):g}" y="{self.y(z):g}" font-size="{size}" class="{cls}" text-anchor="{anchor}">{escape(value)}</text>')

    def circle(self, u, z, r, fill='#fff', stroke='#879389', sw=1.5):
        self.add(f'<circle cx="{self.x(u):g}" cy="{self.y(z):g}" r="{r*S:g}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')

    def hdim(self, a, b, y, label):
        x1,x2=self.x(a),self.x(b)
        self.add(f'<path d="M{x1:g} {y-7:g}V{y+7:g}M{x2:g} {y-7:g}V{y+7:g}M{x1:g} {y:g}H{x2:g}" class="dim"/><text x="{(x1+x2)/2:g}" y="{y-10:g}" class="dimtext" text-anchor="middle">{escape(label)}</text>')

    def vdim(self, a, b, x, label):
        y1,y2=self.y(a),self.y(b)
        cy=(y1+y2)/2
        self.add(f'<path d="M{x-7:g} {y1:g}H{x+7:g}M{x-7:g} {y2:g}H{x+7:g}M{x:g} {y1:g}V{y2:g}" class="dim"/><text x="{x-10:g}" y="{cy:g}" class="dimtext" text-anchor="middle" transform="rotate(-90 {x-10:g} {cy:g})">{escape(label)}</text>')

    def handle(self, u, z, w=10):
        self.line(u-w/2,z,u+w/2,z,'#cbd0c8',3)

    def finish(self, filename, notes, overall_width=True):
        self.vdim(0,H,self.x0-66,'260 от чистого пола')
        if overall_width:
            self.hdim(0,self.width,838,f'{self.width:g} — ширина этой стены')
        self.add('<path d="M45 878H955" stroke="#d8dcd5"/>')
        for i,note in enumerate(notes):
            self.add(f'<text x="45" y="{909+i*27}" font-size="14" class="muted">{escape(note)}</text>')
        self.add('<text x="45" y="1040" font-size="12" class="muted">Сантехника обозначена условно. Размеры в см; монтажные уровни оборудования уточняются по изделиям.</text></svg>')
        (OUT/filename).write_text('\n'.join(self.items),encoding='utf-8')


def vanity():
    d=Drawing(200,'Стена с тумбой','Смотрим от душевой к тумбе. Короб справа; слева — сторона входной двери.')
    d.rect(175,0,25,260,'url(#hatch)')
    x=d.x(187.5); y=d.y(156)
    d.add(f'<text x="{x:g}" y="{y:g}" font-size="15" text-anchor="middle" transform="rotate(-90 {x:g} {y:g})">БОКОВАЯ СТЕНКА КОРОБА · 25</text>')
    d.rect(2,0,171,10,'#574635','#574635')
    for i in range(4):
        d.rect(2+i*42.75,10,42.75,40.8,'#8a674b','#614d3d',1)
        d.handle(2+(i+.5)*42.75,41)
    for left in [2,121.7]:
        for z,label in [(50.8,'17,1'),(67.9,'17,1')]:
            d.rect(left,z,51.3,17.1,'#8a674b','#614d3d',1)
            d.handle(left+25.65,z+12)
            d.text(left+25.65,z+3,label,13,'woodtext')
    d.rect(53.3,50.8,68.4,34.2,'#8a674b','#614d3d',1)
    d.handle(87.5,79)
    d.text(87.5,63,'Ящик под чашей',13,'woodtext')
    d.rect(0,85,175,2,'#e8e8df')
    for x in [8,50]:
        d.rect(x,2,34,6,'#364239','#364239',1)
        for z in [3.5,5,6.5]: d.line(x+1,z,x+33,z,'#a7aa94',.8)
    # Bowl and tap shown schematically at the worktop.
    d.rect(57.5,69,60,16,'none','#a9b3a9',1,'projection',6)
    d.line(87.5,87,87.5,104,'#738277',4)
    d.line(87.5,103,82,103,'#738277',3)
    d.circle(87.5,165,50,'#edf1ed','#78887b',2)
    d.text(87.5,166,'Зеркало Ø100',19)
    d.text(87.5,155,'Центр 165',14,'muted')
    for x in [18.75,156.25]:
        d.circle(x,165,7.5,'#fbf5e5','#434c44',2)
        d.text(x,149,'Бра Ø15',13)
    d.hdim(0,175,143,'175 между стенами')
    d.hdim(175,200,143,'25')
    d.hdim(37.5,137.5,d.y(228),'100')
    d.vdim(0,87,d.x(200)+38,'87 столешница')
    d.vdim(0,165,d.x0-27,'165 ось зеркала и бра')
    d.finish('wall-vanity.svg',[
        'Тумба 175 × 60 × 87; светлая столешница 2; фасады — тёмный орех. Корпус 171 + доборы по 2.',
        'Пять верхних ящиков и четыре нижние дверцы. Цоколь 10, углубление для ног 9; слева две решётки.',
        'Зеркало: низ 115, верх 215. Оси бра: 18,75 и 156,25 от левой стены, высота 165.',
        'Вытяжка находится на боковой стенке короба — она показана на соседней развёртке.',
    ])


def boxing():
    d=Drawing(258,'Стена с коробом и душевой колонной','Смотрим от двери на противоположную стену. Тумба слева, душевая справа.')
    d.rect(0,0,164,260,'url(#hatch)')
    d.rect(164,0,94,260,'#eef3ef')
    # Vanity in side elevation.
    d.rect(0,10,59,75,'#8a674b','#614d3d')
    d.rect(0,0,50,10,'#574635','#574635')
    d.rect(0,85,60,2,'#e8e8df')
    d.text(30,50,'Тумба',16,'woodtext')
    d.text(30,38,'глубина 60',13,'woodtext')
    # Fan on the boxing face near the vanity, no ceiling fixture.
    d.circle(32,235,8,'#fff','#738277')
    d.text(32,219,'PAX Norte',15)
    d.text(32,209,'ось ≈ 235*',13,'muted')
    # Niche 70 wide above installation, no protruding wall volume.
    for u in [82,117]:
        d.rect(u,130,35,120,'#8a674b','#614d3d')
    d.line(113.5,140,113.5,150,'#cbd0c8',3)
    d.line(120.5,140,120.5,150,'#cbd0c8',3)
    d.text(117,204,'Шкаф 70 × 120',15,'woodtext')
    d.text(117,192,'внутри короба',13,'woodtext')
    d.text(117,180,'фасад заподлицо',13,'woodtext')
    d.hdim(82,152,d.y(256),'70')
    d.vdim(130,250,d.x(76),'120 · ниша*')
    d.rect(104.5,98,25,16,'#fff')
    d.circle(112,106,4,'none'); d.circle(122,106,3,'none')
    # WC front symbol: illustrative mounting height, not a product drawing.
    d.rect(97.5,18,39,25,'#fff','#879389',1.5,rx=20)
    d.rect(97.5,41,39,3,'#f2f4ef','#879389',1,rx=5)
    d.text(117,59,'Roca Ona',15)
    # Shower column mounted on this wall; levels illustrative.
    d.line(211,110,211,222,'#738277',3)
    d.line(196,110,226,110,'#738277',5)
    d.line(211,222,224,222,'#738277',3)
    d.add(f'<ellipse cx="{d.x(224):g}" cy="{d.y(219):g}" rx="{15.5*S:g}" ry="4" fill="#b8c2b7" stroke="#738277"/>')
    d.line(211,160,223,173,'#738277',3)
    d.circle(225,176,4,'#b8c2b7','#738277')
    d.add(f'<path d="M{d.x(211):g} {d.y(158):g} Q{d.x(239):g} {d.y(35):g} {d.x(221):g} {d.y(110):g}" class="metal"/>')
    d.text(214,243,'Колонна душа',15)
    d.line(164,0,164,200,'#4388a1',4)
    d.rect(166,0,90,1,'#839687','#52695b',1)
    d.text(213,12,'Трап 90 вдоль стены',14)
    d.hdim(0,164,143,'164 · прямой короб')
    d.hdim(164,258,143,'94 · душевая')
    d.vdim(0,200,d.x(258)+32,'200 · стекло с ребра')
    d.finish('wall-boxing.svg',[
        'Короб глубиной 25 идёт без ступенек от стены с тумбой до душа. За торцом стена уходит назад на 25.',
        'Ниша шкафа — предложение: ширина 70, низ 130, верх 250. Над ней до потолка 10.',
        'Колонна на этой же стороне комнаты; трап 90 параллелен стене. Стекло здесь видно с ребра.',
        '* Ось вытяжки 235 и положение шкафа предварительные. Уровни колонны и унитаза условные.',
    ])


def entrance():
    d=Drawing(258,'Стена с входной дверью','Смотрим от короба к двери. Душевая слева на развёртке, тумба справа.')
    d.rect(0,0,94,260,'#eef3ef')
    d.line(94,0,94,200,'#4388a1',4)
    d.text(46,125,'Душевая',19)
    d.text(46,112,'глубина 94',15)
    # 210 is only a graphical stand-in; door height is not supplied.
    d.rect(103,0,82,210,'#f1f0e9','#89958c',2)
    d.rect(106,1,76,206,'none','#b3b9b0',1)
    d.handle(174,99,7)
    d.text(144,158,'Вход · 82',19)
    d.text(144,145,'Высота проёма',13,'muted')
    d.text(144,135,'по замеру',13,'muted')
    d.rect(199,10,59,75,'#8a674b','#614d3d')
    d.rect(208,0,50,10,'#574635','#574635')
    d.rect(198,85,60,2,'#e8e8df')
    d.text(228,48,'Тумба',16,'woodtext')
    d.text(228,36,'глубина 60',13,'woodtext')
    d.hdim(0,103,143,'103 до начала проёма')
    d.hdim(103,185,143,'82 · дверь')
    d.hdim(185,258,143,'73 до стены')
    d.hdim(185,198,d.y(97),'13')
    d.vdim(0,200,d.x0-26,'200 · стекло с ребра')
    d.vdim(0,87,d.x(258)+32,'87 столешница')
    d.finish('wall-entrance.svg',[
        '103 — расстояние от дальней стены душа до начала дверного проёма, а не глубина душевой.',
        'От конца проёма до стены с тумбой: 258 − 103 − 82 = 73. Тумба глубиной 60 оставляет около 13.',
        'От линии стекла до начала проёма: 103 − 94 = 9. Ширина стекла видна на плане сверху.',
        'Высота двери не задана: контур условный. Точные наличники, петли и открывание — по выбранной двери.',
    ])


def shower():
    d=Drawing(200,'Душевая — вид со стороны тумбы','Смотрим к дальней стене душевой. Короб и колонна слева, открытый вход в душ справа.')
    d.rect(0,0,200,260,'#eef3ef')
    # Projected boxing return and fixed glass, explicitly not fixtures on the back wall.
    d.rect(0,0,25,260,'url(#hatch)')
    d.rect(25,0,100,200,'#e6f1f2','#4388a1',2)
    d.add(f'<path d="M{d.x(48):g} {d.y(50):g}L{d.x(87):g} {d.y(160):g}M{d.x(63):g} {d.y(48):g}L{d.x(102):g} {d.y(158):g}" stroke="#c3dee2" fill="none"/>')
    d.text(75,128,'Стекло',21,'blue')
    d.text(75,115,'100 × 200',17,'blue')
    d.text(163,130,'Вход',21)
    d.text(163,116,'≈ 75',19)
    d.text(100,237,'Потолок без светильников',16)
    d.text(76,217,'60 до потолка',14,'muted')
    d.hdim(0,25,143,'25')
    d.hdim(25,125,143,'100 · стекло')
    d.hdim(125,200,143,'75 · проход')
    d.vdim(0,200,d.x(200)+32,'200 высота стекла')
    d.finish('wall-shower.svg',[
        'Здесь показана проекция стекла и торца короба на дальнюю стену. Пол душа глубиной 94.',
        'Колонна не на дальней стене: она на левой боковой стене за торцом короба. См. развёртку короба.',
        'Трап 90 расположен параллельно левой стене с колонной; его направление видно на плане сверху.',
        'Проход: 200 − 25 − 100 = 75. Стекло высотой 200, до потолка 260 − 200 = 60.',
    ])


def cabinet():
    d=Drawing(150,'Шкаф над унитазом — наполнение','Предложение: ниша 70 × 120, низ 130, верх 250. Короб и размеры ниши проверяются по замеру.')
    d.rect(0,0,150,260,'url(#hatch)')
    # Clear recess 70 x 120, cabinet envelope 69 x 119, 5 mm fitting gaps.
    d.rect(40,130,70,120,'#fff','#614d3d',2)
    d.rect(40.5,130.5,69,119,'#8a674b','#614d3d',1)
    d.rect(42.3,132.3,65.4,115.4,'#f4ede3','#614d3d',1)
    for z in [164.3,192.1,219.9]: d.rect(42.3,z,65.4,1.8,'#8a674b','#614d3d',1)
    for z,label,h in [(132.3,'Флаконы · ежедневное',32),(166.1,'Бумага, салфетки',26),(193.9,'Небольшой запас',26),(221.7,'Редкий запас',26)]:
        d.text(75,z+h*.55,label,13)
        d.text(75,z+h*.55-7,f'Высота в свету {h}',12,'muted')
    d.hdim(40,110,143,'70 · ниша')
    d.vdim(130,250,d.x(119),'120 · ниша')
    d.vdim(0,130,d.x0-27,'130 до низа ниши')
    d.text(75,255,'10 до потолка',13)
    d.hdim(42.3,107.7,d.y(122),'65,4 внутри')
    d.text(75,104,'Две дверцы ≈ 35 × 120',15)
    d.text(75,94,'Петли по внешним бокам',13,'muted')
    d.text(75,84,'Ручки на высоте ≈ 145',13,'muted')
    d.text(75,74,'Открывание около 90°',13,'muted')
    d.text(75,56,'Цель по полезной глубине: 20',15)
    d.text(75,46,'Нужна свободная глубина ниши ≥ 23,1',12,'muted')
    d.text(75,27,'Под шкафом — инсталляция',14)
    d.finish('cabinet.svg',[
        'Расчётный пример: ниша 70 × 120; зазоры по 0,5; наружный корпус 69 × 119; панели и полки 1,8.',
        'Внутри по ширине 65,4. Четыре ячейки: 32 + 26 + 26 + 26; три полки по 1,8.',
        'Уровни опоры вещей: 132,3 / 166,1 / 193,9 / 221,7. Верхние ячейки — для редко нужного.',
        'Глубина 20 в свету: 20 + фасад 1,8 + задник 0,8 + запас 0,5 = 23,1; коммуникации не учтены.',
    ],overall_width=False)


if __name__ == '__main__':
    OUT.mkdir(parents=True,exist_ok=True)
    vanity(); boxing(); entrance(); shower(); cabinet()
    print('Built four bathroom wall elevations and a cabinet detail.')
