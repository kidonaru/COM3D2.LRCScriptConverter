
# LRCスクリプトコンバーター ver1.0.0

- [LRCスクリプトコンバーター ver1.0.0](#LRCスクリプトコンバーター-ver100)
  - [概要](#概要)
    - [DCMとは](#DCMとは)
    - [LRCスクリプトとは](#LRCスクリプトとは)
  - [動作確認バージョン](#動作確認バージョン)
  - [規約](#規約)
  - [変更履歴](#変更履歴)
  - [改修予定](#改修予定)
  - [セットアップ](#セットアップ)
    - [サンプルの再生に必要なもの](#サンプルの再生に必要なもの)
      - [DLC](#DLC)
      - [MOD](#MOD)
  - [各ファイル説明](#各ファイル説明)
  - [コンバート方法](#コンバート方法)
  - [曲の追加手順](#曲の追加手順)
    - [1.ファイル複製](#1ファイル複製)
    - [2.曲情報編集](#2曲情報編集)
    - [3.再生確認](#3再生確認)
    - [4.LRCスクリプトの確認](#4LRCスクリプトの確認)
    - [5.コンバーター設定](#5コンバーター設定)
    - [6.口パクデータの作成](#6口パクデータの作成)
    - [7.演出の作成](#7演出の作成)
    - [8.ポーズを変更する](#8ポーズを変更する)
    - [9.カメラを変更する](#9カメラを変更する)
    - [10.演出を詰める](#10演出を詰める)
  - [LRCスクリプトの仕様](#LRCスクリプトの仕様)
    - [基本的な記述方法](#基本的な記述方法)
    - [コメント](#コメント)
    - [口パクループ](#口パクループ)
    - [タグ](#タグ)
    - [設定タグ](#設定タグ)
      - [設定タグ一覧](#設定タグ一覧)
    - [データ出力タグ](#データ出力タグ)
      - [データ出力タグ一覧](#データ出力タグ一覧)
    - [変数](#変数)
      - [変数一覧](#変数一覧)
    - [カスタムタグ](#カスタムタグ)
      - [カスタムタグの使い方](#カスタムタグの使い方)
      - [カスタムタグ引数](#カスタムタグ引数)
      - [カスタムタグの連結](#カスタムタグの連結)
    - [画像動かしタグ](#画像動かしタグ)
      - [movePngテンプレート](#movePngテンプレート)
      - [MOVE_PNGタグ](#MOVE_PNGタグ)
    - [四則演算](#四則演算)
  - [エラー一覧](#エラー一覧)
    - [引数が足りません](#引数が足りません)
    - [未定義のタグ](#未定義のタグ)
    - [未定義の変数](#未定義の変数)


## 概要

COM3D2.DanceCameraMotion.Plugin (DCM) で使用する各演出ファイルを、
LRCスクリプトを使用して書き出すための非公式ツールです。

※コンバーターの作者 ≠ DCM作者

最低限のDCMの知識がある人向けのツールになります。


### DCMとは

COM3D2でフリーダンスやカメラモーションを再生するプラグインです。
大体なんでもできる神プラグイン。


### LRCスクリプトとは

LRCファイルは元々歌詞の同期用ファイル形式で、
それをDCM演出用に拡張したものをLRCスクリプトと(筆者が勝手に)言っています。


## 動作確認バージョン

- COM3D2 Ver.2.8.0
- COM3D2.DanceCameraMotion.Plugin 6.3.3
- BepInEx 5.4.17
- Windows 10 Home 21H1
- Python 3.9.8


## 規約

自己責任で実行をお願いします。
改造、再配布は問題ありませんが、改造する場合はご連絡いただければできるだけ修正を取り込みます。

連絡先

https://twitter.com/kidonaru

```
※MODはKISSサポート対象外です。
※MODを利用するに当たり、問題が発生してもKISSは一切の責任を負いかねます。
※「カスタムメイド3D2」か「カスタムオーダーメイド3D2」か「CR EditSystem」を購入されている方のみが利用できます。
※「カスタムメイド3D2」か「カスタムオーダーメイド3D2」か「CR EditSystem」上で表示する目的以外の利用は禁止します。
※これらの事項は http://kisskiss.tv/kiss/diary.php?no=558 を優先します。
```


## 変更履歴

- 2021/11/29 v1.0.0公開


## 改修予定

- morph対応
- 複数メイドslot対応


## セットアップ

1. DCMを動く状態にします。
(手順は省略)

2. [このページ](https://github.com/kidonaru/COM3D2.LRCScriptConverter/releases)から最新の`COM3D2.LRCScriptConverter-vX.X.X.zip`をダウンロードします。

3. zipを解答し、中にある`UnityInjector`ディレクトリを、`COM3D2\Sybaris\UnityInjector`に上書きします。
このとき*MaidMouth.csv*を上書きするので、既にカスタマイズ済みの場合はA~nの行だけコピーして使用してください。

4. コンバーターでPythonを使用しているため、Pythonのインストールをします。
Windows 10であれば、コマンドプロンプトで`python`コマンドを実行すると
Microsoft Storeが開き、Pythonのインストールが可能です。


### サンプルの再生に必要なもの

サンプルの再生に下記DLC、MODが必要なため、サンプルを再生する場合はインストールしてください。

#### DLC

- バイノーラルSP
https://com3d2-shop.s-court.me/item.php?iid=1501

#### MOD

※MODの利用は製作者のREADMEに従ってください

- https://twitter.com/route163_cm3d2/status/810550252596002816
  - `COM3D3/Mod`以下へ格納

- https://ux.getuploader.com/cm3d2_e/download/219
  - `COM3D2\Sybaris\UnityInjector\Config\DanceCameraMotion\png`以下へ格納


## 各ファイル説明

エクスプローラーで、
`COM3D2\Sybaris\UnityInjector\Config\DanceCameraMotion\song\サンプル【LRCスクリプト】`
を開きます。

この中にサンプルスクリプト、コンバーター、DCM用の演出ファイル(csv)が格納されています。

- *song.lrc*
  - LRCスクリプト本体です。
  コンバーターを実行すると、このスクリプトを元に演出用csvを吐き出します

- *lrc_script_converter.bat*
  - コンバーターを実行するバッチです。
  実際のコードは*lrc_script_converter.py*にあり、このバッチは*lrc_script_converter.py*を実行しているだけです

- *lrc_script_converter.py*
  - Pythonで書かれたコンバーターの中身です。
  実行ディレクトリ内のLRCスクリプトを検索し、コンバートを実行しています

- **.csv*
  - コンバーターで出力された、DCM用の演出ファイルです


## コンバート方法

*lrc_script_converter.bat*を実行するとコマンドプロンプトが立ち上がり
下記の内容が出力され、csvが吐き出されます。

```
...
csv出力: COM3D2\Sybaris\UnityInjector\Config\DanceCameraMotion\song\サンプル【LRCスクリプト】\shape_song.csv
movePng出力: COM3D2\Sybaris\UnityInjector\Config\DanceCameraMotion\song\サンプル【LRCスクリプト】\movePng_song.xml
すべての処理が完了しました
```

"すべての処理が完了しました" と表示されていれば成功です。

エラー等が表示されている場合は[エラー一覧](#エラー一覧)を参照してください。


## 曲の追加手順

LRCスクリプトを使用した曲を追加するときの参考手順になります。


### 1.ファイル複製

`COM3D2\Sybaris\UnityInjector\Config\DanceCameraMotion\song\サンプル【LRCスクリプト】`
`COM3D2\Sybaris\UnityInjector\Config\DanceCameraMotion\songList\PluginSongList01_サンプル【LRCスクリプト】.xml`

をコピーして

`COM3D2\Sybaris\UnityInjector\Config\DanceCameraMotion\song\[曲名]`
`COM3D2\Sybaris\UnityInjector\Config\DanceCameraMotion\song\songList\PluginSongList01_[曲名].xml`

を作成します。([曲名]は任意)


### 2.曲情報編集

*PluginSongList01_[曲名].xml*
を開いて`label`, `folder`, `endTime`を修正します。

```
  <song label="PluginSongList01_[曲名]" type="song">
    <folder>[曲名]</folder>
    <bgm>song.ogg</bgm>
    <metronome>140</metronome>
    <baseNote>8</baseNote>
    <endTime>60</endTime>
```

この時点では`metronome`、`baseNote`の値は仮でも問題ありません。


### 3.再生確認

`COM3D2\Sybaris\UnityInjector\Config\DanceCameraMotion\song\[曲名]\song.ogg`
を任意の曲に差し替えます。

*lrc_script_converter.bat*を実行し、エラーが無いことを確認します。

あとはDCMで[曲名]を選択して再生できれば土台の作成は完了です。


### 4.LRCスクリプトの確認

*song.lrc*を任意のテキストエディタで開き中身を確認します。

量は多いですが、実際の演出内容は130行目以降のこれだけになります。

```
[00:00.00]## 開始処理
[00:00.00]#BG_1 #LIGHT_2 #CAMERA_2 #MABATAKI_ON #FADE_START:2
[00:00.00]           #FACE_A1 #POSE_C1:0

[00:00.00]## 演出内容
[00:03.00]ぽーずへんこう      #POSE_R1:1.3 #TEXT_2:ポーズ変更
[00:08.00]ん         #FACE_A2              #TEXT_2:表情変更 #PNG_N_R1
[00:13.00](くちぱくしません)               #TEXT_2:()内の文字は口パクしません
[00:18.00]きす                             #TEXT_2:キス
[00:20.00](きす){ABC}#FACE_A3              #TEXT_2:{}内の口パクはループします #PNG_CHU_R1
[00:25.00]           #FACE_A1
[00:25.00]まばたきむこう      #MABATAKI_OFF#TEXT_2:まばたき無効
[00:30.00]まばたきゆうこう    #MABATAKI_ON #TEXT_2:まばたき有効
[00:35.00]ぽーずへんこう      #POSE_L1:1.3 #TEXT_2:ポーズ変更
[00:40.00](なめ){DEF}#FACE_B3              #TEXT_2:舐め #PNG_GUCHU_L1
[00:45.00]           #FACE_B2
[00:45.00]ふえーどあうと      #FADE_WHITE:2,0 #TEXT_2:フェードアウト&脱衣
[00:47.00]ーーだつい          #UNDRESS_WEAR:1 #TEXT_2:フェードアウト&脱衣
[00:52.00]めにゆーへんこう    #MENU_EYE_HI_1  #TEXT_2:メニュー変更
[00:57.00]しようめいへんこう  #LIGHT_1        #TEXT_2:照明変更
[01:02.00]かめらへんこう      #CAMERA_2       #TEXT_2:カメラ変更
[01:07.00]                    #CAMERA_1

[01:07.00]## 終了処理
[01:07.00]#FADE_END:2
```

実際にコンバーターを実行して出力されたcsvを確認すると
中身が理解しやすいと思います。

たとえばこれは

```
[00:03.00]ぽーずへんこう      #POSE_R1:1.3 #TEXT_2:ポーズ変更
```

3秒目のタイミングで、口パク「ぽーずへんこう」を喋らせて、ポーズを`asmr_OM_isu_kousoku_kijyoui_1_f.anm`にブレンド時間1.3秒で変更し、「ポーズ変更」という字幕を出す。

という意味になります。

各csvには下記内容が書き出されます。

*lyrics_song.csv*
```
3.00,ぽーずへんこう
```

*pose_f_song.csv*
```
3.00,1,asmr_OM_isu_kousoku_kijyoui_1_f.anm,1.3,0.5,0,0,0,0,180,0,6,breathoff
```

*text_song.csv*
```
0,ポーズ変更,Yu Gothic Bold,50,3.00,3,-503,0,1,1,0,0,0,100,8.00,3,-503,0,1,1,0,0,0,100,0,50,4,1000,10
1,ポーズ変更,Yu Gothic Bold,50,3.00,0,-500,0,1,1,255,255,255,255,8.00,0,-500,0,1,1,255,255,255,255,0,50,4,1000,10
```


### 5.コンバーター設定

[2.曲情報編集](#2曲情報編集)で入力した`metronome`、`baseNote`、`endTime`の値を
スクリプト1行目に入力してください。

```
[00:00.00]#METRONOME:140 #BASE_NOTE:8 #END_TIME:60
```


### 6.口パクデータの作成

まず再生するBGMに合わせての歌詞をひらがなで書き出します。

```
おはよう
おやすみ
(きす)
```

このとき演出のタイミングについても書いておくとスクリプトが組みやすいです。

次にLRC歌詞エディタで時間を打っていきます。

LRC歌詞エディタはMedia Goなどがおすすめです。
(開発終了しているのでインストールは自己責任でお願いします)

https://ja.vessoft.com/software/windows/download/mediago

```
[00:03.00]おはよう
[00:06.00]おやすみ
[00:09.00](きす)
```


### 7.演出の作成

上で作成した口パクをスクリプトに組み込みます

```
[00:00.00]## 開始処理
[00:00.00]#BG_2 #LIGHT_2 #CAMERA_2 #MABATAKI_ON #FADE_START:2
[00:00.00]           #FACE_A1 #POSE_C1:0

[00:00.00]## 演出内容
[00:03.00]おはよう            #POSE_R1:1.3 #TEXT_2:おはよう
[00:06.00]おやすみ   #FACE_A2              #TEXT_2:おやすみ
[00:09.00](きす){ABC}#FACE_A3              #PNG_CHU_R1

[00:12.00]## 終了処理
[00:12.00]#FADE_END:2
```

サンプルを参考に各タグを付けてください。

作業の流れとしては、

1. *song.lrc*の修正
2. *lrc_script_converter.bat*を実行
3. DCMで再生して確認

を繰り返して演出を作っていきます。


### 8.ポーズを変更する

サンプルで定義済みのポーズはバイノーラルSP系しか無いので
他のポーズにしたい場合は自分で定義する必要があります。

既存のポーズ定義をアニメ名だけ変更してコピーします。

```
[00:00.00]## ポーズ定義
[00:00.00]#POSE_A1   = #POSE_F:$now,1,om_taimenkijyoui_kiss_1_f.anm,$1,1,0,0,0,0,180,0,6,breathoff
[00:00.00]#POSE_A1  += #POSE_M:$now,1,om_taimenkijyoui_kiss_1_m.anm,$1,1,0,0,0,0,180,0,-1,,-1,0,0,0
```

※メイド用と男用で2つのポーズ変更命令が必要なので、基本2行で1セットになります

右側の値の羅列は、DCMのcsvの値になります。

メイド用ポーズのカラム定義は下記のようになっているため、
3列目を変更すればアニメ名が変わります。

```
time,poseType,animation,fadeTime,speed,posX,posY,posZ,rotX,rotY,rotZ,eyeMoveType,option
```

左側の`#POSE_A1`の箇所は任意のタグ名を付けてください。

定義したタグ名を演出部分に書くことで、そのポーズに変更できます。

```
[00:03.00]おはよう            #POSE_A1:1.3 #TEXT_2:おはよう
```


### 9.カメラを変更する

カメラも新しく定義して演出を変更してみます。

```
[00:00.00]## カメラ定義
[00:00.00]#CAMERA_3  = #CAMERA:$frame,-0.02,0.03,0.95,325.82,174.40,1.20,0,45,0
```

```
[00:00.00]## 演出内容
[00:03.00]おはよう            #POSE_A1:1.3 #TEXT_2:おはよう #CAMERA_2
[00:06.00]おやすみ   #FACE_A2              #TEXT_2:おやすみ #CAMERA_3
[00:09.00](きす){ABC}#FACE_A3              #PNG_CHU_R1
```


### 10.演出を詰める

サンプルを参考に演出を作っていきましょう。

スクリプトの細かい仕様は、次項の[LRCスクリプトの仕様](#LRCスクリプトの仕様)を参照してください。


## LRCスクリプトの仕様

結構複雑なので基本はサンプルスクリプトを改造して制作、困ったら仕様を確認する
くらいがいいと思います。


### 基本的な記述方法

`[時間]口パクの内容`というフォーマットで記述します。

歌詞の同期用フォーマットのLRC形式をベースにしています。

例えば

*song.lrc*
```
[00:03.00]ぽーずへんこう
```

と書くと

*lyrics_song.csv*
| time | lyrics |
| --- | --- |
| 3.00 | ぽーずへんこう |

という口パクデータとして吐き出されます。


### コメント

`## コメント`のフォーマットでコメントを記述できます。

また、半角括弧"()"で囲った部分もコメントと同様に扱われます。

例えば

```
[00:03.00]ぽ(ー)ずへんこう ## コメントテスト
```

と書いた場合、コンバート時にコメント部分は排除され、

```
[00:03.00]ぽずへんこう
```

と解釈されます。

"()"は基本的に口パクの調整に使用します。


### 口パクループ

`{ループする文字}`のフォーマットで入力すると、次の行まで口パクをループします。

例: *song.lrc*
```
[00:20.00]{ABC}
[00:25.00]
```

出力データ: *lyrics_song.csv*
| time | lyrics |
| --- | --- |
| 20.00 | ABCABCABCABCABCABCABCAB |


### タグ

口パク以外にも、タグを使用して各演出用にデータを出力することができます。

タグは`#タグ名:引数1,引数2,...`のフォーマットで記述します。


### 設定タグ

コンバート用の設定を行うタグです。
コンバーター内部で時間の計算などに使用しています。


#### 設定タグ一覧

| タグ名 | 内容 |
| --- | --- |
| METRONOME | テンポの指定。*songList.xml*の@metronomeと同じ値に設定 |
| BASE_NOTE | 何分音符かの指定。*songList.xml*の@baseNoteと同じ値に設定 |
| END_TIME | 終了時間を指定。*songList.xml*の@endTimeと同じ値に設定 |
| OFFSET | すべての時間を指定時間(秒)ずらす。負値で早める方向にずらす |

`METRONOME`、`BASE_NOTE`、`END_TIME`はsongListと同じ値を設定してださい。

例えば

*songList.xml*
```
    <metronome>140</metronome>
    <baseNote>8</baseNote>
    <endTime>60</endTime>
```

の場合は

```
[00:00.00]#METRONOME:140 #BASE_NOTE:8 #END_TIME:60
```

と記載してください。


### データ出力タグ

DCM用のcsvデータを生成するタグ。

`#タグ名:csvデータ`の形式で指定します。

例えば

*song.lrc*
```
[00:03.00]#POSE_F:3.0,1,asmr_OM_isu_kousoku_kijyoui_1_f.anm,1.3,0.5,0,0,0,0,180,0,6,breathoff
```

と書くと

*pose_f_song.csv*
| time | poseType | animation | fadeTime | speed | posX | posY | posZ | rotX | rotY | rotZ | eyeMoveType | option |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 3.00 | 1 | asmr_OM_isu_kousoku_kijyoui_1_f.anm | 1.3 | 0.5 | 0 | 0 | 0 | 0 | 180 | 0 | 6 | breathoff |

というポーズデータが吐き出されます。

ただ、このままでは見ずらいため、基本は後述の[変数](#変数)、[カスタムタグ](#カスタムタグ)と併用して記述します。


#### データ出力タグ一覧

| タグ名 | 出力ファイル名 | songList.xmlの項目 | 内容 |
| --- | --- | --- | --- |
| POSE_F | pose_f_[base].csv | @pose | メイドポーズ変更 |
| POSE_M | pose_m_[base].csv | @pose | 男ポーズ変更 |
| FACE | face_[base].csv | @face | メイド表情変更 |
| MABATAKI | mabataki_[base].csv | @mabataki | メイドまばたき変更 |
| EYES | eyes_[base]csv | @eyes | メイド瞳変更 |
| CAMERA | camera_[base].csv | @customMotion | カメラモーション変更 |
| BG | bg_[base].csv | @changeBg | 背景変更 |
| LIGHT | light_[base].csv | @changeLight | 照明の変更 |
| TEXT | text_[base].csv | @changeText | テキストの表示 |
| UNDRESS | undress_[base].csv | @changeUndress | 脱衣状態の指定 |
| MENU | menu_[base].csv | @changeMaidMenu | メイドメニュー変更 |
| SHAPE | shape_[base].csv | @changeShapeKey | シェイプキー変更 |
| FADE | fade_[base]csv | @changeFade | フェード変更 |

出力ファイルの[base]にはLRCスクリプトのファイル名が入ります。
例えばLRCスクリプトが*song.lrc*だと*pose_f_song.csv*というファイル名で出力されます。


### 変数

`$変数名`のフォーマットでコンバート時に動的な値を設定できます。

例えば、現在の行の時間を意味する$nowを使用して

```
[00:03.00]#POSE_F:$now,1,asmr_OM_isu_kousoku_kijyoui_1_f.anm,1.3,0.5,0,0,0,0,180,0,6,breathoff
```

のように書くとコンバート時に

```
[00:03.00]#POSE_F:3.0,1,asmr_OM_isu_kousoku_kijyoui_1_f.anm,1.3,0.5,0,0,0,0,180,0,6,breathoff
```

と解釈して出力されます


#### 変数一覧

| 変数名 | 内容 | スクリプト例 | 結果 |
| --- | --- | --- | --- |
| now | 現在の行の時間 | `[00:01.00]$now` | `[00:01.00]1` |
| next | 次の行の時間。 次の行がない場合、終了時間 | `[00:01.00]$next` `[00:02.00]` | `[00:01.00]2` `[00:02.00]` |
| end | 終了時間 | `[00:00.00]#END_TIME:60` `[00:01.00]$end` | `[00:00.00]#END_TIME:60` `[00:01.00]60` |
| frame | 現在の行のフレーム数(30fps) | `[00:01.00]$frame` | `[00:01.00]30` |
| next_frame | 次の行のフレーム数(30fps)。 次の行がない場合、終了時間 | `[00:01.00]$next_frame` `[00:02.00]` | `[00:01.00]60` `[00:02.00]` |
| csv_next | csvで次の行の時間 ※ | `[00:01.00]$csv_next` `[00:02.00]` | `[00:01.00]2` `[00:02.00]` |
| csv_next_frame | csvで次の行のフレーム数(30fps) ※ | `[00:01.00]$csv_next_frame` `[00:02.00]` | `[00:01.00]60` `[00:02.00]` |

※nextとcsv_nextの違い

`next`はスクリプト上の次の行の時間で、`csv_next`はcsv出力した後の次の行の時間になります。
`next`は違う種類のタグの影響を受けますが、`csv_next`は同じ種類のタグの影響しか受けません。


### カスタムタグ

タグとデータをセットにして別名を付けることができます。


#### カスタムタグの使い方

`#カスタムタグ名 = #タグ名:csvデータ`というフォーマットで定義します。

定義後、任意の場所で`#カスタムタグ名`を書くことで、その場所に定義したタグを差し込むことができます。

例えば

```
[00:00.00]#POSE_R1 = #POSE_F:$now,1,asmr_OM_isu_kousoku_kijyoui_1_f.anm,1.3,0.5,0,0,0,0,180,0,6,breathoff
[00:01.00]#POSE_R1
```

のように書くと、コンバート時に

```
[00:01.00]#POSE_F:1.0,1,asmr_OM_isu_kousoku_kijyoui_1_f.anm,1.3,0.5,0,0,0,0,180,0,6,breathoff
```

と解釈されます。


#### カスタムタグ引数

`#カスタムタグ名:引数1,引数2,...`
のようにカスタムタグ使用時に引数を指定すると、定義側で引数の値を`$1,$2,...`で参照することができます。

例えば

```
[00:00.00]#POSE_R1 = #POSE_F:$now,1,asmr_OM_isu_kousoku_kijyoui_1_f.anm,$1,0.5,0,0,0,0,180,0,6,breathoff
[00:01.00]#POSE_R1:1.3
```

と書くと、コンバート時に

```
[00:01.00]#POSE_F:1.0,1,asmr_OM_isu_kousoku_kijyoui_1_f.anm,1.3,0.5,0,0,0,0,180,0,6,breathoff
```

のように解釈され、blendTimeをタグ使用時に変えることができます。


#### カスタムタグの連結

定義済みのカスタムタグに対して

`#カスタムタグ名 += #タグ名:csvデータ`というフォーマットでタグを連結することが可能です。

よく使うのがポーズの定義で、メイドと男を同時にポーズ変更するときに使用します。

```
[00:00.00]#POSE_R1   = #POSE_F:$now,1,asmr_OM_isu_kousoku_kijyoui_1_f.anm,$1,0.5,0,0,0,0,180,0,6,breathoff
[00:00.00]#POSE_R1  += #POSE_M:$now,1,asmr_OM_isu_kousoku_kijyoui_1_m.anm,$1,0.5,0,0,0,0,180,0,-1,,-1,0,0,0
```


### 画像動かしタグ

movePng用のxmlを生成できます。
まずテンプレート用のxmlを用意して、その中身をスクリプトで書き換えて出力する形になります。


#### movePngテンプレート

出力先に*movePng_template.xml*というxmlを用意して、通常のmovePngのフォーマットで記述します。

例: *movePng_template.xml*
```
<?xml version="1.0" encoding="utf-8"?>
<StagePng>
  <pngGroup label="chuC1">
    <pngName>エフェクト用png\ちゅ.png</pngName>
    <png startTime="0" endTime="1">
      <position x="0.03" y="0.42" z="0.31" />
      <rotation x="0" y="180" z="0" />
      <scale x="0.008" y="0.008" z="0" />
      <isBillboard>1</isBillboard>
    </png>
  </pngGroup>
</StagePng>
```

#### MOVE_PNGタグ

`#MOVE_PNG:label,generateType,loopTime`のフォーマットで、templateからmovePngデータを生成できます。

各パラメータの意味は以下になります。

| パラメータ名 | 内容 |
| --- | --- |
| label | templateで作成した`pngGroup`の`label`を指定 |
| generateType | 生成方法の指定。`repeat`で`loopTime`毎に次の行の時間まで連続して生成。 `expand`で`endTime`を次の行の時間まで引き伸ばして1つ生成 |
| loopTime | 生成方法が`repeat`のとき、何秒ごとに生成するかの指定。0で1つのみ生成 |

例: *song.lrc*
```
[00:20.00]#MOVE_PNG:chuC1,repeat,4
[00:25.00]
```

出力: *movePng_song.xml*
```
<?xml version="1.0" encoding="utf-8"?>
<StagePng>
  <pngGroup label="chuC1">
    <pngName>エフェクト用png\ちゅ.png</pngName>
    <png startTime="20.0" endTime="21.0">
      <position x="0.03" y="0.42" z="0.31" />
      <rotation x="0" y="180" z="0" />
      <scale x="0.008" y="0.008" z="0" />
      <isBillboard>1</isBillboard>
    </png>
    <png startTime="24.0" endTime="25.0">
      <position x="0.03" y="0.42" z="0.31" />
      <rotation x="0" y="180" z="0" />
      <scale x="0.008" y="0.008" z="0" />
      <isBillboard>1</isBillboard>
    </png>
  </pngGroup>
</StagePng>
```


### 四則演算

`$(演算式)`のフォーマットで四則演算を行うことができます。
主にフェードの計算などで使用しています。

例えば

```
[00:00.00]#END_TIME:67

[00:00.00]## 基本フェード定義
[00:00.00]#FADE_END   = #FADE:$($end-$1-1),$($end+1),$1,0,0  ## 曲終了フェード

[01:07.00]#FADE_END:2
```

と書くと、コンバート時に

```
[01:07.00]#FADE:$(67-2-1),$(67+1),2,0,0
```
↓
```
[01:07.00]#FADE:64,68,2,0,0
```

のように演算処理されます。


## エラー一覧

### 引数が足りません

カスタムタグの引数が足りないときに表示されます。
引数の数を確認してください。

例:
```
[ERROR]引数が足りません tag:#FADE_WHITE line:ふえーどあうと      #FADE_WHITE:2
```

フェード定義は2つの引数を使用しているので、`#FADE_WHITE:2,0`のように2つの引数を指定する必要があります。
```
[00:00.00]#FADE_WHITE = #FADE:$now,$($now+$1+$2),$1,$1,1     ## ホワイトフェード
```


### 未定義のタグ

未定義のタグを使用した場合に出ます。
タグ名が間違っていないか確認してください。

例:
```
[ERROR]未定義のタグ tag:#POSE_HOGE line:ぽーずへんこう      #POSE_HOGE:1.3
```


### 未定義の変数

未定義の変数を使用した場合に出ます。
変数名が間違っていないか確認してください。

例:
```
[ERROR]未定義の変数 name:$hoge line:$hoge,エロ好感２,頬２涙０
```

