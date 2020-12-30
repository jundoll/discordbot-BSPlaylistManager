# discordbot-BSPlaylistManager

## 説明
discord上でBeat Saberのプレイリストを管理するbotです。  
herokuとdropboxを利用しています。


## コマンドリスト
### /add
```
/add [Title] [URL]
```
Titleは、管理しているプレイリストのタイトルです。  
URLは、[bsaber.com](https://bsaber.com/)の曲ページのURLです。  
URLの曲が指定のプレイリストに追加されます。
<!--mapperのURLを入れたらその人の曲全てを追加するとか。評価などフィルタできた方がいいか？→その基準は共通設定値でいいか。-->

### /add pl
```
/add pl [Title]
```
Titleは、管理しているプレイリストのタイトルです。  
指定タイトルのプレイリストが新規作成されます。

### /del (/delete)
```
/del [Title] [URL]
```
Titleは、管理しているプレイリストのタイトルです。  
URLは、[bsaber.com](https://bsaber.com/)の曲ページのURLです。  
URLの曲が指定のプレイリストから削除されます。

### /del pl (/delete pl)
```
/del pl [Title]
```
Titleは、管理しているプレイリストのタイトルです。  
指定タイトルのプレイリストが削除されます。

### /dl (/download)
```
/dl [Title]
```
指定タイトルのプレイリストのダウンロードリンクを返します。

### /ping
```
/ping
```
pongと返します。疎通確認用です。

