# 壁ラジアーカイブス台本契約 v1

「15秒だけ壁ラジを浴びる。」勢いよく始まり、勢い余って終わる。会話の真ん中へ突然放り込まれる、短く慌ただしい予告編です。通常の切り抜きの要約・完結版にはしません。

正本: [制作Issue #31](https://github.com/amakawa-chan/KabeRadio/issues/31) と追加コメント。映像仕様は [Radio #99](https://github.com/amakawa-chan/amakawachan-assistant/issues/99)。台本作成はChatGPT/Codexとこのリポジトリで行い、RadioにはAI台本生成を追加しません。

## 選定と編集

1. `episodes/*/script.md` をランダムに再評価し、疑問・共感・意外性・ツッコミ・認識のズレ・くだらない一言のある箇所を探します。通常Shorts採用済みTurnも候補に含めます。
2. 会話本文は概ね10〜15秒相当、出発点は約60〜100文字（話速、間、同時発話で大きく変わります）。文字数で秒数を保証せず、TTS実時間を正とします。冒頭0.6〜1.2秒とCTA約0.5〜1秒は別で、全体12〜20秒程度は目安です。
3. 元の口語・変な間・認識のズレを残します。綺麗な導入、オチ、締め、追加ナレーション、本文の「壁ラジ！」タイトルコールは足しません。会話の途中、文の途中でも自然な語句の境界なら終えて構いません。単語途中の切断、意味・発言意図の捏造、理解不能な接ぎ合わせは禁止します。
4. 元エピソードと1始まりの出典Turnを照合します。同時発話は親Turnを1件、CAST・章は数えません。Host / Guest / Host + Guestと必要なCASTを保持します。元のCASTが途中にあれば抜粋冒頭で有効なCASTも復元します。
5. 再利用・通常Shortsとの重複は許可します。直近アーカイブスと会話本文が完全一致する候補は警告して別候補も検討します。重複自体を禁止せず、同じ素材だけに偏らないようにします。

## 保存とFront Matter

制作日の日本時間で `archives/YYYYMMDD/` に1〜3本保存します。直下の一意な `<id>.md`、または `<id>/script.md` を使用し、両方式を重ねて同じ台本を保存しません。同じフォルダの台本は合計最大3本、IDは一意です。Runtime出力はここへ保存しません。

Radioの既存Canonical ParserがFront Matterを読み飛ばす契約を維持し、`---` で囲む**JSONオブジェクトのみ**をアーカイブスメタデータの形式とします。任意のYAML、別JSON sidecarとの混在はしません。本文は既存の `## 本編`、`### Host` / `### Guest` / `### Host + Guest`、`[CAST: Host=pack-id]` を使用します。Episode Packageの3ファイル契約や通常Shortsの `radioProduction` は変更しません。

`radioArchives` オブジェクト:

| フィールド | 契約 |
|---|---|
| `schemaVersion` | 数値 `1` |
| `id` | 1〜64文字、小文字英数字とハイフン。先頭は英数字 |
| `title` | 管理・投稿用タイトル（必須） |
| `displayTitle` | 映像用の短い見出し（必須） |
| `series` | `壁ラジアーカイブス` |
| `sourceEpisodeKey` | `episodes/<key>/script.md` のキー（必須） |
| `sourceTurns` | 正の整数配列、元の1始まりTurn番号。収録順で記載 |
| `sourceYouTubeVideoId` | 元本編の11文字ID、確認できなければ空文字 |
| `sourceYouTubeUrl` | 元本編のYouTube URL、確認できなければ空文字。IDと両方書く場合は一致 |
| `renderPreset` | `archives-speaker-follow` |
| `cta` | `blur-related-video` |

元動画URL/IDは確認できる公開記録からのみ取得します。推測・架空IDは保存しません。空欄でも候補を保存・レンダーできますが、投稿前には同じチャンネルの公開／限定公開動画として存在・権限を確認する必要があります。Shorts関連動画の設定はアップロード成功とは別で、現行RuntimeはYouTube Studioでの手動設定待ちを記録します。

## Runtimeとの境界

新しい独立したCanonical台本からTTS→Manifest→1080×1920映像を作ります。完成した元動画のクロップ・切り抜き時刻を指定しません。Host/Guestのアップ、短い相槌のカット抑制、同時発話2人表示、固定字幕、ミニアイキャッチOFF／固定／ランダム、最後のブラーCTAはRadioが担当します。

素材ID・抽選結果・素材hash・実尺・音声設定・公開日時・投稿receiptはRuntimeのローカル記録です。台本へ認証情報、秘密情報、端末の絶対パス、ローカル設定、生成音声・映像を書き戻しません。ChatGPT/Codexで台本を作った場合も、Gitへのcommit/pushはユーザーの指示に従います。

## 例と確認

- [テンプレート](../templates/archives/script.md)
- [1本から使える3本例](../archives/20261017/README.md)。各ファイルは元台本のセリフとTurnを直接照合でき、途中終了例を含みます。元動画未確認のためID/URLは空欄です。
- [制作プロンプト](../prompts/chatgpt-archives-v1.md)

保存前にCanonicalで発話が読めること、出典との一致、CAST、ID/URLの一致、直近重複、公開情報だけであることを確認します。実TTS後の尺と字幕の可読性はRuntimeでレビューします。
