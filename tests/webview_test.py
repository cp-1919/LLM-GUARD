import webview

html = """
<!doctype html>
<html lang="en">
	<head>
		<meta charset="utf-8">
        <title>测试应用</title>
        <style>
            .frame {
                border-radius: 5px 5px 0 0;
                position: 固定;
                box-sizing: border-box;
                width: 90%;
                height: 90%;
                background-color: #0055e4;
                box-shadow: inset 1px 1px 1px 0px rgba(255,255,255,.25), inset -1px -1px 1px 0px rgba(0,0,0,.25), inset 0px 2px 4px -2px rgba(255,255,255,1);
            }
            .frame>tbody>tr>td {
                vertical-align: top;
            }
            .header {
                box-sizing: border-box;
                padding: 5px;
                height: 20px;
                font-weight: bold;
                color: white;
            }
            .header>img {
                height: 16px;
                transform: translateY(3px);
            }
            .content {
                box-sizing: border-box;
                background-color: #f0f0e8;
                margin: 0 5px 5px 5px ;
            }
            .bodypanel {
                background-color: #f0f0e8;
                height: 100%;
                box-shadow: 1px 1px 1px 0px rgba(255,255,255,.25), -1px -1px 1px 0px rgba(0,0,0,.25), inset 0px 0px 3px -2px rgba(0,0,0,1);
                padding: 5px;
            }
        </style>
	</head>
	<body>
        <table class="frame">
            <tbody>
                <tr>
                    <td class="header">
                        <img src="folder.png"/>
                        危险!
                    </td>
                </tr>
                <tr>
                    <td class="body">
                        <div class="bodypanel">
                            <b>警告!</b><br>
                            Lorem ipsum dolor sit amet, consectetur adipiscing elit
                        </div>
                    </td>
                </tr>
            </tbody>
        </table>
	</body>
</html>
"""

if __name__ == '__main__':
    # 创建一个透明的webview窗口
    webview.create_window('透明窗口', html=html, transparent=True, frameless=True)
    print(webview.FOLDER_DIALOG)
    webview.start()