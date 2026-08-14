# -*- coding: utf-8 -*-
import json, html, re

raw = open('/home/claude/raw_shops.txt', encoding='utf-8').read().strip().split('\n')
from imgs import IMGS
records = []
for line in raw:
    name, rest = line.split('#', 1)
    floor, unit = rest.split('|', 1)
    records.append({'name': name.strip(), 'floor': floor.strip(), 'unit': unit.strip()})
assert len(records) == len(IMGS), (len(records), len(IMGS))
for i, r in enumerate(records):
    r['img'] = IMGS[i]

# ---- bucket override sets ----
SUPER   = {'Jaya Grocer', 'Panas Express'}
CONVENI = {'CU MART'}
ENT = {'DO ARENA LALAPORT','LaLaspeed E Kart Raceway','Jungle Gym','Indah Family Game Centre',
       'Molly Fantasy','Puzzle Planet','POP PLAY PLANET','Dimension Poptown','KLP48 Theatre',
       'Sonny Box Breaks','Photoism PLAY'}
SERVICE = {'A-Saloon','Jadioc Barbershop','Nailed It Manicure & Pedicure','AM Skin Factories',
           'IKUKO','Klinik Pergigian We Smile','Health Lane Family Pharmacy','Guardian',
           'Calisto Vision Care','Focus Point','Life n Fitness','Magic Photo','TM Currency Exchange',
           'REST N GO','S-Care'}
# explicit extra food names (not caught by FC/FH unit rule)
FOOD_EXTRA = {'Ben Gong\'s Tea','Burger King','Dee Coffee','Dome Cafe','eclipse café and meal',
    'Empire Sushi','FatFire','Go Wei (Go 味)','Hookie Dookie','Hut Dining Buffet','Ikkyu Izakaya',
    'Ippudo','Kita Dining','Koboreya','Koryouriya Tsudoi','KWING','LaLapop by Frozen','LeTen Dim Sum',
    'Lian Jie Noodle House','Lol Soon Kee Desserts','Lucky Cup','Marinero','Matcha Eight','Mee Hiris China Muslim',
    'Memang Meow Kopitiam','Menya Shi Shi Do','MY THAI BAR','Ngam Ngam','Oiso Korean Traditional Cuisine & Cafe',
    'ORBcafe','Padi Malaya','ParaThai','POKOK KL Cafe','Sai Kee Authentic Home Cuisine','Sakanoue Café',
    'Secret Recipe','Seoul Garden','Shabu-yo','Giglio Restaurant','Stammtisch','Subway','Sugar and I',
    'Sukiya','SUKI-YA','Sun San Curry','Sushi King','Sushi Yoshi','Syok Makan','Tan Ngan Lo',
    'The Chicken Rice Shop','V88','Wagyu and Rice','WAGYU DAGIN','Yakiniku Botan+','YOYO Bird\'s Nest Dessert Expert',
    'ZUS Coffee','Starbucks','Doko Koko Café','TOUS les JOURS','DONQ/Mini One','Koong Woh Tong','Cocosan'}

def bucket_of(r):
    n = r['name']; u = r['unit']
    if n in SUPER: return 'super'
    if n in CONVENI: return 'conveni'
    if n in ENT: return 'ent'
    if n in SERVICE: return 'service'
    if 'FC' in u or 'FH' in u or n in FOOD_EXTRA or n in FOOD: return 'food'
    return 'shop'

# ---- genre + japanese keyword base by genre ----
GENRE_KW = {
 'ファッション':'服 ふく ファッション アパレル 洋服 衣料 レディース メンズ',
 'ムスリムファッション':'服 ファッション ヒジャブ スカーフ ムスリム イスラム',
 'シューズ・靴':'靴 くつ シューズ スニーカー サンダル フットウェア',
 'スポーツ':'スポーツ 運動 ランニング スニーカー トレーニング',
 'バッグ・旅行用品':'バッグ かばん 鞄 スーツケース 旅行 キャリー ラゲッジ',
 'ジュエリー・アクセサリー':'アクセサリー ジュエリー ピアス ネックレス 装飾',
 '時計':'時計 とけい ウォッチ 腕時計',
 'アイウェア・メガネ':'メガネ めがね 眼鏡 サングラス アイウェア',
 'コスメ・美容雑貨':'コスメ 化粧品 美容 スキンケア 香水 フレグランス',
 '生活雑貨・インテリア':'雑貨 生活 インテリア 家具 日用品 100均 100円 ホームセンター',
 'キッチン雑貨':'キッチン 調理 鍋 フライパン 台所 調理器具',
 '家電・ガジェット':'家電 ガジェット スマホ 電化製品 電子 カメラ パソコン',
 '本・文具':'本 書店 書籍 文具 ステーショナリー ノート',
 'ホビー・アニメ':'ホビー おもちゃ 玩具 アニメ フィギュア トレカ キャラクター グッズ',
 'キッズ・ベビー':'こども 子供 子ども キッズ ベビー 赤ちゃん 子供服',
 '下着・ランジェリー':'下着 ランジェリー インナー ブラ 肌着',
 '雑貨・ギフト':'雑貨 ギフト プレゼント 贈り物 パーティ 風船',
 'ラーメン':'ラーメン らーめん 麺 とんこつ',
 '寿司':'寿司 すし スシ 回転寿司',
 '和食':'和食 日本食 日本料理 定食',
 '焼肉・鉄板':'焼肉 やきにく 鉄板 バーベキュー BBQ ステーキ 肉',
 'しゃぶしゃぶ・鍋':'しゃぶしゃぶ 鍋 すき焼き 食べ放題 ビュッフェ',
 '中華・点心':'中華 点心 飲茶 中国料理',
 '韓国料理':'韓国 韓国料理 コリアン キンパ チキン',
 'タイ料理':'タイ タイ料理',
 'ローカル飯（マレー・中華）':'ローカル マレーシア料理 マレー ナシ 麺 チキンライス 屋台',
 'ファストフード':'ファストフード ハンバーガー バーガー サンドイッチ 軽食',
 'カフェ・コーヒー':'カフェ コーヒー 珈琲 喫茶 スタバ ラテ',
 'ドリンク・タピオカ':'ドリンク タピオカ ミルクティー お茶 ジュース タピオカティー',
 'スイーツ・デザート':'スイーツ デザート 甘味 アイス ケーキ ドーナツ クッキー パン ベーカリー',
 'バー・居酒屋':'バー 居酒屋 酒 ビール お酒',
 'スーパー':'スーパー 食料品 グロサリー 食品 買い出し',
 'コンビニ':'コンビニ コンビニエンス 24時間',
 'ヘアサロン・理容':'美容室 ヘアサロン 理容 床屋 散髪 髪',
 'ネイル':'ネイル マニキュア ペディキュア 爪',
 'エステ・美容':'エステ 美容 スキンケア 脱毛 フェイシャル',
 '歯科・クリニック':'歯科 歯医者 クリニック 病院 医療',
 '薬局・ドラッグ':'薬局 ドラッグストア 薬 医薬品 ヘルスケア',
 'ジム・フィットネス':'ジム フィットネス 運動 トレーニング',
 '両替':'両替 外貨 換金 マネーチェンジャー',
 '写真・プリント':'写真 プリント フォト 証明写真 プリクラ',
 'ゲームセンター・遊び':'ゲームセンター アミューズメント 遊び 子供 ゲーム',
 'アクティビティ':'アクティビティ アトラクション 体験 遊び',
 '劇場・ホール':'劇場 ホール ライブ アイドル',
 'その他':'',
}

