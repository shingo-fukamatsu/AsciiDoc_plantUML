class Branch:
    def merge_to_main(self):
        print("main ブランチにマージ();")
        spec = Specification()
        spec.convert_to_html()

class Specification:
    def convert_to_html(self):
        print("仕様書を HTML 形式に変換();")
        web_page = WebPage()
        web_page.publish_html_spec()

class WebPage:
    def publish_html_spec(self):
        print("HTML 仕様書を Web ページに公開();")

    def refer_latest_html_spec(self):
        print("HTML 形式の最新仕様書を参照();")

def main():
    branch = Branch()
    web_page = WebPage()
    
    branch.merge_to_main()
    web_page.refer_latest_html_spec()

if __name__ == "__main__":
    main()