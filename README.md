# バ美おじとLLMの壁打ち雑談ラジオ

> バ美おじとLLMが、だいたい何かについて喋っているラジオ。

考えている途中のこと。  
AIとの壁打ち。  
作っているもの。  
日常のどうでもいい話。

まとまることもあれば、まとまらないこともあります。

そんな会話を拾い上げて、キャラクターたちの声でラジオにしています。

通称 **壁ラジ / KabeRadio**。

## About

壁ラジは、あまかわちゃんとLLMの壁打ちから生まれた雑談ラジオです。

もともとはAIとの会話を音声で聞きたかっただけだったはずが、気づけば台本を読み、音声を生成し、キャラクターが口パクし、Podcastと動画まで作るようになりました。

最近では本人が出演しない回まで始まっています。

この先どうなるのかは、本人たちもよく分かっていません。

## Character

- [あまかわちゃん](characters/amakawachan.md)
- [モブ子](characters/mobuko.md)
- [モブ美](characters/mobumi.md)

[CHARACTER一覧 →](characters/README.md)

## Episodes

正式Episodeは`episodes/<episode-key>/`単位で管理します。

[EPISODES →](episodes/README.md)

## 番組の演出

タイトルコール「壁ラジ！」を、6種類のアイキャッチに置き換えられるようになりました。
種類を指定するか、生成時にランダムで選べます。Podcast・動画・Realtime再生で使用します。
対応Runtimeでは、動画に入ったアイキャッチをYouTubeサムネイルにも使用します。

- [アイキャッチの制作ルール](docs/runtime-integration-contract-v1.md)
- [YouTubeサムネイル・公開クレジット](docs/publishing-credits.md)

## 秋シーズン・オープニング

**「秋風のチューニング」 — 壁ラジ Autumn Season Opening Theme**

秋の街、カフェでのひと休み、夕暮れの帰り道、いつものスタジオ。
モブ子が過ごす秋の一日を、少し懐かしく、あたたかなインストゥルメンタルにのせた80秒のオリジナルMVです。

[YouTubeで見る →](https://youtu.be/xJwN_KheKJQ) / [作品紹介 →](extras/autumn-season-opening.md)

## LINEスタンプ

モブ子スタンプは発売中です。壁ラジスタンプ Vol.1・Vol.2 はともに審査中です。

[LINEスタンプの案内](extras/line-stickers.md)

## 配信先

公開動画へのリンクをまとめています。Spotifyへのリンクは準備中です。

[LISTEN / WATCH →](links/README.md)

## About this repository

このRepositoryは、壁ラジの公式アーカイブ兼設定資料であり、将来の公式サイト用Canonical Sourceです。

番組情報、エピソード、台本、キャラクター設定などを記録します。

このRepositoryは現在の可視性設定にかかわらず、**常に外部公開可能な内容だけを保存するPublic-facing Sourceとして扱います**。実行環境・認証情報・セキュリティ設定・個人環境固有情報は保存しません。

### Security / Publication Policy

このRepositoryへ、以下の情報を追加してはいけません。

- API key、Access token、Bot token、Password、Secret、Credential
- Telegram等のUser ID / Chat ID、Allowlist、認証用識別子
- ローカル絶対パス、PCユーザー名、端末固有パス、TTS executable path
- `config.local.json`、`.env`、秘密鍵、証明書などの環境固有設定
- 内部管理URL、非公開Endpoint、運用上のセキュリティ構成
- 公開を意図していない個人情報・家族情報・勤務先情報・位置情報
- その他、RepositoryをPublic化した際に公開すべきでない情報

これらは`amakawa-chan/amakawachan-assistant`側のRuntime、環境変数、ローカル設定、または適切なSecret管理へ分離します。

台本・Character Profile・Episode Packageについても、コミット前に「公式サイトから公開されても問題ない内容か」を基準に確認します。Git履歴に残ることを前提とし、秘密情報を一度でもコミットしない運用を優先します。

キャラクターの性格や関係性は最初からすべて決められているわけではありません。実際のエピソードを通じて生まれた設定が、後からCharacter Profileへ追加されることがあります。

その変化も含めて、壁ラジです。

更新履歴はGitのコミット履歴を正本とし、専用NEWSの二重管理は行いません。将来GitHub Pages化する場合は、Git履歴をUPDATE表示へ利用する想定です。

## Script Production

「壁ラジ台本にして」「壁ラジ化して」「ラジオ用の台本にして」「GitHubの壁ラジ仕様を確認して台本化して」など、正式Episodeを作る依頼はこのRepositoryをコンテンツ正本として扱います。

入口がAmakawachan Radio / Assistant側だった場合も、正式Episodeはここへ戻し、現行のWorkflow / Prompt / Converterを確認してから`episodes/<episode-key>/`へ保存します。版や契約が更新されている場合は固定された旧手順ではなくRepository上の現行正本を優先します。

読む順序:

1. [ChatGPTから正式台本を保存する手順](docs/chatgpt-episode-package-workflow-v1.md)
2. [ChatGPT Episode Package Generator](prompts/chatgpt-episode-package-v1.md)
3. [Canonical Script Converter v0.4](docs/canonical-script-converter-v0.4.md)
4. [Episode Package Template](templates/episode-package/)

## Runtime / Environment

壁ラジのコンテンツはこのRepositoryを正本とし、Podcast / Video / Remote Production / Telegramなどの制作Runtimeは`amakawa-chan/amakawachan-assistant`側で実行します。

Repository間の責務、M6環境設定、Archive / Delivery、Casting / Voiceの境界は次を正本とします。

- [KabeRadio / Amakawachan Radio Runtime Integration Contract v1](docs/runtime-integration-contract-v1.md)