# name -> (genre, extra_katakana_keywords)
G = {
 '3COINS':('生活雑貨・インテリア','スリーコインズ 300円'),
 '6IXTY8IGHT':('下着・ランジェリー','シックスティエイト'),
 'adidas Outlet':('スポーツ','アディダス'),
 'Akemi Outlet':('生活雑貨・インテリア','アケミ 寝具 タオル'),
 'AM Skin Factories':('エステ・美容','スキン'),
 'animate':('ホビー・アニメ','アニメイト'),
 'animate cafe':('カフェ・コーヒー','アニメイトカフェ アニメ'),
 'animate the only shop':('ホビー・アニメ','アニメイト'),
 'A-Saloon':('ヘアサロン・理容','エーサロン'),
 'Babyshop':('キッズ・ベビー','ベビーショップ'),
 'Balabala':('キッズ・ベビー','バラバラ 子供服'),
 'Bata':('シューズ・靴','バタ'),
 'BBCC Sales Gallery':('その他','ギャラリー 販売'),
 'Beauty Scents':('コスメ・美容雑貨','ビューティーセント 香水'),
 'BERFOE':('ファッション','ベルフォー'),
 'BFF Label':('ファッション','レディース'),
 'BOKITTA':('ムスリムファッション','ボキッタ ヒジャブ'),
 'BookXcess':('本・文具','ブックエクセス 洋書 書店'),
 'Butik Izo':('ファッション','ブティック'),
 'Calisto LaLaport Outlet':('アイウェア・メガネ','カリスト メガネ'),
 'Calvin Klein':('ファッション','カルバンクライン CK'),
 'camel active, C by camel active':('ファッション','キャメルアクティブ アウトドア'),
 'Carlo Rino Outlet':('バッグ・旅行用品','カルロリノ 靴 バッグ'),
 'CHAINON':('ファッション','シェノン レディース'),
 'Clarks':('シューズ・靴','クラークス'),
 'Cole Haan':('シューズ・靴','コールハーン'),
 'Coloris':('ジュエリー・アクセサリー','カラリス'),
 'comcoca':('生活雑貨・インテリア','コムコカ'),
 'Comfort Sole':('シューズ・靴','コンフォートソール'),
 'Comfort Sole Outlet':('シューズ・靴','コンフォートソール'),
 'COMO':('ファッション','コモ'),
 'Converse':('シューズ・靴','コンバース'),
 'Couple Lab':('ファッション','カップルラボ ペアルック'),
 'Crocs':('シューズ・靴','クロックス'),
 'Daiso':('生活雑貨・インテリア','ダイソー 100均'),
 'Dapper':('ファッション','ダッパー メンズ'),
 'Delsey':('バッグ・旅行用品','デルセー スーツケース'),
 'Doko Koko Goods':('ホビー・アニメ','ドコココ キャラクター'),
 'Doko Koko Pick Up':('ホビー・アニメ','ドコココ 受取'),
 "D'Passions":('ファッション','パッション'),
 'Dr. Locker':('シューズ・靴','ドクターロッカー スニーカー'),
 'D\'SPECIAL DAY DECOR . GIFT . BALLOON':('雑貨・ギフト','デコレーション 風船 ギフト'),
 'Dzi Kingdom':('ジュエリー・アクセサリー','天珠 パワーストーン'),
 'Earth Music and Ecology':('ファッション','アースミュージック'),
 'Eightiin':('ファッション','エイティーン'),
 'elianto':('コスメ・美容雑貨','エリアント コスメ'),
 'ELLE':('ファッション','エル'),
 'F.O.S':('ファッション','エフオーエス アウトレット'),
 'FILA':('スポーツ','フィラ'),
 'Fipper':('シューズ・靴','フィッパー サンダル ビーチサンダル'),
 'FitFlop':('シューズ・靴','フィットフロップ'),
 'Fleur':('ジュエリー・アクセサリー','フルール'),
 'G2000':('ファッション','ジーニトウセン オフィス スーツ'),
 'Gaagookids':('キッズ・ベビー','子供服'),
 'Garmin':('家電・ガジェット','ガーミン スマートウォッチ GPS'),
 'GEOX':('シューズ・靴','ジェオックス'),
 'Gintell':('家電・ガジェット','ジンテル マッサージチェア 健康'),
 'Global Work':('ファッション','グローバルワーク'),
 'Godzilla':('ホビー・アニメ','ゴジラ キャラクター'),
 'Going Shop':('生活雑貨・インテリア','ゴーイングショップ'),
 'GOOM':('ファッション','グーム'),
 'GShock Casio':('時計','Gショック カシオ 腕時計'),
 'havaianas':('シューズ・靴','ハワイアナス ビーチサンダル'),
 'HEKA AI':('家電・ガジェット','ヘカ ガジェット'),
 'Horgen':('生活雑貨・インテリア','ホーゲン 家具'),
 'IKUKO':('エステ・美容','イクコ 日本 ビューティー'),
 'I-Scent':('コスメ・美容雑貨','アイセント 香水'),
 'Kaadoya':('ホビー・アニメ','カードや トレカ'),
 'Kappa':('スポーツ','カッパ'),
 'Kashkha':('ファッション','カシュカ'),
 'Kickers':('シューズ・靴','キッカーズ'),
 'KKV':('生活雑貨・インテリア','雑貨 ライフスタイル'),
 'KOBO7':('ホビー・アニメ','コーボー グッズ'),
 'LARRIE':('バッグ・旅行用品','ラリー バッグ'),
 'Leather Avenue':('バッグ・旅行用品','レザー 革製品 財布'),
 'Lee Outlet':('ファッション','リー ジーンズ デニム'),
 "Levi's":('ファッション','リーバイス ジーンズ デニム'),
 'Li-Ning, Nike Swim+, Sportsclick Outlet':('スポーツ','リーニン ナイキ 水着'),
 'Lovisa':('ジュエリー・アクセサリー','ロヴィサ アクセサリー'),
 'LuxLexicon':('バッグ・旅行用品','高級ブランドバッグ リセール'),
 'Marcapada.my':('ファッション','マルカパダ'),
 'Max Fashion':('ファッション','マックスファッション'),
 'Metrojaya':('ファッション','メトロジャヤ 百貨店 デパート'),
 'Minimore':('ファッション','ミニモア'),
 'Minitech Gadget':('家電・ガジェット','ガジェット 周辺機器'),
 'Miniso Friends':('生活雑貨・インテリア','メニソ 雑貨'),
 'MiX.Store':('ファッション','ミックスストア セレクト'),
 'MONTIGO, cosmic cookware':('キッチン雑貨','モンティゴ 調理器具'),
 'Mori Mory':('雑貨・ギフト','モリモリ'),
 'Moscule':('ファッション','モスキュル'),
 'MR. D.I.Y.':('生活雑貨・インテリア','ミスターDIY 日用品 工具'),
 'MXD Hobby':('ホビー・アニメ','ホビー プラモデル'),
 'Naelofar':('ムスリムファッション','ナエロファ ヒジャブ'),
 'Nautica':('ファッション','ノーティカ'),
 'NERVEHUNTER':('ファッション','ストリート'),
 'New Era':('ファッション','ニューエラ 帽子 キャップ'),
 'NIID':('バッグ・旅行用品','ニード バックパック リュック'),
 'NITORI':('生活雑貨・インテリア','ニトリ 家具 インテリア'),
 'Nojima':('家電・ガジェット','ノジマ 家電'),
 'NOT ONLY TOY':('ホビー・アニメ','おもちゃ フィギュア'),
 'Nullset Goods':('ホビー・アニメ','グッズ'),
 'Oakley':('アイウェア・メガネ','オークリー サングラス'),
 'Objet':('生活雑貨・インテリア','オブジェ ギフト'),
 'OnlyKorea':('コスメ・美容雑貨','オンリーコリア 韓国コスメ'),
 'Original Classic':('ファッション','オリジナルクラシック'),
 'Oxwhite':('ファッション','オックスホワイト ベーシック'),
 'Panda Eyes':('ファッション','パンダアイズ'),
 'PANGOI':('バッグ・旅行用品','パンゴイ バッグ'),
 'Papeleria by VIVE':('本・文具','文具 ステーショナリー'),
 'Pierre Cardin Lingerie':('下着・ランジェリー','ピエールカルダン 下着'),
 'POLO HAUS':('ファッション','ポロハウス'),
 'POLO HAUS & GENE MARTINO':('ファッション','ポロハウス'),
 'PONEY':('キッズ・ベビー','ポニー 子供服'),
 'Private Stitch':('ファッション','プライベートステッチ メンズ'),
 'Q Pocket':('ホビー・アニメ','キューポケット アニメ グッズ'),
 'QMac':('家電・ガジェット','Qマック アップル Mac iPhone'),
 'Ray-Ban':('アイウェア・メガネ','レイバン サングラス'),
 'Red Wing Shoes':('シューズ・靴','レッドウィング ブーツ'),
 'Regal':('シューズ・靴','リーガル 革靴'),
 'Renoma':('ファッション','レノマ'),
 'Rev Runnr':('スポーツ','ランニング'),
 'Rhapsody':('ファッション','ラプソディ'),
 'Roberto Cavalli':('ファッション','ロベルトカヴァリ 高級'),
 'Rookie':('ファッション','ルーキー'),
 'Running Lab':('スポーツ','ランニング ラボ ランニングシューズ'),
 'Sacoor One':('ファッション','サコール'),
 'Samsonite':('バッグ・旅行用品','サムソナイト スーツケース'),
 'Sasa':('コスメ・美容雑貨','ササ コスメ'),
 'SEMBONIA':('バッグ・旅行用品','センボニア バッグ 革'),
 'Semir':('ファッション','セミール'),
 'Sheldonet.shop':('ホビー・アニメ','シェルドネット おもちゃ'),
 'Skechers':('シューズ・靴','スケッチャーズ'),
 'Smart Master':('家電・ガジェット','スマートマスター スマホ'),
 'SODA':('シューズ・靴','ソーダ 靴'),
 'Sony Store':('家電・ガジェット','ソニー カメラ'),
 'Sorella Gallery':('下着・ランジェリー','ソレラ 下着'),
 'Star Child':('キッズ・ベビー','スターチャイルド 子供 写真'),
 'Sun Paradise':('ファッション','水着 スイムウェア'),
 'Superdry':('ファッション','スーパードライ'),
 'Swarovski':('ジュエリー・アクセサリー','スワロフスキー クリスタル'),
 'Tefal':('キッチン雑貨','ティファール 調理器具 フライパン'),
 'The Green Party':('ジュエリー・アクセサリー','グリーンパーティ アクセサリー'),
 'The Pink Room':('雑貨・ギフト','ピンクルーム ギフト'),
 'Time Movement':('時計','タイムムーブメント 腕時計'),
 'TOY WORLD':('ホビー・アニメ','トイワールド おもちゃ'),
 'Travel For All':('バッグ・旅行用品','スーツケース 旅行'),
 'Travel Zone':('バッグ・旅行用品','旅行用品 スーツケース'),
 'TUFF':('ファッション','タフ アウトドア ワーク'),
 'Under Armour':('スポーツ','アンダーアーマー'),
 'Universal Traveller':('バッグ・旅行用品','ユニバーサルトラベラー スーツケース'),
 'Veesee Collections':('ファッション','ヴィーシー'),
 "VERN'S":('シューズ・靴','バーンズ 靴'),
 'VibeMax':('ファッション','バイブマックス'),
 'VOIR GALLERY':('ファッション','ボア アウトレット'),
 'Wacoal':('下着・ランジェリー','ワコール 下着 ブラ'),
 'WEGO':('ファッション','ウィゴー 古着 カジュアル'),
 'Wt+':('ファッション','ダブルティー'),
 'Xiaomi':('家電・ガジェット','シャオミ スマホ'),
 'Xumi Goods':('雑貨・ギフト','グッズ'),
 'Young Heart':('ファッション','ヤングハート'),
 'Sun San Curry':('ローカル飯（マレー・中華）','サンサンカレー カレー'),
 'Boarding Gate':('バッグ・旅行用品','ボーディングゲート スーツケース 旅行'),
 "L'OCCITANE":('コスメ・美容雑貨','ロクシタン コスメ 香水'),
 'Melissa':('シューズ・靴','メリッサ ジェリーシューズ サンダル'),
 'K+ by Kadokawa gempak starz':('ホビー・アニメ','カドカワ 書籍 アニメ 漫画'),
 'Brooks, Pressio':('スポーツ','ブルックス ランニングシューズ'),
 'The Marathon Shop':('スポーツ','マラソン ランニングシューズ'),
 'YONNY':('その他','ヨニー'),
 'BBCC Sales Gallery':('その他','セールスギャラリー 不動産'),
 # services
 'Jadioc Barbershop':('ヘアサロン・理容','ジャディオック 床屋 バーバー'),
 'Nailed It Manicure & Pedicure':('ネイル','ネイルドイット ネイル'),
 'Klinik Pergigian We Smile':('歯科・クリニック','ウィースマイル 歯医者 歯科'),
 'Health Lane Family Pharmacy':('薬局・ドラッグ','ヘルスレーン 薬局'),
 'Guardian':('薬局・ドラッグ','ガーディアン ドラッグストア 薬'),
 'Calisto Vision Care':('アイウェア・メガネ','カリスト 眼科 メガネ 検眼'),
 'Focus Point':('アイウェア・メガネ','フォーカスポイント メガネ 検眼'),
 'Life n Fitness':('ジム・フィットネス','ライフフィットネス ジム'),
 'Magic Photo':('写真・プリント','マジックフォト 写真 プリント'),
 'TM Currency Exchange':('両替','両替 外貨'),
 'REST N GO':('エステ・美容','休憩 マッサージ'),
 'S-Care':('家電・ガジェット','スマホ 保護 修理'),
 # entertainment
 'DO ARENA LALAPORT':('アクティビティ','ドゥアリーナ eスポーツ 体験'),
 'LaLaspeed E Kart Raceway':('アクティビティ','ゴーカート レーシング カート'),
 'Jungle Gym':('ゲームセンター・遊び','ジャングルジム 子供 遊び'),
 'Indah Family Game Centre':('ゲームセンター・遊び','ゲームセンター アーケード'),
 'Molly Fantasy':('ゲームセンター・遊び','モーリーファンタジー 子供 ゲーム'),
 'Puzzle Planet':('ゲームセンター・遊び','パズルプラネット'),
 'POP PLAY PLANET':('ゲームセンター・遊び','ポッププレイ 子供'),
 'Dimension Poptown':('ゲームセンター・遊び','ディメンション'),
 'KLP48 Theatre':('劇場・ホール','KLP48 アイドル 劇場'),
 'Sonny Box Breaks':('ホビー・アニメ','ソニー ボックスブレイク トレカ'),
 'Photoism PLAY':('写真・プリント','フォトイズム プリクラ 証明写真'),
 # supermarket / conveni
 'Jaya Grocer':('スーパー','ジャヤグローサー スーパー 食料品'),
 'Panas Express':('スーパー','パナス 食料品 グロサリー'),
 'CU MART':('コンビニ','CU コンビニ 韓国'),
}

