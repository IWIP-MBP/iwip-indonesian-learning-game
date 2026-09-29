"""
Generate curated question JSON files for lessons 3-21.
Run this once to create the initial curated question sets.
"""
import os
import json

curated_dir = os.path.join(os.path.dirname(__file__), 'curated')
os.makedirs(curated_dir, exist_ok=True)

# ── Lesson 3: Direction, Kami vs Kita, weather verbs ──────────────────────────
lesson_3 = [
  {"type":"vocab_choice","content":"Kami 和 Kita 都表示我们，区别是什么？","options":[{"text":"Kami 不包括对方，Kita 包括对方","is_correct":True},{"text":"Kita 不包括对方，Kami 包括对方","is_correct":False},{"text":"两者完全相同","is_correct":False},{"text":"Kami 更正式","is_correct":False}],"explanation":"Kami（我们，不含听者）；Kita（咱们，含听者）。"},
  {"type":"vocab_choice","content":"Mereka 是什么意思？","options":[{"text":"他们","is_correct":True},{"text":"你们","is_correct":False},{"text":"咱们","is_correct":False},{"text":"大家","is_correct":False}],"explanation":"Mereka 意为他们/她们/它们，第三人称复数。"},
  {"type":"vocab_choice","content":"kanan 是什么意思？","options":[{"text":"右","is_correct":True},{"text":"左","is_correct":False},{"text":"前面","is_correct":False},{"text":"后面","is_correct":False}],"explanation":"kanan 意为右，kiri 意为左。"},
  {"type":"vocab_choice","content":"kiri 是什么意思？","options":[{"text":"左","is_correct":True},{"text":"右","is_correct":False},{"text":"里","is_correct":False},{"text":"外","is_correct":False}],"explanation":"kiri 意为左，kanan 意为右。"},
  {"type":"vocab_choice","content":"maju 是什么意思？","options":[{"text":"往前/前进","is_correct":True},{"text":"往后","is_correct":False},{"text":"停止","is_correct":False},{"text":"转弯","is_correct":False}],"explanation":"maju 意为往前/前进/先进。"},
  {"type":"vocab_choice","content":"jalan kaki 是什么意思？","options":[{"text":"步行/走路","is_correct":True},{"text":"走路上班","is_correct":False},{"text":"道路","is_correct":False},{"text":"脚步","is_correct":False}],"explanation":"jalan kaki = 走路，jalan 是走/路，kaki 是脚。"},
  {"type":"vocab_choice","content":"mana 是什么意思？","options":[{"text":"哪里","is_correct":True},{"text":"什么","is_correct":False},{"text":"谁","is_correct":False},{"text":"多少","is_correct":False}],"explanation":"mana 意为哪里/哪个，用于询问位置或选择。"},
  {"type":"vocab_choice","content":"situ 是什么意思？","options":[{"text":"那儿（中距离）","is_correct":True},{"text":"这里","is_correct":False},{"text":"那里（远）","is_correct":False},{"text":"哪里","is_correct":False}],"explanation":"situ 是中等距离的那儿，sini 是近处的这里，sana 是远处的那里。"},
  {"type":"vocab_choice","content":"句子 Kamu di kiri. 的意思是？","options":[{"text":"你在左边","is_correct":True},{"text":"你在右边","is_correct":False},{"text":"你在前面","is_correct":False},{"text":"你往左走","is_correct":False}],"explanation":"Kamu di kiri. = 你（kamu）+ 在（di）+ 左边（kiri）= 你在左边。"},
  {"type":"vocab_choice","content":"句子 Di mana mereka? 的意思是？","options":[{"text":"他们在哪里？","is_correct":True},{"text":"他们是谁？","is_correct":False},{"text":"他们做什么？","is_correct":False},{"text":"他们什么时候来？","is_correct":False}],"explanation":"Di mana mereka? = 在哪里（di mana）+ 他们（mereka）= 他们在哪里？"},
  {"type":"vocab_choice","content":"barat 是什么意思？","options":[{"text":"西","is_correct":True},{"text":"东","is_correct":False},{"text":"南","is_correct":False},{"text":"北","is_correct":False}],"explanation":"barat 是西方，方位词：utara（北）、selatan（南）、timur（东）、barat（西）。"},
  {"type":"vocab_choice","content":"bersama 是什么意思？","options":[{"text":"一起","is_correct":True},{"text":"分开","is_correct":False},{"text":"独自","is_correct":False},{"text":"合作","is_correct":False}],"explanation":"bersama 意为一起/共同。"},
  {"type":"vocab_choice","content":"basah 是什么意思？","options":[{"text":"湿","is_correct":True},{"text":"干","is_correct":False},{"text":"热","is_correct":False},{"text":"冷","is_correct":False}],"explanation":"basah 意为湿，kering 意为干。"},
  {"type":"vocab_choice","content":"batal 是什么意思？","options":[{"text":"取消","is_correct":True},{"text":"完成","is_correct":False},{"text":"推迟","is_correct":False},{"text":"开始","is_correct":False}],"explanation":"batal 意为取消/作废，如 dibatalkan（被取消）。"},
  {"type":"vocab_choice","content":"bernyanyi 是什么意思？","options":[{"text":"唱歌","is_correct":True},{"text":"跳舞","is_correct":False},{"text":"跑步","is_correct":False},{"text":"游泳","is_correct":False}],"explanation":"bernyanyi = ber + nyanyi（唱），意为唱歌。"},
  {"type":"cn_to_indo","content":"中文他们对应的印尼语是？","options":[{"text":"mereka","is_correct":True},{"text":"kami","is_correct":False},{"text":"kita","is_correct":False},{"text":"kalian","is_correct":False}],"explanation":"mereka 是第三人称复数他们。"},
  {"type":"cn_to_indo","content":"中文右对应的印尼语是？","options":[{"text":"kanan","is_correct":True},{"text":"kiri","is_correct":False},{"text":"depan","is_correct":False},{"text":"belakang","is_correct":False}],"explanation":"kanan 是右，kiri 是左。"},
  {"type":"cn_to_indo","content":"中文左对应的印尼语是？","options":[{"text":"kiri","is_correct":True},{"text":"kanan","is_correct":False},{"text":"maju","is_correct":False},{"text":"mundur","is_correct":False}],"explanation":"kiri 是左，kanan 是右。"},
  {"type":"cn_to_indo","content":"中文哪里对应的印尼语疑问词是？","options":[{"text":"mana","is_correct":True},{"text":"apa","is_correct":False},{"text":"siapa","is_correct":False},{"text":"kapan","is_correct":False}],"explanation":"mana 意为哪里，用于询问位置。"},
  {"type":"cn_to_indo","content":"中文唱歌对应的印尼语是？","options":[{"text":"bernyanyi","is_correct":True},{"text":"berdansa","is_correct":False},{"text":"bermain","is_correct":False},{"text":"berlari","is_correct":False}],"explanation":"bernyanyi 意为唱歌，ber- 是动词前缀。"},
  {"type":"cn_to_indo","content":"中文取消对应的印尼语是？","options":[{"text":"batal","is_correct":True},{"text":"berhenti","is_correct":False},{"text":"buang","is_correct":False},{"text":"belok","is_correct":False}],"explanation":"batal 意为取消/作废。"},
  {"type":"cn_to_indo","content":"中文湿对应的印尼语是？","options":[{"text":"basah","is_correct":True},{"text":"kering","is_correct":False},{"text":"panas","is_correct":False},{"text":"dingin","is_correct":False}],"explanation":"basah 意为湿，kering 意为干。"},
  {"type":"cn_to_indo","content":"中文干净对应的印尼语是？","options":[{"text":"bersih","is_correct":True},{"text":"kotor","is_correct":False},{"text":"basah","is_correct":False},{"text":"kering","is_correct":False}],"explanation":"bersih 意为干净，kotor 意为脏。"},
  {"type":"cn_to_indo","content":"中文骑自行车对应的印尼语是？","options":[{"text":"bersepeda","is_correct":True},{"text":"berlari","is_correct":False},{"text":"berenang","is_correct":False},{"text":"berjalan","is_correct":False}],"explanation":"bersepeda 意为骑自行车，sepeda 是自行车。"},
  {"type":"cn_to_indo","content":"中文旅游对应的印尼语是？","options":[{"text":"berwisata","is_correct":True},{"text":"bepergian","is_correct":False},{"text":"berjalan","is_correct":False},{"text":"berlibur","is_correct":False}],"explanation":"berwisata 意为旅游/观光，wisata 是旅游。"},
  {"type":"indo_to_cn","content":"选择正确的中文翻译：\n【 bersama 】","options":[{"text":"一起","is_correct":True},{"text":"分开","is_correct":False},{"text":"独自","is_correct":False},{"text":"对面","is_correct":False}],"explanation":"bersama 意为一起/共同。"},
  {"type":"indo_to_cn","content":"选择正确的中文翻译：\n【 barat 】","options":[{"text":"西","is_correct":True},{"text":"东","is_correct":False},{"text":"南","is_correct":False},{"text":"北","is_correct":False}],"explanation":"barat 是西方。"},
  {"type":"indo_to_cn","content":"选择正确的中文翻译：\n【 batuk 】","options":[{"text":"咳嗽","is_correct":True},{"text":"发烧","is_correct":False},{"text":"腹泻","is_correct":False},{"text":"过敏","is_correct":False}],"explanation":"batuk 意为咳嗽。"},
  {"type":"indo_to_cn","content":"选择正确的中文翻译：\n【 bekerja 】","options":[{"text":"做工作/干活","is_correct":True},{"text":"游泳","is_correct":False},{"text":"购物","is_correct":False},{"text":"散步","is_correct":False}],"explanation":"bekerja 意为工作/干活，kerja 是工作。"},
  {"type":"indo_to_cn","content":"选择正确的中文翻译：\n【 belakang 】","options":[{"text":"后面","is_correct":True},{"text":"前面","is_correct":False},{"text":"旁边","is_correct":False},{"text":"左边","is_correct":False}],"explanation":"belakang 意为后面，depan 意为前面。"},
  {"type":"indo_to_cn","content":"选择正确的中文翻译：\n【 berapa 】","options":[{"text":"几/多少","is_correct":True},{"text":"什么","is_correct":False},{"text":"哪里","is_correct":False},{"text":"为什么","is_correct":False}],"explanation":"berapa 意为几/多少，如 Berapa harganya?（多少钱？）"}
]

