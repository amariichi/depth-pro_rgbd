#https://qiita.com/kongo-jun/items/55acdaa851a7668dd36b を一部改変。(1)白黒反転させるとともに、正規化を画像のデプスに応じて調整、(2)inputフォルダ内のファイルをすべてRGBDにしてoutputフォルダに保存。

import torch
import cv2
import numpy as np
#import matplotlib.pyplot as plt
from PIL import Image
import depth_pro
import os
import argparse

DEFAULT_FOLDER_PATH = './input'
ALLOWED_EXTENSIONS = ('.jpg', '.png')

def generate_depth_map(input_path, output_path):
    # GPUが利用可能な場合はGPUを使用
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")
    
    # モデルとトランスフォームの読み込み
    model, transform = depth_pro.create_model_and_transforms()
    model = model.to(device)
    model.eval()

    #ガンマ補正値
    alpha = 0.6
    beta = 2.2

    #指定した入力フォルダのファイルリストを取得
    files = [f for f in os.listdir(input_path) if os.path.isfile(os.path.join(input_path, f)) 
             and f.lower().endswith(ALLOWED_EXTENSIONS)]
    
    # ファイルを順番に処理
    for file in files:
        file_path = os.path.join(input_path, file)


        # 画像の読み込みと前処理
        image, _, f_px = depth_pro.load_rgb(file_path)
        image = transform(image).unsqueeze(0).to(device)
    
        # 推論の実行
        with torch.no_grad():
            prediction = model.infer(image, f_px=f_px)
    
        # デプスマップの取得
        depth = prediction["depth"].squeeze().cpu().numpy()
        inverse_depth = 1 / depth

        # Visualize inverse depth instead of depth, clipped to [0.1m;250m] range for better visualization.
        max_invdepth_vizu = min(inverse_depth.max(), 1 / 0.1)
        min_invdepth_vizu = max(1 / 250, inverse_depth.min())
        inverse_depth_normalized = (inverse_depth - min_invdepth_vizu) / (
            max_invdepth_vizu - min_invdepth_vizu
            )
        #color_depth = (inverse_depth_normalized * 255).astype(np.uint8)
        color_depth = (255 * ((inverse_depth_normalized))**(alpha + (beta - alpha)*(inverse_depth_normalized))).astype(np.uint8)
        print(depth.min(), depth.max())
        #plt.hist(color_depth)
        #plt.show()

        # デプスマップをグレースケール画像として保存
        depth_image = cv2.hconcat([cv2.imread(file_path), cv2.cvtColor(color_depth, cv2.COLOR_GRAY2BGR)])
        cv2.imwrite(os.path.join(output_path, os.path.splitext(file)[0] + "_RGBD" + os.path.splitext(file)[1]), depth_image)
        print(f"Depth map of {file} is saved to {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='フォルダ内のJPGとPNG画像を処理します。')
    parser.add_argument('--folder', type=str, default=DEFAULT_FOLDER_PATH,
                        help='処理するフォルダのパス（デフォルト: %(default)s）')

    args = parser.parse_args()
    input_image_path = args.folder  # 入力画像のパスを指定
    output_image_path = "./output"  # 出力画像のパスを指定
    generate_depth_map(input_image_path, output_image_path)