# ---- food: genre + price + note ----
# price tiers: 1=お手軽(¥) 2=普通(¥¥) 3=ちょっと贅沢(¥¥¥)
FOOD = {
 'Akiba Ramen':('ラーメン',2,'秋葉ラーメン。フードコートで手軽に食べられる日本式ラーメン'),
 'Ayam Penyet Best':('ローカル飯（マレー・中華）',1,'アヤムペネット（インドネシア/マレー式の潰し揚げ鶏）'),
 "Ben Gong's Tea":('ドリンク・タピオカ',1,'台湾系ティースタンド'),
 'Boost Juice':('ドリンク・タピオカ',1,'豪州発の生ジュース・スムージー'),
 'Burger King':('ファストフード',1,'世界的バーガーチェーン'),
 'Cocosan':('スイーツ・デザート',1,'ココナッツ系スイーツ'),
 'Container Kebab':('ファストフード',1,'ケバブのテイクアウト'),
 'Dee Coffee':('カフェ・コーヒー',1,'コーヒースタンド'),
 'Dee Thai Restaurant':('タイ料理',2,'タイ料理'),
 'Dome Cafe':('カフェ・コーヒー',2,'豪州style オールデイカフェ'),
 "DONQ/Mini One":('スイーツ・デザート',2,'日本のベーカリー「ドンク」。ミニクロワッサンが名物'),
 'Doutor':('カフェ・コーヒー',1,'日本のコーヒーチェーン「ドトール」'),
 'Doko Koko Café':('カフェ・コーヒー',2,'キャラクター系コンセプトカフェ'),
 'Dunkin\'':('スイーツ・デザート',1,'ダンキン。ドーナツとコーヒー'),
 'eclipse café and meal':('カフェ・コーヒー',2,'カフェ＆軽食'),
 'Empire Sushi':('寿司',2,'マレーシアの回転寿司チェーン'),
 'ENAK ENAK express':('ローカル飯（マレー・中華）',1,'ローカルのお手軽飯'),
 'Famous Amos':('スイーツ・デザート',1,'有名なチョコチップクッキー店'),
 'FatFire':('バー・居酒屋',2,'グリル＆バー系'),
 'Giglio Restaurant':('和食',3,'落ち着いた雰囲気のレストラン'),
 'Go Wei (Go 味)':('中華・点心',2,'中華系'),
 'Gong Cha':('ドリンク・タピオカ',1,'貢茶。台湾系タピオカミルクティー大手'),
 'Happy Potato':('ファストフード',1,'ポテト系スナック'),
 'Hawker Chan':('ローカル飯（マレー・中華）',1,'シンガポール発、ミシュラン由来の醤油鶏飯（チキンライス）で有名'),
 'Hercaa':('ローカル飯（マレー・中華）',1,'フードホールのローカル飯'),
 "Hot & Roll, IMP'za":('ファストフード',1,'ロール系スナックとピザ'),
 'Hut Dining Buffet':('しゃぶしゃぶ・鍋',3,'ビュッフェダイニング'),
 'I Love Yoo!':('中華・点心',1,'油條（ヨウティャオ）と粥のローカルブランド'),
 'Ikkyu Izakaya':('バー・居酒屋',3,'日本式居酒屋'),
 'Ippudo':('ラーメン',2,'博多発祥の有名とんこつラーメンチェーン「一風堂」'),
 'JJ Chili Pan Mee':('ローカル飯（マレー・中華）',1,'チリパンミー（干し麺）の人気ローカル店'),
 'Kaki Lima Corner':('ローカル飯（マレー・中華）',1,'屋台風ローカル飯'),
 'Killiney':('カフェ・コーヒー',1,'シンガポール発の老舗コピティアム'),
 'Kita Dining':('和食',2,'日本式ダイニング'),
 'Koboreya':('和食',2,'こぼれや。日本式の料理'),
 'Koong Woh Tong':('ドリンク・タピオカ',1,'恭和堂。亀ゼリー（亀苓膏）と漢方ドリンク'),
 'KorFry':('韓国料理',1,'韓国式フライドチキン'),
 'Koryouriya Tsudoi':('和食',3,'小料理屋つどい。本格和食'),
 'KWING':('ローカル飯（マレー・中華）',2,'ローカル系ダイニング'),
 'LaLapop by Frozen':('スイーツ・デザート',1,'アイス／冷菓'),
 'LeTen Dim Sum':('中華・点心',2,'点心・飲茶'),
 'Lian Jie Noodle House':('中華・点心',1,'麺料理'),
 'Little Wok Fried Rice':('中華・点心',1,'炒飯（チャーハン）専門'),
 'Llao Llao':('スイーツ・デザート',1,'スペイン発フローズンヨーグルト'),
 'Lol Soon Kee Desserts':('スイーツ・デザート',1,'囉信記。中華系の糖水（甘味）'),
 'Lucky Cup':('ドリンク・タピオカ',1,'ドリンクスタンド'),
 'Marinero':('和食',3,'シーフード系レストラン'),
 'Matcha Eight':('スイーツ・デザート',2,'抹茶スイーツ専門'),
 'Mee Brothers':('ローカル飯（マレー・中華）',1,'麺料理'),
 'Mee Hiris China Muslim':('ローカル飯（マレー・中華）',1,'中華ムスリム系の麺料理'),
 'Memang Meow Kopitiam':('ローカル飯（マレー・中華）',1,'ローカルのコピティアム'),
 'Menya Shi Shi Do':('ラーメン',2,'麺屋 宍道。日本式ラーメン'),
 'Meow Western':('ファストフード',1,'ローカル式の洋食（ウェスタン）'),
 'MIXUE':('スイーツ・デザート',1,'中国発の激安アイス＆ドリンク「蜜雪氷城」'),
 'MR CORN':('スイーツ・デザート',1,'カップコーン系スナック'),
 'Mr. Chizu':('スイーツ・デザート',1,'チーズ系スナック'),
 'MY THAI BAR':('タイ料理',2,'タイ料理＆バー'),
 'NAM HEONG SINCE 1938':('カフェ・コーヒー',1,'1938年創業のイポー発コピティアム。ホワイトコーヒーが名物'),
 'Nasi Lemak by Memang':('ローカル飯（マレー・中華）',1,'マレーシアの国民食ナシレマ'),
 'Ngam Ngam':('カフェ・コーヒー',2,'ネイバーフッド系カフェ'),
 'Oiso Korean Traditional Cuisine & Cafe':('韓国料理',2,'韓国の伝統料理＆カフェ'),
 'ORBcafe':('カフェ・コーヒー',2,'カフェ'),
 'Padi Malaya':('ローカル飯（マレー・中華）',2,'マレー料理'),
 'ParaThai':('タイ料理',2,'タイ料理'),
 'Pizza Gao! Gao!':('ファストフード',2,'ピザ'),
 'POKOK KL Cafe':('カフェ・コーヒー',2,'KL発の人気カフェ'),
 'Restoran Loong Kee':('ローカル飯（マレー・中華）',1,'福建麺（ホッケンミー）などのローカル飯'),
 'Sai Kee Authentic Home Cuisine':('中華・点心',2,'家庭的な中華料理'),
 'Sakanoue Café':('カフェ・コーヒー',2,'坂の上カフェ。和カフェ'),
 'Secret Recipe':('カフェ・コーヒー',2,'マレーシアのケーキ＆カフェチェーン'),
 'Seoul Garden':('韓国料理',3,'韓国式BBQ＆スチームボート食べ放題の人気チェーン'),
 'Shabu-yo':('しゃぶしゃぶ・鍋',3,'日本のしゃぶしゃぶ食べ放題チェーン「しゃぶ葉」'),
 'Sizz Mee':('ローカル飯（マレー・中華）',1,'麺料理'),
 'Sizzling Master':('焼肉・鉄板',2,'鉄板ステーキ'),
 'Stack\'d':('ファストフード',2,'バーガー系'),
 'Stammtisch':('バー・居酒屋',3,'ドイツ料理＆ビアバー'),
 'Subway':('ファストフード',2,'サンドイッチチェーン'),
 'Sugar and I':('スイーツ・デザート',2,'デザート＆スイーツ'),
 'Sukiya':('和食',1,'日本の牛丼チェーン「すき家」'),
 'SUKI-YA':('しゃぶしゃぶ・鍋',3,'しゃぶしゃぶ・すき焼き食べ放題'),
 'Sun San Curry':('ローカル飯（マレー・中華）',1,'カレー系ローカル飯'),
 'Sushi King':('寿司',2,'マレーシアの回転寿司大手チェーン'),
 'Sushi Yoshi':('寿司',3,'本格寿司'),
 'Syok Makan':('ローカル飯（マレー・中華）',1,'ローカル飯'),
 'Tan Ngan Lo':('ドリンク・タピオカ',1,'陳源和。ハーバル飲料（涼茶）'),
 'Tealive':('ドリンク・タピオカ',1,'マレーシア最大のミルクティーチェーン'),
 'The Chicken Rice Shop':('ローカル飯（マレー・中華）',2,'マレーシアのチキンライス専門チェーン'),
 'Torigen Chicken Ramen':('ラーメン',1,'鶏系ラーメン'),
 'TOUS les JOURS':('スイーツ・デザート',2,'韓国系ベーカリーカフェ'),
 'V88':('カフェ・コーヒー',2,'カフェ＆バー'),
 'Wagyu and Rice':('焼肉・鉄板',3,'和牛丼'),
 'WAGYU DAGIN':('焼肉・鉄板',3,'和牛焼肉'),
 'Wok On Fire':('中華・点心',1,'中華鍋料理'),
 'Yakiniku Botan+':('焼肉・鉄板',2,'焼肉ぼたん'),
 "YOYO Bird's Nest Dessert Expert":('スイーツ・デザート',2,'燕の巣デザート専門'),
 'ZUS Coffee':('カフェ・コーヒー',1,'マレーシア発で急成長中の人気コーヒーチェーン'),
 'Starbucks':('カフェ・コーヒー',2,'世界的コーヒーチェーン「スタバ」'),
}

