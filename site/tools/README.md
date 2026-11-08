# 紹介音声の生成

`pr.txt` は表示・字幕・X用、`pr-speech.txt` はモブ子の合成用です。両方を同じ内容で用意します。ローカルAivisSpeechを起動し、FFmpegをPATHに追加してから実行します。

```sh
python site/tools/generate_pr_intro.py <episode-key>
python site/tools/build_episode_index.py
```

生成したMP3と `.sha256` は同じ組として扱います。索引はPR文、読み上げ版、MP3が生成時と一致するときに音声へのリンクを含めます。片方が空、欠落、変更済みの回はテキスト表示を使います。両PRファイルが存在しない旧回では従来の紹介音声を利用します。
