# requirements

- docker
- docker-compose >= 1.13.0

# run

```
# setup
cd worker
mkdir archive
mkdir data
./create_db.sh test.db
```

```
docker-compose up --scale worker=4
```

# 動作

諸々改修予定ですが現状の動作は以下です

worker/dataディレクトリに実行可能ファイルを投げるとN(N=worker数)並列で10回実行します
実行ファイルは、実行後にscoreのみを1行出力するものを前提としています(int(output)しているので)
出力結果はtest.dbに吐き出されます

現状は`node <exec_file>`が実行されるのでjsのみ対応

# TODO

- 諸々のリファクタリング
  - 各種settingをファイルに書き出す
  - db schemeの見直し
- 各種言語への対応
- 実行ファイルの出力フォーマット検討
  - json等何かしらの標準を採用
  - debug出力無視
  - フォーマット可変
- web app化
  - apiに実行ファイルをpostできるようにする
  - 結果集計画面の作成
- 通知
  - runnerに終了後の通知を追加
- workerのメモリ制限など