# ---- finer food sub-genres (my classification, 目安) ----
FOOD_FINE = {
 'Ippudo':'ラーメン','Menya Shi Shi Do':'ラーメン','Akiba Ramen':'ラーメン','Torigen Chicken Ramen':'ラーメン',
 'Empire Sushi':'寿司','Sushi King':'寿司','Sushi Yoshi':'寿司',
 'Sukiya':'牛丼・丼もの','Wagyu and Rice':'牛丼・丼もの',
 'Yakiniku Botan+':'焼肉','WAGYU DAGIN':'焼肉',
 'Sizzling Master':'鉄板・ステーキ',
 'Shabu-yo':'しゃぶしゃぶ・すき焼き','SUKI-YA':'しゃぶしゃぶ・すき焼き',
 'Kita Dining':'和食・小料理','Koboreya':'和食・小料理','Koryouriya Tsudoi':'和食・小料理',
 'Ikkyu Izakaya':'居酒屋・バー','FatFire':'居酒屋・バー',
 'LeTen Dim Sum':'中華・点心','Sai Kee Authentic Home Cuisine':'中華・点心','Go Wei (Go 味)':'中華・点心',
 'Wok On Fire':'中華・点心','Little Wok Fried Rice':'中華・点心',
 'Lian Jie Noodle House':'中華麺・ローカル麺','Restoran Loong Kee':'中華麺・ローカル麺','Sizz Mee':'中華麺・ローカル麺',
 'Mee Brothers':'中華麺・ローカル麺','Mee Hiris China Muslim':'中華麺・ローカル麺','JJ Chili Pan Mee':'中華麺・ローカル麺',
 'Hawker Chan':'チキンライス','The Chicken Rice Shop':'チキンライス',
 'I Love Yoo!':'粥・中華軽食',
 'Nasi Lemak by Memang':'マレー料理','Padi Malaya':'マレー料理','Ayam Penyet Best':'マレー料理',
 'Hercaa':'マレーシア・ローカル飯','Kaki Lima Corner':'マレーシア・ローカル飯','Syok Makan':'マレーシア・ローカル飯',
 'ENAK ENAK express':'マレーシア・ローカル飯','KWING':'マレーシア・ローカル飯','Hookie Dookie':'マレーシア・ローカル飯',
 'Papafry':'スナック・軽食',
 'Sun San Curry':'カレー',
 'Oiso Korean Traditional Cuisine & Cafe':'韓国料理・韓国BBQ','Seoul Garden':'韓国料理・韓国BBQ',
 'KorFry':'韓国チキン',
 'ParaThai':'タイ料理','Dee Thai Restaurant':'タイ料理','MY THAI BAR':'タイ料理',
 'Giglio Restaurant':'洋食・イタリアン','Marinero':'洋食・イタリアン','Stammtisch':'洋食・イタリアン','Meow Western':'洋食・イタリアン',
 'Burger King':'ハンバーガー',"Stack'd":'ハンバーガー',
 'Subway':'サンドイッチ',
 'Pizza Gao! Gao!':'ピザ',"Hot & Roll, IMP'za":'ピザ',
 'Container Kebab':'スナック・軽食','Happy Potato':'スナック・軽食','MR CORN':'スナック・軽食','Mr. Chizu':'スナック・軽食',
 'Doko Koko Café':'カフェ','Dome Cafe':'カフェ','eclipse café and meal':'カフェ','ORBcafe':'カフェ',
 'Sakanoue Café':'カフェ','V88':'カフェ','POKOK KL Cafe':'カフェ','Ngam Ngam':'カフェ','Secret Recipe':'カフェ',
 'NAM HEONG SINCE 1938':'コピティアム（伝統喫茶）','Killiney':'コピティアム（伝統喫茶）','Memang Meow Kopitiam':'コピティアム（伝統喫茶）',
 'Dee Coffee':'コーヒースタンド','Doutor':'コーヒースタンド','Starbucks':'コーヒースタンド','ZUS Coffee':'コーヒースタンド',
 'Gong Cha':'タピオカ・ミルクティー','Tealive':'タピオカ・ミルクティー',"Ben Gong's Tea":'タピオカ・ミルクティー','Lucky Cup':'タピオカ・ミルクティー',
 'Boost Juice':'ジュース・スムージー',
 'Koong Woh Tong':'涼茶・ハーバル','Tan Ngan Lo':'涼茶・ハーバル',
 'DONQ/Mini One':'ベーカリー・パン','TOUS les JOURS':'ベーカリー・パン',
 "Dunkin'":'ドーナツ',
 'Llao Llao':'アイス・フローズン','MIXUE':'アイス・フローズン','LaLapop by Frozen':'アイス・フローズン','Cocosan':'アイス・フローズン',
 'Famous Amos':'スイーツ・デザート','Lol Soon Kee Desserts':'スイーツ・デザート','Matcha Eight':'スイーツ・デザート',
 'Sugar and I':'スイーツ・デザート',"YOYO Bird's Nest Dessert Expert":'スイーツ・デザート',
 'Hut Dining Buffet':'ビュッフェ',
}
GENRE_KW.update({
 '牛丼・丼もの':'牛丼 丼 どんぶり ぎゅうどん 和食 日本',
 '焼肉':'焼肉 やきにく BBQ バーベキュー 肉 和牛',
 '鉄板・ステーキ':'ステーキ 鉄板 肉 ステーキハウス 洋食',
 'しゃぶしゃぶ・すき焼き':'しゃぶしゃぶ すき焼き 鍋 食べ放題 ビュッフェ 日本',
 '和食・小料理':'和食 日本料理 小料理 定食 日本',
 '居酒屋・バー':'居酒屋 バー 酒 ビール お酒 日本',
 '中華麺・ローカル麺':'麺 ヌードル ローカル 中華 パンミー ホッケンミー',
 'チキンライス':'チキンライス 鶏飯 ローカル マレーシア チキン',
 '粥・中華軽食':'粥 おかゆ 中華 軽食 ローカル',
 'マレー料理':'マレー マレーシア料理 ナシ ナシレマ ハラル ローカル',
 'マレーシア・ローカル飯':'ローカル マレーシア 屋台 ローカル飯 ハラル',
 'カレー':'カレー curry ローカル インド',
 '韓国料理・韓国BBQ':'韓国 韓国料理 コリアン 韓国BBQ 焼肉 サムギョプサル キンパ',
 '韓国チキン':'韓国 韓国チキン フライドチキン チキン コリアン',
 '洋食・イタリアン':'洋食 イタリアン パスタ ピザ ウエスタン ステーキ 西洋',
 'ハンバーガー':'ハンバーガー バーガー ファストフード 洋食',
 'サンドイッチ':'サンドイッチ サブ 軽食 ファストフード',
 'ピザ':'ピザ pizza イタリアン',
 'スナック・軽食':'軽食 スナック テイクアウト ケバブ ポテト おやつ',
 'カフェ':'カフェ 喫茶 コーヒー スタバ お茶 軽食',
 'コピティアム（伝統喫茶）':'コピティアム 喫茶 コーヒー ローカル 白珈琲 カフェ',
 'コーヒースタンド':'コーヒー 珈琲 カフェ スタバ ラテ エスプレッソ',
 'ジュース・スムージー':'ジュース スムージー ドリンク フルーツ',
 '涼茶・ハーバル':'涼茶 ハーバル 漢方 亀ゼリー ドリンク お茶',
 'ベーカリー・パン':'ベーカリー パン パン屋 bakery クロワッサン',
 'ドーナツ':'ドーナツ donut スイーツ おやつ',
 'アイス・フローズン':'アイス ジェラート フローズンヨーグルト かき氷 スイーツ 冷たい',
 'ビュッフェ':'ビュッフェ 食べ放題 バイキング',
})