# ── Lesson 4: Ownership, Thank you, greeting phrases ──────────────────────────
lesson_4 = [
  {"type":"vocab_choice","content":"Terima kasih 是什么意思？","options":[{"text":"谢谢","is_correct":True},{"text":"对不起","is_correct":False},{"text":"不客气","is_correct":False},{"text":"你好","is_correct":False}],"explanation":"Terima kasih 是印尼语谢谢，非常常用的礼貌用语。"},
  {"type":"vocab_choice","content":"Sama-sama 是什么意思？","options":[{"text":"不客气","is_correct":True},{"text":"谢谢","is_correct":False},{"text":"对不起","is_correct":False},{"text":"你好","is_correct":False}],"explanation":"Sama-sama 是回应感谢的用语，意为不客气，相当于英语 You are welcome。"},
  {"type":"vocab_choice","content":"Siapa 是什么意思？","options":[{"text":"谁","is_correct":True},{"text":"什么","is_correct":False},{"text":"哪里","is_correct":False},{"text":"什么时候","is_correct":False}],"explanation":"Siapa 是印尼语谁，如 Siapa nama kamu?（你叫什么名字？）"},
  {"type":"vocab_choice","content":"Sudah 是什么意思？","options":[{"text":"已经","is_correct":True},{"text":"还没有","is_correct":False},{"text":"刚才","is_correct":False},{"text":"将要","is_correct":False}],"explanation":"Sudah 意为已经，表示某事已发生，与 belum（还没）相对。"},
  {"type":"vocab_choice","content":"Kalian 是什么意思？","options":[{"text":"你们","is_correct":True},{"text":"咱们","is_correct":False},{"text":"他们","is_correct":False},{"text":"我们","is_correct":False}],"explanation":"Kalian 意为你们（第二人称复数），比 Anda 更口语。"},
  {"type":"vocab_choice","content":"Apakah ini barang kamu? 的意思是？","options":[{"text":"这是你的东西吗？","is_correct":True},{"text":"这是什么东西？","is_correct":False},{"text":"你的东西在哪里？","is_correct":False},{"text":"谁的东西是这个？","is_correct":False}],"explanation":"Apakah ini barang kamu? = 这（ini）+ 是（=）+ 你的（kamu）+ 东西（barang）吗（apakah）？"},
  {"type":"vocab_choice","content":"Barang ini milik siapa? 的意思是？","options":[{"text":"这个东西是谁的？","is_correct":True},{"text":"这是什么东西？","is_correct":False},{"text":"东西在哪里？","is_correct":False},{"text":"谁买了这个东西？","is_correct":False}],"explanation":"milik 表示属于，Barang ini milik siapa? 意为这个东西是谁的？"},
  {"type":"vocab_choice","content":"milik 是什么意思？","options":[{"text":"属于","is_correct":True},{"text":"买","is_correct":False},{"text":"拿","is_correct":False},{"text":"送","is_correct":False}],"explanation":"milik 意为属于/所有，如 ini milik saya（这是我的）。"},
  {"type":"vocab_choice","content":"Terima kasih sudah bantu kami. 的意思是？","options":[{"text":"谢谢你帮助了我们","is_correct":True},{"text":"我们需要你的帮助","is_correct":False},{"text":"你已经帮过我们","is_correct":False},{"text":"感谢你来看我们","is_correct":False}],"explanation":"Terima kasih + sudah（已经）+ bantu（帮助）+ kami（我们），意为谢谢你帮助了我们。"},
  {"type":"vocab_choice","content":"beli 是什么意思？","options":[{"text":"买","is_correct":True},{"text":"卖","is_correct":False},{"text":"拿","is_correct":False},{"text":"用","is_correct":False}],"explanation":"beli 意为买，menjual 意为卖。"},
  {"type":"vocab_choice","content":"bisa 是什么意思？","options":[{"text":"会/能（有能力）","is_correct":True},{"text":"可以（被允许）","is_correct":False},{"text":"必须","is_correct":False},{"text":"想要","is_correct":False}],"explanation":"bisa 意为会/能（有能力做）；boleh 意为可以（被允许）。"},
  {"type":"vocab_choice","content":"belok 是什么意思？","options":[{"text":"拐","is_correct":True},{"text":"直走","is_correct":False},{"text":"停止","is_correct":False},{"text":"返回","is_correct":False}],"explanation":"belok 意为拐/转弯，如 belok kanan（右转）。"},
  {"type":"vocab_choice","content":"bisKuit 是什么意思？","options":[{"text":"饼干","is_correct":True},{"text":"蛋糕","is_correct":False},{"text":"面包","is_correct":False},{"text":"糖果","is_correct":False}],"explanation":"biskuit 是饼干，源自英语 biscuit。"},
  {"type":"vocab_choice","content":"bola voli 是什么意思？","options":[{"text":"排球","is_correct":True},{"text":"足球","is_correct":False},{"text":"篮球","is_correct":False},{"text":"羽毛球","is_correct":False}],"explanation":"bola voli 是排球，bola 是球，voli 是排球运动。"},
  {"type":"vocab_choice","content":"benar 是什么意思？","options":[{"text":"正确","is_correct":True},{"text":"错误","is_correct":False},{"text":"好","is_correct":False},{"text":"坏","is_correct":False}],"explanation":"benar 意为正确/对，与 betul 同义，与 salah（错）相对。"},
  {"type":"cn_to_indo","content":"中文谢谢对应的印尼语是？","options":[{"text":"Terima kasih","is_correct":True},{"text":"Sama-sama","is_correct":False},{"text":"Maaf","is_correct":False},{"text":"Permisi","is_correct":False}],"explanation":"Terima kasih 是谢谢。"},
  {"type":"cn_to_indo","content":"中文不客气对应的印尼语是？","options":[{"text":"Sama-sama","is_correct":True},{"text":"Terima kasih","is_correct":False},{"text":"Maaf","is_correct":False},{"text":"Baik","is_correct":False}],"explanation":"Sama-sama 是不客气，回应谢谢的标准用法。"},
  {"type":"cn_to_indo","content":"中文谁对应的印尼语疑问词是？","options":[{"text":"siapa","is_correct":True},{"text":"apa","is_correct":False},{"text":"mana","is_correct":False},{"text":"kapan","is_correct":False}],"explanation":"siapa 意为谁。"},
  {"type":"cn_to_indo","content":"中文已经对应的印尼语是？","options":[{"text":"sudah","is_correct":True},{"text":"belum","is_correct":False},{"text":"akan","is_correct":False},{"text":"sedang","is_correct":False}],"explanation":"sudah 意为已经，与 belum（还没有）相对。"},
  {"type":"cn_to_indo","content":"中文属于对应的印尼语是？","options":[{"text":"milik","is_correct":True},{"text":"minta","is_correct":False},{"text":"makan","is_correct":False},{"text":"maju","is_correct":False}],"explanation":"milik 意为属于/所有，如 ini milik saya（这是我的）。"},
  {"type":"cn_to_indo","content":"中文买对应的印尼语是？","options":[{"text":"beli","is_correct":True},{"text":"bayar","is_correct":False},{"text":"bantu","is_correct":False},{"text":"bawa","is_correct":False}],"explanation":"beli 意为买。"},
  {"type":"cn_to_indo","content":"中文正确对应的印尼语是？","options":[{"text":"benar","is_correct":True},{"text":"baik","is_correct":False},{"text":"betul","is_correct":False},{"text":"salah","is_correct":False}],"explanation":"benar 意为正确，与 betul 同义。"},
  {"type":"cn_to_indo","content":"中文可以（有能力）对应的印尼语是？","options":[{"text":"bisa","is_correct":True},{"text":"boleh","is_correct":False},{"text":"harus","is_correct":False},{"text":"mau","is_correct":False}],"explanation":"bisa 意为能/会（有能力），boleh 意为可以（被允许）。"},
  {"type":"cn_to_indo","content":"中文排球对应的印尼语是？","options":[{"text":"bola voli","is_correct":True},{"text":"bola basket","is_correct":False},{"text":"bulu tangkis","is_correct":False},{"text":"sepak bola","is_correct":False}],"explanation":"bola voli 是排球。"},
  {"type":"cn_to_indo","content":"中文饼干对应的印尼语是？","options":[{"text":"biskuit","is_correct":True},{"text":"roti","is_correct":False},{"text":"kue","is_correct":False},{"text":"coklat","is_correct":False}],"explanation":"biskuit 是饼干（源自英语 biscuit）。"},
  {"type":"indo_to_cn","content":"选择正确的中文翻译：\n【 Terima kasih 】","options":[{"text":"谢谢","is_correct":True},{"text":"对不起","is_correct":False},{"text":"不客气","is_correct":False},{"text":"你好","is_correct":False}],"explanation":"Terima kasih 意为谢谢。"},
  {"type":"indo_to_cn","content":"选择正确的中文翻译：\n【 Sama-sama 】","options":[{"text":"不客气","is_correct":True},{"text":"谢谢","is_correct":False},{"text":"对不起","is_correct":False},{"text":"再见","is_correct":False}],"explanation":"Sama-sama 意为不客气。"},
  {"type":"indo_to_cn","content":"选择正确的中文翻译：\n【 milik 】","options":[{"text":"属于","is_correct":True},{"text":"买","is_correct":False},{"text":"拿","is_correct":False},{"text":"给","is_correct":False}],"explanation":"milik 意为属于/所有。"},
  {"type":"indo_to_cn","content":"选择正确的中文翻译：\n【 sudah 】","options":[{"text":"已经","is_correct":True},{"text":"还没有","is_correct":False},{"text":"刚才","is_correct":False},{"text":"将要","is_correct":False}],"explanation":"sudah 意为已经。"},
  {"type":"indo_to_cn","content":"选择正确的中文翻译：\n【 siapa 】","options":[{"text":"谁","is_correct":True},{"text":"什么","is_correct":False},{"text":"哪里","is_correct":False},{"text":"多少","is_correct":False}],"explanation":"siapa 意为谁。"},
  {"type":"indo_to_cn","content":"选择正确的中文翻译：\n【 bisa 】","options":[{"text":"会/能（有能力）","is_correct":True},{"text":"可以（被允许）","is_correct":False},{"text":"必须","is_correct":False},{"text":"想要","is_correct":False}],"explanation":"bisa 意为能/会（有能力），boleh 意为可以（被允许）。"}
]

