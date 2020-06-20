************
TIPS
************

SQLパフォーマンスチューニング
==============================================

.. important::

   PostgreSQLを用いて説明しています。

Level 0 実行計画(Query Plan)の読み方
---------------------------------------
以下のようなSQLの実行計画を取得してみる。

.. code:: postgresql

    UPDATE
          T_ITEM_INBOUND t3
        SET
          status_flag = '9'
          , updated_datetime = CURRENT_TIMESTAMP
          , updated_by = 'APP_001'
        FROM
          (
            SELECT
              t1.group_num
              , t1.level3_item_code
            FROM
              T_ITEM_INBOUND t1
            WHERE
              t1.status_flag = '1'
              AND t1.group_num = '10'
              AND t1.level3_item_code = '1000-2000-3000'
            GROUP BY
              t1.group_num
              , t1.level1_item_code
              , t1.level2_item_code
              , t1.level3_item_code
              , t1.color_code
              , t1.size_code
              , t1.pattern_length_code
            HAVING
              1   <   COUNT(t1.group_num)
          ) t2
        WHERE
          t3.status_flag = '1'
          AND t3.group_num = t2.group_num
          AND t3.level3_item_code = t2.level3_item_code
          AND t3.brand_code = 'TK'
          AND t3.region_code = 'JP'

上記クエリの先頭に ``EXPLAIN ANALYZE`` というフレーズを付与→実行することで、以下のように実行計画が出力される。

.. code:: postgresql-console

    Update on T_ITEM_INBOUND t3  (cost=19152.43..40432.82 rows=1 width=299) (actual time=65.760..65.760 rows=0 loops=1)
      ->  Hash Join  (cost=19152.43..40432.82 rows=1 width=299) (actual time=65.758..65.758 rows=0 loops=1)
            Hash Cond: (((t3.group_num)::text = (t2.group_num)::text) AND (t3.level3_item_code = t2.level3_item_code))
            ->  Seq Scan on T_ITEM_INBOUND t3  (cost=0.00..19152.36 rows=283735 width=150) (actual time=4.019..4.019 rows=1 loops=1)
                  Filter: (((status_flag)::text = '1'::text) AND (brand_code = 'TK'::text) AND (region_code = 'JP'::text))
                  Rows Removed by Filter: 11
            ->  Hash  (cost=19152.42..19152.42 rows=1 width=62) (actual time=61.731..61.731 rows=0 loops=1)
                  Buckets: 1024  Batches: 1  Memory Usage: 8kB
                  ->  Subquery Scan on t2  (cost=19152.37..19152.42 rows=1 width=62) (actual time=61.730..61.730 rows=0 loops=1)
                        ->  GroupAggregate  (cost=19152.37..19152.41 rows=1 width=55) (actual time=61.730..61.730 rows=0 loops=1)
                              Group Key: t1.group_num, t1.level1_item_code, t1.level2_item_code, t1.level3_item_code, t1.color_code, t1.size_code, t1.pattern_length_code
                              Filter: (1 < count(t1.group_num))
                              Rows Removed by Filter: 1
                              ->  Sort  (cost=19152.37..19152.38 rows=1 width=55) (actual time=61.724..61.724 rows=1 loops=1)
                                    Sort Key: t1.level1_item_code, t1.level2_item_code, t1.color_code, t1.size_code, t1.pattern_length_code
                                    Sort Method: quicksort  Memory: 25kB
                                    ->  Seq Scan on T_ITEM_INBOUND t1  (cost=0.00..19152.36 rows=1 width=55) (actual time=21.804..61.714 rows=1 loops=1)
                                          Filter: (((status_flag)::text = '1'::text) AND ((group_num)::text = '10'::text) AND (l3_item_code = '1000-2000-3000'::text))
                                          Rows Removed by Filter: 283734

全てを説明するのは長くなるので要点だけ。

インデントは処理の順番を表す
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#. 処理を行う単位（=実行計画の各レコード）ノードと呼ぶ。
#. ノードはツリー構造で表現される。最下層のノード（=リーフノード）は必ずテーブルスキャンノードとなる。
#. 最下層（=インデントが深い）のノードから順に実行される。
#. 最下層ノードの親は結合ノードでさらにその親はその他のノードになっている。

テーブルスキャンノード
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
テーブルからデータを取り出す役割。代表的なスキャン方法は以下の通り。

#. Seq Scan: テーブル全体を順番にスキャンする
#. Index Scan: テーブルに付与されているインデックスのみをスキャンし、実テーブルはスキャンしない

今回の例では ``Seq Scan`` が使われいている。

結合系ノード
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
複数のテーブルを結合する役割のノードです。代表的な結合方法は以下の通り。

#. Nested Loop: 外側テーブルの行毎に内側テーブルのすべての行を突き合わせ結合する
#. Hash Join: 内側テーブルの結合キーでハッシュを作成し、ハッシュと外側テーブルの結合キーで一致する行を結合する

処理コスト
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
実行計画の各ノードには、始動コストと総コスト、行数と行の長さが記載されている。

* 始動コスト: 一件目のデータを返すのにかかる想定のコストを表す( ``..`` の前)
* 総コスト: 処理完了までにかかる想定のコストを表す( ``..`` の後)
* 行数： ノード実行によって返却される行数を表す( ``rows`` )
* 行の長さ： ノードの実行によって返却される行の平均の長さを表す( ``width`` )

.. important::

   * ``EXPLAIN`` のみをつけて実行計画を取得すると、プランナによって見積もられたコストとなる。
   * ``EXPLAIN ANALYZE`` をつけて実行計画を取得すると、実際に実行して得られた結果となる。( `actual` 以降の情報がそれ)
   * なので、 ``cost`` と ``actual`` の ``rows`` が大きくずれている場合は統計情報が古い可能性がある。

Level 1 Index利用による高速化
-----------------------------

Level 2 部分Indexの利用
------------------------

Command メモ
================

ここではなくgistに記載：https://gist.github.com/ny1030