PRICE_LABEL = {1:'¥ お手軽', 2:'¥¥ 普通', 3:'¥¥¥ ちょっと贅沢'}
BUCKET_LABEL = {'shop':'ショップ','food':'飲食','super':'スーパー','conveni':'コンビニ的',
                'ent':'娯楽・エンタメ','service':'サービス・美容'}

for r in records:
    b = bucket_of(r)
    r['bucket'] = b
    name = r['name']
    price = ''
    note = ''
    if b == 'food':
        if name in FOOD:
            genre, tier, note = FOOD[name]
        else:
            genre = 'マレーシア・ローカル飯'
            tier = 1 if ('FC' in r['unit'] or 'FH' in r['unit']) else 2
            note = ''
        genre = FOOD_FINE.get(name, genre)
        r['genre'] = genre
        r['price'] = tier
        r['price_label'] = PRICE_LABEL[tier]
        r['_kata'] = ''
        r['note'] = note
    else:
        if name in G:
            genre, kata = G[name]
        else:
            genre, kata = ('その他', '')
        r['genre'] = genre
        r['price'] = 0
        r['price_label'] = ''
        r['_kata'] = kata
        r['note'] = note  # '' for shops

# rename some genre labels to the user's vocabulary
RENAME = {'ファッション':'アパレル', 'コスメ・美容雑貨':'美容・コスメ'}
for r in records:
    r['genre'] = RENAME.get(r['genre'], r['genre'])

