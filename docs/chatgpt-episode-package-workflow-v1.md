# ChatGPTから壁ラジ正式台本を保存する手順 v1

## 目的

ChatGPTで壁打ちログを台本化するとき、会話本文だけでなく、Remote Productionが必要とするepisode directory一式を同じ形式で保存するための手順です。

詳細な編集思想は[Canonical Script Converter v0.4](canonical-script-converter-v0.4.md)、実行用プロンプトは[ChatGPT Episode Package Generator v1](../prompts/chatgpt-episode-package-v1.md)を正本とします。note制作記は[note記事契約 v1](note-article-contract-v1.md)を正本とします。

OpenAIの公式ガイダンスにある、目標・制約・成功条件・出力形を具体的に示し、代表的な形式で検証する考え方を採用しています。

## 「壁ラジにして」の解釈ルール

「壁ラジ台本にして」「壁ラジ化して」「正式に壁ラジにして」「壁ラジのエピソードにして」など、ユーザーが会話や壁打ちを壁ラジとして残す意図を示した場合は、単にMarkdown本文を返す依頼ではなく、**KabeRadioの正式Episode Packageを作成・保存する依頼**として扱います。

特に次を混同しないでください。

- `amakawachan-assistant/Radio/` は再生・Render・配信などのRuntime実装です。
- `KabeRadio/episodes/` は壁ラジのコンテンツ正本です。
- 正式Episodeを作る依頼では、入口の会話がAssistantやRadioの機能実装についてであっても、保存先はKabeRadio側です。
- `Radio/scripts/` 等へ単独台本を追加することを「正式な壁ラジ化」の完了条件にしません。

Repositoryへ書き込める環境では、ユーザーが「台本を書いて見せて」など出力だけを明示していない限り、現行Workflow / Prompt / Templateを確認してepisode packageを保存し、通常のGit運用に従って変更を提示します。

判断に迷った場合は、まずKabeRadioの`README.md`とこの文書を確認し、既存Episodeを1件参照してから保存先・形式を決めます。過去の会話記憶よりRepository上の現行正本を優先します。

## 保存単位

新しい台本には [Shorts台本契約](shorts-script-contract-v1.md) に沿ったJSON Front Matterを付けます。
本文完成後に0〜6件の候補を選び、通常回では原則6件を目標にTurn番号・短い見出しを確認します。候補なしも正常です。
ローカル動画生成の対象は `selectedClipIds` で指定します。候補だけでは自動採用しません。
この設定は `script.md` に含め、4つ目のファイルや環境設定をPackageへ追加しません。

正式台本はMarkdownファイル1つではなく、次のepisode packageとして保存します。

```text
episodes/<episode-key>/
├─ README.md
├─ script.md
└─ production.json
```

| ファイル | 正本とする内容 |
|---|---|
| `README.md` | 人がGitHubで読むepisode案内、Cast、台本リンク、検証目的 |
| `script.md` | Radio ParserとTTSへ渡す正式台本、Episode Description |
| `production.json` | Remote Workerが読む制作状態、初期Casting、公開状態 |

## note companion

正式Episode Packageは従来どおり3ファイルで固定し、Radio Runtimeの契約を変更しません。
同じ壁打ちログに制作記として残す思考の移動がある場合だけ、別treeへnote companionを保存します。

```text
notes/<episode-key>/
├─ article.md
├─ article.html
└─ index.html
```

- `article.md`: 編集・履歴管理用Markdown
- `article.html`: note貼り付け用のsemantic HTML本文断片
- `index.html`: 壁ラジ公式側で一般公開する制作ノートページ。iPhone / Safariから読めて本文コピーもできる
- note companionを生成したら`episodes/<episode-key>/README.md`へ公開ページの「Webで読む」リンクを追加する
- `notes/index.html` / `notes/README.md` の一覧にも新しい制作ノートを追加する
- note記事は壁ラジの会話台本を文章化するのではなく、あまかわちゃん側の思考記録として編集する
- モブ子の発言は思考が動いた箇所だけ引用する
- 太字強調などのAI的な文章癖を原則避ける
- 内容が薄い検証回や告知回では無理に作らない

noteへの公開処理、Credential、Cookie、非公開APIやブラウザ自動化設定はKabeRadioの保存対象にしません。

