# Issue #33 調査・技術検証・設計（2026-10-21）

対象: https://github.com/amakawa-chan/KabeRadio/issues/33

この文書は初回Spike時点の調査記録です。その後、固定画像・クレジット3秒化・生成前の選択UI・台本ごとの特別画像設定を実装しました。現在の操作と検証範囲は[固定カードの説明](../extras/endcards/fixed-aftertalk-v1/README.md)とIssue #33の追記を参照してください。以下の「未変更・未実装」は初回調査時点を指します。

## 結論

既存のOUTROレンダラー、Git台本取得、noteバナーギャラリー、投稿receipt、Studio関連動画ワーカーを拡張する構成を推奨する。新しい投稿サービス・画像管理サービス・Episode Event構文は不要。

- **動画演出は実現可能**。既存静止画で6秒固定／5秒保持＋1秒遷移＋6秒背景の最小MP4を実生成した。
- **公式Data APIに終了画面設定用の公開リソース・更新フィールドはない**。アップロード・予約・概要欄は既存API処理、終了画面は別工程にする。
- **Studioに「動画からインポート」が実在することを実画面で確認**。ただし今回選んだ元動画には終了画面がなく、複製成功・保存・再読込後の維持までは未検証。
- MVPは「6秒固定背景＋Studio手動設定支援」。任意アセットと個別演出を追加し、自動保存は実機検証・規約面の確認後に独立機能として進める。

本番コード・設定・投稿・公開状態を変更していない。Gitのcommit/push、画像公開、新規Issue作成もしていない。以下のJSON・状態名・ファイル追加案は設計案であり、実装済み機能ではない。

## 1. 調査した既存実装

KabeRadio checkoutは `8dadf32`。調査時GitHub mainは `927b3c0a60ac8da3633ad86d5d8c9fe3169ee6ee`。比較で、その間にEpisode・note・workflow文書が追加されていることを確認。Runtime GitHub mainは `3322f74cb875b194debe7b88e673c0498a466bf9`。

|責務|既存箇所・確認結果|拡張方針|
|---|---|---|
|コンテンツとRuntimeの境界|KabeRadio `docs/runtime-integration-contract-v1.md`。正式入力は `episodes/<key>/{README.md,script.md,production.json}`、実行はAssistant|画像はExtrasへ置き、台本から参照。Runtime receiptと認証情報をコンテンツrepoに持ち込まない|
|Canonical本文|Assistant `Radio/RadioCore.ps1: ConvertFrom-RadioMarkdownDocument`。`[OUTRO: preset]`をeventとして解析|新しい演出タグを増やさず既存OUTROを使用|
|台本内JSON|`Radio/EpisodeProductionCore.ps1: Read-RadioEpisodeProduction`。`radioProduction.schemaVersion=1`、音声調整・Shorts候補。sidecarとの二重指定を拒否|同じJSON front matterに公開可能なassets/endCard設定を追加し、共通resolverへ渡す。現状はアセット自動解決を実装していない|
|設定・動画入口|`Radio/config.json` のoutro presetは静止画＋**5秒**。`Radio.ps1` の `Start-VideoRender` 周辺、`RemoteProductionCore.ps1: Get-RemoteRadioOutro / Invoke-RemoteRadioVideoRender` が解決|desktop/remote双方から同じresolverを呼ぶ。新しい明示presetを6秒にし旧presetを勝手に変えない|
|タイムライン・合成|`Radio/VideoRenderCore.ps1: Get-RadioVideoTimeline` は本編→credits→endcard。`New-RadioVideoFfmpegArguments` は静止画loop/overlay、音声apad、H.264/AAC。OPは最後にconcat|既存Outroを段階化。OP加算後の完成動画尺でYouTube時刻を計算|
|生成の連携|`Radio/EpisodeRenderCore.ps1`、`EpisodeProductionCore.ps1`、`Radio.ps1`|音声再利用、完成動画の識別、映像確認の失効を既存フローに接続。Shortsへ12秒カードを自動付加しない|
|Git台本取得|`Radio/GitEpisodeCore.ps1: Invoke-RadioEpisodeGit / Show-RadioGitEpisodes`、`remoteProduction.kabeRadioRepository`|既存cloneとGit認証を再利用。アセットだけの第二OAuthを作らない|
|概要欄|`Radio/DescriptionExportCore.ps1: Resolve-RadioEpisodeMetadata / ConvertTo-RadioDescriptionText / Write-RadioPublishingPackage`|YouTube向け生成箇所にギャラリーブロックを追加。現状のmetadata resolverはJSON assetsを自動転送しないため明示的な配線が必要|
|投稿と予約|`Radio/tools/publish-radio.py: prepare / upload`、`youtube_batch.py`、`PublishingReviewCore.ps1`。アップロードreceiptと独立したShorts処理|動画ID確定後に終了画面タスクを作る。アップロード再実行をリトライ手段にしない|
|Studio自動化|`Radio/tools/studio-related-video.py`。専用永続プロファイル、profile lock、チャンネル照合、保存後再読込。`publish-archives.py` / `youtube_batch.py`から接続|プロファイル・lock・認証エラー分類を共通化し、終了画面adapterを追加。関連動画用セレクターと保存検証を流用しない|
|既存画像|KabeRadio `extras/endcards/README.md` と1920×1080の秋カード|既存保管場所をエピソード別に拡張。旧画像を移動して参照を壊さない|
|ギャラリー・note|`extras/gallery/README.md`、`extras/gallery/note-banners/{README.md,index.html}`、`note-article-pop/`。記事用1280×670、プロフィール用1920×1006等|エピソード用noteバナーを既存一覧へ追加。用途の異なるサイズを混同しない|
|note取得|`tools/build-note-catalog.cjs`、`.github/workflows/note-catalog.yml`、`notes/catalog.json`|一覧は静的カタログ方式を踏襲。画像ごとのGitHub履歴取得を追加しない|

