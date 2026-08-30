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

## Listen / Watch

YouTube / Spotifyへのリンクは後日設定します。

[LISTEN / WATCH →](links/README.md)

## About this repository

このRepositoryは、壁ラジの公式アーカイブ兼設定資料です。

番組情報、エピソード、台本、キャラクター設定などを記録します。

キャラクターの性格や関係性は最初からすべて決められているわけではありません。実際のエピソードを通じて生まれた設定が、後からCharacter Profileへ追加されることがあります。

その変化も含めて、壁ラジです。

更新履歴はGitのコミット履歴を正本とし、専用NEWSの二重管理は行いません。将来GitHub Pages化する場合は、Git履歴をUPDATE表示へ利用する想定です。

## Script Production

- [ChatGPTから正式台本を保存する手順](docs/chatgpt-episode-package-workflow-v1.md)
- [ChatGPT Episode Package Generator](prompts/chatgpt-episode-package-v1.md)
- [Canonical Script Converter v0.4](docs/canonical-script-converter-v0.4.md)
- [Episode Package Template](templates/episode-package/)

## Runtime / Environment

壁ラジのコンテンツはこのRepositoryを正本とし、Podcast / Video / Remote Production / Telegramなどの制作Runtimeは`amakawa-chan/amakawachan-assistant`側で実行します。

Repository間の責務、M6環境設定、Archive / Delivery、Casting / Voiceの境界は次を正本とします。

- [KabeRadio / Amakawachan Radio Runtime Integration Contract v1](docs/runtime-integration-contract-v1.md)
