# deskApp-PMAPP
* パスワード管理システム(デスクトップアプリVer.)
* 2023年4月度の修正(パスワードの暗号化対応まで行っています。)
## Issue #1
* 設定ファイルを新規作成
* 文字列を暗号化・復号化するプログラムを作成
* 設定ファイルに記載した項目は、設定ファイルの値を復号化して取得するよう修正
## Issue #4
* リファクタリングを実施
* 分量が長いクラスを複数クラスに分割
* 一部クラス名・メソッド名の変更を実施
## Issue #7
* アカウント必要区分が「必要」のアプリケーションのパスワードを検索した際、システムが落ちる現象を修正
* パスワードテーブルにワークテーブルを新設し、システム終了時に登録忘れがあった場合、正規のテーブルに登録を促す処理を追加
## 2023/07/08 Version 3 リリース
* アクションクラスの新規作成
## Issue #14
* ワークテーブルに登録されていて、本登録されていないパスワードの一覧を表示する画面を作成
## Issue #16
* 本番DBをローカルのMySQLからPlanetScaleのMySQLに変更
## Issue #18
* パスワード生成機能に記号なしモードを追加
## Issue #21
* モバイルマスタメンテナンス画面を作成
## Issue #25 Version 4 リリース
* PlanetScale Hobbyプラン無料期間終了に伴うAPI利用への移行(MySQL→Postgresへの移行)
