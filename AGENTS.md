# KabeRadio制作ルール

## アーカイブス台本のGitHub保存

2026-10-24のユーザー指定により、壁ラジアーカイブス台本の作成依頼は原則としてGitHub既定ブランチへの保存（commit/push）まで含む。毎回の追加確認は不要。「ローカルのみ」「pushしない」等の明示指定があれば優先する。

- 現行の制作契約と手順は `docs/archives-script-contract-v1.md` と `prompts/chatgpt-archives-v1.md` を参照する。
- 作成した台本と必要な一覧・制作ルールのみを対象にし、無関係な作業中の変更は含めない。
- 出典Turn・CAST・Parser・重複・公開可能な情報だけであることを確認して保存する。
- リモートの保存コミットとファイルを確認して完了報告する。PRのみの場合は既定ブランチ未反映と明記する。
- 音声生成・レンダー・投稿・予約公開はこの保存依頼には含まない。

## 公開状態の同期

公開状態の正本は各Episodeの `publication.json`（アップロード側が記録する）。`production.json` の `publish` は作成時の初期値 `false` のままでは実態とズレるため、公開を確認したら `tools/sync_publish_status.py` を実行し、`production.json.publish` の同期を同じコミットに含めること。

- スクリプトは `publication.json` が公開を示す場合だけ `false → true` へ更新する（YouTubeは `actualPrivacy: public`、または `private` でも `publishAt` が過去。Spotifyは `status: published`）。
- 逆向きの不一致（production が `true` で publication が非公開）はスクリプトでは自動修正せず、警告として人が確認する。