# ---- multi-tag: 1店が複数サブジャンルに出てOK（重複OK）。final labels only ----
TAGS_EXTRA = {
 # 飲食：かけ持ちジャンル
 'Seoul Garden':['焼肉','ビュッフェ'],
 'Oiso Korean Traditional Cuisine & Cafe':['カフェ'],
 'KorFry':['韓国料理・韓国BBQ'],
 'Yakiniku Botan+':['和食・小料理'],
 'Shabu-yo':['ビュッフェ','和食・小料理'],
 'SUKI-YA':['ビュッフェ','和食・小料理'],
 'Hut Dining Buffet':['洋食・イタリアン'],
 'Sukiya':['和食・小料理'],
 'Wagyu and Rice':['焼肉'],
 'Secret Recipe':['スイーツ・デザート'],
 'TOUS les JOURS':['カフェ','スイーツ・デザート'],
 'DONQ/Mini One':['スイーツ・デザート'],
 'Sugar and I':['カフェ'],
 'Matcha Eight':['カフェ'],
 'Sakanoue Café':['和食・小料理'],
 'eclipse café and meal':['洋食・イタリアン'],
 'V88':['居酒屋・バー'],
 'Starbucks':['カフェ'],
 'ZUS Coffee':['カフェ'],
 'Doutor':['カフェ'],
 'Dee Coffee':['カフェ'],
 'NAM HEONG SINCE 1938':['カフェ','コーヒースタンド'],
 'Killiney':['カフェ','コーヒースタンド'],
 'Memang Meow Kopitiam':['カフェ'],
 "Dunkin'":['コーヒースタンド'],
 'MIXUE':['タピオカ・ミルクティー'],
 'Llao Llao':['スイーツ・デザート'],
 'Cocosan':['スイーツ・デザート'],
 'LaLapop by Frozen':['スイーツ・デザート'],
 'Koong Woh Tong':['スイーツ・デザート'],
 'The Chicken Rice Shop':['マレーシア・ローカル飯'],
 'Pizza Gao! Gao!':['洋食・イタリアン'],
 # 物販：靴・スポーツのかけ持ち
 'Carlo Rino Outlet':['シューズ・靴'],
 'SEMBONIA':['シューズ・靴'],
 'LARRIE':['シューズ・靴'],
 'Brooks, Pressio':['シューズ・靴'],
 'Running Lab':['シューズ・靴'],
 'The Marathon Shop':['シューズ・靴'],
 'Rev Runnr':['シューズ・靴'],
 'adidas Outlet':['シューズ・靴'],
 'Under Armour':['シューズ・靴'],
 'Garmin':['スポーツ'],
}
for r in records:
    tags = [r['genre']]
    for t in TAGS_EXTRA.get(r['name'], []):
        if t not in tags:
            tags.append(t)
    r['tags'] = tags
    kwparts = [r['name']] + tags + [GENRE_KW.get(t, '') for t in tags] + [r.get('_kata',''), r.get('note','')]
    r['kw'] = ' '.join(kwparts).lower()

