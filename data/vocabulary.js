const vocabularyData = [
  {
    "index": "1",
    "kanji": "",
    "reading": "あ",
    "romaji": "a",
    "type": "Expression",
    "meaning": "Ah; oh"
  },
  {
    "index": "2",
    "kanji": "",
    "reading": "ああ",
    "romaji": "aa",
    "type": "Adverb",
    "meaning": "ah; yes"
  },
  {
    "index": "3",
    "kanji": "",
    "reading": "アフリカ",
    "romaji": "afurika",
    "type": "Noun, Katakana",
    "meaning": "Africa"
  },
  {
    "index": "4",
    "kanji": "上がる",
    "reading": "あがる",
    "romaji": "agaru",
    "type": "Verb, Godan verb, Intransitive verb",
    "meaning": "to rise"
  },
  {
    "index": "5",
    "kanji": "挨拶",
    "reading": "あいさつ",
    "romaji": "aisatsu",
    "type": "Noun, Suru verb",
    "meaning": "to greet"
  },
  {
    "index": "6",
    "kanji": "味",
    "reading": "あじ",
    "romaji": "aji",
    "type": "Noun",
    "meaning": "flavor; taste​; uniqueness; attractiveness; experience"
  },
  {
    "index": "7",
    "kanji": "",
    "reading": "アジア",
    "romaji": "ajia",
    "type": "Noun, Katakana",
    "meaning": "Asia"
  },
  {
    "index": "8",
    "kanji": "赤ちゃん",
    "reading": "あかちゃん",
    "romaji": "akachan",
    "type": "Noun",
    "meaning": "baby; infant"
  },
  {
    "index": "9",
    "kanji": "赤ん坊",
    "reading": "あかんぼう",
    "romaji": "akanbou",
    "type": "Noun",
    "meaning": "baby; infant"
  },
  {
    "index": "10",
    "kanji": "",
    "reading": "アクセサリー",
    "romaji": "akusesarii",
    "type": "Noun, Katakana",
    "meaning": "accessory"
  },
  {
    "index": "11",
    "kanji": "",
    "reading": "アメリカ",
    "romaji": "amerika",
    "type": "Noun, Katakana",
    "meaning": "America"
  },
  {
    "index": "12",
    "kanji": "",
    "reading": "アナウンサー",
    "romaji": "anaunsaa",
    "type": "Noun, Katakana",
    "meaning": "announcer"
  },
  {
    "index": "13",
    "kanji": "",
    "reading": "あんな",
    "romaji": "anna",
    "type": "Pre-noun adjectival",
    "meaning": "such"
  },
  {
    "index": "14",
    "kanji": "案内",
    "reading": "あんない",
    "romaji": "annai",
    "type": "Noun, Suru verb",
    "meaning": "to guide"
  },
  {
    "index": "15",
    "kanji": "安心",
    "reading": "あんしん",
    "romaji": "anshin",
    "type": "Noun, Adjective, な-adjective, Suru verb",
    "meaning": "peace of mind"
  },
  {
    "index": "16",
    "kanji": "安全",
    "reading": "あんぜん",
    "romaji": "anzen",
    "type": "Noun, Adjective, な-adjective",
    "meaning": "safety; security​"
  },
  {
    "index": "17",
    "kanji": "",
    "reading": "アルバイト",
    "romaji": "arubaito",
    "type": "Noun, Suru verb, Katakana",
    "meaning": "part-time job"
  },
  {
    "index": "18",
    "kanji": "",
    "reading": "アルコール",
    "romaji": "arukooru",
    "type": "Noun, Katakana",
    "meaning": "alcohol"
  },
  {
    "index": "19",
    "kanji": "浅い",
    "reading": "あさい",
    "romaji": "asai",
    "type": "Adjective, い-adjective",
    "meaning": "shallow"
  },
  {
    "index": "20",
    "kanji": "遊び",
    "reading": "あそび",
    "romaji": "asobi",
    "type": "Noun",
    "meaning": "playing"
  },
  {
    "index": "21",
    "kanji": "集まる",
    "reading": "あつまる",
    "romaji": "atsumaru",
    "type": "Verb, Godan verb, Intransitive verb",
    "meaning": "to gather; to collect; to assemble"
  },
  {
    "index": "22",
    "kanji": "集める",
    "reading": "あつめる",
    "romaji": "atsumeru",
    "type": "Verb, Ichidan verb, Transitive verb",
    "meaning": "to collect; to assemble; to gather"
  },
  {
    "index": "23",
    "kanji": "謝る",
    "reading": "あやまる",
    "romaji": "ayamaru",
    "type": "Verb, Godan verb",
    "meaning": "to apologize"
  },
  {
    "index": "24",
    "kanji": "倍",
    "reading": "ばい",
    "romaji": "bai",
    "type": "Noun",
    "meaning": "double"
  },
  {
    "index": "25",
    "kanji": "番組",
    "reading": "ばんぐみ",
    "romaji": "bangumi",
    "type": "Noun",
    "meaning": "program (e.g. TV)"
  },
  {
    "index": "26",
    "kanji": "場所",
    "reading": "ばしょ",
    "romaji": "basho",
    "type": "Noun",
    "meaning": "place"
  },
  {
    "index": "27",
    "kanji": "",
    "reading": "ベル",
    "romaji": "beru",
    "type": "Noun, Katakana",
    "meaning": "bell"
  },
  {
    "index": "28",
    "kanji": "美術館",
    "reading": "びじゅつかん",
    "romaji": "bijutsukan",
    "type": "Noun",
    "meaning": "art gallery; art museum"
  },
  {
    "index": "29",
    "kanji": "",
    "reading": "びっくり",
    "romaji": "bikkuri",
    "type": "Adverb, Suru verb",
    "meaning": "to be surprised"
  },
  {
    "index": "30",
    "kanji": "",
    "reading": "ビル",
    "romaji": "biru",
    "type": "Noun, Katakana",
    "meaning": "building"
  },
  {
    "index": "31",
    "kanji": "僕",
    "reading": "ぼく",
    "romaji": "boku",
    "type": "Pronoun",
    "meaning": "I (used by males)"
  },
  {
    "index": "32",
    "kanji": "貿易",
    "reading": "ぼうえき",
    "romaji": "boueki",
    "type": "Noun, Suru verb",
    "meaning": "trade"
  },
  {
    "index": "33",
    "kanji": "部長",
    "reading": "ぶちょう",
    "romaji": "buchou",
    "type": "Noun",
    "meaning": "manager; head (chief, director) of a section or department"
  },
  {
    "index": "34",
    "kanji": "",
    "reading": "ぶどう",
    "romaji": "budou",
    "type": "Noun",
    "meaning": "grapes"
  },
  {
    "index": "35",
    "kanji": "文学",
    "reading": "ぶんがく",
    "romaji": "bungaku",
    "type": "Noun",
    "meaning": "literature"
  },
  {
    "index": "36",
    "kanji": "文化",
    "reading": "ぶんか",
    "romaji": "bunka",
    "type": "Noun",
    "meaning": "culture"
  },
  {
    "index": "37",
    "kanji": "文法",
    "reading": "ぶんぽう",
    "romaji": "bunpou",
    "type": "Noun",
    "meaning": "grammar"
  },
  {
    "index": "38",
    "kanji": "",
    "reading": "ちゃん",
    "romaji": "chan",
    "type": "Suffix",
    "meaning": "suffix for familiar female person"
  },
  {
    "index": "39",
    "kanji": "",
    "reading": "チェック",
    "romaji": "chekku",
    "type": "Noun, Suru verb, Katakana",
    "meaning": "to check"
  },
  {
    "index": "40",
    "kanji": "血",
    "reading": "ち",
    "romaji": "chi",
    "type": "Noun",
    "meaning": "blood"
  },
  {
    "index": "41",
    "kanji": "力",
    "reading": "ちから",
    "romaji": "chikara",
    "type": "Noun",
    "meaning": "energy; force; strength; might; power"
  },
  {
    "index": "42",
    "kanji": "地理",
    "reading": "ちり",
    "romaji": "chiri",
    "type": "Noun",
    "meaning": "geography"
  },
  {
    "index": "43",
    "kanji": "中学校",
    "reading": "ちゅうがっこう",
    "romaji": "chuugakkou",
    "type": "Noun",
    "meaning": "junior high school; middle school"
  },
  {
    "index": "44",
    "kanji": "注意",
    "reading": "ちゅうい",
    "romaji": "chuui",
    "type": "Noun, Suru verb",
    "meaning": "caution"
  },
  {
    "index": "45",
    "kanji": "注射",
    "reading": "ちゅうしゃ",
    "romaji": "chuusha",
    "type": "Noun, Suru verb",
    "meaning": "injection"
  },
  {
    "index": "46",
    "kanji": "駐車場",
    "reading": "ちゅうしゃじょう",
    "romaji": "chuushajou",
    "type": "Noun",
    "meaning": "parking lot"
  },
  {
    "index": "47",
    "kanji": "大分",
    "reading": "だいぶ",
    "romaji": "daibu",
    "type": "Adverb",
    "meaning": "considerably; greatly; a lot​"
  },
  {
    "index": "48",
    "kanji": "大学生",
    "reading": "だいがくせい",
    "romaji": "daigakusei",
    "type": "Noun",
    "meaning": "university student; college student"
  },
  {
    "index": "49",
    "kanji": "大事",
    "reading": "だいじ",
    "romaji": "daiji",
    "type": "Adjective, な-adjective",
    "meaning": "important; serious; crucial"
  },
  {
    "index": "50",
    "kanji": "大体",
    "reading": "だいたい",
    "romaji": "daitai",
    "type": "Noun",
    "meaning": "roughly"
  },
  {
    "index": "51",
    "kanji": "暖房",
    "reading": "だんぼう",
    "romaji": "danbou",
    "type": "Noun, Suru verb",
    "meaning": "heating"
  },
  {
    "index": "52",
    "kanji": "男性",
    "reading": "だんせい",
    "romaji": "dansei",
    "type": "Noun",
    "meaning": "man; male"
  },
  {
    "index": "53",
    "kanji": "",
    "reading": "できるだけ",
    "romaji": "dekiru dake",
    "type": "Adverb, Expression",
    "meaning": "as much as possible"
  },
  {
    "index": "54",
    "kanji": "電報",
    "reading": "でんぽう",
    "romaji": "denpou",
    "type": "Noun",
    "meaning": "telegram"
  },
  {
    "index": "55",
    "kanji": "電灯",
    "reading": "でんとう",
    "romaji": "dentou",
    "type": "Noun",
    "meaning": "electric light"
  },
  {
    "index": "56",
    "kanji": "",
    "reading": "どんどん",
    "romaji": "dondon",
    "type": "Adverb",
    "meaning": "rapidly; more and more"
  },
  {
    "index": "57",
    "kanji": "泥棒",
    "reading": "どろぼう",
    "romaji": "dorobou",
    "type": "Noun",
    "meaning": "thief"
  },
  {
    "index": "58",
    "kanji": "動物園",
    "reading": "どうぶつえん",
    "romaji": "doubutsuen",
    "type": "Noun",
    "meaning": "zoo; zoological gardens"
  },
  {
    "index": "59",
    "kanji": "道具",
    "reading": "どうぐ",
    "romaji": "dougu",
    "type": "Noun",
    "meaning": "tool"
  },
  {
    "index": "60",
    "kanji": "枝",
    "reading": "えだ",
    "romaji": "eda",
    "type": "Noun",
    "meaning": "branch"
  },
  {
    "index": "61",
    "kanji": "遠慮",
    "reading": "えんりょ",
    "romaji": "enryo",
    "type": "Noun, Suru verb",
    "meaning": "reserve; refraining"
  },
  {
    "index": "62",
    "kanji": "選ぶ",
    "reading": "えらぶ",
    "romaji": "erabu",
    "type": "Verb, Godan verb, Transitive verb",
    "meaning": "to choose"
  },
  {
    "index": "63",
    "kanji": "",
    "reading": "エスカレーター",
    "romaji": "esukareetaa",
    "type": "Noun, Katakana",
    "meaning": "escalator"
  },
  {
    "index": "64",
    "kanji": "",
    "reading": "ファックス",
    "romaji": "fakkusu",
    "type": "Noun, Suru verb, Katakana",
    "meaning": "fax"
  },
  {
    "index": "65",
    "kanji": "不便",
    "reading": "ふべん",
    "romaji": "fuben",
    "type": "Noun, Adjective, な-adjective",
    "meaning": "inconvenience"
  },
  {
    "index": "66",
    "kanji": "増える",
    "reading": "ふえる",
    "romaji": "fueru",
    "type": "Verb, Ichidan verb, Intransitive verb",
    "meaning": "to increase"
  },
  {
    "index": "67",
    "kanji": "深い",
    "reading": "ふかい",
    "romaji": "fukai",
    "type": "Adjective, い-adjective",
    "meaning": "deep"
  },
  {
    "index": "68",
    "kanji": "復習",
    "reading": "ふくしゅう",
    "romaji": "fukushuu",
    "type": "Noun, Verb, Suru verb",
    "meaning": "review (of learned material); revision"
  },
  {
    "index": "69",
    "kanji": "複雑",
    "reading": "ふくざつ",
    "romaji": "fukuzatsu",
    "type": "Noun, Adjective, な-adjective",
    "meaning": "complexity; complication"
  },
  {
    "index": "70",
    "kanji": "踏む",
    "reading": "ふむ",
    "romaji": "fumu",
    "type": "Verb, Godan verb, Transitive verb",
    "meaning": "to step on"
  },
  {
    "index": "71",
    "kanji": "船",
    "reading": "ふね",
    "romaji": "fune",
    "type": "Noun",
    "meaning": "ship"
  },
  {
    "index": "72",
    "kanji": "降り出す",
    "reading": "ふりだす",
    "romaji": "furidasu",
    "type": "Verb, Godan verb, Intransitive verb",
    "meaning": "to start to rain"
  },
  {
    "index": "73",
    "kanji": "布団",
    "reading": "ふとん",
    "romaji": "futon",
    "type": "Noun",
    "meaning": "Japanese bedding, futon"
  },
  {
    "index": "74",
    "kanji": "太る",
    "reading": "ふとる",
    "romaji": "futoru",
    "type": "Verb, Godan verb, Intransitive verb",
    "meaning": "to become fat"
  },
  {
    "index": "75",
    "kanji": "普通",
    "reading": "ふつう",
    "romaji": "futsuu",
    "type": "Noun, Adverb",
    "meaning": "usually"
  },
  {
    "index": "76",
    "kanji": "",
    "reading": "ガラス",
    "romaji": "garasu",
    "type": "Noun, Katakana",
    "meaning": "a glass"
  },
  {
    "index": "77",
    "kanji": "",
    "reading": "ガソリン",
    "romaji": "gasorin",
    "type": "Noun, Katakana",
    "meaning": "gasoline; petrol"
  },
  {
    "index": "78",
    "kanji": "",
    "reading": "ガソリンスタンド",
    "romaji": "gasorin sutando",
    "type": "Noun, Katakana",
    "meaning": "petrol station"
  },
  {
    "index": "79",
    "kanji": "",
    "reading": "ガス",
    "romaji": "gasu",
    "type": "Noun, Katakana",
    "meaning": "petrol"
  },
  {
    "index": "80",
    "kanji": "原因",
    "reading": "げんいん",
    "romaji": "genin",
    "type": "Noun, Suru verb",
    "meaning": "cause"
  },
  {
    "index": "81",
    "kanji": "下宿",
    "reading": "げしゅく",
    "romaji": "geshuku",
    "type": "Noun, Suru verb",
    "meaning": "lodging"
  },
  {
    "index": "82",
    "kanji": "技術",
    "reading": "ぎじゅつ",
    "romaji": "gijutsu",
    "type": "Noun",
    "meaning": "art,technology,skill"
  },
  {
    "index": "83",
    "kanji": "",
    "reading": "ごちそう",
    "romaji": "gochisou",
    "type": "Noun, Suru verb",
    "meaning": "a feast"
  },
  {
    "index": "84",
    "kanji": "",
    "reading": "ごみ",
    "romaji": "gomi",
    "type": "Noun",
    "meaning": "rubbish"
  },
  {
    "index": "85",
    "kanji": "ご覧になる",
    "reading": "ごらんになる",
    "romaji": "goran ni naru",
    "type": "Verb, Godan verb, Expression",
    "meaning": "(respectful) to see"
  },
  {
    "index": "86",
    "kanji": "ご主人",
    "reading": "ごしゅじん",
    "romaji": "goshujin",
    "type": "Noun",
    "meaning": "your husband; her husband"
  },
  {
    "index": "87",
    "kanji": "ご存じ",
    "reading": "ごぞんじ",
    "romaji": "gozonji",
    "type": "Noun",
    "meaning": "knowing"
  },
  {
    "index": "88",
    "kanji": "具合",
    "reading": "ぐあい",
    "romaji": "guai",
    "type": "Noun",
    "meaning": "condition; health"
  },
  {
    "index": "89",
    "kanji": "葉",
    "reading": "は",
    "romaji": "ha",
    "type": "Noun",
    "meaning": "leaves; leaf"
  },
  {
    "index": "90",
    "kanji": "拝見",
    "reading": "はいけん",
    "romaji": "haiken",
    "type": "Noun, Suru verb",
    "meaning": "seeing; looking at​"
  },
  {
    "index": "91",
    "kanji": "歯医者",
    "reading": "はいしゃ",
    "romaji": "haisha",
    "type": "Noun",
    "meaning": "dentist"
  },
  {
    "index": "92",
    "kanji": "",
    "reading": "はっきり",
    "romaji": "hakkiri",
    "type": "Adverb",
    "meaning": "clearly"
  },
  {
    "index": "93",
    "kanji": "運ぶ",
    "reading": "はこぶ",
    "romaji": "hakobu",
    "type": "Verb, Godan verb, Transitive verb",
    "meaning": "to carry"
  },
  {
    "index": "94",
    "kanji": "花見",
    "reading": "はなみ",
    "romaji": "hanami",
    "type": "Noun, Verb, Suru verb",
    "meaning": "cherry blossom viewing; flower viewing"
  },
  {
    "index": "95",
    "kanji": "",
    "reading": "ハンドバッグ",
    "romaji": "handobaggu",
    "type": "Noun, Katakana",
    "meaning": "handbag"
  },
  {
    "index": "96",
    "kanji": "反対",
    "reading": "はんたい",
    "romaji": "hantai",
    "type": "Noun, Adjective, な-adjective, Suru verb",
    "meaning": "opposition"
  },
  {
    "index": "97",
    "kanji": "払う",
    "reading": "はらう",
    "romaji": "harau",
    "type": "Verb, Godan verb, Transitive verb",
    "meaning": "to pay"
  },
  {
    "index": "98",
    "kanji": "発音",
    "reading": "はつおん",
    "romaji": "hatsuon",
    "type": "Noun, Suru verb",
    "meaning": "pronunciation"
  },
  {
    "index": "99",
    "kanji": "林",
    "reading": "はやし",
    "romaji": "hayashi",
    "type": "Noun",
    "meaning": "woods; forest"
  },
  {
    "index": "100",
    "kanji": "恥ずかしい",
    "reading": "はずかしい",
    "romaji": "hazukashii",
    "type": "#",
    "meaning": "ごい\tVocabulary\tType\tMeaning"
  },
  {
    "index": "101",
    "kanji": "変",
    "reading": "へん",
    "romaji": "hen",
    "type": "Noun, Adjective, な-adjective",
    "meaning": "strange; peculiar; weird"
  },
  {
    "index": "102",
    "kanji": "返事",
    "reading": "へんじ",
    "romaji": "henji",
    "type": "Noun, Suru verb",
    "meaning": "reply; answer; response"
  },
  {
    "index": "103",
    "kanji": "火",
    "reading": "ひ",
    "romaji": "hi",
    "type": "Noun",
    "meaning": "fire"
  },
  {
    "index": "104",
    "kanji": "酷い",
    "reading": "ひどい",
    "romaji": "hidoi",
    "type": "Adjective, い-adjective",
    "meaning": "terrible; awful​"
  },
  {
    "index": "105",
    "kanji": "冷える",
    "reading": "ひえる",
    "romaji": "hieru",
    "type": "Verb, Ichidan verb, Intransitive verb",
    "meaning": "to grow cold"
  },
  {
    "index": "106",
    "kanji": "髭",
    "reading": "ひげ",
    "romaji": "hige",
    "type": "Noun",
    "meaning": "beard"
  },
  {
    "index": "107",
    "kanji": "非常に",
    "reading": "ひじょうに",
    "romaji": "hijou ni",
    "type": "Adverb",
    "meaning": "extremely"
  },
  {
    "index": "108",
    "kanji": "光",
    "reading": "ひかり",
    "romaji": "hikari",
    "type": "Noun",
    "meaning": "light"
  },
  {
    "index": "109",
    "kanji": "光る",
    "reading": "ひかる",
    "romaji": "hikaru",
    "type": "Verb, Godan verb, Intransitive verb",
    "meaning": "to shine"
  },
  {
    "index": "110",
    "kanji": "引き出し",
    "reading": "ひきだし",
    "romaji": "hikidashi",
    "type": "Noun",
    "meaning": "drawer"
  },
  {
    "index": "111",
    "kanji": "引き出す",
    "reading": "ひきだす",
    "romaji": "hikidasu",
    "type": "Verb, Godan verb, Transitive verb",
    "meaning": "to withdraw"
  },
  {
    "index": "112",
    "kanji": "引っ越す",
    "reading": "ひっこす",
    "romaji": "hikkosu",
    "type": "Verb, Godan verb, Intransitive verb",
    "meaning": "to move house"
  },
  {
    "index": "113",
    "kanji": "飛行場",
    "reading": "ひこうじょう",
    "romaji": "hikoujou",
    "type": "Noun",
    "meaning": "airfield; airport"
  },
  {
    "index": "114",
    "kanji": "開く",
    "reading": "ひらく",
    "romaji": "hiraku",
    "type": "Verb, Godan verb, Intransitive verb, Transitive verb",
    "meaning": "to open; to undo; to unseal; to unpack"
  },
  {
    "index": "115",
    "kanji": "拾う",
    "reading": "ひろう",
    "romaji": "hirou",
    "type": "Verb, Godan verb, Transitive verb",
    "meaning": "to pick up"
  },
  {
    "index": "116",
    "kanji": "昼間",
    "reading": "ひるま",
    "romaji": "hiruma",
    "type": "Noun",
    "meaning": "daytime; during the day"
  },
  {
    "index": "117",
    "kanji": "昼休み",
    "reading": "ひるやすみ",
    "romaji": "hiruyasumi",
    "type": "Noun",
    "meaning": "lunch break; noon recess; noon rest period"
  },
  {
    "index": "118",
    "kanji": "久しぶり",
    "reading": "ひさしぶり",
    "romaji": "hisashiburi",
    "type": "Noun, Adjective, な-adjective",
    "meaning": "after a long time"
  },
  {
    "index": "119",
    "kanji": "褒める",
    "reading": "ほめる",
    "romaji": "homeru",
    "type": "Verb, Ichidan verb, Transitive verb",
    "meaning": "to praise"
  },
  {
    "index": "120",
    "kanji": "翻訳",
    "reading": "ほんやく",
    "romaji": "honyaku",
    "type": "Noun, Suru verb",
    "meaning": "translation"
  },
  {
    "index": "121",
    "kanji": "星",
    "reading": "ほし",
    "romaji": "hoshi",
    "type": "Noun",
    "meaning": "star"
  },
  {
    "index": "122",
    "kanji": "",
    "reading": "ほとんど",
    "romaji": "hotondo",
    "type": "Adverbial Noun",
    "meaning": "mostly"
  },
  {
    "index": "123",
    "kanji": "法律",
    "reading": "ほうりつ",
    "romaji": "houritsu",
    "type": "Noun",
    "meaning": "law"
  },
  {
    "index": "124",
    "kanji": "放送",
    "reading": "ほうそう",
    "romaji": "housou",
    "type": "Noun, Suru verb",
    "meaning": "to broadcast"
  },
  {
    "index": "125",
    "kanji": "一度",
    "reading": "いちど",
    "romaji": "ichido",
    "type": "Noun",
    "meaning": "once; one time; on one occasion"
  },
  {
    "index": "126",
    "kanji": "以外",
    "reading": "いがい",
    "romaji": "igai",
    "type": "Noun",
    "meaning": "with the exception of; excepting"
  },
  {
    "index": "127",
    "kanji": "医学",
    "reading": "いがく",
    "romaji": "igaku",
    "type": "Noun",
    "meaning": "medical science; medicine"
  },
  {
    "index": "128",
    "kanji": "",
    "reading": "いじめる",
    "romaji": "ijimeru",
    "type": "Verb, Ichidan verb, Transitive verb",
    "meaning": "to tease"
  },
  {
    "index": "129",
    "kanji": "以上",
    "reading": "いじょう",
    "romaji": "ijou",
    "type": "Noun, Adverbial Noun",
    "meaning": "... and more; ... and upwards​"
  },
  {
    "index": "130",
    "kanji": "以下",
    "reading": "いか",
    "romaji": "ika",
    "type": "Noun",
    "meaning": "not exceeding"
  },
  {
    "index": "131",
    "kanji": "意見",
    "reading": "いけん",
    "romaji": "iken",
    "type": "Noun, Verb, Suru verb",
    "meaning": "opinion; view; comment"
  },
  {
    "index": "132",
    "kanji": "生き物",
    "reading": "いきもの",
    "romaji": "ikimono",
    "type": "Noun",
    "meaning": "living thing"
  },
  {
    "index": "133",
    "kanji": "生きる",
    "reading": "いきる",
    "romaji": "ikiru",
    "type": "Verb, Ichidan verb, Intransitive verb",
    "meaning": "to live"
  },
  {
    "index": "134",
    "kanji": "以内",
    "reading": "いない",
    "romaji": "inai",
    "type": "Noun, Suffix",
    "meaning": "within"
  },
  {
    "index": "135",
    "kanji": "田舎",
    "reading": "いなか",
    "romaji": "inaka",
    "type": "Noun",
    "meaning": "countryside"
  },
  {
    "index": "136",
    "kanji": "祈る",
    "reading": "いのる",
    "romaji": "inoru",
    "type": "Verb, Godan verb, Transitive verb",
    "meaning": "to pray"
  },
  {
    "index": "137",
    "kanji": "",
    "reading": "いっぱい",
    "romaji": "ippai",
    "type": "Noun, Adjective, な-adjective, Adverb",
    "meaning": "full"
  },
  {
    "index": "138",
    "kanji": "色んな",
    "reading": "いろんな",
    "romaji": "ironna",
    "type": "Pre-noun adjectival",
    "meaning": "various"
  },
  {
    "index": "139",
    "kanji": "石",
    "reading": "いし",
    "romaji": "ishi",
    "type": "Noun",
    "meaning": "stone"
  },
  {
    "index": "140",
    "kanji": "急ぐ",
    "reading": "いそぐ",
    "romaji": "isogu",
    "type": "Verb, Godan verb, Intransitive verb",
    "meaning": "to hurry; to rush; to hasten; to make something happen sooner"
  },
  {
    "index": "141",
    "kanji": "一生懸命",
    "reading": "いっしょうけんめい",
    "romaji": "isshoukenmei",
    "type": "Noun, Adverbial Noun, Adjective, な-adjective",
    "meaning": "very hard; with utmost effort"
  },
  {
    "index": "142",
    "kanji": "頂く",
    "reading": "いただく",
    "romaji": "itadaku",
    "type": "Verb, Godan verb, Transitive verb",
    "meaning": "(humble) to receive"
  },
  {
    "index": "143",
    "kanji": "致す",
    "reading": "いたす",
    "romaji": "itasu",
    "type": "Verb, Godan verb, Transitive verb",
    "meaning": "(humble) to do"
  },
  {
    "index": "144",
    "kanji": "糸",
    "reading": "いと",
    "romaji": "ito",
    "type": "Noun",
    "meaning": "thread"
  },
  {
    "index": "145",
    "kanji": "",
    "reading": "ジャム",
    "romaji": "jamu",
    "type": "Noun, Katakana",
    "meaning": "jam"
  },
  {
    "index": "146",
    "kanji": "字",
    "reading": "じ",
    "romaji": "ji",
    "type": "Noun",
    "meaning": "character"
  },
  {
    "index": "147",
    "kanji": "時代",
    "reading": "じだい",
    "romaji": "jidai",
    "type": "Noun",
    "meaning": "period"
  },
  {
    "index": "148",
    "kanji": "事故",
    "reading": "じこ",
    "romaji": "jiko",
    "type": "Noun",
    "meaning": "accident"
  },
  {
    "index": "149",
    "kanji": "事務所",
    "reading": "じむしょ",
    "romaji": "jimusho",
    "type": "Noun",
    "meaning": "office"
  },
  {
    "index": "150",
    "kanji": "神社",
    "reading": "じんじゃ",
    "romaji": "jinja",
    "type": "Noun",
    "meaning": "Shinto shrine"
  },
  {
    "index": "151",
    "kanji": "人口",
    "reading": "じんこう",
    "romaji": "jinkou",
    "type": "Noun",
    "meaning": "population"
  },
  {
    "index": "152",
    "kanji": "人生",
    "reading": "じんせい",
    "romaji": "jinsei",
    "type": "Noun",
    "meaning": "human life"
  },
  {
    "index": "153",
    "kanji": "地震",
    "reading": "じしん",
    "romaji": "jishin",
    "type": "Noun",
    "meaning": "earthquake"
  },
  {
    "index": "154",
    "kanji": "辞典",
    "reading": "じてん",
    "romaji": "jiten",
    "type": "Noun",
    "meaning": "dictionary"
  },
  {
    "index": "155",
    "kanji": "自由",
    "reading": "じゆう",
    "romaji": "jiyuu",
    "type": "Noun, Adjective, な-adjective, Expression",
    "meaning": "freedom"
  },
  {
    "index": "156",
    "kanji": "女性",
    "reading": "じょせい",
    "romaji": "josei",
    "type": "Noun",
    "meaning": "woman; female"
  },
  {
    "index": "157",
    "kanji": "準備",
    "reading": "じゅんび",
    "romaji": "junbi",
    "type": "Noun, Suru verb",
    "meaning": "to prepare"
  },
  {
    "index": "158",
    "kanji": "十分",
    "reading": "じゅうぶん",
    "romaji": "juubun",
    "type": "Noun, Adjective, な-adjective, Adverb",
    "meaning": "enough; sufficient; plenty; adequate; satisfactory"
  },
  {
    "index": "159",
    "kanji": "柔道",
    "reading": "じゅうどう",
    "romaji": "juudou",
    "type": "Noun",
    "meaning": "judo"
  },
  {
    "index": "160",
    "kanji": "住所",
    "reading": "じゅうしょ",
    "romaji": "juusho",
    "type": "Noun",
    "meaning": "address"
  },
  {
    "index": "161",
    "kanji": "",
    "reading": "カーテン",
    "romaji": "kaaten",
    "type": "Noun, Katakana",
    "meaning": "curtain"
  },
  {
    "index": "162",
    "kanji": "壁",
    "reading": "かべ",
    "romaji": "kabe",
    "type": "Noun",
    "meaning": "wall"
  },
  {
    "index": "163",
    "kanji": "課長",
    "reading": "かちょう",
    "romaji": "kachou",
    "type": "Noun",
    "meaning": "section manager; section chief"
  },
  {
    "index": "164",
    "kanji": "帰り",
    "reading": "かえり",
    "romaji": "kaeri",
    "type": "Noun",
    "meaning": "return; coming back"
  },
  {
    "index": "165",
    "kanji": "変える",
    "reading": "かえる",
    "romaji": "kaeru",
    "type": "Verb, Ichidan verb, Transitive verb",
    "meaning": "to change; to transform"
  },
  {
    "index": "166",
    "kanji": "科学",
    "reading": "かがく",
    "romaji": "kagaku",
    "type": "Noun",
    "meaning": "science"
  },
  {
    "index": "167",
    "kanji": "鏡",
    "reading": "かがみ",
    "romaji": "kagami",
    "type": "Noun",
    "meaning": "mirror"
  },
  {
    "index": "168",
    "kanji": "海岸",
    "reading": "かいがん",
    "romaji": "kaigan",
    "type": "Noun",
    "meaning": "coast"
  },
  {
    "index": "169",
    "kanji": "会議",
    "reading": "かいぎ",
    "romaji": "kaigi",
    "type": "Noun, Verb, Suru verb",
    "meaning": "meeting; conference; session; assembly"
  },
  {
    "index": "170",
    "kanji": "会議室",
    "reading": "かいぎしつ",
    "romaji": "kaigishitsu",
    "type": "Noun",
    "meaning": "conference room; conference hall; council room"
  },
  {
    "index": "171",
    "kanji": "会場",
    "reading": "かいじょう",
    "romaji": "kaijou",
    "type": "Noun",
    "meaning": "assembly hall; meeting place; venue; grounds"
  },
  {
    "index": "172",
    "kanji": "会話",
    "reading": "かいわ",
    "romaji": "kaiwa",
    "type": "Noun, Verb, Suru verb",
    "meaning": "conversation"
  },
  {
    "index": "173",
    "kanji": "火事",
    "reading": "かじ",
    "romaji": "kaji",
    "type": "Noun",
    "meaning": "fire"
  },
  {
    "index": "174",
    "kanji": "格好",
    "reading": "かっこう",
    "romaji": "kakkou",
    "type": "Noun",
    "meaning": "appearance"
  },
  {
    "index": "175",
    "kanji": "構う",
    "reading": "かまう",
    "romaji": "kamau",
    "type": "Verb, Godan verb",
    "meaning": "to mind"
  },
  {
    "index": "176",
    "kanji": "髪",
    "reading": "かみ",
    "romaji": "kami",
    "type": "Noun",
    "meaning": "hair"
  },
  {
    "index": "177",
    "kanji": "噛む",
    "reading": "かむ",
    "romaji": "kamu",
    "type": "Verb, Godan verb, Transitive verb",
    "meaning": "to bite,to chew"
  },
  {
    "index": "178",
    "kanji": "家内",
    "reading": "かない",
    "romaji": "kanai",
    "type": "Noun",
    "meaning": "(my) wife; inside the home; one's family"
  },
  {
    "index": "179",
    "kanji": "必ず",
    "reading": "かならず",
    "romaji": "kanarazu",
    "type": "Adverb",
    "meaning": "always; certainly"
  },
  {
    "index": "180",
    "kanji": "悲しい",
    "reading": "かなしい",
    "romaji": "kanashii",
    "type": "Adjective, い-adjective",
    "meaning": "sad"
  },
  {
    "index": "181",
    "kanji": "考える",
    "reading": "かんがえる",
    "romaji": "kangaeru",
    "type": "Verb, Ichidan verb, Transitive verb",
    "meaning": "to think"
  },
  {
    "index": "182",
    "kanji": "看護婦",
    "reading": "かんごふ",
    "romaji": "kangofu",
    "type": "Noun",
    "meaning": "female nurse"
  },
  {
    "index": "183",
    "kanji": "関係",
    "reading": "かんけい",
    "romaji": "kankei",
    "type": "Noun, Suru verb",
    "meaning": "relationship"
  },
  {
    "index": "184",
    "kanji": "彼女",
    "reading": "かのじょ",
    "romaji": "kanojo",
    "type": "Pronoun",
    "meaning": "she; her​"
  },
  {
    "index": "185",
    "kanji": "簡単",
    "reading": "かんたん",
    "romaji": "kantan",
    "type": "Noun, Adjective, な-adjective",
    "meaning": "simple; easy"
  },
  {
    "index": "186",
    "kanji": "彼",
    "reading": "かれ",
    "romaji": "kare",
    "type": "Pronoun",
    "meaning": "he; him​; his"
  },
  {
    "index": "187",
    "kanji": "彼ら",
    "reading": "かれら",
    "romaji": "karera",
    "type": "Pronoun",
    "meaning": "they; them"
  },
  {
    "index": "188",
    "kanji": "形",
    "reading": "かたち",
    "romaji": "katachi",
    "type": "Noun",
    "meaning": "shape"
  },
  {
    "index": "189",
    "kanji": "片付ける",
    "reading": "かたづける",
    "romaji": "katadzukeru",
    "type": "Verb, Ichidan verb, Transitive verb",
    "meaning": "to tidy up"
  },
  {
    "index": "190",
    "kanji": "硬い",
    "reading": "かたい",
    "romaji": "katai",
    "type": "Adjective, い-adjective",
    "meaning": "hard"
  },
  {
    "index": "191",
    "kanji": "勝つ",
    "reading": "かつ",
    "romaji": "katsu",
    "type": "Verb, Godan verb, Intransitive verb",
    "meaning": "to win"
  },
  {
    "index": "192",
    "kanji": "乾く",
    "reading": "かわく",
    "romaji": "kawaku",
    "type": "Verb, Godan verb, Intransitive verb",
    "meaning": "to get dry"
  },
  {
    "index": "193",
    "kanji": "代わり",
    "reading": "かわり",
    "romaji": "kawari",
    "type": "Noun",
    "meaning": "instead; in place"
  },
  {
    "index": "194",
    "kanji": "変わる",
    "reading": "かわる",
    "romaji": "kawaru",
    "type": "Verb, Godan verb, Intransitive verb",
    "meaning": "to change"
  },
  {
    "index": "195",
    "kanji": "通う",
    "reading": "かよう",
    "romaji": "kayou",
    "type": "Verb, Godan verb, Intransitive verb",
    "meaning": "to commute"
  },
  {
    "index": "196",
    "kanji": "飾る",
    "reading": "かざる",
    "romaji": "kazaru",
    "type": "Verb, Godan verb, Transitive verb",
    "meaning": "to decorate"
  },
  {
    "index": "197",
    "kanji": "毛",
    "reading": "け",
    "romaji": "ke",
    "type": "Noun",
    "meaning": "hair or fur"
  },
  {
    "index": "198",
    "kanji": "",
    "reading": "ケーキ",
    "romaji": "keeki",
    "type": "Noun, Katakana",
    "meaning": "cake"
  },
  {
    "index": "199",
    "kanji": "怪我",
    "reading": "けが",
    "romaji": "kega",
    "type": "Noun, Suru verb",
    "meaning": "to injure"
  },
  {
    "index": "200",
    "kanji": "計画",
    "reading": "けいかく",
    "romaji": "keikaku",
    "type": "#",
    "meaning": "ごい\tVocabulary\tType\tMeaning"
  },
  {
    "index": "201",
    "kanji": "経験",
    "reading": "けいけん",
    "romaji": "keiken",
    "type": "Noun, Suru verb",
    "meaning": "to experience"
  },
  {
    "index": "202",
    "kanji": "警察",
    "reading": "けいさつ",
    "romaji": "keisatsu",
    "type": "Noun",
    "meaning": "police"
  },
  {
    "index": "203",
    "kanji": "経済",
    "reading": "けいざい",
    "romaji": "keizai",
    "type": "Noun",
    "meaning": "finance, economy"
  },
  {
    "index": "204",
    "kanji": "見物",
    "reading": "けんぶつ",
    "romaji": "kenbutsu",
    "type": "Noun, Suru verb",
    "meaning": "sightseeing; visit"
  },
  {
    "index": "205",
    "kanji": "喧嘩",
    "reading": "けんか",
    "romaji": "kenka",
    "type": "Noun, Suru verb",
    "meaning": "to quarrel"
  },
  {
    "index": "206",
    "kanji": "研究",
    "reading": "けんきゅう",
    "romaji": "kenkyuu",
    "type": "Noun, Suru verb",
    "meaning": "research"
  },
  {
    "index": "207",
    "kanji": "研究室",
    "reading": "けんきゅうしつ",
    "romaji": "kenkyuushitsu",
    "type": "Noun",
    "meaning": "laboratory"
  },
  {
    "index": "208",
    "kanji": "",
    "reading": "消しゴム",
    "romaji": "keshigomu",
    "type": "Noun",
    "meaning": "eraser"
  },
  {
    "index": "209",
    "kanji": "景色",
    "reading": "けしき",
    "romaji": "keshiki",
    "type": "Noun",
    "meaning": "scenery"
  },
  {
    "index": "210",
    "kanji": "気",
    "reading": "き",
    "romaji": "ki",
    "type": "Noun",
    "meaning": "spirit"
  },
  {
    "index": "211",
    "kanji": "厳しい",
    "reading": "きびしい",
    "romaji": "kibishii",
    "type": "Adjective, い-adjective",
    "meaning": "strict"
  },
  {
    "index": "212",
    "kanji": "気分",
    "reading": "きぶん",
    "romaji": "kibun",
    "type": "Noun",
    "meaning": "feeling; mood"
  },
  {
    "index": "213",
    "kanji": "機会",
    "reading": "きかい",
    "romaji": "kikai",
    "type": "Noun",
    "meaning": "chance; opportunity"
  },
  {
    "index": "214",
    "kanji": "危険",
    "reading": "きけん",
    "romaji": "kiken",
    "type": "Noun, Adjective, な-adjective",
    "meaning": "danger"
  },
  {
    "index": "215",
    "kanji": "聞こえる",
    "reading": "きこえる",
    "romaji": "kikoeru",
    "type": "Verb, Ichidan verb, Intransitive verb",
    "meaning": "to be heard; to be audible; to be said"
  },
  {
    "index": "216",
    "kanji": "決まる",
    "reading": "きまる",
    "romaji": "kimaru",
    "type": "Verb, Godan verb, Intransitive verb",
    "meaning": "to be decided"
  },
  {
    "index": "217",
    "kanji": "決める",
    "reading": "きめる",
    "romaji": "kimeru",
    "type": "Verb, Ichidan verb, Transitive verb",
    "meaning": "to decide"
  },
  {
    "index": "218",
    "kanji": "君",
    "reading": "きみ",
    "romaji": "kimi",
    "type": "Pronoun",
    "meaning": "You"
  },
  {
    "index": "219",
    "kanji": "気持ち",
    "reading": "きもち",
    "romaji": "kimochi",
    "type": "Noun",
    "meaning": "feeling"
  },
  {
    "index": "220",
    "kanji": "着物",
    "reading": "きもの",
    "romaji": "kimono",
    "type": "Noun",
    "meaning": "kimono; Japanese traditional clothing"
  },
  {
    "index": "221",
    "kanji": "近所",
    "reading": "きんじょ",
    "romaji": "kinjo",
    "type": "Noun",
    "meaning": "neighbourhood"
  },
  {
    "index": "222",
    "kanji": "絹",
    "reading": "きぬ",
    "romaji": "kinu",
    "type": "Noun",
    "meaning": "silk"
  },
  {
    "index": "223",
    "kanji": "季節",
    "reading": "きせつ",
    "romaji": "kisetsu",
    "type": "Noun",
    "meaning": "season"
  },
  {
    "index": "224",
    "kanji": "汽車",
    "reading": "きしゃ",
    "romaji": "kisha",
    "type": "Noun",
    "meaning": "train"
  },
  {
    "index": "225",
    "kanji": "規則",
    "reading": "きそく",
    "romaji": "kisoku",
    "type": "Noun",
    "meaning": "rule"
  },
  {
    "index": "226",
    "kanji": "子",
    "reading": "こ",
    "romaji": "ko",
    "type": "Noun",
    "meaning": "child"
  },
  {
    "index": "227",
    "kanji": "心",
    "reading": "こころ",
    "romaji": "kokoro",
    "type": "Noun",
    "meaning": "heart"
  },
  {
    "index": "228",
    "kanji": "国際",
    "reading": "こくさい",
    "romaji": "kokusai",
    "type": "Noun",
    "meaning": "international"
  },
  {
    "index": "229",
    "kanji": "細かい",
    "reading": "こまかい",
    "romaji": "komakai",
    "type": "Adjective, い-adjective",
    "meaning": "small, fine"
  },
  {
    "index": "230",
    "kanji": "米",
    "reading": "こめ",
    "romaji": "kome",
    "type": "Noun",
    "meaning": "(husked grains of) rice"
  },
  {
    "index": "231",
    "kanji": "込む",
    "reading": "こむ",
    "romaji": "komu",
    "type": "Verb, Godan verb, Intransitive verb",
    "meaning": "to be crowded"
  },
  {
    "index": "232",
    "kanji": "今度",
    "reading": "こんど",
    "romaji": "kondo",
    "type": "Noun",
    "meaning": "this time; next time"
  },
  {
    "index": "233",
    "kanji": "この間",
    "reading": "このあいだ",
    "romaji": "kono aida",
    "type": "Adverbial Noun",
    "meaning": "the other day; recently"
  },
  {
    "index": "234",
    "kanji": "",
    "reading": "このごろ",
    "romaji": "kono goro",
    "type": "Adverbial Noun",
    "meaning": "these days; nowadays"
  },
  {
    "index": "235",
    "kanji": "",
    "reading": "コンピュータ",
    "romaji": "konpyuuta",
    "type": "Noun, Katakana",
    "meaning": "computer"
  },
  {
    "index": "236",
    "kanji": "",
    "reading": "コンサート",
    "romaji": "konsaato",
    "type": "Noun, Katakana",
    "meaning": "concert"
  },
  {
    "index": "237",
    "kanji": "今夜",
    "reading": "こんや",
    "romaji": "konya",
    "type": "Noun",
    "meaning": "this evening; tonigh"
  },
  {
    "index": "238",
    "kanji": "",
    "reading": "これから",
    "romaji": "korekara",
    "type": "Conjunction",
    "meaning": "after this"
  },
  {
    "index": "239",
    "kanji": "故障",
    "reading": "こしょう",
    "romaji": "koshou",
    "type": "Noun, Suru verb",
    "meaning": "to break-down"
  },
  {
    "index": "240",
    "kanji": "答え",
    "reading": "こたえ",
    "romaji": "kotae",
    "type": "Noun",
    "meaning": "response"
  },
  {
    "index": "241",
    "kanji": "小鳥",
    "reading": "ことり",
    "romaji": "kotori",
    "type": "Noun",
    "meaning": "small bird"
  },
  {
    "index": "242",
    "kanji": "",
    "reading": "こう",
    "romaji": "kou",
    "type": "Adverb",
    "meaning": "this way"
  },
  {
    "index": "243",
    "kanji": "校長",
    "reading": "こうちょう",
    "romaji": "kouchou",
    "type": "Noun",
    "meaning": "principal; headmaster"
  },
  {
    "index": "244",
    "kanji": "講堂",
    "reading": "こうどう",
    "romaji": "koudou",
    "type": "Noun",
    "meaning": "auditorium"
  },
  {
    "index": "245",
    "kanji": "郊外",
    "reading": "こうがい",
    "romaji": "kougai",
    "type": "Noun",
    "meaning": "suburb; residential area on the outskirt of a city"
  },
  {
    "index": "246",
    "kanji": "講義",
    "reading": "こうぎ",
    "romaji": "kougi",
    "type": "Noun, Suru verb",
    "meaning": "lecture"
  },
  {
    "index": "247",
    "kanji": "工業",
    "reading": "こうぎょう",
    "romaji": "kougyou",
    "type": "Noun",
    "meaning": "industry"
  },
  {
    "index": "248",
    "kanji": "工場",
    "reading": "こうじょう",
    "romaji": "koujou",
    "type": "Noun",
    "meaning": "factory"
  },
  {
    "index": "249",
    "kanji": "高校",
    "reading": "こうこう",
    "romaji": "koukou",
    "type": "Noun",
    "meaning": "senior high school; high school​"
  },
  {
    "index": "250",
    "kanji": "高校生",
    "reading": "こうこうせい",
    "romaji": "koukousei",
    "type": "Noun",
    "meaning": "high school student"
  },
  {
    "index": "251",
    "kanji": "公務員",
    "reading": "こうむいん",
    "romaji": "koumuin",
    "type": "Noun",
    "meaning": "government worker"
  },
  {
    "index": "252",
    "kanji": "高等学校",
    "reading": "こうとうがっこう",
    "romaji": "koutougakkou",
    "type": "Noun",
    "meaning": "high school"
  },
  {
    "index": "253",
    "kanji": "交通",
    "reading": "こうつう",
    "romaji": "koutsuu",
    "type": "Noun",
    "meaning": "traffic"
  },
  {
    "index": "254",
    "kanji": "怖い",
    "reading": "こわい",
    "romaji": "kowai",
    "type": "Adjective, い-adjective",
    "meaning": "frightening"
  },
  {
    "index": "255",
    "kanji": "壊れる",
    "reading": "こわれる",
    "romaji": "kowareru",
    "type": "Verb, Ichidan verb, Intransitive verb",
    "meaning": "to be broken"
  },
  {
    "index": "256",
    "kanji": "壊す",
    "reading": "こわす",
    "romaji": "kowasu",
    "type": "Verb, Godan verb, Transitive verb",
    "meaning": "to break"
  },
  {
    "index": "257",
    "kanji": "首",
    "reading": "くび",
    "romaji": "kubi",
    "type": "Noun",
    "meaning": "neck"
  },
  {
    "index": "258",
    "kanji": "下さる",
    "reading": "くださる",
    "romaji": "kudasaru",
    "type": "Verb, Godan verb",
    "meaning": "(respectful) to give"
  },
  {
    "index": "259",
    "kanji": "雲",
    "reading": "くも",
    "romaji": "kumo",
    "type": "Noun",
    "meaning": "cloud"
  },
  {
    "index": "260",
    "kanji": "君",
    "reading": "くん",
    "romaji": "kun",
    "type": "Suffix",
    "meaning": "suffix for familiar young male"
  },
  {
    "index": "261",
    "kanji": "比べる",
    "reading": "くらべる",
    "romaji": "kuraberu",
    "type": "Verb, Ichidan verb, Transitive verb",
    "meaning": "to compare"
  },
  {
    "index": "262",
    "kanji": "暮れる",
    "reading": "くれる",
    "romaji": "kureru",
    "type": "Verb, Ichidan verb, Intransitive verb",
    "meaning": "to get dark"
  },
  {
    "index": "263",
    "kanji": "草",
    "reading": "くさ",
    "romaji": "kusa",
    "type": "Noun",
    "meaning": "grass"
  },
  {
    "index": "264",
    "kanji": "空気",
    "reading": "くうき",
    "romaji": "kuuki",
    "type": "Noun",
    "meaning": "air"
  },
  {
    "index": "265",
    "kanji": "空港",
    "reading": "くうこう",
    "romaji": "kuukou",
    "type": "Noun",
    "meaning": "airport"
  },
  {
    "index": "266",
    "kanji": "客",
    "reading": "きゃく",
    "romaji": "kyaku",
    "type": "Noun",
    "meaning": "guest; customer"
  },
  {
    "index": "267",
    "kanji": "教育",
    "reading": "きょういく",
    "romaji": "kyouiku",
    "type": "Noun, Suru verb",
    "meaning": "education"
  },
  {
    "index": "268",
    "kanji": "教会",
    "reading": "きょうかい",
    "romaji": "kyoukai",
    "type": "Noun",
    "meaning": "church; congregation; Christian church"
  },
  {
    "index": "269",
    "kanji": "興味",
    "reading": "きょうみ",
    "romaji": "kyoumi",
    "type": "Noun",
    "meaning": "interest (in something); curiosity (about something); zest (for)"
  },
  {
    "index": "270",
    "kanji": "競争",
    "reading": "きょうそう",
    "romaji": "kyousou",
    "type": "Noun, Suru verb",
    "meaning": "competition"
  },
  {
    "index": "271",
    "kanji": "急",
    "reading": "きゅう",
    "romaji": "kyuu",
    "type": "Adjective, な-adjective",
    "meaning": "sudden; abrupt; unexpected"
  },
  {
    "index": "272",
    "kanji": "急行",
    "reading": "きゅうこう",
    "romaji": "kyuukou",
    "type": "Noun, Verb, Suru verb",
    "meaning": "hurrying (to somewhere); rushing; hastening"
  },
  {
    "index": "273",
    "kanji": "間違える",
    "reading": "まちがえる",
    "romaji": "machigaeru",
    "type": "Verb, Ichidan verb, Transitive verb",
    "meaning": "to make a mistake (in)"
  },
  {
    "index": "274",
    "kanji": "参る",
    "reading": "まいる",
    "romaji": "mairu",
    "type": "Verb, Godan verb, Intransitive verb",
    "meaning": "(humble) to go; to come"
  },
  {
    "index": "275",
    "kanji": "負ける",
    "reading": "まける",
    "romaji": "makeru",
    "type": "Verb, Ichidan verb, Intransitive verb",
    "meaning": "to lose"
  },
  {
    "index": "276",
    "kanji": "漫画",
    "reading": "まんが",
    "romaji": "manga",
    "type": "Noun",
    "meaning": "comic"
  },
  {
    "index": "277",
    "kanji": "間に合う",
    "reading": "まにあう",
    "romaji": "maniau",
    "type": "Verb, Godan verb, Intransitive verb",
    "meaning": "to be in time (for)"
  },
  {
    "index": "278",
    "kanji": "真ん中",
    "reading": "まんなか",
    "romaji": "mannaka",
    "type": "Noun",
    "meaning": "middle; centre; center"
  },
  {
    "index": "279",
    "kanji": "周り",
    "reading": "まわり",
    "romaji": "mawari",
    "type": "Noun",
    "meaning": "around"
  },
  {
    "index": "280",
    "kanji": "回る",
    "reading": "まわる",
    "romaji": "mawaru",
    "type": "Verb, Godan verb, Intransitive verb",
    "meaning": "to go around"
  },
  {
    "index": "281",
    "kanji": "",
    "reading": "まず",
    "romaji": "mazu",
    "type": "Adverb",
    "meaning": "first of all"
  },
  {
    "index": "282",
    "kanji": "召し上がる",
    "reading": "めしあがる",
    "romaji": "meshiagaru",
    "type": "Verb, Godan verb, Transitive verb",
    "meaning": "to eat; to drink​"
  },
  {
    "index": "283",
    "kanji": "珍しい",
    "reading": "めずらしい",
    "romaji": "mezurashii",
    "type": "Adjective, い-adjective",
    "meaning": "unusual; rare"
  },
  {
    "index": "284",
    "kanji": "見える",
    "reading": "みえる",
    "romaji": "mieru",
    "type": "Verb, Ichidan verb, Intransitive verb",
    "meaning": "to be seen; to be in sight; to look; to seem"
  },
  {
    "index": "285",
    "kanji": "港",
    "reading": "みなと",
    "romaji": "minato",
    "type": "Noun",
    "meaning": "harbour"
  },
  {
    "index": "286",
    "kanji": "味噌",
    "reading": "みそ",
    "romaji": "miso",
    "type": "Noun",
    "meaning": "fermented condiment made from soybeans"
  },
  {
    "index": "287",
    "kanji": "見つかる",
    "reading": "みつかる",
    "romaji": "mitsukaru",
    "type": "Verb, Godan verb, Intransitive verb",
    "meaning": "to be found; to be discovered"
  },
  {
    "index": "288",
    "kanji": "見つける",
    "reading": "みつける",
    "romaji": "mitsukeru",
    "type": "Verb, Ichidan verb, Transitive verb",
    "meaning": "to discover; to find; to come across; to detect; to spot"
  },
  {
    "index": "289",
    "kanji": "都",
    "reading": "みやこ",
    "romaji": "miyako",
    "type": "Noun",
    "meaning": "capital"
  },
  {
    "index": "290",
    "kanji": "湖",
    "reading": "みずうみ",
    "romaji": "mizuumi",
    "type": "Noun",
    "meaning": "lake"
  },
  {
    "index": "291",
    "kanji": "戻る",
    "reading": "もどる",
    "romaji": "modoru",
    "type": "Verb, Godan verb, Intransitive verb",
    "meaning": "to turn back"
  },
  {
    "index": "292",
    "kanji": "木綿",
    "reading": "もめん",
    "romaji": "momen",
    "type": "Noun",
    "meaning": "cotton (material)"
  },
  {
    "index": "293",
    "kanji": "森",
    "reading": "もり",
    "romaji": "mori",
    "type": "Noun",
    "meaning": "forest"
  },
  {
    "index": "294",
    "kanji": "",
    "reading": "もし",
    "romaji": "moshi",
    "type": "Adverb",
    "meaning": "if; in case; supposing"
  },
  {
    "index": "295",
    "kanji": "申し上げる",
    "reading": "もうしあげる",
    "romaji": "moushiageru",
    "type": "Verb, Ichidan verb, Transitive verb",
    "meaning": "to say; to offer"
  },
  {
    "index": "296",
    "kanji": "申す",
    "reading": "もうす",
    "romaji": "mousu",
    "type": "Verb, Godan verb, Transitive verb",
    "meaning": "to be called; to say"
  },
  {
    "index": "297",
    "kanji": "",
    "reading": "もうすぐ",
    "romaji": "mousugu",
    "type": "Adverb, Expression",
    "meaning": "soon"
  },
  {
    "index": "298",
    "kanji": "迎える",
    "reading": "むかえる",
    "romaji": "mukaeru",
    "type": "Verb, Ichidan verb, Transitive verb",
    "meaning": "to go out to meet"
  },
  {
    "index": "299",
    "kanji": "昔",
    "reading": "むかし",
    "romaji": "mukashi",
    "type": "Noun, Adverbial noun",
    "meaning": "olden days, former"
  },
  {
    "index": "300",
    "kanji": "向かう",
    "reading": "むかう",
    "romaji": "mukau",
    "type": "#",
    "meaning": "ごい\tVocabulary\tType\tMeaning"
  },
  {
    "index": "301",
    "kanji": "無理",
    "reading": "むり",
    "romaji": "muri",
    "type": "Noun, Adjective, な-adjective, Suru verb",
    "meaning": "impossible"
  },
  {
    "index": "302",
    "kanji": "虫",
    "reading": "むし",
    "romaji": "mushi",
    "type": "Noun",
    "meaning": "insect"
  },
  {
    "index": "303",
    "kanji": "息子",
    "reading": "むすこ",
    "romaji": "musuko",
    "type": "Noun",
    "meaning": "son"
  },
  {
    "index": "304",
    "kanji": "娘",
    "reading": "むすめ",
    "romaji": "musume",
    "type": "Noun",
    "meaning": "daughter"
  },
  {
    "index": "305",
    "kanji": "投げる",
    "reading": "なげる",
    "romaji": "nageru",
    "type": "Verb, Ichidan verb, Transitive verb",
    "meaning": "to throw or cast away"
  },
  {
    "index": "306",
    "kanji": "泣く",
    "reading": "なく",
    "romaji": "naku",
    "type": "Verb, Godan verb",
    "meaning": "to weep"
  },
  {
    "index": "307",
    "kanji": "無くなる",
    "reading": "なくなる",
    "romaji": "naku naru",
    "type": "Verb, Godan verb, Intransitive verb",
    "meaning": "to disappear; to get lost"
  },
  {
    "index": "308",
    "kanji": "亡くなる",
    "reading": "なくなる",
    "romaji": "nakunaru",
    "type": "Verb, Godan verb, Intransitive verb",
    "meaning": "to die"
  },
  {
    "index": "309",
    "kanji": "生",
    "reading": "なま",
    "romaji": "nama",
    "type": "Noun, Prefix",
    "meaning": "raw"
  },
  {
    "index": "310",
    "kanji": "直る",
    "reading": "なおる",
    "romaji": "naoru",
    "type": "Verb, Godan verb, Intransitive verb",
    "meaning": "to be fixed,to be repaired"
  },
  {
    "index": "311",
    "kanji": "治る",
    "reading": "なおる",
    "romaji": "naoru",
    "type": "Verb, Godan verb, Intransitive verb",
    "meaning": "to be cured; to heal"
  },
  {
    "index": "312",
    "kanji": "慣れる",
    "reading": "なれる",
    "romaji": "nareru",
    "type": "Verb, Ichidan verb, Intransitive verb",
    "meaning": "to get used to"
  },
  {
    "index": "313",
    "kanji": "鳴る",
    "reading": "なる",
    "romaji": "naru",
    "type": "Verb, Godan verb, Intransitive verb",
    "meaning": "to sound"
  },
  {
    "index": "314",
    "kanji": "",
    "reading": "なるほど",
    "romaji": "naruhodo",
    "type": "Adverb, Expression",
    "meaning": "now I understand"
  },
  {
    "index": "315",
    "kanji": "寝坊",
    "reading": "ねぼう",
    "romaji": "nebou",
    "type": "Noun, Verb, Suru verb",
    "meaning": "sleeping in late; oversleeping"
  },
  {
    "index": "316",
    "kanji": "値段",
    "reading": "ねだん",
    "romaji": "nedan",
    "type": "Noun",
    "meaning": "price; cost"
  },
  {
    "index": "317",
    "kanji": "眠い",
    "reading": "ねむい",
    "romaji": "nemui",
    "type": "Adjective, い-adjective",
    "meaning": "sleepy"
  },
  {
    "index": "318",
    "kanji": "眠る",
    "reading": "ねむる",
    "romaji": "nemuru",
    "type": "Verb, Godan verb, Intransitive verb",
    "meaning": "to sleep"
  },
  {
    "index": "319",
    "kanji": "熱",
    "reading": "ねつ",
    "romaji": "netsu",
    "type": "Noun",
    "meaning": "fever"
  },
  {
    "index": "320",
    "kanji": "苦い",
    "reading": "にがい",
    "romaji": "nigai",
    "type": "Adjective, い-adjective",
    "meaning": "bitter"
  },
  {
    "index": "321",
    "kanji": "逃げる",
    "reading": "にげる",
    "romaji": "nigeru",
    "type": "Verb, Ichidan verb, Intransitive verb",
    "meaning": "to escape"
  },
  {
    "index": "322",
    "kanji": "二階建て",
    "reading": "にかいだて",
    "romaji": "nikaidate",
    "type": "Noun",
    "meaning": "two-storied building"
  },
  {
    "index": "323",
    "kanji": "人形",
    "reading": "にんぎょう",
    "romaji": "ningyou",
    "type": "Noun",
    "meaning": "doll"
  },
  {
    "index": "324",
    "kanji": "匂い",
    "reading": "におい",
    "romaji": "nioi",
    "type": "Noun",
    "meaning": "a smell"
  },
  {
    "index": "325",
    "kanji": "似る",
    "reading": "にる",
    "romaji": "niru",
    "type": "Verb, Ichidan verb, Intransitive verb",
    "meaning": "to be similar"
  },
  {
    "index": "326",
    "kanji": "喉",
    "reading": "のど",
    "romaji": "nodo",
    "type": "Noun",
    "meaning": "throat"
  },
  {
    "index": "327",
    "kanji": "残る",
    "reading": "のこる",
    "romaji": "nokoru",
    "type": "Verb, Godan verb, Intransitive verb",
    "meaning": "to remain"
  },
  {
    "index": "328",
    "kanji": "乗り換える",
    "reading": "のりかえる",
    "romaji": "norikaeru",
    "type": "Verb, Ichidan verb, Transitive verb",
    "meaning": "to change between buses or trains"
  },
  {
    "index": "329",
    "kanji": "乗り物",
    "reading": "のりもの",
    "romaji": "norimono",
    "type": "Noun",
    "meaning": "vehicle"
  },
  {
    "index": "330",
    "kanji": "濡れる",
    "reading": "ぬれる",
    "romaji": "nureru",
    "type": "Verb, Ichidan verb, Intransitive verb",
    "meaning": "to get wet"
  },
  {
    "index": "331",
    "kanji": "塗る",
    "reading": "ぬる",
    "romaji": "nuru",
    "type": "Verb, Godan verb, Transitive verb",
    "meaning": "to paint; to plaster"
  },
  {
    "index": "332",
    "kanji": "盗む",
    "reading": "ぬすむ",
    "romaji": "nusumu",
    "type": "Verb, Godan verb, Transitive verb",
    "meaning": "to steal"
  },
  {
    "index": "333",
    "kanji": "入学",
    "reading": "にゅうがく",
    "romaji": "nyuugaku",
    "type": "Noun, Verb, Suru verb",
    "meaning": "entry to school or university; enrollment"
  },
  {
    "index": "334",
    "kanji": "入院",
    "reading": "にゅういん",
    "romaji": "nyuuin",
    "type": "Noun, Verb, Suru verb",
    "meaning": "hospitalization"
  },
  {
    "index": "335",
    "kanji": "落ちる",
    "reading": "おちる",
    "romaji": "ochiru",
    "type": "Verb, Ichidan verb, Intransitive verb",
    "meaning": "to fall or drop"
  },
  {
    "index": "336",
    "kanji": "踊り",
    "reading": "おどり",
    "romaji": "odori",
    "type": "Noun",
    "meaning": "a dance"
  },
  {
    "index": "337",
    "kanji": "驚く",
    "reading": "おどろく",
    "romaji": "odoroku",
    "type": "Verb, Godan verb, Intransitive verb",
    "meaning": "to be surprised"
  },
  {
    "index": "338",
    "kanji": "踊る",
    "reading": "おどる",
    "romaji": "odoru",
    "type": "Verb, Godan verb, Intransitive verb",
    "meaning": "to dance"
  },
  {
    "index": "339",
    "kanji": "お出でになる",
    "reading": "おいでになる",
    "romaji": "oide ni naru",
    "type": "Verb, Godan verb, Expression",
    "meaning": "(respectful) to be"
  },
  {
    "index": "340",
    "kanji": "お祝い",
    "reading": "おいわい",
    "romaji": "oiwai",
    "type": "Noun, Suru verb",
    "meaning": "congratulation"
  },
  {
    "index": "341",
    "kanji": "お嬢さん",
    "reading": "おじょうさん",
    "romaji": "ojousan",
    "type": "Noun",
    "meaning": "(another's) daughter"
  },
  {
    "index": "342",
    "kanji": "可笑しい",
    "reading": "おかしい",
    "romaji": "okashii",
    "type": "Adjective, い-adjective",
    "meaning": "strange or funny"
  },
  {
    "index": "343",
    "kanji": "行う",
    "reading": "おこなう",
    "romaji": "okonau",
    "type": "Verb, Godan verb, Transitive verb",
    "meaning": "to perform; to do; to carry out"
  },
  {
    "index": "344",
    "kanji": "怒る",
    "reading": "おこる",
    "romaji": "okoru",
    "type": "Verb, Godan verb, Intransitive verb",
    "meaning": "to be angry"
  },
  {
    "index": "345",
    "kanji": "起こす",
    "reading": "おこす",
    "romaji": "okosu",
    "type": "Verb, Godan verb, Transitive verb",
    "meaning": "to wake"
  },
  {
    "index": "346",
    "kanji": "億",
    "reading": "おく",
    "romaji": "oku",
    "type": "Numeric",
    "meaning": "one hundred million"
  },
  {
    "index": "347",
    "kanji": "屋上",
    "reading": "おくじょう",
    "romaji": "okujou",
    "type": "Noun",
    "meaning": "rooftop​"
  },
  {
    "index": "348",
    "kanji": "遅れる",
    "reading": "おくれる",
    "romaji": "okureru",
    "type": "Verb, Ichidan verb, Intransitive verb",
    "meaning": "to be late"
  },
  {
    "index": "349",
    "kanji": "贈り物",
    "reading": "おくりもの",
    "romaji": "okurimono",
    "type": "Noun",
    "meaning": "present; gift"
  },
  {
    "index": "350",
    "kanji": "送る",
    "reading": "おくる",
    "romaji": "okuru",
    "type": "Verb, Godan verb, Transitive verb",
    "meaning": "to send"
  },
  {
    "index": "351",
    "kanji": "お祭り",
    "reading": "おまつり",
    "romaji": "omatsuri",
    "type": "Noun",
    "meaning": "festival"
  },
  {
    "index": "352",
    "kanji": "お見舞い",
    "reading": "おみまい",
    "romaji": "omimai",
    "type": "Noun",
    "meaning": "visiting ill or distressed people"
  },
  {
    "index": "353",
    "kanji": "お土産",
    "reading": "おみやげ",
    "romaji": "omiyage",
    "type": "Noun",
    "meaning": "souvenir"
  },
  {
    "index": "354",
    "kanji": "",
    "reading": "おもちゃ",
    "romaji": "omocha",
    "type": "Noun",
    "meaning": "toy"
  },
  {
    "index": "355",
    "kanji": "思い出す",
    "reading": "おもいだす",
    "romaji": "omoidasu",
    "type": "Verb, Godan verb, Transitive verb",
    "meaning": "to remember"
  },
  {
    "index": "356",
    "kanji": "表",
    "reading": "おもて",
    "romaji": "omote",
    "type": "Noun",
    "meaning": "the front"
  },
  {
    "index": "357",
    "kanji": "",
    "reading": "オートバイ",
    "romaji": "ootobai",
    "type": "Noun, Katakana",
    "meaning": "motorcycle"
  },
  {
    "index": "358",
    "kanji": "お礼",
    "reading": "おれい",
    "romaji": "orei",
    "type": "Noun",
    "meaning": "thanks"
  },
  {
    "index": "359",
    "kanji": "折れる",
    "reading": "おれる",
    "romaji": "oreru",
    "type": "Verb, Ichidan verb, Intransitive verb",
    "meaning": "to break; to be broken"
  },
  {
    "index": "360",
    "kanji": "下りる",
    "reading": "おりる",
    "romaji": "oriru",
    "type": "Verb, Ichidan verb, Intransitive verb",
    "meaning": "to get off"
  },
  {
    "index": "361",
    "kanji": "折る",
    "reading": "おる",
    "romaji": "oru",
    "type": "Verb, Godan verb, Transitive verb",
    "meaning": "to break or to fold"
  },
  {
    "index": "362",
    "kanji": "押し入れ",
    "reading": "おしいれ",
    "romaji": "oshiire",
    "type": "Noun",
    "meaning": "closet"
  },
  {
    "index": "363",
    "kanji": "仰る",
    "reading": "おっしゃる",
    "romaji": "ossharu",
    "type": "Verb, Godan verb, Transitive verb",
    "meaning": "(respectful) to say"
  },
  {
    "index": "364",
    "kanji": "お宅",
    "reading": "おたく",
    "romaji": "otaku",
    "type": "Noun",
    "meaning": "your home"
  },
  {
    "index": "365",
    "kanji": "音",
    "reading": "おと",
    "romaji": "oto",
    "type": "Noun",
    "meaning": "sound; note"
  },
  {
    "index": "366",
    "kanji": "落とす",
    "reading": "おとす",
    "romaji": "otosu",
    "type": "Verb, Godan verb, Transitive verb",
    "meaning": "to drop"
  },
  {
    "index": "367",
    "kanji": "お釣り",
    "reading": "おつり",
    "romaji": "otsuri",
    "type": "Noun",
    "meaning": "change (for a purchase)​"
  },
  {
    "index": "368",
    "kanji": "夫",
    "reading": "おっと",
    "romaji": "otto",
    "type": "Noun",
    "meaning": "husband"
  },
  {
    "index": "369",
    "kanji": "終わり",
    "reading": "おわり",
    "romaji": "owari",
    "type": "Noun",
    "meaning": "the end"
  },
  {
    "index": "370",
    "kanji": "親",
    "reading": "おや",
    "romaji": "oya",
    "type": "Noun",
    "meaning": "parents"
  },
  {
    "index": "371",
    "kanji": "泳ぎ方",
    "reading": "およぎかた",
    "romaji": "oyogikata",
    "type": "Noun",
    "meaning": "way of swimming"
  },
  {
    "index": "372",
    "kanji": "",
    "reading": "パート",
    "romaji": "paato",
    "type": "Noun, Katakana",
    "meaning": "part; part time"
  },
  {
    "index": "373",
    "kanji": "",
    "reading": "パソコン",
    "romaji": "pasokon",
    "type": "Noun, Katakana",
    "meaning": "personal computer"
  },
  {
    "index": "374",
    "kanji": "",
    "reading": "ピアノ",
    "romaji": "piano",
    "type": "Noun, Katakana",
    "meaning": "piano"
  },
  {
    "index": "375",
    "kanji": "",
    "reading": "プレゼント",
    "romaji": "purezento",
    "type": "Noun, Katakana",
    "meaning": "present; gift"
  },
  {
    "index": "376",
    "kanji": "冷房",
    "reading": "れいぼう",
    "romaji": "reibou",
    "type": "Noun, Suru verb",
    "meaning": "air conditioning"
  },
  {
    "index": "377",
    "kanji": "",
    "reading": "レジ",
    "romaji": "reji",
    "type": "Noun, Katakana",
    "meaning": "cashier​"
  },
  {
    "index": "378",
    "kanji": "歴史",
    "reading": "れきし",
    "romaji": "rekishi",
    "type": "Noun",
    "meaning": "history"
  },
  {
    "index": "379",
    "kanji": "連絡",
    "reading": "れんらく",
    "romaji": "renraku",
    "type": "Suru verb",
    "meaning": "to contact; to get in touch​"
  },
  {
    "index": "380",
    "kanji": "",
    "reading": "レポート",
    "romaji": "repooto",
    "type": "Noun, Katakana",
    "meaning": "report"
  },
  {
    "index": "381",
    "kanji": "利用",
    "reading": "りよう",
    "romaji": "riyou",
    "type": "Noun, Verb, Suru verb",
    "meaning": "use; utilization; application"
  },
  {
    "index": "382",
    "kanji": "理由",
    "reading": "りゆう",
    "romaji": "riyuu",
    "type": "Noun",
    "meaning": "reason"
  },
  {
    "index": "383",
    "kanji": "留守",
    "reading": "るす",
    "romaji": "rusu",
    "type": "Noun, Suru verb",
    "meaning": "absence"
  },
  {
    "index": "384",
    "kanji": "旅館",
    "reading": "りょかん",
    "romaji": "ryokan",
    "type": "Noun",
    "meaning": "traditional inn; Japanese-style lodging"
  },
  {
    "index": "385",
    "kanji": "両方",
    "reading": "りょうほう",
    "romaji": "ryouhou",
    "type": "Noun",
    "meaning": "both sides"
  },
  {
    "index": "386",
    "kanji": "寂しい",
    "reading": "さびしい",
    "romaji": "sabishii",
    "type": "Adjective, い-adjective",
    "meaning": "lonely"
  },
  {
    "index": "387",
    "kanji": "下がる",
    "reading": "さがる",
    "romaji": "sagaru",
    "type": "Verb, Godan verb, Intransitive verb",
    "meaning": "to get down"
  },
  {
    "index": "388",
    "kanji": "探す",
    "reading": "さがす",
    "romaji": "sagasu",
    "type": "Verb, Godan verb, Transitive verb",
    "meaning": "to look for"
  },
  {
    "index": "389",
    "kanji": "下げる",
    "reading": "さげる",
    "romaji": "sageru",
    "type": "Verb, Ichidan verb, Transitive verb",
    "meaning": "to lower"
  },
  {
    "index": "390",
    "kanji": "最後",
    "reading": "さいご",
    "romaji": "saigo",
    "type": "Noun",
    "meaning": "end; last"
  },
  {
    "index": "391",
    "kanji": "最近",
    "reading": "さいきん",
    "romaji": "saikin",
    "type": "Noun, Adverbial Noun",
    "meaning": "recently"
  },
  {
    "index": "392",
    "kanji": "最初",
    "reading": "さいしょ",
    "romaji": "saisho",
    "type": "Noun, Adverbial Noun",
    "meaning": "beginning; first"
  },
  {
    "index": "393",
    "kanji": "坂",
    "reading": "さか",
    "romaji": "saka",
    "type": "Noun",
    "meaning": "slope; hill"
  },
  {
    "index": "394",
    "kanji": "盛ん",
    "reading": "さかん",
    "romaji": "sakan",
    "type": "Adjective, な-adjective",
    "meaning": "popularity; prosperous"
  },
  {
    "index": "395",
    "kanji": "昨夜",
    "reading": "さくや",
    "romaji": "sakuya",
    "type": "Noun, Adverbial Noun",
    "meaning": "last night"
  },
  {
    "index": "396",
    "kanji": "",
    "reading": "サンダル",
    "romaji": "sandaru",
    "type": "Noun, Katakana",
    "meaning": "sandal"
  },
  {
    "index": "397",
    "kanji": "",
    "reading": "サンドイッチ",
    "romaji": "sandoicchi",
    "type": "Noun, Katakana",
    "meaning": "sandwich"
  },
  {
    "index": "398",
    "kanji": "産業",
    "reading": "さんぎょう",
    "romaji": "sangyou",
    "type": "Noun",
    "meaning": "industry"
  },
  {
    "index": "399",
    "kanji": "",
    "reading": "サラダ",
    "romaji": "sarada",
    "type": "Noun, Katakana",
    "meaning": "salad"
  },
  {
    "index": "400",
    "kanji": "再来月",
    "reading": "さらいげつ",
    "romaji": "saraigetsu",
    "type": "#",
    "meaning": "ごい\tVocabulary\tType\tMeaning"
  },
  {
    "index": "401",
    "kanji": "再来週",
    "reading": "さらいしゅう",
    "romaji": "saraishuu",
    "type": "Noun, Adverbial Noun",
    "meaning": "week after next"
  },
  {
    "index": "402",
    "kanji": "差し上げる",
    "reading": "さしあげる",
    "romaji": "sashiageru",
    "type": "Verb, Ichidan verb, Transitive verb",
    "meaning": "to give"
  },
  {
    "index": "403",
    "kanji": "騒ぐ",
    "reading": "さわぐ",
    "romaji": "sawagu",
    "type": "Verb, Godan verb, Intransitive verb",
    "meaning": "to make noise,to be excited"
  },
  {
    "index": "404",
    "kanji": "触る",
    "reading": "さわる",
    "romaji": "sawaru",
    "type": "Verb, Godan verb, Intransitive verb",
    "meaning": "to touch"
  },
  {
    "index": "405",
    "kanji": "生物",
    "reading": "せいぶつ",
    "romaji": "seibutsu",
    "type": "Noun",
    "meaning": "living thing"
  },
  {
    "index": "406",
    "kanji": "政治",
    "reading": "せいじ",
    "romaji": "seiji",
    "type": "Noun",
    "meaning": "politics"
  },
  {
    "index": "407",
    "kanji": "生活",
    "reading": "せいかつ",
    "romaji": "seikatsu",
    "type": "Noun, Suru verb",
    "meaning": "to live"
  },
  {
    "index": "408",
    "kanji": "生命",
    "reading": "せいめい",
    "romaji": "seimei",
    "type": "Noun",
    "meaning": "life"
  },
  {
    "index": "409",
    "kanji": "生産",
    "reading": "せいさん",
    "romaji": "seisan",
    "type": "Noun, Suru verb",
    "meaning": "production"
  },
  {
    "index": "410",
    "kanji": "西洋",
    "reading": "せいよう",
    "romaji": "seiyou",
    "type": "Noun",
    "meaning": "the west; Western countries"
  },
  {
    "index": "411",
    "kanji": "世界",
    "reading": "せかい",
    "romaji": "sekai",
    "type": "Noun",
    "meaning": "the world"
  },
  {
    "index": "412",
    "kanji": "席",
    "reading": "せき",
    "romaji": "seki",
    "type": "Noun",
    "meaning": "seat"
  },
  {
    "index": "413",
    "kanji": "線",
    "reading": "せん",
    "romaji": "sen",
    "type": "Noun",
    "meaning": "line"
  },
  {
    "index": "414",
    "kanji": "背中",
    "reading": "せなか",
    "romaji": "senaka",
    "type": "Noun",
    "meaning": "back (of body)"
  },
  {
    "index": "415",
    "kanji": "先輩",
    "reading": "せんぱい",
    "romaji": "senpai",
    "type": "Noun",
    "meaning": "senior"
  },
  {
    "index": "416",
    "kanji": "戦争",
    "reading": "せんそう",
    "romaji": "sensou",
    "type": "Noun, Suru verb",
    "meaning": "war"
  },
  {
    "index": "417",
    "kanji": "説明",
    "reading": "せつめい",
    "romaji": "setsumei",
    "type": "Noun, Verb, Suru verb",
    "meaning": "explanation"
  },
  {
    "index": "418",
    "kanji": "社長",
    "reading": "しゃちょう",
    "romaji": "shachou",
    "type": "Noun",
    "meaning": "company president; manager; director"
  },
  {
    "index": "419",
    "kanji": "社会",
    "reading": "しゃかい",
    "romaji": "shakai",
    "type": "Noun",
    "meaning": "society; public; community; the world"
  },
  {
    "index": "420",
    "kanji": "市",
    "reading": "し",
    "romaji": "shi",
    "type": "Noun",
    "meaning": "city"
  },
  {
    "index": "421",
    "kanji": "試合",
    "reading": "しあい",
    "romaji": "shiai",
    "type": "Noun, Suru verb",
    "meaning": "match,game"
  },
  {
    "index": "422",
    "kanji": "叱る",
    "reading": "しかる",
    "romaji": "shikaru",
    "type": "Verb, Godan verb, Transitive verb",
    "meaning": "to scold"
  },
  {
    "index": "423",
    "kanji": "仕方",
    "reading": "しかた",
    "romaji": "shikata",
    "type": "Noun",
    "meaning": "way; method"
  },
  {
    "index": "424",
    "kanji": "試験",
    "reading": "しけん",
    "romaji": "shiken",
    "type": "Noun, Suru verb",
    "meaning": "examination"
  },
  {
    "index": "425",
    "kanji": "",
    "reading": "しっかり",
    "romaji": "shikkari",
    "type": "Adverb, Suru verb",
    "meaning": "firmly; steadily"
  },
  {
    "index": "426",
    "kanji": "島",
    "reading": "しま",
    "romaji": "shima",
    "type": "Noun",
    "meaning": "island"
  },
  {
    "index": "427",
    "kanji": "市民",
    "reading": "市民",
    "romaji": "shimin",
    "type": "Noun",
    "meaning": "citizen"
  },
  {
    "index": "428",
    "kanji": "品物",
    "reading": "しなもの",
    "romaji": "shinamono",
    "type": "Noun",
    "meaning": "goods; article; thing"
  },
  {
    "index": "429",
    "kanji": "新聞社",
    "reading": "しんぶんしゃ",
    "romaji": "shinbunsha",
    "type": "Noun",
    "meaning": "newspaper company"
  },
  {
    "index": "430",
    "kanji": "親切",
    "reading": "しんせつ",
    "romaji": "shinsetsu",
    "type": "Noun, Adjective, な-adjective",
    "meaning": "kindness"
  },
  {
    "index": "431",
    "kanji": "失敗",
    "reading": "しっぱい",
    "romaji": "shippai",
    "type": "Noun, Suru verb",
    "meaning": "failure"
  },
  {
    "index": "432",
    "kanji": "調べる",
    "reading": "しらべる",
    "romaji": "shiraberu",
    "type": "Verb, Ichidan verb, Transitive verb",
    "meaning": "to investigate"
  },
  {
    "index": "433",
    "kanji": "知らせる",
    "reading": "しらせる",
    "romaji": "shiraseru",
    "type": "Verb, Ichidan verb, Transitive verb",
    "meaning": "to notify"
  },
  {
    "index": "434",
    "kanji": "下着",
    "reading": "したぎ",
    "romaji": "shitagi",
    "type": "Noun",
    "meaning": "underwear"
  },
  {
    "index": "435",
    "kanji": "食料品",
    "reading": "しょくりょうひん",
    "romaji": "shokuryouhin",
    "type": "Noun",
    "meaning": "food; groceries"
  },
  {
    "index": "436",
    "kanji": "小学校",
    "reading": "しょうがっこう",
    "romaji": "shougakkou",
    "type": "Noun",
    "meaning": "elementary school"
  },
  {
    "index": "437",
    "kanji": "生じる",
    "reading": "しょうじる",
    "romaji": "shoujiru",
    "type": "Verb, Ichidan verb, Transitive verb",
    "meaning": "to produce"
  },
  {
    "index": "438",
    "kanji": "紹介",
    "reading": "しょうかい",
    "romaji": "shoukai",
    "type": "Noun, Suru verb",
    "meaning": "introduction"
  },
  {
    "index": "439",
    "kanji": "将来",
    "reading": "しょうらい",
    "romaji": "shourai",
    "type": "Noun, Adverbial Noun",
    "meaning": "future"
  },
  {
    "index": "440",
    "kanji": "小説",
    "reading": "しょうせつ",
    "romaji": "shousetsu",
    "type": "Noun",
    "meaning": "novel"
  },
  {
    "index": "441",
    "kanji": "趣味",
    "reading": "しゅみ",
    "romaji": "shumi",
    "type": "Noun",
    "meaning": "hobby; pastime; preference"
  },
  {
    "index": "442",
    "kanji": "習慣",
    "reading": "しゅうかん",
    "romaji": "shuukan",
    "type": "Noun",
    "meaning": "habit; custom; cultural practice."
  },
  {
    "index": "443",
    "kanji": "祖母",
    "reading": "そぼ",
    "romaji": "sobo",
    "type": "Noun",
    "meaning": "grandmother"
  },
  {
    "index": "444",
    "kanji": "育てる",
    "reading": "そだてる",
    "romaji": "sodateru",
    "type": "Verb, Ichidan verb, Transitive verb",
    "meaning": "to rear,to bring up"
  },
  {
    "index": "445",
    "kanji": "祖父",
    "reading": "そふ",
    "romaji": "sofu",
    "type": "Noun",
    "meaning": "grandfather"
  },
  {
    "index": "446",
    "kanji": "",
    "reading": "ソフト",
    "romaji": "sofuto",
    "type": "Noun, Katakana",
    "meaning": "soft"
  },
  {
    "index": "447",
    "kanji": "",
    "reading": "そんな",
    "romaji": "sonna",
    "type": "Pre-noun adjectival",
    "meaning": "that sort of"
  },
  {
    "index": "448",
    "kanji": "",
    "reading": "それで",
    "romaji": "sore de",
    "type": "Conjunction",
    "meaning": "because of that"
  },
  {
    "index": "449",
    "kanji": "",
    "reading": "それほど",
    "romaji": "sore hodo",
    "type": "Adverb",
    "meaning": "to that extent"
  },
  {
    "index": "450",
    "kanji": "",
    "reading": "そろそろ",
    "romaji": "sorosoro",
    "type": "Adverb",
    "meaning": "gradually; soon"
  },
  {
    "index": "451",
    "kanji": "卒業",
    "reading": "そつぎょう",
    "romaji": "sotsugyou",
    "type": "Noun, Suru verb",
    "meaning": "graduation"
  },
  {
    "index": "452",
    "kanji": "相談",
    "reading": "そうだん",
    "romaji": "soudan",
    "type": "Noun, Suru verb",
    "meaning": "to discuss"
  },
  {
    "index": "453",
    "kanji": "素晴らしい",
    "reading": "すばらしい",
    "romaji": "subarashii",
    "type": "Adjective, い-adjective",
    "meaning": "wonderful"
  },
  {
    "index": "454",
    "kanji": "滑る",
    "reading": "すべる",
    "romaji": "suberu",
    "type": "Verb, Godan verb, Intransitive verb",
    "meaning": "to slide; to slip"
  },
  {
    "index": "455",
    "kanji": "凄い",
    "reading": "すごい",
    "romaji": "sugoi",
    "type": "Adjective, い-adjective",
    "meaning": "terrific"
  },
  {
    "index": "456",
    "kanji": "水道",
    "reading": "すいどう",
    "romaji": "suidou",
    "type": "Noun",
    "meaning": "water supply"
  },
  {
    "index": "457",
    "kanji": "水泳",
    "reading": "すいえい",
    "romaji": "suiei",
    "type": "Noun, Suru verb",
    "meaning": "swimming"
  },
  {
    "index": "458",
    "kanji": "",
    "reading": "すっかり",
    "romaji": "sukkari",
    "type": "Adverb",
    "meaning": "completely"
  },
  {
    "index": "459",
    "kanji": "空く",
    "reading": "すく",
    "romaji": "suku",
    "type": "Verb, Godan verb, Intransitive verb",
    "meaning": "to be hungry"
  },
  {
    "index": "460",
    "kanji": "",
    "reading": "スクリーン",
    "romaji": "sukuriin",
    "type": "Noun, Katakana",
    "meaning": "screen"
  },
  {
    "index": "461",
    "kanji": "隅",
    "reading": "すみ",
    "romaji": "sumi",
    "type": "Noun",
    "meaning": "corner; nook"
  },
  {
    "index": "462",
    "kanji": "済む",
    "reading": "すむ",
    "romaji": "sumu",
    "type": "Verb, Godan verb, Intransitive verb",
    "meaning": "to finish"
  },
  {
    "index": "463",
    "kanji": "砂",
    "reading": "すな",
    "romaji": "suna",
    "type": "Noun",
    "meaning": "sand"
  },
  {
    "index": "464",
    "kanji": "",
    "reading": "すり",
    "romaji": "suri",
    "type": "Noun",
    "meaning": "pickpocket"
  },
  {
    "index": "465",
    "kanji": "",
    "reading": "スーツケース",
    "romaji": "sustsukeesu",
    "type": "Noun, Katakana",
    "meaning": "suitcase"
  },
  {
    "index": "466",
    "kanji": "進む",
    "reading": "すすむ",
    "romaji": "susumu",
    "type": "Verb, Godan verb, Intransitive verb",
    "meaning": "to make progress"
  },
  {
    "index": "467",
    "kanji": "",
    "reading": "ステーキ",
    "romaji": "suteeki",
    "type": "Noun, Katakana",
    "meaning": "steak"
  },
  {
    "index": "468",
    "kanji": "",
    "reading": "ステレオ",
    "romaji": "sutereo",
    "type": "Noun, Katakana",
    "meaning": "stereo"
  },
  {
    "index": "469",
    "kanji": "捨てる",
    "reading": "すてる",
    "romaji": "suteru",
    "type": "Verb, Ichidan verb, Transitive verb",
    "meaning": "to throw away"
  },
  {
    "index": "470",
    "kanji": "数学",
    "reading": "すうがく",
    "romaji": "suugaku",
    "type": "Noun",
    "meaning": "mathematics; arithmetic"
  },
  {
    "index": "471",
    "kanji": "",
    "reading": "スーツ",
    "romaji": "suutsu",
    "type": "Noun, Katakana",
    "meaning": "suit"
  },
  {
    "index": "472",
    "kanji": "正しい",
    "reading": "ただしい",
    "romaji": "tadashii",
    "type": "Adjective, い-adjective",
    "meaning": "right; correct"
  },
  {
    "index": "473",
    "kanji": "退院",
    "reading": "たいいん",
    "romaji": "tai'in",
    "type": "Noun, Verb, Suru verb",
    "meaning": "leaving hospital; discharge from hospital"
  },
  {
    "index": "474",
    "kanji": "台風",
    "reading": "たいふう",
    "romaji": "taifuu",
    "type": "Noun",
    "meaning": "typhoon"
  },
  {
    "index": "475",
    "kanji": "",
    "reading": "タイプ",
    "romaji": "taipu",
    "type": "Noun",
    "meaning": "type,style"
  },
  {
    "index": "476",
    "kanji": "",
    "reading": "たいてい",
    "romaji": "taitei",
    "type": "Noun, Adjective, な-adjective, Adverb",
    "meaning": "usually"
  },
  {
    "index": "477",
    "kanji": "",
    "reading": "たまに",
    "romaji": "tamani",
    "type": "Adverb",
    "meaning": "occasionally"
  },
  {
    "index": "478",
    "kanji": "棚",
    "reading": "たな",
    "romaji": "tana",
    "type": "Noun",
    "meaning": "shelves"
  },
  {
    "index": "479",
    "kanji": "誕生",
    "reading": "たんじょう",
    "romaji": "tanjou",
    "type": "Noun, Suru verb",
    "meaning": "birth"
  },
  {
    "index": "480",
    "kanji": "楽しみ",
    "reading": "たのしみ",
    "romaji": "tanoshimi",
    "type": "Noun, Adjective, な-adjective",
    "meaning": "looking forward to​"
  },
  {
    "index": "481",
    "kanji": "倒れる",
    "reading": "たおれる",
    "romaji": "taoreru",
    "type": "Verb, Ichidan verb, Intransitive verb",
    "meaning": "to fall (over, down)"
  },
  {
    "index": "482",
    "kanji": "足りる",
    "reading": "たりる",
    "romaji": "tariru",
    "type": "Verb, Ichidan verb, Intransitive verb",
    "meaning": "to be sufficient; to be enough"
  },
  {
    "index": "483",
    "kanji": "足す",
    "reading": "たす",
    "romaji": "tasu",
    "type": "Verb, Godan verb, Transitive verb",
    "meaning": "to add (numbers / something)"
  },
  {
    "index": "484",
    "kanji": "畳",
    "reading": "たたみ",
    "romaji": "tatami",
    "type": "Noun",
    "meaning": "Japanese straw mat"
  },
  {
    "index": "485",
    "kanji": "建てる",
    "reading": "たてる",
    "romaji": "tateru",
    "type": "Verb, Ichidan verb, Transitive verb",
    "meaning": "to build"
  },
  {
    "index": "486",
    "kanji": "尋ねる",
    "reading": "たずねる",
    "romaji": "tazuneru",
    "type": "Verb, Ichidan verb, Transitive verb",
    "meaning": "to ask"
  },
  {
    "index": "487",
    "kanji": "訪ねる",
    "reading": "たずねる",
    "romaji": "tazuneru",
    "type": "Verb, Ichidan verb, Transitive verb",
    "meaning": "to visit"
  },
  {
    "index": "488",
    "kanji": "手袋",
    "reading": "てぶくろ",
    "romaji": "tebukuro",
    "type": "Noun",
    "meaning": "glove"
  },
  {
    "index": "489",
    "kanji": "丁寧",
    "reading": "ていねい",
    "romaji": "teinei",
    "type": "Noun, Adjective, な-adjective",
    "meaning": "polite"
  },
  {
    "index": "490",
    "kanji": "",
    "reading": "テキスト",
    "romaji": "tekisuto",
    "type": "Noun, Katakana",
    "meaning": "text; textbook"
  },
  {
    "index": "491",
    "kanji": "適当",
    "reading": "てきとう",
    "romaji": "tekitou",
    "type": "Noun, Adjective, な-adjective",
    "meaning": "suitable"
  },
  {
    "index": "492",
    "kanji": "点",
    "reading": "てん",
    "romaji": "ten",
    "type": "Noun",
    "meaning": "point; dot"
  },
  {
    "index": "493",
    "kanji": "店員",
    "reading": "てんいん",
    "romaji": "ten'in",
    "type": "Noun",
    "meaning": "employee (of a store); shop assistant; clerk"
  },
  {
    "index": "494",
    "kanji": "",
    "reading": "テニス",
    "romaji": "tenisu",
    "type": "Noun, Katakana",
    "meaning": "tennis"
  },
  {
    "index": "495",
    "kanji": "天気予報",
    "reading": "てんきよほう",
    "romaji": "tenkiyohou",
    "type": "Noun",
    "meaning": "weather forecast"
  },
  {
    "index": "496",
    "kanji": "展覧会",
    "reading": "てんらんかい",
    "romaji": "tenrankai",
    "type": "Noun",
    "meaning": "exhibition"
  },
  {
    "index": "497",
    "kanji": "寺",
    "reading": "てら",
    "romaji": "tera",
    "type": "Noun",
    "meaning": "temple"
  },
  {
    "index": "498",
    "kanji": "手伝う",
    "reading": "てつだう",
    "romaji": "tetsudau",
    "type": "Verb, Godan verb, Transitive verb",
    "meaning": "to help; to assist; to aid​"
  },
  {
    "index": "499",
    "kanji": "途中",
    "reading": "とちゅう",
    "romaji": "tochuu",
    "type": "Noun, Adverbial Noun",
    "meaning": "on the way"
  },
  {
    "index": "500",
    "kanji": "届ける",
    "reading": "とどける",
    "romaji": "todokeru",
    "type": "#",
    "meaning": "ごい\tVocabulary\tType\tMeaning"
  },
  {
    "index": "501",
    "kanji": "特急",
    "reading": "とっきゅう",
    "romaji": "tokkyuu",
    "type": "Noun",
    "meaning": "limited express (train, faster than an express)"
  },
  {
    "index": "502",
    "kanji": "床屋",
    "reading": "とこや",
    "romaji": "tokoya",
    "type": "Noun",
    "meaning": "barber"
  },
  {
    "index": "503",
    "kanji": "特別",
    "reading": "とくべつ",
    "romaji": "tokubetsu",
    "type": "Noun, Adjective, な-adjective",
    "meaning": "special; particular; extraordinary; exceptional"
  },
  {
    "index": "504",
    "kanji": "特に",
    "reading": "とくに",
    "romaji": "tokuni",
    "type": "Adverb",
    "meaning": "particularly; especially; in particular; expressly"
  },
  {
    "index": "505",
    "kanji": "泊まる",
    "reading": "とまる",
    "romaji": "tomaru",
    "type": "Verb, Godan verb, Intransitive verb",
    "meaning": "to stay at"
  },
  {
    "index": "506",
    "kanji": "止める",
    "reading": "とめる",
    "romaji": "tomeru",
    "type": "Verb, Ichidan verb, Transitive verb",
    "meaning": "to stop something"
  },
  {
    "index": "507",
    "kanji": "遠く",
    "reading": "とおく",
    "romaji": "tooku",
    "type": "Noun, Adverbial Noun",
    "meaning": "distant"
  },
  {
    "index": "508",
    "kanji": "通る",
    "reading": "とおる",
    "romaji": "tooru",
    "type": "Verb, Godan verb, Intransitive verb",
    "meaning": "to go through"
  },
  {
    "index": "509",
    "kanji": "取り替える",
    "reading": "とりかえる",
    "romaji": "torikaeru",
    "type": "Verb, Ichidan verb, Transitive verb",
    "meaning": "to exchange; to swap; to replace"
  },
  {
    "index": "510",
    "kanji": "到頭",
    "reading": "とうとう",
    "romaji": "toutou",
    "type": "Adverb",
    "meaning": "finally, after all"
  },
  {
    "index": "511",
    "kanji": "続ける",
    "reading": "つづける",
    "romaji": "tsudzukeru",
    "type": "Verb, Ichidan verb, Transitive verb",
    "meaning": "to continue; to keep up; to keep on"
  },
  {
    "index": "512",
    "kanji": "続く",
    "reading": "つづく",
    "romaji": "tsudzuku",
    "type": "Verb, Godan verb, Intransitive verb",
    "meaning": "to continue"
  },
  {
    "index": "513",
    "kanji": "都合",
    "reading": "つごう",
    "romaji": "tsugou",
    "type": "Noun, Adverb",
    "meaning": "convenience"
  },
  {
    "index": "514",
    "kanji": "捕まえる",
    "reading": "つかまえる",
    "romaji": "tsukamaeru",
    "type": "Verb, Ichidan verb, Transitive verb",
    "meaning": "to catch"
  },
  {
    "index": "515",
    "kanji": "漬ける",
    "reading": "つける",
    "romaji": "tsukeru",
    "type": "Verb, Ichidan verb, Transitive verb",
    "meaning": "to soak; to pickle"
  },
  {
    "index": "516",
    "kanji": "月",
    "reading": "つき",
    "romaji": "tsuki",
    "type": "Noun",
    "meaning": "moon"
  },
  {
    "index": "517",
    "kanji": "付く",
    "reading": "つく",
    "romaji": "tsuku",
    "type": "Verb, Godan verb, Intransitive verb",
    "meaning": "to be attached"
  },
  {
    "index": "518",
    "kanji": "妻",
    "reading": "つま",
    "romaji": "tsuma",
    "type": "Noun",
    "meaning": "(humble) wife"
  },
  {
    "index": "519",
    "kanji": "連れる",
    "reading": "つれる",
    "romaji": "tsureru",
    "type": "Verb, Ichidan verb, Transitive verb",
    "meaning": "to take (someone) with one"
  },
  {
    "index": "520",
    "kanji": "釣る",
    "reading": "つる",
    "romaji": "tsuru",
    "type": "Verb, Godan verb, Transitive verb",
    "meaning": "to fish"
  },
  {
    "index": "521",
    "kanji": "伝える",
    "reading": "つたえる",
    "romaji": "tsutaeru",
    "type": "Verb, Ichidan verb, Transitive verb",
    "meaning": "to report; to tell"
  },
  {
    "index": "522",
    "kanji": "包む",
    "reading": "つつむ",
    "romaji": "tsutsumu",
    "type": "Verb, Godan verb, Transitive verb",
    "meaning": "to wrap"
  },
  {
    "index": "523",
    "kanji": "腕",
    "reading": "うで",
    "romaji": "ude",
    "type": "Noun",
    "meaning": "arm"
  },
  {
    "index": "524",
    "kanji": "植える",
    "reading": "うえる",
    "romaji": "ueru",
    "type": "Verb, Ichidan verb, Transitive verb",
    "meaning": "to plant; to grow"
  },
  {
    "index": "525",
    "kanji": "動く",
    "reading": "うごく",
    "romaji": "ugoku",
    "type": "Verb, Godan verb, Intransitive verb",
    "meaning": "to move"
  },
  {
    "index": "526",
    "kanji": "伺う",
    "reading": "うかがう",
    "romaji": "ukagau",
    "type": "Verb, Godan verb, Transitive verb",
    "meaning": "to visit"
  },
  {
    "index": "527",
    "kanji": "受ける",
    "reading": "うける",
    "romaji": "ukeru",
    "type": "Verb, Ichidan verb, Transitive verb",
    "meaning": "to take a lesson or test"
  },
  {
    "index": "528",
    "kanji": "受付",
    "reading": "うけつけ",
    "romaji": "uketsuke",
    "type": "Noun",
    "meaning": "reception (desk); information desk​"
  },
  {
    "index": "529",
    "kanji": "生まれ",
    "reading": "うまれ",
    "romaji": "umare",
    "type": "Noun",
    "meaning": "birth"
  },
  {
    "index": "530",
    "kanji": "運転手",
    "reading": "うんてんしゅ",
    "romaji": "untenshu",
    "type": "Noun",
    "meaning": "driver; chauffeur"
  },
  {
    "index": "531",
    "kanji": "裏",
    "reading": "うら",
    "romaji": "ura",
    "type": "Noun",
    "meaning": "reverse side"
  },
  {
    "index": "532",
    "kanji": "嬉しい",
    "reading": "うれしい",
    "romaji": "ureshii",
    "type": "Adjective, い-adjective",
    "meaning": "happy"
  },
  {
    "index": "533",
    "kanji": "売り場",
    "reading": "うりば",
    "romaji": "uriba",
    "type": "Noun",
    "meaning": "selling area"
  },
  {
    "index": "534",
    "kanji": "嘘",
    "reading": "うそ",
    "romaji": "uso",
    "type": "Noun",
    "meaning": "a lie"
  },
  {
    "index": "535",
    "kanji": "打つ",
    "reading": "うつ",
    "romaji": "utsu",
    "type": "Verb, Godan verb, Transitive verb",
    "meaning": "to hit"
  },
  {
    "index": "536",
    "kanji": "美しい",
    "reading": "うつくしい",
    "romaji": "utsukushii",
    "type": "Adjective, い-adjective",
    "meaning": "beautiful"
  },
  {
    "index": "537",
    "kanji": "移る",
    "reading": "うつる",
    "romaji": "utsuru",
    "type": "Verb, Godan verb, Intransitive verb",
    "meaning": "to move house or transfer"
  },
  {
    "index": "538",
    "kanji": "写す",
    "reading": "うつす",
    "romaji": "utsusu",
    "type": "Verb, Godan verb, Transitive verb",
    "meaning": "to copy or photograph"
  },
  {
    "index": "539",
    "kanji": "",
    "reading": "ワープロ",
    "romaji": "waapuro",
    "type": "Noun, Katakana",
    "meaning": "word processor"
  },
  {
    "index": "540",
    "kanji": "別れる",
    "reading": "わかれる",
    "romaji": "wakareru",
    "type": "Verb, Ichidan verb, Intransitive verb",
    "meaning": "to separate"
  },
  {
    "index": "541",
    "kanji": "沸かす",
    "reading": "わかす",
    "romaji": "wakasu",
    "type": "Verb, Godan verb, Transitive verb",
    "meaning": "to boil; to heat"
  },
  {
    "index": "542",
    "kanji": "沸く",
    "reading": "わく",
    "romaji": "waku",
    "type": "Verb, Godan verb, Intransitive verb",
    "meaning": "to boil"
  },
  {
    "index": "543",
    "kanji": "笑う",
    "reading": "わらう",
    "romaji": "warau",
    "type": "Verb, Godan verb, Intransitive verb",
    "meaning": "to laugh; to smile"
  },
  {
    "index": "544",
    "kanji": "割れる",
    "reading": "われる",
    "romaji": "wareru",
    "type": "Verb, Ichidan verb, Intransitive verb",
    "meaning": "to break"
  },
  {
    "index": "545",
    "kanji": "割合",
    "reading": "わりあい",
    "romaji": "wariai",
    "type": "Noun",
    "meaning": "rate; ratio"
  },
  {
    "index": "546",
    "kanji": "忘れ物",
    "reading": "わすれもの",
    "romaji": "wasuremono",
    "type": "Noun",
    "meaning": "lost article"
  },
  {
    "index": "547",
    "kanji": "焼ける",
    "reading": "やける",
    "romaji": "yakeru",
    "type": "Verb, Ichidan verb, Intransitive verb",
    "meaning": "to burn; to be roasted"
  },
  {
    "index": "548",
    "kanji": "焼く",
    "reading": "やく",
    "romaji": "yaku",
    "type": "Verb, Godan verb, Transitive verb",
    "meaning": "to bake; to grill"
  },
  {
    "index": "549",
    "kanji": "役に立つ",
    "reading": "やくにたつ",
    "romaji": "yakunitatsu",
    "type": "Verb, Godan verb, Expression",
    "meaning": "to be helpful"
  },
  {
    "index": "550",
    "kanji": "約束",
    "reading": "やくそく",
    "romaji": "yakusoku",
    "type": "Noun, Suru verb",
    "meaning": "promise"
  },
  {
    "index": "551",
    "kanji": "止む",
    "reading": "やむ",
    "romaji": "yamu",
    "type": "Verb, Godan verb, Intransitive verb",
    "meaning": "to stop"
  },
  {
    "index": "552",
    "kanji": "",
    "reading": "やっぱり",
    "romaji": "yappari",
    "type": "Adverb",
    "meaning": "as I thought"
  },
  {
    "index": "553",
    "kanji": "優しい",
    "reading": "やさしい",
    "romaji": "yasashii",
    "type": "Adjective, い-adjective",
    "meaning": "kind"
  },
  {
    "index": "554",
    "kanji": "痩せる",
    "reading": "やせる",
    "romaji": "yaseru",
    "type": "Verb, Ichidan verb, Intransitive verb",
    "meaning": "to become thin"
  },
  {
    "index": "555",
    "kanji": "柔らかい",
    "reading": "やわらかい",
    "romaji": "yawarakai",
    "type": "Adjective, い-adjective",
    "meaning": "soft"
  },
  {
    "index": "556",
    "kanji": "汚れる",
    "reading": "よごれる",
    "romaji": "yogoreru",
    "type": "Verb, Ichidan verb, Intransitive verb",
    "meaning": "to get dirty"
  },
  {
    "index": "557",
    "kanji": "喜ぶ",
    "reading": "よろこぶ",
    "romaji": "yorokobu",
    "type": "Verb, Godan verb",
    "meaning": "to be delighted"
  },
  {
    "index": "558",
    "kanji": "寄る",
    "reading": "よる",
    "romaji": "yoru",
    "type": "Verb, Godan verb, Intransitive verb",
    "meaning": "to visit; to drop by"
  },
  {
    "index": "559",
    "kanji": "予習",
    "reading": "よしゅう",
    "romaji": "yoshuu",
    "type": "Noun, Verb, Suru verb",
    "meaning": "preparation for a lesson"
  },
  {
    "index": "560",
    "kanji": "予定",
    "reading": "よてい",
    "romaji": "yotei",
    "type": "Noun, Suru verb",
    "meaning": "plan"
  },
  {
    "index": "561",
    "kanji": "用",
    "reading": "よう",
    "romaji": "you",
    "type": "Noun, Suffix",
    "meaning": "business; task; errand; use; purpose"
  },
  {
    "index": "562",
    "kanji": "用意",
    "reading": "ようい",
    "romaji": "youi",
    "type": "Noun, Verb, Suru verb",
    "meaning": "preparation; arrangements; provision; getting ready"
  },
  {
    "index": "563",
    "kanji": "用事",
    "reading": "ようじ",
    "romaji": "youji",
    "type": "Noun",
    "meaning": "tasks; things to do; errand; business (to take care of)"
  },
  {
    "index": "564",
    "kanji": "予約",
    "reading": "よやく",
    "romaji": "yoyaku",
    "type": "Noun, Suru verb",
    "meaning": "reservation"
  },
  {
    "index": "565",
    "kanji": "湯",
    "reading": "ゆ",
    "romaji": "yu",
    "type": "Noun",
    "meaning": "hot water"
  },
  {
    "index": "566",
    "kanji": "指",
    "reading": "ゆび",
    "romaji": "yubi",
    "type": "Noun",
    "meaning": "finger"
  },
  {
    "index": "567",
    "kanji": "指輪",
    "reading": "ゆびわ",
    "romaji": "yubiwa",
    "type": "Noun",
    "meaning": "finger ring"
  },
  {
    "index": "568",
    "kanji": "夢",
    "reading": "ゆめ",
    "romaji": "yume",
    "type": "Noun",
    "meaning": "dream"
  },
  {
    "index": "569",
    "kanji": "揺れる",
    "reading": "ゆれる",
    "romaji": "yureru",
    "type": "Verb, Ichidan verb, Intransitive verb",
    "meaning": "to shake"
  },
  {
    "index": "570",
    "kanji": "残念",
    "reading": "ざんねん",
    "romaji": "zannen",
    "type": "Noun, Adjective, な-adjective",
    "meaning": "regrettable; unfortunate"
  },
  {
    "index": "571",
    "kanji": "全然",
    "reading": "ぜんぜん",
    "romaji": "zenzen",
    "type": "Adverb",
    "meaning": "not entirely (used in a negative sentence)"
  }
];