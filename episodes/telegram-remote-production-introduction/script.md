# Telegramから壁ラジ制作を呼び出せるようになりました

## Episode Description

壁ラジの正式台本を、Radioアプリを開かずM6でPodcastと動画にするRemote Production。今回はその入口をTelegramへつなぎました。勝手な実行や二重Renderを防ぎながら、外から制作状況を確認し、一度だけRenderしてiCloudへ届ける仕組みを紹介します。

## 本編

### Host

壁ラジ制作、ついにTelegramから呼び出せるところまで来ました。

### Guest

外出先から、M6にあるRadioのボタンを遠隔操作するんですか。

### Host

ボタンは触らんよ。既存のRadio Coreを使うCLIへ、Telegramの入口を付けた。

### Guest

GUIを無理やり自動操作しないのは大事ですね。

### Host

コマンドは、一覧、状態確認、キャスト変更、準備、Render、再Deliveryだけ。

### Guest

送られてきた文字を、そのままPowerShellとして実行したりは。

### Host

しません。決めた形式だけ解析して、Chat IDとUser IDも許可リストで確認します。

### Guest

では、知らない人がBotを見つけても制作は動かせない。

### Host

そう。しかもRenderは、最後に小文字のconfirmを付けないと開始しない。

### Guest

うっかり送信対策ですね。長い音声と動画を何度も作ったら大変ですから。

### Host

処理済みのTelegram Updateも保存するから、返信だけ失敗して同じRenderを繰り返すのも防ぐ。

### Guest

Render済み成果物の正本は、これまで通りM6のLocal Archiveですか。

### Host

うん。iCloudには投稿用の五ファイルだけコピーする。同期に失敗したら、再Renderせずdeliverだけやり直す。

### Guest

音声エンジンは事前にRadioアプリを開いておく必要がありますか。

### Host

ないよ。必要になったVOICEVOXやAivisSpeechを、共有Coreがバックグラウンドで準備する。

### Guest

ではこの回そのものをTelegramから一度だけRenderして、仕組みが本当に通るか確認しましょう。