# ---- area (zone) assignment. 目安。現状 LG1 のみ地図から割り当て、他階は後日 ----
def area_of(r):
    if r['floor'] != 'LG1':
        return ''
    m = r['unit'].upper()
    if 'FH' in m:
        return 'Main Atrium（F）・デパ地下エリア'
    if 'FC' in m:
        return 'East Atrium（D）・フードコートエリア'
    mm = re.search(r'LG1-?0*(\d+)', m)
    if mm:
        n = int(mm.group(1))
        if n <= 6:
            return 'West Atrium（A）エリア'
        if n <= 8:
            return 'Main Atrium（F）エリア'
        if n in (15, 16):
            return '中央・Jaya Grocer前エリア'
        return 'East Atrium（D）エリア'
    return ''
for r in records:
    r['area'] = area_of(r)

# ---- 特別営業時間（公式 brandDetail から確認済み。2026-08時点） ----
# early=開店が10:00より早い / late=閉店が23:00以降（深夜）
SPECIAL_HOURS = {
    'ZUS Coffee':        {'hours': '8:00–22:00（毎日）',                         'tags': ['早朝']},
    'Starbucks':         {'hours': '9:00–22:00（毎日）',                         'tags': ['早朝']},
    'Marinero':          {'hours': '9:30–23:00',                                 'tags': ['早朝', '深夜']},
    'FatFire':           {'hours': '平日11:00–23:00／土日9:30–23:00',            'tags': ['深夜', '早朝(土日)']},
    'MY THAI BAR':       {'hours': '11:00–翌1:00',                               'tags': ['深夜']},
    'KWING':             {'hours': '11:00–翌0:00（金土は翌1:00）',               'tags': ['深夜']},
    'Hookie Dookie':     {'hours': '11:30–翌0:00',                               'tags': ['深夜']},
    'Stammtisch':        {'hours': '平日12:00–23:00／週末12:00–翌0:00',          'tags': ['深夜']},
    'Giglio Restaurant': {'hours': '月木11:00–15:00・17:00–22:00／金日11:00–23:00','tags': ['深夜']},
}
for r in records:
    sh = SPECIAL_HOURS.get(r['name'])
    r['hours'] = sh['hours'] if sh else ''
    r['openTags'] = sh['tags'] if sh else []

# ---- 料理タグ（公式紹介文由来）を検索kwへ追加。和食・日本の店はフィルタ用タグも付与 ----
from cuisine_tags import CUISINE_TAGS
for r in records:
    ct = CUISINE_TAGS.get(r['name'], '')
    if not ct:
        continue
    r['kw'] = (r['kw'] + ' ' + ct).lower()
    if '和食' in ct and '和食・日本' not in r['tags']:
        r['tags'].append('和食・日本')
        r['kw'] += ' 和食 日本食 japanese japan'

# ---- 日本語インデックス（英語キャプション由来・全ジャンル）を検索kwへ追加 ----
FOOD_JP = set('和食日本料理 寿司 ラーメン麺 和牛焼肉すき焼きしゃぶ 居酒屋バー 韓国料理 タイ料理 中華点心 洋食イタリアン バーガー チキン マレー料理ローカル デザートケーキスイーツ アイスクリーム ベーカリーパン コーヒーカフェ タピオカお茶ドリンク 抹茶 食べ放題ビュッフェ ハラル'.split())
def _norm(s):
    return re.sub(r'[^0-9a-z぀-ヿ一-鿿]', '', s.lower())
_rec_by_norm = {_norm(r['name']): r for r in records}
_food_name_re = re.compile(r'cafe|caf|coffee|\btea\b|dining|restaurant|kitchen|\bbar\b|grill|sushi|ramen|eatery|dessert|bakery|makan', re.I)
_jp_unmatched = []
try:
    _jp_lines = open('jp_index_raw.txt', encoding='utf-8').read().splitlines()
except FileNotFoundError:
    _jp_lines = []
for _line in _jp_lines:
    if ':::' not in _line:
        continue
    _nm, _tagstr = _line.split(':::', 1)
    _r = _rec_by_norm.get(_norm(_nm))
    if not _r:
        _jp_unmatched.append(_nm)
        continue
    _tags = _tagstr.split()
    _isfood = _r.get('bucket') in ('food', 'super', 'conveni') or _food_name_re.search(_r['name'])
    if not _isfood:
        _tags = [t for t in _tags if t not in FOOD_JP]
    # 「マレー料理ローカル」は Malaysia 由来の誤検出が多いので、マレー/ローカルの店だけに限定
    if 'マレー料理ローカル' in _tags:
        _malay_ok = bool(re.search(r'nasi|ayam|padi|hawker|kopitiam|mamak|lemak|makan|penyet|\broti|satay|malay|chili pan|loong kee|nam heong|tan ngan|syok|enak|dzi|godzilla|marcapada', _r['name'], re.I)) \
            or any(('マレー' in t or 'ローカル' in t) for t in _r.get('tags', []))
        if not _malay_ok:
            _tags = [t for t in _tags if t != 'マレー料理ローカル']
    if _tags:
        _r['kw'] = (_r['kw'] + ' ' + ' '.join(_tags)).strip()
if _jp_unmatched:
    print('JP index unmatched:', _jp_unmatched)

