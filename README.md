# 3ds-bfnt-converter
更新：
觉醒的高清字库也已经制作完毕。
https://github.com/UndertaleAlphys/3ds-bfnt-converter/releases/download/bfnt_converter_Alpha_0.1/awakening.song.zip

3ds上的三作火纹一直没有真正高清化的中文文字。这与其字库文件的特殊性有关。其字库文件后缀为bfnt。bfnt文件不是如bcfnt/bffnt一般被3ds游戏广泛使用的文件格式，就目前而言仅有3ds火纹三部曲和

极少数游戏例如蒸汽世界(STEAMWORLD)使用，因而也没有现成的处理工具。目前唯一能部分处理bfnt的工具FEAT仅能导出低分辨率的纹理图，而对码表无能为力。

因此，我编写了一个简单的处理工具，该工具能够根据bfnt文件中的码表绘制高清的字体。

## 0. 前言 bfnt文件码表解析
bfnt中的所有数字均为低位存储，unsigned类型。

以下为绝对地址：

0x1A 该地址储存了bfnt文件中纹理的数量，i.e.最后生成的png数量，unsigned short类型，占2个字节。

0x22 该地址储存了bfnt文件中字符的数量， unsigned short类型，占2个字节。

0x30 码表的开始，之后每0x10字节都是一个字符

对于码表内每0x10个字符而言，以下为相对地址：

0x00 该地址开始的两个字节储存了字符的UNICODE编码

0x02 该地址开始的两个字节储存了字符属于哪个纹理，如为0，则属于第0个纹理。

0x04 该地址开始的两个字节储存了字符判定框的水平偏移值，记为x

0x06 该地址开始的两个字节储存了字符判定框的垂直偏移值，记为y

*原点(0, 0)为png最左上角，(x, y)为字符判定框左上角的坐标。

0x08 该地址开始的两个字节储存了字符判定框的宽度，记为length。

*无效字符：码表中，并非每个字符都有效，全部打印出来可能造成纹理被污染。

*根据目前的研究，无效字符的共同规律是length == 0x101

*if的无效字符还具有如下规律：0x0a（相对地址）与0x08（绝对地址）存储的值相等，但是回声并不具有以上规律。

0x0b 该地址开始的两个字节储存了字符判定框的高度，记为height。

## 1. 开始前的准备
a. 解包rom得到的.bfnt文件，.bfnt.lz文件可以用FEAT转为.bfnt

https://github.com/SciresM/FEAT/releases/download/1.4/FEAT.zip

b. 目标的字体文件

c. 打包好的bfnt-converter alpha 0.1

https://github.com/UndertaleAlphys/3ds-bfnt-converter/releases/download/bfnt_converter_Alpha_0.1/bfnt_png_converter_amd64_windows.zip

## 2. 了解bfnt-converter配置 Alpha 0.1

所有设置存储在data.txt中。

X_CENTERED : bool 强制水平居中，若无把握建议开启，对观感影响不大。

Y_CENTERED : bool 强制竖直居中，有些纹理（如if的标题大字库）使用竖直居中，其他则不使用。根据具体情况开启，强行开启可能导致字体不对齐。

STROKE_WIDTH: Optional[int] 字体粗细，设为None则代表默认，一般默认比1还要细。

FONT_NAME : str 字体文件路径，可以是绝对或相对。

*所有str类型变量不能含有#，若含有空格需要用英文双引号或者单引号扩起来。

FONT_SIZE ：int 字体大小。以16进制表示。

IN_DIR : str 输入文件夹，该文件夹中的所有.bfnt文件都会被处理。

OUT_DIR : str 输出文件夹，png纹理会生成在该文件夹，若有重名则自动在文件名后面加上2。

TEST : bool 开启后会生成辅助测试的红框。

## 3. 生成字库的一般流程 Alpha 0.1

a. 将TEST设为True，拷贝字体路径填入FONT_NAME，将bfnt文件放入input文件夹，设定好FONT_SIZE，运行main.exe生成png。

b. 从生成的png里，找出自己需要的。为了方便，可以编写批处理文件重命名（我写好了if和回声的），若太小就增大字体再尝试，若太大就减小字体再尝试，直到文字与红框上部紧密贴合，记下此时的字体大小
并暂时保存该文件，将其余文件删除。每张png每个字体都有适合的字库大小，可以多尝试几次。

c. 等每张png都找到合适大小时，将生成的文件拖入citra的自定义纹理文件夹，运行试一试，有些问题可以在实测中发现，例如if的标题字库，必须采用垂直居中才能避免显示错误。

d. 等到所有设置都准确无误后，将TEST设定为False，重新生成每张png，大功告成！

效果：
![4](https://github.com/UndertaleAlphys/3ds-bfnt-converter/assets/90361250/73ff9853-ba50-4f76-8238-1e49ca19f1ad)
## 4. 本程序的一些缺陷 Alpha 0.1
a. 没能实现图形化界面，没有为每个纹理分别配置设置，操作较为繁琐

b. 其实同一个纹理的不同字符也可以有不同设置，例如同一个纹理中的中文为一个字体，字母数字则为另一个字体。本程序没能实现这一点。

以上，期待某位大佬能在路过时看一眼我的代码，改进完成。

## 5. 成品下载：
IF明尚体4x：

https://github.com/UndertaleAlphys/3ds-bfnt-converter/releases/download/bfnt_converter_Alpha_0.1/if.zip

回声雅黑4x：

https://github.com/UndertaleAlphys/3ds-bfnt-converter/releases/download/bfnt_converter_Alpha_0.1/echoes.zip