# ── Lesson 5: Negation, karena/bisa/tidak/mau ─────────────────────────────────
lesson_5 = [
  {"type":"vocab_choice","content":"Tidak 是什么意思？","options":[{"text":"不/没","is_correct":True},{"text":"也","is_correct":False},{"text":"已经","is_correct":False},{"text":"还","is_correct":False}],"explanation":"tidak 是印尼语的否定词，相当于中文的不或没，用于否定动词和形容词。"},
  {"type":"vocab_choice","content":"Bukan 和 Tidak 有什么区别？","options":[{"text":"Bukan 否定名词，Tidak 否定动词/形容词","is_correct":True},{"text":"Tidak 否定名词，Bukan 否定动词","is_correct":False},{"text":"两者完全相同","is_correct":False},{"text":"Bukan 更正式","is_correct":False}],"explanation":"Bukan 用于否定名词（Bukan dokter=不是医生），Tidak 用于否定动词/形容词（Tidak baik=不好）。"},
  {"type":"vocab_choice","content":"Karena 是什么意思？","options":[{"text":"因为","is_correct":True},{"text":"所以","is_correct":False},{"text":"但是","is_correct":False},{"text":"如果","is_correct":False}],"explanation":"Karena 意为因为，用于解释原因，如 Karena sakit（因为生病）。"},
  {"type":"vocab_choice","content":"Mau 是什么意思？","options":[{"text":"要/想要","is_correct":True},{"text":"能/会","is_correct":False},{"text":"必须","is_correct":False},{"text":"可以","is_correct":False}],"explanation":"Mau 意为要/想要，表达意愿，如 Saya mau makan（我想吃东西）。"},
  {"type":"vocab_choice","content":"Oke 是什么意思？","options":[{"text":"好的/OK","is_correct":True},{"text":"不","is_correct":False},{"text":"对的","is_correct":False},{"text":"当然","is_correct":False}],"explanation":"Oke 来自英语 OK，意为好的/确定。"},
  {"type":"vocab_choice","content":"Salah 是什么意思？","options":[{"text":"错","is_correct":True},{"text":"对","is_correct":False},{"text":"不好","is_correct":False},{"text":"危险","is_correct":False}],"explanation":"Salah 意为错/错误，与 benar 或 betul（对/正确）相对。"},
  {"type":"vocab_choice","content":"Dia tidak bisa datang. 的意思是？","options":[{"text":"他/她不能来","is_correct":True},{"text":"他/她不来","is_correct":False},{"text":"他/她来不了吗？","is_correct":False},{"text":"他/她没有来","is_correct":False}],"explanation":"tidak + bisa（能）+ datang（来）= 不能来，dia 是第三人称单数他/她。"},
  {"type":"vocab_choice","content":"Datang 是什么意思？","options":[{"text":"来","is_correct":True},{"text":"去","is_correct":False},{"text":"离开","is_correct":False},{"text":"回来","is_correct":False}],"explanation":"datang 意为来，pergi 意为去。"},
  {"type":"vocab_choice","content":"Pergi 是什么意思？","options":[{"text":"去","is_correct":True},{"text":"来","is_correct":False},{"text":"出发","is_correct":False},{"text":"到达","is_correct":False}],"explanation":"pergi 意为去，datang 意为来。"},
  {"type":"vocab_choice","content":"Baik 是什么意思？","options":[{"text":"好","is_correct":True},{"text":"坏","is_correct":False},{"text":"美","is_correct":False},{"text":"大","is_correct":False}],"explanation":"baik 意为好/良好，常用于回答 Apa kabar?（你好吗？）= Baik（很好）。"},
  {"type":"vocab_choice","content":"Kamu benar dan saya salah. 的意思是？","options":[{"text":"你对我错","is_correct":True},{"text":"你错我对","is_correct":False},{"text":"我们都对","is_correct":False},{"text":"你我都错","is_correct":False}],"explanation":"benar（对）dan（和）salah（错），这句话意为你对我错。"},
  {"type":"vocab_choice","content":"dokter 是什么意思？","options":[{"text":"医生","is_correct":True},{"text":"护士","is_correct":False},{"text":"工程师","is_correct":False},{"text":"老师","is_correct":False}],"explanation":"dokter 意为医生，源自英语 doctor。"},
  {"type":"vocab_choice","content":"demam 是什么意思？","options":[{"text":"发烧","is_correct":True},{"text":"咳嗽","is_correct":False},{"text":"头痛","is_correct":False},{"text":"腹泻","is_correct":False}],"explanation":"demam 意为发烧，是工厂医疗场景常见词。"},
  {"type":"vocab_choice","content":"diare 是什么意思？","options":[{"text":"腹泻","is_correct":True},{"text":"发烧","is_correct":False},{"text":"过敏","is_correct":False},{"text":"咳嗽","is_correct":False}],"explanation":"diare 意为腹泻，是医疗场景常见词。"},
  {"type":"vocab_choice","content":"dilarang 是什么意思？","options":[{"text":"禁止","is_correct":True},{"text":"允许","is_correct":False},{"text":"必须","is_correct":False},{"text":"可以","is_correct":False}],"explanation":"dilarang 意为禁止，常见于工厂安全规定，如 Dilarang merokok（禁止吸烟）。"},
  {"type":"cn_to_indo","content":"中文不/没对应的印尼语是？","options":[{"text":"tidak","is_correct":True},{"text":"bukan","is_correct":False},{"text":"jangan","is_correct":False},{"text":"belum","is_correct":False}],"explanation":"tidak 否定动词/形容词，bukan 否定名词。"},
  {"type":"cn_to_indo","content":"中文因为对应的印尼语是？","options":[{"text":"karena","is_correct":True},{"text":"jadi","is_correct":False},{"text":"tetapi","is_correct":False},{"text":"kalau","is_correct":False}],"explanation":"karena 意为因为。"},
  {"type":"cn_to_indo","content":"中文来对应的印尼语是？","options":[{"text":"datang","is_correct":True},{"text":"pergi","is_correct":False},{"text":"pulang","is_correct":False},{"text":"balik","is_correct":False}],"explanation":"datang 意为来，pergi 意为去。"},
  {"type":"cn_to_indo","content":"中文去对应的印尼语是？","options":[{"text":"pergi","is_correct":True},{"text":"datang","is_correct":False},{"text":"pulang","is_correct":False},{"text":"balik","is_correct":False}],"explanation":"pergi 意为去，datang 意为来。"},
  {"type":"cn_to_indo","content":"中文错对应的印尼语是？","options":[{"text":"salah","is_correct":True},{"text":"benar","is_correct":False},{"text":"betul","is_correct":False},{"text":"baik","is_correct":False}],"explanation":"salah 意为错，benar/betul 意为对。"},
  {"type":"cn_to_indo","content":"中文禁止对应的印尼语是？","options":[{"text":"dilarang","is_correct":True},{"text":"tidak boleh","is_correct":False},{"text":"harus","is_correct":False},{"text":"wajib","is_correct":False}],"explanation":"dilarang 意为禁止，工厂安全规定常见词。"},
  {"type":"cn_to_indo","content":"中文发烧对应的印尼语是？","options":[{"text":"demam","is_correct":True},{"text":"batuk","is_correct":False},{"text":"diare","is_correct":False},{"text":"alergi","is_correct":False}],"explanation":"demam 意为发烧。"},
  {"type":"cn_to_indo","content":"中文腹泻对应的印尼语是？","options":[{"text":"diare","is_correct":True},{"text":"demam","is_correct":False},{"text":"batuk","is_correct":False},{"text":"sakit kepala","is_correct":False}],"explanation":"diare 意为腹泻。"},
  {"type":"cn_to_indo","content":"中文医生对应的印尼语是？","options":[{"text":"dokter","is_correct":True},{"text":"perawat","is_correct":False},{"text":"bidan","is_correct":False},{"text":"polisi","is_correct":False}],"explanation":"dokter 意为医生，源自英语 doctor。"},
  {"type":"cn_to_indo","content":"中文在（介词）对应的印尼语是？","options":[{"text":"di","is_correct":True},{"text":"ke","is_correct":False},{"text":"dari","is_correct":False},{"text":"untuk","is_correct":False}],"explanation":"di 是位置介词在，ke 是方向介词去/来，dari 是来源介词从。"},
  {"type":"indo_to_cn","content":"选择正确的中文翻译：\n【 tidak 】","options":[{"text":"不/没","is_correct":True},{"text":"也","is_correct":False},{"text":"已经","is_correct":False},{"text":"很","is_correct":False}],"explanation":"tidak 是否定词不/没。"},
  {"type":"indo_to_cn","content":"选择正确的中文翻译：\n【 karena 】","options":[{"text":"因为","is_correct":True},{"text":"所以","is_correct":False},{"text":"但是","is_correct":False},{"text":"如果","is_correct":False}],"explanation":"karena 意为因为。"},
  {"type":"indo_to_cn","content":"选择正确的中文翻译：\n【 mau 】","options":[{"text":"要/想要","is_correct":True},{"text":"能/会","is_correct":False},{"text":"必须","is_correct":False},{"text":"可以","is_correct":False}],"explanation":"mau 意为要/想要。"},
  {"type":"indo_to_cn","content":"选择正确的中文翻译：\n【 salah 】","options":[{"text":"错","is_correct":True},{"text":"对","is_correct":False},{"text":"不","is_correct":False},{"text":"好","is_correct":False}],"explanation":"salah 意为错误。"},
  {"type":"indo_to_cn","content":"选择正确的中文翻译：\n【 dilarang 】","options":[{"text":"禁止","is_correct":True},{"text":"允许","is_correct":False},{"text":"必须","is_correct":False},{"text":"可以","is_correct":False}],"explanation":"dilarang 意为禁止，常见于安全警示。"},
  {"type":"indo_to_cn","content":"选择正确的中文翻译：\n【 dokter 】","options":[{"text":"医生","is_correct":True},{"text":"护士","is_correct":False},{"text":"工程师","is_correct":False},{"text":"老师","is_correct":False}],"explanation":"dokter 意为医生。"}
]

# Save lessons 3-5
for lid, data in [(3, lesson_3), (4, lesson_4), (5, lesson_5)]:
    path = os.path.join(curated_dir, f'lesson_{lid}.json')
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f'Saved lesson_{lid}.json with {len(data)} questions')

print('Done!')