関連Issueを確認: KabeRadio #21（予約）、#24（Shorts関連動画）、#31（アーカイブ契約）、Assistant #47（Media Library/OUTRO）。特に #47 は「OUTROがない台本へ暗黙追加しない」「実ファイルパスを台詞へ書かない」を定義している。通常回の6秒化は、新規テンプレートでOUTROを明示する方式とし、既存台本を読むだけで挙動を変えない。

### 通常起動先

デスクトップの `Amakawachan Radio.lnk` → `remote-production-pr-worktree/KawaiiLauncher.vbs` → `KawaiiLauncher.ps1` のRadio項目 → `Radio/launcher.ps1` → 同じディレクトリの `Radio.ps1` を追跡した。

起動先checkoutのHEADは `e75521c` で、多数の既存ローカル変更を含む。単なるHEADだけで実機内容を判断しない。GitHub mainとの比較では、`VideoRenderCore.ps1`、`EpisodeProductionCore.ps1`、`DescriptionExportCore.ps1`は改行正規化後一致。一方 `publish-radio.py` と `youtube_batch.py` は異なり、起動先には予約日時処理や概要欄追記等の差分がある。今回は調査のみで反映作業なし。後続実装では差分を保護し、必要箇所だけ実起動先にも反映する。

## 2. YouTube終了画面：資料・実画面・未検証の区別

### 公式資料

