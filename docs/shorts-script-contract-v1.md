# 壁ラジ Shorts 台本契約 v1

## 制作の流れ

台本生成時にLLMが0〜3件のClip候補を提案する方式をPrimaryとします。
完成後の追加解析はSecondary（将来拡張）です。公開判断と候補抽出は分離します。

1. 会話本文を完成させ、Parserの1始まりのTurn番号を数える。
2. 独立して伝わるフックからオチ・結論までを候補にする。
3. 台本と候補を確認し、ローカル動画にする候補を `selectedClipIds` に指定する。
4. Runtimeで音声生成 → 音声差異の調整 → 本編動画 → 完成本編からShorts生成。
5. 完成動画を確認してから、別の公開操作へ進む。生成だけでは投稿しない。

「同時生成」は1回の生成操作を意味します。Shorts専用のTTSや別の音声調整は行いません。
GUIはアプリで選択したCasting・音声設定、Remoteは `production.json.casting` と
Runtimeの音声設定を使用します。GUIで台本を開くだけではRemoteのCastingを適用しません。

## 台本内の設定

`script.md` 冒頭にJSON形式のFront Matter（YAMLとしても有効）を置きます。
本文・概要・発話見出しは従来どおりです。Front Matterは読み上げません。
通常のYAMLキー記法の中へこのオブジェクトを混在させないでください。

```json
{
  "radioProduction": {
    "schemaVersion": 1,
    "selectionMethod": "script-primary-reviewed",
    "audioAdjustment": { "mode": "auto", "targetRmsDbfs": -23 },
    "selectedClipIds": ["start-small"],
    "clips": [
      {
        "id": "start-small",
        "title": "準備で満足してしまう話",
        "displayTitle": "準備だけで\n満足してない？",
        "startTurn": 6,
        "endTurn": 9,
        "hook": "片付けただけで満足する身近な失敗から始める",
        "point": "最初の一行を書こう、まで会話が着地する",
        "targetDuration": 40,
        "platforms": ["youtube-shorts"]
      }
    ]
  }
}
```

実際の台本では、このJSONの前後をそれぞれ独立した `---` 行で囲みます。
上のTurn番号は形式例です。自分の台本の番号へ必ず置き換えます。

| 項目 | ルール |
|---|---|
| `episodeNumber` | 任意・通常は省略。生成動画に番号を焼かず、投稿時に採番する。既存の明示指定は互換用 |
| `id` | 英数字で開始し、英数字・`_`・`-`のみ、64文字以内。一意にする |
| `title` | Clipの管理用タイトル。本文にない主張や過度な煽りを足さない |
| `displayTitle` | 画面用見出し。1〜2行、1行9文字以内。推奨6〜8文字、`\n`で改行 |
| `startTurn` / `endTurn` | Parser文書順、1始まり、両端を含む整数 |
| `hook` / `point` | 選定理由の編集メモ。映像に表示せず、読み上げない |
| `targetDuration` | 30〜60秒を目安とする編集上の目標。実時間は音声生成後に決まる |
| `platforms` | 編集上の配信先候補。自動投稿を有効にする設定ではない |
| `selectedClipIds` | ローカル生成の対象。空配列は未採用。公開の許可ではない |

台本の `### Host` / `### Guest` が各1 Turn、`### Host + Guest` も親Turnとして1件です。
タイトルコールも数え、CAST行・説明文・章見出しは数えません。
本文を増減・並べ替えたら、候補範囲も再確認します。時間に合わせた早送りや文途中の切断はしません。
候補を作るために会話を水増しせず、適切な範囲がない場合は `clips: []` を正常結果とします。

## 投稿番号との分離

新しい台本のClip設定にはEpisode番号を持たせません。番号未設定でも採用Clipを生成します。
投稿時にRuntimeの公開画面で番号を自動取得・確認し、投稿タイトルへ付けます。
生成動画に番号を焼き込まないため、投稿順が変わっても再レンダー不要です。

## 固定デザイン

1080×1920、上部に専用「壁ラジ切り抜き」ステッカー・見出し、中央に
本編16:9、下部に色が流れる `#壁ラジ` ロゴ・既存の踊るモブ子・固定CTAを配置します。
本編の焼き込み字幕を保持します。Shorts専用の概要、追加字幕、ナレーション、画像生成は不要です。
新しい台本で `template` / `bodyMode` を指定する必要はありません。Runtimeの既定デザインを使います。

## 音声と互換性

`audioAdjustment` の例は話者間の自動RMS補正です。声質を変更する指定ではありません。
目標は-30〜-16 dBFS、ピーク保護は-1 dBFS。省略時はGUIの従来の音声確認を使用します。
同時発話の自動補正は未対応です。含む台本ではこの指定を省略して手動確認するか、
通常の交互発話へ編集してください。未対応音声を勝手に未補正へ切り替えません。

設定なしの既存Episodeは引き続き本編のみ生成します。既存Episodeへ一括で設定を追加しません。
補正済みMP3はRuntimeの `podcast-adjusted.mp3` に保存します。元のPodcastと既存Delivery契約は維持し、
補正済みPodcast・Shortsの自動Deliveryや投稿は別の拡張とします。

## Repository境界

KabeRadioに置くのは公開できる台本・選定意図だけです。Credential、Provider/Style ID、
token、ローカルパス、素材ファイル指定、レンダーreceiptは置きません。
素材・FFmpeg・設定・検証・時間解決はAssistant Runtimeが管理します。
自己参照になるためLLMは `source.sha256` を記入しません。Runtimeが確定入力から計算します。

既存の `clip-candidates.json` 方式もRuntimeで利用できますが、台本内設定とは併用しません。
新しいEpisode Packageは従来の3ファイルのまま作成します。

Shorts失敗でも本編は保持されます。Runtimeの `shorts-generation.json` で状態を確認し、
単独Shorts CLIで再試行します。既存成果物と異なる入力は新しいClip IDで生成します。
