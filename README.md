# depth-pro_rgbd
A small script to create RGB-D jpg files using Apple's depth-pro.
(It’s like a prototype for my own learning purposes.)

It batch converts jpg and png files in the specified folder and stores them in the output folder.

I used the script from the following website. (I express my gratitude.)

[Running apple/DepthPro locally](https://qiita.com/kongo-jun/items/55acdaa851a7668dd36b)

Modifications I made:
- Changed the method of depth map normalization (inverted black and white, added a correction to emphasize differences in closer areas)
- Converted all files in the folder to RGBD format (left: original image, right: depth image)

Since I’m still figuring things out, I ended up using both OpenCV and PIL.

In addition to the original source's method of normalization using 1/Depth, I also added a gamma correction formula.

For reference, I consulted the following paper, which I found through a Google search:

[Interactive Image Quality Enhancement Support System by Tone Curve Correction Based on Human KANSEI](https://www.jstage.jst.go.jp/article/ieejias/129/6/129_6_593/_pdf)

![fig](https://github.com/user-attachments/assets/0ad92add-7fb7-488f-a646-8658edd117fe)


Apple が作成した Depth-Pro をコマンドラインで動かして、RGBD画像を作るスクリプトです。

（自分用の勉強用試作品のようなものです）

指定したフォルダ内の jpg, png ファイルを一括変換して output フォルダに格納します。


以下のサイトのスクリプトを利用させていただきました。（感謝申し上げます。）

[apple/DepthProをローカルで動かす](https://qiita.com/kongo-jun/items/55acdaa851a7668dd36b)

## 改造したところ。
- デプスマップの正規化の方法（白黒を反転、近いところの差を大きくする補正を追加）
- フォルダ内のファイルをすべてRGBD形式（左元画像、右デプス画像）に変換

色々よくわかっていないので、OpenCVとPILの両方を使ってしまっています。

オリジナルののソースにあった 1/Depth で正規化する方法に加えて、ガンマ補正の式を付け加えてみました。

その際、ネットで検索して見つけた以下の論文を参考にしました。

[トーンカーブ補正による感性に基づく対話的高画質化支援システム](https://www.jstage.jst.go.jp/article/ieejias/129/6/129_6_593/_pdf)