- [終了画面ヘルプ](https://support.google.com/youtube/answer/6388789?hl=ja): 最後の5〜20秒、動画全長25秒以上、16:9では最大4要素。おすすめ動画・再生リスト・登録の3要素は仕様上収まる。子ども向け等は利用不可。モバイルWeb等に表示制限があり、端末や視聴条件により表示が変わり得る。
- [アップロード手順](https://support.google.com/youtube/answer/57407?hl=en): 公開設定選択前に終了画面を追加する工程があり、その後に限定公開・予約を選べる。**公開前設定が可能な設計と推定できるが、予約済み動画へのインポート保存を実証した資料ではない**。
- [Videos resource](https://developers.google.com/youtube/v3/docs/videos) と [videos.update](https://developers.google.com/youtube/v3/docs/videos/update): 終了画面用の公開フィールドなし。予約はprivate＋publishAt。APIで終了画面の保存結果を照合できるとも扱わない。Analyticsの終了画面指標は設定APIの代替ではない。
- [YouTube利用規約](https://www.youtube.com/static?template=terms): 自動アクセスに制限がある。自己所有チャンネル・ユーザー操作開始・既存Playwright実装があることだけで、UI自動化が許諾済みとは判断できない。無人自動適用の導入前に適用条件／必要な許可を確認する。非公開Studio APIの直接呼出しや認証回避は設計に含めない。

### 今回の実画面確認（保存なし）

ログイン済みEdgeの壁ラジチャンネルで確認した。新規タブから動画編集URLを開いた最初の試行はエラーになったが、既存のStudioタブからリンクをたどると編集画面へ到達できた。原因は未特定であり、認証障害と断定しない。

|項目|今回の結果|
|---|---|
|公開動画の終了画面エディタ|既存の公開回（#33 定食の呪い）で開けた|
|標準テンプレート|「1 本の動画, 1 個の再生リスト, 1 件のチャンネル登録」を実画面で確認|
|過去動画から再利用|「動画からインポート」を押すと「特定の動画の選択」と検索欄・候補一覧が開いた|
|元動画選択|既存公開回 #32 を選ぶと「この動画にはインポート可能な終了画面がありません」と表示。候補一覧への掲載はインポート可能性の保証ではない|
|限定公開への適用|既存の限定公開配信アーカイブ1本で、終了画面エディタとインポートボタンが利用可能だった。通常アップロード動画全般や保存成功の実証ではない|
|変更の保存|保存していない。ダイアログを閉じ「変更を破棄」後、詳細画面の保存・変更を戻すボタンが無効であることを確認|
|予約中動画|終了画面の編集・保存は未検証|
|複製される内容|種類・リンク先・座標・サイズ・時間の保持は未検証。終了画面を持つ元動画が必要|
|尺違いのインポート|末尾へ自動整列するか、絶対時刻を保持するか、短い動画で切り詰めるかは未検証|
|再読込・公開後・スマホ|保存後維持、予約公開後の維持、スマホYouTubeアプリでの表示・タップは未検証|

限定公開動画のURL/IDや非公開情報はこの公開コメントへ転記しない。今回は任意の本番動画に終了画面を新規保存してテンプレート化する操作はしていない。

### API / Studioの比較と推奨

|方式|長所|制約・採用判断|
|---|---|---|
|公式Data APIだけ|既存OAuth・予約・receiptを利用できる|終了画面を設定できない。概要欄・投稿に限定して維持|
|Studio手動＋アプリ支援|既存機能で運用開始できる。実行動画・テンプレート・時刻を提示できる|利用者による設定／確認が必要。MVP推奨|
|Studio UI自動化|既存のローカルワーカー基盤を再利用可能|専用プロファイルのログイン、別チャンネル、UI変更、同時起動、保存不確定、規約上の確認が必要。後続の検証対象|

テンプレート元は同じチャンネル・16:9の既存動画から選び、3要素が保存済みであることを初回確認する。インポートできなければ標準の3要素テンプレートから手動作成。設定失敗でも動画ID・予約時刻・公開状態は保持し、Studioへの導線と必要な時刻・リンク先を表示する。

## 3. 演出・タイムライン・共通配置

`T = OP・本編・credits・endcardをすべて含む完成MP4の映像終端` とする。音声長やPodcast manifest.duration、Studio一覧の丸め表示を正本にしない。

|方式|完成動画内の区間|YouTubeの3要素|
|---|---|---|
|通常 fixed|`[T−6,T)` 固定カード|`[T−6,T)`|
|個別 illustration-blur|`[T−12,T−7)` イラスト、`[T−7,T−6)` ぼかし背景へ遷移、`[T−6,T)` 暗めのぼかし背景|最後の6秒のみ。最初のイラスト鑑賞5秒と遷移1秒には出さない|
|代替 illustration-fixed|最初の5秒は個別絵、次の1秒で固定カードへ切替、最後の6秒は固定カード|同じ最後の6秒|

今回のぼかし試作はsigmaを連続変更する方式ではなく、**原画と事前にぼかして暗くした背景を1秒クロスフェード**する。固定カード切替は同じ時間配分でクロスフェード、または5秒保持＋1秒の切替区間終端でhard cutにできる。既存カードだけで始める場合はfixedが最小。

ぼかし方式は絵との連続性が良い一方、顔・文字・明暗でリンクの見やすさが変わる。固定方式は常に同じ背景でQAしやすい。第一候補はぼかしを維持し、明るい／情報量の多い絵には固定方式を選べるようにする。暗さ・blur強度は調整値として確定する。

### 共通テンプレート

`kaberadio-3elements-v1` のようなlayout IDに、背景のsafe areaとYouTube側のtemplateVideoId・3要素定義を対応付ける。UIのクリック座標ではなく、映像内の正規化座標を保存する。

初期デザイン案（Studioで受理される位置・サイズの確定値ではない）:

- おすすめ動画: 左側、矩形 `(x=.08,y=.30,w=.32,h=.32)`
- 壁ラジプレイリスト: 右側、矩形 `(x=.60,y=.30,w=.32,h=.32)`
- 登録: 中央下、中心 `(.50,.75)`、直径は映像高さの約 `.14`

下端のプレーヤー操作帯を避け、画像に小さな文字や「ここをクリック」の位置依存表現を焼き込まない。YouTube側でサイズ・重なり制約を満たす配置を一度確認してからtemplateVersionを固定する。背景とUI要素は別レイヤーであり、MP4に描いた枠はリンクにならない。スマホ表示は実際のYouTubeアプリで確認し、ローカル縮小プレビューだけで合格にしない。

尺設定は30fpsなら整数フレームへ量子化。リンク区間は5〜20秒、かつ確保した背景区間内、全長25秒以上を検証する。完成MP4をffprobeで照合し、Studioの表示フレーム精度との差を調整する。インポート後も各要素の開始・終了を読み、`T−linkDuration`〜`T`へ合わせる。異なる尺のテンプレートの暗黙補正に依存しない。

### 実施したローカル検証

FFmpeg 9.0で既存カードを入力にし、既存動画・投稿成果物と別の検証フォルダへ出力した。AI画像の新規生成はしていない。

|試作|ffprobe結果|
|---|---|
|fixed-6s.mp4|1920×1080 / H.264 / yuv420p / 30fps / 6.000秒 / 180 frames|
|illustration-blur-12s.mp4|同形式 / 12.000秒 / 360 frames|
|illustration-fixed-12s.mp4|同形式 / 12.000秒 / 360 frames|

ぼかし版はフレーム0・149・165・180・359を抽出して目視し、原画保持→中間状態→ぼかし背景維持を確認した。試作は無音の映像だけであり、YouTubeへの投稿用完成品ではない。字幕・BGM・OPを含む全編統合レンダーとGPU性能、スマホ視認性は未検証。

核となるFFmpeg filterは以下（30fps、同一解像度・SARへ正規化した入力）:

```text
[0:v]split=2[a][b];
[a]format=yuv420p,setsar=1[c];
[b]gblur=sigma=24,eq=brightness=-0.12,format=yuv420p,setsar=1[d];
[c][d]xfade=transition=fade:duration=1:offset=5,trim=duration=12[v]
```

起動先の既存 `Get-RadioVideoTimeline` も合成fixtureで実行。本編40秒＋credits3秒に対し、6秒設定はstart=43/end=49、12秒設定はstart=43/end=55。末尾6秒の開始は43/49、OP2秒を加えた計算では45/51となる。最初にvoice trackを省略した試験入力は既存validationで拒否されたため、有効なvoice track付きfixtureに修正して確認した。これはアプリの不具合ではない。

## 4. GitHubアセット契約案

既存 `extras/endcards/` を再利用する。個別絵が必要な回だけ次を作り、通常回にはmanifestすら要求しない。

```text
extras/endcards/<episode-key>/
  README.md          # GitHubで読めるギャラリーページ
  manifest.json      # 公開可能な入力だけ
  endcard-original.png
  endcard-1920x1080.png
  note-banner-1280x670.png
```

noteバナーは単純resizeではなく切り抜き位置を決め、顔・ロゴ欠けを確認する。バナーが不要ならそのassetは省略可能。既存の共通バナーは複製せず既存パスを参照する。`extras/gallery/note-banners/` と `extras/gallery/README.md` に同じ実ファイルへのリンクを追加し、別の画像原本管理を作らない。

manifestの例（hashは例示用。実ファイルのSHA-256が必須）:

```json
{
  "schemaVersion": 1,
  "episodeKey": "example-episode",
  "assetSetId": "example-episode-endcard-v1",
  "galleryPath": "extras/endcards/example-episode/README.md",
  "publication": { "approved": false },
  "assets": [
    {
      "id": "endcard-v1",
      "role": "endcard",
      "path": "extras/endcards/example-episode/endcard-1920x1080.png",
      "width": 1920, "height": 1080,
      "sha256": "<64-hex>",
      "provenance": { "method": "ai-generated", "tool": "Codex" }
    },
    {
      "id": "note-banner-v1",
      "role": "note-banner",
      "path": "extras/endcards/example-episode/note-banner-1280x670.png",
      "width": 1280, "height": 670,
      "sha256": "<64-hex>",
      "derivedFrom": "endcard-v1"
    }
  ]
}
```

台本の既存JSONへ追加する候補:

```json
{
  "radioProduction": {
    "schemaVersion": 1,
    "assets": {
      "assetSetId": "example-episode-endcard-v1",
      "manifestPath": "extras/endcards/example-episode/manifest.json",
      "galleryUrl": "https://github.com/amakawa-chan/KabeRadio/blob/main/extras/endcards/example-episode/README.md"
    },
    "endCard": {
      "mode": "illustration-blur",
      "assetId": "endcard-v1",
      "layoutId": "kaberadio-3elements-v1",
      "holdSeconds": 5,
      "transitionSeconds": 1,
      "linkSeconds": 6,
      "appendGalleryUrl": false
    }
  }
}
```

既存のaudioAdjustment/clips等は保持する。台詞本文には従来の `[OUTRO: ...]` を残し、公開可能なrepo相対パスはmetadataに限定。機械固有パス・Cookie・認証情報を保存しない。`production.json` に同じ設定を重複保持しない。3ファイルPackageとDeliveryの5ファイル契約を維持し、追加画像はExtrasへの参照で扱う。

### 自動検出・選択・キャッシュ

1. 選択台本のepisodeKey/source hashを確定し、既存Git cloneからmanifestを読む。GitHub取得が必要なら既存の更新操作を通す。一覧ごとの履歴API呼出しはしない。
2. アプリは「通常／個別ぼかし／個別→固定／なし」、画像、秒数、リンク設定「手動／自動（後続）／なし」を提示。優先順位はその回への明示選択→台本設定→既定値。別回の選択を持ち越さない。
3. 参照をcommitへ解決し、repo＋commit＋asset path＋SHAでキャッシュ。必要な回の画像だけ取得し、一覧は一つの静的catalog（必要になった段階で追加）で足りる。
4. repo内パス・画像形式・容量・寸法・SHAを検証。取得先を限定し、一時保存→検査→atomic rename。生成開始時に確定素材を成果物へコピーし、処理途中のmain更新に影響されないようにする。
5. 404/429/offline/hash不一致は同じhashの検証済みcacheを優先。なければ通常カードへfallbackし、画面とrender receiptに理由・実際に使った素材を記録。通常カードも欠損なら無言で別画像を使わず生成を止める。
6. fallbackで12秒→6秒になったら、完成尺・リンク時刻・映像確認も再計算。失敗した個別画像を「使用済み」として概要欄へ記録しない。
7. 選択画像hash・mode・尺・layoutVersionを映像の再生成判定に含める。音声入力が同じなら音声は再利用できる。既存の生成済み状態で新設定が無視されないことを試験する。

概要欄は `appendGalleryUrl=true` かつ公開承認済み・参照先存在確認済みの場合だけ、YouTube descriptionへ「今回のイラスト／ギャラリー」ブロックを1回追加。GitHub READMEページURLを使い、raw画像URLやローカルパスを入れない。Spotifyへの自動追加はしない。既存の手編集概要欄・クレジット・ハッシュタグを保持し、最終文字数制限を検査する。再生成時に同じURLを重複追加しない。

KabeRadioは調査時publicであることを確認済み。ただしpublic repoであることと新画像の公開承認は別。manifestのapprovedフラグはアクセス制御ではなく、publicへpushした時点で画像は公開される。未承認画像はローカルに置く。今回は画像のアップロード／ギャラリーページの公開は行っていない。

## 5. 投稿への統合と復旧

```text
既存APIアップロード成功・videoId/receipt確定
  → 終了画面タスクの作成（処理完了待ちを含む）
  → Studio手動支援、または後続の独立adapter
  → 保存後再読込で要素・リンク先・時刻・配置を照合
  → endScreen結果だけ更新
```

既存のアップロードreceiptを正本とし、終了画面の結果は独立した `youtube-end-screen.json` 等へ保存する。例: videoId、channelId、videoSha256、templateVideoId、layoutVersion、desired要素、末尾からのoffsetと解決済み時刻、status、attemptedAt、verifiedAt、reason。設定希望と適用実績を分ける。

状態候補は disabled / pending / waiting-processing / running / configured / auth-required / manual-required / failed。実保存を検証できない場合はconfiguredにしない。手動の確認完了は手動確認として記録し、自動検証済みと区別する。

- APIの動画所有チャンネル、投稿receipt、Studioの選択チャンネルを照合。API OAuthとブラウザのログインを同一視しない。
- 同じprofile lockを共有し、関連動画ワーカーとの同時操作を防ぐ。ID＋希望設定hashを冪等キーにし、アプリ再起動後はStudioの実状態と照合して再開。
- 再読込後におすすめ動画の種類、playlist ID、登録先、3要素の時刻・配置を確認。検証できない項目を「クリックできた」だけで成功にしない。
- ユーザーが既にカスタム終了画面を設定している場合は自動上書きせず差分を提示する。
- 失敗時もアップロード成功・予約・公開状態・Shortsを巻き戻さない。終了画面だけを再試行するボタンを用意し、本編の確認解除に依存させない。
- 公開直前まで未設定なら要対応表示。自動で予約延期・限定公開化しない。即時公開の場合、終了画面設定までの空白時間があり得ることをUIで説明。
- 初回ログイン／再認証／CAPTCHAは利用者対応。過度なリトライを避け、認証情報をGit・ログへ出さない。

## 6. MVP・後続Issue分割案

新規Issueは今回は作成せず、以下を分割案として残す。

|順|候補Issue／実装箇所|受け入れ条件|
|---|---|---|
|A・最優先|終了画面テンプレートの実機検証（Assistant）|終了画面保存済みテンプレートを1本確定。テスト用の予約・限定公開動画について、種類/playlist ID/座標/サイズ/時刻の転送、尺違い、保存再読込、同設定再適用、公開後維持を確認。できない項目は未検証のまま|
|B・MVP|6秒固定カードと手動設定支援（Assistant）|既存OUTRO preset/VideoRenderCore/Radio UIを拡張。新規回は明示6秒、旧回は不変。完成尺から最後6秒を表示しStudioへ誘導。OP有無、credits、音声末尾、字幕、通常ランチャーで確認|
|C|任意アセット契約と取得（KabeRadio＋Assistant）|上記manifest、既存ギャラリー索引、EpisodeProduction/GitEpisodeのresolver。素材なし回・404/429・破損・offline・別回切替・cache・公開URL・概要欄重複を確認|
|D|個別演出とUI（Assistant）|5+1+6のぼかし／固定切替を共通レンダラーへ。フレーム数、境界、字幕残り、OPオフセット、fallback後時刻、設定変更時再生成を確認。各方式を実素材でプレビュー|
|E|終了画面adapterと投稿後タスク（Assistant）|Aと規約上の確認を前提。既存profile/lockを共通化。予約状態不変、保存後照合、再起動復旧、認証切れ・別チャンネル・UI変更時安全停止、二重アップロードなし、手動代替を検証|

Aの検証待ちでもB〜Dの映像／素材設計は進められる。EをMVPの必須条件にしない。Media Library全体の構築はAssistant #47に寄せ、この機能だけで別のライブラリーUIを作らない。

## 7. 開発ナレッジの適用

README・prevention・indexから関連事例を読んだ。

- DEV-0017: 候補一覧の未選択表示を保存失敗と決めつけない。終了画面は独自の保存後検証が必要。
- DEV-0022: 静的カタログ＋成功cacheを使用し、画像／記事ごとの履歴API要求を増やさない。
- DEV-0010: 新規テンプレート→入力読込→解決→renderの配線と映像再生成判定を一緒に確認。
- DEV-0023: アップロード完了後でも独立タスクの再試行ボタンが利用できることを完了callbackまで検証。
- DEV-0008: APIの認証先とStudioの実操作チャンネルを個別に照合する。
- DEV-0033: IssueコメントをUTF-8単一文字列として保存し、投稿後に本文・改行を読戻して照合する。

今回、新しいアプリ不具合の再現は確定していないため、推測を新規ナレッジ事例として登録していない。インポート元に終了画面がない事象、初回新規タブのエラー、GitHub mainと起動先の差は、観測事実と調査上の制約として上記に記録した。
