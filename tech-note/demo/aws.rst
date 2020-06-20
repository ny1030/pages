************
AWS
************

qualification
=================

aws certified solutions architect(AWS-SA)
---------------------------------------------

Storage
^^^^^^^^^^^^^^^^

C社では現在Amazon Aurora MySQLデータベースによるデータ運用を行っています。当該データベースに保存されているデータは業務上で非常に重要であるため、災害発生時に別リージョンでデータを利用できるようにする必要があります。そのため、毎月の請求期間における月間稼働率が99％以上で使用できるようにするSLAが設けられています。

最も回復性が速い方式で、この要件を達成するための方法を選択してください。

#. AuroraのマルチAZ構成による高速フェールオーバーを実施する。
#. AuroraデータベースのマルチAZ構成を有効化する。
#. Auroraデータベースのリードレプリカを作成する。
#. Auroraデータベースのスナップショットを作成する。

解説：

.. toggle-header::
    :header: Example 1 **Show/Hide Code**

        Content for header

３が正解。

AuroraはソースDBクラスターとは異なるリージョンにリードレプリカを作成することができます。 この方法を採用すると、障害回復機能を向上させ、読み取り操作をユーザーに近いリージョンに拡張しつつ、あるリージョンから別のリージョンへの移行を容易にすることができます。Amazon Aurora MySQL DB クラスターを、ソース DB クラスターとは異なる AWS リージョンにリードレプリカとして作成できます。このアプローチを使用すると、災害対策機能が向上し、ユーザーに近い AWS リージョンへの読み取りオペレーションをスケールして、AWS リージョン間の移行を容易にすることができる。

オプション１:マルチAZの対応だから、リージョン障害には対応できない。

オプション２：１〜２分の停止でフェイルオーバできるがオプション１に劣るし、そもそもリージョン障害に対応できない。

オプション４：スナップショットを作成して別リージョンで回復させることも可能だが、時間を要する。（他の案よりはマシ）

----------

automation
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


