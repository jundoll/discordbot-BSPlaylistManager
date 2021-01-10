# discordbot-BSPlaylistManager
discord上でBeat Saberのプレイリストを管理するbotです。  
herokuとdropboxを利用しています。


## 目次
#### 追加系
- [/add](#add)
- [/add pl](#add_pl)
- [/regist](#regist)
#### 削除系
- [/del](#del)
- [/del pl](#del_pl)
- [/rst](#rst)
#### 更新系
- [/upd](#upd)
- [/upd name](#upd_name)
- [/upd key](#upd_key)
- [/upd title](#upd_title)
- [/upd author](#upd_author)
- [/upd desc](#upd_desc)
- [/upd img](#upd_img)
#### その他
- [/dl](#dl)
- [/search](#search)
- [/usage](#usage)
- [/ping](#ping)


## 各コマンドの説明
### /add
<a id="add"></a>
```
/add [KEYWORD] [URL]
```
指定した曲またはMapperの曲全てを、指定のプレイリストに追加します。
|引数|説明|
|----|----|
|KEYWORD|プレイリストの検索用キーワードです。|
|URL|曲による指定とMapperによる指定が可能です。<br>曲の場合は、[beatsaver.com](https://beatsaver.com/)または[bsaber.com](https://bsaber.com/)の各曲ページのURLを指定してください。<br>Mapperの場合は、[beatsaver.com](https://beatsaver.com/)の各MapperページのURLを指定してください。

### /add pl
<a id="add_pl"></a>
```
/add pl [KEYWORD]
```
指定のプレイリストを新規作成します。
|引数|説明|
|----|----|
|KEYWORD|プレイリストの検索用キーワードです。|

### /regist (/register)
<a id="regist"></a>
```
/regist [KEYWORD] ([PLAYLIST_FILE])
```
既存のプレイリストを登録します。  
プレイリストは次のどちらかで指定してください。  
プレイリストはjson形式のみ対応しています。
1. PLAYLIST_FILE にプレイリストのURLを指定します。
2. ファイルアップロード時に入力できるコメントにコマンドを指定します。<br>その際、PLAYLIST_FILEは不要です。

|引数|説明|
|----|----|
|KEYWORD|プレイリストの検索用キーワードです。|
|[option]<br>PLAYLIST_FILE|任意の指定項目です。<br>指定方法1の場合に利用してください。|

### /del (/delete)
<a id="del"></a>
```
/del [KEYWORD] [URL]
```
指定した曲またはMapperの曲全てを、指定のプレイリストから削除します。
|引数|説明|
|----|----|
|KEYWORD|プレイリストの検索用キーワードです。|
|URL|曲による指定とMapperによる指定が可能です。<br>曲の場合は、[beatsaver.com](https://beatsaver.com/)または[bsaber.com](https://bsaber.com/)の各曲ページのURLを指定してください。<br>Mapperの場合は、[beatsaver.com](https://beatsaver.com/)の各MapperページのURLを指定してください。

### /del pl (/del playlist)
<a id="del_pl"></a>
```
/del pl [KEYWORD]
```
指定タイトルのプレイリストを削除します。
|引数|説明|
|----|----|
|KEYWORD|プレイリストの検索用キーワードです。|

### /rst (/restore)
<a id="rst"></a>
```
/rst [KEYWORD]
```
指定のプレイリストを復元します。
同じ検索用キーワードのプレイリストが新規作成されるまでは復元可能です。
|引数|説明|
|----|----|
|KEYWORD|プレイリストの検索用キーワードです。|

### /upd (/up, /update)
<a id="upd"></a>
プレイリスト情報を更新します。  
更新する情報に対応するコマンドを利用してください。

### /upd name (/upd f, /upd file, /upd filename)
<a id="upd_name"></a>
```
/upd name [KEYWORD] [NEW_NAME]
```
指定のプレイリストのファイル名を更新します。
|引数|説明|
|----|----|
|KEYWORD|プレイリストの検索用キーワードです。|
|NEW_NAME|更新後のファイル名です。<br>拡張子(.json)は含めないでください。|

### /upd key (/upd k, /upd keyword)
<a id="upd_key"></a>
```
/upd key [KEYWORD] [NEW_KEYWORD]
```
指定のプレイリストの検索用キーワードを更新します。
|引数|説明|
|----|----|
|KEYWORD|プレイリストの検索用キーワードです。|
|NEW_KEYWORD|更新後の検索用キーワードです。|

### /upd title (/upd t)
<a id="upd_title"></a>
```
/upd title [KEYWORD] [NEW_TITLE]
```
指定のプレイリストのタイトルを更新します。
|引数|説明|
|----|----|
|KEYWORD|プレイリストの検索用キーワードです。|
|NEW_TITLE|更新後のタイトルです。|

### /upd author (/upd a)
<a id="upd_author"></a>
```
/upd author [KEYWORD] [NEW_AUTHOR]
```
指定のプレイリストの作成者名を更新します。
|引数|説明|
|----|----|
|KEYWORD|プレイリストの検索用キーワードです。|
|NEW_AUTHOR|更新後の作成者名です。|

### /upd desc (/upd d, /upd description)
<a id="upd_desc"></a>
```
/upd desc [KEYWORD] [NEW_DESC]
```
指定のプレイリストの説明を更新します。
|引数|説明|
|----|----|
|KEYWORD|プレイリストの検索用キーワードです。|
|NEW_DESC|更新後の説明です。<br>スペースを空ける場合などは""で囲んでください。|

### /upd img (/upd i, /upd image)
<a id="upd_img"></a>
```
/upd img [KEYWORD] ([NEW_IMG])
```
指定のプレイリストのサムネイル画像を更新します。  
画像は次のどちらかで指定してください。
1. NEW_IMG にサムネイル画像(pngまたはjpeg)のURLを指定します。
2. ファイルアップロード時に入力できるコメントにコマンドを指定します。<br>その際、NEW_IMGは不要です。

|引数|説明|
|----|----|
|KEYWORD|プレイリストの検索用キーワードです。|
|[option]<br>NEW_IMG|任意の指定項目です。<br>指定方法1の場合に利用してください。|

### /dl (/download)
<a id="dl"></a>
```
/dl [KEYWORD]
```
指定のプレイリストのダウンロードリンクを返します。
|引数|説明|
|----|----|
|KEYWORD|プレイリストの検索用キーワードです。|

### /search
<a id="search"></a>
```
/search [SEARCH_KEYWORD]
```
検索用キーワードに一致した全てのプレイリスト情報を返します。
|引数|説明|
|----|----|
|SEARCH_KEYWORD|プレイリストの検索用キーワードです。<br>ワイルドカード(*)を使った検索が可能です。|

### /usage
<a id="usage"></a>
```
/usage
```
使い方の案内として、このREADMEへのリンクを返します。

### /ping
<a id="ping"></a>
```
/ping
```
pongと返します。疎通確認用です。

