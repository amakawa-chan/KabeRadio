# Publishing Credits

KabeRadioのYouTube / Spotify等で使用する概要欄・クレジットのCanonicalな方針を定義する。

## 基本方針

公開用概要欄は、固定情報とEpisodeごとに変化する情報を分離する。

手動更新を前提とする情報を増やさず、Amakawachan Radioから取得できる情報は将来的に自動生成する。

概ね以下を組み合わせて公開用テキストを生成する。

```text
Episode Description
+
Cast / Voice Credits
+
Fixed Production Credits
+
hashtags
```

## Episodeごとに変化する情報

以下はKabeRadioの固定テンプレートへ直接埋め込まず、Amakawachan Radio側のCasting / Character Pack / Render情報から解決することを目標とする。

- Host / Guestのキャラクター
- 表示名
- 使用TTS engine
- voice / model / style名
- voice model等のcredit URL（存在する場合）
- Renderに使用したAmakawachan Radio version
- 必要に応じて、その回だけ使用した素材情報

Character Packに`defaultVoice`を持たせる場合、公開クレジット生成に必要なmetadataも同じ境界から取得できる構造を検討する。

例：

- `engineName`
- `creditName`
- `creditUrl`
- voice / model / styleを特定する情報

実際のRenderでvoice overrideを使用した場合は、Pack defaultではなく実際に使用したvoice設定とクレジットが一致することを優先する。

## 固定クレジット

以下のような番組全体で繰り返し使用する情報は、このドキュメントをCanonical Sourceとして管理する。

### キャラクターイラスト

画像生成・制作：PixAI

https://pixai.art/

### Radio Studio背景

イマテカ商店 / 多重人格Vtuber「りべるりべる」

「【配信画面テンプレート】ラジオ局風コラボ画面【Vtuber向け】」

https://booth.pm/ja/items/2822617

(c)Imateka_L_Liebe

### 音声合成

VOICEVOX

https://voicevox.hiroshiba.jp/

AivisSpeech

https://aivis-project.com/AivisSpeech

## 現行の概要欄構成

### YouTube

```text
【壁ラジ】#<episode>

■ 出演・音声

<Cast / Voice Credits>

■ キャラクターイラスト

<Fixed Character Art Credit>

■ Radio Studio背景

<Fixed Radio Studio Credit>

■ 音声合成

<Fixed TTS Credits>

■ 制作

Amakawachan Radio <rendered version>

#壁ラジ #VOICEVOX #AivisSpeech
```

必要な場合のみ、実際の出演キャラクター・音声に対応したハッシュタグを追加する。

### Spotify

```text
【壁ラジ】#<episode>

■ 出演・音声

<Cast / Voice Credits>

■ 音声合成

<Fixed TTS Credits>

■ 制作

Amakawachan Radio <rendered version>
```

SpotifyではYouTubeより簡潔なクレジット構成を基本とする。

## Current Voice Credit Example

現行のモブ子音声で使用しているAivisSpeechモデル：

- モブ子（Guest / LLM）
- AivisSpeech：まお
- https://hub.aivis-project.com/aivm-models/a59cb814-0083-4369-8542-f51a29e72af7?owner=ozchat

この情報は固定のEpisodeテンプレートへ埋め込まず、Character Pack / voice profile側から解決できる形への移行を目標とする。

## 公開後リンク

Spotify / YouTubeの各Episode URLなど、公開後に手動で追加する必要がある情報は必須項目にしない。

自動取得・自動同期できる仕組みを実装した場合に、GitHub Pages等の表示層へ追加する。

チャンネル・番組全体へのリンクは`links/`で管理する。

## Principle

> 固定クレジットはKabeRadioで管理し、Episode依存のクレジットはRender時の実データから生成する。

手作業で概要欄を同期し続ける構造を避け、実際に使用したキャラクター・音声・バージョンと公開クレジットが一致することを優先する。