# ---- 各店の特徴語（厳選）を検索kwへ追加 ----
from specific_tags import SPECIFIC_TAGS
_sp_by_norm = {_norm(k): v for k, v in SPECIFIC_TAGS.items()}
for r in records:
    sp = _sp_by_norm.get(_norm(r['name']))
    if sp:
        r['kw'] = (r['kw'] + ' ' + sp).strip()

# ---- 一行の「売り」（HP由来）。カードに表示＋検索にも反映 ----
from hooks import HOOKS
# ロゴ＋帯の合成画像の店。上のロゴ部分だけ映す（cropで表示）
CROP_TOP = set()
for r in records:
    r['crop'] = r['name'] in CROP_TOP
_hook_by_norm = {_norm(k): v for k, v in HOOKS.items()}
for r in records:
    h = _hook_by_norm.get(_norm(r['name']), '')
    r['hook'] = h
    if h:
        r['kw'] = (r['kw'] + ' ' + h).strip()

# floor order
FLOOR_ORDER = {'LG1':0,'G':1,'L1':2,'L2':3,'L3':4,'L4':5,'L5':6}
records.sort(key=lambda r:(FLOOR_ORDER.get(r['floor'],9), r['name'].lower()))

# counts
from collections import Counter
bc = Counter(r['bucket'] for r in records)
print('TOTAL', len(records))
for k in ['shop','food','super','conveni','ent','service']:
    print(k, bc.get(k,0))

# ---- 料理系ジャンルのボタンを検索索引(kw)と一致させる。飲食店のみタグ補完 ----
GENRE_AUG = [
    ('しゃぶしゃぶ・すき焼き', ['すき焼き', 'しゃぶ']),
    ('焼肉', ['焼肉']),
    ('ラーメン', ['ラーメン']),
    ('寿司', ['寿司']),
    ('居酒屋・バー', ['居酒屋']),
    ('カレー', ['カレー']),
    ('タイ料理', ['タイ料理']),
    ('韓国料理・韓国BBQ', ['韓国料理', '韓国BBQ', 'キムチ']),
    ('中華・点心', ['点心', '小籠包', '火鍋', '中華点心']),
    ('スイーツ・デザート', ['デザート', 'ケーキ', 'ボンボローニ', 'スイーツ', 'ワッフル', 'クレープ']),
    ('アイス・フローズン', ['アイスクリーム', 'ジェラート']),
    ('ベーカリー・パン', ['ベーカリー', 'クロワッサン', '食パン']),
    ('カフェ', ['コーヒーカフェ']),
    ('タピオカ・ミルクティー', ['タピオカ', 'ミルクティー', 'バブルティー']),
    ('ビュッフェ', ['食べ放題', 'ビュッフェ']),
    ('ハンバーガー', ['バーガー']),
    ('チキンライス', ['チキンライス']),
    ('和食・小料理', ['天ぷら', '天丼', 'うどん', 'そば', '小料理', 'とんかつ', 'うなぎ', 'おにぎり', '弁当']),
]
for r in records:
    isfood = r.get('bucket') in ('food', 'super', 'conveni') or _food_name_re.search(r['name'])
    if not isfood:
        continue
    kw = r['kw']
    for tag, terms in GENRE_AUG:
        if any(t in kw for t in terms) and tag not in r['tags']:
            r['tags'].append(tag)

# ---- 物販・サービス系ジャンルの補完（jp-index精密カテゴリで判定。誤爆はEXCLUDE）----
GENRE_AUG2 = {
    '時計': ['時計腕時計ウォッチ'],
    '寝具': ['寝具ベッド'],
    'シューズ・靴': ['靴シューズスニーカー'],
    'バッグ・旅行用品': ['バッグ鞄リュック旅行用品'],
    'アイウェア・メガネ': ['メガネ眼鏡アイウェア'],
    '美容・コスメ': ['美容コスメ化粧品スキンケア'],
    'ヘアサロン・理容': ['ヘアサロン美容室理容'],
    'ネイル': ['ネイル'],
    '薬局・ドラッグ': ['薬局ドラッグストア'],
    '家電・ガジェット': ['家電ガジェット'],
    'ホビー・アニメ': ['アニメグッズ', 'フィギュア模型プラモ', '漫画コミック', 'ホビー趣味'],
    '本・文具': ['書籍本文具'],
    '生活雑貨・インテリア': ['家具インテリア', '生活雑貨キッチン日用品'],
    'スポーツ': ['スポーツ用品'],
    '両替': ['両替金融銀行'],
}
GENRE_AUG2_EXCLUDE = {
    'ホビー・アニメ': {'6IXTY8IGHT'},
    'バッグ・旅行用品': {'Dr. Locker'},
    'ヘアサロン・理容': {'AM Skin Factories'},
}
for r in records:
    for tag, keys in GENRE_AUG2.items():
        if r['name'] in GENRE_AUG2_EXCLUDE.get(tag, set()):
            continue
        if any(k in r['kw'] for k in keys) and tag not in r['tags']:
            r['tags'].append(tag)

# ---- 元分類の明確な誤りを修正（全店点検で発見）----
TAG_REMOVE = {
    'Dr. Locker': ['シューズ・靴'],                 # ロッカー預かりサービス（靴店ではない）
    'S-Care': ['家電・ガジェット'],                  # 健康シューズ（家電ではない）→ シューズ・靴は補完で付与
    'Focus Point': ['本・文具'],                    # 光学店（本屋ではない）
    'Calisto Vision Care': ['本・文具'],            # 光学店
    'NAM HEONG SINCE 1938': ['本・文具'],           # レストラン（誤検出）
    'Doko Koko Café': ['生活雑貨・インテリア'],       # アニメカフェ（雑貨店ではない）
    'ORBcafe': ['生活雑貨・インテリア'],             # アニメカフェ
}
for r in records:
    for t in TAG_REMOVE.get(r['name'], []):
        if t in r['tags']:
            r['tags'].remove(t)

# ---- サブジャンルの整理：重複・細かすぎる区分を統合（ドリンク系は据え置き）----
GENRE_MERGE = {
    'カフェ': 'カフェ・コーヒー',
    'コーヒースタンド': 'カフェ・コーヒー',
    '和食・小料理': '和食・日本',
    '中華麺・ローカル麺': '中華・点心',
    '粥・中華軽食': '中華・点心',
    'マレー料理': 'マレーシア・ローカル飯',
    '韓国チキン': '韓国料理・韓国BBQ',
    'ドーナツ': 'スイーツ・デザート',
    'サンドイッチ': 'ベーカリー・パン',
}
for r in records:
    newtags = []
    for t in r['tags']:
        t2 = GENRE_MERGE.get(t, t)
        if t2 not in newtags:
            newtags.append(t2)
    r['tags'] = newtags

# emit JSON for the html
data = [{'name':r['name'],'floor':r['floor'],'unit':r['unit'],'bucket':r['bucket'],
         'genre':r['genre'],'tags':r['tags'],'price':r['price'],'priceLabel':r['price_label'],
         'note':r.get('note',''),'hook':r.get('hook',''),'crop':r.get('crop',False),'area':r.get('area',''),'hours':r.get('hours',''),
         'openTags':r.get('openTags',[]),'img':r['img'],'kw':r['kw']} for r in records]
open('/home/claude/shops.json','w',encoding='utf-8').write(json.dumps(data,ensure_ascii=False))
print('wrote shops.json')
