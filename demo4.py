from PIL import Image, ImageDraw, ImageFont, ImageEnhance
from enum import Enum

#升级内容
#字体样式控制
#描边颜色控制
#间距控制：标题和正文之间的间距，正文行间距倍数
class TextAlign(Enum):
    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"


def create_styled_text_image(
        background_path,
        title,
        content_lines,
        output_path="output.jpg",
        # 字体设置
        title_font_path="simhei.ttf",  # 标题字体文件路径
        content_font_path="simhei.ttf",  # 正文字体文件路径
        title_font_size=80,
        content_font_size=40,
        # 颜色设置
        title_color=(255, 255, 255),
        content_color=(255, 255, 0),
        title_stroke_color=(0, 0, 0, 255),  # 标题描边颜色
        content_stroke_color=(0, 0, 0, 255),  # 正文描边颜色
        # 描边设置
        title_stroke_width=3,
        content_stroke_width=2,
        # 对齐设置
        title_align=TextAlign.CENTER,
        content_align=TextAlign.LEFT,
        # 边距设置
        margin_left=50,
        margin_right=50,
        # 间距设置
        title_content_spacing=50,  # 标题和正文之间的间距
        content_line_spacing=1.5  # 正文行间距倍数
):
    """
    创建带有设计感的图文，支持更多自定义选项

    新增参数:
    title_font_path: 标题字体文件路径
    content_font_path: 正文字体文件路径
    title_stroke_color: 标题描边颜色 (R,G,B,A)
    content_stroke_color: 正文描边颜色 (R,G,B,A)
    title_content_spacing: 标题和正文之间的间距
    content_line_spacing: 正文行间距倍数
    """
    try:
        background = Image.open(background_path).convert('RGBA')
        enhancer = ImageEnhance.Contrast(background)
        background = enhancer.enhance(1.2)
    except Exception as e:
        print(f"无法打开背景图片: {e}")
        return

    txt = Image.new('RGBA', background.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(txt)

    try:
        title_font = ImageFont.truetype(title_font_path, title_font_size)
        content_font = ImageFont.truetype(content_font_path, content_font_size)
    except Exception as e:
        print(f"无法加载字体: {e}")
        return

    width, height = background.size

    # 绘制标题
    title_y = height // 6
    draw_styled_text(
        draw=draw,
        text=title,
        font=title_font,
        position_y=title_y,
        image_width=width,
        text_color=title_color,
        align=title_align,
        margin_left=margin_left,
        margin_right=margin_right,
        stroke_width=title_stroke_width,
        stroke_color=title_stroke_color
    )

    # 计算正文起始位置（考虑标题和正文间距）
    content_y = title_y + title_font_size + title_content_spacing

    # 计算正文行间距
    line_spacing = content_font_size * content_line_spacing

    # 绘制正文
    for line in content_lines:
        if line.strip():  # 如果不是空行
            content_y = draw_styled_text(
                draw=draw,
                text=line,
                font=content_font,
                position_y=content_y,
                image_width=width,
                text_color=content_color,
                align=content_align,
                margin_left=margin_left,
                margin_right=margin_right,
                stroke_width=content_stroke_width,
                stroke_color=content_stroke_color
            )
        content_y += line_spacing

    # 合并图层并保存
    out = Image.alpha_composite(background, txt)
    out = out.convert('RGB')
    try:
        out.save(output_path, quality=95)
        print(f"图片已保存至: {output_path}")
    except Exception as e:
        print(f"保存图片时出错: {e}")


def draw_styled_text(
        draw,
        text,
        font,
        position_y,
        image_width,
        text_color=(255, 255, 255),
        align=TextAlign.CENTER,
        margin_left=50,
        margin_right=50,
        stroke_width=3,
        stroke_color=(0, 0, 0, 255)
):
    """绘制带样式的文本"""
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]

    # 计算有效绘制区域宽度
    available_width = image_width - margin_left - margin_right

    # 根据对齐方式计算x坐标
    if align == TextAlign.LEFT:
        text_x = margin_left
    elif align == TextAlign.CENTER:
        text_x = margin_left + (available_width - text_width) // 2
    else:  # RIGHT
        text_x = image_width - margin_right - text_width

    # 绘制描边
    if stroke_width > 0:
        for offset_x in range(-stroke_width, stroke_width + 1):
            for offset_y in range(-stroke_width, stroke_width + 1):
                draw.text(
                    (text_x + offset_x, position_y + offset_y),
                    text,
                    font=font,
                    fill=stroke_color
                )

    # 绘制主文本
    draw.text(
        (text_x, position_y),
        text,
        font=font,
        fill=text_color
    )

    return position_y


# 使用示例
if __name__ == "__main__":
    title = "你的人生取决于当下"
    content_lines = [
        '活在"如果怎样怎样"之类的假设之中',
        '就根本无法改变',
        '',  # 空行示例
        '你只想活在',
        '"如果有时间我也可以"',
        '"只要环境具备我也可以"',
        '"自己有这种才能"之类的可能性中',
        '或许再过5年或10年',
        '你又会开始使用',
        '"不再年轻""已有家庭"之类的借口'
    ]


    # 示例2：自定义样式
    create_styled_text_image(
        background_path="people.jpg",
        title=title,
        content_lines=content_lines,
        output_path="custom_styled_output.jpg",
        # 字体设置
        title_font_path="msyh.ttc",  # 微软雅黑字体
        content_font_path="simkai.ttf",  # 楷体字体
        title_font_size=280,
        content_font_size=180,
        # 颜色设置
        title_color=(0, 0, 0),  # 淡黄色标题
        content_color=(255,215,0),  # 淡绿色正文
        title_stroke_color=(255, 255, 255),  # 深蓝色描边
        content_stroke_color=(0, 0, 0),  # 深红色描边
        # 描边设置
        title_stroke_width=15,
        content_stroke_width=8,
        # 对齐设置
        title_align=TextAlign.LEFT,
        content_align=TextAlign.LEFT,
        # 边距设置
        margin_left=80,
        margin_right=80,
        # 间距设置
        title_content_spacing=400,  # 标题和正文间距加大
        content_line_spacing=1.0  # 正文行间距加大
    )