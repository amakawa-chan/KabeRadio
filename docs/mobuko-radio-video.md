# モブ子 壁ラジ配信用ビジュアル／ループ動画

## 現在の成果物

今回の配信用ビジュアルは、モブ子の全画面キー画像をコマ送りで並べています。最新版v5では頬杖の差分を物理的な動作順に作り直し、その区間だけFFmpegの双方向動き補間で24fpsへ展開しています。指が途中で開閉する旧差分を外し、猫招きのように見える反復を解消しています。

成果物は `assets/mobuko-radio/` にまとめています。

- `mobuko-radio-story-loop-v2.mp4`: 1280x720、24fps、12秒、無音の最新版ループ
- `mobuko-radio-story-loop-v2.gif`: スマホ確認用の640x360 GIF
- `mobuko-radio-story-loop-v2-preview.png`: 1秒ごとの一覧プレビュー
- `mobuko-radio-face-motion-v2-preview.png`: 顔まわりの動作確認用プレビュー
- `mobuko-radio-hand-motion-v2-preview.png`: 手元の動作確認用プレビュー
- `mobuko-radio-story-loop-v3.mp4`: 1280x720、24fps、14秒、頬杖8段階版
- `mobuko-radio-story-loop-v3.gif`: スマホ確認用の頬杖8段階版GIF
- `mobuko-radio-story-loop-v3-preview.png`: v3の1秒ごとの一覧プレビュー
- `mobuko-radio-cheek-focus-v3-preview.png`: 頬杖の段階確認用拡大プレビュー
- `mobuko-radio-story-loop-v4.mp4`: 1280x720、24fps、14秒、全画面コマ送り版
- `mobuko-radio-story-loop-v4.gif`: スマホ確認用の全画面コマ送り版
- `mobuko-radio-story-loop-v4-preview.png`: v4の1秒ごとの一覧プレビュー
- `mobuko-radio-cheek-focus-v4-preview.png`: v4頬杖の拡大プレビュー
- `mobuko-radio-story-loop-v5.mp4`: 1280x720、24fps、26.67秒、頬杖低頻度・滑らか版
- `mobuko-radio-story-loop-v5.gif`: スマホ確認用のv5 GIF
- `mobuko-radio-story-loop-v5-preview.png`: v5の3秒ごとの一覧プレビュー
- `mobuko-radio-cheek-motion-v5.mp4`: 9.33秒の頬杖区間単体プレビュー
- `mobuko-radio-cheek-motion-v5-preview.png`: 頬杖区間の1秒ごとの一覧プレビュー
- `mobuko-radio-cheek-v5-01.png` ～ `mobuko-radio-cheek-v5-06.png`: 指をほどき、手のひらへ重心を移し、頬を預ける順番の全画面差分
- `mobuko-radio-diff-writing.png`: ノートを書く差分
- `mobuko-radio-diff-writing-early.png`: 筆記開始の中間差分
- `mobuko-radio-diff-writing-mid.png`: 筆記途中の中間差分
- `mobuko-radio-diff-blink.png`: 瞬き差分
- `mobuko-radio-diff-cheek-mid.png`: 頬杖つきなおしの中間差分
- `mobuko-radio-diff-cheek-rest.png`: 頬杖をつきなおす差分
- `mobuko-radio-diff-cheek-15.png` ～ `mobuko-radio-diff-cheek-90.png`: 頬杖6段階の中間差分
- `mobuko-radio-diff-cheek-rest-target-v3.png`: ユーザー提供の頬杖終点差分
- `mobuko-radio-diff-glance-25.png`: 視線移動25%の差分
- `mobuko-radio-diff-glance-50.png`: 視線移動50%の差分
- `mobuko-radio-diff-glance-75.png`: 視線移動75%の差分
- `mobuko-radio-diff-glance-smile.png`: こちらへ視線を向けて軽く微笑む差分

視線・微笑みは、配信画面へ戻る動作を主にしつつ、短い間だけ視聴者側へ注意を向ける演出です。頬杖は開始ポーズから目標画像へ向けて手・手首・頬の接触だけを段階的に変え、背景やカメラは固定しています。

## ループ構成

`tools/build_mobuko_story_loop_v5.py` が全画面キー画像を640フレームへ展開します。頬杖は6枚の新しい差分を一方向に通過し、完成姿勢を3秒保ち、同じ差分を逆順で戻します。頬杖区間は224フレームで、ループ中の実行は1回だけです。v3・v4も比較用に残しています。

1. 待機
2. ノートを書く
3. 待機
4. 瞬き
5. 待機
6. 頬杖つきなおし（指をほどく → 手首を内側へ回す → 頬へ触れる → 手のひらへ重心を移す → 3秒静止 → 同じ軌道で戻る）
7. 待機
8. 視線をこちらへ25%移す
9. 視線を50%移す
10. 視線を75%移し、微笑みを始める
11. 軽く微笑む
12. 視線を段階的に画面へ戻す
13. 待機

開始・終了フレームは同じ基準絵です。現在は発話・口パク・音声トラックを含みません。v5全体は26.67秒で、頬杖区間は9.33秒です。頬杖は約2.4秒で姿勢を移し、3秒静止し、約2.4秒で戻ります。動き補間は全画面差分間に限定し、局所マスク合成は行いません。

## 再生成

Python で差分画像とPNGフレームを生成します。

```powershell
python tools/build_mobuko_story_loop_v5.py
```

FFmpegでMP4へ変換する例です。

```powershell
ffmpeg -y -framerate 24 -i _tmp_mobuko_story_v5/frame-%04d.png `
  -c:v libx264 -pix_fmt yuv420p -movflags +faststart `
  assets/mobuko-radio/mobuko-radio-story-loop-v5.mp4
```

## 次のIssue候補：長時間配信・定期データ収集

画面配信形式が固まった後、3時間・6時間・12時間・24時間の配信時間プリセットを追加する。24時間運用を見越し、1時間ごとなどの間隔で定期的にデータ収集を行う。

収集タイミングは、システムが停止したように見せず、次の状態遷移として扱う想定です。

1. 発話を停止
2. 「モブ子休憩中」専用画面と短い環境音／ループを表示
3. データを収集・保存
4. 失敗時は再試行し、ログへ記録
5. 通常の配信画面へ復帰

実装時に検討する項目：

- 収集間隔、休憩時間、配信時間プリセットの設定
- オフライン時のキューイングと再試行
- 保存先、保持期間、ユーザーの収集許可
- 24時間連続稼働時のメモリ・ディスク・ログ肥大化
- 休憩画面から通常画面へ戻る際の状態復元
- 3／6／12／24時間の各プリセットによる負荷テスト
