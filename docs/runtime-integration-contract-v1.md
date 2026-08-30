# KabeRadio / Amakawachan Radio Runtime Integration Contract v1

## 目的

壁ラジの「コンテンツ正本」と、Amakawachan Assistant内の「制作Runtime」を分離したまま、ChatGPT・M6・Telegram・iCloudまで同じ制作フローで扱うための境界を定義します。

この文書はRepository間の責務と制作フローの正本です。台本編集ルールは`canonical-script-converter-v0.4.md`、ChatGPTからの保存形式は`chatgpt-episode-package-workflow-v1.md`を正本とします。

## Repositoryの責務

### `amakawa-chan/KabeRadio`

番組とコンテンツの正本です。

管理対象:

- 番組設定・編集思想
- Character Profileの公開設定
- Episode Package
- 正式台本
- Episode Description
- 制作開始時点のCasting
- Git履歴として残す公開前入力

正式な制作入力は次の単位です。

```text
episodes/<episode-key>/
├─ README.md
├─ script.md
└─ production.json
```

GitHub上の`production.json`は再現可能な入力として原則`status: ready`、`render.audio/video: pending`を維持します。

### `amakawa-chan/amakawachan-assistant`

実行環境と制作Runtimeの正本です。

管理対象:

- Amakawachan Radio GUI
- Canonical Script Parser
- Character Pack Runtime
- TTS Provider統合
- Podcast Render
- Video Render
- Remote Production Worker
- Telegram Remote Radio adapter
- M6固有設定を読み込むRuntime契約

壁ラジの正式Episode本文はAssistant Repositoryへ複製しません。`Radio/scripts/`はRuntimeのsample・test・互換確認に限定し、公開用Episodeの保存先にはしません。

## 環境固有設定

Token、User ID、Chat ID、ローカル絶対パス、TTS executable pathなどはGitへ保存しません。

M6では`amakawachan-assistant/Radio/config.local.json`を環境設定の入口とします。

最低限の役割:

```text
remoteProduction.kabeRadioRepository
  -> KabeRadioのローカルclone

remoteProduction.archiveDirectory
  -> Render済み成果物のローカル正本

remoteProduction.deliveryDirectory
  -> iCloud等の投稿待ちフォルダ

ttsProviderOverrides
  -> M6上のTTS Provider起動設定

telegramRemoteRadio
  -> Telegram adapterの許可リストと実行設定
```

Bot tokenは環境変数へ置き、Repositoryへ保存しません。

## 正本の流れ

```text
ChatGPT / 人間の壁打ち
        ↓
KabeRadio episode package (GitHub: ready)
        ↓
M6 KabeRadio local clone
        ↓
Amakawachan Radio Remote Production
        ↓
Local Archive (rendered成果物の正本)
        ↓
Delivery directory (投稿用5ファイルのみ)
        ↓
Spotify / YouTubeへの投稿
```

GitHub上の`ready`とM6ローカルの`rendered`は意図した差です。Remote WorkerはMVPでは制作状態をGitHubへpushしません。

## ChatGPTから正式Episodeを作る場合

1. KabeRadioの`prompts/chatgpt-episode-package-v1.md`を読む
2. `docs/canonical-script-converter-v0.4.md`を読む
3. 新しい`episodes/<episode-key>/`だけを作る
4. `README.md`、`script.md`、`production.json`を揃える
5. `production.json`は`ready`で保存する
6. 既存EpisodeやRender済みArchiveを編集・再Renderしない

ChatGPTがGitHubへ直接書き込める場合でも、正式台本をAmakawachan Assistant側へ保存しません。

## M6での制作

KabeRadio cloneを更新した後、Amakawachan Assistantの`Radio/RemoteRadio.ps1`を入口にします。

```powershell
.\RemoteRadio.ps1 status <episode-key> --json
.\RemoteRadio.ps1 prepare <episode-key> --json
.\RemoteRadio.ps1 render <episode-key>
```

Castingを変更する場合はRender前かつArchive未作成のEpisodeだけ`cast`を使用します。

```powershell
.\RemoteRadio.ps1 cast <episode-key> --host amakawachan-layered --guest mobuko-v2
```

RenderはPodcastとVideoを一度だけ生成し、Archiveを成果物の正本にします。Deliveryだけ失敗した場合は`deliver`のみ再実行し、再Renderしません。

## Casting / Voice境界

- `production.json.casting`: Character Pack IDを保存
- Character Pack: 見た目と`defaultVoice`を保持
- `config.local.json.voiceAssignments`: M6で明示的に上書きする場合のみ使用
- 台本途中の変更: `[CAST: Role=character-pack-id]`

Voice ProviderやStyle IDをEpisode Packageへ直接固定しません。

## Telegramの位置付け

Telegram Remote Radioは制作Runtimeの外部入口です。

Telegram adapterは、許可されたUser / ChatからRemote Production commandを呼び出します。Episode本文や制作ロジックをTelegram側へ複製しません。

初回設定では`-InspectIdentity`でBotへ届いたUser / Chat IDを確認し、その後にallowlistへ保存します。

## Delivery契約

Delivery directoryへコピーするのは投稿に必要な次の5ファイルだけです。

- `podcast.mp3`
- `youtube.mp4`
- `title.txt`
- `spotify-description.txt`
- `youtube-description.txt`

`master.wav`、`clips/`、`manifest.json`、`source.md`、一時ファイルはArchive側だけに保持します。

## 変更時のルール

Repository間の契約を変更する場合は、次の順に更新します。

1. このIntegration Contractを更新
2. Amakawachan AssistantのRuntime実装・READMEを更新
3. KabeRadioのEpisode Package workflow / prompt / templateを必要に応じて更新
4. pure logic test
5. 必要なら新しい「壁ラジ機能実装会」Episodeで実TTS・Podcast・Video・Deliveryを検証

既存の公開Episodeを仕様確認のために再Renderしません。
