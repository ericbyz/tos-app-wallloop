#!/usr/bin/env python3
"""Generate wallloop.lang for the TOS App Center (26 locales).

TOS 7.0 baseline ships 14 languages; TOS 7.1 documents a 26-language set.
We generate all 26 so the app displays correctly on both. Sections present
must never have empty name/auth/descript (review rule 8.5) — untranslated
languages are filled with English. Output: UTF-8 without BOM, LF endings.
"""
NAME_EN = "WallLoop"
AUTHOR = "ericbyz"
DESC_EN = (
    "Self-hosted dynamic wallpaper service: keep a wallpaper library (video/"
    "image) on the NAS and turn any browser screen — TV, tablet, phone — into "
    "a live wallpaper at http://<NAS>:18240/play. Interval rotation or day/"
    "night time-slot switching, a Chinese-first original admin panel inside "
    "the TOS desktop floating window, and demo wallpapers synthesized locally "
    "with the factory ffmpeg (no bundled media assets). Client API: "
    "GET /api/v1/now."
)
NOTE_EN = "1. Original app developed for the TOS App Center."
NOTE_ZH = "1. 为 TOS 应用中心原创开发的应用。"

# (locale, native name, native description) — English fallback for the rest
PRIMARY = [
    ("zh-cn", "WallLoop 动态壁纸",
     "自托管动态壁纸服务：把壁纸库（视频/图片）存在 NAS 上，电视、平板、手机浏览器"
     "打开 http://<NAS>:18240/play 即成动态壁纸大屏。支持间隔轮换与日/夜时段切换，"
     "管理面板为原创中文优先设计，内嵌于 TOS 桌面悬浮窗；演示壁纸由 NAS 本机 ffmpeg "
     "现场合成，不捆绑任何素材。客户端 API：GET /api/v1/now。"),
    ("zh-hk", "WallLoop 動態壁紙",
     "自託管動態壁紙服務：把壁紙庫（視頻/圖片）存在 NAS 上，電視、平板、手機瀏覽器"
     "打開 http://<NAS>:18240/play 即成動態壁紙大屏。支持間隔輪換與日/夜時段切換，"
     "管理面板為原創中文優先設計，內嵌於 TOS 桌面懸浮窗；演示壁紙由 NAS 本機 ffmpeg "
     "現場合成，不捆綁任何素材。客戶端 API：GET /api/v1/now。"),
]

