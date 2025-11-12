# local_html2text.py (【最終修正版】)
import glob
import os
import sys

from bs4 import BeautifulSoup


def convert_html_to_text(html_dir, output_dir):
    """
    指定されたディレクトリ内のHTMLファイルをテキストに変換して保存する。
    ディレクトリ構造を反映したユニークなファイル名を生成する。
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 対象の拡張子を複数サポート（.html と .htm）
    html_files = glob.glob(os.path.join(html_dir, "**", "*.html"), recursive=True)
    html_files += glob.glob(os.path.join(html_dir, "**", "*.htm"), recursive=True)

    if not html_files:
        print(
            f"HTMLファイルが見つかりませんでした。ディレクトリ '{html_dir}' を確認してください。"
        )
        return

    print(f"{len(html_files)} 個のHTMLファイルを処理します...")

    for html_path in html_files:
        print(f"処理中: {html_path}")
        try:
            with open(html_path, "r", encoding="utf-8") as f:
                soup = BeautifulSoup(f.read(), "lxml")

            # 本文要素を複数の候補から探す（Googleのdevsite構造 / GitLabの構造 / フォールバック）
            content_div = (
                soup.find("div", class_="devsite-article-body")
                or soup.find("div", attrs={"data-pagefind-body": True})
                or soup.find("div", class_="docs-content")
                or soup.select_one("div[data-pagefind-body]")
                or soup.find("main")
                or soup.find("article")
                or soup.body
            )

            # relative path -> unique basename
            relative_path = os.path.relpath(html_path, html_dir)
            base_name_without_ext = os.path.splitext(relative_path)[0]
            # ディレクトリ区切りをハイフンにしてユニークなファイル名を作る
            unique_base_name = base_name_without_ext.replace(os.sep, "-")
            output_filename = f"{unique_base_name}.txt"
            output_path = os.path.join(output_dir, output_filename)

            if not content_div:
                print(
                    f"  注意: 本文要素が見つかりませんでした (fallback もなし): {html_path}\n  -> body 全文を出力します"
                )
                text = soup.get_text(separator="\n", strip=True)
            else:
                text = content_div.get_text(separator="\n", strip=True)

            # 保存
            with open(output_path, "w", encoding="utf-8") as out_f:
                out_f.write(f"Source Path: {html_path}\n\n")
                out_f.write(text)

            print(f"変換完了: {output_path}")

        except Exception as e:
            print(f"エラーが発生しました ({html_path}): {e}")


# --- GitHub Actions と ローカル実行の両方に対応 ---
if __name__ == "__main__":
    if len(sys.argv) == 3:
        input_dir = sys.argv[1]
        output_dir = sys.argv[2]
        print(
            f"--- Processing files from '{input_dir}' to '{output_dir}' (from command line) ---"
        )
        convert_html_to_text(input_dir, output_dir)
    else:
        print("--- Running with default settings for local testing ---")

        # --- ローカルでテスト実行したい場合の設定 ---
        # 既存のテキストフォルダを一度削除すると確実です
        # if os.path.exists('gas_docs_txt'):
        #      import shutil
        #      shutil.rmtree('gas_docs_txt')
        # if os.path.exists('gemini_api_docs_txt'):
        #      import shutil
        #      shutil.rmtree('gemini_api_docs_txt')
        if os.path.exists("gitlab_docs_txt"):
            import shutil

            shutil.rmtree("gitlab_docs_txt")

        # GAS
        # convert_html_to_text('gas_docs_html', 'gas_docs_txt')
        # Gemini API
        # convert_html_to_text('gemini_api_docs_html', 'gemini_api_docs_txt')
        # GitLab CI
        convert_html_to_text("gitlab_docs_html", "gitlab_docs_txt")
