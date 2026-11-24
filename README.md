# 大象的口袋海 · 立体绘本

一本会动的毛毡立体书：8 个跨页、5 个场景（沙滩、山路、山坡、圆屋里、池塘边）。拖动书页翻页，小象豆豆和小羊毛毛按脚本在书页上表演、对话，底部进度条显示每页的表演进度。

在线阅读：https://chatyu12.github.io/elephant-pocket-sea-popup-book/ （网址后加 `#p1`–`#p8` 可直达某页）

- `index.html`：three.js 立体书页面
- `art/*.webp`：角色和场景拆件（原始资产图裁切压缩 + SVG 预渲染）
- `art/svg/`：新增场景的毛毡风 SVG 源文件
- `tools/gen_svg.py`：生成这些 SVG 的脚本
- `SCRIPT.md`：互动脚本（每页的动作节拍和台词）