NATIVE = {
    "ko-kr": "셀프 호스팅 동적 배경화면 서비스입니다. 배경화면 라이브러리(동영상/이미지)를 NAS에 두고 TV·태블릿·휴대폰 브라우저에서 http://<NAS>:18240/play 를 열면 동적 배경화면이 됩니다. 간격 순환 또는 낮/밤 시간대 전환을 지원하며, TOS 데스크톱 플로팅 창 안에 한국어·중국어 우선의 오리지널 관리 패널이 내장됩니다. 데모 배경화면은 NAS의 ffmpeg으로 로컬 합성되며 미디어 에셋을 번들하지 않습니다. 클라이언트 API: GET /api/v1/now.",
    "ja-jp": "セルフホストのダイナミック壁紙サービス。壁紙ライブラリ(動画/画像)を NAS に置き、TV・タブレット・スマホのブラウザで http://<NAS>:18240/play を開くだけでライブ壁紙になります。間隔ローテーションと昼/夜タイムスロット切替に対応し、TOS デスクトップのフローティングウィンドウ内に中国語優先のオリジナル管理パネルを内蔵。デモ壁紙は NAS 本体の ffmpeg でローカル合成し、メディアアセットは同梱しません。クライアント API: GET /api/v1/now.",
    "de-de": "Selbst gehosteter dynamischer Hintergrundbild-Dienst: Die Hintergrundbibliothek (Video/Bild) liegt auf dem NAS, und jeder Browser — TV, Tablet, Smartphone — wird unter http://<NAS>:18240/play zum Live-Hintergrund. Intervall-Rotation oder Tag/Nacht-Zeitschichten, ein chinesisch-firstiges Original-Adminpanel im TOS-Schwebefenster sowie lokal per ffmpeg synthetisierte Demo-Hintergründe (keine mitgelieferten Medien). Client-API: GET /api/v1/now.",
    "fr-fr": "Service de fonds d'écran dynamiques auto-hébergé : la bibliothèque (vidéo/image) reste sur le NAS et n'importe quel navigateur — TV, tablette, téléphone — devient un fond d'écran animé via http://<NAS>:18240/play. Rotation par intervalle ou créneaux jour/nuit, panneau d'administration original sinophone en fenêtre flottante TOS, fonds de démonstration synthétisés en local par ffmpeg (aucun média embarqué). API client : GET /api/v1/now.",
    "it-it": "Servizio di sfondi dinamici self-hosted: la libreria (video/immagini) resta sul NAS e qualsiasi browser — TV, tablet, telefono — diventa uno sfondo animato su http://<NAS>:18240/play. Rotazione a intervalli o fasce giorno/notte, pannello di amministrazione originale in cinese nella finestra flottante TOS, sfondi demo sintetizzati in locale con ffmpeg (nessun materiale multimediale incluso). API client: GET /api/v1/now.",
    "es-es": "Servicio de fondos dinámicos autoalojado: la biblioteca (vídeo/imagen) vive en el NAS y cualquier navegador — TV, tableta, teléfono — se convierte en fondo animado en http://<NAS>:18240/play. Rotación por intervalos o franjas día/noche, panel de administración original en chino en la ventana flotante de TOS y fondos de demostración sintetizados localmente con ffmpeg (sin materiales incluidos). API de cliente: GET /api/v1/now.",
    "hu-hu": "Önhosztolt dinamikus háttérkép-szolgáltatás: a háttérkönyvtár (videó/kép) a NAS-on marad, és bármely böngésző — TV, tablet, telefon — élő háttérré válik a http://<NAS>:18240/play oldalon. Időközönkénti rotáció vagy nappal/éjszaka idősáv-váltás, kínai nyelvű eredeti adminpanel a TOS lebegő ablakában, valamint helyben ffmpeg-fel előállított demó-hátterek (nincs becsomagolt média). Kliens API: GET /api/v1/now.",
    "pl-pl": "Samodzielnie hostowana usługa dynamicznych tapet: biblioteka tapet (wideo/obraz) jest na NAS-ie, a dowolna przeglądarka — TV, tablet, telefon — staje się żywą tapetą pod adresem http://<NAS>:18240/play. Rotacja interwałowa lub tryby dzień/noc, oryginalny panel administracyjny (najpierw chiński) w pływającym oknie TOS oraz tapety demonstracyjne syntetyzowane lokalnie przez ffmpeg (brak dołączonych mediów). API klienta: GET /api/v1/now.",
    "tr-tr": "Kendi kendine barındırılan dinamik duvar kağıdı hizmeti: duvar kağıdı kitaplığı (video/görsel) NAS'ta durur ve herhangi bir tarayıcı — TV, tablet, telefon — http://<NAS>:18240/play adresinde canlı duvar kağıdına dönüşür. Aralıklı rotasyon veya gündüz/gece zaman dilimi geçişi, TOS yüzen penceresinde Çince öncelikli özgün yönetim paneli ve fabrika ffmpeg'i ile yerel olarak sentezlenen demo duvar kağıtları (medya varlığı paketlenmez). İstemci API'si: GET /api/v1/now.",
    "ru-ru": "Самостоятельно размещаемый сервис динамических обоев: библиотека обоев (видео/изображения) хранится на NAS, и любой браузер — телевизор, планшет, телефон — становится живыми обоями на http://<NAS>:18240/play. Ротация по интервалу или переключение день/ночь, оригинальная китайскоязычная панель управления в плавающем окне TOS и демо-обои, синтезируемые локально фабричным ffmpeg (медиафайлы не поставляются). Клиентский API: GET /api/v1/now.",
    "pt-pt": "Serviço de papéis de parede dinâmicos auto-hospedado: a biblioteca (vídeo/imagem) fica no NAS e qualquer navegador — TV, tablet, telefone — torna-se um papel de parede animado em http://<NAS>:18240/play. Rotação por intervalo ou faixas dia/noite, painel de administração original em chinês na janela flutuante do TOS e papéis de demonstração sintetizados localmente com o ffmpeg de fábrica (sem materiais incluídos). API do cliente: GET /api/v1/now.",
    "cs-cz": "Samostatně hostovaná služba dynamických tapet: knihovna tapet (video/obrázek) je na NAS a libovolný prohlížeč — TV, tablet, telefon — se na http://<NAS>:18240/play stane živou tapetou. Rotace po intervalu nebo denní/noční časové pásmy, originální čínsky orientovaný administrační panel v plovoucím okně TOS a demo tapety syntetizované lokálně pomocí ffmpeg (bez přiložených médií). Klientské API: GET /api/v1/now.",
    "da-dk": "Selv-hostet dynamisk tapetservice: tapetbiblioteket (video/billede) ligger på NAS'en, og enhver browser — TV, tablet, telefon — bliver et levende tapet på http://<NAS>:18240/play. Intervalrotation eller dag/nadtidsrum, originalt kinesisk-først adminpanel i TOS' flydende vindue samt demo-tapeter syntetiseret lokalt med fabrikens ffmpeg (ingen indlejrede medier). Klient-API: GET /api/v1/now.",
    "nl-nl": "Zelf gehoste dynamische achtergrondservice: de bibliotheek (video/afbeelding) staat op de NAS en elke browser — tv, tablet, telefoon — wordt een levende achtergrond via http://<NAS>:18240/play. Intervalrotatie of dag/nachttijden, een origineel Chineestalig adminpaneel in het TOS-zwevende venster en lokaal met ffmpeg gesynthetiseerde demo-achtergronden (geen meegeleverde media). Client-API: GET /api/v1/now.",
    "nb-no": "Selvhostet dynamisk bakgrunnstjeneste: bakgrunnsbiblioteket (video/bilde) ligger på NAS-en, og enhver nettleser — TV, nettbrett, telefon — blir en levende bakgrunn på http://<NAS>:18240/play. Intervallrotasjon eller dag/natt-tidsrom, originalt kinesisk-først adminpanel i TOS' flytende vindu samt demobakgrunner syntetisert lokalt med fabrikkens ffmpeg (ingen innebygde medier). Klient-API: GET /api/v1/now.",
    "sv-se": "Självhostad dynamisk bakgrundstjänst: bakgrundsbiblioteket (video/bild) ligger på NAS:et och vilken webbläsare som helst — TV, surfplatta, telefon — blir en levande bakgrund på http://<NAS>:18240/play. Intervallrotation eller dag/natt-tidsrum, originalkinesisk adminpanel i TOS flytande fönster samt demobakgrunder syntetiserade lokalt med fabrikens ffmpeg (inga inbäddade medier). Klient-API: GET /api/v1/now.",
    "el-gr": "Υποδομή δυναμικών ταπετσαριών σε self-hosting: η βιβλιοθήκη ταπετσαριών (βίντεο/εικόνα) βρίσκεται στο NAS και οποιοσδήποτε browser — τηλεόραση, tablet, τηλέφωνο — γίνεται ζωντανή ταπετσαρία στο http://<NAS>:18240/play. Περιστροφή ανά διάστημα ή ζώνες ημέρας/νύχτας, πρωτότυπος πίνακας διαχείρισης (κυρίως κινεζικά) στο αιωρούμενο παράθυρο TOS και ταπετσαρίες demo συντεθιμένες τοπικά με το ffmpeg του εργοστασίου (χωρίς ενσωματωμένα μέσα). API πελάτη: GET /api/v1/now.",
    "ro-ro": "Serviciu auto-găzduit de tapete dinamice: biblioteca de tapete (video/imagini) stă pe NAS, iar orice browser — TV, tabletă, telefon — devine o tapetă vie la http://<NAS>:18240/play. Rotație la intervale sau intervale zi/noapte, panou de administrare original (chineză prioritar) în fereastra flotantă TOS și tapete demonstrative sintetizate local cu ffmpeg-ul din fabrică (fără media incluse). API client: GET /api/v1/now.",
    "th-th": "บริการวอลเปเปอร์ dynamic แบบเซลฟ์โฮสต์: เก็บคลังวอลเปเปอร์ (วิดีโอ/รูปภาพ) ไว้บน NAS แล้วเปิด http://<NAS>:18240/play จากเบราว์เซอร์ใดก็ได้ — TV แท็บเล็ต โทรศัพท์ — ให้กลายเป็นวอลเปเปอร์เคลื่อนไหว รองรับการหมุนเวียนตามช่วงเวลาหรือกลางวัน/กลางคืน แผงผู้ดูแลต้นฉบับจีนเป็นหลักในหน้าต่างลอยของ TOS และวอลเปเปอร์ตัวอย่างสังเคราะห์ในเครื่องด้วย ffmpeg ของระบบ (ไม่แถมสื่อ) API ไคลเอนต์: GET /api/v1/now",
    "vi-vn": "Dịch vụ hình nền động tự lưu trữ: thư viện hình nền (video/ảnh) nằm trên NAS, mọi trình duyệt — TV, máy tính bảng, điện thoại — trở thành hình nền động tại http://<NAS>:18240/play. Hỗ trợ luân chuyển theo khoảng thời gian hoặc khung ngày/đêm, bảng quản trị gốc ưu tiên tiếng Trung trong cửa sổ nổi TOS, hình nền demo được tổng hợp cục bộ bằng ffmpeg của máy (không kèm dữ liệu media). API máy khách: GET /api/v1/now.",
    "id-id": "Layanan wallpaper dinamis yang di-hosting sendiri: pustaka wallpaper (video/gambar) disimpan di NAS, dan browser mana pun — TV, tablet, ponsel — menjadi wallpaper hidup di http://<NAS>:18240/play. Mendukung rotasi berkala atau pergantian slot siang/malam, panel admin orisinal berbahasa Mandarin di jendela mengambang TOS, serta wallpaper demo yang disintesis lokal dengan ffmpeg bawaan (tanpa aset media bawaan). API klien: GET /api/v1/now.",
    "ar-sa": "خدمة خلفيات ديناميكية مستضافة ذاتيًا: مكتبة الخلفيات (فيديو/صور) على NAS، وأي متصفح — تلفاز أو لوحي أو هاتف — يصبح خلفية حية على http://<NAS>:18240/play. تدعم التدوير الزمني أو التبديل بين فترتي النهار والليل، لوحة إدارة أصلية بالصينية أولاً داخل النافذة العائمة لـ TOS، وخلفيات تجريبية تُخلَّق محليًا بـ ffmpeg المدمج في النظام (بدون وسائط مرفقة). واجهة العميل: GET /api/v1/now.",
    "he-il": "שירות טפטים דינמיים מאוחסן-עצמי: ספריית הטפטים (וידאו/תמונה) נשארת ב-NAS, וכל דפדפן — טלוויזיה, טאבלט, טלפון — הופך לטפט חי בכתובת http://<NAS>:18240/play. תמיכה ברוטציה מחזורית או מקטעי יום/לילה, פאנל ניהול מקורי (סינית בראש סדר העדיפויות) בחלון הצף של TOS, וטפטי הדגמה המסונתזים מקומית עם ה-ffmpeg המובנה (ללא מדיה מצורפת). API לקוח: GET /api/v1/now.",
}

ORDER = ["zh-cn", "zh-hk", "en-us", "ko-kr", "ja-jp", "de-de", "fr-fr", "it-it",
         "es-es", "hu-hu", "pl-pl", "tr-tr", "ru-ru", "pt-pt", "cs-cz", "da-dk",
         "nl-nl", "nb-no", "sv-se", "el-gr", "ro-ro", "th-th", "vi-vn", "id-id",
         "ar-sa", "he-il"]


def main(out_path: str) -> int:
    lines = []
    for loc in ORDER:
        for l, n, d in PRIMARY:
            if l == loc:
                name, desc = n, d
                break
        else:
            name, desc = NAME_EN, NATIVE.get(loc, DESC_EN)
        note = NOTE_ZH if loc in ("zh-cn", "zh-hk") else NOTE_EN
        lines.append(f"[{loc}]")
        lines.append(f'name = "{name}"')
        lines.append(f'auth = "{AUTHOR}"')
        lines.append(f'descript = "{desc}"')
        lines.append(f'note = "{note}"')
        lines.append("")
    open(out_path, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
    print(f"wrote {out_path}: {len(ORDER)} locales")


if __name__ == "__main__":
    raise SystemExit(main("wallloop.lang"))
