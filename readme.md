Inv_mod

![](F:\Img_Markdown\2023-10-01-04-41-40-image.png)

Stash mode 

同时点击仓库和 g 可以同时打开

![](F:\Img_Markdown\2023-10-02-23-49-44-image.png)

![](F:\Img_Markdown\2023-10-02-00-12-55-image.png)

### 1. 自动六分仪

F4

1. 打开背包，最小化地图集

2. 填写第一个格子的坐标，每个各自的间隔（12x5）

3. 填写虚空石头坐标（Mpos获取指针坐标）

4. 点击开始

脚本流程

1. 鼠标移动到slot 1 ，右键点击，移动到void stone 位置 左键点击

2. 鼠标移动到slot 1  left + 1 ，右键点击，移动到移动到void stone 位置 左键点击， 再移动到 slot 1  left + 2 位置，左键点击放下罗盘

3. 循环1 2 ，每一步计算位置

4. 当计数达到50的时候弹窗提示

关于词缀判断的思考

罗盘成本和仓储成本

大仓库 24 x 24  = 576

**like human behaviour**

todo:

1.每次点击的坐标为base坐标附近15像素范围内的点，而非固定坐标。click 操作press release的时间也随机。

2.鼠标移动轨迹随机化

3.随机休息，每成功洗60个罗盘，随机 sleep 30-50秒,每洗1000个罗盘，休息1-4分钟

4.每成功洗一次罗盘后，随机点击无效区域随机坐标的点，随机重复1-3次。

5.穿插点击一些随机但不影响操作的按键

6.洗完以后/exit退出登录并给自己发送邮件提醒

### 2. 自动从仓库取高亮罗盘

F6

### 3. 所有物品从背包放入仓库

F7

### 定时更新库存

```javadoclike
    // 寻找文本为 "Load 6 Tabs" 的按钮并点击
    let loadButtons = document.querySelectorAll('button');
    loadButtons.forEach(function(button) {
        if (button.textContent.trim() === 'Load 5 Tabs') {
            button.click();console.log("click Load tabs button");
        }
    });

    // 等待30秒后点击 "Post to TFT" 按钮
    setTimeout(function() {
        let postButtons = document.querySelectorAll('button');
        postButtons.forEach(function(button) {
            if (button.textContent.trim() === 'Post to TFT') {
                button.click();button.click();button.click();button.click();button.click();console.log("click POST to TFT button");
            }
        });
    }, 15000); // 30000毫秒 == 30秒
setInterval(function() {
    // 寻找文本为 "Load 5 Tabs" 的按钮并点击
    let loadButtons = document.querySelectorAll('button');
    loadButtons.forEach(function(button) {
        if (button.textContent.trim() === 'Load 5 Tabs') {
            button.click();console.log("click Load tabs button");
        }
    });

    // 等待30秒后点击 "Post to TFT" 按钮
    setTimeout(function() {
        let postButtons = document.querySelectorAll('button');
        postButtons.forEach(function(button) {
            if (button.textContent.trim() === 'Post to TFT') {
                button.click();button.click();button.click();button.click();button.click();console.log("click POST to TFT button");
            }
        });
    }, 15000); // 30000毫秒 == 30秒
}, 350000); // 610000毫秒 == 10.1分钟
```

### TFT WTT

WTT Softcore
My 175:chaos:  for your 1 :divine: (always buying)
Stock  5000+ :chaos:
My 1 :divine: for your 58 Awakened Sextants (always buying )
stock: 100+ :divine:
IGN: Stackoverflow_AF

211

$58:1D收六分仪  无限收  直接报数量

WTT Softcore
My 1 :divine: for your 55 Awakened Sextants (always buying )
stock: 150+ :divine:
IGN: Stackoverflow_AF

(ON SALE! 3c each if you buy more than 40)
