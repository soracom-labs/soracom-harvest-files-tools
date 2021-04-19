# Soracom Harvest Files Tools
## soracom_harvest_files_downloader.py

SORACOM Harvest Filesから複数のファイルをダウンロードするサンプルスクリプトです。

### How to use

1. [SORACOM API 利用ガイド](https://users.soracom.io/ja-jp/tools/api/) を参考にAPIキーとAPIトークンを発行します  
    1. 発行するSAMユーザには`FileEntry:listFiles`と`FileEntry:getFile`の権限を付与してください
```
{
  "statements": [
    {
      "effect": "allow",
      "api": "FileEntry:listFiles"
    },
    {
      "effect": "allow",
      "api": "FileEntry:getFile"
    }
  ]
}
```
2. スクリプトを任意のディレクトリに配置します
3. 次のコマンドで実行します `python3 soracom_harvest_files_downloader.py --auth_key_id [AUTH_KEY_ID] --auth_key [AUTH_KEY_SECRET] --base_path "./"`

### Parameter
--auth_key_id: 認証キー ID  
--auth_key: 認証キー シークレット  
--base_path: ファイルの取得元のパス
--save_path: (optional default="./") ファイルの保存先  
--search: (optional default=None) ファイル名の検索文字列  
--limit_num_to_list": (optional default=100) 取得するファイル数  
--limit_num_to_list_per_req: (optional default=100) 1回のLIST Requestで取得するファイル数  
--limit_size_to_files: (optional default=2.5GB) 取得する最大合計ファイルサイズ ※1  
--last_evaluated_key: (optional default=None) 最後のファイルエントリの filePath 。このパラメータを指定することで次のファイルエントリ以降を取得できる  
--coverage: (optional default="jp") 処理対象のカバレッジタイプ  
--delete: (optional default=false) 指定された場合、ファイルを取得後にSORACOM Harvest Filesから削除する  
--debug: (optional defailt=false) 指定された場合、デバッグログを出力する  

### Note
- `--delete` を付与することでダウンロードしたファイルをHarvest Filesから削除します。ただし、ダウンロードしたファイルの正常チェックは行っていないため、もしファイルが正しくダウンロード出来ていなかった場合はファイルを失う可能性があります
- `--limit_num_to_list NNNN`(NNNNは数字) を付与することで一度に取得するファイル数を指定することができます。ファイル数が増えると処理時間もダウンロードサイズも増えますのでご注意ください
- `--limit_size_to_files NNNN`(NNNNは数字) を付与することで一度に取得する最大合計ダウンロードサイズを指定(簡易)することができます。このサンプルでは指定されたサイズ(単位:byte)を超えた場合に処理を終了する実装となっているため厳密ではない点にご注意ください(最後にダウンロードしたファイルのサイズが大きいと大きく超えてしまいます)。指定しない場合は初期値2.5GBを最大として処理されます
- ファイルのダウンロードにはSORACOM Harvest Filesの[エクスポート料金](https://soracom.jp/services/harvest/price/)が発生します
- API リクエストに関しては、オペレーターごとに API の Path 単位で 1 分間あたりの最大リクエスト数が定められています(スロットリング)。スロットリングが発生する場合は[制限事項と注意事項](https://users.soracom.io/ja-jp/tools/api/limitations/)を参考にサポート窓口へご相談ください
