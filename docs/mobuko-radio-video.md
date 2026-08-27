# モブ子 壁ラジ配信用ビジュアル／ループ動画

## 現在の成果物

今回の配信用ビジュアルは、モブ子の全画面キー画像をコマ送りで並べています。局所合成やクロスフェードを使わないため、手・頬・袖の境界が崩れる問題を避けられます。最新版v9では、従来の頬杖・飲み物・背伸び・視線に加え、ノート、あくび、ヘッドホン、夜景、カチューシャの動作を収録しています。

成果物は `assets/mobuko-radio/` にまとめています。

- `mobuko-radio-story-loop-v9.mp4`: 1280x720、24fps、2分30秒、全9動作の配信用ショーケース
- `mobuko-radio-notebook-v9.mp4`: 文字を書き足し、ページをめくって白紙へ戻る12.17秒のクリップ
- `mobuko-radio-yawn-v9.mp4`: 口元を手で隠す9秒のあくびクリップ
- `mobuko-radio-headphones-v9.mp4`: ヘッドホンを装着し、半目で微笑みながら頭を小さく左右へ揺らす16秒のクリップ
- `mobuko-radio-window-v9.mp4`: 窓の夜景を眺める10.67秒のクリップ
- `mobuko-radio-headband-v9.mp4`: ずれたカチューシャを両手で直す9秒のクリップ
- `mobuko-radio-*-v9-contact-sheet.png`: 各クリップと長尺版のコマ確認用一覧
- `mobuko-radio-{notebook,yawn,headphones,window,headband}-v9-*.png`: v9の全画面完成コマ17枚

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

`tools/build_mobuko_story_loop_v9.py` は、全画面完成コマを補間・クロスフェードなしで24fpsへ展開します。単体5本に加え、各動作の間へ約7.7秒の待機を置いた2分30秒の長尺版を生成します。

長尺版の順番は、ノートとページめくり、あくび、飲み物、ヘッドホンと軽い頭揺れ、夜景、カチューシャ直し、背伸び、頬杖、視線と微笑みです。ヘッドホンの頭揺れだけ中央→左→中央→右→中央を2往復し、その他の大きな動作は1周につき1回です。

`tools/build_mobuko_story_loop_v4.py` が完成済みの全画面キー画像を補間せずにコマ送りで並べ、336フレームへ展開します。v3の局所マスク版も比較用に残しています。

1. 待機
2. ノートを書く
3. 待機
4. 瞬き
5. 待機
6. 頬杖つきなおし（15% → 30% → 45% → 60% → 75% → 90% → 目標の全画面コマ）
7. 待機
8. 視線をこちらへ25%移す
9. 視線を50%移す
10. 視線を75%移し、微笑みを始める
11. 軽く微笑む
12. 視線を段階的に画面へ戻す
13. 待機

開始・終了フレームは同じ基準絵です。現在は発話・口パク・音声トラックを含みません。頬杖の往復は約3秒、視線の往復はそれぞれ約1秒、筆記は往復約2秒、全体は14秒です。v4は全画面コマの切り替えのみで、フレーム間の画像ブレンドは行いません。

## 再生成

v9はPythonとFFmpegをPATHへ入れた状態で、次の1コマンドから単体5本と長尺版を再生成できます。

```powershell
python tools/build_mobuko_story_loop_v9.py
```

Python で差分画像とPNGフレームを生成します。

```powershell
python tools/build_mobuko_story_loop_v4.py
```

FFmpegでMP4へ変換する例です。

```powershell
ffmpeg -y -framerate 24 -i _tmp_mobuko_story_v4/frame-%04d.png `
  -c:v libx264 -pix_fmt yuv420p -movflags +faststart `
  assets/mobuko-radio/mobuko-radio-story-loop-v4.mp4
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