## ChatGPTでの使い方

### 通常のChatGPT

1. `prompts/chatgpt-episode-package-v1.md`をコピーして送信
2. その後へ元ログを貼り付ける
3. 出力されたepisode keyと3ファイルを同じdirectoryへ保存
4. note companion対象なら3ファイルを`notes/<episode-key>/`へ保存し、Episode READMEと制作ノート一覧のリンクも反映
5. `production.json`がJSONとして開けることを確認
6. GitHubへcommitする前に、タイトル、事実関係、公開してよい内容を人が確認

### Repositoryへ書き込めるChatGPT／Codex

KabeRadio Repositoryを作業対象として渡し、実行用プロンプトと元ログを指定します。AIには新規episode directoryだけを作成させ、既存episodeやRender済みArchiveを変更させません。

保存後は次を実行します。

```powershell
.\RemoteRadio.ps1 status <episode-key> --json
.\RemoteRadio.ps1 prepare <episode-key> --json
```

`status`でCastingと解決音声を確認し、`prepare`で必要なTTS ProviderとFFmpegを確認してから`render`します。

## episode key

- ASCII英数字で開始
- 使用可能文字は英数字、`.`、`_`、`-`
- 日本語、空白、`/`、`\`、`..`を使用しない
- 内容が分かる短いslugにする

例：

```text
remote-production-casting-validation
why-search-keeps-growing
feature-telegram-command-boundary
```

## CastingとVoice

初期Castingは`production.json.casting`へCharacter Pack IDで保存します。

```json
"casting": {
  "Host": "amakawachan-layered",
  "Guest": "mobuko-v2"
}
```

Character Pack IDは動画の見た目を決めます。VoiceはPackの`defaultVoice`から決まるため、同じAivisSpeech Voiceを使用する次の2つも見た目で区別できます。

- `mobuko-layered`: 旧モブ子
- `mobuko-v2`: モブ子v2

本編途中の変更だけ、script.mdへ`[CAST: Guest=mobuko-layered]`のように記述します。

## GitHubとM6ローカルの状態

GitHub上の正式台本は、再現可能な入力として`status: ready`、`render.audio/video: pending`で保存します。M6でRenderすると、ローカルcloneのproduction.jsonだけが`rendering`から`rendered`へ更新されます。

MVPではWorkerがGit commit／pushを行わないため、GitHubの`ready`とM6ローカルの`rendered`は意図した違いです。Archiveが存在するepisodeは、GitHubが`ready`でも再Renderしません。

## 機能実装会

実TTS・Podcast・Videoが必要な機能検証では、新しいepisode keyと短い紹介台本を作ります。検証台本は使い捨てにせず「壁ラジ機能実装会」の配信素材として扱います。

```text
機能実装
→ pure logicテスト
→ ChatGPTで短い正式台本化
→ GitHubへready episodeを保存
→ cast / status / prepare
→ Render once
→ Archive / Delivery / hash確認
→ 配信
```

既存episodeをテストのために再Renderしません。修正版が必要なら新しいepisode keyを使用します。

## 保存前チェック

- 元ログにない事実や結論を追加していない
- 個人情報、Token、ローカル絶対パスを台本へ含めていない
- H1タイトルと`## Episode Description`がある
- 発話対象は`## 本編`以降にある
- 見出しは`### Host`、`### Guest`、必要時だけ`### Host + Guest`
- 1 Turnが長すぎず、TTSで読める口語になっている
- `production.json`はコメントなしの有効なJSON
- note companionを作った場合、Episode READMEにその回の制作ノート公開リンクがある
- note companionを作った場合、制作ノート一覧に新記事が追加されている
- `status`は`ready`
- CastingはVoice IDではなくCharacter Pack ID
- `publish.spotify/youtube`は初期値`false`

## Render後チェック

- `manifest.json.initialCasting`がproduction.jsonと一致
- manifestのTurnに期待した`characterId`とProviderが記録されている
- ArchiveにMP3、MP4、master、manifest、source、説明文がある
- iCloudには投稿用5ファイルだけがある
- ArchiveとDeliveryの投稿用ファイルhashが一致
- 再DeliveryでArchive hashが変わらない
