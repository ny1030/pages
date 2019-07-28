************
AWS
************

自動化関連
============

RDSログを取得
--------------

自動化をしたい場合にRDSログをAPI経由で取得したいケースがある。

1. AWS CLIを利用
^^^^^^^^^^^^^^^^

DB識別子(DBInstanceIdentifier)の一覧を取得

.. code:: bash

    aws rds describe-db-instances  --region ap-northeast-1 | jq '.DBInstances[].DBInstanceIdentifier'
    "database-test"

特定のDBのログファイル名一覧を取得

.. code:: bash

    aws rds describe-db-log-files --db-instance-identifier database-test --region ap-northeast-1
    {
    "DescribeDBLogFiles": [
        {
            "LogFileName": "error/postgres.log",
            "LastWritten": 1572672642000,
            "Size": 455
        }
    ...

ログファイルを出力

.. code:: bash

    aws rds download-db-log-file-portion --db-instance-identifier database-test --log-file-name "error/postgresql.log.2019-11-02-09"  --output text --region ap-northeast-1
    2019-11-02 09:02:45 UTC::@:[5385]:LOG:  checkpoint starting: time
    2019-11-02 09:02:45 UTC::@:[5385]:LOG:  checkpoint complete: wrote 1 buffers (0.0%); 0 WAL file(s) added, 0 removed, 1 recycled; write=0.101 s, sync=0.001 s, total=0.113 s; sync files=1, longest=0.001 s, average=0.001 s; distance=65535 kB, estimate=65536 kB
    ...

なお、上記コマンドではログファイルサイズが1MB以上はダウンロードすることができない。
全てを取得したい場合、以下オプションで出来る。

.. code:: bash

    aws rds download-db-log-file-portion --db-instance-identifier database-test --log-file-name "error/postgresql.log.2019-11-02-09"  --output text --region ap-northeast-1 --cli-input-json '{ "Marker": "0" }'


